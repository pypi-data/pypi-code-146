'''
# `cloudflare_waiting_room`

Refer to the Terraform Registory for docs: [`cloudflare_waiting_room`](https://www.terraform.io/docs/providers/cloudflare/r/waiting_room).
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


class WaitingRoom(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.waitingRoom.WaitingRoom",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room cloudflare_waiting_room}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        host: builtins.str,
        name: builtins.str,
        new_users_per_minute: jsii.Number,
        total_active_users: jsii.Number,
        zone_id: builtins.str,
        custom_page_html: typing.Optional[builtins.str] = None,
        default_template_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_session_renewal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        json_response_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
        queue_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        queueing_method: typing.Optional[builtins.str] = None,
        session_duration: typing.Optional[jsii.Number] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["WaitingRoomTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room cloudflare_waiting_room} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param host: Host name for which the waiting room will be applied (no wildcards). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#host WaitingRoom#host}
        :param name: A unique name to identify the waiting room. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#name WaitingRoom#name}
        :param new_users_per_minute: The number of new users that will be let into the route every minute. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#new_users_per_minute WaitingRoom#new_users_per_minute}
        :param total_active_users: The total number of active user sessions on the route at a point in time. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#total_active_users WaitingRoom#total_active_users}
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#zone_id WaitingRoom#zone_id}
        :param custom_page_html: This is a templated html file that will be rendered at the edge. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#custom_page_html WaitingRoom#custom_page_html}
        :param default_template_language: The language to use for the default waiting room page. Available values: ``de-DE``, ``es-ES``, ``en-US``, ``fr-FR``, ``id-ID``, ``it-IT``, ``ja-JP``, ``ko-KR``, ``nl-NL``, ``pl-PL``, ``pt-BR``, ``tr-TR``, ``zh-CN``, ``zh-TW``. Defaults to ``en-US``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#default_template_language WaitingRoom#default_template_language}
        :param description: A description to add more details about the waiting room. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#description WaitingRoom#description}
        :param disable_session_renewal: Disables automatic renewal of session cookies. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#disable_session_renewal WaitingRoom#disable_session_renewal}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#id WaitingRoom#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param json_response_enabled: If true, requests to the waiting room with the header ``Accept: application/json`` will receive a JSON response object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#json_response_enabled WaitingRoom#json_response_enabled}
        :param path: The path within the host to enable the waiting room on. Defaults to ``/``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#path WaitingRoom#path}
        :param queue_all: If queue_all is true, then all traffic will be sent to the waiting room. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#queue_all WaitingRoom#queue_all}
        :param queueing_method: The queueing method used by the waiting room. Available values: ``fifo``, ``random``, ``passthrough``, ``reject``. Defaults to ``fifo``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#queueing_method WaitingRoom#queueing_method}
        :param session_duration: Lifetime of a cookie (in minutes) set by Cloudflare for users who get access to the origin. Defaults to ``5``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#session_duration WaitingRoom#session_duration}
        :param suspended: Suspends the waiting room. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#suspended WaitingRoom#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#timeouts WaitingRoom#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d737128371b91dc67e76dc498443dc339a660aa9509d247243c49a6c9f5a6d80)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WaitingRoomConfig(
            host=host,
            name=name,
            new_users_per_minute=new_users_per_minute,
            total_active_users=total_active_users,
            zone_id=zone_id,
            custom_page_html=custom_page_html,
            default_template_language=default_template_language,
            description=description,
            disable_session_renewal=disable_session_renewal,
            id=id,
            json_response_enabled=json_response_enabled,
            path=path,
            queue_all=queue_all,
            queueing_method=queueing_method,
            session_duration=session_duration,
            suspended=suspended,
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

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#create WaitingRoom#create}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#update WaitingRoom#update}.
        '''
        value = WaitingRoomTimeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomPageHtml")
    def reset_custom_page_html(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPageHtml", []))

    @jsii.member(jsii_name="resetDefaultTemplateLanguage")
    def reset_default_template_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTemplateLanguage", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisableSessionRenewal")
    def reset_disable_session_renewal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableSessionRenewal", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJsonResponseEnabled")
    def reset_json_response_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonResponseEnabled", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetQueueAll")
    def reset_queue_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueAll", []))

    @jsii.member(jsii_name="resetQueueingMethod")
    def reset_queueing_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueingMethod", []))

    @jsii.member(jsii_name="resetSessionDuration")
    def reset_session_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionDuration", []))

    @jsii.member(jsii_name="resetSuspended")
    def reset_suspended(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspended", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WaitingRoomTimeoutsOutputReference":
        return typing.cast("WaitingRoomTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="customPageHtmlInput")
    def custom_page_html_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customPageHtmlInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTemplateLanguageInput")
    def default_template_language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultTemplateLanguageInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableSessionRenewalInput")
    def disable_session_renewal_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableSessionRenewalInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonResponseEnabledInput")
    def json_response_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "jsonResponseEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="newUsersPerMinuteInput")
    def new_users_per_minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "newUsersPerMinuteInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="queueAllInput")
    def queue_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "queueAllInput"))

    @builtins.property
    @jsii.member(jsii_name="queueingMethodInput")
    def queueing_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueingMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionDurationInput")
    def session_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendedInput")
    def suspended_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suspendedInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["WaitingRoomTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["WaitingRoomTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="totalActiveUsersInput")
    def total_active_users_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "totalActiveUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customPageHtml")
    def custom_page_html(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customPageHtml"))

    @custom_page_html.setter
    def custom_page_html(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c09cb9ece44f399d78d953e46df87b8436fa04c2cc6fb0c118c0589e144379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPageHtml", value)

    @builtins.property
    @jsii.member(jsii_name="defaultTemplateLanguage")
    def default_template_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultTemplateLanguage"))

    @default_template_language.setter
    def default_template_language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__969d8244c2f72aaa4ee1c5d68a01df650631f899d5b3592e6c7ee246068a7d9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTemplateLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f30d0cb2906b147f6cf4f8372df5283d1e846cd119a8d8f23eb3a868af4060b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="disableSessionRenewal")
    def disable_session_renewal(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableSessionRenewal"))

    @disable_session_renewal.setter
    def disable_session_renewal(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ad261883326e9a9804b22864a7b94dfd7185bd735cb99ac76189594fceeb6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableSessionRenewal", value)

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0209441a13abea89a612cc455d474cffbe978ccfa3e6c7641606c3fba5d750f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b4560d1f57b6b772ed3ebc856af4c824f3ac083428211d326c1599e8adbf1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="jsonResponseEnabled")
    def json_response_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "jsonResponseEnabled"))

    @json_response_enabled.setter
    def json_response_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f88dea94bc4c673e79b7e30ffd6b4785c3765bba6d21634ec47ba87f61fbaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonResponseEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf77968b4f2854b1a4a67b3e46d1fdbbb3011fd2a8971cffb8747bdc0c164df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="newUsersPerMinute")
    def new_users_per_minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "newUsersPerMinute"))

    @new_users_per_minute.setter
    def new_users_per_minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1b91c649c55391030282e67f922293c72f360190666c593e9f9b3f762b814e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newUsersPerMinute", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__311db3e13367a00c1bb9bc9f9fbe22338d52ed8c9b53246bf0187ddfd2fdb7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="queueAll")
    def queue_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "queueAll"))

    @queue_all.setter
    def queue_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e8a601ee2eec0d8b5e3ecd699e09e9dffc8c546ae84b92f3b49e540d19df79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueAll", value)

    @builtins.property
    @jsii.member(jsii_name="queueingMethod")
    def queueing_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueingMethod"))

    @queueing_method.setter
    def queueing_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387c1b2a7e715268ed49e011f33ac68b2248b2cb9a60e2890b342126fbf89951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueingMethod", value)

    @builtins.property
    @jsii.member(jsii_name="sessionDuration")
    def session_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionDuration"))

    @session_duration.setter
    def session_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b38fc44390838c7fa98c179cc12a76e97e9c10f093104ed6754915746232677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionDuration", value)

    @builtins.property
    @jsii.member(jsii_name="suspended")
    def suspended(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suspended"))

    @suspended.setter
    def suspended(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb516a930e2ad062317a964a4c17be49c8ecc7f83a1e24818b756377ec64b1b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value)

    @builtins.property
    @jsii.member(jsii_name="totalActiveUsers")
    def total_active_users(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalActiveUsers"))

    @total_active_users.setter
    def total_active_users(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e9745f39e08ed798ec32b953cbf71156d2913ae8b2d984cab9cc9d13cfb961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalActiveUsers", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda4fb123f4ab106fe556d19e569abbfda45e0f076496ba9135d7b7fe0fd3df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.waitingRoom.WaitingRoomConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "host": "host",
        "name": "name",
        "new_users_per_minute": "newUsersPerMinute",
        "total_active_users": "totalActiveUsers",
        "zone_id": "zoneId",
        "custom_page_html": "customPageHtml",
        "default_template_language": "defaultTemplateLanguage",
        "description": "description",
        "disable_session_renewal": "disableSessionRenewal",
        "id": "id",
        "json_response_enabled": "jsonResponseEnabled",
        "path": "path",
        "queue_all": "queueAll",
        "queueing_method": "queueingMethod",
        "session_duration": "sessionDuration",
        "suspended": "suspended",
        "timeouts": "timeouts",
    },
)
class WaitingRoomConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        host: builtins.str,
        name: builtins.str,
        new_users_per_minute: jsii.Number,
        total_active_users: jsii.Number,
        zone_id: builtins.str,
        custom_page_html: typing.Optional[builtins.str] = None,
        default_template_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_session_renewal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        json_response_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
        queue_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        queueing_method: typing.Optional[builtins.str] = None,
        session_duration: typing.Optional[jsii.Number] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["WaitingRoomTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param host: Host name for which the waiting room will be applied (no wildcards). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#host WaitingRoom#host}
        :param name: A unique name to identify the waiting room. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#name WaitingRoom#name}
        :param new_users_per_minute: The number of new users that will be let into the route every minute. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#new_users_per_minute WaitingRoom#new_users_per_minute}
        :param total_active_users: The total number of active user sessions on the route at a point in time. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#total_active_users WaitingRoom#total_active_users}
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#zone_id WaitingRoom#zone_id}
        :param custom_page_html: This is a templated html file that will be rendered at the edge. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#custom_page_html WaitingRoom#custom_page_html}
        :param default_template_language: The language to use for the default waiting room page. Available values: ``de-DE``, ``es-ES``, ``en-US``, ``fr-FR``, ``id-ID``, ``it-IT``, ``ja-JP``, ``ko-KR``, ``nl-NL``, ``pl-PL``, ``pt-BR``, ``tr-TR``, ``zh-CN``, ``zh-TW``. Defaults to ``en-US``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#default_template_language WaitingRoom#default_template_language}
        :param description: A description to add more details about the waiting room. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#description WaitingRoom#description}
        :param disable_session_renewal: Disables automatic renewal of session cookies. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#disable_session_renewal WaitingRoom#disable_session_renewal}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#id WaitingRoom#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param json_response_enabled: If true, requests to the waiting room with the header ``Accept: application/json`` will receive a JSON response object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#json_response_enabled WaitingRoom#json_response_enabled}
        :param path: The path within the host to enable the waiting room on. Defaults to ``/``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#path WaitingRoom#path}
        :param queue_all: If queue_all is true, then all traffic will be sent to the waiting room. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#queue_all WaitingRoom#queue_all}
        :param queueing_method: The queueing method used by the waiting room. Available values: ``fifo``, ``random``, ``passthrough``, ``reject``. Defaults to ``fifo``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#queueing_method WaitingRoom#queueing_method}
        :param session_duration: Lifetime of a cookie (in minutes) set by Cloudflare for users who get access to the origin. Defaults to ``5``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#session_duration WaitingRoom#session_duration}
        :param suspended: Suspends the waiting room. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#suspended WaitingRoom#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#timeouts WaitingRoom#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = WaitingRoomTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71218a0efc55f5ae63de81f8f8687b06300c02b6514087e449eefe5fcf43c58c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument new_users_per_minute", value=new_users_per_minute, expected_type=type_hints["new_users_per_minute"])
            check_type(argname="argument total_active_users", value=total_active_users, expected_type=type_hints["total_active_users"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument custom_page_html", value=custom_page_html, expected_type=type_hints["custom_page_html"])
            check_type(argname="argument default_template_language", value=default_template_language, expected_type=type_hints["default_template_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_session_renewal", value=disable_session_renewal, expected_type=type_hints["disable_session_renewal"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument json_response_enabled", value=json_response_enabled, expected_type=type_hints["json_response_enabled"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument queue_all", value=queue_all, expected_type=type_hints["queue_all"])
            check_type(argname="argument queueing_method", value=queueing_method, expected_type=type_hints["queueing_method"])
            check_type(argname="argument session_duration", value=session_duration, expected_type=type_hints["session_duration"])
            check_type(argname="argument suspended", value=suspended, expected_type=type_hints["suspended"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "name": name,
            "new_users_per_minute": new_users_per_minute,
            "total_active_users": total_active_users,
            "zone_id": zone_id,
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
        if custom_page_html is not None:
            self._values["custom_page_html"] = custom_page_html
        if default_template_language is not None:
            self._values["default_template_language"] = default_template_language
        if description is not None:
            self._values["description"] = description
        if disable_session_renewal is not None:
            self._values["disable_session_renewal"] = disable_session_renewal
        if id is not None:
            self._values["id"] = id
        if json_response_enabled is not None:
            self._values["json_response_enabled"] = json_response_enabled
        if path is not None:
            self._values["path"] = path
        if queue_all is not None:
            self._values["queue_all"] = queue_all
        if queueing_method is not None:
            self._values["queueing_method"] = queueing_method
        if session_duration is not None:
            self._values["session_duration"] = session_duration
        if suspended is not None:
            self._values["suspended"] = suspended
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
    def host(self) -> builtins.str:
        '''Host name for which the waiting room will be applied (no wildcards).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#host WaitingRoom#host}
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A unique name to identify the waiting room. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#name WaitingRoom#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_users_per_minute(self) -> jsii.Number:
        '''The number of new users that will be let into the route every minute.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#new_users_per_minute WaitingRoom#new_users_per_minute}
        '''
        result = self._values.get("new_users_per_minute")
        assert result is not None, "Required property 'new_users_per_minute' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def total_active_users(self) -> jsii.Number:
        '''The total number of active user sessions on the route at a point in time.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#total_active_users WaitingRoom#total_active_users}
        '''
        result = self._values.get("total_active_users")
        assert result is not None, "Required property 'total_active_users' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def zone_id(self) -> builtins.str:
        '''The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#zone_id WaitingRoom#zone_id}
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_page_html(self) -> typing.Optional[builtins.str]:
        '''This is a templated html file that will be rendered at the edge.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#custom_page_html WaitingRoom#custom_page_html}
        '''
        result = self._values.get("custom_page_html")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_template_language(self) -> typing.Optional[builtins.str]:
        '''The language to use for the default waiting room page.

        Available values: ``de-DE``, ``es-ES``, ``en-US``, ``fr-FR``, ``id-ID``, ``it-IT``, ``ja-JP``, ``ko-KR``, ``nl-NL``, ``pl-PL``, ``pt-BR``, ``tr-TR``, ``zh-CN``, ``zh-TW``. Defaults to ``en-US``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#default_template_language WaitingRoom#default_template_language}
        '''
        result = self._values.get("default_template_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description to add more details about the waiting room.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#description WaitingRoom#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_session_renewal(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables automatic renewal of session cookies.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#disable_session_renewal WaitingRoom#disable_session_renewal}
        '''
        result = self._values.get("disable_session_renewal")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#id WaitingRoom#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def json_response_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, requests to the waiting room with the header ``Accept: application/json`` will receive a JSON response object.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#json_response_enabled WaitingRoom#json_response_enabled}
        '''
        result = self._values.get("json_response_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path within the host to enable the waiting room on. Defaults to ``/``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#path WaitingRoom#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If queue_all is true, then all traffic will be sent to the waiting room.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#queue_all WaitingRoom#queue_all}
        '''
        result = self._values.get("queue_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def queueing_method(self) -> typing.Optional[builtins.str]:
        '''The queueing method used by the waiting room. Available values: ``fifo``, ``random``, ``passthrough``, ``reject``. Defaults to ``fifo``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#queueing_method WaitingRoom#queueing_method}
        '''
        result = self._values.get("queueing_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_duration(self) -> typing.Optional[jsii.Number]:
        '''Lifetime of a cookie (in minutes) set by Cloudflare for users who get access to the origin.

        Defaults to ``5``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#session_duration WaitingRoom#session_duration}
        '''
        result = self._values.get("session_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Suspends the waiting room.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#suspended WaitingRoom#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WaitingRoomTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#timeouts WaitingRoom#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WaitingRoomTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaitingRoomConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.waitingRoom.WaitingRoomTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class WaitingRoomTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#create WaitingRoom#create}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#update WaitingRoom#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adfc39cfc62d58486be99c6cc358b9f1ec35593fd6ba8d312d4f46e0783ae898)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#create WaitingRoom#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/waiting_room#update WaitingRoom#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaitingRoomTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WaitingRoomTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.waitingRoom.WaitingRoomTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eccfee1be787ad41b1cf6b0a5a5c2d015b3cfdbaa866b5a3844527453474c0a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ceec3962be8f689311df47184c96f6b7e57fe2514a70bdae61754982ccd2ca45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e035d40382f0e4d03d804c9524cebb9686b12627f69a17359589b4001f850b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WaitingRoomTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WaitingRoomTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WaitingRoomTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdab482da22b5d1353d9de02cfc88f5cfe86ac1e214d71116ac2e24be92fcf72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "WaitingRoom",
    "WaitingRoomConfig",
    "WaitingRoomTimeouts",
    "WaitingRoomTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d737128371b91dc67e76dc498443dc339a660aa9509d247243c49a6c9f5a6d80(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    host: builtins.str,
    name: builtins.str,
    new_users_per_minute: jsii.Number,
    total_active_users: jsii.Number,
    zone_id: builtins.str,
    custom_page_html: typing.Optional[builtins.str] = None,
    default_template_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disable_session_renewal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    json_response_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
    queue_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    queueing_method: typing.Optional[builtins.str] = None,
    session_duration: typing.Optional[jsii.Number] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[WaitingRoomTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__00c09cb9ece44f399d78d953e46df87b8436fa04c2cc6fb0c118c0589e144379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969d8244c2f72aaa4ee1c5d68a01df650631f899d5b3592e6c7ee246068a7d9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f30d0cb2906b147f6cf4f8372df5283d1e846cd119a8d8f23eb3a868af4060b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ad261883326e9a9804b22864a7b94dfd7185bd735cb99ac76189594fceeb6f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0209441a13abea89a612cc455d474cffbe978ccfa3e6c7641606c3fba5d750f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b4560d1f57b6b772ed3ebc856af4c824f3ac083428211d326c1599e8adbf1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f88dea94bc4c673e79b7e30ffd6b4785c3765bba6d21634ec47ba87f61fbaa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf77968b4f2854b1a4a67b3e46d1fdbbb3011fd2a8971cffb8747bdc0c164df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1b91c649c55391030282e67f922293c72f360190666c593e9f9b3f762b814e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311db3e13367a00c1bb9bc9f9fbe22338d52ed8c9b53246bf0187ddfd2fdb7eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e8a601ee2eec0d8b5e3ecd699e09e9dffc8c546ae84b92f3b49e540d19df79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387c1b2a7e715268ed49e011f33ac68b2248b2cb9a60e2890b342126fbf89951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b38fc44390838c7fa98c179cc12a76e97e9c10f093104ed6754915746232677(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb516a930e2ad062317a964a4c17be49c8ecc7f83a1e24818b756377ec64b1b9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e9745f39e08ed798ec32b953cbf71156d2913ae8b2d984cab9cc9d13cfb961(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda4fb123f4ab106fe556d19e569abbfda45e0f076496ba9135d7b7fe0fd3df1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71218a0efc55f5ae63de81f8f8687b06300c02b6514087e449eefe5fcf43c58c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host: builtins.str,
    name: builtins.str,
    new_users_per_minute: jsii.Number,
    total_active_users: jsii.Number,
    zone_id: builtins.str,
    custom_page_html: typing.Optional[builtins.str] = None,
    default_template_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disable_session_renewal: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    json_response_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
    queue_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    queueing_method: typing.Optional[builtins.str] = None,
    session_duration: typing.Optional[jsii.Number] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[WaitingRoomTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adfc39cfc62d58486be99c6cc358b9f1ec35593fd6ba8d312d4f46e0783ae898(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccfee1be787ad41b1cf6b0a5a5c2d015b3cfdbaa866b5a3844527453474c0a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceec3962be8f689311df47184c96f6b7e57fe2514a70bdae61754982ccd2ca45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e035d40382f0e4d03d804c9524cebb9686b12627f69a17359589b4001f850b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdab482da22b5d1353d9de02cfc88f5cfe86ac1e214d71116ac2e24be92fcf72(
    value: typing.Optional[typing.Union[WaitingRoomTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
