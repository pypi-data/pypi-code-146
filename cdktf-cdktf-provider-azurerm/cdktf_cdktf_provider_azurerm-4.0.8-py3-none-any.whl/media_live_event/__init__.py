'''
# `azurerm_media_live_event`

Refer to the Terraform Registory for docs: [`azurerm_media_live_event`](https://www.terraform.io/docs/providers/azurerm/r/media_live_event).
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


class MediaLiveEvent(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEvent",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event azurerm_media_live_event}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        input: typing.Union["MediaLiveEventInput", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        media_services_account_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        auto_start_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cross_site_access_policy: typing.Optional[typing.Union["MediaLiveEventCrossSiteAccessPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        encoding: typing.Optional[typing.Union["MediaLiveEventEncoding", typing.Dict[builtins.str, typing.Any]]] = None,
        hostname_prefix: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        preview: typing.Optional[typing.Union["MediaLiveEventPreview", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MediaLiveEventTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transcription_languages: typing.Optional[typing.Sequence[builtins.str]] = None,
        use_static_hostname: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event azurerm_media_live_event} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param input: input block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#input MediaLiveEvent#input}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#location MediaLiveEvent#location}.
        :param media_services_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#media_services_account_name MediaLiveEvent#media_services_account_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#name MediaLiveEvent#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#resource_group_name MediaLiveEvent#resource_group_name}.
        :param auto_start_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#auto_start_enabled MediaLiveEvent#auto_start_enabled}.
        :param cross_site_access_policy: cross_site_access_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#cross_site_access_policy MediaLiveEvent#cross_site_access_policy}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#description MediaLiveEvent#description}.
        :param encoding: encoding block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#encoding MediaLiveEvent#encoding}
        :param hostname_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#hostname_prefix MediaLiveEvent#hostname_prefix}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#id MediaLiveEvent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param preview: preview block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#preview MediaLiveEvent#preview}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#tags MediaLiveEvent#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#timeouts MediaLiveEvent#timeouts}
        :param transcription_languages: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#transcription_languages MediaLiveEvent#transcription_languages}.
        :param use_static_hostname: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#use_static_hostname MediaLiveEvent#use_static_hostname}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ba1361290340f82443589c170eb8d6f24804dc0d4c781851725bb05cc64651)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MediaLiveEventConfig(
            input=input,
            location=location,
            media_services_account_name=media_services_account_name,
            name=name,
            resource_group_name=resource_group_name,
            auto_start_enabled=auto_start_enabled,
            cross_site_access_policy=cross_site_access_policy,
            description=description,
            encoding=encoding,
            hostname_prefix=hostname_prefix,
            id=id,
            preview=preview,
            tags=tags,
            timeouts=timeouts,
            transcription_languages=transcription_languages,
            use_static_hostname=use_static_hostname,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putCrossSiteAccessPolicy")
    def put_cross_site_access_policy(
        self,
        *,
        client_access_policy: typing.Optional[builtins.str] = None,
        cross_domain_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_access_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#client_access_policy MediaLiveEvent#client_access_policy}.
        :param cross_domain_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#cross_domain_policy MediaLiveEvent#cross_domain_policy}.
        '''
        value = MediaLiveEventCrossSiteAccessPolicy(
            client_access_policy=client_access_policy,
            cross_domain_policy=cross_domain_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putCrossSiteAccessPolicy", [value]))

    @jsii.member(jsii_name="putEncoding")
    def put_encoding(
        self,
        *,
        key_frame_interval: typing.Optional[builtins.str] = None,
        preset_name: typing.Optional[builtins.str] = None,
        stretch_mode: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_frame_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#key_frame_interval MediaLiveEvent#key_frame_interval}.
        :param preset_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#preset_name MediaLiveEvent#preset_name}.
        :param stretch_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#stretch_mode MediaLiveEvent#stretch_mode}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#type MediaLiveEvent#type}.
        '''
        value = MediaLiveEventEncoding(
            key_frame_interval=key_frame_interval,
            preset_name=preset_name,
            stretch_mode=stretch_mode,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putEncoding", [value]))

    @jsii.member(jsii_name="putInput")
    def put_input(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        ip_access_control_allow: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaLiveEventInputIpAccessControlAllow", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key_frame_interval_duration: typing.Optional[builtins.str] = None,
        streaming_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#access_token MediaLiveEvent#access_token}.
        :param ip_access_control_allow: ip_access_control_allow block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#ip_access_control_allow MediaLiveEvent#ip_access_control_allow}
        :param key_frame_interval_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#key_frame_interval_duration MediaLiveEvent#key_frame_interval_duration}.
        :param streaming_protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#streaming_protocol MediaLiveEvent#streaming_protocol}.
        '''
        value = MediaLiveEventInput(
            access_token=access_token,
            ip_access_control_allow=ip_access_control_allow,
            key_frame_interval_duration=key_frame_interval_duration,
            streaming_protocol=streaming_protocol,
        )

        return typing.cast(None, jsii.invoke(self, "putInput", [value]))

    @jsii.member(jsii_name="putPreview")
    def put_preview(
        self,
        *,
        alternative_media_id: typing.Optional[builtins.str] = None,
        ip_access_control_allow: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaLiveEventPreviewIpAccessControlAllow", typing.Dict[builtins.str, typing.Any]]]]] = None,
        preview_locator: typing.Optional[builtins.str] = None,
        streaming_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alternative_media_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#alternative_media_id MediaLiveEvent#alternative_media_id}.
        :param ip_access_control_allow: ip_access_control_allow block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#ip_access_control_allow MediaLiveEvent#ip_access_control_allow}
        :param preview_locator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#preview_locator MediaLiveEvent#preview_locator}.
        :param streaming_policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#streaming_policy_name MediaLiveEvent#streaming_policy_name}.
        '''
        value = MediaLiveEventPreview(
            alternative_media_id=alternative_media_id,
            ip_access_control_allow=ip_access_control_allow,
            preview_locator=preview_locator,
            streaming_policy_name=streaming_policy_name,
        )

        return typing.cast(None, jsii.invoke(self, "putPreview", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#create MediaLiveEvent#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#delete MediaLiveEvent#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#read MediaLiveEvent#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#update MediaLiveEvent#update}.
        '''
        value = MediaLiveEventTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoStartEnabled")
    def reset_auto_start_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoStartEnabled", []))

    @jsii.member(jsii_name="resetCrossSiteAccessPolicy")
    def reset_cross_site_access_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossSiteAccessPolicy", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetHostnamePrefix")
    def reset_hostname_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostnamePrefix", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPreview")
    def reset_preview(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreview", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTranscriptionLanguages")
    def reset_transcription_languages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTranscriptionLanguages", []))

    @jsii.member(jsii_name="resetUseStaticHostname")
    def reset_use_static_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseStaticHostname", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="crossSiteAccessPolicy")
    def cross_site_access_policy(
        self,
    ) -> "MediaLiveEventCrossSiteAccessPolicyOutputReference":
        return typing.cast("MediaLiveEventCrossSiteAccessPolicyOutputReference", jsii.get(self, "crossSiteAccessPolicy"))

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> "MediaLiveEventEncodingOutputReference":
        return typing.cast("MediaLiveEventEncodingOutputReference", jsii.get(self, "encoding"))

    @builtins.property
    @jsii.member(jsii_name="input")
    def input(self) -> "MediaLiveEventInputOutputReference":
        return typing.cast("MediaLiveEventInputOutputReference", jsii.get(self, "input"))

    @builtins.property
    @jsii.member(jsii_name="preview")
    def preview(self) -> "MediaLiveEventPreviewOutputReference":
        return typing.cast("MediaLiveEventPreviewOutputReference", jsii.get(self, "preview"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MediaLiveEventTimeoutsOutputReference":
        return typing.cast("MediaLiveEventTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoStartEnabledInput")
    def auto_start_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoStartEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="crossSiteAccessPolicyInput")
    def cross_site_access_policy_input(
        self,
    ) -> typing.Optional["MediaLiveEventCrossSiteAccessPolicy"]:
        return typing.cast(typing.Optional["MediaLiveEventCrossSiteAccessPolicy"], jsii.get(self, "crossSiteAccessPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional["MediaLiveEventEncoding"]:
        return typing.cast(typing.Optional["MediaLiveEventEncoding"], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnamePrefixInput")
    def hostname_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inputInput")
    def input_input(self) -> typing.Optional["MediaLiveEventInput"]:
        return typing.cast(typing.Optional["MediaLiveEventInput"], jsii.get(self, "inputInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="mediaServicesAccountNameInput")
    def media_services_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mediaServicesAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="previewInput")
    def preview_input(self) -> typing.Optional["MediaLiveEventPreview"]:
        return typing.cast(typing.Optional["MediaLiveEventPreview"], jsii.get(self, "previewInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MediaLiveEventTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MediaLiveEventTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transcriptionLanguagesInput")
    def transcription_languages_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transcriptionLanguagesInput"))

    @builtins.property
    @jsii.member(jsii_name="useStaticHostnameInput")
    def use_static_hostname_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useStaticHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="autoStartEnabled")
    def auto_start_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoStartEnabled"))

    @auto_start_enabled.setter
    def auto_start_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29557b8c4f62ceff4249272133c9a6211fa4b2081d78f80d9deeff3b947d3a27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoStartEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3b28a309af7f223f72e22062914c1312a1898ea35292cce8d2c5ec9361fc22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="hostnamePrefix")
    def hostname_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostnamePrefix"))

    @hostname_prefix.setter
    def hostname_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcef4243f9f012f489591b986fffea664efac673c6bc3d3a51a47feb93a78bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostnamePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1eb7750039e59cd4e7f74f55c82be7626cdbf7f9dabb1f770b612bbe25e12d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4cfa507ca6b417d11e416f893a1237f335f2971679e9a1c6ec2de8560a8669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="mediaServicesAccountName")
    def media_services_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mediaServicesAccountName"))

    @media_services_account_name.setter
    def media_services_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11484efd66159574278ceb191fe60211db033cf863ac099e08fb24d107fdd8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mediaServicesAccountName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26088f619cb5dbc639ebee596bcafd4dce03f9cc38b83fff09e86c7bfb9179a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc98475c8d83d87b2add942b19cbd48a47686ee5cfda2bb409f6b2a141838e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c324a8776a9f7a446d9acde5c67e6896f05e76c748501a4b40fbe8849847ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="transcriptionLanguages")
    def transcription_languages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transcriptionLanguages"))

    @transcription_languages.setter
    def transcription_languages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3525ccd52b80acf02a86ba215991f3132045692d59e8bb825f54fb3082cc35d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transcriptionLanguages", value)

    @builtins.property
    @jsii.member(jsii_name="useStaticHostname")
    def use_static_hostname(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useStaticHostname"))

    @use_static_hostname.setter
    def use_static_hostname(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae74e9fb0ad5323e6946ece09a24e19792195feeef2652a5014af6b9ec16017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useStaticHostname", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "input": "input",
        "location": "location",
        "media_services_account_name": "mediaServicesAccountName",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "auto_start_enabled": "autoStartEnabled",
        "cross_site_access_policy": "crossSiteAccessPolicy",
        "description": "description",
        "encoding": "encoding",
        "hostname_prefix": "hostnamePrefix",
        "id": "id",
        "preview": "preview",
        "tags": "tags",
        "timeouts": "timeouts",
        "transcription_languages": "transcriptionLanguages",
        "use_static_hostname": "useStaticHostname",
    },
)
class MediaLiveEventConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        input: typing.Union["MediaLiveEventInput", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        media_services_account_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        auto_start_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cross_site_access_policy: typing.Optional[typing.Union["MediaLiveEventCrossSiteAccessPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        encoding: typing.Optional[typing.Union["MediaLiveEventEncoding", typing.Dict[builtins.str, typing.Any]]] = None,
        hostname_prefix: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        preview: typing.Optional[typing.Union["MediaLiveEventPreview", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MediaLiveEventTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transcription_languages: typing.Optional[typing.Sequence[builtins.str]] = None,
        use_static_hostname: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param input: input block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#input MediaLiveEvent#input}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#location MediaLiveEvent#location}.
        :param media_services_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#media_services_account_name MediaLiveEvent#media_services_account_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#name MediaLiveEvent#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#resource_group_name MediaLiveEvent#resource_group_name}.
        :param auto_start_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#auto_start_enabled MediaLiveEvent#auto_start_enabled}.
        :param cross_site_access_policy: cross_site_access_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#cross_site_access_policy MediaLiveEvent#cross_site_access_policy}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#description MediaLiveEvent#description}.
        :param encoding: encoding block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#encoding MediaLiveEvent#encoding}
        :param hostname_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#hostname_prefix MediaLiveEvent#hostname_prefix}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#id MediaLiveEvent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param preview: preview block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#preview MediaLiveEvent#preview}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#tags MediaLiveEvent#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#timeouts MediaLiveEvent#timeouts}
        :param transcription_languages: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#transcription_languages MediaLiveEvent#transcription_languages}.
        :param use_static_hostname: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#use_static_hostname MediaLiveEvent#use_static_hostname}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(input, dict):
            input = MediaLiveEventInput(**input)
        if isinstance(cross_site_access_policy, dict):
            cross_site_access_policy = MediaLiveEventCrossSiteAccessPolicy(**cross_site_access_policy)
        if isinstance(encoding, dict):
            encoding = MediaLiveEventEncoding(**encoding)
        if isinstance(preview, dict):
            preview = MediaLiveEventPreview(**preview)
        if isinstance(timeouts, dict):
            timeouts = MediaLiveEventTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8d53aa9f3a0b12aaf1c94939cee4d6cc5201d9b134e721cfdad26f20c9b9c9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument media_services_account_name", value=media_services_account_name, expected_type=type_hints["media_services_account_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument auto_start_enabled", value=auto_start_enabled, expected_type=type_hints["auto_start_enabled"])
            check_type(argname="argument cross_site_access_policy", value=cross_site_access_policy, expected_type=type_hints["cross_site_access_policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument hostname_prefix", value=hostname_prefix, expected_type=type_hints["hostname_prefix"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument preview", value=preview, expected_type=type_hints["preview"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument transcription_languages", value=transcription_languages, expected_type=type_hints["transcription_languages"])
            check_type(argname="argument use_static_hostname", value=use_static_hostname, expected_type=type_hints["use_static_hostname"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input": input,
            "location": location,
            "media_services_account_name": media_services_account_name,
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
        if auto_start_enabled is not None:
            self._values["auto_start_enabled"] = auto_start_enabled
        if cross_site_access_policy is not None:
            self._values["cross_site_access_policy"] = cross_site_access_policy
        if description is not None:
            self._values["description"] = description
        if encoding is not None:
            self._values["encoding"] = encoding
        if hostname_prefix is not None:
            self._values["hostname_prefix"] = hostname_prefix
        if id is not None:
            self._values["id"] = id
        if preview is not None:
            self._values["preview"] = preview
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if transcription_languages is not None:
            self._values["transcription_languages"] = transcription_languages
        if use_static_hostname is not None:
            self._values["use_static_hostname"] = use_static_hostname

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
    def input(self) -> "MediaLiveEventInput":
        '''input block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#input MediaLiveEvent#input}
        '''
        result = self._values.get("input")
        assert result is not None, "Required property 'input' is missing"
        return typing.cast("MediaLiveEventInput", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#location MediaLiveEvent#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def media_services_account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#media_services_account_name MediaLiveEvent#media_services_account_name}.'''
        result = self._values.get("media_services_account_name")
        assert result is not None, "Required property 'media_services_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#name MediaLiveEvent#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#resource_group_name MediaLiveEvent#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_start_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#auto_start_enabled MediaLiveEvent#auto_start_enabled}.'''
        result = self._values.get("auto_start_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cross_site_access_policy(
        self,
    ) -> typing.Optional["MediaLiveEventCrossSiteAccessPolicy"]:
        '''cross_site_access_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#cross_site_access_policy MediaLiveEvent#cross_site_access_policy}
        '''
        result = self._values.get("cross_site_access_policy")
        return typing.cast(typing.Optional["MediaLiveEventCrossSiteAccessPolicy"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#description MediaLiveEvent#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encoding(self) -> typing.Optional["MediaLiveEventEncoding"]:
        '''encoding block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#encoding MediaLiveEvent#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional["MediaLiveEventEncoding"], result)

    @builtins.property
    def hostname_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#hostname_prefix MediaLiveEvent#hostname_prefix}.'''
        result = self._values.get("hostname_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#id MediaLiveEvent#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preview(self) -> typing.Optional["MediaLiveEventPreview"]:
        '''preview block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#preview MediaLiveEvent#preview}
        '''
        result = self._values.get("preview")
        return typing.cast(typing.Optional["MediaLiveEventPreview"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#tags MediaLiveEvent#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MediaLiveEventTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#timeouts MediaLiveEvent#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MediaLiveEventTimeouts"], result)

    @builtins.property
    def transcription_languages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#transcription_languages MediaLiveEvent#transcription_languages}.'''
        result = self._values.get("transcription_languages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def use_static_hostname(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#use_static_hostname MediaLiveEvent#use_static_hostname}.'''
        result = self._values.get("use_static_hostname")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventCrossSiteAccessPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "client_access_policy": "clientAccessPolicy",
        "cross_domain_policy": "crossDomainPolicy",
    },
)
class MediaLiveEventCrossSiteAccessPolicy:
    def __init__(
        self,
        *,
        client_access_policy: typing.Optional[builtins.str] = None,
        cross_domain_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_access_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#client_access_policy MediaLiveEvent#client_access_policy}.
        :param cross_domain_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#cross_domain_policy MediaLiveEvent#cross_domain_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bfd699ec6dad15953c6ab801608b45202a7e02e4703d52878968382b4dffa73)
            check_type(argname="argument client_access_policy", value=client_access_policy, expected_type=type_hints["client_access_policy"])
            check_type(argname="argument cross_domain_policy", value=cross_domain_policy, expected_type=type_hints["cross_domain_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_access_policy is not None:
            self._values["client_access_policy"] = client_access_policy
        if cross_domain_policy is not None:
            self._values["cross_domain_policy"] = cross_domain_policy

    @builtins.property
    def client_access_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#client_access_policy MediaLiveEvent#client_access_policy}.'''
        result = self._values.get("client_access_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_domain_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#cross_domain_policy MediaLiveEvent#cross_domain_policy}.'''
        result = self._values.get("cross_domain_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventCrossSiteAccessPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaLiveEventCrossSiteAccessPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventCrossSiteAccessPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd0c67ed9bffdcb00a3a8080e7f76e0f99d2cd84bb6ab4f317756938a100b9df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientAccessPolicy")
    def reset_client_access_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientAccessPolicy", []))

    @jsii.member(jsii_name="resetCrossDomainPolicy")
    def reset_cross_domain_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossDomainPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="clientAccessPolicyInput")
    def client_access_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientAccessPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="crossDomainPolicyInput")
    def cross_domain_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossDomainPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="clientAccessPolicy")
    def client_access_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientAccessPolicy"))

    @client_access_policy.setter
    def client_access_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f34333485069bfd766fde7a650cc9066c4dfe60ba50198a50b75b009cdcf70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientAccessPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="crossDomainPolicy")
    def cross_domain_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossDomainPolicy"))

    @cross_domain_policy.setter
    def cross_domain_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c0526712708d927410747db3aad46551632c583b1a6d3acd3d48aae29738a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossDomainPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MediaLiveEventCrossSiteAccessPolicy]:
        return typing.cast(typing.Optional[MediaLiveEventCrossSiteAccessPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaLiveEventCrossSiteAccessPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4b477921d1c379911a76fd2e8a771d7dd6d568584ac7468023226ac3700dff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventEncoding",
    jsii_struct_bases=[],
    name_mapping={
        "key_frame_interval": "keyFrameInterval",
        "preset_name": "presetName",
        "stretch_mode": "stretchMode",
        "type": "type",
    },
)
class MediaLiveEventEncoding:
    def __init__(
        self,
        *,
        key_frame_interval: typing.Optional[builtins.str] = None,
        preset_name: typing.Optional[builtins.str] = None,
        stretch_mode: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_frame_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#key_frame_interval MediaLiveEvent#key_frame_interval}.
        :param preset_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#preset_name MediaLiveEvent#preset_name}.
        :param stretch_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#stretch_mode MediaLiveEvent#stretch_mode}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#type MediaLiveEvent#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0353ef3e6b25954afaf3f4837fa822b0819f5e6fdc143ede5e799a84ed79fd74)
            check_type(argname="argument key_frame_interval", value=key_frame_interval, expected_type=type_hints["key_frame_interval"])
            check_type(argname="argument preset_name", value=preset_name, expected_type=type_hints["preset_name"])
            check_type(argname="argument stretch_mode", value=stretch_mode, expected_type=type_hints["stretch_mode"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key_frame_interval is not None:
            self._values["key_frame_interval"] = key_frame_interval
        if preset_name is not None:
            self._values["preset_name"] = preset_name
        if stretch_mode is not None:
            self._values["stretch_mode"] = stretch_mode
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def key_frame_interval(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#key_frame_interval MediaLiveEvent#key_frame_interval}.'''
        result = self._values.get("key_frame_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preset_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#preset_name MediaLiveEvent#preset_name}.'''
        result = self._values.get("preset_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stretch_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#stretch_mode MediaLiveEvent#stretch_mode}.'''
        result = self._values.get("stretch_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#type MediaLiveEvent#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventEncoding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaLiveEventEncodingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventEncodingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cf53a878cde169403358da7dcdae4e226dbdd973a3ace6816522634bc107278)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeyFrameInterval")
    def reset_key_frame_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyFrameInterval", []))

    @jsii.member(jsii_name="resetPresetName")
    def reset_preset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPresetName", []))

    @jsii.member(jsii_name="resetStretchMode")
    def reset_stretch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStretchMode", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="keyFrameIntervalInput")
    def key_frame_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyFrameIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="presetNameInput")
    def preset_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "presetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="stretchModeInput")
    def stretch_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stretchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="keyFrameInterval")
    def key_frame_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyFrameInterval"))

    @key_frame_interval.setter
    def key_frame_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a5a0dcf56e9a965a7d47792125cad0fdc8b6909132c96d21f9e7692d6dffe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyFrameInterval", value)

    @builtins.property
    @jsii.member(jsii_name="presetName")
    def preset_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "presetName"))

    @preset_name.setter
    def preset_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a7e5b3776ed81e08dbe01d7d512123648ca9c66e90884e0782bd617475bf92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presetName", value)

    @builtins.property
    @jsii.member(jsii_name="stretchMode")
    def stretch_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stretchMode"))

    @stretch_mode.setter
    def stretch_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bac910cd7251c5122a75d324acad70dd846bf73eccf2afaa646326dccaeb3ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stretchMode", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8925678800f4423652d32ddeca5cbb16464ba969d2d640c12bd93c5814391d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MediaLiveEventEncoding]:
        return typing.cast(typing.Optional[MediaLiveEventEncoding], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MediaLiveEventEncoding]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cceb72dd567ddc1b1fdbf7745bf32f267ff39bf59e0e2cc34b6fe1a3d33bf69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventInput",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "ip_access_control_allow": "ipAccessControlAllow",
        "key_frame_interval_duration": "keyFrameIntervalDuration",
        "streaming_protocol": "streamingProtocol",
    },
)
class MediaLiveEventInput:
    def __init__(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        ip_access_control_allow: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaLiveEventInputIpAccessControlAllow", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key_frame_interval_duration: typing.Optional[builtins.str] = None,
        streaming_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#access_token MediaLiveEvent#access_token}.
        :param ip_access_control_allow: ip_access_control_allow block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#ip_access_control_allow MediaLiveEvent#ip_access_control_allow}
        :param key_frame_interval_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#key_frame_interval_duration MediaLiveEvent#key_frame_interval_duration}.
        :param streaming_protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#streaming_protocol MediaLiveEvent#streaming_protocol}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795135a3c5511151b10a7f9a95a5e92fe8093e022f3f6a9899ddb130a1dc871b)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument ip_access_control_allow", value=ip_access_control_allow, expected_type=type_hints["ip_access_control_allow"])
            check_type(argname="argument key_frame_interval_duration", value=key_frame_interval_duration, expected_type=type_hints["key_frame_interval_duration"])
            check_type(argname="argument streaming_protocol", value=streaming_protocol, expected_type=type_hints["streaming_protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if ip_access_control_allow is not None:
            self._values["ip_access_control_allow"] = ip_access_control_allow
        if key_frame_interval_duration is not None:
            self._values["key_frame_interval_duration"] = key_frame_interval_duration
        if streaming_protocol is not None:
            self._values["streaming_protocol"] = streaming_protocol

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#access_token MediaLiveEvent#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_access_control_allow(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaLiveEventInputIpAccessControlAllow"]]]:
        '''ip_access_control_allow block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#ip_access_control_allow MediaLiveEvent#ip_access_control_allow}
        '''
        result = self._values.get("ip_access_control_allow")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaLiveEventInputIpAccessControlAllow"]]], result)

    @builtins.property
    def key_frame_interval_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#key_frame_interval_duration MediaLiveEvent#key_frame_interval_duration}.'''
        result = self._values.get("key_frame_interval_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def streaming_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#streaming_protocol MediaLiveEvent#streaming_protocol}.'''
        result = self._values.get("streaming_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventInputEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class MediaLiveEventInputEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventInputEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaLiveEventInputEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventInputEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24a457151f8297f6ef25562483c05be5c2d2c1b8ded99214676f18e5a84cf058)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MediaLiveEventInputEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3ae17ca8f5612e73d87e73e9d07c32d4c2ad9f6ff3960c2213c2e5a14b156f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MediaLiveEventInputEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f6e78ce51498b3e03ec0f46952c94c69a3c6125894c1e1c990e1f94a907b81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b36c3e6e1d710ff43a5e09eeef0870df2c05052cf25d18ae0533f620cc09a60a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfeb8f8d318d61127439a08e3a6775f2c87387ad4d34b8259af02cacaabd2f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class MediaLiveEventInputEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventInputEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ff817110f91e6a928c47264806e1d2ce563f9ab775750a08cd720a00a86e5a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MediaLiveEventInputEndpoint]:
        return typing.cast(typing.Optional[MediaLiveEventInputEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaLiveEventInputEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__276a0174e4cad4ee0a9eee80016ee1783bb35faad5ed7955e57b0170d41b9fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventInputIpAccessControlAllow",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "name": "name",
        "subnet_prefix_length": "subnetPrefixLength",
    },
)
class MediaLiveEventInputIpAccessControlAllow:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        subnet_prefix_length: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#address MediaLiveEvent#address}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#name MediaLiveEvent#name}.
        :param subnet_prefix_length: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#subnet_prefix_length MediaLiveEvent#subnet_prefix_length}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7295f584c83cb79ac1755a5532928d52d8b1a699722140fc967cb39c95cfc0d)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnet_prefix_length", value=subnet_prefix_length, expected_type=type_hints["subnet_prefix_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if name is not None:
            self._values["name"] = name
        if subnet_prefix_length is not None:
            self._values["subnet_prefix_length"] = subnet_prefix_length

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#address MediaLiveEvent#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#name MediaLiveEvent#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_prefix_length(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#subnet_prefix_length MediaLiveEvent#subnet_prefix_length}.'''
        result = self._values.get("subnet_prefix_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventInputIpAccessControlAllow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaLiveEventInputIpAccessControlAllowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventInputIpAccessControlAllowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f38f1f678cfd669614c92ef6fa574d3d155377e5c5f3079dbeec2ab9e9e66827)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MediaLiveEventInputIpAccessControlAllowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5b508aa643e470936a7d4c9461abb7067499dcf3cafc99bbf464044d305c73)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MediaLiveEventInputIpAccessControlAllowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b491786fc44e3ff168a7cc2d99971cb2ea058095afbaf4c4f592223bba745a54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__284b0d18ba2b3e7e264a83006a07ae8355b91c9db9821cc4f85ee00b00e140a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da00cb427042874aef5bc69a8a4ca4d57c4542744162fa328502ff6f326b5162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventInputIpAccessControlAllow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventInputIpAccessControlAllow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventInputIpAccessControlAllow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e273e8b9008366bcf6f2ccbe6434ea0a7ab40f9af2651534180ea375a1969717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaLiveEventInputIpAccessControlAllowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventInputIpAccessControlAllowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7338c83247c55e2861b56af790bff8eef89307c114e8803e82b335c71190ae1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSubnetPrefixLength")
    def reset_subnet_prefix_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetPrefixLength", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetPrefixLengthInput")
    def subnet_prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "subnetPrefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f2f87209abab85c8b11791bb4a845512b307f5b34b049a7b8ac840e8d5020f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc8f57bc2461fbdcf672f6bd97d226eb387584f580af8624065d43c4f183f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="subnetPrefixLength")
    def subnet_prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "subnetPrefixLength"))

    @subnet_prefix_length.setter
    def subnet_prefix_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e41b48f149799f2c7057e2f8b2eb7de77436b9d7692c8f4f746ef7c951d3d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetPrefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaLiveEventInputIpAccessControlAllow, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaLiveEventInputIpAccessControlAllow, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaLiveEventInputIpAccessControlAllow, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb37534fea9455d563505e8433ea32e332d59a7f0a8d3342b8c6f5b072a1f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaLiveEventInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9d2121d745321555f271ea428e18837d29976aae408c937c8a607f67f932ca0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpAccessControlAllow")
    def put_ip_access_control_allow(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaLiveEventInputIpAccessControlAllow, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab63860848f34d3a4e1c85ddee3491d15b9818cf093559539bed6624cd62492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpAccessControlAllow", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetIpAccessControlAllow")
    def reset_ip_access_control_allow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAccessControlAllow", []))

    @jsii.member(jsii_name="resetKeyFrameIntervalDuration")
    def reset_key_frame_interval_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyFrameIntervalDuration", []))

    @jsii.member(jsii_name="resetStreamingProtocol")
    def reset_streaming_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreamingProtocol", []))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> MediaLiveEventInputEndpointList:
        return typing.cast(MediaLiveEventInputEndpointList, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="ipAccessControlAllow")
    def ip_access_control_allow(self) -> MediaLiveEventInputIpAccessControlAllowList:
        return typing.cast(MediaLiveEventInputIpAccessControlAllowList, jsii.get(self, "ipAccessControlAllow"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAccessControlAllowInput")
    def ip_access_control_allow_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventInputIpAccessControlAllow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventInputIpAccessControlAllow]]], jsii.get(self, "ipAccessControlAllowInput"))

    @builtins.property
    @jsii.member(jsii_name="keyFrameIntervalDurationInput")
    def key_frame_interval_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyFrameIntervalDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="streamingProtocolInput")
    def streaming_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamingProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aad9b0ce6e480af862726222c610510e2901269d449deaa2d3c21a2e4499160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value)

    @builtins.property
    @jsii.member(jsii_name="keyFrameIntervalDuration")
    def key_frame_interval_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyFrameIntervalDuration"))

    @key_frame_interval_duration.setter
    def key_frame_interval_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fee4832c093c8a6989f8bc283119c5ccf9e7ce224f09bb4414aa726a8ca141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyFrameIntervalDuration", value)

    @builtins.property
    @jsii.member(jsii_name="streamingProtocol")
    def streaming_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamingProtocol"))

    @streaming_protocol.setter
    def streaming_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006d04e71baa5b0fdc91274ca9eae02d6a78477155f1c0dcd198db8359084487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamingProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MediaLiveEventInput]:
        return typing.cast(typing.Optional[MediaLiveEventInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MediaLiveEventInput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0376ac5c506356b4085cd25d28210a8c62c338f372a2505e5b903477df7f9af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventPreview",
    jsii_struct_bases=[],
    name_mapping={
        "alternative_media_id": "alternativeMediaId",
        "ip_access_control_allow": "ipAccessControlAllow",
        "preview_locator": "previewLocator",
        "streaming_policy_name": "streamingPolicyName",
    },
)
class MediaLiveEventPreview:
    def __init__(
        self,
        *,
        alternative_media_id: typing.Optional[builtins.str] = None,
        ip_access_control_allow: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaLiveEventPreviewIpAccessControlAllow", typing.Dict[builtins.str, typing.Any]]]]] = None,
        preview_locator: typing.Optional[builtins.str] = None,
        streaming_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alternative_media_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#alternative_media_id MediaLiveEvent#alternative_media_id}.
        :param ip_access_control_allow: ip_access_control_allow block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#ip_access_control_allow MediaLiveEvent#ip_access_control_allow}
        :param preview_locator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#preview_locator MediaLiveEvent#preview_locator}.
        :param streaming_policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#streaming_policy_name MediaLiveEvent#streaming_policy_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec03f4c46c7ab2af4dcecadf0896c428ea5845d9172f9775ef9e40edb64c054)
            check_type(argname="argument alternative_media_id", value=alternative_media_id, expected_type=type_hints["alternative_media_id"])
            check_type(argname="argument ip_access_control_allow", value=ip_access_control_allow, expected_type=type_hints["ip_access_control_allow"])
            check_type(argname="argument preview_locator", value=preview_locator, expected_type=type_hints["preview_locator"])
            check_type(argname="argument streaming_policy_name", value=streaming_policy_name, expected_type=type_hints["streaming_policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alternative_media_id is not None:
            self._values["alternative_media_id"] = alternative_media_id
        if ip_access_control_allow is not None:
            self._values["ip_access_control_allow"] = ip_access_control_allow
        if preview_locator is not None:
            self._values["preview_locator"] = preview_locator
        if streaming_policy_name is not None:
            self._values["streaming_policy_name"] = streaming_policy_name

    @builtins.property
    def alternative_media_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#alternative_media_id MediaLiveEvent#alternative_media_id}.'''
        result = self._values.get("alternative_media_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_access_control_allow(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaLiveEventPreviewIpAccessControlAllow"]]]:
        '''ip_access_control_allow block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#ip_access_control_allow MediaLiveEvent#ip_access_control_allow}
        '''
        result = self._values.get("ip_access_control_allow")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaLiveEventPreviewIpAccessControlAllow"]]], result)

    @builtins.property
    def preview_locator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#preview_locator MediaLiveEvent#preview_locator}.'''
        result = self._values.get("preview_locator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def streaming_policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#streaming_policy_name MediaLiveEvent#streaming_policy_name}.'''
        result = self._values.get("streaming_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventPreview(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventPreviewEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class MediaLiveEventPreviewEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventPreviewEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaLiveEventPreviewEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventPreviewEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__540e4fd1b3a7b07be40cbdc08a2d7e0b4e5d345a446f848e1e0246909d25fbdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MediaLiveEventPreviewEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa60b6d9c58a3233b2f41fcfdfecba5a37a9d1c14313907b5fc3cb9f32eaec8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MediaLiveEventPreviewEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378173be1375e597c3255fcb2a9176a91f266fab98847f7a845c5df093e299ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3789dc5951b0af3587029ad5bcac291af3edad85d45b3787b46da1e88ff7b7b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__583510bd1d9932d6962e1502df4f290c45b4afd52dc68c4ad50e7a3effb77f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class MediaLiveEventPreviewEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventPreviewEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5c52f8b4758db915001189a9d4d14ab03df2d28bff9fc2bf609b69290065c2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MediaLiveEventPreviewEndpoint]:
        return typing.cast(typing.Optional[MediaLiveEventPreviewEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaLiveEventPreviewEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3372d32a40fb5eac251cf711ed623486d2efa715c8e5fc3a4d276af59bf71a24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventPreviewIpAccessControlAllow",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "name": "name",
        "subnet_prefix_length": "subnetPrefixLength",
    },
)
class MediaLiveEventPreviewIpAccessControlAllow:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        subnet_prefix_length: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#address MediaLiveEvent#address}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#name MediaLiveEvent#name}.
        :param subnet_prefix_length: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#subnet_prefix_length MediaLiveEvent#subnet_prefix_length}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82cea7f02d912dd49c0c7e5ad57991a8715d51b7197fe47a30da8c9b249e7a4c)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnet_prefix_length", value=subnet_prefix_length, expected_type=type_hints["subnet_prefix_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if name is not None:
            self._values["name"] = name
        if subnet_prefix_length is not None:
            self._values["subnet_prefix_length"] = subnet_prefix_length

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#address MediaLiveEvent#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#name MediaLiveEvent#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_prefix_length(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#subnet_prefix_length MediaLiveEvent#subnet_prefix_length}.'''
        result = self._values.get("subnet_prefix_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventPreviewIpAccessControlAllow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaLiveEventPreviewIpAccessControlAllowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventPreviewIpAccessControlAllowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93513e58219611377549f3968ba302682a0a466cc2882e2d92261939041eff6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MediaLiveEventPreviewIpAccessControlAllowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f76fbc648de59cbb631dfdcbd5f251492fb419f0d7af789eb6ccbe40189ef0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MediaLiveEventPreviewIpAccessControlAllowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87487985fb84604b9b27d4ff0091d82faf5c337bc373f82f80ef0c8bfe87af0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6978504beb0b2897ec9e335d8c782ed2783391f450d54387e130a38c8ccbd80d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__128ba675f8e1de52f8d71780f61913611dd406cc215db39cbfba98a554b612ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventPreviewIpAccessControlAllow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventPreviewIpAccessControlAllow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventPreviewIpAccessControlAllow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ba469db25a27976fd821af32cd83ea8d3183e10e2a74deffe48e15c3d98850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaLiveEventPreviewIpAccessControlAllowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventPreviewIpAccessControlAllowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8806a70042d5d844a6f5823251ade5bbb2f37820fcbbfa2dbb360cc23527afe1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSubnetPrefixLength")
    def reset_subnet_prefix_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetPrefixLength", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetPrefixLengthInput")
    def subnet_prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "subnetPrefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85915edafbc23dba38515ce2c850b2cbb4fd6a0a9321ef924f7cd8280b80c020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e32643dada0cf4e7c9999e2a8fc9f6f57bbc811c10f2f4fea004799f40235d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="subnetPrefixLength")
    def subnet_prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "subnetPrefixLength"))

    @subnet_prefix_length.setter
    def subnet_prefix_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00427135d07f5ef477b8deb3b1c074d35ba193eff4c1b20d15cf189bc7f39450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetPrefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaLiveEventPreviewIpAccessControlAllow, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaLiveEventPreviewIpAccessControlAllow, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaLiveEventPreviewIpAccessControlAllow, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d20ee461f83852b5ae36374d6bba3d3e3934af5528cd8fda20b5f2de04046cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaLiveEventPreviewOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventPreviewOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe35754e6de8bf351bfac3b0cddca8b5d7d8398c9e6b43143c63129de764d93c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpAccessControlAllow")
    def put_ip_access_control_allow(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaLiveEventPreviewIpAccessControlAllow, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19674192a4b81936b94318b894546acc1acde433c8abadf90daa64760395fae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpAccessControlAllow", [value]))

    @jsii.member(jsii_name="resetAlternativeMediaId")
    def reset_alternative_media_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlternativeMediaId", []))

    @jsii.member(jsii_name="resetIpAccessControlAllow")
    def reset_ip_access_control_allow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAccessControlAllow", []))

    @jsii.member(jsii_name="resetPreviewLocator")
    def reset_preview_locator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreviewLocator", []))

    @jsii.member(jsii_name="resetStreamingPolicyName")
    def reset_streaming_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreamingPolicyName", []))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> MediaLiveEventPreviewEndpointList:
        return typing.cast(MediaLiveEventPreviewEndpointList, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="ipAccessControlAllow")
    def ip_access_control_allow(self) -> MediaLiveEventPreviewIpAccessControlAllowList:
        return typing.cast(MediaLiveEventPreviewIpAccessControlAllowList, jsii.get(self, "ipAccessControlAllow"))

    @builtins.property
    @jsii.member(jsii_name="alternativeMediaIdInput")
    def alternative_media_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alternativeMediaIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAccessControlAllowInput")
    def ip_access_control_allow_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventPreviewIpAccessControlAllow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventPreviewIpAccessControlAllow]]], jsii.get(self, "ipAccessControlAllowInput"))

    @builtins.property
    @jsii.member(jsii_name="previewLocatorInput")
    def preview_locator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "previewLocatorInput"))

    @builtins.property
    @jsii.member(jsii_name="streamingPolicyNameInput")
    def streaming_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamingPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="alternativeMediaId")
    def alternative_media_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alternativeMediaId"))

    @alternative_media_id.setter
    def alternative_media_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8dd46838efbfb2fc4d403ddfee44565c3818d743de4373266513547f6a4aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alternativeMediaId", value)

    @builtins.property
    @jsii.member(jsii_name="previewLocator")
    def preview_locator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "previewLocator"))

    @preview_locator.setter
    def preview_locator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d8c539007d04daac569da14051778fe09ef047bbf99fb4873cd21c428f5240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "previewLocator", value)

    @builtins.property
    @jsii.member(jsii_name="streamingPolicyName")
    def streaming_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamingPolicyName"))

    @streaming_policy_name.setter
    def streaming_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac343ec2d5ef4bc32d00d1cf2fdd6150abfc97069b6c7fa882bda8fe35b999b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamingPolicyName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MediaLiveEventPreview]:
        return typing.cast(typing.Optional[MediaLiveEventPreview], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MediaLiveEventPreview]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ddc25d54d6419a5c6e0ca455059bd70957194d271b3046bd864db873a89c09a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MediaLiveEventTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#create MediaLiveEvent#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#delete MediaLiveEvent#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#read MediaLiveEvent#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#update MediaLiveEvent#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39115dec8de3aee2a5f79a4dadc24df8a8b9ccb5c4964ce09a70a42f857b59a7)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#create MediaLiveEvent#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#delete MediaLiveEvent#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#read MediaLiveEvent#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_live_event#update MediaLiveEvent#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaLiveEventTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaLiveEventTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaLiveEvent.MediaLiveEventTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73dc91f30db547683d40b76622f8a2c4e6a13e89ead29917b91467871e00c0ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bc41ba10519cb56a21a03366278879a117939b1952cffdaac1f0fa35d5e1754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c0b96f76bab638623b90172089b5b16be1a1987d31b660d3a9bde3a42e7efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd056096f8ad600d9323820f17b3af5a7c0f454a653d6f52ff2a7eca8bc65980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d997a042efebd3f549d0a3ddd11203dc3fcffc39d4881688019e45b5c0ee89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaLiveEventTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaLiveEventTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaLiveEventTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5246cae1d323dd4103f3c797e1754327dfbf9482857bc72ebb9788d83cf76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MediaLiveEvent",
    "MediaLiveEventConfig",
    "MediaLiveEventCrossSiteAccessPolicy",
    "MediaLiveEventCrossSiteAccessPolicyOutputReference",
    "MediaLiveEventEncoding",
    "MediaLiveEventEncodingOutputReference",
    "MediaLiveEventInput",
    "MediaLiveEventInputEndpoint",
    "MediaLiveEventInputEndpointList",
    "MediaLiveEventInputEndpointOutputReference",
    "MediaLiveEventInputIpAccessControlAllow",
    "MediaLiveEventInputIpAccessControlAllowList",
    "MediaLiveEventInputIpAccessControlAllowOutputReference",
    "MediaLiveEventInputOutputReference",
    "MediaLiveEventPreview",
    "MediaLiveEventPreviewEndpoint",
    "MediaLiveEventPreviewEndpointList",
    "MediaLiveEventPreviewEndpointOutputReference",
    "MediaLiveEventPreviewIpAccessControlAllow",
    "MediaLiveEventPreviewIpAccessControlAllowList",
    "MediaLiveEventPreviewIpAccessControlAllowOutputReference",
    "MediaLiveEventPreviewOutputReference",
    "MediaLiveEventTimeouts",
    "MediaLiveEventTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b6ba1361290340f82443589c170eb8d6f24804dc0d4c781851725bb05cc64651(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    input: typing.Union[MediaLiveEventInput, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    media_services_account_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    auto_start_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cross_site_access_policy: typing.Optional[typing.Union[MediaLiveEventCrossSiteAccessPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    encoding: typing.Optional[typing.Union[MediaLiveEventEncoding, typing.Dict[builtins.str, typing.Any]]] = None,
    hostname_prefix: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    preview: typing.Optional[typing.Union[MediaLiveEventPreview, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MediaLiveEventTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transcription_languages: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_static_hostname: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__29557b8c4f62ceff4249272133c9a6211fa4b2081d78f80d9deeff3b947d3a27(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3b28a309af7f223f72e22062914c1312a1898ea35292cce8d2c5ec9361fc22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcef4243f9f012f489591b986fffea664efac673c6bc3d3a51a47feb93a78bcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1eb7750039e59cd4e7f74f55c82be7626cdbf7f9dabb1f770b612bbe25e12d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4cfa507ca6b417d11e416f893a1237f335f2971679e9a1c6ec2de8560a8669(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11484efd66159574278ceb191fe60211db033cf863ac099e08fb24d107fdd8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26088f619cb5dbc639ebee596bcafd4dce03f9cc38b83fff09e86c7bfb9179a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc98475c8d83d87b2add942b19cbd48a47686ee5cfda2bb409f6b2a141838e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c324a8776a9f7a446d9acde5c67e6896f05e76c748501a4b40fbe8849847ba(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3525ccd52b80acf02a86ba215991f3132045692d59e8bb825f54fb3082cc35d6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae74e9fb0ad5323e6946ece09a24e19792195feeef2652a5014af6b9ec16017(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8d53aa9f3a0b12aaf1c94939cee4d6cc5201d9b134e721cfdad26f20c9b9c9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    input: typing.Union[MediaLiveEventInput, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    media_services_account_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    auto_start_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cross_site_access_policy: typing.Optional[typing.Union[MediaLiveEventCrossSiteAccessPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    encoding: typing.Optional[typing.Union[MediaLiveEventEncoding, typing.Dict[builtins.str, typing.Any]]] = None,
    hostname_prefix: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    preview: typing.Optional[typing.Union[MediaLiveEventPreview, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MediaLiveEventTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transcription_languages: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_static_hostname: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bfd699ec6dad15953c6ab801608b45202a7e02e4703d52878968382b4dffa73(
    *,
    client_access_policy: typing.Optional[builtins.str] = None,
    cross_domain_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0c67ed9bffdcb00a3a8080e7f76e0f99d2cd84bb6ab4f317756938a100b9df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f34333485069bfd766fde7a650cc9066c4dfe60ba50198a50b75b009cdcf70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c0526712708d927410747db3aad46551632c583b1a6d3acd3d48aae29738a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4b477921d1c379911a76fd2e8a771d7dd6d568584ac7468023226ac3700dff(
    value: typing.Optional[MediaLiveEventCrossSiteAccessPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0353ef3e6b25954afaf3f4837fa822b0819f5e6fdc143ede5e799a84ed79fd74(
    *,
    key_frame_interval: typing.Optional[builtins.str] = None,
    preset_name: typing.Optional[builtins.str] = None,
    stretch_mode: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf53a878cde169403358da7dcdae4e226dbdd973a3ace6816522634bc107278(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a5a0dcf56e9a965a7d47792125cad0fdc8b6909132c96d21f9e7692d6dffe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a7e5b3776ed81e08dbe01d7d512123648ca9c66e90884e0782bd617475bf92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bac910cd7251c5122a75d324acad70dd846bf73eccf2afaa646326dccaeb3ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8925678800f4423652d32ddeca5cbb16464ba969d2d640c12bd93c5814391d59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cceb72dd567ddc1b1fdbf7745bf32f267ff39bf59e0e2cc34b6fe1a3d33bf69(
    value: typing.Optional[MediaLiveEventEncoding],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795135a3c5511151b10a7f9a95a5e92fe8093e022f3f6a9899ddb130a1dc871b(
    *,
    access_token: typing.Optional[builtins.str] = None,
    ip_access_control_allow: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaLiveEventInputIpAccessControlAllow, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_frame_interval_duration: typing.Optional[builtins.str] = None,
    streaming_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a457151f8297f6ef25562483c05be5c2d2c1b8ded99214676f18e5a84cf058(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3ae17ca8f5612e73d87e73e9d07c32d4c2ad9f6ff3960c2213c2e5a14b156f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f6e78ce51498b3e03ec0f46952c94c69a3c6125894c1e1c990e1f94a907b81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36c3e6e1d710ff43a5e09eeef0870df2c05052cf25d18ae0533f620cc09a60a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfeb8f8d318d61127439a08e3a6775f2c87387ad4d34b8259af02cacaabd2f0a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff817110f91e6a928c47264806e1d2ce563f9ab775750a08cd720a00a86e5a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276a0174e4cad4ee0a9eee80016ee1783bb35faad5ed7955e57b0170d41b9fc2(
    value: typing.Optional[MediaLiveEventInputEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7295f584c83cb79ac1755a5532928d52d8b1a699722140fc967cb39c95cfc0d(
    *,
    address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    subnet_prefix_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38f1f678cfd669614c92ef6fa574d3d155377e5c5f3079dbeec2ab9e9e66827(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5b508aa643e470936a7d4c9461abb7067499dcf3cafc99bbf464044d305c73(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b491786fc44e3ff168a7cc2d99971cb2ea058095afbaf4c4f592223bba745a54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284b0d18ba2b3e7e264a83006a07ae8355b91c9db9821cc4f85ee00b00e140a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da00cb427042874aef5bc69a8a4ca4d57c4542744162fa328502ff6f326b5162(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e273e8b9008366bcf6f2ccbe6434ea0a7ab40f9af2651534180ea375a1969717(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventInputIpAccessControlAllow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7338c83247c55e2861b56af790bff8eef89307c114e8803e82b335c71190ae1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f2f87209abab85c8b11791bb4a845512b307f5b34b049a7b8ac840e8d5020f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc8f57bc2461fbdcf672f6bd97d226eb387584f580af8624065d43c4f183f4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e41b48f149799f2c7057e2f8b2eb7de77436b9d7692c8f4f746ef7c951d3d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb37534fea9455d563505e8433ea32e332d59a7f0a8d3342b8c6f5b072a1f47(
    value: typing.Optional[typing.Union[MediaLiveEventInputIpAccessControlAllow, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d2121d745321555f271ea428e18837d29976aae408c937c8a607f67f932ca0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab63860848f34d3a4e1c85ddee3491d15b9818cf093559539bed6624cd62492(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaLiveEventInputIpAccessControlAllow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aad9b0ce6e480af862726222c610510e2901269d449deaa2d3c21a2e4499160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fee4832c093c8a6989f8bc283119c5ccf9e7ce224f09bb4414aa726a8ca141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006d04e71baa5b0fdc91274ca9eae02d6a78477155f1c0dcd198db8359084487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0376ac5c506356b4085cd25d28210a8c62c338f372a2505e5b903477df7f9af5(
    value: typing.Optional[MediaLiveEventInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec03f4c46c7ab2af4dcecadf0896c428ea5845d9172f9775ef9e40edb64c054(
    *,
    alternative_media_id: typing.Optional[builtins.str] = None,
    ip_access_control_allow: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaLiveEventPreviewIpAccessControlAllow, typing.Dict[builtins.str, typing.Any]]]]] = None,
    preview_locator: typing.Optional[builtins.str] = None,
    streaming_policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540e4fd1b3a7b07be40cbdc08a2d7e0b4e5d345a446f848e1e0246909d25fbdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa60b6d9c58a3233b2f41fcfdfecba5a37a9d1c14313907b5fc3cb9f32eaec8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378173be1375e597c3255fcb2a9176a91f266fab98847f7a845c5df093e299ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3789dc5951b0af3587029ad5bcac291af3edad85d45b3787b46da1e88ff7b7b3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583510bd1d9932d6962e1502df4f290c45b4afd52dc68c4ad50e7a3effb77f14(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c52f8b4758db915001189a9d4d14ab03df2d28bff9fc2bf609b69290065c2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3372d32a40fb5eac251cf711ed623486d2efa715c8e5fc3a4d276af59bf71a24(
    value: typing.Optional[MediaLiveEventPreviewEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82cea7f02d912dd49c0c7e5ad57991a8715d51b7197fe47a30da8c9b249e7a4c(
    *,
    address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    subnet_prefix_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93513e58219611377549f3968ba302682a0a466cc2882e2d92261939041eff6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f76fbc648de59cbb631dfdcbd5f251492fb419f0d7af789eb6ccbe40189ef0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87487985fb84604b9b27d4ff0091d82faf5c337bc373f82f80ef0c8bfe87af0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6978504beb0b2897ec9e335d8c782ed2783391f450d54387e130a38c8ccbd80d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128ba675f8e1de52f8d71780f61913611dd406cc215db39cbfba98a554b612ac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ba469db25a27976fd821af32cd83ea8d3183e10e2a74deffe48e15c3d98850(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaLiveEventPreviewIpAccessControlAllow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8806a70042d5d844a6f5823251ade5bbb2f37820fcbbfa2dbb360cc23527afe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85915edafbc23dba38515ce2c850b2cbb4fd6a0a9321ef924f7cd8280b80c020(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e32643dada0cf4e7c9999e2a8fc9f6f57bbc811c10f2f4fea004799f40235d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00427135d07f5ef477b8deb3b1c074d35ba193eff4c1b20d15cf189bc7f39450(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d20ee461f83852b5ae36374d6bba3d3e3934af5528cd8fda20b5f2de04046cb(
    value: typing.Optional[typing.Union[MediaLiveEventPreviewIpAccessControlAllow, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe35754e6de8bf351bfac3b0cddca8b5d7d8398c9e6b43143c63129de764d93c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19674192a4b81936b94318b894546acc1acde433c8abadf90daa64760395fae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaLiveEventPreviewIpAccessControlAllow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8dd46838efbfb2fc4d403ddfee44565c3818d743de4373266513547f6a4aa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d8c539007d04daac569da14051778fe09ef047bbf99fb4873cd21c428f5240(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac343ec2d5ef4bc32d00d1cf2fdd6150abfc97069b6c7fa882bda8fe35b999b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ddc25d54d6419a5c6e0ca455059bd70957194d271b3046bd864db873a89c09a(
    value: typing.Optional[MediaLiveEventPreview],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39115dec8de3aee2a5f79a4dadc24df8a8b9ccb5c4964ce09a70a42f857b59a7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73dc91f30db547683d40b76622f8a2c4e6a13e89ead29917b91467871e00c0ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc41ba10519cb56a21a03366278879a117939b1952cffdaac1f0fa35d5e1754(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c0b96f76bab638623b90172089b5b16be1a1987d31b660d3a9bde3a42e7efc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd056096f8ad600d9323820f17b3af5a7c0f454a653d6f52ff2a7eca8bc65980(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d997a042efebd3f549d0a3ddd11203dc3fcffc39d4881688019e45b5c0ee89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5246cae1d323dd4103f3c797e1754327dfbf9482857bc72ebb9788d83cf76d(
    value: typing.Optional[typing.Union[MediaLiveEventTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
