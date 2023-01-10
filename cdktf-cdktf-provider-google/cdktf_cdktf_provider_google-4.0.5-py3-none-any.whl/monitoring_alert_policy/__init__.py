'''
# `google_monitoring_alert_policy`

Refer to the Terraform Registory for docs: [`google_monitoring_alert_policy`](https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy).
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


class MonitoringAlertPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicy",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy google_monitoring_alert_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        combiner: builtins.str,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitoringAlertPolicyConditions", typing.Dict[builtins.str, typing.Any]]]],
        display_name: builtins.str,
        alert_strategy: typing.Optional[typing.Union["MonitoringAlertPolicyAlertStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        documentation: typing.Optional[typing.Union["MonitoringAlertPolicyDocumentation", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MonitoringAlertPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy google_monitoring_alert_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param combiner: How to combine the results of multiple conditions to determine if an incident should be opened. Possible values: ["AND", "OR", "AND_WITH_MATCHING_RESOURCE"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#combiner MonitoringAlertPolicy#combiner}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#conditions MonitoringAlertPolicy#conditions}
        :param display_name: A short name or phrase used to identify the policy in dashboards, notifications, and incidents. To avoid confusion, don't use the same display name for multiple policies in the same project. The name is limited to 512 Unicode characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#display_name MonitoringAlertPolicy#display_name}
        :param alert_strategy: alert_strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#alert_strategy MonitoringAlertPolicy#alert_strategy}
        :param documentation: documentation block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#documentation MonitoringAlertPolicy#documentation}
        :param enabled: Whether or not the policy is enabled. The default is true. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#enabled MonitoringAlertPolicy#enabled}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#id MonitoringAlertPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_channels: Identifies the notification channels to which notifications should be sent when incidents are opened or closed or when new violations occur on an already opened incident. Each element of this array corresponds to the name field in each of the NotificationChannel objects that are returned from the notificationChannels.list method. The syntax of the entries in this field is 'projects/[PROJECT_ID]/notificationChannels/[CHANNEL_ID]' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#notification_channels MonitoringAlertPolicy#notification_channels}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#project MonitoringAlertPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#timeouts MonitoringAlertPolicy#timeouts}
        :param user_labels: This field is intended to be used for organizing and identifying the AlertPolicy objects.The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#user_labels MonitoringAlertPolicy#user_labels}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4dede7ed28781086f3815ef1819ea5dd0b5fd4d8e952fd9448b8d887f5e4f49)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitoringAlertPolicyConfig(
            combiner=combiner,
            conditions=conditions,
            display_name=display_name,
            alert_strategy=alert_strategy,
            documentation=documentation,
            enabled=enabled,
            id=id,
            notification_channels=notification_channels,
            project=project,
            timeouts=timeouts,
            user_labels=user_labels,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAlertStrategy")
    def put_alert_strategy(
        self,
        *,
        auto_close: typing.Optional[builtins.str] = None,
        notification_rate_limit: typing.Optional[typing.Union["MonitoringAlertPolicyAlertStrategyNotificationRateLimit", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_close: If an alert policy that was active has no data for this long, any open incidents will close. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#auto_close MonitoringAlertPolicy#auto_close}
        :param notification_rate_limit: notification_rate_limit block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#notification_rate_limit MonitoringAlertPolicy#notification_rate_limit}
        '''
        value = MonitoringAlertPolicyAlertStrategy(
            auto_close=auto_close, notification_rate_limit=notification_rate_limit
        )

        return typing.cast(None, jsii.invoke(self, "putAlertStrategy", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitoringAlertPolicyConditions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60514aecb51156ded1a1b39649b9320636c74f0ce412890e6ed36902e3fd78f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putDocumentation")
    def put_documentation(
        self,
        *,
        content: typing.Optional[builtins.str] = None,
        mime_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: The text of the documentation, interpreted according to mimeType. The content may not exceed 8,192 Unicode characters and may not exceed more than 10,240 bytes when encoded in UTF-8 format, whichever is smaller. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#content MonitoringAlertPolicy#content}
        :param mime_type: The format of the content field. Presently, only the value "text/markdown" is supported. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#mime_type MonitoringAlertPolicy#mime_type}
        '''
        value = MonitoringAlertPolicyDocumentation(
            content=content, mime_type=mime_type
        )

        return typing.cast(None, jsii.invoke(self, "putDocumentation", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#create MonitoringAlertPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#delete MonitoringAlertPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#update MonitoringAlertPolicy#update}.
        '''
        value = MonitoringAlertPolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAlertStrategy")
    def reset_alert_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertStrategy", []))

    @jsii.member(jsii_name="resetDocumentation")
    def reset_documentation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentation", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotificationChannels")
    def reset_notification_channels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationChannels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserLabels")
    def reset_user_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserLabels", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="alertStrategy")
    def alert_strategy(self) -> "MonitoringAlertPolicyAlertStrategyOutputReference":
        return typing.cast("MonitoringAlertPolicyAlertStrategyOutputReference", jsii.get(self, "alertStrategy"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "MonitoringAlertPolicyConditionsList":
        return typing.cast("MonitoringAlertPolicyConditionsList", jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="creationRecord")
    def creation_record(self) -> "MonitoringAlertPolicyCreationRecordList":
        return typing.cast("MonitoringAlertPolicyCreationRecordList", jsii.get(self, "creationRecord"))

    @builtins.property
    @jsii.member(jsii_name="documentation")
    def documentation(self) -> "MonitoringAlertPolicyDocumentationOutputReference":
        return typing.cast("MonitoringAlertPolicyDocumentationOutputReference", jsii.get(self, "documentation"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitoringAlertPolicyTimeoutsOutputReference":
        return typing.cast("MonitoringAlertPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="alertStrategyInput")
    def alert_strategy_input(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyAlertStrategy"]:
        return typing.cast(typing.Optional["MonitoringAlertPolicyAlertStrategy"], jsii.get(self, "alertStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="combinerInput")
    def combiner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "combinerInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringAlertPolicyConditions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringAlertPolicyConditions"]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="documentationInput")
    def documentation_input(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyDocumentation"]:
        return typing.cast(typing.Optional["MonitoringAlertPolicyDocumentation"], jsii.get(self, "documentationInput"))

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
    @jsii.member(jsii_name="notificationChannelsInput")
    def notification_channels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationChannelsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MonitoringAlertPolicyTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MonitoringAlertPolicyTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userLabelsInput")
    def user_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "userLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="combiner")
    def combiner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "combiner"))

    @combiner.setter
    def combiner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3d392318d0d33693652f53d055be463faeb5d128d51dfe9c977a935fe782c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "combiner", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66032d2a474eb481c11569f23ddfca35a10c4a8f13d78ca04cec5ea10af0b94e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__847e820255288b77ff7df41d441ec46a9340b81fcf37e91441e276e17d2b5b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a3376a4aa0e22273583e080b4686065efd0f482d070fc24fb429c2a12fc971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="notificationChannels")
    def notification_channels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notificationChannels"))

    @notification_channels.setter
    def notification_channels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34425d599d535b622470828a517aeecc8523b87a3f3c12556ecaf4cdc64352a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationChannels", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db54bced32ba987482bd15f4da7f4e0ee59bfb9c60f2f9707f69eb455bb7cb36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="userLabels")
    def user_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "userLabels"))

    @user_labels.setter
    def user_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73684cff2b7b8cae8822a5f3fbe4d40e5377280360c5d854da900712c192b23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userLabels", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyAlertStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "auto_close": "autoClose",
        "notification_rate_limit": "notificationRateLimit",
    },
)
class MonitoringAlertPolicyAlertStrategy:
    def __init__(
        self,
        *,
        auto_close: typing.Optional[builtins.str] = None,
        notification_rate_limit: typing.Optional[typing.Union["MonitoringAlertPolicyAlertStrategyNotificationRateLimit", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_close: If an alert policy that was active has no data for this long, any open incidents will close. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#auto_close MonitoringAlertPolicy#auto_close}
        :param notification_rate_limit: notification_rate_limit block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#notification_rate_limit MonitoringAlertPolicy#notification_rate_limit}
        '''
        if isinstance(notification_rate_limit, dict):
            notification_rate_limit = MonitoringAlertPolicyAlertStrategyNotificationRateLimit(**notification_rate_limit)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2364dbbe9665488b8e2e79e86ec303a1b1c70ef470ef8efebcb6896f887158d8)
            check_type(argname="argument auto_close", value=auto_close, expected_type=type_hints["auto_close"])
            check_type(argname="argument notification_rate_limit", value=notification_rate_limit, expected_type=type_hints["notification_rate_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_close is not None:
            self._values["auto_close"] = auto_close
        if notification_rate_limit is not None:
            self._values["notification_rate_limit"] = notification_rate_limit

    @builtins.property
    def auto_close(self) -> typing.Optional[builtins.str]:
        '''If an alert policy that was active has no data for this long, any open incidents will close.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#auto_close MonitoringAlertPolicy#auto_close}
        '''
        result = self._values.get("auto_close")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_rate_limit(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyAlertStrategyNotificationRateLimit"]:
        '''notification_rate_limit block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#notification_rate_limit MonitoringAlertPolicy#notification_rate_limit}
        '''
        result = self._values.get("notification_rate_limit")
        return typing.cast(typing.Optional["MonitoringAlertPolicyAlertStrategyNotificationRateLimit"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyAlertStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyAlertStrategyNotificationRateLimit",
    jsii_struct_bases=[],
    name_mapping={"period": "period"},
)
class MonitoringAlertPolicyAlertStrategyNotificationRateLimit:
    def __init__(self, *, period: typing.Optional[builtins.str] = None) -> None:
        '''
        :param period: Not more than one notification per period. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#period MonitoringAlertPolicy#period}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__084f3c444b7a690363c4356877bebe5ebc426259fcfb7ad3943703c9ab0c9f50)
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if period is not None:
            self._values["period"] = period

    @builtins.property
    def period(self) -> typing.Optional[builtins.str]:
        '''Not more than one notification per period.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#period MonitoringAlertPolicy#period}
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyAlertStrategyNotificationRateLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyAlertStrategyNotificationRateLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyAlertStrategyNotificationRateLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c89046ec4f094dfa079409286539dd01b9df4abcf05e7ca0726998c85af1e9f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPeriod")
    def reset_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriod", []))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "period"))

    @period.setter
    def period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0bfe0944af6b9c6afb2cd637d7685f3c07ccafba310cc016b68bfc2e5f65ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyAlertStrategyNotificationRateLimit]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyAlertStrategyNotificationRateLimit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringAlertPolicyAlertStrategyNotificationRateLimit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc77428c39cc354ce33fe4b030e7396cd31627aaf3af64d5fb0d9c2bc899fb46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitoringAlertPolicyAlertStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyAlertStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4d3abe12bab58bb47709a209a09d622af39a0cd6bea9b1e8e195b263175535c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNotificationRateLimit")
    def put_notification_rate_limit(
        self,
        *,
        period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param period: Not more than one notification per period. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#period MonitoringAlertPolicy#period}
        '''
        value = MonitoringAlertPolicyAlertStrategyNotificationRateLimit(period=period)

        return typing.cast(None, jsii.invoke(self, "putNotificationRateLimit", [value]))

    @jsii.member(jsii_name="resetAutoClose")
    def reset_auto_close(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoClose", []))

    @jsii.member(jsii_name="resetNotificationRateLimit")
    def reset_notification_rate_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationRateLimit", []))

    @builtins.property
    @jsii.member(jsii_name="notificationRateLimit")
    def notification_rate_limit(
        self,
    ) -> MonitoringAlertPolicyAlertStrategyNotificationRateLimitOutputReference:
        return typing.cast(MonitoringAlertPolicyAlertStrategyNotificationRateLimitOutputReference, jsii.get(self, "notificationRateLimit"))

    @builtins.property
    @jsii.member(jsii_name="autoCloseInput")
    def auto_close_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoCloseInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationRateLimitInput")
    def notification_rate_limit_input(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyAlertStrategyNotificationRateLimit]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyAlertStrategyNotificationRateLimit], jsii.get(self, "notificationRateLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="autoClose")
    def auto_close(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoClose"))

    @auto_close.setter
    def auto_close(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3999bc002b969b9c7dd78dcef689eab1b1cc83f807299e30ed128ba88ce47cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoClose", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitoringAlertPolicyAlertStrategy]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyAlertStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringAlertPolicyAlertStrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c11b78d9b760098f3a9af7bd61abe074871305e29c82a0680c203781dca16bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditions",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "condition_absent": "conditionAbsent",
        "condition_matched_log": "conditionMatchedLog",
        "condition_monitoring_query_language": "conditionMonitoringQueryLanguage",
        "condition_threshold": "conditionThreshold",
    },
)
class MonitoringAlertPolicyConditions:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        condition_absent: typing.Optional[typing.Union["MonitoringAlertPolicyConditionsConditionAbsent", typing.Dict[builtins.str, typing.Any]]] = None,
        condition_matched_log: typing.Optional[typing.Union["MonitoringAlertPolicyConditionsConditionMatchedLog", typing.Dict[builtins.str, typing.Any]]] = None,
        condition_monitoring_query_language: typing.Optional[typing.Union["MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage", typing.Dict[builtins.str, typing.Any]]] = None,
        condition_threshold: typing.Optional[typing.Union["MonitoringAlertPolicyConditionsConditionThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param display_name: A short name or phrase used to identify the condition in dashboards, notifications, and incidents. To avoid confusion, don't use the same display name for multiple conditions in the same policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#display_name MonitoringAlertPolicy#display_name}
        :param condition_absent: condition_absent block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#condition_absent MonitoringAlertPolicy#condition_absent}
        :param condition_matched_log: condition_matched_log block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#condition_matched_log MonitoringAlertPolicy#condition_matched_log}
        :param condition_monitoring_query_language: condition_monitoring_query_language block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#condition_monitoring_query_language MonitoringAlertPolicy#condition_monitoring_query_language}
        :param condition_threshold: condition_threshold block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#condition_threshold MonitoringAlertPolicy#condition_threshold}
        '''
        if isinstance(condition_absent, dict):
            condition_absent = MonitoringAlertPolicyConditionsConditionAbsent(**condition_absent)
        if isinstance(condition_matched_log, dict):
            condition_matched_log = MonitoringAlertPolicyConditionsConditionMatchedLog(**condition_matched_log)
        if isinstance(condition_monitoring_query_language, dict):
            condition_monitoring_query_language = MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage(**condition_monitoring_query_language)
        if isinstance(condition_threshold, dict):
            condition_threshold = MonitoringAlertPolicyConditionsConditionThreshold(**condition_threshold)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4161648379b85387e461783e402b170bf33dd7551ae25e82adb3d0b8db2a340)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument condition_absent", value=condition_absent, expected_type=type_hints["condition_absent"])
            check_type(argname="argument condition_matched_log", value=condition_matched_log, expected_type=type_hints["condition_matched_log"])
            check_type(argname="argument condition_monitoring_query_language", value=condition_monitoring_query_language, expected_type=type_hints["condition_monitoring_query_language"])
            check_type(argname="argument condition_threshold", value=condition_threshold, expected_type=type_hints["condition_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
        }
        if condition_absent is not None:
            self._values["condition_absent"] = condition_absent
        if condition_matched_log is not None:
            self._values["condition_matched_log"] = condition_matched_log
        if condition_monitoring_query_language is not None:
            self._values["condition_monitoring_query_language"] = condition_monitoring_query_language
        if condition_threshold is not None:
            self._values["condition_threshold"] = condition_threshold

    @builtins.property
    def display_name(self) -> builtins.str:
        '''A short name or phrase used to identify the condition in dashboards, notifications, and incidents.

        To avoid confusion, don't use the same
        display name for multiple conditions in the same
        policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#display_name MonitoringAlertPolicy#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition_absent(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyConditionsConditionAbsent"]:
        '''condition_absent block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#condition_absent MonitoringAlertPolicy#condition_absent}
        '''
        result = self._values.get("condition_absent")
        return typing.cast(typing.Optional["MonitoringAlertPolicyConditionsConditionAbsent"], result)

    @builtins.property
    def condition_matched_log(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyConditionsConditionMatchedLog"]:
        '''condition_matched_log block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#condition_matched_log MonitoringAlertPolicy#condition_matched_log}
        '''
        result = self._values.get("condition_matched_log")
        return typing.cast(typing.Optional["MonitoringAlertPolicyConditionsConditionMatchedLog"], result)

    @builtins.property
    def condition_monitoring_query_language(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage"]:
        '''condition_monitoring_query_language block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#condition_monitoring_query_language MonitoringAlertPolicy#condition_monitoring_query_language}
        '''
        result = self._values.get("condition_monitoring_query_language")
        return typing.cast(typing.Optional["MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage"], result)

    @builtins.property
    def condition_threshold(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyConditionsConditionThreshold"]:
        '''condition_threshold block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#condition_threshold MonitoringAlertPolicy#condition_threshold}
        '''
        result = self._values.get("condition_threshold")
        return typing.cast(typing.Optional["MonitoringAlertPolicyConditionsConditionThreshold"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionAbsent",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "aggregations": "aggregations",
        "filter": "filter",
        "trigger": "trigger",
    },
)
class MonitoringAlertPolicyConditionsConditionAbsent:
    def __init__(
        self,
        *,
        duration: builtins.str,
        aggregations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitoringAlertPolicyConditionsConditionAbsentAggregations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        filter: typing.Optional[builtins.str] = None,
        trigger: typing.Optional[typing.Union["MonitoringAlertPolicyConditionsConditionAbsentTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param duration: The amount of time that a time series must fail to report new data to be considered failing. Currently, only values that are a multiple of a minute--e.g. 60s, 120s, or 300s --are supported. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#duration MonitoringAlertPolicy#duration}
        :param aggregations: aggregations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#aggregations MonitoringAlertPolicy#aggregations}
        :param filter: A filter that identifies which time series should be compared with the threshold.The filter is similar to the one that is specified in the MetricService.ListTimeSeries request (that call is useful to verify the time series that will be retrieved / processed) and must specify the metric type and optionally may contain restrictions on resource type, resource labels, and metric labels. This field may not exceed 2048 Unicode characters in length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#filter MonitoringAlertPolicy#filter}
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#trigger MonitoringAlertPolicy#trigger}
        '''
        if isinstance(trigger, dict):
            trigger = MonitoringAlertPolicyConditionsConditionAbsentTrigger(**trigger)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409a36add30e1115098721c7644e970fe0638bdd8d6e3cb7aaacb11e1765f90e)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument aggregations", value=aggregations, expected_type=type_hints["aggregations"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration": duration,
        }
        if aggregations is not None:
            self._values["aggregations"] = aggregations
        if filter is not None:
            self._values["filter"] = filter
        if trigger is not None:
            self._values["trigger"] = trigger

    @builtins.property
    def duration(self) -> builtins.str:
        '''The amount of time that a time series must fail to report new data to be considered failing.

        Currently, only values that are a
        multiple of a minute--e.g. 60s, 120s, or 300s
        --are supported.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#duration MonitoringAlertPolicy#duration}
        '''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aggregations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringAlertPolicyConditionsConditionAbsentAggregations"]]]:
        '''aggregations block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#aggregations MonitoringAlertPolicy#aggregations}
        '''
        result = self._values.get("aggregations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringAlertPolicyConditionsConditionAbsentAggregations"]]], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''A filter that identifies which time series should be compared with the threshold.The filter is similar to the one that is specified in the MetricService.ListTimeSeries request (that call is useful to verify the time series that will be retrieved / processed) and must specify the metric type and optionally may contain restrictions on resource type, resource labels, and metric labels. This field may not exceed 2048 Unicode characters in length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#filter MonitoringAlertPolicy#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyConditionsConditionAbsentTrigger"]:
        '''trigger block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#trigger MonitoringAlertPolicy#trigger}
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional["MonitoringAlertPolicyConditionsConditionAbsentTrigger"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConditionsConditionAbsent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionAbsentAggregations",
    jsii_struct_bases=[],
    name_mapping={
        "alignment_period": "alignmentPeriod",
        "cross_series_reducer": "crossSeriesReducer",
        "group_by_fields": "groupByFields",
        "per_series_aligner": "perSeriesAligner",
    },
)
class MonitoringAlertPolicyConditionsConditionAbsentAggregations:
    def __init__(
        self,
        *,
        alignment_period: typing.Optional[builtins.str] = None,
        cross_series_reducer: typing.Optional[builtins.str] = None,
        group_by_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        per_series_aligner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alignment_period: The alignment period for per-time series alignment. If present, alignmentPeriod must be at least 60 seconds. After per-time series alignment, each time series will contain data points only on the period boundaries. If perSeriesAligner is not specified or equals ALIGN_NONE, then this field is ignored. If perSeriesAligner is specified and does not equal ALIGN_NONE, then this field must be defined; otherwise an error is returned. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#alignment_period MonitoringAlertPolicy#alignment_period}
        :param cross_series_reducer: The approach to be used to combine time series. Not all reducer functions may be applied to all time series, depending on the metric type and the value type of the original time series. Reduction may change the metric type of value type of the time series.Time series data must be aligned in order to perform cross- time series reduction. If crossSeriesReducer is specified, then perSeriesAligner must be specified and not equal ALIGN_NONE and alignmentPeriod must be specified; otherwise, an error is returned. Possible values: ["REDUCE_NONE", "REDUCE_MEAN", "REDUCE_MIN", "REDUCE_MAX", "REDUCE_SUM", "REDUCE_STDDEV", "REDUCE_COUNT", "REDUCE_COUNT_TRUE", "REDUCE_COUNT_FALSE", "REDUCE_FRACTION_TRUE", "REDUCE_PERCENTILE_99", "REDUCE_PERCENTILE_95", "REDUCE_PERCENTILE_50", "REDUCE_PERCENTILE_05"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#cross_series_reducer MonitoringAlertPolicy#cross_series_reducer}
        :param group_by_fields: The set of fields to preserve when crossSeriesReducer is specified. The groupByFields determine how the time series are partitioned into subsets prior to applying the aggregation function. Each subset contains time series that have the same value for each of the grouping fields. Each individual time series is a member of exactly one subset. The crossSeriesReducer is applied to each subset of time series. It is not possible to reduce across different resource types, so this field implicitly contains resource.type. Fields not specified in groupByFields are aggregated away. If groupByFields is not specified and all the time series have the same resource type, then the time series are aggregated into a single output time series. If crossSeriesReducer is not defined, this field is ignored. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#group_by_fields MonitoringAlertPolicy#group_by_fields}
        :param per_series_aligner: The approach to be used to align individual time series. Not all alignment functions may be applied to all time series, depending on the metric type and value type of the original time series. Alignment may change the metric type or the value type of the time series.Time series data must be aligned in order to perform cross- time series reduction. If crossSeriesReducer is specified, then perSeriesAligner must be specified and not equal ALIGN_NONE and alignmentPeriod must be specified; otherwise, an error is returned. Possible values: ["ALIGN_NONE", "ALIGN_DELTA", "ALIGN_RATE", "ALIGN_INTERPOLATE", "ALIGN_NEXT_OLDER", "ALIGN_MIN", "ALIGN_MAX", "ALIGN_MEAN", "ALIGN_COUNT", "ALIGN_SUM", "ALIGN_STDDEV", "ALIGN_COUNT_TRUE", "ALIGN_COUNT_FALSE", "ALIGN_FRACTION_TRUE", "ALIGN_PERCENTILE_99", "ALIGN_PERCENTILE_95", "ALIGN_PERCENTILE_50", "ALIGN_PERCENTILE_05", "ALIGN_PERCENT_CHANGE"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#per_series_aligner MonitoringAlertPolicy#per_series_aligner}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3e08d55a94fa994436873c2070762ab9690de187fc1a7774a3dcd84252d1d6)
            check_type(argname="argument alignment_period", value=alignment_period, expected_type=type_hints["alignment_period"])
            check_type(argname="argument cross_series_reducer", value=cross_series_reducer, expected_type=type_hints["cross_series_reducer"])
            check_type(argname="argument group_by_fields", value=group_by_fields, expected_type=type_hints["group_by_fields"])
            check_type(argname="argument per_series_aligner", value=per_series_aligner, expected_type=type_hints["per_series_aligner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alignment_period is not None:
            self._values["alignment_period"] = alignment_period
        if cross_series_reducer is not None:
            self._values["cross_series_reducer"] = cross_series_reducer
        if group_by_fields is not None:
            self._values["group_by_fields"] = group_by_fields
        if per_series_aligner is not None:
            self._values["per_series_aligner"] = per_series_aligner

    @builtins.property
    def alignment_period(self) -> typing.Optional[builtins.str]:
        '''The alignment period for per-time series alignment.

        If present,
        alignmentPeriod must be at least
        60 seconds. After per-time series
        alignment, each time series will
        contain data points only on the
        period boundaries. If
        perSeriesAligner is not specified
        or equals ALIGN_NONE, then this
        field is ignored. If
        perSeriesAligner is specified and
        does not equal ALIGN_NONE, then
        this field must be defined;
        otherwise an error is returned.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#alignment_period MonitoringAlertPolicy#alignment_period}
        '''
        result = self._values.get("alignment_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_series_reducer(self) -> typing.Optional[builtins.str]:
        '''The approach to be used to combine time series.

        Not all reducer
        functions may be applied to all
        time series, depending on the
        metric type and the value type of
        the original time series.
        Reduction may change the metric
        type of value type of the time
        series.Time series data must be
        aligned in order to perform cross-
        time series reduction. If
        crossSeriesReducer is specified,
        then perSeriesAligner must be
        specified and not equal ALIGN_NONE
        and alignmentPeriod must be
        specified; otherwise, an error is
        returned. Possible values: ["REDUCE_NONE", "REDUCE_MEAN", "REDUCE_MIN", "REDUCE_MAX", "REDUCE_SUM", "REDUCE_STDDEV", "REDUCE_COUNT", "REDUCE_COUNT_TRUE", "REDUCE_COUNT_FALSE", "REDUCE_FRACTION_TRUE", "REDUCE_PERCENTILE_99", "REDUCE_PERCENTILE_95", "REDUCE_PERCENTILE_50", "REDUCE_PERCENTILE_05"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#cross_series_reducer MonitoringAlertPolicy#cross_series_reducer}
        '''
        result = self._values.get("cross_series_reducer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_by_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of fields to preserve when crossSeriesReducer is specified.

        The groupByFields determine how
        the time series are partitioned
        into subsets prior to applying the
        aggregation function. Each subset
        contains time series that have the
        same value for each of the
        grouping fields. Each individual
        time series is a member of exactly
        one subset. The crossSeriesReducer
        is applied to each subset of time
        series. It is not possible to
        reduce across different resource
        types, so this field implicitly
        contains resource.type. Fields not
        specified in groupByFields are
        aggregated away. If groupByFields
        is not specified and all the time
        series have the same resource
        type, then the time series are
        aggregated into a single output
        time series. If crossSeriesReducer
        is not defined, this field is
        ignored.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#group_by_fields MonitoringAlertPolicy#group_by_fields}
        '''
        result = self._values.get("group_by_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def per_series_aligner(self) -> typing.Optional[builtins.str]:
        '''The approach to be used to align individual time series.

        Not all
        alignment functions may be applied
        to all time series, depending on
        the metric type and value type of
        the original time series.
        Alignment may change the metric
        type or the value type of the time
        series.Time series data must be
        aligned in order to perform cross-
        time series reduction. If
        crossSeriesReducer is specified,
        then perSeriesAligner must be
        specified and not equal ALIGN_NONE
        and alignmentPeriod must be
        specified; otherwise, an error is
        returned. Possible values: ["ALIGN_NONE", "ALIGN_DELTA", "ALIGN_RATE", "ALIGN_INTERPOLATE", "ALIGN_NEXT_OLDER", "ALIGN_MIN", "ALIGN_MAX", "ALIGN_MEAN", "ALIGN_COUNT", "ALIGN_SUM", "ALIGN_STDDEV", "ALIGN_COUNT_TRUE", "ALIGN_COUNT_FALSE", "ALIGN_FRACTION_TRUE", "ALIGN_PERCENTILE_99", "ALIGN_PERCENTILE_95", "ALIGN_PERCENTILE_50", "ALIGN_PERCENTILE_05", "ALIGN_PERCENT_CHANGE"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#per_series_aligner MonitoringAlertPolicy#per_series_aligner}
        '''
        result = self._values.get("per_series_aligner")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConditionsConditionAbsentAggregations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyConditionsConditionAbsentAggregationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionAbsentAggregationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69650333d52ba2eaac35b99e8a0807b6b03b0b944c9757114b908aaff1ad1d32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitoringAlertPolicyConditionsConditionAbsentAggregationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b8876f7e64011b41429f767f3b312b52de74f8a81182a462848bd343746620)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitoringAlertPolicyConditionsConditionAbsentAggregationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe01c79a8613eb51923c5d5130645682295cf969f6b7da779e3df5cf59a5a67d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef88bed33cf5178b939b838b08550edac0416543294d95adfe90476ff38b45e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9b80a6bc9dc38deab00050b79bd2adfd032202a1ad63b67e0d2947c942df8f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionAbsentAggregations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionAbsentAggregations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionAbsentAggregations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__251eb0995135cabd17d017b6758167b5d776b184011b9c7f617691af35bd203f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitoringAlertPolicyConditionsConditionAbsentAggregationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionAbsentAggregationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1f4598994dd29c29bef6559883765e53125524d308f52a95ad15cd123343647)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAlignmentPeriod")
    def reset_alignment_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlignmentPeriod", []))

    @jsii.member(jsii_name="resetCrossSeriesReducer")
    def reset_cross_series_reducer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossSeriesReducer", []))

    @jsii.member(jsii_name="resetGroupByFields")
    def reset_group_by_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupByFields", []))

    @jsii.member(jsii_name="resetPerSeriesAligner")
    def reset_per_series_aligner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerSeriesAligner", []))

    @builtins.property
    @jsii.member(jsii_name="alignmentPeriodInput")
    def alignment_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alignmentPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="crossSeriesReducerInput")
    def cross_series_reducer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossSeriesReducerInput"))

    @builtins.property
    @jsii.member(jsii_name="groupByFieldsInput")
    def group_by_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupByFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="perSeriesAlignerInput")
    def per_series_aligner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "perSeriesAlignerInput"))

    @builtins.property
    @jsii.member(jsii_name="alignmentPeriod")
    def alignment_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alignmentPeriod"))

    @alignment_period.setter
    def alignment_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__384479429fc2df813fc96021a73784630b80625c425f193210aa44d36549a215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alignmentPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="crossSeriesReducer")
    def cross_series_reducer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossSeriesReducer"))

    @cross_series_reducer.setter
    def cross_series_reducer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38b02ae75baa6983e3dac993770c13f54226493c639f04b1fb9f3aa5e4edc272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossSeriesReducer", value)

    @builtins.property
    @jsii.member(jsii_name="groupByFields")
    def group_by_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupByFields"))

    @group_by_fields.setter
    def group_by_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d03cb97f8448170d7a49c895d7a666615c7480752a25c0e906f6ce86360431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupByFields", value)

    @builtins.property
    @jsii.member(jsii_name="perSeriesAligner")
    def per_series_aligner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perSeriesAligner"))

    @per_series_aligner.setter
    def per_series_aligner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34723f6a20216852632235e8464e9a8f41173e741913048cdf69ea85388511dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perSeriesAligner", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionAbsentAggregations, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionAbsentAggregations, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionAbsentAggregations, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c712fd793c60616563e3decf83b759c1f9855221c74ad0077fd7cddb92e99be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitoringAlertPolicyConditionsConditionAbsentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionAbsentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7666d05aedd204214e08160cde0472bfc399378fac8c4d9135946c7682fee34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAggregations")
    def put_aggregations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionAbsentAggregations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee16bc44fb36fde89cc79567b88c0cf69b095bc6efdeb0c346dc24b566ff11ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAggregations", [value]))

    @jsii.member(jsii_name="putTrigger")
    def put_trigger(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: The absolute number of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#count MonitoringAlertPolicy#count}
        :param percent: The percentage of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#percent MonitoringAlertPolicy#percent}
        '''
        value = MonitoringAlertPolicyConditionsConditionAbsentTrigger(
            count=count, percent=percent
        )

        return typing.cast(None, jsii.invoke(self, "putTrigger", [value]))

    @jsii.member(jsii_name="resetAggregations")
    def reset_aggregations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregations", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetTrigger")
    def reset_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrigger", []))

    @builtins.property
    @jsii.member(jsii_name="aggregations")
    def aggregations(
        self,
    ) -> MonitoringAlertPolicyConditionsConditionAbsentAggregationsList:
        return typing.cast(MonitoringAlertPolicyConditionsConditionAbsentAggregationsList, jsii.get(self, "aggregations"))

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(
        self,
    ) -> "MonitoringAlertPolicyConditionsConditionAbsentTriggerOutputReference":
        return typing.cast("MonitoringAlertPolicyConditionsConditionAbsentTriggerOutputReference", jsii.get(self, "trigger"))

    @builtins.property
    @jsii.member(jsii_name="aggregationsInput")
    def aggregations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionAbsentAggregations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionAbsentAggregations]]], jsii.get(self, "aggregationsInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerInput")
    def trigger_input(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyConditionsConditionAbsentTrigger"]:
        return typing.cast(typing.Optional["MonitoringAlertPolicyConditionsConditionAbsentTrigger"], jsii.get(self, "triggerInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d874da3c1514b76bfd1d654aa28dbe4709a6787ca895e4dfda1d99cd34c162c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value)

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774f0252d30c2f665153febfffd6f020fb170cc828fdf94d0e233c6bc0f66311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyConditionsConditionAbsent]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyConditionsConditionAbsent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringAlertPolicyConditionsConditionAbsent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d72db521b454e002142e9e8af4ee9841faa733d3a06bf9483a54bb2e18b46fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionAbsentTrigger",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "percent": "percent"},
)
class MonitoringAlertPolicyConditionsConditionAbsentTrigger:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: The absolute number of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#count MonitoringAlertPolicy#count}
        :param percent: The percentage of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#percent MonitoringAlertPolicy#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a1f5daefceaa164a95b07da04c060fa9bf602d2c9b51882604cd470b93c0af)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument percent", value=percent, expected_type=type_hints["percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if percent is not None:
            self._values["percent"] = percent

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''The absolute number of time series that must fail the predicate for the condition to be triggered.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#count MonitoringAlertPolicy#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''The percentage of time series that must fail the predicate for the condition to be triggered.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#percent MonitoringAlertPolicy#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConditionsConditionAbsentTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyConditionsConditionAbsentTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionAbsentTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f328b46ac9aa1533a884a63e3d630e90fe2d206c48085b9e1684aad499f0d93b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetPercent")
    def reset_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercent", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="percentInput")
    def percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b2b5999c3d285ed7e4f8a376441d9fcfc9ed68c033bf782b4cceff68a1a82b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b0290ca17ad1a8441516f914b91107978584345172e936a1d468baaca53659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyConditionsConditionAbsentTrigger]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyConditionsConditionAbsentTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringAlertPolicyConditionsConditionAbsentTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177ea7ed71a8c2e9b61311ece52eb4d8d8aa7a6a46f71df1419a7d29b717e82b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionMatchedLog",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter", "label_extractors": "labelExtractors"},
)
class MonitoringAlertPolicyConditionsConditionMatchedLog:
    def __init__(
        self,
        *,
        filter: builtins.str,
        label_extractors: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param filter: A logs-based filter. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#filter MonitoringAlertPolicy#filter}
        :param label_extractors: A map from a label key to an extractor expression, which is used to extract the value for this label key. Each entry in this map is a specification for how data should be extracted from log entries that match filter. Each combination of extracted values is treated as a separate rule for the purposes of triggering notifications. Label keys and corresponding values can be used in notifications generated by this condition. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#label_extractors MonitoringAlertPolicy#label_extractors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe545dc7153670ced08e4e26d712983aa566e5e036a59f8aeb91ae2706721935)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument label_extractors", value=label_extractors, expected_type=type_hints["label_extractors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
        }
        if label_extractors is not None:
            self._values["label_extractors"] = label_extractors

    @builtins.property
    def filter(self) -> builtins.str:
        '''A logs-based filter.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#filter MonitoringAlertPolicy#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def label_extractors(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map from a label key to an extractor expression, which is used to extract the value for this label key.

        Each entry in this map is
        a specification for how data should be extracted from log entries that
        match filter. Each combination of extracted values is treated as
        a separate rule for the purposes of triggering notifications.
        Label keys and corresponding values can be used in notifications
        generated by this condition.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#label_extractors MonitoringAlertPolicy#label_extractors}
        '''
        result = self._values.get("label_extractors")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConditionsConditionMatchedLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyConditionsConditionMatchedLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionMatchedLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0fc8a2c7888fad38b1946597252a7ff69385c9859410c4f0146a9872c2c60fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLabelExtractors")
    def reset_label_extractors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabelExtractors", []))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="labelExtractorsInput")
    def label_extractors_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelExtractorsInput"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cf2a93548cf13298d1f5d153b9bf0639cce007fa847448c9d4f6958a49dc72d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value)

    @builtins.property
    @jsii.member(jsii_name="labelExtractors")
    def label_extractors(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labelExtractors"))

    @label_extractors.setter
    def label_extractors(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511c79a579cfcde5adbf7f64f59f4c92ee4e61dcff4a94681face990e7469452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelExtractors", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyConditionsConditionMatchedLog]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyConditionsConditionMatchedLog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringAlertPolicyConditionsConditionMatchedLog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630e65c564d1b7a5d75f99d4013e087f63fd45f9bbc3e253e64ae08b34a6e933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "query": "query",
        "evaluation_missing_data": "evaluationMissingData",
        "trigger": "trigger",
    },
)
class MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage:
    def __init__(
        self,
        *,
        duration: builtins.str,
        query: builtins.str,
        evaluation_missing_data: typing.Optional[builtins.str] = None,
        trigger: typing.Optional[typing.Union["MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param duration: The amount of time that a time series must violate the threshold to be considered failing. Currently, only values that are a multiple of a minute--e.g., 0, 60, 120, or 300 seconds--are supported. If an invalid value is given, an error will be returned. When choosing a duration, it is useful to keep in mind the frequency of the underlying time series data (which may also be affected by any alignments specified in the aggregations field); a good duration is long enough so that a single outlier does not generate spurious alerts, but short enough that unhealthy states are detected and alerted on quickly. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#duration MonitoringAlertPolicy#duration}
        :param query: Monitoring Query Language query that outputs a boolean stream. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#query MonitoringAlertPolicy#query}
        :param evaluation_missing_data: A condition control that determines how metric-threshold conditions are evaluated when data stops arriving. Possible values: ["EVALUATION_MISSING_DATA_INACTIVE", "EVALUATION_MISSING_DATA_ACTIVE", "EVALUATION_MISSING_DATA_NO_OP"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#evaluation_missing_data MonitoringAlertPolicy#evaluation_missing_data}
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#trigger MonitoringAlertPolicy#trigger}
        '''
        if isinstance(trigger, dict):
            trigger = MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger(**trigger)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2151750a297ba1c00c893ebdedc2bbe570100713d4337544d483afdcaff44897)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument evaluation_missing_data", value=evaluation_missing_data, expected_type=type_hints["evaluation_missing_data"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration": duration,
            "query": query,
        }
        if evaluation_missing_data is not None:
            self._values["evaluation_missing_data"] = evaluation_missing_data
        if trigger is not None:
            self._values["trigger"] = trigger

    @builtins.property
    def duration(self) -> builtins.str:
        '''The amount of time that a time series must violate the threshold to be considered failing.

        Currently, only values that are a
        multiple of a minute--e.g., 0, 60, 120, or
        300 seconds--are supported. If an invalid
        value is given, an error will be returned.
        When choosing a duration, it is useful to
        keep in mind the frequency of the underlying
        time series data (which may also be affected
        by any alignments specified in the
        aggregations field); a good duration is long
        enough so that a single outlier does not
        generate spurious alerts, but short enough
        that unhealthy states are detected and
        alerted on quickly.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#duration MonitoringAlertPolicy#duration}
        '''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''Monitoring Query Language query that outputs a boolean stream.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#query MonitoringAlertPolicy#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def evaluation_missing_data(self) -> typing.Optional[builtins.str]:
        '''A condition control that determines how metric-threshold conditions are evaluated when data stops arriving. Possible values: ["EVALUATION_MISSING_DATA_INACTIVE", "EVALUATION_MISSING_DATA_ACTIVE", "EVALUATION_MISSING_DATA_NO_OP"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#evaluation_missing_data MonitoringAlertPolicy#evaluation_missing_data}
        '''
        result = self._values.get("evaluation_missing_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger"]:
        '''trigger block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#trigger MonitoringAlertPolicy#trigger}
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional["MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a20c2869ffa7599836025eed635c71f62cc98e20c84174548462126ee3e6140f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTrigger")
    def put_trigger(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: The absolute number of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#count MonitoringAlertPolicy#count}
        :param percent: The percentage of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#percent MonitoringAlertPolicy#percent}
        '''
        value = MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger(
            count=count, percent=percent
        )

        return typing.cast(None, jsii.invoke(self, "putTrigger", [value]))

    @jsii.member(jsii_name="resetEvaluationMissingData")
    def reset_evaluation_missing_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationMissingData", []))

    @jsii.member(jsii_name="resetTrigger")
    def reset_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrigger", []))

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(
        self,
    ) -> "MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTriggerOutputReference":
        return typing.cast("MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTriggerOutputReference", jsii.get(self, "trigger"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationMissingDataInput")
    def evaluation_missing_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluationMissingDataInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerInput")
    def trigger_input(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger"]:
        return typing.cast(typing.Optional["MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger"], jsii.get(self, "triggerInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb946fe85d87cc98a2ef672d22f1437659daf8d46ba10e5aa83a188df51e7c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value)

    @builtins.property
    @jsii.member(jsii_name="evaluationMissingData")
    def evaluation_missing_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluationMissingData"))

    @evaluation_missing_data.setter
    def evaluation_missing_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66315cf97429cd49fb7a5e744127196e20b0231c1f89df022b0ae700f29fa601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMissingData", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe4e2adddf4b5570568a0305028f4471084f47ee924073aefd1f9a8f3fa6dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86dd8de4968a47c29e1bfb236a314b1f68f76957d190708de073d733d971953a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "percent": "percent"},
)
class MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: The absolute number of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#count MonitoringAlertPolicy#count}
        :param percent: The percentage of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#percent MonitoringAlertPolicy#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853a1c44faf1ca74bf50f298c7f09e1a7840360b9ba0cf14d597298bd8bd9a00)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument percent", value=percent, expected_type=type_hints["percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if percent is not None:
            self._values["percent"] = percent

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''The absolute number of time series that must fail the predicate for the condition to be triggered.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#count MonitoringAlertPolicy#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''The percentage of time series that must fail the predicate for the condition to be triggered.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#percent MonitoringAlertPolicy#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8945e528c29bf2719d541a51fa26e7cf97b31faf49209c44a1dd672d75a26ab2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetPercent")
    def reset_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercent", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="percentInput")
    def percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d267a71cd77825d8fe70a0f1ee05cb58719cd812b9ae80950a813cd7290368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5398a6f640e5488c8576d29160bc67077fc88b107820e0c0342f885a2ef02da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48e76021d20fe524d91397b405a71a101573c3281f0c14db7a9f88cbf4aade6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionThreshold",
    jsii_struct_bases=[],
    name_mapping={
        "comparison": "comparison",
        "duration": "duration",
        "aggregations": "aggregations",
        "denominator_aggregations": "denominatorAggregations",
        "denominator_filter": "denominatorFilter",
        "evaluation_missing_data": "evaluationMissingData",
        "filter": "filter",
        "threshold_value": "thresholdValue",
        "trigger": "trigger",
    },
)
class MonitoringAlertPolicyConditionsConditionThreshold:
    def __init__(
        self,
        *,
        comparison: builtins.str,
        duration: builtins.str,
        aggregations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitoringAlertPolicyConditionsConditionThresholdAggregations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        denominator_aggregations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        denominator_filter: typing.Optional[builtins.str] = None,
        evaluation_missing_data: typing.Optional[builtins.str] = None,
        filter: typing.Optional[builtins.str] = None,
        threshold_value: typing.Optional[jsii.Number] = None,
        trigger: typing.Optional[typing.Union["MonitoringAlertPolicyConditionsConditionThresholdTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param comparison: The comparison to apply between the time series (indicated by filter and aggregation) and the threshold (indicated by threshold_value). The comparison is applied on each time series, with the time series on the left-hand side and the threshold on the right-hand side. Only COMPARISON_LT and COMPARISON_GT are supported currently. Possible values: ["COMPARISON_GT", "COMPARISON_GE", "COMPARISON_LT", "COMPARISON_LE", "COMPARISON_EQ", "COMPARISON_NE"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#comparison MonitoringAlertPolicy#comparison}
        :param duration: The amount of time that a time series must violate the threshold to be considered failing. Currently, only values that are a multiple of a minute--e.g., 0, 60, 120, or 300 seconds--are supported. If an invalid value is given, an error will be returned. When choosing a duration, it is useful to keep in mind the frequency of the underlying time series data (which may also be affected by any alignments specified in the aggregations field); a good duration is long enough so that a single outlier does not generate spurious alerts, but short enough that unhealthy states are detected and alerted on quickly. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#duration MonitoringAlertPolicy#duration}
        :param aggregations: aggregations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#aggregations MonitoringAlertPolicy#aggregations}
        :param denominator_aggregations: denominator_aggregations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#denominator_aggregations MonitoringAlertPolicy#denominator_aggregations}
        :param denominator_filter: A filter that identifies a time series that should be used as the denominator of a ratio that will be compared with the threshold. If a denominator_filter is specified, the time series specified by the filter field will be used as the numerator.The filter is similar to the one that is specified in the MetricService.ListTimeSeries request (that call is useful to verify the time series that will be retrieved / processed) and must specify the metric type and optionally may contain restrictions on resource type, resource labels, and metric labels. This field may not exceed 2048 Unicode characters in length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#denominator_filter MonitoringAlertPolicy#denominator_filter}
        :param evaluation_missing_data: A condition control that determines how metric-threshold conditions are evaluated when data stops arriving. Possible values: ["EVALUATION_MISSING_DATA_INACTIVE", "EVALUATION_MISSING_DATA_ACTIVE", "EVALUATION_MISSING_DATA_NO_OP"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#evaluation_missing_data MonitoringAlertPolicy#evaluation_missing_data}
        :param filter: A filter that identifies which time series should be compared with the threshold.The filter is similar to the one that is specified in the MetricService.ListTimeSeries request (that call is useful to verify the time series that will be retrieved / processed) and must specify the metric type and optionally may contain restrictions on resource type, resource labels, and metric labels. This field may not exceed 2048 Unicode characters in length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#filter MonitoringAlertPolicy#filter}
        :param threshold_value: A value against which to compare the time series. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#threshold_value MonitoringAlertPolicy#threshold_value}
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#trigger MonitoringAlertPolicy#trigger}
        '''
        if isinstance(trigger, dict):
            trigger = MonitoringAlertPolicyConditionsConditionThresholdTrigger(**trigger)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98970952b6b65f11fac6e7d16f6fedf157165a6f9a12b86f038c4d06ca775e0c)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument aggregations", value=aggregations, expected_type=type_hints["aggregations"])
            check_type(argname="argument denominator_aggregations", value=denominator_aggregations, expected_type=type_hints["denominator_aggregations"])
            check_type(argname="argument denominator_filter", value=denominator_filter, expected_type=type_hints["denominator_filter"])
            check_type(argname="argument evaluation_missing_data", value=evaluation_missing_data, expected_type=type_hints["evaluation_missing_data"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument threshold_value", value=threshold_value, expected_type=type_hints["threshold_value"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comparison": comparison,
            "duration": duration,
        }
        if aggregations is not None:
            self._values["aggregations"] = aggregations
        if denominator_aggregations is not None:
            self._values["denominator_aggregations"] = denominator_aggregations
        if denominator_filter is not None:
            self._values["denominator_filter"] = denominator_filter
        if evaluation_missing_data is not None:
            self._values["evaluation_missing_data"] = evaluation_missing_data
        if filter is not None:
            self._values["filter"] = filter
        if threshold_value is not None:
            self._values["threshold_value"] = threshold_value
        if trigger is not None:
            self._values["trigger"] = trigger

    @builtins.property
    def comparison(self) -> builtins.str:
        '''The comparison to apply between the time series (indicated by filter and aggregation) and the threshold (indicated by threshold_value).

        The comparison is applied
        on each time series, with the time series on
        the left-hand side and the threshold on the
        right-hand side. Only COMPARISON_LT and
        COMPARISON_GT are supported currently. Possible values: ["COMPARISON_GT", "COMPARISON_GE", "COMPARISON_LT", "COMPARISON_LE", "COMPARISON_EQ", "COMPARISON_NE"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#comparison MonitoringAlertPolicy#comparison}
        '''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> builtins.str:
        '''The amount of time that a time series must violate the threshold to be considered failing.

        Currently, only values that are a
        multiple of a minute--e.g., 0, 60, 120, or
        300 seconds--are supported. If an invalid
        value is given, an error will be returned.
        When choosing a duration, it is useful to
        keep in mind the frequency of the underlying
        time series data (which may also be affected
        by any alignments specified in the
        aggregations field); a good duration is long
        enough so that a single outlier does not
        generate spurious alerts, but short enough
        that unhealthy states are detected and
        alerted on quickly.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#duration MonitoringAlertPolicy#duration}
        '''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aggregations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringAlertPolicyConditionsConditionThresholdAggregations"]]]:
        '''aggregations block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#aggregations MonitoringAlertPolicy#aggregations}
        '''
        result = self._values.get("aggregations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringAlertPolicyConditionsConditionThresholdAggregations"]]], result)

    @builtins.property
    def denominator_aggregations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations"]]]:
        '''denominator_aggregations block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#denominator_aggregations MonitoringAlertPolicy#denominator_aggregations}
        '''
        result = self._values.get("denominator_aggregations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations"]]], result)

    @builtins.property
    def denominator_filter(self) -> typing.Optional[builtins.str]:
        '''A filter that identifies a time series that should be used as the denominator of a ratio that will be compared with the threshold.

        If
        a denominator_filter is specified, the time
        series specified by the filter field will be
        used as the numerator.The filter is similar
        to the one that is specified in the
        MetricService.ListTimeSeries request (that
        call is useful to verify the time series
        that will be retrieved / processed) and must
        specify the metric type and optionally may
        contain restrictions on resource type,
        resource labels, and metric labels. This
        field may not exceed 2048 Unicode characters
        in length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#denominator_filter MonitoringAlertPolicy#denominator_filter}
        '''
        result = self._values.get("denominator_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evaluation_missing_data(self) -> typing.Optional[builtins.str]:
        '''A condition control that determines how metric-threshold conditions are evaluated when data stops arriving. Possible values: ["EVALUATION_MISSING_DATA_INACTIVE", "EVALUATION_MISSING_DATA_ACTIVE", "EVALUATION_MISSING_DATA_NO_OP"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#evaluation_missing_data MonitoringAlertPolicy#evaluation_missing_data}
        '''
        result = self._values.get("evaluation_missing_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''A filter that identifies which time series should be compared with the threshold.The filter is similar to the one that is specified in the MetricService.ListTimeSeries request (that call is useful to verify the time series that will be retrieved / processed) and must specify the metric type and optionally may contain restrictions on resource type, resource labels, and metric labels. This field may not exceed 2048 Unicode characters in length.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#filter MonitoringAlertPolicy#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold_value(self) -> typing.Optional[jsii.Number]:
        '''A value against which to compare the time series.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#threshold_value MonitoringAlertPolicy#threshold_value}
        '''
        result = self._values.get("threshold_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trigger(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyConditionsConditionThresholdTrigger"]:
        '''trigger block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#trigger MonitoringAlertPolicy#trigger}
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional["MonitoringAlertPolicyConditionsConditionThresholdTrigger"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConditionsConditionThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionThresholdAggregations",
    jsii_struct_bases=[],
    name_mapping={
        "alignment_period": "alignmentPeriod",
        "cross_series_reducer": "crossSeriesReducer",
        "group_by_fields": "groupByFields",
        "per_series_aligner": "perSeriesAligner",
    },
)
class MonitoringAlertPolicyConditionsConditionThresholdAggregations:
    def __init__(
        self,
        *,
        alignment_period: typing.Optional[builtins.str] = None,
        cross_series_reducer: typing.Optional[builtins.str] = None,
        group_by_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        per_series_aligner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alignment_period: The alignment period for per-time series alignment. If present, alignmentPeriod must be at least 60 seconds. After per-time series alignment, each time series will contain data points only on the period boundaries. If perSeriesAligner is not specified or equals ALIGN_NONE, then this field is ignored. If perSeriesAligner is specified and does not equal ALIGN_NONE, then this field must be defined; otherwise an error is returned. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#alignment_period MonitoringAlertPolicy#alignment_period}
        :param cross_series_reducer: The approach to be used to combine time series. Not all reducer functions may be applied to all time series, depending on the metric type and the value type of the original time series. Reduction may change the metric type of value type of the time series.Time series data must be aligned in order to perform cross- time series reduction. If crossSeriesReducer is specified, then perSeriesAligner must be specified and not equal ALIGN_NONE and alignmentPeriod must be specified; otherwise, an error is returned. Possible values: ["REDUCE_NONE", "REDUCE_MEAN", "REDUCE_MIN", "REDUCE_MAX", "REDUCE_SUM", "REDUCE_STDDEV", "REDUCE_COUNT", "REDUCE_COUNT_TRUE", "REDUCE_COUNT_FALSE", "REDUCE_FRACTION_TRUE", "REDUCE_PERCENTILE_99", "REDUCE_PERCENTILE_95", "REDUCE_PERCENTILE_50", "REDUCE_PERCENTILE_05"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#cross_series_reducer MonitoringAlertPolicy#cross_series_reducer}
        :param group_by_fields: The set of fields to preserve when crossSeriesReducer is specified. The groupByFields determine how the time series are partitioned into subsets prior to applying the aggregation function. Each subset contains time series that have the same value for each of the grouping fields. Each individual time series is a member of exactly one subset. The crossSeriesReducer is applied to each subset of time series. It is not possible to reduce across different resource types, so this field implicitly contains resource.type. Fields not specified in groupByFields are aggregated away. If groupByFields is not specified and all the time series have the same resource type, then the time series are aggregated into a single output time series. If crossSeriesReducer is not defined, this field is ignored. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#group_by_fields MonitoringAlertPolicy#group_by_fields}
        :param per_series_aligner: The approach to be used to align individual time series. Not all alignment functions may be applied to all time series, depending on the metric type and value type of the original time series. Alignment may change the metric type or the value type of the time series.Time series data must be aligned in order to perform cross- time series reduction. If crossSeriesReducer is specified, then perSeriesAligner must be specified and not equal ALIGN_NONE and alignmentPeriod must be specified; otherwise, an error is returned. Possible values: ["ALIGN_NONE", "ALIGN_DELTA", "ALIGN_RATE", "ALIGN_INTERPOLATE", "ALIGN_NEXT_OLDER", "ALIGN_MIN", "ALIGN_MAX", "ALIGN_MEAN", "ALIGN_COUNT", "ALIGN_SUM", "ALIGN_STDDEV", "ALIGN_COUNT_TRUE", "ALIGN_COUNT_FALSE", "ALIGN_FRACTION_TRUE", "ALIGN_PERCENTILE_99", "ALIGN_PERCENTILE_95", "ALIGN_PERCENTILE_50", "ALIGN_PERCENTILE_05", "ALIGN_PERCENT_CHANGE"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#per_series_aligner MonitoringAlertPolicy#per_series_aligner}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59366f4d9e9f8e0f5fa353585d37c682274dccfb9b1c0b4a9f0b0cc12b052299)
            check_type(argname="argument alignment_period", value=alignment_period, expected_type=type_hints["alignment_period"])
            check_type(argname="argument cross_series_reducer", value=cross_series_reducer, expected_type=type_hints["cross_series_reducer"])
            check_type(argname="argument group_by_fields", value=group_by_fields, expected_type=type_hints["group_by_fields"])
            check_type(argname="argument per_series_aligner", value=per_series_aligner, expected_type=type_hints["per_series_aligner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alignment_period is not None:
            self._values["alignment_period"] = alignment_period
        if cross_series_reducer is not None:
            self._values["cross_series_reducer"] = cross_series_reducer
        if group_by_fields is not None:
            self._values["group_by_fields"] = group_by_fields
        if per_series_aligner is not None:
            self._values["per_series_aligner"] = per_series_aligner

    @builtins.property
    def alignment_period(self) -> typing.Optional[builtins.str]:
        '''The alignment period for per-time series alignment.

        If present,
        alignmentPeriod must be at least
        60 seconds. After per-time series
        alignment, each time series will
        contain data points only on the
        period boundaries. If
        perSeriesAligner is not specified
        or equals ALIGN_NONE, then this
        field is ignored. If
        perSeriesAligner is specified and
        does not equal ALIGN_NONE, then
        this field must be defined;
        otherwise an error is returned.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#alignment_period MonitoringAlertPolicy#alignment_period}
        '''
        result = self._values.get("alignment_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_series_reducer(self) -> typing.Optional[builtins.str]:
        '''The approach to be used to combine time series.

        Not all reducer
        functions may be applied to all
        time series, depending on the
        metric type and the value type of
        the original time series.
        Reduction may change the metric
        type of value type of the time
        series.Time series data must be
        aligned in order to perform cross-
        time series reduction. If
        crossSeriesReducer is specified,
        then perSeriesAligner must be
        specified and not equal ALIGN_NONE
        and alignmentPeriod must be
        specified; otherwise, an error is
        returned. Possible values: ["REDUCE_NONE", "REDUCE_MEAN", "REDUCE_MIN", "REDUCE_MAX", "REDUCE_SUM", "REDUCE_STDDEV", "REDUCE_COUNT", "REDUCE_COUNT_TRUE", "REDUCE_COUNT_FALSE", "REDUCE_FRACTION_TRUE", "REDUCE_PERCENTILE_99", "REDUCE_PERCENTILE_95", "REDUCE_PERCENTILE_50", "REDUCE_PERCENTILE_05"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#cross_series_reducer MonitoringAlertPolicy#cross_series_reducer}
        '''
        result = self._values.get("cross_series_reducer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_by_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of fields to preserve when crossSeriesReducer is specified.

        The groupByFields determine how
        the time series are partitioned
        into subsets prior to applying the
        aggregation function. Each subset
        contains time series that have the
        same value for each of the
        grouping fields. Each individual
        time series is a member of exactly
        one subset. The crossSeriesReducer
        is applied to each subset of time
        series. It is not possible to
        reduce across different resource
        types, so this field implicitly
        contains resource.type. Fields not
        specified in groupByFields are
        aggregated away. If groupByFields
        is not specified and all the time
        series have the same resource
        type, then the time series are
        aggregated into a single output
        time series. If crossSeriesReducer
        is not defined, this field is
        ignored.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#group_by_fields MonitoringAlertPolicy#group_by_fields}
        '''
        result = self._values.get("group_by_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def per_series_aligner(self) -> typing.Optional[builtins.str]:
        '''The approach to be used to align individual time series.

        Not all
        alignment functions may be applied
        to all time series, depending on
        the metric type and value type of
        the original time series.
        Alignment may change the metric
        type or the value type of the time
        series.Time series data must be
        aligned in order to perform cross-
        time series reduction. If
        crossSeriesReducer is specified,
        then perSeriesAligner must be
        specified and not equal ALIGN_NONE
        and alignmentPeriod must be
        specified; otherwise, an error is
        returned. Possible values: ["ALIGN_NONE", "ALIGN_DELTA", "ALIGN_RATE", "ALIGN_INTERPOLATE", "ALIGN_NEXT_OLDER", "ALIGN_MIN", "ALIGN_MAX", "ALIGN_MEAN", "ALIGN_COUNT", "ALIGN_SUM", "ALIGN_STDDEV", "ALIGN_COUNT_TRUE", "ALIGN_COUNT_FALSE", "ALIGN_FRACTION_TRUE", "ALIGN_PERCENTILE_99", "ALIGN_PERCENTILE_95", "ALIGN_PERCENTILE_50", "ALIGN_PERCENTILE_05", "ALIGN_PERCENT_CHANGE"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#per_series_aligner MonitoringAlertPolicy#per_series_aligner}
        '''
        result = self._values.get("per_series_aligner")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConditionsConditionThresholdAggregations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyConditionsConditionThresholdAggregationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionThresholdAggregationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7463ef907f8cbddfa0f854b73bd9fa7b74e9143761bc797b640069bf381eb21b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitoringAlertPolicyConditionsConditionThresholdAggregationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52305c1c64ccb5d7c71a2aa0dcb416a2f4f978640a92c739b8b3371bf852872)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitoringAlertPolicyConditionsConditionThresholdAggregationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b55704b013c7220a77268ffbaca38ee8c8c50a72da943abfb3920693d40f4be7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e1d2084149246fbe7f8bb82c75f5381d0bb822b28e80aa029ba1c8777f73511)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3a1fb538aea7214b16e06119c9b5c3441c2bc2f30278ba56a57a7016fb53889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdAggregations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdAggregations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdAggregations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824e6273f19e3cf171d6782d611fd9b2aac96d07499858b2a3fc127cde5964d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitoringAlertPolicyConditionsConditionThresholdAggregationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionThresholdAggregationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83f5d0e4398cc369b3d34bc3003a0fe3a6199efafd181c4da0648cdcd2f7e493)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAlignmentPeriod")
    def reset_alignment_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlignmentPeriod", []))

    @jsii.member(jsii_name="resetCrossSeriesReducer")
    def reset_cross_series_reducer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossSeriesReducer", []))

    @jsii.member(jsii_name="resetGroupByFields")
    def reset_group_by_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupByFields", []))

    @jsii.member(jsii_name="resetPerSeriesAligner")
    def reset_per_series_aligner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerSeriesAligner", []))

    @builtins.property
    @jsii.member(jsii_name="alignmentPeriodInput")
    def alignment_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alignmentPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="crossSeriesReducerInput")
    def cross_series_reducer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossSeriesReducerInput"))

    @builtins.property
    @jsii.member(jsii_name="groupByFieldsInput")
    def group_by_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupByFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="perSeriesAlignerInput")
    def per_series_aligner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "perSeriesAlignerInput"))

    @builtins.property
    @jsii.member(jsii_name="alignmentPeriod")
    def alignment_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alignmentPeriod"))

    @alignment_period.setter
    def alignment_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a85fc7d82660e6c1e6be9591aa674a72e6a8e0bf074f3b1cc4b9f7a0fcf431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alignmentPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="crossSeriesReducer")
    def cross_series_reducer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossSeriesReducer"))

    @cross_series_reducer.setter
    def cross_series_reducer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63a55f2c39724af6e8209c2c3a19cd2950cdaf6866956f45daac95c4762a9a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossSeriesReducer", value)

    @builtins.property
    @jsii.member(jsii_name="groupByFields")
    def group_by_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupByFields"))

    @group_by_fields.setter
    def group_by_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45809104ec5dc1c1eb825527ce27ab14db1ee6d419ff207393e45f1e15bb2986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupByFields", value)

    @builtins.property
    @jsii.member(jsii_name="perSeriesAligner")
    def per_series_aligner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perSeriesAligner"))

    @per_series_aligner.setter
    def per_series_aligner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42a2cd13942b0287ed02ed4d52e45e2a9036e2ca25ae9dc9be387f710ca1852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perSeriesAligner", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdAggregations, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdAggregations, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdAggregations, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49bada02f5f02269c5477117fb4b694317bbaed73053b38d389b24d179e9368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations",
    jsii_struct_bases=[],
    name_mapping={
        "alignment_period": "alignmentPeriod",
        "cross_series_reducer": "crossSeriesReducer",
        "group_by_fields": "groupByFields",
        "per_series_aligner": "perSeriesAligner",
    },
)
class MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations:
    def __init__(
        self,
        *,
        alignment_period: typing.Optional[builtins.str] = None,
        cross_series_reducer: typing.Optional[builtins.str] = None,
        group_by_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        per_series_aligner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alignment_period: The alignment period for per-time series alignment. If present, alignmentPeriod must be at least 60 seconds. After per-time series alignment, each time series will contain data points only on the period boundaries. If perSeriesAligner is not specified or equals ALIGN_NONE, then this field is ignored. If perSeriesAligner is specified and does not equal ALIGN_NONE, then this field must be defined; otherwise an error is returned. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#alignment_period MonitoringAlertPolicy#alignment_period}
        :param cross_series_reducer: The approach to be used to combine time series. Not all reducer functions may be applied to all time series, depending on the metric type and the value type of the original time series. Reduction may change the metric type of value type of the time series.Time series data must be aligned in order to perform cross- time series reduction. If crossSeriesReducer is specified, then perSeriesAligner must be specified and not equal ALIGN_NONE and alignmentPeriod must be specified; otherwise, an error is returned. Possible values: ["REDUCE_NONE", "REDUCE_MEAN", "REDUCE_MIN", "REDUCE_MAX", "REDUCE_SUM", "REDUCE_STDDEV", "REDUCE_COUNT", "REDUCE_COUNT_TRUE", "REDUCE_COUNT_FALSE", "REDUCE_FRACTION_TRUE", "REDUCE_PERCENTILE_99", "REDUCE_PERCENTILE_95", "REDUCE_PERCENTILE_50", "REDUCE_PERCENTILE_05"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#cross_series_reducer MonitoringAlertPolicy#cross_series_reducer}
        :param group_by_fields: The set of fields to preserve when crossSeriesReducer is specified. The groupByFields determine how the time series are partitioned into subsets prior to applying the aggregation function. Each subset contains time series that have the same value for each of the grouping fields. Each individual time series is a member of exactly one subset. The crossSeriesReducer is applied to each subset of time series. It is not possible to reduce across different resource types, so this field implicitly contains resource.type. Fields not specified in groupByFields are aggregated away. If groupByFields is not specified and all the time series have the same resource type, then the time series are aggregated into a single output time series. If crossSeriesReducer is not defined, this field is ignored. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#group_by_fields MonitoringAlertPolicy#group_by_fields}
        :param per_series_aligner: The approach to be used to align individual time series. Not all alignment functions may be applied to all time series, depending on the metric type and value type of the original time series. Alignment may change the metric type or the value type of the time series.Time series data must be aligned in order to perform cross- time series reduction. If crossSeriesReducer is specified, then perSeriesAligner must be specified and not equal ALIGN_NONE and alignmentPeriod must be specified; otherwise, an error is returned. Possible values: ["ALIGN_NONE", "ALIGN_DELTA", "ALIGN_RATE", "ALIGN_INTERPOLATE", "ALIGN_NEXT_OLDER", "ALIGN_MIN", "ALIGN_MAX", "ALIGN_MEAN", "ALIGN_COUNT", "ALIGN_SUM", "ALIGN_STDDEV", "ALIGN_COUNT_TRUE", "ALIGN_COUNT_FALSE", "ALIGN_FRACTION_TRUE", "ALIGN_PERCENTILE_99", "ALIGN_PERCENTILE_95", "ALIGN_PERCENTILE_50", "ALIGN_PERCENTILE_05", "ALIGN_PERCENT_CHANGE"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#per_series_aligner MonitoringAlertPolicy#per_series_aligner}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c2229303ea64067d702107df485d8fefe5b77846a941a7d87bbb11fb7a20ce)
            check_type(argname="argument alignment_period", value=alignment_period, expected_type=type_hints["alignment_period"])
            check_type(argname="argument cross_series_reducer", value=cross_series_reducer, expected_type=type_hints["cross_series_reducer"])
            check_type(argname="argument group_by_fields", value=group_by_fields, expected_type=type_hints["group_by_fields"])
            check_type(argname="argument per_series_aligner", value=per_series_aligner, expected_type=type_hints["per_series_aligner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alignment_period is not None:
            self._values["alignment_period"] = alignment_period
        if cross_series_reducer is not None:
            self._values["cross_series_reducer"] = cross_series_reducer
        if group_by_fields is not None:
            self._values["group_by_fields"] = group_by_fields
        if per_series_aligner is not None:
            self._values["per_series_aligner"] = per_series_aligner

    @builtins.property
    def alignment_period(self) -> typing.Optional[builtins.str]:
        '''The alignment period for per-time series alignment.

        If present,
        alignmentPeriod must be at least
        60 seconds. After per-time series
        alignment, each time series will
        contain data points only on the
        period boundaries. If
        perSeriesAligner is not specified
        or equals ALIGN_NONE, then this
        field is ignored. If
        perSeriesAligner is specified and
        does not equal ALIGN_NONE, then
        this field must be defined;
        otherwise an error is returned.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#alignment_period MonitoringAlertPolicy#alignment_period}
        '''
        result = self._values.get("alignment_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_series_reducer(self) -> typing.Optional[builtins.str]:
        '''The approach to be used to combine time series.

        Not all reducer
        functions may be applied to all
        time series, depending on the
        metric type and the value type of
        the original time series.
        Reduction may change the metric
        type of value type of the time
        series.Time series data must be
        aligned in order to perform cross-
        time series reduction. If
        crossSeriesReducer is specified,
        then perSeriesAligner must be
        specified and not equal ALIGN_NONE
        and alignmentPeriod must be
        specified; otherwise, an error is
        returned. Possible values: ["REDUCE_NONE", "REDUCE_MEAN", "REDUCE_MIN", "REDUCE_MAX", "REDUCE_SUM", "REDUCE_STDDEV", "REDUCE_COUNT", "REDUCE_COUNT_TRUE", "REDUCE_COUNT_FALSE", "REDUCE_FRACTION_TRUE", "REDUCE_PERCENTILE_99", "REDUCE_PERCENTILE_95", "REDUCE_PERCENTILE_50", "REDUCE_PERCENTILE_05"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#cross_series_reducer MonitoringAlertPolicy#cross_series_reducer}
        '''
        result = self._values.get("cross_series_reducer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_by_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of fields to preserve when crossSeriesReducer is specified.

        The groupByFields determine how
        the time series are partitioned
        into subsets prior to applying the
        aggregation function. Each subset
        contains time series that have the
        same value for each of the
        grouping fields. Each individual
        time series is a member of exactly
        one subset. The crossSeriesReducer
        is applied to each subset of time
        series. It is not possible to
        reduce across different resource
        types, so this field implicitly
        contains resource.type. Fields not
        specified in groupByFields are
        aggregated away. If groupByFields
        is not specified and all the time
        series have the same resource
        type, then the time series are
        aggregated into a single output
        time series. If crossSeriesReducer
        is not defined, this field is
        ignored.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#group_by_fields MonitoringAlertPolicy#group_by_fields}
        '''
        result = self._values.get("group_by_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def per_series_aligner(self) -> typing.Optional[builtins.str]:
        '''The approach to be used to align individual time series.

        Not all
        alignment functions may be applied
        to all time series, depending on
        the metric type and value type of
        the original time series.
        Alignment may change the metric
        type or the value type of the time
        series.Time series data must be
        aligned in order to perform cross-
        time series reduction. If
        crossSeriesReducer is specified,
        then perSeriesAligner must be
        specified and not equal ALIGN_NONE
        and alignmentPeriod must be
        specified; otherwise, an error is
        returned. Possible values: ["ALIGN_NONE", "ALIGN_DELTA", "ALIGN_RATE", "ALIGN_INTERPOLATE", "ALIGN_NEXT_OLDER", "ALIGN_MIN", "ALIGN_MAX", "ALIGN_MEAN", "ALIGN_COUNT", "ALIGN_SUM", "ALIGN_STDDEV", "ALIGN_COUNT_TRUE", "ALIGN_COUNT_FALSE", "ALIGN_FRACTION_TRUE", "ALIGN_PERCENTILE_99", "ALIGN_PERCENTILE_95", "ALIGN_PERCENTILE_50", "ALIGN_PERCENTILE_05", "ALIGN_PERCENT_CHANGE"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#per_series_aligner MonitoringAlertPolicy#per_series_aligner}
        '''
        result = self._values.get("per_series_aligner")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72eda0291ce2d28ce67612649a15fe6c7d7650dc7b20357267c69114814f30d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c54e3ff60b97383bc2f6ff5df6c88886954c5aca3577e8ae422eb8457eb4501)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb53c308f4610ff94ed08bae2d804cd096b58d7c6ee629d7c3c98d7c825197e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__721b4c71e5592b31167e5c1d67280f5d44c8e62ead49403d94074ec5c719bbe8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0096d7e92d7000815f4c9259f94d21f87b295db2ae36c6cd3a5d03fd9abbc73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccdc50429aa1f9d299313ffb578048cdf6cbecd2dd1a291e5aa7a76bba76b16e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60c5a947d2196f02a804348872817a6bbb6c43192461e7060c352b81e5fb03d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAlignmentPeriod")
    def reset_alignment_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlignmentPeriod", []))

    @jsii.member(jsii_name="resetCrossSeriesReducer")
    def reset_cross_series_reducer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossSeriesReducer", []))

    @jsii.member(jsii_name="resetGroupByFields")
    def reset_group_by_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupByFields", []))

    @jsii.member(jsii_name="resetPerSeriesAligner")
    def reset_per_series_aligner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerSeriesAligner", []))

    @builtins.property
    @jsii.member(jsii_name="alignmentPeriodInput")
    def alignment_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alignmentPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="crossSeriesReducerInput")
    def cross_series_reducer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossSeriesReducerInput"))

    @builtins.property
    @jsii.member(jsii_name="groupByFieldsInput")
    def group_by_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupByFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="perSeriesAlignerInput")
    def per_series_aligner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "perSeriesAlignerInput"))

    @builtins.property
    @jsii.member(jsii_name="alignmentPeriod")
    def alignment_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alignmentPeriod"))

    @alignment_period.setter
    def alignment_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c38e1c7e03e39f082563836bfd5092169dd61386a515f7eaaee0ddbf90a13a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alignmentPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="crossSeriesReducer")
    def cross_series_reducer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossSeriesReducer"))

    @cross_series_reducer.setter
    def cross_series_reducer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__311a97db0f5a0efcf526cfedd50f3bfe9fe304e3d50bf3a64c6fb079fa2fc58b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossSeriesReducer", value)

    @builtins.property
    @jsii.member(jsii_name="groupByFields")
    def group_by_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupByFields"))

    @group_by_fields.setter
    def group_by_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48d3a7232685d4da3bbdca88250309dda3e488da14b225f346f9b7a5a3c72c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupByFields", value)

    @builtins.property
    @jsii.member(jsii_name="perSeriesAligner")
    def per_series_aligner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perSeriesAligner"))

    @per_series_aligner.setter
    def per_series_aligner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0edb8833d2c6ca750fce808d57093c8fb51bd96c655b317bd61fbb0116a2adeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perSeriesAligner", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9ea7c089fa3f41d5b8d802f563b46dbd4c959ef4d235746998715f3796046a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitoringAlertPolicyConditionsConditionThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d16e3a2fecfeb1f1ab98fb79b2fb7f99855d5bed1a4a4a853d52c28d0bbb978b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAggregations")
    def put_aggregations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdAggregations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86024bf7c756e71909cced138ae53a30cab4867d9f33e2dba83e28ef96a045cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAggregations", [value]))

    @jsii.member(jsii_name="putDenominatorAggregations")
    def put_denominator_aggregations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8fc8f7e47fc33fd5a30841f2d1e2eec4231cbbf36d1dd0656c35ac291fbd4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDenominatorAggregations", [value]))

    @jsii.member(jsii_name="putTrigger")
    def put_trigger(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: The absolute number of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#count MonitoringAlertPolicy#count}
        :param percent: The percentage of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#percent MonitoringAlertPolicy#percent}
        '''
        value = MonitoringAlertPolicyConditionsConditionThresholdTrigger(
            count=count, percent=percent
        )

        return typing.cast(None, jsii.invoke(self, "putTrigger", [value]))

    @jsii.member(jsii_name="resetAggregations")
    def reset_aggregations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregations", []))

    @jsii.member(jsii_name="resetDenominatorAggregations")
    def reset_denominator_aggregations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenominatorAggregations", []))

    @jsii.member(jsii_name="resetDenominatorFilter")
    def reset_denominator_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenominatorFilter", []))

    @jsii.member(jsii_name="resetEvaluationMissingData")
    def reset_evaluation_missing_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationMissingData", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetThresholdValue")
    def reset_threshold_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdValue", []))

    @jsii.member(jsii_name="resetTrigger")
    def reset_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrigger", []))

    @builtins.property
    @jsii.member(jsii_name="aggregations")
    def aggregations(
        self,
    ) -> MonitoringAlertPolicyConditionsConditionThresholdAggregationsList:
        return typing.cast(MonitoringAlertPolicyConditionsConditionThresholdAggregationsList, jsii.get(self, "aggregations"))

    @builtins.property
    @jsii.member(jsii_name="denominatorAggregations")
    def denominator_aggregations(
        self,
    ) -> MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregationsList:
        return typing.cast(MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregationsList, jsii.get(self, "denominatorAggregations"))

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(
        self,
    ) -> "MonitoringAlertPolicyConditionsConditionThresholdTriggerOutputReference":
        return typing.cast("MonitoringAlertPolicyConditionsConditionThresholdTriggerOutputReference", jsii.get(self, "trigger"))

    @builtins.property
    @jsii.member(jsii_name="aggregationsInput")
    def aggregations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdAggregations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdAggregations]]], jsii.get(self, "aggregationsInput"))

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="denominatorAggregationsInput")
    def denominator_aggregations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations]]], jsii.get(self, "denominatorAggregationsInput"))

    @builtins.property
    @jsii.member(jsii_name="denominatorFilterInput")
    def denominator_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "denominatorFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationMissingDataInput")
    def evaluation_missing_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluationMissingDataInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdValueInput")
    def threshold_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdValueInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerInput")
    def trigger_input(
        self,
    ) -> typing.Optional["MonitoringAlertPolicyConditionsConditionThresholdTrigger"]:
        return typing.cast(typing.Optional["MonitoringAlertPolicyConditionsConditionThresholdTrigger"], jsii.get(self, "triggerInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c7091e5a19c4dec4c225fb4e152e5b59465096e2757db2a5d025ab9d4a570cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value)

    @builtins.property
    @jsii.member(jsii_name="denominatorFilter")
    def denominator_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "denominatorFilter"))

    @denominator_filter.setter
    def denominator_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2dd0fa5f600156aa57b82b20003f4017168b1e9de7448bbc40a812463f8b161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denominatorFilter", value)

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664689d0f74408aa11c496e4d4fb6c37e44f3e22958303435b9ee4cb999977c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value)

    @builtins.property
    @jsii.member(jsii_name="evaluationMissingData")
    def evaluation_missing_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluationMissingData"))

    @evaluation_missing_data.setter
    def evaluation_missing_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e0a7c5531629f0b08257285193b41743ad18aba98a28c831618137717e7613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMissingData", value)

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74468bfd11f1197330ae3b85e1391869ab9afb55708b663a1ee9880f6c0234b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value)

    @builtins.property
    @jsii.member(jsii_name="thresholdValue")
    def threshold_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdValue"))

    @threshold_value.setter
    def threshold_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a56ad7cf405da0fd02780d1fdd0a997b059f632281a8792cc101ff534eb9fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyConditionsConditionThreshold]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyConditionsConditionThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringAlertPolicyConditionsConditionThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92274b7248c1942b6dd3ebac26d63f218949c8d328d88b788f256a365b16ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionThresholdTrigger",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "percent": "percent"},
)
class MonitoringAlertPolicyConditionsConditionThresholdTrigger:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: The absolute number of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#count MonitoringAlertPolicy#count}
        :param percent: The percentage of time series that must fail the predicate for the condition to be triggered. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#percent MonitoringAlertPolicy#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997d53444c6bcb5973e21890e2c130ee3d5cec7fe707fe86424251f43c4edbd1)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument percent", value=percent, expected_type=type_hints["percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if percent is not None:
            self._values["percent"] = percent

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''The absolute number of time series that must fail the predicate for the condition to be triggered.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#count MonitoringAlertPolicy#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''The percentage of time series that must fail the predicate for the condition to be triggered.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#percent MonitoringAlertPolicy#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConditionsConditionThresholdTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyConditionsConditionThresholdTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsConditionThresholdTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2c8332d2f9c1052dcb2f5e6c2b7156190c6a719c06d153791d93e0881396c5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetPercent")
    def reset_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercent", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="percentInput")
    def percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1c2c20716a9282c4fc78391c06f90a12762a1d01d3ca328cf6cd52f1a2d8ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879ca1b470fab87acd371064c592496bde97f78c02cea0b99f8bab8c8056c94e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyConditionsConditionThresholdTrigger]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyConditionsConditionThresholdTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringAlertPolicyConditionsConditionThresholdTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6b7911589b80ebdd814ef8bc24017d70ce805510b98725bdc79e9c2f29407b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitoringAlertPolicyConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4732fb3dc33dd39f5ed314728d190ab1db640f1e195ff8ffed9819e264c21b22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitoringAlertPolicyConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5dbad5661a4d8db1f959f6e7e1d99105592b563f8b567eb8362a3daace05db)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitoringAlertPolicyConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c898e571d88494437275e3a4879b3db511ae76f230dfcf7f7092b0bf98551e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd999ce7c43a462c9c3e28896aedefc5188d209699278f1fddbce78565b5bf4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b927d4209ba8ebdda315f8e1b1961fa810217f36a117208152cb6d25b52261a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7ee5c76f7bd96e9c4e8eaddcee2f81d95eb7c8f72b5598c4f69967289aab3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitoringAlertPolicyConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__758a7feb4e9c2e0e3e626c0371a291f541cc26219911df25f9c3f41182c3f5ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConditionAbsent")
    def put_condition_absent(
        self,
        *,
        duration: builtins.str,
        aggregations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionAbsentAggregations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        filter: typing.Optional[builtins.str] = None,
        trigger: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionAbsentTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param duration: The amount of time that a time series must fail to report new data to be considered failing. Currently, only values that are a multiple of a minute--e.g. 60s, 120s, or 300s --are supported. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#duration MonitoringAlertPolicy#duration}
        :param aggregations: aggregations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#aggregations MonitoringAlertPolicy#aggregations}
        :param filter: A filter that identifies which time series should be compared with the threshold.The filter is similar to the one that is specified in the MetricService.ListTimeSeries request (that call is useful to verify the time series that will be retrieved / processed) and must specify the metric type and optionally may contain restrictions on resource type, resource labels, and metric labels. This field may not exceed 2048 Unicode characters in length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#filter MonitoringAlertPolicy#filter}
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#trigger MonitoringAlertPolicy#trigger}
        '''
        value = MonitoringAlertPolicyConditionsConditionAbsent(
            duration=duration,
            aggregations=aggregations,
            filter=filter,
            trigger=trigger,
        )

        return typing.cast(None, jsii.invoke(self, "putConditionAbsent", [value]))

    @jsii.member(jsii_name="putConditionMatchedLog")
    def put_condition_matched_log(
        self,
        *,
        filter: builtins.str,
        label_extractors: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param filter: A logs-based filter. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#filter MonitoringAlertPolicy#filter}
        :param label_extractors: A map from a label key to an extractor expression, which is used to extract the value for this label key. Each entry in this map is a specification for how data should be extracted from log entries that match filter. Each combination of extracted values is treated as a separate rule for the purposes of triggering notifications. Label keys and corresponding values can be used in notifications generated by this condition. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#label_extractors MonitoringAlertPolicy#label_extractors}
        '''
        value = MonitoringAlertPolicyConditionsConditionMatchedLog(
            filter=filter, label_extractors=label_extractors
        )

        return typing.cast(None, jsii.invoke(self, "putConditionMatchedLog", [value]))

    @jsii.member(jsii_name="putConditionMonitoringQueryLanguage")
    def put_condition_monitoring_query_language(
        self,
        *,
        duration: builtins.str,
        query: builtins.str,
        evaluation_missing_data: typing.Optional[builtins.str] = None,
        trigger: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param duration: The amount of time that a time series must violate the threshold to be considered failing. Currently, only values that are a multiple of a minute--e.g., 0, 60, 120, or 300 seconds--are supported. If an invalid value is given, an error will be returned. When choosing a duration, it is useful to keep in mind the frequency of the underlying time series data (which may also be affected by any alignments specified in the aggregations field); a good duration is long enough so that a single outlier does not generate spurious alerts, but short enough that unhealthy states are detected and alerted on quickly. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#duration MonitoringAlertPolicy#duration}
        :param query: Monitoring Query Language query that outputs a boolean stream. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#query MonitoringAlertPolicy#query}
        :param evaluation_missing_data: A condition control that determines how metric-threshold conditions are evaluated when data stops arriving. Possible values: ["EVALUATION_MISSING_DATA_INACTIVE", "EVALUATION_MISSING_DATA_ACTIVE", "EVALUATION_MISSING_DATA_NO_OP"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#evaluation_missing_data MonitoringAlertPolicy#evaluation_missing_data}
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#trigger MonitoringAlertPolicy#trigger}
        '''
        value = MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage(
            duration=duration,
            query=query,
            evaluation_missing_data=evaluation_missing_data,
            trigger=trigger,
        )

        return typing.cast(None, jsii.invoke(self, "putConditionMonitoringQueryLanguage", [value]))

    @jsii.member(jsii_name="putConditionThreshold")
    def put_condition_threshold(
        self,
        *,
        comparison: builtins.str,
        duration: builtins.str,
        aggregations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdAggregations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        denominator_aggregations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        denominator_filter: typing.Optional[builtins.str] = None,
        evaluation_missing_data: typing.Optional[builtins.str] = None,
        filter: typing.Optional[builtins.str] = None,
        threshold_value: typing.Optional[jsii.Number] = None,
        trigger: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param comparison: The comparison to apply between the time series (indicated by filter and aggregation) and the threshold (indicated by threshold_value). The comparison is applied on each time series, with the time series on the left-hand side and the threshold on the right-hand side. Only COMPARISON_LT and COMPARISON_GT are supported currently. Possible values: ["COMPARISON_GT", "COMPARISON_GE", "COMPARISON_LT", "COMPARISON_LE", "COMPARISON_EQ", "COMPARISON_NE"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#comparison MonitoringAlertPolicy#comparison}
        :param duration: The amount of time that a time series must violate the threshold to be considered failing. Currently, only values that are a multiple of a minute--e.g., 0, 60, 120, or 300 seconds--are supported. If an invalid value is given, an error will be returned. When choosing a duration, it is useful to keep in mind the frequency of the underlying time series data (which may also be affected by any alignments specified in the aggregations field); a good duration is long enough so that a single outlier does not generate spurious alerts, but short enough that unhealthy states are detected and alerted on quickly. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#duration MonitoringAlertPolicy#duration}
        :param aggregations: aggregations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#aggregations MonitoringAlertPolicy#aggregations}
        :param denominator_aggregations: denominator_aggregations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#denominator_aggregations MonitoringAlertPolicy#denominator_aggregations}
        :param denominator_filter: A filter that identifies a time series that should be used as the denominator of a ratio that will be compared with the threshold. If a denominator_filter is specified, the time series specified by the filter field will be used as the numerator.The filter is similar to the one that is specified in the MetricService.ListTimeSeries request (that call is useful to verify the time series that will be retrieved / processed) and must specify the metric type and optionally may contain restrictions on resource type, resource labels, and metric labels. This field may not exceed 2048 Unicode characters in length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#denominator_filter MonitoringAlertPolicy#denominator_filter}
        :param evaluation_missing_data: A condition control that determines how metric-threshold conditions are evaluated when data stops arriving. Possible values: ["EVALUATION_MISSING_DATA_INACTIVE", "EVALUATION_MISSING_DATA_ACTIVE", "EVALUATION_MISSING_DATA_NO_OP"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#evaluation_missing_data MonitoringAlertPolicy#evaluation_missing_data}
        :param filter: A filter that identifies which time series should be compared with the threshold.The filter is similar to the one that is specified in the MetricService.ListTimeSeries request (that call is useful to verify the time series that will be retrieved / processed) and must specify the metric type and optionally may contain restrictions on resource type, resource labels, and metric labels. This field may not exceed 2048 Unicode characters in length. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#filter MonitoringAlertPolicy#filter}
        :param threshold_value: A value against which to compare the time series. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#threshold_value MonitoringAlertPolicy#threshold_value}
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#trigger MonitoringAlertPolicy#trigger}
        '''
        value = MonitoringAlertPolicyConditionsConditionThreshold(
            comparison=comparison,
            duration=duration,
            aggregations=aggregations,
            denominator_aggregations=denominator_aggregations,
            denominator_filter=denominator_filter,
            evaluation_missing_data=evaluation_missing_data,
            filter=filter,
            threshold_value=threshold_value,
            trigger=trigger,
        )

        return typing.cast(None, jsii.invoke(self, "putConditionThreshold", [value]))

    @jsii.member(jsii_name="resetConditionAbsent")
    def reset_condition_absent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionAbsent", []))

    @jsii.member(jsii_name="resetConditionMatchedLog")
    def reset_condition_matched_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionMatchedLog", []))

    @jsii.member(jsii_name="resetConditionMonitoringQueryLanguage")
    def reset_condition_monitoring_query_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionMonitoringQueryLanguage", []))

    @jsii.member(jsii_name="resetConditionThreshold")
    def reset_condition_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="conditionAbsent")
    def condition_absent(
        self,
    ) -> MonitoringAlertPolicyConditionsConditionAbsentOutputReference:
        return typing.cast(MonitoringAlertPolicyConditionsConditionAbsentOutputReference, jsii.get(self, "conditionAbsent"))

    @builtins.property
    @jsii.member(jsii_name="conditionMatchedLog")
    def condition_matched_log(
        self,
    ) -> MonitoringAlertPolicyConditionsConditionMatchedLogOutputReference:
        return typing.cast(MonitoringAlertPolicyConditionsConditionMatchedLogOutputReference, jsii.get(self, "conditionMatchedLog"))

    @builtins.property
    @jsii.member(jsii_name="conditionMonitoringQueryLanguage")
    def condition_monitoring_query_language(
        self,
    ) -> MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageOutputReference:
        return typing.cast(MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageOutputReference, jsii.get(self, "conditionMonitoringQueryLanguage"))

    @builtins.property
    @jsii.member(jsii_name="conditionThreshold")
    def condition_threshold(
        self,
    ) -> MonitoringAlertPolicyConditionsConditionThresholdOutputReference:
        return typing.cast(MonitoringAlertPolicyConditionsConditionThresholdOutputReference, jsii.get(self, "conditionThreshold"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="conditionAbsentInput")
    def condition_absent_input(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyConditionsConditionAbsent]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyConditionsConditionAbsent], jsii.get(self, "conditionAbsentInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionMatchedLogInput")
    def condition_matched_log_input(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyConditionsConditionMatchedLog]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyConditionsConditionMatchedLog], jsii.get(self, "conditionMatchedLogInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionMonitoringQueryLanguageInput")
    def condition_monitoring_query_language_input(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage], jsii.get(self, "conditionMonitoringQueryLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionThresholdInput")
    def condition_threshold_input(
        self,
    ) -> typing.Optional[MonitoringAlertPolicyConditionsConditionThreshold]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyConditionsConditionThreshold], jsii.get(self, "conditionThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6cb1fb687418569edf80ab44200aa852e6f63e2a28f2a3d88b9e5b13ea3c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitoringAlertPolicyConditions, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitoringAlertPolicyConditions, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitoringAlertPolicyConditions, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028814361c62933ca120a56a51c8be4e1c570138953c4fab24547830a739d215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "combiner": "combiner",
        "conditions": "conditions",
        "display_name": "displayName",
        "alert_strategy": "alertStrategy",
        "documentation": "documentation",
        "enabled": "enabled",
        "id": "id",
        "notification_channels": "notificationChannels",
        "project": "project",
        "timeouts": "timeouts",
        "user_labels": "userLabels",
    },
)
class MonitoringAlertPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        combiner: builtins.str,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
        display_name: builtins.str,
        alert_strategy: typing.Optional[typing.Union[MonitoringAlertPolicyAlertStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
        documentation: typing.Optional[typing.Union["MonitoringAlertPolicyDocumentation", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MonitoringAlertPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param combiner: How to combine the results of multiple conditions to determine if an incident should be opened. Possible values: ["AND", "OR", "AND_WITH_MATCHING_RESOURCE"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#combiner MonitoringAlertPolicy#combiner}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#conditions MonitoringAlertPolicy#conditions}
        :param display_name: A short name or phrase used to identify the policy in dashboards, notifications, and incidents. To avoid confusion, don't use the same display name for multiple policies in the same project. The name is limited to 512 Unicode characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#display_name MonitoringAlertPolicy#display_name}
        :param alert_strategy: alert_strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#alert_strategy MonitoringAlertPolicy#alert_strategy}
        :param documentation: documentation block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#documentation MonitoringAlertPolicy#documentation}
        :param enabled: Whether or not the policy is enabled. The default is true. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#enabled MonitoringAlertPolicy#enabled}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#id MonitoringAlertPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_channels: Identifies the notification channels to which notifications should be sent when incidents are opened or closed or when new violations occur on an already opened incident. Each element of this array corresponds to the name field in each of the NotificationChannel objects that are returned from the notificationChannels.list method. The syntax of the entries in this field is 'projects/[PROJECT_ID]/notificationChannels/[CHANNEL_ID]' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#notification_channels MonitoringAlertPolicy#notification_channels}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#project MonitoringAlertPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#timeouts MonitoringAlertPolicy#timeouts}
        :param user_labels: This field is intended to be used for organizing and identifying the AlertPolicy objects.The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#user_labels MonitoringAlertPolicy#user_labels}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(alert_strategy, dict):
            alert_strategy = MonitoringAlertPolicyAlertStrategy(**alert_strategy)
        if isinstance(documentation, dict):
            documentation = MonitoringAlertPolicyDocumentation(**documentation)
        if isinstance(timeouts, dict):
            timeouts = MonitoringAlertPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b10165cb559bd919d435310ff920de2092b9d41dce03821f0a09f022bc69c0e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument combiner", value=combiner, expected_type=type_hints["combiner"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument alert_strategy", value=alert_strategy, expected_type=type_hints["alert_strategy"])
            check_type(argname="argument documentation", value=documentation, expected_type=type_hints["documentation"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notification_channels", value=notification_channels, expected_type=type_hints["notification_channels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_labels", value=user_labels, expected_type=type_hints["user_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "combiner": combiner,
            "conditions": conditions,
            "display_name": display_name,
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
        if alert_strategy is not None:
            self._values["alert_strategy"] = alert_strategy
        if documentation is not None:
            self._values["documentation"] = documentation
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if notification_channels is not None:
            self._values["notification_channels"] = notification_channels
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_labels is not None:
            self._values["user_labels"] = user_labels

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
    def combiner(self) -> builtins.str:
        '''How to combine the results of multiple conditions to determine if an incident should be opened.

        Possible values: ["AND", "OR", "AND_WITH_MATCHING_RESOURCE"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#combiner MonitoringAlertPolicy#combiner}
        '''
        result = self._values.get("combiner")
        assert result is not None, "Required property 'combiner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditions]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#conditions MonitoringAlertPolicy#conditions}
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditions]], result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''A short name or phrase used to identify the policy in dashboards, notifications, and incidents.

        To avoid confusion, don't use
        the same display name for multiple policies in the same project. The
        name is limited to 512 Unicode characters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#display_name MonitoringAlertPolicy#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alert_strategy(self) -> typing.Optional[MonitoringAlertPolicyAlertStrategy]:
        '''alert_strategy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#alert_strategy MonitoringAlertPolicy#alert_strategy}
        '''
        result = self._values.get("alert_strategy")
        return typing.cast(typing.Optional[MonitoringAlertPolicyAlertStrategy], result)

    @builtins.property
    def documentation(self) -> typing.Optional["MonitoringAlertPolicyDocumentation"]:
        '''documentation block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#documentation MonitoringAlertPolicy#documentation}
        '''
        result = self._values.get("documentation")
        return typing.cast(typing.Optional["MonitoringAlertPolicyDocumentation"], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the policy is enabled. The default is true.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#enabled MonitoringAlertPolicy#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#id MonitoringAlertPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_channels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Identifies the notification channels to which notifications should be sent when incidents are opened or closed or when new violations occur on an already opened incident.

        Each element of this array corresponds
        to the name field in each of the NotificationChannel objects that are
        returned from the notificationChannels.list method. The syntax of the
        entries in this field is
        'projects/[PROJECT_ID]/notificationChannels/[CHANNEL_ID]'

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#notification_channels MonitoringAlertPolicy#notification_channels}
        '''
        result = self._values.get("notification_channels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#project MonitoringAlertPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitoringAlertPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#timeouts MonitoringAlertPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitoringAlertPolicyTimeouts"], result)

    @builtins.property
    def user_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''This field is intended to be used for organizing and identifying the AlertPolicy objects.The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#user_labels MonitoringAlertPolicy#user_labels}
        '''
        result = self._values.get("user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyCreationRecord",
    jsii_struct_bases=[],
    name_mapping={},
)
class MonitoringAlertPolicyCreationRecord:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyCreationRecord(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyCreationRecordList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyCreationRecordList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef60a7f3b6c70e7f347164fb0c7f034ea002401591ddb015b9d5ab7b872387a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitoringAlertPolicyCreationRecordOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb068f8b79b3a113aa17b3a71f4d6a5f2d944009987a78f419ae2f357ccc8c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitoringAlertPolicyCreationRecordOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ddd6cc16780ba8528a3dc77c8cba15b204f104dd48100d28b7c86f48be55e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4102d1f7f6c78d3609af1bdfa1b6055462cb070f3d916d272b36cddd640efc64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__572437330167e578204fcf6b9c8b12434252fdecf4a8f1c5473573636d8bb503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class MonitoringAlertPolicyCreationRecordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyCreationRecordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__843d295560ee1eafd6145f8a4f9a3bbc22b1f8ee37c7938386d8f4804632d088)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="mutatedBy")
    def mutated_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mutatedBy"))

    @builtins.property
    @jsii.member(jsii_name="mutateTime")
    def mutate_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mutateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitoringAlertPolicyCreationRecord]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyCreationRecord], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringAlertPolicyCreationRecord],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6269448ef8cca111c580c36149fae84ff00b6a00597ec9fa908593e0a4cc4d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyDocumentation",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "mime_type": "mimeType"},
)
class MonitoringAlertPolicyDocumentation:
    def __init__(
        self,
        *,
        content: typing.Optional[builtins.str] = None,
        mime_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: The text of the documentation, interpreted according to mimeType. The content may not exceed 8,192 Unicode characters and may not exceed more than 10,240 bytes when encoded in UTF-8 format, whichever is smaller. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#content MonitoringAlertPolicy#content}
        :param mime_type: The format of the content field. Presently, only the value "text/markdown" is supported. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#mime_type MonitoringAlertPolicy#mime_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71319047c287190f09c6488011b7b09984c691bdd1620ebb01f5b20a3d4f7980)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument mime_type", value=mime_type, expected_type=type_hints["mime_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content is not None:
            self._values["content"] = content
        if mime_type is not None:
            self._values["mime_type"] = mime_type

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''The text of the documentation, interpreted according to mimeType.

        The content may not exceed 8,192 Unicode characters and may not
        exceed more than 10,240 bytes when encoded in UTF-8 format,
        whichever is smaller.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#content MonitoringAlertPolicy#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mime_type(self) -> typing.Optional[builtins.str]:
        '''The format of the content field. Presently, only the value "text/markdown" is supported.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#mime_type MonitoringAlertPolicy#mime_type}
        '''
        result = self._values.get("mime_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyDocumentation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyDocumentationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyDocumentationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__629ded6117f72c2ab16684296a91cbc792d501c53fe9d04da038c0388480baf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetMimeType")
    def reset_mime_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMimeType", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="mimeTypeInput")
    def mime_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mimeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bcf2493429ea789be43603fafedd72c034e3b09d5bb79f60e7006c344d35e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="mimeType")
    def mime_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mimeType"))

    @mime_type.setter
    def mime_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b1bca65f5ab7756c79afd0029077eb0ed3d7dbfa3ea7f9e28ec76c2e21ebc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mimeType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitoringAlertPolicyDocumentation]:
        return typing.cast(typing.Optional[MonitoringAlertPolicyDocumentation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitoringAlertPolicyDocumentation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49a7b217717f6bef285f4df5d770f12647892011e515d9593f326678c862485e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MonitoringAlertPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#create MonitoringAlertPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#delete MonitoringAlertPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#update MonitoringAlertPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96265b5b927dc6856b472696da9ee7a07e45fe846e20dd3044dae7db081ac71f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#create MonitoringAlertPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#delete MonitoringAlertPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/monitoring_alert_policy#update MonitoringAlertPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringAlertPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitoringAlertPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.monitoringAlertPolicy.MonitoringAlertPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8b876b49414062864ffdeed8e9d3aab39d07312319675139298ee3d0667d866)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6406bf71533db74bf8dd21bf865f4615801aebd04d34964b755c1564b163eeff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939ae86382e1f175b4f328a3a8cc84d4a67f3ce59cfd7c48895cc246af7781db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37413e72c055c2be3cf88a7d15e91727f6fc83e6179dbf7b08998fa4f9972e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitoringAlertPolicyTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitoringAlertPolicyTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitoringAlertPolicyTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b9a06561770752cfb6096c59593cf22f8b027f4f2e107c3e0c5c1b80a16b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MonitoringAlertPolicy",
    "MonitoringAlertPolicyAlertStrategy",
    "MonitoringAlertPolicyAlertStrategyNotificationRateLimit",
    "MonitoringAlertPolicyAlertStrategyNotificationRateLimitOutputReference",
    "MonitoringAlertPolicyAlertStrategyOutputReference",
    "MonitoringAlertPolicyConditions",
    "MonitoringAlertPolicyConditionsConditionAbsent",
    "MonitoringAlertPolicyConditionsConditionAbsentAggregations",
    "MonitoringAlertPolicyConditionsConditionAbsentAggregationsList",
    "MonitoringAlertPolicyConditionsConditionAbsentAggregationsOutputReference",
    "MonitoringAlertPolicyConditionsConditionAbsentOutputReference",
    "MonitoringAlertPolicyConditionsConditionAbsentTrigger",
    "MonitoringAlertPolicyConditionsConditionAbsentTriggerOutputReference",
    "MonitoringAlertPolicyConditionsConditionMatchedLog",
    "MonitoringAlertPolicyConditionsConditionMatchedLogOutputReference",
    "MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage",
    "MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageOutputReference",
    "MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger",
    "MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTriggerOutputReference",
    "MonitoringAlertPolicyConditionsConditionThreshold",
    "MonitoringAlertPolicyConditionsConditionThresholdAggregations",
    "MonitoringAlertPolicyConditionsConditionThresholdAggregationsList",
    "MonitoringAlertPolicyConditionsConditionThresholdAggregationsOutputReference",
    "MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations",
    "MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregationsList",
    "MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregationsOutputReference",
    "MonitoringAlertPolicyConditionsConditionThresholdOutputReference",
    "MonitoringAlertPolicyConditionsConditionThresholdTrigger",
    "MonitoringAlertPolicyConditionsConditionThresholdTriggerOutputReference",
    "MonitoringAlertPolicyConditionsList",
    "MonitoringAlertPolicyConditionsOutputReference",
    "MonitoringAlertPolicyConfig",
    "MonitoringAlertPolicyCreationRecord",
    "MonitoringAlertPolicyCreationRecordList",
    "MonitoringAlertPolicyCreationRecordOutputReference",
    "MonitoringAlertPolicyDocumentation",
    "MonitoringAlertPolicyDocumentationOutputReference",
    "MonitoringAlertPolicyTimeouts",
    "MonitoringAlertPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f4dede7ed28781086f3815ef1819ea5dd0b5fd4d8e952fd9448b8d887f5e4f49(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    combiner: builtins.str,
    conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
    display_name: builtins.str,
    alert_strategy: typing.Optional[typing.Union[MonitoringAlertPolicyAlertStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    documentation: typing.Optional[typing.Union[MonitoringAlertPolicyDocumentation, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MonitoringAlertPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__60514aecb51156ded1a1b39649b9320636c74f0ce412890e6ed36902e3fd78f0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3d392318d0d33693652f53d055be463faeb5d128d51dfe9c977a935fe782c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66032d2a474eb481c11569f23ddfca35a10c4a8f13d78ca04cec5ea10af0b94e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847e820255288b77ff7df41d441ec46a9340b81fcf37e91441e276e17d2b5b0f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a3376a4aa0e22273583e080b4686065efd0f482d070fc24fb429c2a12fc971(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34425d599d535b622470828a517aeecc8523b87a3f3c12556ecaf4cdc64352a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db54bced32ba987482bd15f4da7f4e0ee59bfb9c60f2f9707f69eb455bb7cb36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73684cff2b7b8cae8822a5f3fbe4d40e5377280360c5d854da900712c192b23(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2364dbbe9665488b8e2e79e86ec303a1b1c70ef470ef8efebcb6896f887158d8(
    *,
    auto_close: typing.Optional[builtins.str] = None,
    notification_rate_limit: typing.Optional[typing.Union[MonitoringAlertPolicyAlertStrategyNotificationRateLimit, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__084f3c444b7a690363c4356877bebe5ebc426259fcfb7ad3943703c9ab0c9f50(
    *,
    period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89046ec4f094dfa079409286539dd01b9df4abcf05e7ca0726998c85af1e9f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0bfe0944af6b9c6afb2cd637d7685f3c07ccafba310cc016b68bfc2e5f65ec4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc77428c39cc354ce33fe4b030e7396cd31627aaf3af64d5fb0d9c2bc899fb46(
    value: typing.Optional[MonitoringAlertPolicyAlertStrategyNotificationRateLimit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d3abe12bab58bb47709a209a09d622af39a0cd6bea9b1e8e195b263175535c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3999bc002b969b9c7dd78dcef689eab1b1cc83f807299e30ed128ba88ce47cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11b78d9b760098f3a9af7bd61abe074871305e29c82a0680c203781dca16bad(
    value: typing.Optional[MonitoringAlertPolicyAlertStrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4161648379b85387e461783e402b170bf33dd7551ae25e82adb3d0b8db2a340(
    *,
    display_name: builtins.str,
    condition_absent: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionAbsent, typing.Dict[builtins.str, typing.Any]]] = None,
    condition_matched_log: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionMatchedLog, typing.Dict[builtins.str, typing.Any]]] = None,
    condition_monitoring_query_language: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage, typing.Dict[builtins.str, typing.Any]]] = None,
    condition_threshold: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409a36add30e1115098721c7644e970fe0638bdd8d6e3cb7aaacb11e1765f90e(
    *,
    duration: builtins.str,
    aggregations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionAbsentAggregations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter: typing.Optional[builtins.str] = None,
    trigger: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionAbsentTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3e08d55a94fa994436873c2070762ab9690de187fc1a7774a3dcd84252d1d6(
    *,
    alignment_period: typing.Optional[builtins.str] = None,
    cross_series_reducer: typing.Optional[builtins.str] = None,
    group_by_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    per_series_aligner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69650333d52ba2eaac35b99e8a0807b6b03b0b944c9757114b908aaff1ad1d32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b8876f7e64011b41429f767f3b312b52de74f8a81182a462848bd343746620(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe01c79a8613eb51923c5d5130645682295cf969f6b7da779e3df5cf59a5a67d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef88bed33cf5178b939b838b08550edac0416543294d95adfe90476ff38b45e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b80a6bc9dc38deab00050b79bd2adfd032202a1ad63b67e0d2947c942df8f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251eb0995135cabd17d017b6758167b5d776b184011b9c7f617691af35bd203f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionAbsentAggregations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f4598994dd29c29bef6559883765e53125524d308f52a95ad15cd123343647(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__384479429fc2df813fc96021a73784630b80625c425f193210aa44d36549a215(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b02ae75baa6983e3dac993770c13f54226493c639f04b1fb9f3aa5e4edc272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d03cb97f8448170d7a49c895d7a666615c7480752a25c0e906f6ce86360431(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34723f6a20216852632235e8464e9a8f41173e741913048cdf69ea85388511dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c712fd793c60616563e3decf83b759c1f9855221c74ad0077fd7cddb92e99be(
    value: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionAbsentAggregations, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7666d05aedd204214e08160cde0472bfc399378fac8c4d9135946c7682fee34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee16bc44fb36fde89cc79567b88c0cf69b095bc6efdeb0c346dc24b566ff11ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionAbsentAggregations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d874da3c1514b76bfd1d654aa28dbe4709a6787ca895e4dfda1d99cd34c162c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774f0252d30c2f665153febfffd6f020fb170cc828fdf94d0e233c6bc0f66311(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d72db521b454e002142e9e8af4ee9841faa733d3a06bf9483a54bb2e18b46fa(
    value: typing.Optional[MonitoringAlertPolicyConditionsConditionAbsent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a1f5daefceaa164a95b07da04c060fa9bf602d2c9b51882604cd470b93c0af(
    *,
    count: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f328b46ac9aa1533a884a63e3d630e90fe2d206c48085b9e1684aad499f0d93b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b2b5999c3d285ed7e4f8a376441d9fcfc9ed68c033bf782b4cceff68a1a82b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b0290ca17ad1a8441516f914b91107978584345172e936a1d468baaca53659(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177ea7ed71a8c2e9b61311ece52eb4d8d8aa7a6a46f71df1419a7d29b717e82b(
    value: typing.Optional[MonitoringAlertPolicyConditionsConditionAbsentTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe545dc7153670ced08e4e26d712983aa566e5e036a59f8aeb91ae2706721935(
    *,
    filter: builtins.str,
    label_extractors: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fc8a2c7888fad38b1946597252a7ff69385c9859410c4f0146a9872c2c60fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf2a93548cf13298d1f5d153b9bf0639cce007fa847448c9d4f6958a49dc72d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511c79a579cfcde5adbf7f64f59f4c92ee4e61dcff4a94681face990e7469452(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630e65c564d1b7a5d75f99d4013e087f63fd45f9bbc3e253e64ae08b34a6e933(
    value: typing.Optional[MonitoringAlertPolicyConditionsConditionMatchedLog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2151750a297ba1c00c893ebdedc2bbe570100713d4337544d483afdcaff44897(
    *,
    duration: builtins.str,
    query: builtins.str,
    evaluation_missing_data: typing.Optional[builtins.str] = None,
    trigger: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20c2869ffa7599836025eed635c71f62cc98e20c84174548462126ee3e6140f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb946fe85d87cc98a2ef672d22f1437659daf8d46ba10e5aa83a188df51e7c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66315cf97429cd49fb7a5e744127196e20b0231c1f89df022b0ae700f29fa601(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe4e2adddf4b5570568a0305028f4471084f47ee924073aefd1f9a8f3fa6dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86dd8de4968a47c29e1bfb236a314b1f68f76957d190708de073d733d971953a(
    value: typing.Optional[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853a1c44faf1ca74bf50f298c7f09e1a7840360b9ba0cf14d597298bd8bd9a00(
    *,
    count: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8945e528c29bf2719d541a51fa26e7cf97b31faf49209c44a1dd672d75a26ab2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d267a71cd77825d8fe70a0f1ee05cb58719cd812b9ae80950a813cd7290368(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5398a6f640e5488c8576d29160bc67077fc88b107820e0c0342f885a2ef02da2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48e76021d20fe524d91397b405a71a101573c3281f0c14db7a9f88cbf4aade6(
    value: typing.Optional[MonitoringAlertPolicyConditionsConditionMonitoringQueryLanguageTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98970952b6b65f11fac6e7d16f6fedf157165a6f9a12b86f038c4d06ca775e0c(
    *,
    comparison: builtins.str,
    duration: builtins.str,
    aggregations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdAggregations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    denominator_aggregations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    denominator_filter: typing.Optional[builtins.str] = None,
    evaluation_missing_data: typing.Optional[builtins.str] = None,
    filter: typing.Optional[builtins.str] = None,
    threshold_value: typing.Optional[jsii.Number] = None,
    trigger: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59366f4d9e9f8e0f5fa353585d37c682274dccfb9b1c0b4a9f0b0cc12b052299(
    *,
    alignment_period: typing.Optional[builtins.str] = None,
    cross_series_reducer: typing.Optional[builtins.str] = None,
    group_by_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    per_series_aligner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7463ef907f8cbddfa0f854b73bd9fa7b74e9143761bc797b640069bf381eb21b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52305c1c64ccb5d7c71a2aa0dcb416a2f4f978640a92c739b8b3371bf852872(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55704b013c7220a77268ffbaca38ee8c8c50a72da943abfb3920693d40f4be7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1d2084149246fbe7f8bb82c75f5381d0bb822b28e80aa029ba1c8777f73511(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a1fb538aea7214b16e06119c9b5c3441c2bc2f30278ba56a57a7016fb53889(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824e6273f19e3cf171d6782d611fd9b2aac96d07499858b2a3fc127cde5964d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdAggregations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f5d0e4398cc369b3d34bc3003a0fe3a6199efafd181c4da0648cdcd2f7e493(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a85fc7d82660e6c1e6be9591aa674a72e6a8e0bf074f3b1cc4b9f7a0fcf431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63a55f2c39724af6e8209c2c3a19cd2950cdaf6866956f45daac95c4762a9a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45809104ec5dc1c1eb825527ce27ab14db1ee6d419ff207393e45f1e15bb2986(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42a2cd13942b0287ed02ed4d52e45e2a9036e2ca25ae9dc9be387f710ca1852(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49bada02f5f02269c5477117fb4b694317bbaed73053b38d389b24d179e9368(
    value: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdAggregations, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c2229303ea64067d702107df485d8fefe5b77846a941a7d87bbb11fb7a20ce(
    *,
    alignment_period: typing.Optional[builtins.str] = None,
    cross_series_reducer: typing.Optional[builtins.str] = None,
    group_by_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    per_series_aligner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72eda0291ce2d28ce67612649a15fe6c7d7650dc7b20357267c69114814f30d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c54e3ff60b97383bc2f6ff5df6c88886954c5aca3577e8ae422eb8457eb4501(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb53c308f4610ff94ed08bae2d804cd096b58d7c6ee629d7c3c98d7c825197e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721b4c71e5592b31167e5c1d67280f5d44c8e62ead49403d94074ec5c719bbe8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0096d7e92d7000815f4c9259f94d21f87b295db2ae36c6cd3a5d03fd9abbc73(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccdc50429aa1f9d299313ffb578048cdf6cbecd2dd1a291e5aa7a76bba76b16e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c5a947d2196f02a804348872817a6bbb6c43192461e7060c352b81e5fb03d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c38e1c7e03e39f082563836bfd5092169dd61386a515f7eaaee0ddbf90a13a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311a97db0f5a0efcf526cfedd50f3bfe9fe304e3d50bf3a64c6fb079fa2fc58b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48d3a7232685d4da3bbdca88250309dda3e488da14b225f346f9b7a5a3c72c9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0edb8833d2c6ca750fce808d57093c8fb51bd96c655b317bd61fbb0116a2adeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9ea7c089fa3f41d5b8d802f563b46dbd4c959ef4d235746998715f3796046a(
    value: typing.Optional[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16e3a2fecfeb1f1ab98fb79b2fb7f99855d5bed1a4a4a853d52c28d0bbb978b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86024bf7c756e71909cced138ae53a30cab4867d9f33e2dba83e28ef96a045cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdAggregations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8fc8f7e47fc33fd5a30841f2d1e2eec4231cbbf36d1dd0656c35ac291fbd4a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditionsConditionThresholdDenominatorAggregations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7091e5a19c4dec4c225fb4e152e5b59465096e2757db2a5d025ab9d4a570cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2dd0fa5f600156aa57b82b20003f4017168b1e9de7448bbc40a812463f8b161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664689d0f74408aa11c496e4d4fb6c37e44f3e22958303435b9ee4cb999977c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e0a7c5531629f0b08257285193b41743ad18aba98a28c831618137717e7613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74468bfd11f1197330ae3b85e1391869ab9afb55708b663a1ee9880f6c0234b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a56ad7cf405da0fd02780d1fdd0a997b059f632281a8792cc101ff534eb9fcb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92274b7248c1942b6dd3ebac26d63f218949c8d328d88b788f256a365b16ab3(
    value: typing.Optional[MonitoringAlertPolicyConditionsConditionThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997d53444c6bcb5973e21890e2c130ee3d5cec7fe707fe86424251f43c4edbd1(
    *,
    count: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c8332d2f9c1052dcb2f5e6c2b7156190c6a719c06d153791d93e0881396c5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1c2c20716a9282c4fc78391c06f90a12762a1d01d3ca328cf6cd52f1a2d8ab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879ca1b470fab87acd371064c592496bde97f78c02cea0b99f8bab8c8056c94e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6b7911589b80ebdd814ef8bc24017d70ce805510b98725bdc79e9c2f29407b(
    value: typing.Optional[MonitoringAlertPolicyConditionsConditionThresholdTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4732fb3dc33dd39f5ed314728d190ab1db640f1e195ff8ffed9819e264c21b22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5dbad5661a4d8db1f959f6e7e1d99105592b563f8b567eb8362a3daace05db(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c898e571d88494437275e3a4879b3db511ae76f230dfcf7f7092b0bf98551e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd999ce7c43a462c9c3e28896aedefc5188d209699278f1fddbce78565b5bf4a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b927d4209ba8ebdda315f8e1b1961fa810217f36a117208152cb6d25b52261a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7ee5c76f7bd96e9c4e8eaddcee2f81d95eb7c8f72b5598c4f69967289aab3e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitoringAlertPolicyConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758a7feb4e9c2e0e3e626c0371a291f541cc26219911df25f9c3f41182c3f5ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6cb1fb687418569edf80ab44200aa852e6f63e2a28f2a3d88b9e5b13ea3c4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028814361c62933ca120a56a51c8be4e1c570138953c4fab24547830a739d215(
    value: typing.Optional[typing.Union[MonitoringAlertPolicyConditions, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b10165cb559bd919d435310ff920de2092b9d41dce03821f0a09f022bc69c0e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    combiner: builtins.str,
    conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitoringAlertPolicyConditions, typing.Dict[builtins.str, typing.Any]]]],
    display_name: builtins.str,
    alert_strategy: typing.Optional[typing.Union[MonitoringAlertPolicyAlertStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    documentation: typing.Optional[typing.Union[MonitoringAlertPolicyDocumentation, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    notification_channels: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MonitoringAlertPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef60a7f3b6c70e7f347164fb0c7f034ea002401591ddb015b9d5ab7b872387a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb068f8b79b3a113aa17b3a71f4d6a5f2d944009987a78f419ae2f357ccc8c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ddd6cc16780ba8528a3dc77c8cba15b204f104dd48100d28b7c86f48be55e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4102d1f7f6c78d3609af1bdfa1b6055462cb070f3d916d272b36cddd640efc64(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572437330167e578204fcf6b9c8b12434252fdecf4a8f1c5473573636d8bb503(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843d295560ee1eafd6145f8a4f9a3bbc22b1f8ee37c7938386d8f4804632d088(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6269448ef8cca111c580c36149fae84ff00b6a00597ec9fa908593e0a4cc4d61(
    value: typing.Optional[MonitoringAlertPolicyCreationRecord],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71319047c287190f09c6488011b7b09984c691bdd1620ebb01f5b20a3d4f7980(
    *,
    content: typing.Optional[builtins.str] = None,
    mime_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629ded6117f72c2ab16684296a91cbc792d501c53fe9d04da038c0388480baf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1bcf2493429ea789be43603fafedd72c034e3b09d5bb79f60e7006c344d35e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b1bca65f5ab7756c79afd0029077eb0ed3d7dbfa3ea7f9e28ec76c2e21ebc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a7b217717f6bef285f4df5d770f12647892011e515d9593f326678c862485e(
    value: typing.Optional[MonitoringAlertPolicyDocumentation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96265b5b927dc6856b472696da9ee7a07e45fe846e20dd3044dae7db081ac71f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b876b49414062864ffdeed8e9d3aab39d07312319675139298ee3d0667d866(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6406bf71533db74bf8dd21bf865f4615801aebd04d34964b755c1564b163eeff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939ae86382e1f175b4f328a3a8cc84d4a67f3ce59cfd7c48895cc246af7781db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37413e72c055c2be3cf88a7d15e91727f6fc83e6179dbf7b08998fa4f9972e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b9a06561770752cfb6096c59593cf22f8b027f4f2e107c3e0c5c1b80a16b52(
    value: typing.Optional[typing.Union[MonitoringAlertPolicyTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
