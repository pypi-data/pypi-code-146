'''
# `cloudflare_device_settings_policy`

Refer to the Terraform Registory for docs: [`cloudflare_device_settings_policy`](https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy).
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


class DeviceSettingsPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.deviceSettingsPolicy.DeviceSettingsPolicy",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy cloudflare_device_settings_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        name: builtins.str,
        allowed_to_leave: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_mode_switch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_connect: typing.Optional[jsii.Number] = None,
        captive_portal: typing.Optional[jsii.Number] = None,
        default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_auto_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        match: typing.Optional[builtins.str] = None,
        precedence: typing.Optional[jsii.Number] = None,
        service_mode_v2_mode: typing.Optional[builtins.str] = None,
        service_mode_v2_port: typing.Optional[jsii.Number] = None,
        support_url: typing.Optional[builtins.str] = None,
        switch_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy cloudflare_device_settings_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#account_id DeviceSettingsPolicy#account_id}
        :param name: Name of the policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#name DeviceSettingsPolicy#name}
        :param allowed_to_leave: Whether to allow devices to leave the organization. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#allowed_to_leave DeviceSettingsPolicy#allowed_to_leave}
        :param allow_mode_switch: Whether to allow mode switch for this policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#allow_mode_switch DeviceSettingsPolicy#allow_mode_switch}
        :param allow_updates: Whether to allow updates under this policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#allow_updates DeviceSettingsPolicy#allow_updates}
        :param auto_connect: The amount of time in minutes to reconnect after having been disabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#auto_connect DeviceSettingsPolicy#auto_connect}
        :param captive_portal: The captive portal value for this policy. Defaults to ``180``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#captive_portal DeviceSettingsPolicy#captive_portal}
        :param default: Whether the policy refers to the default account policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#default DeviceSettingsPolicy#default}
        :param disable_auto_fallback: Whether to disable auto fallback for this policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#disable_auto_fallback DeviceSettingsPolicy#disable_auto_fallback}
        :param enabled: Whether the policy is enabled (cannot be set for default policies). Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#enabled DeviceSettingsPolicy#enabled}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#id DeviceSettingsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match: Wirefilter expression to match a device against when evaluating whether this policy should take effect for that device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#match DeviceSettingsPolicy#match}
        :param precedence: The precedence of the policy. Lower values indicate higher precedence. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#precedence DeviceSettingsPolicy#precedence}
        :param service_mode_v2_mode: The service mode. Defaults to ``warp``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#service_mode_v2_mode DeviceSettingsPolicy#service_mode_v2_mode}
        :param service_mode_v2_port: The port to use for the proxy service mode. Required when using ``service_mode_v2_mode``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#service_mode_v2_port DeviceSettingsPolicy#service_mode_v2_port}
        :param support_url: The support URL that will be opened when sending feedback. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#support_url DeviceSettingsPolicy#support_url}
        :param switch_locked: Enablement of the ZT client switch lock. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#switch_locked DeviceSettingsPolicy#switch_locked}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e17fef340d2d466fa88b4bc1c9452eeafae6abffa5bd3bec88d4fb9991b626e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DeviceSettingsPolicyConfig(
            account_id=account_id,
            name=name,
            allowed_to_leave=allowed_to_leave,
            allow_mode_switch=allow_mode_switch,
            allow_updates=allow_updates,
            auto_connect=auto_connect,
            captive_portal=captive_portal,
            default=default,
            disable_auto_fallback=disable_auto_fallback,
            enabled=enabled,
            id=id,
            match=match,
            precedence=precedence,
            service_mode_v2_mode=service_mode_v2_mode,
            service_mode_v2_port=service_mode_v2_port,
            support_url=support_url,
            switch_locked=switch_locked,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAllowedToLeave")
    def reset_allowed_to_leave(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedToLeave", []))

    @jsii.member(jsii_name="resetAllowModeSwitch")
    def reset_allow_mode_switch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowModeSwitch", []))

    @jsii.member(jsii_name="resetAllowUpdates")
    def reset_allow_updates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowUpdates", []))

    @jsii.member(jsii_name="resetAutoConnect")
    def reset_auto_connect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoConnect", []))

    @jsii.member(jsii_name="resetCaptivePortal")
    def reset_captive_portal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaptivePortal", []))

    @jsii.member(jsii_name="resetDefault")
    def reset_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefault", []))

    @jsii.member(jsii_name="resetDisableAutoFallback")
    def reset_disable_auto_fallback(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableAutoFallback", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @jsii.member(jsii_name="resetPrecedence")
    def reset_precedence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrecedence", []))

    @jsii.member(jsii_name="resetServiceModeV2Mode")
    def reset_service_mode_v2_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceModeV2Mode", []))

    @jsii.member(jsii_name="resetServiceModeV2Port")
    def reset_service_mode_v2_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceModeV2Port", []))

    @jsii.member(jsii_name="resetSupportUrl")
    def reset_support_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportUrl", []))

    @jsii.member(jsii_name="resetSwitchLocked")
    def reset_switch_locked(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwitchLocked", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedToLeaveInput")
    def allowed_to_leave_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowedToLeaveInput"))

    @builtins.property
    @jsii.member(jsii_name="allowModeSwitchInput")
    def allow_mode_switch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowModeSwitchInput"))

    @builtins.property
    @jsii.member(jsii_name="allowUpdatesInput")
    def allow_updates_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowUpdatesInput"))

    @builtins.property
    @jsii.member(jsii_name="autoConnectInput")
    def auto_connect_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="captivePortalInput")
    def captive_portal_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "captivePortalInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="disableAutoFallbackInput")
    def disable_auto_fallback_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableAutoFallbackInput"))

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
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="precedenceInput")
    def precedence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "precedenceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceModeV2ModeInput")
    def service_mode_v2_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceModeV2ModeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceModeV2PortInput")
    def service_mode_v2_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serviceModeV2PortInput"))

    @builtins.property
    @jsii.member(jsii_name="supportUrlInput")
    def support_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="switchLockedInput")
    def switch_locked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "switchLockedInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2daf9c6c62add300cda39e1523825eab6e7316ef0d140d805597a8728e7d126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="allowedToLeave")
    def allowed_to_leave(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowedToLeave"))

    @allowed_to_leave.setter
    def allowed_to_leave(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5bf8148eea64d9b8cb5d806e9f5bd5b8227fefedb4db562280f4e239a6a0902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedToLeave", value)

    @builtins.property
    @jsii.member(jsii_name="allowModeSwitch")
    def allow_mode_switch(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowModeSwitch"))

    @allow_mode_switch.setter
    def allow_mode_switch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e20ff6fb866dc034c16ead2a97a09acffc5b1a9c6838da47177d11cfff0a162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowModeSwitch", value)

    @builtins.property
    @jsii.member(jsii_name="allowUpdates")
    def allow_updates(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowUpdates"))

    @allow_updates.setter
    def allow_updates(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af03d222c999e09d6b40f76d9367ef7a5257882af508c45ccc2587af1077a104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowUpdates", value)

    @builtins.property
    @jsii.member(jsii_name="autoConnect")
    def auto_connect(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoConnect"))

    @auto_connect.setter
    def auto_connect(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46fb2084d9f7f04640678432d2817973a22ada5352dafbfc6291e67a72f06b28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoConnect", value)

    @builtins.property
    @jsii.member(jsii_name="captivePortal")
    def captive_portal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "captivePortal"))

    @captive_portal.setter
    def captive_portal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ac07224d9a0e4abfd954c2f5a9918a58d570ee03d024582870f36350b5fb4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "captivePortal", value)

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "default"))

    @default.setter
    def default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8110d951dc51129188809e786631ba5770475dcf6b341f437928e5cd4c9daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value)

    @builtins.property
    @jsii.member(jsii_name="disableAutoFallback")
    def disable_auto_fallback(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableAutoFallback"))

    @disable_auto_fallback.setter
    def disable_auto_fallback(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d48bee59394d0b3d2242dda95d840ec56fd0948b606501aebe9a12d707ef618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableAutoFallback", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__d0d7aae6d4aa51c41aa2a0cc7b3ea2965e1885e040d7b5e83e2c51d4b05546ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6e03c9ca69a24453236e7cc2163f0c5e5a62407f8a81c70255b40a6767c62f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "match"))

    @match.setter
    def match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a918f4b729b469827575daea2082cb11c9d2eabd12fd44897b8baf4cbe9531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "match", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b1c299af1e10646aa0c6ade2091c2987221ee49b8ad8a39766d6f234d54a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="precedence")
    def precedence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precedence"))

    @precedence.setter
    def precedence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140143f3bac2610550db9243af3e2ee44537f310332b8eba85979ab02c3a3191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "precedence", value)

    @builtins.property
    @jsii.member(jsii_name="serviceModeV2Mode")
    def service_mode_v2_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceModeV2Mode"))

    @service_mode_v2_mode.setter
    def service_mode_v2_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11bd5e82b484638a86055a0b92aa56c43ea33b2fc93d29669cfe25bec1258aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceModeV2Mode", value)

    @builtins.property
    @jsii.member(jsii_name="serviceModeV2Port")
    def service_mode_v2_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serviceModeV2Port"))

    @service_mode_v2_port.setter
    def service_mode_v2_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e5c676c0910e1fdd3b67d461282fcb1bc1325176c1cf1fb3a52edb4f3d02d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceModeV2Port", value)

    @builtins.property
    @jsii.member(jsii_name="supportUrl")
    def support_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportUrl"))

    @support_url.setter
    def support_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c9e8b4196e50846304eda8105b7e77ad57f185132571cf8d6871979c65db00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportUrl", value)

    @builtins.property
    @jsii.member(jsii_name="switchLocked")
    def switch_locked(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "switchLocked"))

    @switch_locked.setter
    def switch_locked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a6da89e5afdfe832b8504c7670bc16900e304c058a422e5c55655dae6746eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "switchLocked", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.deviceSettingsPolicy.DeviceSettingsPolicyConfig",
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
        "allowed_to_leave": "allowedToLeave",
        "allow_mode_switch": "allowModeSwitch",
        "allow_updates": "allowUpdates",
        "auto_connect": "autoConnect",
        "captive_portal": "captivePortal",
        "default": "default",
        "disable_auto_fallback": "disableAutoFallback",
        "enabled": "enabled",
        "id": "id",
        "match": "match",
        "precedence": "precedence",
        "service_mode_v2_mode": "serviceModeV2Mode",
        "service_mode_v2_port": "serviceModeV2Port",
        "support_url": "supportUrl",
        "switch_locked": "switchLocked",
    },
)
class DeviceSettingsPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allowed_to_leave: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_mode_switch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_connect: typing.Optional[jsii.Number] = None,
        captive_portal: typing.Optional[jsii.Number] = None,
        default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_auto_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        match: typing.Optional[builtins.str] = None,
        precedence: typing.Optional[jsii.Number] = None,
        service_mode_v2_mode: typing.Optional[builtins.str] = None,
        service_mode_v2_port: typing.Optional[jsii.Number] = None,
        support_url: typing.Optional[builtins.str] = None,
        switch_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#account_id DeviceSettingsPolicy#account_id}
        :param name: Name of the policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#name DeviceSettingsPolicy#name}
        :param allowed_to_leave: Whether to allow devices to leave the organization. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#allowed_to_leave DeviceSettingsPolicy#allowed_to_leave}
        :param allow_mode_switch: Whether to allow mode switch for this policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#allow_mode_switch DeviceSettingsPolicy#allow_mode_switch}
        :param allow_updates: Whether to allow updates under this policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#allow_updates DeviceSettingsPolicy#allow_updates}
        :param auto_connect: The amount of time in minutes to reconnect after having been disabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#auto_connect DeviceSettingsPolicy#auto_connect}
        :param captive_portal: The captive portal value for this policy. Defaults to ``180``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#captive_portal DeviceSettingsPolicy#captive_portal}
        :param default: Whether the policy refers to the default account policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#default DeviceSettingsPolicy#default}
        :param disable_auto_fallback: Whether to disable auto fallback for this policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#disable_auto_fallback DeviceSettingsPolicy#disable_auto_fallback}
        :param enabled: Whether the policy is enabled (cannot be set for default policies). Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#enabled DeviceSettingsPolicy#enabled}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#id DeviceSettingsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match: Wirefilter expression to match a device against when evaluating whether this policy should take effect for that device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#match DeviceSettingsPolicy#match}
        :param precedence: The precedence of the policy. Lower values indicate higher precedence. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#precedence DeviceSettingsPolicy#precedence}
        :param service_mode_v2_mode: The service mode. Defaults to ``warp``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#service_mode_v2_mode DeviceSettingsPolicy#service_mode_v2_mode}
        :param service_mode_v2_port: The port to use for the proxy service mode. Required when using ``service_mode_v2_mode``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#service_mode_v2_port DeviceSettingsPolicy#service_mode_v2_port}
        :param support_url: The support URL that will be opened when sending feedback. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#support_url DeviceSettingsPolicy#support_url}
        :param switch_locked: Enablement of the ZT client switch lock. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#switch_locked DeviceSettingsPolicy#switch_locked}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9eb63acb8587c4172d3ff5584694e2b8adf7111877ede3b4d06f5870ee0bc7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_to_leave", value=allowed_to_leave, expected_type=type_hints["allowed_to_leave"])
            check_type(argname="argument allow_mode_switch", value=allow_mode_switch, expected_type=type_hints["allow_mode_switch"])
            check_type(argname="argument allow_updates", value=allow_updates, expected_type=type_hints["allow_updates"])
            check_type(argname="argument auto_connect", value=auto_connect, expected_type=type_hints["auto_connect"])
            check_type(argname="argument captive_portal", value=captive_portal, expected_type=type_hints["captive_portal"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument disable_auto_fallback", value=disable_auto_fallback, expected_type=type_hints["disable_auto_fallback"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument precedence", value=precedence, expected_type=type_hints["precedence"])
            check_type(argname="argument service_mode_v2_mode", value=service_mode_v2_mode, expected_type=type_hints["service_mode_v2_mode"])
            check_type(argname="argument service_mode_v2_port", value=service_mode_v2_port, expected_type=type_hints["service_mode_v2_port"])
            check_type(argname="argument support_url", value=support_url, expected_type=type_hints["support_url"])
            check_type(argname="argument switch_locked", value=switch_locked, expected_type=type_hints["switch_locked"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
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
        if allowed_to_leave is not None:
            self._values["allowed_to_leave"] = allowed_to_leave
        if allow_mode_switch is not None:
            self._values["allow_mode_switch"] = allow_mode_switch
        if allow_updates is not None:
            self._values["allow_updates"] = allow_updates
        if auto_connect is not None:
            self._values["auto_connect"] = auto_connect
        if captive_portal is not None:
            self._values["captive_portal"] = captive_portal
        if default is not None:
            self._values["default"] = default
        if disable_auto_fallback is not None:
            self._values["disable_auto_fallback"] = disable_auto_fallback
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if match is not None:
            self._values["match"] = match
        if precedence is not None:
            self._values["precedence"] = precedence
        if service_mode_v2_mode is not None:
            self._values["service_mode_v2_mode"] = service_mode_v2_mode
        if service_mode_v2_port is not None:
            self._values["service_mode_v2_port"] = service_mode_v2_port
        if support_url is not None:
            self._values["support_url"] = support_url
        if switch_locked is not None:
            self._values["switch_locked"] = switch_locked

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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#account_id DeviceSettingsPolicy#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#name DeviceSettingsPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_to_leave(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow devices to leave the organization. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#allowed_to_leave DeviceSettingsPolicy#allowed_to_leave}
        '''
        result = self._values.get("allowed_to_leave")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_mode_switch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow mode switch for this policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#allow_mode_switch DeviceSettingsPolicy#allow_mode_switch}
        '''
        result = self._values.get("allow_mode_switch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_updates(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow updates under this policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#allow_updates DeviceSettingsPolicy#allow_updates}
        '''
        result = self._values.get("allow_updates")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_connect(self) -> typing.Optional[jsii.Number]:
        '''The amount of time in minutes to reconnect after having been disabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#auto_connect DeviceSettingsPolicy#auto_connect}
        '''
        result = self._values.get("auto_connect")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def captive_portal(self) -> typing.Optional[jsii.Number]:
        '''The captive portal value for this policy. Defaults to ``180``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#captive_portal DeviceSettingsPolicy#captive_portal}
        '''
        result = self._values.get("captive_portal")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the policy refers to the default account policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#default DeviceSettingsPolicy#default}
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_auto_fallback(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to disable auto fallback for this policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#disable_auto_fallback DeviceSettingsPolicy#disable_auto_fallback}
        '''
        result = self._values.get("disable_auto_fallback")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the policy is enabled (cannot be set for default policies). Defaults to ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#enabled DeviceSettingsPolicy#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#id DeviceSettingsPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match(self) -> typing.Optional[builtins.str]:
        '''Wirefilter expression to match a device against when evaluating whether this policy should take effect for that device.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#match DeviceSettingsPolicy#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def precedence(self) -> typing.Optional[jsii.Number]:
        '''The precedence of the policy. Lower values indicate higher precedence.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#precedence DeviceSettingsPolicy#precedence}
        '''
        result = self._values.get("precedence")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_mode_v2_mode(self) -> typing.Optional[builtins.str]:
        '''The service mode. Defaults to ``warp``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#service_mode_v2_mode DeviceSettingsPolicy#service_mode_v2_mode}
        '''
        result = self._values.get("service_mode_v2_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_mode_v2_port(self) -> typing.Optional[jsii.Number]:
        '''The port to use for the proxy service mode. Required when using ``service_mode_v2_mode``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#service_mode_v2_port DeviceSettingsPolicy#service_mode_v2_port}
        '''
        result = self._values.get("service_mode_v2_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def support_url(self) -> typing.Optional[builtins.str]:
        '''The support URL that will be opened when sending feedback.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#support_url DeviceSettingsPolicy#support_url}
        '''
        result = self._values.get("support_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def switch_locked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enablement of the ZT client switch lock.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_settings_policy#switch_locked DeviceSettingsPolicy#switch_locked}
        '''
        result = self._values.get("switch_locked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeviceSettingsPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DeviceSettingsPolicy",
    "DeviceSettingsPolicyConfig",
]

publication.publish()

def _typecheckingstub__4e17fef340d2d466fa88b4bc1c9452eeafae6abffa5bd3bec88d4fb9991b626e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    name: builtins.str,
    allowed_to_leave: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_mode_switch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_connect: typing.Optional[jsii.Number] = None,
    captive_portal: typing.Optional[jsii.Number] = None,
    default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_auto_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    match: typing.Optional[builtins.str] = None,
    precedence: typing.Optional[jsii.Number] = None,
    service_mode_v2_mode: typing.Optional[builtins.str] = None,
    service_mode_v2_port: typing.Optional[jsii.Number] = None,
    support_url: typing.Optional[builtins.str] = None,
    switch_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__e2daf9c6c62add300cda39e1523825eab6e7316ef0d140d805597a8728e7d126(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bf8148eea64d9b8cb5d806e9f5bd5b8227fefedb4db562280f4e239a6a0902(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e20ff6fb866dc034c16ead2a97a09acffc5b1a9c6838da47177d11cfff0a162(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af03d222c999e09d6b40f76d9367ef7a5257882af508c45ccc2587af1077a104(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46fb2084d9f7f04640678432d2817973a22ada5352dafbfc6291e67a72f06b28(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ac07224d9a0e4abfd954c2f5a9918a58d570ee03d024582870f36350b5fb4a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8110d951dc51129188809e786631ba5770475dcf6b341f437928e5cd4c9daa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d48bee59394d0b3d2242dda95d840ec56fd0948b606501aebe9a12d707ef618(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d7aae6d4aa51c41aa2a0cc7b3ea2965e1885e040d7b5e83e2c51d4b05546ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6e03c9ca69a24453236e7cc2163f0c5e5a62407f8a81c70255b40a6767c62f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a918f4b729b469827575daea2082cb11c9d2eabd12fd44897b8baf4cbe9531(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b1c299af1e10646aa0c6ade2091c2987221ee49b8ad8a39766d6f234d54a6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140143f3bac2610550db9243af3e2ee44537f310332b8eba85979ab02c3a3191(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11bd5e82b484638a86055a0b92aa56c43ea33b2fc93d29669cfe25bec1258aa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e5c676c0910e1fdd3b67d461282fcb1bc1325176c1cf1fb3a52edb4f3d02d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c9e8b4196e50846304eda8105b7e77ad57f185132571cf8d6871979c65db00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a6da89e5afdfe832b8504c7670bc16900e304c058a422e5c55655dae6746eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9eb63acb8587c4172d3ff5584694e2b8adf7111877ede3b4d06f5870ee0bc7(
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
    allowed_to_leave: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_mode_switch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_connect: typing.Optional[jsii.Number] = None,
    captive_portal: typing.Optional[jsii.Number] = None,
    default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_auto_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    match: typing.Optional[builtins.str] = None,
    precedence: typing.Optional[jsii.Number] = None,
    service_mode_v2_mode: typing.Optional[builtins.str] = None,
    service_mode_v2_port: typing.Optional[jsii.Number] = None,
    support_url: typing.Optional[builtins.str] = None,
    switch_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
