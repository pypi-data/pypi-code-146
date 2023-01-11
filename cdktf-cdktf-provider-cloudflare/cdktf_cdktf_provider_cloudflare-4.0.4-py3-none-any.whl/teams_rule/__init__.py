'''
# `cloudflare_teams_rule`

Refer to the Terraform Registory for docs: [`cloudflare_teams_rule`](https://www.terraform.io/docs/providers/cloudflare/r/teams_rule).
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


class TeamsRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsRule.TeamsRule",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule cloudflare_teams_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        action: builtins.str,
        description: builtins.str,
        name: builtins.str,
        precedence: jsii.Number,
        device_posture: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[builtins.str] = None,
        rule_settings: typing.Optional[typing.Union["TeamsRuleRuleSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule cloudflare_teams_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#account_id TeamsRule#account_id}
        :param action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#action TeamsRule#action}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#description TeamsRule#description}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#name TeamsRule#name}.
        :param precedence: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#precedence TeamsRule#precedence}.
        :param device_posture: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#device_posture TeamsRule#device_posture}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#enabled TeamsRule#enabled}.
        :param filters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#filters TeamsRule#filters}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#id TeamsRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#identity TeamsRule#identity}.
        :param rule_settings: rule_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#rule_settings TeamsRule#rule_settings}
        :param traffic: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#traffic TeamsRule#traffic}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4e342b2cb92c5948e44188454b91a51aa7ff0d5e5b211d9801bfa8e09ae930)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = TeamsRuleConfig(
            account_id=account_id,
            action=action,
            description=description,
            name=name,
            precedence=precedence,
            device_posture=device_posture,
            enabled=enabled,
            filters=filters,
            id=id,
            identity=identity,
            rule_settings=rule_settings,
            traffic=traffic,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putRuleSettings")
    def put_rule_settings(
        self,
        *,
        add_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        biso_admin_controls: typing.Optional[typing.Union["TeamsRuleRuleSettingsBisoAdminControls", typing.Dict[builtins.str, typing.Any]]] = None,
        block_page_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        block_page_reason: typing.Optional[builtins.str] = None,
        check_session: typing.Optional[typing.Union["TeamsRuleRuleSettingsCheckSession", typing.Dict[builtins.str, typing.Any]]] = None,
        insecure_disable_dnssec_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        l4_override: typing.Optional[typing.Union["TeamsRuleRuleSettingsL4Override", typing.Dict[builtins.str, typing.Any]]] = None,
        override_host: typing.Optional[builtins.str] = None,
        override_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param add_headers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#add_headers TeamsRule#add_headers}.
        :param biso_admin_controls: biso_admin_controls block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#biso_admin_controls TeamsRule#biso_admin_controls}
        :param block_page_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#block_page_enabled TeamsRule#block_page_enabled}.
        :param block_page_reason: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#block_page_reason TeamsRule#block_page_reason}.
        :param check_session: check_session block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#check_session TeamsRule#check_session}
        :param insecure_disable_dnssec_validation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#insecure_disable_dnssec_validation TeamsRule#insecure_disable_dnssec_validation}.
        :param l4_override: l4override block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#l4override TeamsRule#l4override}
        :param override_host: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#override_host TeamsRule#override_host}.
        :param override_ips: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#override_ips TeamsRule#override_ips}.
        '''
        value = TeamsRuleRuleSettings(
            add_headers=add_headers,
            biso_admin_controls=biso_admin_controls,
            block_page_enabled=block_page_enabled,
            block_page_reason=block_page_reason,
            check_session=check_session,
            insecure_disable_dnssec_validation=insecure_disable_dnssec_validation,
            l4_override=l4_override,
            override_host=override_host,
            override_ips=override_ips,
        )

        return typing.cast(None, jsii.invoke(self, "putRuleSettings", [value]))

    @jsii.member(jsii_name="resetDevicePosture")
    def reset_device_posture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevicePosture", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFilters")
    def reset_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilters", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetRuleSettings")
    def reset_rule_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleSettings", []))

    @jsii.member(jsii_name="resetTraffic")
    def reset_traffic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraffic", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="ruleSettings")
    def rule_settings(self) -> "TeamsRuleRuleSettingsOutputReference":
        return typing.cast("TeamsRuleRuleSettingsOutputReference", jsii.get(self, "ruleSettings"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="devicePostureInput")
    def device_posture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "devicePostureInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filtersInput")
    def filters_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "filtersInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="precedenceInput")
    def precedence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "precedenceInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleSettingsInput")
    def rule_settings_input(self) -> typing.Optional["TeamsRuleRuleSettings"]:
        return typing.cast(typing.Optional["TeamsRuleRuleSettings"], jsii.get(self, "ruleSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficInput")
    def traffic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trafficInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416f83bebf6e7bf8ae9d66755d0e670477897f80ae783b8d3b95ad4c8d7c7c33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d94b029af48248d3107fb55460eb2bc09ed4ef50d863df6b6edd059f59551f3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a4257557fd0fd94512ca4734c3aa7aecec26e6d954b2706e852c0d64b99572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="devicePosture")
    def device_posture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "devicePosture"))

    @device_posture.setter
    def device_posture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05fe3df17eaecfd11fd847f23e704389aa770870817810ae8f0e4e30195ad50a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "devicePosture", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__cc67b1694782612d5a16746e31d4fb9240ddebd77adf6db38453dbea55c29dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "filters"))

    @filters.setter
    def filters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e7f6eb6bcc8d63e3af6c7a4535b644484a96981f56cf087d28a8d39ef1022f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filters", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f8435e849c076986b45a68dbedb290d88b2753a34bac28e6a86e9d14d4e5233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identity"))

    @identity.setter
    def identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80fce5279d4e22c53a01e251ad7fe838bf8030fe6b10bcc471ee936fd7be871c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identity", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea85cd5e1d6e42381426c17a11cb316e0af3f90e884e84e8c3687556d8c1e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="precedence")
    def precedence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precedence"))

    @precedence.setter
    def precedence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d1766070835a96c29e707c97ff7985a4860a5aea5463242bee4e42f9a3ffeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "precedence", value)

    @builtins.property
    @jsii.member(jsii_name="traffic")
    def traffic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traffic"))

    @traffic.setter
    def traffic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8675a886cf74a176548b18ca6a0cbf5a41f34e80c2088a4db89bf06f7f6f29a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traffic", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsRule.TeamsRuleConfig",
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
        "action": "action",
        "description": "description",
        "name": "name",
        "precedence": "precedence",
        "device_posture": "devicePosture",
        "enabled": "enabled",
        "filters": "filters",
        "id": "id",
        "identity": "identity",
        "rule_settings": "ruleSettings",
        "traffic": "traffic",
    },
)
class TeamsRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action: builtins.str,
        description: builtins.str,
        name: builtins.str,
        precedence: jsii.Number,
        device_posture: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[builtins.str] = None,
        rule_settings: typing.Optional[typing.Union["TeamsRuleRuleSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#account_id TeamsRule#account_id}
        :param action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#action TeamsRule#action}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#description TeamsRule#description}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#name TeamsRule#name}.
        :param precedence: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#precedence TeamsRule#precedence}.
        :param device_posture: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#device_posture TeamsRule#device_posture}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#enabled TeamsRule#enabled}.
        :param filters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#filters TeamsRule#filters}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#id TeamsRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#identity TeamsRule#identity}.
        :param rule_settings: rule_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#rule_settings TeamsRule#rule_settings}
        :param traffic: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#traffic TeamsRule#traffic}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(rule_settings, dict):
            rule_settings = TeamsRuleRuleSettings(**rule_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3effa16ab2128e4e494cd72c1bd18a0fb3bca5dcab8c31fcf49ce3119d0d52a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument precedence", value=precedence, expected_type=type_hints["precedence"])
            check_type(argname="argument device_posture", value=device_posture, expected_type=type_hints["device_posture"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument rule_settings", value=rule_settings, expected_type=type_hints["rule_settings"])
            check_type(argname="argument traffic", value=traffic, expected_type=type_hints["traffic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "action": action,
            "description": description,
            "name": name,
            "precedence": precedence,
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
        if device_posture is not None:
            self._values["device_posture"] = device_posture
        if enabled is not None:
            self._values["enabled"] = enabled
        if filters is not None:
            self._values["filters"] = filters
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if rule_settings is not None:
            self._values["rule_settings"] = rule_settings
        if traffic is not None:
            self._values["traffic"] = traffic

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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#account_id TeamsRule#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#action TeamsRule#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#description TeamsRule#description}.'''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#name TeamsRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def precedence(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#precedence TeamsRule#precedence}.'''
        result = self._values.get("precedence")
        assert result is not None, "Required property 'precedence' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def device_posture(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#device_posture TeamsRule#device_posture}.'''
        result = self._values.get("device_posture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#enabled TeamsRule#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#filters TeamsRule#filters}.'''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#id TeamsRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#identity TeamsRule#identity}.'''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_settings(self) -> typing.Optional["TeamsRuleRuleSettings"]:
        '''rule_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#rule_settings TeamsRule#rule_settings}
        '''
        result = self._values.get("rule_settings")
        return typing.cast(typing.Optional["TeamsRuleRuleSettings"], result)

    @builtins.property
    def traffic(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#traffic TeamsRule#traffic}.'''
        result = self._values.get("traffic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsRule.TeamsRuleRuleSettings",
    jsii_struct_bases=[],
    name_mapping={
        "add_headers": "addHeaders",
        "biso_admin_controls": "bisoAdminControls",
        "block_page_enabled": "blockPageEnabled",
        "block_page_reason": "blockPageReason",
        "check_session": "checkSession",
        "insecure_disable_dnssec_validation": "insecureDisableDnssecValidation",
        "l4_override": "l4Override",
        "override_host": "overrideHost",
        "override_ips": "overrideIps",
    },
)
class TeamsRuleRuleSettings:
    def __init__(
        self,
        *,
        add_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        biso_admin_controls: typing.Optional[typing.Union["TeamsRuleRuleSettingsBisoAdminControls", typing.Dict[builtins.str, typing.Any]]] = None,
        block_page_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        block_page_reason: typing.Optional[builtins.str] = None,
        check_session: typing.Optional[typing.Union["TeamsRuleRuleSettingsCheckSession", typing.Dict[builtins.str, typing.Any]]] = None,
        insecure_disable_dnssec_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        l4_override: typing.Optional[typing.Union["TeamsRuleRuleSettingsL4Override", typing.Dict[builtins.str, typing.Any]]] = None,
        override_host: typing.Optional[builtins.str] = None,
        override_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param add_headers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#add_headers TeamsRule#add_headers}.
        :param biso_admin_controls: biso_admin_controls block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#biso_admin_controls TeamsRule#biso_admin_controls}
        :param block_page_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#block_page_enabled TeamsRule#block_page_enabled}.
        :param block_page_reason: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#block_page_reason TeamsRule#block_page_reason}.
        :param check_session: check_session block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#check_session TeamsRule#check_session}
        :param insecure_disable_dnssec_validation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#insecure_disable_dnssec_validation TeamsRule#insecure_disable_dnssec_validation}.
        :param l4_override: l4override block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#l4override TeamsRule#l4override}
        :param override_host: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#override_host TeamsRule#override_host}.
        :param override_ips: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#override_ips TeamsRule#override_ips}.
        '''
        if isinstance(biso_admin_controls, dict):
            biso_admin_controls = TeamsRuleRuleSettingsBisoAdminControls(**biso_admin_controls)
        if isinstance(check_session, dict):
            check_session = TeamsRuleRuleSettingsCheckSession(**check_session)
        if isinstance(l4_override, dict):
            l4_override = TeamsRuleRuleSettingsL4Override(**l4_override)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbd85acb07d8bc35ee710e905e6eb4e5535cdb3eb313c3a99615ded28b0bc14)
            check_type(argname="argument add_headers", value=add_headers, expected_type=type_hints["add_headers"])
            check_type(argname="argument biso_admin_controls", value=biso_admin_controls, expected_type=type_hints["biso_admin_controls"])
            check_type(argname="argument block_page_enabled", value=block_page_enabled, expected_type=type_hints["block_page_enabled"])
            check_type(argname="argument block_page_reason", value=block_page_reason, expected_type=type_hints["block_page_reason"])
            check_type(argname="argument check_session", value=check_session, expected_type=type_hints["check_session"])
            check_type(argname="argument insecure_disable_dnssec_validation", value=insecure_disable_dnssec_validation, expected_type=type_hints["insecure_disable_dnssec_validation"])
            check_type(argname="argument l4_override", value=l4_override, expected_type=type_hints["l4_override"])
            check_type(argname="argument override_host", value=override_host, expected_type=type_hints["override_host"])
            check_type(argname="argument override_ips", value=override_ips, expected_type=type_hints["override_ips"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_headers is not None:
            self._values["add_headers"] = add_headers
        if biso_admin_controls is not None:
            self._values["biso_admin_controls"] = biso_admin_controls
        if block_page_enabled is not None:
            self._values["block_page_enabled"] = block_page_enabled
        if block_page_reason is not None:
            self._values["block_page_reason"] = block_page_reason
        if check_session is not None:
            self._values["check_session"] = check_session
        if insecure_disable_dnssec_validation is not None:
            self._values["insecure_disable_dnssec_validation"] = insecure_disable_dnssec_validation
        if l4_override is not None:
            self._values["l4_override"] = l4_override
        if override_host is not None:
            self._values["override_host"] = override_host
        if override_ips is not None:
            self._values["override_ips"] = override_ips

    @builtins.property
    def add_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#add_headers TeamsRule#add_headers}.'''
        result = self._values.get("add_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def biso_admin_controls(
        self,
    ) -> typing.Optional["TeamsRuleRuleSettingsBisoAdminControls"]:
        '''biso_admin_controls block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#biso_admin_controls TeamsRule#biso_admin_controls}
        '''
        result = self._values.get("biso_admin_controls")
        return typing.cast(typing.Optional["TeamsRuleRuleSettingsBisoAdminControls"], result)

    @builtins.property
    def block_page_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#block_page_enabled TeamsRule#block_page_enabled}.'''
        result = self._values.get("block_page_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def block_page_reason(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#block_page_reason TeamsRule#block_page_reason}.'''
        result = self._values.get("block_page_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def check_session(self) -> typing.Optional["TeamsRuleRuleSettingsCheckSession"]:
        '''check_session block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#check_session TeamsRule#check_session}
        '''
        result = self._values.get("check_session")
        return typing.cast(typing.Optional["TeamsRuleRuleSettingsCheckSession"], result)

    @builtins.property
    def insecure_disable_dnssec_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#insecure_disable_dnssec_validation TeamsRule#insecure_disable_dnssec_validation}.'''
        result = self._values.get("insecure_disable_dnssec_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def l4_override(self) -> typing.Optional["TeamsRuleRuleSettingsL4Override"]:
        '''l4override block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#l4override TeamsRule#l4override}
        '''
        result = self._values.get("l4_override")
        return typing.cast(typing.Optional["TeamsRuleRuleSettingsL4Override"], result)

    @builtins.property
    def override_host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#override_host TeamsRule#override_host}.'''
        result = self._values.get("override_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def override_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#override_ips TeamsRule#override_ips}.'''
        result = self._values.get("override_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsRuleRuleSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsRule.TeamsRuleRuleSettingsBisoAdminControls",
    jsii_struct_bases=[],
    name_mapping={
        "disable_copy_paste": "disableCopyPaste",
        "disable_download": "disableDownload",
        "disable_keyboard": "disableKeyboard",
        "disable_printing": "disablePrinting",
        "disable_upload": "disableUpload",
    },
)
class TeamsRuleRuleSettingsBisoAdminControls:
    def __init__(
        self,
        *,
        disable_copy_paste: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_keyboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_printing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_upload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_copy_paste: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_copy_paste TeamsRule#disable_copy_paste}.
        :param disable_download: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_download TeamsRule#disable_download}.
        :param disable_keyboard: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_keyboard TeamsRule#disable_keyboard}.
        :param disable_printing: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_printing TeamsRule#disable_printing}.
        :param disable_upload: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_upload TeamsRule#disable_upload}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8b2a1cc4e29b1b8cb2edb13884ab1f20a8368313a448331b3937f5759faa3d)
            check_type(argname="argument disable_copy_paste", value=disable_copy_paste, expected_type=type_hints["disable_copy_paste"])
            check_type(argname="argument disable_download", value=disable_download, expected_type=type_hints["disable_download"])
            check_type(argname="argument disable_keyboard", value=disable_keyboard, expected_type=type_hints["disable_keyboard"])
            check_type(argname="argument disable_printing", value=disable_printing, expected_type=type_hints["disable_printing"])
            check_type(argname="argument disable_upload", value=disable_upload, expected_type=type_hints["disable_upload"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_copy_paste is not None:
            self._values["disable_copy_paste"] = disable_copy_paste
        if disable_download is not None:
            self._values["disable_download"] = disable_download
        if disable_keyboard is not None:
            self._values["disable_keyboard"] = disable_keyboard
        if disable_printing is not None:
            self._values["disable_printing"] = disable_printing
        if disable_upload is not None:
            self._values["disable_upload"] = disable_upload

    @builtins.property
    def disable_copy_paste(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_copy_paste TeamsRule#disable_copy_paste}.'''
        result = self._values.get("disable_copy_paste")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_download(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_download TeamsRule#disable_download}.'''
        result = self._values.get("disable_download")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_keyboard(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_keyboard TeamsRule#disable_keyboard}.'''
        result = self._values.get("disable_keyboard")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_printing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_printing TeamsRule#disable_printing}.'''
        result = self._values.get("disable_printing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_upload(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_upload TeamsRule#disable_upload}.'''
        result = self._values.get("disable_upload")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsRuleRuleSettingsBisoAdminControls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsRuleRuleSettingsBisoAdminControlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsRule.TeamsRuleRuleSettingsBisoAdminControlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c43355753706babcc2910822523a07649505aebef2bec77356a5808a9999da2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisableCopyPaste")
    def reset_disable_copy_paste(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableCopyPaste", []))

    @jsii.member(jsii_name="resetDisableDownload")
    def reset_disable_download(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableDownload", []))

    @jsii.member(jsii_name="resetDisableKeyboard")
    def reset_disable_keyboard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableKeyboard", []))

    @jsii.member(jsii_name="resetDisablePrinting")
    def reset_disable_printing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisablePrinting", []))

    @jsii.member(jsii_name="resetDisableUpload")
    def reset_disable_upload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableUpload", []))

    @builtins.property
    @jsii.member(jsii_name="disableCopyPasteInput")
    def disable_copy_paste_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableCopyPasteInput"))

    @builtins.property
    @jsii.member(jsii_name="disableDownloadInput")
    def disable_download_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableDownloadInput"))

    @builtins.property
    @jsii.member(jsii_name="disableKeyboardInput")
    def disable_keyboard_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableKeyboardInput"))

    @builtins.property
    @jsii.member(jsii_name="disablePrintingInput")
    def disable_printing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disablePrintingInput"))

    @builtins.property
    @jsii.member(jsii_name="disableUploadInput")
    def disable_upload_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableUploadInput"))

    @builtins.property
    @jsii.member(jsii_name="disableCopyPaste")
    def disable_copy_paste(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableCopyPaste"))

    @disable_copy_paste.setter
    def disable_copy_paste(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c07cded569ed72a51ded47da35c2dc1e89bd01753e1dfaf3decd3d325ccb686d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableCopyPaste", value)

    @builtins.property
    @jsii.member(jsii_name="disableDownload")
    def disable_download(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableDownload"))

    @disable_download.setter
    def disable_download(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d117c06108559c432dc8d1e581cad0033553c227a4a855fe99778e0a59e6e74e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableDownload", value)

    @builtins.property
    @jsii.member(jsii_name="disableKeyboard")
    def disable_keyboard(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableKeyboard"))

    @disable_keyboard.setter
    def disable_keyboard(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa35f16025a25779b3613f4189e1036a3316813c707eeb80976ff97972258613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableKeyboard", value)

    @builtins.property
    @jsii.member(jsii_name="disablePrinting")
    def disable_printing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disablePrinting"))

    @disable_printing.setter
    def disable_printing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d77c7724c3eb95440a411f92d9b7d3031625f3493d812ed4ff772097f58ea40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disablePrinting", value)

    @builtins.property
    @jsii.member(jsii_name="disableUpload")
    def disable_upload(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableUpload"))

    @disable_upload.setter
    def disable_upload(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bea932ab3d072ffceda6ef47b07845dcaa5b6d2516951d1137de225a48b974a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableUpload", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsRuleRuleSettingsBisoAdminControls]:
        return typing.cast(typing.Optional[TeamsRuleRuleSettingsBisoAdminControls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsRuleRuleSettingsBisoAdminControls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf1aea788e5d990f9da7eba9ea8a5cb2a922b8697739ab93f0c1f7a27bf0e22e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsRule.TeamsRuleRuleSettingsCheckSession",
    jsii_struct_bases=[],
    name_mapping={"duration": "duration", "enforce": "enforce"},
)
class TeamsRuleRuleSettingsCheckSession:
    def __init__(
        self,
        *,
        duration: builtins.str,
        enforce: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#duration TeamsRule#duration}.
        :param enforce: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#enforce TeamsRule#enforce}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6562f9f6b37bd5dce65106a92acb7de09d28f7bc0c2d562e0aee7839ed446242)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration": duration,
            "enforce": enforce,
        }

    @builtins.property
    def duration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#duration TeamsRule#duration}.'''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#enforce TeamsRule#enforce}.'''
        result = self._values.get("enforce")
        assert result is not None, "Required property 'enforce' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsRuleRuleSettingsCheckSession(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsRuleRuleSettingsCheckSessionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsRule.TeamsRuleRuleSettingsCheckSessionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1238ceef1f71b79b8a34929a998cc624e06cfc9676bcd1d41293b2ab82ccb44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f982e6cba0835a289cc247a5308077895df4c5c2fc7a4b7a5cb29ccba390aba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value)

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee19e11e0c03725f2bde7ba33bc0f418207d1b7cdf8c980d89488395a3f26a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsRuleRuleSettingsCheckSession]:
        return typing.cast(typing.Optional[TeamsRuleRuleSettingsCheckSession], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsRuleRuleSettingsCheckSession],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b42b0db18ccb17cfd365074ced19ad968e7b4f1d679f9820ccf057ee0c2ca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsRule.TeamsRuleRuleSettingsL4Override",
    jsii_struct_bases=[],
    name_mapping={"ip": "ip", "port": "port"},
)
class TeamsRuleRuleSettingsL4Override:
    def __init__(self, *, ip: builtins.str, port: jsii.Number) -> None:
        '''
        :param ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#ip TeamsRule#ip}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#port TeamsRule#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f677f3b527735bac7484a0db0b7272068363ff1030e6b1ab11edc457475c31)
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip": ip,
            "port": port,
        }

    @builtins.property
    def ip(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#ip TeamsRule#ip}.'''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#port TeamsRule#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsRuleRuleSettingsL4Override(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsRuleRuleSettingsL4OverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsRule.TeamsRuleRuleSettingsL4OverrideOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b38268da64b375013b4968be12c616b9543d82a787cfadcf50701b408dbefc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3716aa2ac1b6f966696d5812eb7f60a88b485f35398fab3af0940098f42a657)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7ce8c725d4e0831186fec3dc7fa220fdb5ed3a8dcaa22706bba8778a9d6abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsRuleRuleSettingsL4Override]:
        return typing.cast(typing.Optional[TeamsRuleRuleSettingsL4Override], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsRuleRuleSettingsL4Override],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0eab80105b842a9e40858c072742abccfd1fa0fe0dd263d7fb3d0df51dc2bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class TeamsRuleRuleSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsRule.TeamsRuleRuleSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a064ccdd2cd4acbaca0d11c82e1b71f6b2481337abe56ae98e890dc18294afc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBisoAdminControls")
    def put_biso_admin_controls(
        self,
        *,
        disable_copy_paste: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_keyboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_printing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_upload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_copy_paste: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_copy_paste TeamsRule#disable_copy_paste}.
        :param disable_download: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_download TeamsRule#disable_download}.
        :param disable_keyboard: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_keyboard TeamsRule#disable_keyboard}.
        :param disable_printing: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_printing TeamsRule#disable_printing}.
        :param disable_upload: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#disable_upload TeamsRule#disable_upload}.
        '''
        value = TeamsRuleRuleSettingsBisoAdminControls(
            disable_copy_paste=disable_copy_paste,
            disable_download=disable_download,
            disable_keyboard=disable_keyboard,
            disable_printing=disable_printing,
            disable_upload=disable_upload,
        )

        return typing.cast(None, jsii.invoke(self, "putBisoAdminControls", [value]))

    @jsii.member(jsii_name="putCheckSession")
    def put_check_session(
        self,
        *,
        duration: builtins.str,
        enforce: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#duration TeamsRule#duration}.
        :param enforce: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#enforce TeamsRule#enforce}.
        '''
        value = TeamsRuleRuleSettingsCheckSession(duration=duration, enforce=enforce)

        return typing.cast(None, jsii.invoke(self, "putCheckSession", [value]))

    @jsii.member(jsii_name="putL4Override")
    def put_l4_override(self, *, ip: builtins.str, port: jsii.Number) -> None:
        '''
        :param ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#ip TeamsRule#ip}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/teams_rule#port TeamsRule#port}.
        '''
        value = TeamsRuleRuleSettingsL4Override(ip=ip, port=port)

        return typing.cast(None, jsii.invoke(self, "putL4Override", [value]))

    @jsii.member(jsii_name="resetAddHeaders")
    def reset_add_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddHeaders", []))

    @jsii.member(jsii_name="resetBisoAdminControls")
    def reset_biso_admin_controls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBisoAdminControls", []))

    @jsii.member(jsii_name="resetBlockPageEnabled")
    def reset_block_page_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockPageEnabled", []))

    @jsii.member(jsii_name="resetBlockPageReason")
    def reset_block_page_reason(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockPageReason", []))

    @jsii.member(jsii_name="resetCheckSession")
    def reset_check_session(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckSession", []))

    @jsii.member(jsii_name="resetInsecureDisableDnssecValidation")
    def reset_insecure_disable_dnssec_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureDisableDnssecValidation", []))

    @jsii.member(jsii_name="resetL4Override")
    def reset_l4_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetL4Override", []))

    @jsii.member(jsii_name="resetOverrideHost")
    def reset_override_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideHost", []))

    @jsii.member(jsii_name="resetOverrideIps")
    def reset_override_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideIps", []))

    @builtins.property
    @jsii.member(jsii_name="bisoAdminControls")
    def biso_admin_controls(
        self,
    ) -> TeamsRuleRuleSettingsBisoAdminControlsOutputReference:
        return typing.cast(TeamsRuleRuleSettingsBisoAdminControlsOutputReference, jsii.get(self, "bisoAdminControls"))

    @builtins.property
    @jsii.member(jsii_name="checkSession")
    def check_session(self) -> TeamsRuleRuleSettingsCheckSessionOutputReference:
        return typing.cast(TeamsRuleRuleSettingsCheckSessionOutputReference, jsii.get(self, "checkSession"))

    @builtins.property
    @jsii.member(jsii_name="l4Override")
    def l4_override(self) -> TeamsRuleRuleSettingsL4OverrideOutputReference:
        return typing.cast(TeamsRuleRuleSettingsL4OverrideOutputReference, jsii.get(self, "l4Override"))

    @builtins.property
    @jsii.member(jsii_name="addHeadersInput")
    def add_headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "addHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="bisoAdminControlsInput")
    def biso_admin_controls_input(
        self,
    ) -> typing.Optional[TeamsRuleRuleSettingsBisoAdminControls]:
        return typing.cast(typing.Optional[TeamsRuleRuleSettingsBisoAdminControls], jsii.get(self, "bisoAdminControlsInput"))

    @builtins.property
    @jsii.member(jsii_name="blockPageEnabledInput")
    def block_page_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "blockPageEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="blockPageReasonInput")
    def block_page_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockPageReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="checkSessionInput")
    def check_session_input(self) -> typing.Optional[TeamsRuleRuleSettingsCheckSession]:
        return typing.cast(typing.Optional[TeamsRuleRuleSettingsCheckSession], jsii.get(self, "checkSessionInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureDisableDnssecValidationInput")
    def insecure_disable_dnssec_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureDisableDnssecValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="l4OverrideInput")
    def l4_override_input(self) -> typing.Optional[TeamsRuleRuleSettingsL4Override]:
        return typing.cast(typing.Optional[TeamsRuleRuleSettingsL4Override], jsii.get(self, "l4OverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideHostInput")
    def override_host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overrideHostInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideIpsInput")
    def override_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "overrideIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="addHeaders")
    def add_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "addHeaders"))

    @add_headers.setter
    def add_headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e21e76084ac4b20c1accaf0bcd912ad6d1e3576bb447eaa8d2425e2b4955441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addHeaders", value)

    @builtins.property
    @jsii.member(jsii_name="blockPageEnabled")
    def block_page_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "blockPageEnabled"))

    @block_page_enabled.setter
    def block_page_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc0380f5525e63d13319738ebf1280805edb9dbb90e4d34c7f5d3c323f2da4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockPageEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="blockPageReason")
    def block_page_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockPageReason"))

    @block_page_reason.setter
    def block_page_reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47c0150f24aef91b1a21146a2d983e28247c2cdade5a07f3fa8d7b89dd907b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockPageReason", value)

    @builtins.property
    @jsii.member(jsii_name="insecureDisableDnssecValidation")
    def insecure_disable_dnssec_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecureDisableDnssecValidation"))

    @insecure_disable_dnssec_validation.setter
    def insecure_disable_dnssec_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6466c2970a76a885c1e68bf22b8f3b92683c147b8c3e4dbe745c66f97d36ecfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureDisableDnssecValidation", value)

    @builtins.property
    @jsii.member(jsii_name="overrideHost")
    def override_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overrideHost"))

    @override_host.setter
    def override_host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d30dabad90ed03fcf67b04ad9831575125ad02f850326e014337470dee49a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideHost", value)

    @builtins.property
    @jsii.member(jsii_name="overrideIps")
    def override_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "overrideIps"))

    @override_ips.setter
    def override_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02460da3696f52fd990413a1e98be6cd417e4a3c74c23eca39510c43594bd175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideIps", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsRuleRuleSettings]:
        return typing.cast(typing.Optional[TeamsRuleRuleSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsRuleRuleSettings]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d3da8d5ba679e75837415eea3fb92ddee309dd464bbec5425ec290851d7a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "TeamsRule",
    "TeamsRuleConfig",
    "TeamsRuleRuleSettings",
    "TeamsRuleRuleSettingsBisoAdminControls",
    "TeamsRuleRuleSettingsBisoAdminControlsOutputReference",
    "TeamsRuleRuleSettingsCheckSession",
    "TeamsRuleRuleSettingsCheckSessionOutputReference",
    "TeamsRuleRuleSettingsL4Override",
    "TeamsRuleRuleSettingsL4OverrideOutputReference",
    "TeamsRuleRuleSettingsOutputReference",
]

publication.publish()

def _typecheckingstub__8d4e342b2cb92c5948e44188454b91a51aa7ff0d5e5b211d9801bfa8e09ae930(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    action: builtins.str,
    description: builtins.str,
    name: builtins.str,
    precedence: jsii.Number,
    device_posture: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[builtins.str] = None,
    rule_settings: typing.Optional[typing.Union[TeamsRuleRuleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__416f83bebf6e7bf8ae9d66755d0e670477897f80ae783b8d3b95ad4c8d7c7c33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94b029af48248d3107fb55460eb2bc09ed4ef50d863df6b6edd059f59551f3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a4257557fd0fd94512ca4734c3aa7aecec26e6d954b2706e852c0d64b99572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fe3df17eaecfd11fd847f23e704389aa770870817810ae8f0e4e30195ad50a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc67b1694782612d5a16746e31d4fb9240ddebd77adf6db38453dbea55c29dc0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7f6eb6bcc8d63e3af6c7a4535b644484a96981f56cf087d28a8d39ef1022f5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8435e849c076986b45a68dbedb290d88b2753a34bac28e6a86e9d14d4e5233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fce5279d4e22c53a01e251ad7fe838bf8030fe6b10bcc471ee936fd7be871c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea85cd5e1d6e42381426c17a11cb316e0af3f90e884e84e8c3687556d8c1e63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d1766070835a96c29e707c97ff7985a4860a5aea5463242bee4e42f9a3ffeb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8675a886cf74a176548b18ca6a0cbf5a41f34e80c2088a4db89bf06f7f6f29a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3effa16ab2128e4e494cd72c1bd18a0fb3bca5dcab8c31fcf49ce3119d0d52a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    action: builtins.str,
    description: builtins.str,
    name: builtins.str,
    precedence: jsii.Number,
    device_posture: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[builtins.str] = None,
    rule_settings: typing.Optional[typing.Union[TeamsRuleRuleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbd85acb07d8bc35ee710e905e6eb4e5535cdb3eb313c3a99615ded28b0bc14(
    *,
    add_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    biso_admin_controls: typing.Optional[typing.Union[TeamsRuleRuleSettingsBisoAdminControls, typing.Dict[builtins.str, typing.Any]]] = None,
    block_page_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    block_page_reason: typing.Optional[builtins.str] = None,
    check_session: typing.Optional[typing.Union[TeamsRuleRuleSettingsCheckSession, typing.Dict[builtins.str, typing.Any]]] = None,
    insecure_disable_dnssec_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    l4_override: typing.Optional[typing.Union[TeamsRuleRuleSettingsL4Override, typing.Dict[builtins.str, typing.Any]]] = None,
    override_host: typing.Optional[builtins.str] = None,
    override_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8b2a1cc4e29b1b8cb2edb13884ab1f20a8368313a448331b3937f5759faa3d(
    *,
    disable_copy_paste: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_keyboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_printing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_upload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c43355753706babcc2910822523a07649505aebef2bec77356a5808a9999da2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c07cded569ed72a51ded47da35c2dc1e89bd01753e1dfaf3decd3d325ccb686d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d117c06108559c432dc8d1e581cad0033553c227a4a855fe99778e0a59e6e74e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa35f16025a25779b3613f4189e1036a3316813c707eeb80976ff97972258613(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d77c7724c3eb95440a411f92d9b7d3031625f3493d812ed4ff772097f58ea40(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bea932ab3d072ffceda6ef47b07845dcaa5b6d2516951d1137de225a48b974a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1aea788e5d990f9da7eba9ea8a5cb2a922b8697739ab93f0c1f7a27bf0e22e(
    value: typing.Optional[TeamsRuleRuleSettingsBisoAdminControls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6562f9f6b37bd5dce65106a92acb7de09d28f7bc0c2d562e0aee7839ed446242(
    *,
    duration: builtins.str,
    enforce: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1238ceef1f71b79b8a34929a998cc624e06cfc9676bcd1d41293b2ab82ccb44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f982e6cba0835a289cc247a5308077895df4c5c2fc7a4b7a5cb29ccba390aba0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee19e11e0c03725f2bde7ba33bc0f418207d1b7cdf8c980d89488395a3f26a9e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b42b0db18ccb17cfd365074ced19ad968e7b4f1d679f9820ccf057ee0c2ca4(
    value: typing.Optional[TeamsRuleRuleSettingsCheckSession],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f677f3b527735bac7484a0db0b7272068363ff1030e6b1ab11edc457475c31(
    *,
    ip: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b38268da64b375013b4968be12c616b9543d82a787cfadcf50701b408dbefc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3716aa2ac1b6f966696d5812eb7f60a88b485f35398fab3af0940098f42a657(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7ce8c725d4e0831186fec3dc7fa220fdb5ed3a8dcaa22706bba8778a9d6abd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0eab80105b842a9e40858c072742abccfd1fa0fe0dd263d7fb3d0df51dc2bd0(
    value: typing.Optional[TeamsRuleRuleSettingsL4Override],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a064ccdd2cd4acbaca0d11c82e1b71f6b2481337abe56ae98e890dc18294afc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e21e76084ac4b20c1accaf0bcd912ad6d1e3576bb447eaa8d2425e2b4955441(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc0380f5525e63d13319738ebf1280805edb9dbb90e4d34c7f5d3c323f2da4b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c0150f24aef91b1a21146a2d983e28247c2cdade5a07f3fa8d7b89dd907b09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6466c2970a76a885c1e68bf22b8f3b92683c147b8c3e4dbe745c66f97d36ecfc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d30dabad90ed03fcf67b04ad9831575125ad02f850326e014337470dee49a5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02460da3696f52fd990413a1e98be6cd417e4a3c74c23eca39510c43594bd175(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d3da8d5ba679e75837415eea3fb92ddee309dd464bbec5425ec290851d7a33(
    value: typing.Optional[TeamsRuleRuleSettings],
) -> None:
    """Type checking stubs"""
    pass
