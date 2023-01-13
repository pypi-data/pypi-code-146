'''
# `azurerm_media_streaming_policy`

Refer to the Terraform Registory for docs: [`azurerm_media_streaming_policy`](https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy).
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


class MediaStreamingPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicy",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy azurerm_media_streaming_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        media_services_account_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        common_encryption_cbcs: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCbcs", typing.Dict[builtins.str, typing.Any]]] = None,
        common_encryption_cenc: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCenc", typing.Dict[builtins.str, typing.Any]]] = None,
        default_content_key_policy_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        no_encryption_enabled_protocols: typing.Optional[typing.Union["MediaStreamingPolicyNoEncryptionEnabledProtocols", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MediaStreamingPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy azurerm_media_streaming_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param media_services_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#media_services_account_name MediaStreamingPolicy#media_services_account_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#name MediaStreamingPolicy#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#resource_group_name MediaStreamingPolicy#resource_group_name}.
        :param common_encryption_cbcs: common_encryption_cbcs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#common_encryption_cbcs MediaStreamingPolicy#common_encryption_cbcs}
        :param common_encryption_cenc: common_encryption_cenc block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#common_encryption_cenc MediaStreamingPolicy#common_encryption_cenc}
        :param default_content_key_policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#default_content_key_policy_name MediaStreamingPolicy#default_content_key_policy_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#id MediaStreamingPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param no_encryption_enabled_protocols: no_encryption_enabled_protocols block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#no_encryption_enabled_protocols MediaStreamingPolicy#no_encryption_enabled_protocols}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#timeouts MediaStreamingPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16257c9d0eb4ef2573bad9116d8bb571c21ba680834a3edd53f19a45ea21697c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MediaStreamingPolicyConfig(
            media_services_account_name=media_services_account_name,
            name=name,
            resource_group_name=resource_group_name,
            common_encryption_cbcs=common_encryption_cbcs,
            common_encryption_cenc=common_encryption_cenc,
            default_content_key_policy_name=default_content_key_policy_name,
            id=id,
            no_encryption_enabled_protocols=no_encryption_enabled_protocols,
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

    @jsii.member(jsii_name="putCommonEncryptionCbcs")
    def put_common_encryption_cbcs(
        self,
        *,
        default_content_key: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey", typing.Dict[builtins.str, typing.Any]]] = None,
        drm_fairplay: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled_protocols: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_content_key: default_content_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#default_content_key MediaStreamingPolicy#default_content_key}
        :param drm_fairplay: drm_fairplay block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#drm_fairplay MediaStreamingPolicy#drm_fairplay}
        :param enabled_protocols: enabled_protocols block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#enabled_protocols MediaStreamingPolicy#enabled_protocols}
        '''
        value = MediaStreamingPolicyCommonEncryptionCbcs(
            default_content_key=default_content_key,
            drm_fairplay=drm_fairplay,
            enabled_protocols=enabled_protocols,
        )

        return typing.cast(None, jsii.invoke(self, "putCommonEncryptionCbcs", [value]))

    @jsii.member(jsii_name="putCommonEncryptionCenc")
    def put_common_encryption_cenc(
        self,
        *,
        default_content_key: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCencDefaultContentKey", typing.Dict[builtins.str, typing.Any]]] = None,
        drm_playready: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCencDrmPlayready", typing.Dict[builtins.str, typing.Any]]] = None,
        drm_widevine_custom_license_acquisition_url_template: typing.Optional[builtins.str] = None,
        enabled_protocols: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCencEnabledProtocols", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_content_key: default_content_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#default_content_key MediaStreamingPolicy#default_content_key}
        :param drm_playready: drm_playready block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#drm_playready MediaStreamingPolicy#drm_playready}
        :param drm_widevine_custom_license_acquisition_url_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#drm_widevine_custom_license_acquisition_url_template MediaStreamingPolicy#drm_widevine_custom_license_acquisition_url_template}.
        :param enabled_protocols: enabled_protocols block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#enabled_protocols MediaStreamingPolicy#enabled_protocols}
        '''
        value = MediaStreamingPolicyCommonEncryptionCenc(
            default_content_key=default_content_key,
            drm_playready=drm_playready,
            drm_widevine_custom_license_acquisition_url_template=drm_widevine_custom_license_acquisition_url_template,
            enabled_protocols=enabled_protocols,
        )

        return typing.cast(None, jsii.invoke(self, "putCommonEncryptionCenc", [value]))

    @jsii.member(jsii_name="putNoEncryptionEnabledProtocols")
    def put_no_encryption_enabled_protocols(
        self,
        *,
        dash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dash: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#dash MediaStreamingPolicy#dash}.
        :param download: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#download MediaStreamingPolicy#download}.
        :param hls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#hls MediaStreamingPolicy#hls}.
        :param smooth_streaming: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#smooth_streaming MediaStreamingPolicy#smooth_streaming}.
        '''
        value = MediaStreamingPolicyNoEncryptionEnabledProtocols(
            dash=dash, download=download, hls=hls, smooth_streaming=smooth_streaming
        )

        return typing.cast(None, jsii.invoke(self, "putNoEncryptionEnabledProtocols", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#create MediaStreamingPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#delete MediaStreamingPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#read MediaStreamingPolicy#read}.
        '''
        value = MediaStreamingPolicyTimeouts(create=create, delete=delete, read=read)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCommonEncryptionCbcs")
    def reset_common_encryption_cbcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonEncryptionCbcs", []))

    @jsii.member(jsii_name="resetCommonEncryptionCenc")
    def reset_common_encryption_cenc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonEncryptionCenc", []))

    @jsii.member(jsii_name="resetDefaultContentKeyPolicyName")
    def reset_default_content_key_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultContentKeyPolicyName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNoEncryptionEnabledProtocols")
    def reset_no_encryption_enabled_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoEncryptionEnabledProtocols", []))

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
    @jsii.member(jsii_name="commonEncryptionCbcs")
    def common_encryption_cbcs(
        self,
    ) -> "MediaStreamingPolicyCommonEncryptionCbcsOutputReference":
        return typing.cast("MediaStreamingPolicyCommonEncryptionCbcsOutputReference", jsii.get(self, "commonEncryptionCbcs"))

    @builtins.property
    @jsii.member(jsii_name="commonEncryptionCenc")
    def common_encryption_cenc(
        self,
    ) -> "MediaStreamingPolicyCommonEncryptionCencOutputReference":
        return typing.cast("MediaStreamingPolicyCommonEncryptionCencOutputReference", jsii.get(self, "commonEncryptionCenc"))

    @builtins.property
    @jsii.member(jsii_name="noEncryptionEnabledProtocols")
    def no_encryption_enabled_protocols(
        self,
    ) -> "MediaStreamingPolicyNoEncryptionEnabledProtocolsOutputReference":
        return typing.cast("MediaStreamingPolicyNoEncryptionEnabledProtocolsOutputReference", jsii.get(self, "noEncryptionEnabledProtocols"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MediaStreamingPolicyTimeoutsOutputReference":
        return typing.cast("MediaStreamingPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="commonEncryptionCbcsInput")
    def common_encryption_cbcs_input(
        self,
    ) -> typing.Optional["MediaStreamingPolicyCommonEncryptionCbcs"]:
        return typing.cast(typing.Optional["MediaStreamingPolicyCommonEncryptionCbcs"], jsii.get(self, "commonEncryptionCbcsInput"))

    @builtins.property
    @jsii.member(jsii_name="commonEncryptionCencInput")
    def common_encryption_cenc_input(
        self,
    ) -> typing.Optional["MediaStreamingPolicyCommonEncryptionCenc"]:
        return typing.cast(typing.Optional["MediaStreamingPolicyCommonEncryptionCenc"], jsii.get(self, "commonEncryptionCencInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultContentKeyPolicyNameInput")
    def default_content_key_policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultContentKeyPolicyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mediaServicesAccountNameInput")
    def media_services_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mediaServicesAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="noEncryptionEnabledProtocolsInput")
    def no_encryption_enabled_protocols_input(
        self,
    ) -> typing.Optional["MediaStreamingPolicyNoEncryptionEnabledProtocols"]:
        return typing.cast(typing.Optional["MediaStreamingPolicyNoEncryptionEnabledProtocols"], jsii.get(self, "noEncryptionEnabledProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MediaStreamingPolicyTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MediaStreamingPolicyTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultContentKeyPolicyName")
    def default_content_key_policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultContentKeyPolicyName"))

    @default_content_key_policy_name.setter
    def default_content_key_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__badf15e349fea53ef2d71af9be9e08e1d57078eba7ad82a37537c9ad9e35e289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultContentKeyPolicyName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff0b82166f2e3cc5b8a19afc3ad1c2953313cd570160adc319cc9f2938e42cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="mediaServicesAccountName")
    def media_services_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mediaServicesAccountName"))

    @media_services_account_name.setter
    def media_services_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef24ac8e44129183e202d3955033b3db5d2e961074bccd7c531c7b4de79f4ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mediaServicesAccountName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1817cf563292950dd7674c6e5943446c3ae92dabcada03aa91a431160cb1913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2343a6be28faf7afc420b5544b2d2a12504c3003edac9bd7d75e2d1e31b3b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCbcs",
    jsii_struct_bases=[],
    name_mapping={
        "default_content_key": "defaultContentKey",
        "drm_fairplay": "drmFairplay",
        "enabled_protocols": "enabledProtocols",
    },
)
class MediaStreamingPolicyCommonEncryptionCbcs:
    def __init__(
        self,
        *,
        default_content_key: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey", typing.Dict[builtins.str, typing.Any]]] = None,
        drm_fairplay: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled_protocols: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_content_key: default_content_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#default_content_key MediaStreamingPolicy#default_content_key}
        :param drm_fairplay: drm_fairplay block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#drm_fairplay MediaStreamingPolicy#drm_fairplay}
        :param enabled_protocols: enabled_protocols block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#enabled_protocols MediaStreamingPolicy#enabled_protocols}
        '''
        if isinstance(default_content_key, dict):
            default_content_key = MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey(**default_content_key)
        if isinstance(drm_fairplay, dict):
            drm_fairplay = MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay(**drm_fairplay)
        if isinstance(enabled_protocols, dict):
            enabled_protocols = MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols(**enabled_protocols)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f2f0b8c5454c08c0821875d5ee9a811693b5af751cf21119b10a0a410a401e)
            check_type(argname="argument default_content_key", value=default_content_key, expected_type=type_hints["default_content_key"])
            check_type(argname="argument drm_fairplay", value=drm_fairplay, expected_type=type_hints["drm_fairplay"])
            check_type(argname="argument enabled_protocols", value=enabled_protocols, expected_type=type_hints["enabled_protocols"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_content_key is not None:
            self._values["default_content_key"] = default_content_key
        if drm_fairplay is not None:
            self._values["drm_fairplay"] = drm_fairplay
        if enabled_protocols is not None:
            self._values["enabled_protocols"] = enabled_protocols

    @builtins.property
    def default_content_key(
        self,
    ) -> typing.Optional["MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey"]:
        '''default_content_key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#default_content_key MediaStreamingPolicy#default_content_key}
        '''
        result = self._values.get("default_content_key")
        return typing.cast(typing.Optional["MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey"], result)

    @builtins.property
    def drm_fairplay(
        self,
    ) -> typing.Optional["MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay"]:
        '''drm_fairplay block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#drm_fairplay MediaStreamingPolicy#drm_fairplay}
        '''
        result = self._values.get("drm_fairplay")
        return typing.cast(typing.Optional["MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay"], result)

    @builtins.property
    def enabled_protocols(
        self,
    ) -> typing.Optional["MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols"]:
        '''enabled_protocols block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#enabled_protocols MediaStreamingPolicy#enabled_protocols}
        '''
        result = self._values.get("enabled_protocols")
        return typing.cast(typing.Optional["MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingPolicyCommonEncryptionCbcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "policy_name": "policyName"},
)
class MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey:
    def __init__(
        self,
        *,
        label: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param label: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#label MediaStreamingPolicy#label}.
        :param policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#policy_name MediaStreamingPolicy#policy_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede7ee0570a9ddbb9ba5a5caef594fa2f4159fb46e0a51f5d0b9e09adc2370db)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if label is not None:
            self._values["label"] = label
        if policy_name is not None:
            self._values["policy_name"] = policy_name

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#label MediaStreamingPolicy#label}.'''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#policy_name MediaStreamingPolicy#policy_name}.'''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5b5e607ad30a9be53e0b83067853e5b2f214f011af2f66e2b09b662dde3290e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @jsii.member(jsii_name="resetPolicyName")
    def reset_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyName", []))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="policyNameInput")
    def policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5229cfd5cd24821db6983663746c27a69d3f094ed8ede51ced1b86c50cda2bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1036a6fad843a59ada93c3d43b1a3e21c891d7e362e29a33f9e6e8919d45521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ca0fdc5283ee78c87188f8ed20d4dbe611d81dcfda261877001c3f673ecb6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay",
    jsii_struct_bases=[],
    name_mapping={
        "allow_persistent_license": "allowPersistentLicense",
        "custom_license_acquisition_url_template": "customLicenseAcquisitionUrlTemplate",
    },
)
class MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay:
    def __init__(
        self,
        *,
        allow_persistent_license: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_license_acquisition_url_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_persistent_license: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#allow_persistent_license MediaStreamingPolicy#allow_persistent_license}.
        :param custom_license_acquisition_url_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#custom_license_acquisition_url_template MediaStreamingPolicy#custom_license_acquisition_url_template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7174b584ea9a9539ddac7668b51f26c8039cc313b13b9be2302fd9f6bf6efe70)
            check_type(argname="argument allow_persistent_license", value=allow_persistent_license, expected_type=type_hints["allow_persistent_license"])
            check_type(argname="argument custom_license_acquisition_url_template", value=custom_license_acquisition_url_template, expected_type=type_hints["custom_license_acquisition_url_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_persistent_license is not None:
            self._values["allow_persistent_license"] = allow_persistent_license
        if custom_license_acquisition_url_template is not None:
            self._values["custom_license_acquisition_url_template"] = custom_license_acquisition_url_template

    @builtins.property
    def allow_persistent_license(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#allow_persistent_license MediaStreamingPolicy#allow_persistent_license}.'''
        result = self._values.get("allow_persistent_license")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom_license_acquisition_url_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#custom_license_acquisition_url_template MediaStreamingPolicy#custom_license_acquisition_url_template}.'''
        result = self._values.get("custom_license_acquisition_url_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingPolicyCommonEncryptionCbcsDrmFairplayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCbcsDrmFairplayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c4bdcfacaea39711c881a5a7b1df0a28f2c923be9926d2c357e26f4e09cd7c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowPersistentLicense")
    def reset_allow_persistent_license(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowPersistentLicense", []))

    @jsii.member(jsii_name="resetCustomLicenseAcquisitionUrlTemplate")
    def reset_custom_license_acquisition_url_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomLicenseAcquisitionUrlTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="allowPersistentLicenseInput")
    def allow_persistent_license_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowPersistentLicenseInput"))

    @builtins.property
    @jsii.member(jsii_name="customLicenseAcquisitionUrlTemplateInput")
    def custom_license_acquisition_url_template_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customLicenseAcquisitionUrlTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="allowPersistentLicense")
    def allow_persistent_license(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowPersistentLicense"))

    @allow_persistent_license.setter
    def allow_persistent_license(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b8d44f09612e02d6504bca4a6d5c4bac69b728992ca8012c1cdbe31f11dab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowPersistentLicense", value)

    @builtins.property
    @jsii.member(jsii_name="customLicenseAcquisitionUrlTemplate")
    def custom_license_acquisition_url_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customLicenseAcquisitionUrlTemplate"))

    @custom_license_acquisition_url_template.setter
    def custom_license_acquisition_url_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b0640991de63328e9e26599b124c108242e36cc0af810c79669cac1201d5fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customLicenseAcquisitionUrlTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39d4bc20f79fb2b9feac05ea89512168f7722552b1094672ed6681638844a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols",
    jsii_struct_bases=[],
    name_mapping={
        "dash": "dash",
        "download": "download",
        "hls": "hls",
        "smooth_streaming": "smoothStreaming",
    },
)
class MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols:
    def __init__(
        self,
        *,
        dash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dash: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#dash MediaStreamingPolicy#dash}.
        :param download: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#download MediaStreamingPolicy#download}.
        :param hls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#hls MediaStreamingPolicy#hls}.
        :param smooth_streaming: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#smooth_streaming MediaStreamingPolicy#smooth_streaming}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bfb76a64ab70b7fa8dbb552b01c261074be771e95eb8b70f0c350d035d993f1)
            check_type(argname="argument dash", value=dash, expected_type=type_hints["dash"])
            check_type(argname="argument download", value=download, expected_type=type_hints["download"])
            check_type(argname="argument hls", value=hls, expected_type=type_hints["hls"])
            check_type(argname="argument smooth_streaming", value=smooth_streaming, expected_type=type_hints["smooth_streaming"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dash is not None:
            self._values["dash"] = dash
        if download is not None:
            self._values["download"] = download
        if hls is not None:
            self._values["hls"] = hls
        if smooth_streaming is not None:
            self._values["smooth_streaming"] = smooth_streaming

    @builtins.property
    def dash(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#dash MediaStreamingPolicy#dash}.'''
        result = self._values.get("dash")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def download(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#download MediaStreamingPolicy#download}.'''
        result = self._values.get("download")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#hls MediaStreamingPolicy#hls}.'''
        result = self._values.get("hls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def smooth_streaming(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#smooth_streaming MediaStreamingPolicy#smooth_streaming}.'''
        result = self._values.get("smooth_streaming")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36a7dba195f8b13866dccb21db829241f95a19d59c337faa123ead142d4bc3cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDash")
    def reset_dash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDash", []))

    @jsii.member(jsii_name="resetDownload")
    def reset_download(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDownload", []))

    @jsii.member(jsii_name="resetHls")
    def reset_hls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHls", []))

    @jsii.member(jsii_name="resetSmoothStreaming")
    def reset_smooth_streaming(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmoothStreaming", []))

    @builtins.property
    @jsii.member(jsii_name="dashInput")
    def dash_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dashInput"))

    @builtins.property
    @jsii.member(jsii_name="downloadInput")
    def download_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "downloadInput"))

    @builtins.property
    @jsii.member(jsii_name="hlsInput")
    def hls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hlsInput"))

    @builtins.property
    @jsii.member(jsii_name="smoothStreamingInput")
    def smooth_streaming_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "smoothStreamingInput"))

    @builtins.property
    @jsii.member(jsii_name="dash")
    def dash(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dash"))

    @dash.setter
    def dash(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16dc9c4d20b9742b29840125966dc4d14be4c069d4dd25bfafea21f1bf7351f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dash", value)

    @builtins.property
    @jsii.member(jsii_name="download")
    def download(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "download"))

    @download.setter
    def download(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e2afb95a5e576459b1bdb5d4458fa6cbc29abe27c58158f7a3108d18c2148a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "download", value)

    @builtins.property
    @jsii.member(jsii_name="hls")
    def hls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hls"))

    @hls.setter
    def hls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b1518de1a2d5493cb51432ea461754bb7fab40bd017b85dfbe6ca8793a2202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hls", value)

    @builtins.property
    @jsii.member(jsii_name="smoothStreaming")
    def smooth_streaming(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "smoothStreaming"))

    @smooth_streaming.setter
    def smooth_streaming(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb87cbdc0363e774765dc7994a0dcafa629f1477bbf6d82e502b0e84de53c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smoothStreaming", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e516a5b4e7e65edd93a26dc50caf0c01de1f5862601b15452ff5be4adae5610f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaStreamingPolicyCommonEncryptionCbcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCbcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d1f1b13db911520be88377e7a65308d43898860c66ba03d141aa2c83c663337)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDefaultContentKey")
    def put_default_content_key(
        self,
        *,
        label: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param label: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#label MediaStreamingPolicy#label}.
        :param policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#policy_name MediaStreamingPolicy#policy_name}.
        '''
        value = MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey(
            label=label, policy_name=policy_name
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultContentKey", [value]))

    @jsii.member(jsii_name="putDrmFairplay")
    def put_drm_fairplay(
        self,
        *,
        allow_persistent_license: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_license_acquisition_url_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_persistent_license: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#allow_persistent_license MediaStreamingPolicy#allow_persistent_license}.
        :param custom_license_acquisition_url_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#custom_license_acquisition_url_template MediaStreamingPolicy#custom_license_acquisition_url_template}.
        '''
        value = MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay(
            allow_persistent_license=allow_persistent_license,
            custom_license_acquisition_url_template=custom_license_acquisition_url_template,
        )

        return typing.cast(None, jsii.invoke(self, "putDrmFairplay", [value]))

    @jsii.member(jsii_name="putEnabledProtocols")
    def put_enabled_protocols(
        self,
        *,
        dash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dash: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#dash MediaStreamingPolicy#dash}.
        :param download: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#download MediaStreamingPolicy#download}.
        :param hls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#hls MediaStreamingPolicy#hls}.
        :param smooth_streaming: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#smooth_streaming MediaStreamingPolicy#smooth_streaming}.
        '''
        value = MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols(
            dash=dash, download=download, hls=hls, smooth_streaming=smooth_streaming
        )

        return typing.cast(None, jsii.invoke(self, "putEnabledProtocols", [value]))

    @jsii.member(jsii_name="resetDefaultContentKey")
    def reset_default_content_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultContentKey", []))

    @jsii.member(jsii_name="resetDrmFairplay")
    def reset_drm_fairplay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrmFairplay", []))

    @jsii.member(jsii_name="resetEnabledProtocols")
    def reset_enabled_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabledProtocols", []))

    @builtins.property
    @jsii.member(jsii_name="defaultContentKey")
    def default_content_key(
        self,
    ) -> MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKeyOutputReference:
        return typing.cast(MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKeyOutputReference, jsii.get(self, "defaultContentKey"))

    @builtins.property
    @jsii.member(jsii_name="drmFairplay")
    def drm_fairplay(
        self,
    ) -> MediaStreamingPolicyCommonEncryptionCbcsDrmFairplayOutputReference:
        return typing.cast(MediaStreamingPolicyCommonEncryptionCbcsDrmFairplayOutputReference, jsii.get(self, "drmFairplay"))

    @builtins.property
    @jsii.member(jsii_name="enabledProtocols")
    def enabled_protocols(
        self,
    ) -> MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocolsOutputReference:
        return typing.cast(MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocolsOutputReference, jsii.get(self, "enabledProtocols"))

    @builtins.property
    @jsii.member(jsii_name="defaultContentKeyInput")
    def default_content_key_input(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey], jsii.get(self, "defaultContentKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="drmFairplayInput")
    def drm_fairplay_input(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay], jsii.get(self, "drmFairplayInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledProtocolsInput")
    def enabled_protocols_input(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols], jsii.get(self, "enabledProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCbcs]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCbcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaStreamingPolicyCommonEncryptionCbcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc579000a5aa76493f51ea936530d93c896241a795afb830eaebf1658e2cab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCenc",
    jsii_struct_bases=[],
    name_mapping={
        "default_content_key": "defaultContentKey",
        "drm_playready": "drmPlayready",
        "drm_widevine_custom_license_acquisition_url_template": "drmWidevineCustomLicenseAcquisitionUrlTemplate",
        "enabled_protocols": "enabledProtocols",
    },
)
class MediaStreamingPolicyCommonEncryptionCenc:
    def __init__(
        self,
        *,
        default_content_key: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCencDefaultContentKey", typing.Dict[builtins.str, typing.Any]]] = None,
        drm_playready: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCencDrmPlayready", typing.Dict[builtins.str, typing.Any]]] = None,
        drm_widevine_custom_license_acquisition_url_template: typing.Optional[builtins.str] = None,
        enabled_protocols: typing.Optional[typing.Union["MediaStreamingPolicyCommonEncryptionCencEnabledProtocols", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_content_key: default_content_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#default_content_key MediaStreamingPolicy#default_content_key}
        :param drm_playready: drm_playready block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#drm_playready MediaStreamingPolicy#drm_playready}
        :param drm_widevine_custom_license_acquisition_url_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#drm_widevine_custom_license_acquisition_url_template MediaStreamingPolicy#drm_widevine_custom_license_acquisition_url_template}.
        :param enabled_protocols: enabled_protocols block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#enabled_protocols MediaStreamingPolicy#enabled_protocols}
        '''
        if isinstance(default_content_key, dict):
            default_content_key = MediaStreamingPolicyCommonEncryptionCencDefaultContentKey(**default_content_key)
        if isinstance(drm_playready, dict):
            drm_playready = MediaStreamingPolicyCommonEncryptionCencDrmPlayready(**drm_playready)
        if isinstance(enabled_protocols, dict):
            enabled_protocols = MediaStreamingPolicyCommonEncryptionCencEnabledProtocols(**enabled_protocols)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df29267f26859d504dd3a49915c66d747218279c77bb061c01f0e4915caeb732)
            check_type(argname="argument default_content_key", value=default_content_key, expected_type=type_hints["default_content_key"])
            check_type(argname="argument drm_playready", value=drm_playready, expected_type=type_hints["drm_playready"])
            check_type(argname="argument drm_widevine_custom_license_acquisition_url_template", value=drm_widevine_custom_license_acquisition_url_template, expected_type=type_hints["drm_widevine_custom_license_acquisition_url_template"])
            check_type(argname="argument enabled_protocols", value=enabled_protocols, expected_type=type_hints["enabled_protocols"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_content_key is not None:
            self._values["default_content_key"] = default_content_key
        if drm_playready is not None:
            self._values["drm_playready"] = drm_playready
        if drm_widevine_custom_license_acquisition_url_template is not None:
            self._values["drm_widevine_custom_license_acquisition_url_template"] = drm_widevine_custom_license_acquisition_url_template
        if enabled_protocols is not None:
            self._values["enabled_protocols"] = enabled_protocols

    @builtins.property
    def default_content_key(
        self,
    ) -> typing.Optional["MediaStreamingPolicyCommonEncryptionCencDefaultContentKey"]:
        '''default_content_key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#default_content_key MediaStreamingPolicy#default_content_key}
        '''
        result = self._values.get("default_content_key")
        return typing.cast(typing.Optional["MediaStreamingPolicyCommonEncryptionCencDefaultContentKey"], result)

    @builtins.property
    def drm_playready(
        self,
    ) -> typing.Optional["MediaStreamingPolicyCommonEncryptionCencDrmPlayready"]:
        '''drm_playready block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#drm_playready MediaStreamingPolicy#drm_playready}
        '''
        result = self._values.get("drm_playready")
        return typing.cast(typing.Optional["MediaStreamingPolicyCommonEncryptionCencDrmPlayready"], result)

    @builtins.property
    def drm_widevine_custom_license_acquisition_url_template(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#drm_widevine_custom_license_acquisition_url_template MediaStreamingPolicy#drm_widevine_custom_license_acquisition_url_template}.'''
        result = self._values.get("drm_widevine_custom_license_acquisition_url_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled_protocols(
        self,
    ) -> typing.Optional["MediaStreamingPolicyCommonEncryptionCencEnabledProtocols"]:
        '''enabled_protocols block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#enabled_protocols MediaStreamingPolicy#enabled_protocols}
        '''
        result = self._values.get("enabled_protocols")
        return typing.cast(typing.Optional["MediaStreamingPolicyCommonEncryptionCencEnabledProtocols"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingPolicyCommonEncryptionCenc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCencDefaultContentKey",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "policy_name": "policyName"},
)
class MediaStreamingPolicyCommonEncryptionCencDefaultContentKey:
    def __init__(
        self,
        *,
        label: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param label: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#label MediaStreamingPolicy#label}.
        :param policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#policy_name MediaStreamingPolicy#policy_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3853958f59dba38974fce1224f059072240ec78ad75374837e8ce7214d36797e)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if label is not None:
            self._values["label"] = label
        if policy_name is not None:
            self._values["policy_name"] = policy_name

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#label MediaStreamingPolicy#label}.'''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#policy_name MediaStreamingPolicy#policy_name}.'''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingPolicyCommonEncryptionCencDefaultContentKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingPolicyCommonEncryptionCencDefaultContentKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCencDefaultContentKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4efef38efa531147056a619b8885d276abebcce8dd666191fccf7e40960e33e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @jsii.member(jsii_name="resetPolicyName")
    def reset_policy_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyName", []))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="policyNameInput")
    def policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d533a5812e4d27fd6f3c75f7731990e44edd7d77a43377d7e5899f4eb61da6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ba5a8438ae3f2140e0007cc666be8fb5aebaa88dc08125fa5218463c1b1ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCencDefaultContentKey]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCencDefaultContentKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaStreamingPolicyCommonEncryptionCencDefaultContentKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693978bf058aae51a1211ff26551943b154c86bd260ef228b7d301c15a5a309b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCencDrmPlayready",
    jsii_struct_bases=[],
    name_mapping={
        "custom_attributes": "customAttributes",
        "custom_license_acquisition_url_template": "customLicenseAcquisitionUrlTemplate",
    },
)
class MediaStreamingPolicyCommonEncryptionCencDrmPlayready:
    def __init__(
        self,
        *,
        custom_attributes: typing.Optional[builtins.str] = None,
        custom_license_acquisition_url_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_attributes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#custom_attributes MediaStreamingPolicy#custom_attributes}.
        :param custom_license_acquisition_url_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#custom_license_acquisition_url_template MediaStreamingPolicy#custom_license_acquisition_url_template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd053b9c0cf786dd29ec64c2403e20da7a062060fb4d28235b6e45d5fd5cd4a)
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument custom_license_acquisition_url_template", value=custom_license_acquisition_url_template, expected_type=type_hints["custom_license_acquisition_url_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if custom_license_acquisition_url_template is not None:
            self._values["custom_license_acquisition_url_template"] = custom_license_acquisition_url_template

    @builtins.property
    def custom_attributes(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#custom_attributes MediaStreamingPolicy#custom_attributes}.'''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_license_acquisition_url_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#custom_license_acquisition_url_template MediaStreamingPolicy#custom_license_acquisition_url_template}.'''
        result = self._values.get("custom_license_acquisition_url_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingPolicyCommonEncryptionCencDrmPlayready(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingPolicyCommonEncryptionCencDrmPlayreadyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCencDrmPlayreadyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c730cac1e5d5ba96f3eac29fd7db2bad91c727880f0f108ea16e4c0b24c17c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomAttributes")
    def reset_custom_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomAttributes", []))

    @jsii.member(jsii_name="resetCustomLicenseAcquisitionUrlTemplate")
    def reset_custom_license_acquisition_url_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomLicenseAcquisitionUrlTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="customAttributesInput")
    def custom_attributes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="customLicenseAcquisitionUrlTemplateInput")
    def custom_license_acquisition_url_template_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customLicenseAcquisitionUrlTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="customAttributes")
    def custom_attributes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customAttributes"))

    @custom_attributes.setter
    def custom_attributes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f81b22ae3d4b4eeee8f29302a5f199102babbfeeac878b18b26c28cec92286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="customLicenseAcquisitionUrlTemplate")
    def custom_license_acquisition_url_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customLicenseAcquisitionUrlTemplate"))

    @custom_license_acquisition_url_template.setter
    def custom_license_acquisition_url_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda5a43db3e9deff6dcbc04dcee89e003f8add169fdbb9c769a8aa04421eca48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customLicenseAcquisitionUrlTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCencDrmPlayready]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCencDrmPlayready], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaStreamingPolicyCommonEncryptionCencDrmPlayready],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90d6e7b999d3c281d3e00e14481fca2b6e928f04d6bd16c1c014c127626c513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCencEnabledProtocols",
    jsii_struct_bases=[],
    name_mapping={
        "dash": "dash",
        "download": "download",
        "hls": "hls",
        "smooth_streaming": "smoothStreaming",
    },
)
class MediaStreamingPolicyCommonEncryptionCencEnabledProtocols:
    def __init__(
        self,
        *,
        dash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dash: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#dash MediaStreamingPolicy#dash}.
        :param download: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#download MediaStreamingPolicy#download}.
        :param hls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#hls MediaStreamingPolicy#hls}.
        :param smooth_streaming: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#smooth_streaming MediaStreamingPolicy#smooth_streaming}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09af986d6ac2499aedb220d3b8daec7897d9e7ae8ffc812249f1f96149a306d)
            check_type(argname="argument dash", value=dash, expected_type=type_hints["dash"])
            check_type(argname="argument download", value=download, expected_type=type_hints["download"])
            check_type(argname="argument hls", value=hls, expected_type=type_hints["hls"])
            check_type(argname="argument smooth_streaming", value=smooth_streaming, expected_type=type_hints["smooth_streaming"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dash is not None:
            self._values["dash"] = dash
        if download is not None:
            self._values["download"] = download
        if hls is not None:
            self._values["hls"] = hls
        if smooth_streaming is not None:
            self._values["smooth_streaming"] = smooth_streaming

    @builtins.property
    def dash(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#dash MediaStreamingPolicy#dash}.'''
        result = self._values.get("dash")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def download(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#download MediaStreamingPolicy#download}.'''
        result = self._values.get("download")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#hls MediaStreamingPolicy#hls}.'''
        result = self._values.get("hls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def smooth_streaming(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#smooth_streaming MediaStreamingPolicy#smooth_streaming}.'''
        result = self._values.get("smooth_streaming")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingPolicyCommonEncryptionCencEnabledProtocols(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingPolicyCommonEncryptionCencEnabledProtocolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCencEnabledProtocolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e0ffff93f4a33e9bdf699c4b0da83a58e1e35fb6ca5faa120132bccb9e98ced)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDash")
    def reset_dash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDash", []))

    @jsii.member(jsii_name="resetDownload")
    def reset_download(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDownload", []))

    @jsii.member(jsii_name="resetHls")
    def reset_hls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHls", []))

    @jsii.member(jsii_name="resetSmoothStreaming")
    def reset_smooth_streaming(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmoothStreaming", []))

    @builtins.property
    @jsii.member(jsii_name="dashInput")
    def dash_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dashInput"))

    @builtins.property
    @jsii.member(jsii_name="downloadInput")
    def download_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "downloadInput"))

    @builtins.property
    @jsii.member(jsii_name="hlsInput")
    def hls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hlsInput"))

    @builtins.property
    @jsii.member(jsii_name="smoothStreamingInput")
    def smooth_streaming_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "smoothStreamingInput"))

    @builtins.property
    @jsii.member(jsii_name="dash")
    def dash(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dash"))

    @dash.setter
    def dash(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937729370b28437bf6c69443173c9ead21f327b646bd7839bceca2949437c6eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dash", value)

    @builtins.property
    @jsii.member(jsii_name="download")
    def download(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "download"))

    @download.setter
    def download(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6123f542cb33a5bf58c46e8a6c9ed0fed427cc00350781cc3c0ef057c610f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "download", value)

    @builtins.property
    @jsii.member(jsii_name="hls")
    def hls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hls"))

    @hls.setter
    def hls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e404ef10d056b6a8c117ab9b2374a04c35276ec8bd08591c48c4b99e0bee2837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hls", value)

    @builtins.property
    @jsii.member(jsii_name="smoothStreaming")
    def smooth_streaming(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "smoothStreaming"))

    @smooth_streaming.setter
    def smooth_streaming(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9074ac3b8289533f75eeeeecc5352c1779cfd13019a3ca5c883f1bf7331ed5a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smoothStreaming", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCencEnabledProtocols]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCencEnabledProtocols], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaStreamingPolicyCommonEncryptionCencEnabledProtocols],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86eee1014fd79ccecd826e4bab205431539bed119d4b6fbc66eb8e9eae416d68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaStreamingPolicyCommonEncryptionCencOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyCommonEncryptionCencOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d23bb54baa8204ad7a37438c701807627e2d5ebaac190251b4fb75acb577a2c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDefaultContentKey")
    def put_default_content_key(
        self,
        *,
        label: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param label: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#label MediaStreamingPolicy#label}.
        :param policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#policy_name MediaStreamingPolicy#policy_name}.
        '''
        value = MediaStreamingPolicyCommonEncryptionCencDefaultContentKey(
            label=label, policy_name=policy_name
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultContentKey", [value]))

    @jsii.member(jsii_name="putDrmPlayready")
    def put_drm_playready(
        self,
        *,
        custom_attributes: typing.Optional[builtins.str] = None,
        custom_license_acquisition_url_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_attributes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#custom_attributes MediaStreamingPolicy#custom_attributes}.
        :param custom_license_acquisition_url_template: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#custom_license_acquisition_url_template MediaStreamingPolicy#custom_license_acquisition_url_template}.
        '''
        value = MediaStreamingPolicyCommonEncryptionCencDrmPlayready(
            custom_attributes=custom_attributes,
            custom_license_acquisition_url_template=custom_license_acquisition_url_template,
        )

        return typing.cast(None, jsii.invoke(self, "putDrmPlayready", [value]))

    @jsii.member(jsii_name="putEnabledProtocols")
    def put_enabled_protocols(
        self,
        *,
        dash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dash: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#dash MediaStreamingPolicy#dash}.
        :param download: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#download MediaStreamingPolicy#download}.
        :param hls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#hls MediaStreamingPolicy#hls}.
        :param smooth_streaming: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#smooth_streaming MediaStreamingPolicy#smooth_streaming}.
        '''
        value = MediaStreamingPolicyCommonEncryptionCencEnabledProtocols(
            dash=dash, download=download, hls=hls, smooth_streaming=smooth_streaming
        )

        return typing.cast(None, jsii.invoke(self, "putEnabledProtocols", [value]))

    @jsii.member(jsii_name="resetDefaultContentKey")
    def reset_default_content_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultContentKey", []))

    @jsii.member(jsii_name="resetDrmPlayready")
    def reset_drm_playready(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrmPlayready", []))

    @jsii.member(jsii_name="resetDrmWidevineCustomLicenseAcquisitionUrlTemplate")
    def reset_drm_widevine_custom_license_acquisition_url_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrmWidevineCustomLicenseAcquisitionUrlTemplate", []))

    @jsii.member(jsii_name="resetEnabledProtocols")
    def reset_enabled_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabledProtocols", []))

    @builtins.property
    @jsii.member(jsii_name="defaultContentKey")
    def default_content_key(
        self,
    ) -> MediaStreamingPolicyCommonEncryptionCencDefaultContentKeyOutputReference:
        return typing.cast(MediaStreamingPolicyCommonEncryptionCencDefaultContentKeyOutputReference, jsii.get(self, "defaultContentKey"))

    @builtins.property
    @jsii.member(jsii_name="drmPlayready")
    def drm_playready(
        self,
    ) -> MediaStreamingPolicyCommonEncryptionCencDrmPlayreadyOutputReference:
        return typing.cast(MediaStreamingPolicyCommonEncryptionCencDrmPlayreadyOutputReference, jsii.get(self, "drmPlayready"))

    @builtins.property
    @jsii.member(jsii_name="enabledProtocols")
    def enabled_protocols(
        self,
    ) -> MediaStreamingPolicyCommonEncryptionCencEnabledProtocolsOutputReference:
        return typing.cast(MediaStreamingPolicyCommonEncryptionCencEnabledProtocolsOutputReference, jsii.get(self, "enabledProtocols"))

    @builtins.property
    @jsii.member(jsii_name="defaultContentKeyInput")
    def default_content_key_input(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCencDefaultContentKey]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCencDefaultContentKey], jsii.get(self, "defaultContentKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="drmPlayreadyInput")
    def drm_playready_input(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCencDrmPlayready]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCencDrmPlayready], jsii.get(self, "drmPlayreadyInput"))

    @builtins.property
    @jsii.member(jsii_name="drmWidevineCustomLicenseAcquisitionUrlTemplateInput")
    def drm_widevine_custom_license_acquisition_url_template_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "drmWidevineCustomLicenseAcquisitionUrlTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledProtocolsInput")
    def enabled_protocols_input(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCencEnabledProtocols]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCencEnabledProtocols], jsii.get(self, "enabledProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="drmWidevineCustomLicenseAcquisitionUrlTemplate")
    def drm_widevine_custom_license_acquisition_url_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "drmWidevineCustomLicenseAcquisitionUrlTemplate"))

    @drm_widevine_custom_license_acquisition_url_template.setter
    def drm_widevine_custom_license_acquisition_url_template(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2dd59fd2ec10680d56ab27119a4f6c25f59afc9c2384783981261fd51d31a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drmWidevineCustomLicenseAcquisitionUrlTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCenc]:
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCenc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaStreamingPolicyCommonEncryptionCenc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5904c93fe96e8f068d4f5a8832df3f24b189f2d79bc34bb84535ac135860046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "media_services_account_name": "mediaServicesAccountName",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "common_encryption_cbcs": "commonEncryptionCbcs",
        "common_encryption_cenc": "commonEncryptionCenc",
        "default_content_key_policy_name": "defaultContentKeyPolicyName",
        "id": "id",
        "no_encryption_enabled_protocols": "noEncryptionEnabledProtocols",
        "timeouts": "timeouts",
    },
)
class MediaStreamingPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        media_services_account_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        common_encryption_cbcs: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCbcs, typing.Dict[builtins.str, typing.Any]]] = None,
        common_encryption_cenc: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCenc, typing.Dict[builtins.str, typing.Any]]] = None,
        default_content_key_policy_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        no_encryption_enabled_protocols: typing.Optional[typing.Union["MediaStreamingPolicyNoEncryptionEnabledProtocols", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MediaStreamingPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param media_services_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#media_services_account_name MediaStreamingPolicy#media_services_account_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#name MediaStreamingPolicy#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#resource_group_name MediaStreamingPolicy#resource_group_name}.
        :param common_encryption_cbcs: common_encryption_cbcs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#common_encryption_cbcs MediaStreamingPolicy#common_encryption_cbcs}
        :param common_encryption_cenc: common_encryption_cenc block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#common_encryption_cenc MediaStreamingPolicy#common_encryption_cenc}
        :param default_content_key_policy_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#default_content_key_policy_name MediaStreamingPolicy#default_content_key_policy_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#id MediaStreamingPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param no_encryption_enabled_protocols: no_encryption_enabled_protocols block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#no_encryption_enabled_protocols MediaStreamingPolicy#no_encryption_enabled_protocols}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#timeouts MediaStreamingPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(common_encryption_cbcs, dict):
            common_encryption_cbcs = MediaStreamingPolicyCommonEncryptionCbcs(**common_encryption_cbcs)
        if isinstance(common_encryption_cenc, dict):
            common_encryption_cenc = MediaStreamingPolicyCommonEncryptionCenc(**common_encryption_cenc)
        if isinstance(no_encryption_enabled_protocols, dict):
            no_encryption_enabled_protocols = MediaStreamingPolicyNoEncryptionEnabledProtocols(**no_encryption_enabled_protocols)
        if isinstance(timeouts, dict):
            timeouts = MediaStreamingPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4878ea4131a87d6d60113eddadf694d41b21b62e1465ce6346541ff147d60e0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument media_services_account_name", value=media_services_account_name, expected_type=type_hints["media_services_account_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument common_encryption_cbcs", value=common_encryption_cbcs, expected_type=type_hints["common_encryption_cbcs"])
            check_type(argname="argument common_encryption_cenc", value=common_encryption_cenc, expected_type=type_hints["common_encryption_cenc"])
            check_type(argname="argument default_content_key_policy_name", value=default_content_key_policy_name, expected_type=type_hints["default_content_key_policy_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument no_encryption_enabled_protocols", value=no_encryption_enabled_protocols, expected_type=type_hints["no_encryption_enabled_protocols"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if common_encryption_cbcs is not None:
            self._values["common_encryption_cbcs"] = common_encryption_cbcs
        if common_encryption_cenc is not None:
            self._values["common_encryption_cenc"] = common_encryption_cenc
        if default_content_key_policy_name is not None:
            self._values["default_content_key_policy_name"] = default_content_key_policy_name
        if id is not None:
            self._values["id"] = id
        if no_encryption_enabled_protocols is not None:
            self._values["no_encryption_enabled_protocols"] = no_encryption_enabled_protocols
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
    def media_services_account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#media_services_account_name MediaStreamingPolicy#media_services_account_name}.'''
        result = self._values.get("media_services_account_name")
        assert result is not None, "Required property 'media_services_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#name MediaStreamingPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#resource_group_name MediaStreamingPolicy#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def common_encryption_cbcs(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCbcs]:
        '''common_encryption_cbcs block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#common_encryption_cbcs MediaStreamingPolicy#common_encryption_cbcs}
        '''
        result = self._values.get("common_encryption_cbcs")
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCbcs], result)

    @builtins.property
    def common_encryption_cenc(
        self,
    ) -> typing.Optional[MediaStreamingPolicyCommonEncryptionCenc]:
        '''common_encryption_cenc block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#common_encryption_cenc MediaStreamingPolicy#common_encryption_cenc}
        '''
        result = self._values.get("common_encryption_cenc")
        return typing.cast(typing.Optional[MediaStreamingPolicyCommonEncryptionCenc], result)

    @builtins.property
    def default_content_key_policy_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#default_content_key_policy_name MediaStreamingPolicy#default_content_key_policy_name}.'''
        result = self._values.get("default_content_key_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#id MediaStreamingPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_encryption_enabled_protocols(
        self,
    ) -> typing.Optional["MediaStreamingPolicyNoEncryptionEnabledProtocols"]:
        '''no_encryption_enabled_protocols block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#no_encryption_enabled_protocols MediaStreamingPolicy#no_encryption_enabled_protocols}
        '''
        result = self._values.get("no_encryption_enabled_protocols")
        return typing.cast(typing.Optional["MediaStreamingPolicyNoEncryptionEnabledProtocols"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MediaStreamingPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#timeouts MediaStreamingPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MediaStreamingPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyNoEncryptionEnabledProtocols",
    jsii_struct_bases=[],
    name_mapping={
        "dash": "dash",
        "download": "download",
        "hls": "hls",
        "smooth_streaming": "smoothStreaming",
    },
)
class MediaStreamingPolicyNoEncryptionEnabledProtocols:
    def __init__(
        self,
        *,
        dash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dash: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#dash MediaStreamingPolicy#dash}.
        :param download: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#download MediaStreamingPolicy#download}.
        :param hls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#hls MediaStreamingPolicy#hls}.
        :param smooth_streaming: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#smooth_streaming MediaStreamingPolicy#smooth_streaming}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f083587dd133afccaa6be026dc81882afcc768870d89a0a2d44f6468b78108dc)
            check_type(argname="argument dash", value=dash, expected_type=type_hints["dash"])
            check_type(argname="argument download", value=download, expected_type=type_hints["download"])
            check_type(argname="argument hls", value=hls, expected_type=type_hints["hls"])
            check_type(argname="argument smooth_streaming", value=smooth_streaming, expected_type=type_hints["smooth_streaming"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dash is not None:
            self._values["dash"] = dash
        if download is not None:
            self._values["download"] = download
        if hls is not None:
            self._values["hls"] = hls
        if smooth_streaming is not None:
            self._values["smooth_streaming"] = smooth_streaming

    @builtins.property
    def dash(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#dash MediaStreamingPolicy#dash}.'''
        result = self._values.get("dash")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def download(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#download MediaStreamingPolicy#download}.'''
        result = self._values.get("download")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#hls MediaStreamingPolicy#hls}.'''
        result = self._values.get("hls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def smooth_streaming(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#smooth_streaming MediaStreamingPolicy#smooth_streaming}.'''
        result = self._values.get("smooth_streaming")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingPolicyNoEncryptionEnabledProtocols(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingPolicyNoEncryptionEnabledProtocolsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyNoEncryptionEnabledProtocolsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73d2665195eba89e489e69054cb7937e793854448cf8607cd5d54174e1b2ba5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDash")
    def reset_dash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDash", []))

    @jsii.member(jsii_name="resetDownload")
    def reset_download(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDownload", []))

    @jsii.member(jsii_name="resetHls")
    def reset_hls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHls", []))

    @jsii.member(jsii_name="resetSmoothStreaming")
    def reset_smooth_streaming(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmoothStreaming", []))

    @builtins.property
    @jsii.member(jsii_name="dashInput")
    def dash_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dashInput"))

    @builtins.property
    @jsii.member(jsii_name="downloadInput")
    def download_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "downloadInput"))

    @builtins.property
    @jsii.member(jsii_name="hlsInput")
    def hls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hlsInput"))

    @builtins.property
    @jsii.member(jsii_name="smoothStreamingInput")
    def smooth_streaming_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "smoothStreamingInput"))

    @builtins.property
    @jsii.member(jsii_name="dash")
    def dash(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dash"))

    @dash.setter
    def dash(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13ed9d75a632d7896c7b641967584095cd66b9224f9b0aff861e3fa32c68ecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dash", value)

    @builtins.property
    @jsii.member(jsii_name="download")
    def download(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "download"))

    @download.setter
    def download(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e818d3b051fbe60a96bee37254798b5fa9278d290f5aabd67ffd5506964f22b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "download", value)

    @builtins.property
    @jsii.member(jsii_name="hls")
    def hls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hls"))

    @hls.setter
    def hls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e555f99f25b511c676e200f8aa90d8f2b4e962d5d02720d73d0242d556050dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hls", value)

    @builtins.property
    @jsii.member(jsii_name="smoothStreaming")
    def smooth_streaming(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "smoothStreaming"))

    @smooth_streaming.setter
    def smooth_streaming(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b452c41d75701c3b696306783c8fe3df95647b45f70b6fb8199a3143262490f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smoothStreaming", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaStreamingPolicyNoEncryptionEnabledProtocols]:
        return typing.cast(typing.Optional[MediaStreamingPolicyNoEncryptionEnabledProtocols], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaStreamingPolicyNoEncryptionEnabledProtocols],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66bb6b94ce85b074c94d4ff456c77755111286089ade97fb874a415867501b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class MediaStreamingPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#create MediaStreamingPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#delete MediaStreamingPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#read MediaStreamingPolicy#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c45c8637f6ce20fd4230f054db64bbefda9a4ad734f3da73d6eb2e3d479693)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#create MediaStreamingPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#delete MediaStreamingPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_policy#read MediaStreamingPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingPolicy.MediaStreamingPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__090e66135f5e1c317dbc9a7660d407266f0432c7e2543ae1aa88a13603b7be58)
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
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ba4c208fe9a7b155221b7399a00011d87510bebe2cfec4be9e905e89b35b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b463a42a5ee4a03592af84e3615f89c7db0db856f8d639ae1df843e36fe3bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e5cd9e067c7404426aff6c241112f88bb869cbaa3be8f4f973678beed920c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaStreamingPolicyTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaStreamingPolicyTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaStreamingPolicyTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__634394e79a20c88a5f866ee2fc9b0a85994cf73ebdc5af85f33fec236ad324fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MediaStreamingPolicy",
    "MediaStreamingPolicyCommonEncryptionCbcs",
    "MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey",
    "MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKeyOutputReference",
    "MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay",
    "MediaStreamingPolicyCommonEncryptionCbcsDrmFairplayOutputReference",
    "MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols",
    "MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocolsOutputReference",
    "MediaStreamingPolicyCommonEncryptionCbcsOutputReference",
    "MediaStreamingPolicyCommonEncryptionCenc",
    "MediaStreamingPolicyCommonEncryptionCencDefaultContentKey",
    "MediaStreamingPolicyCommonEncryptionCencDefaultContentKeyOutputReference",
    "MediaStreamingPolicyCommonEncryptionCencDrmPlayready",
    "MediaStreamingPolicyCommonEncryptionCencDrmPlayreadyOutputReference",
    "MediaStreamingPolicyCommonEncryptionCencEnabledProtocols",
    "MediaStreamingPolicyCommonEncryptionCencEnabledProtocolsOutputReference",
    "MediaStreamingPolicyCommonEncryptionCencOutputReference",
    "MediaStreamingPolicyConfig",
    "MediaStreamingPolicyNoEncryptionEnabledProtocols",
    "MediaStreamingPolicyNoEncryptionEnabledProtocolsOutputReference",
    "MediaStreamingPolicyTimeouts",
    "MediaStreamingPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__16257c9d0eb4ef2573bad9116d8bb571c21ba680834a3edd53f19a45ea21697c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    media_services_account_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    common_encryption_cbcs: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCbcs, typing.Dict[builtins.str, typing.Any]]] = None,
    common_encryption_cenc: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCenc, typing.Dict[builtins.str, typing.Any]]] = None,
    default_content_key_policy_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    no_encryption_enabled_protocols: typing.Optional[typing.Union[MediaStreamingPolicyNoEncryptionEnabledProtocols, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MediaStreamingPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__badf15e349fea53ef2d71af9be9e08e1d57078eba7ad82a37537c9ad9e35e289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff0b82166f2e3cc5b8a19afc3ad1c2953313cd570160adc319cc9f2938e42cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef24ac8e44129183e202d3955033b3db5d2e961074bccd7c531c7b4de79f4ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1817cf563292950dd7674c6e5943446c3ae92dabcada03aa91a431160cb1913(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2343a6be28faf7afc420b5544b2d2a12504c3003edac9bd7d75e2d1e31b3b2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f2f0b8c5454c08c0821875d5ee9a811693b5af751cf21119b10a0a410a401e(
    *,
    default_content_key: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey, typing.Dict[builtins.str, typing.Any]]] = None,
    drm_fairplay: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled_protocols: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede7ee0570a9ddbb9ba5a5caef594fa2f4159fb46e0a51f5d0b9e09adc2370db(
    *,
    label: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b5e607ad30a9be53e0b83067853e5b2f214f011af2f66e2b09b662dde3290e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5229cfd5cd24821db6983663746c27a69d3f094ed8ede51ced1b86c50cda2bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1036a6fad843a59ada93c3d43b1a3e21c891d7e362e29a33f9e6e8919d45521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ca0fdc5283ee78c87188f8ed20d4dbe611d81dcfda261877001c3f673ecb6f(
    value: typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDefaultContentKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7174b584ea9a9539ddac7668b51f26c8039cc313b13b9be2302fd9f6bf6efe70(
    *,
    allow_persistent_license: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_license_acquisition_url_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4bdcfacaea39711c881a5a7b1df0a28f2c923be9926d2c357e26f4e09cd7c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b8d44f09612e02d6504bca4a6d5c4bac69b728992ca8012c1cdbe31f11dab0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b0640991de63328e9e26599b124c108242e36cc0af810c79669cac1201d5fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39d4bc20f79fb2b9feac05ea89512168f7722552b1094672ed6681638844a0c(
    value: typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsDrmFairplay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfb76a64ab70b7fa8dbb552b01c261074be771e95eb8b70f0c350d035d993f1(
    *,
    dash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a7dba195f8b13866dccb21db829241f95a19d59c337faa123ead142d4bc3cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16dc9c4d20b9742b29840125966dc4d14be4c069d4dd25bfafea21f1bf7351f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e2afb95a5e576459b1bdb5d4458fa6cbc29abe27c58158f7a3108d18c2148a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b1518de1a2d5493cb51432ea461754bb7fab40bd017b85dfbe6ca8793a2202(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb87cbdc0363e774765dc7994a0dcafa629f1477bbf6d82e502b0e84de53c7a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e516a5b4e7e65edd93a26dc50caf0c01de1f5862601b15452ff5be4adae5610f(
    value: typing.Optional[MediaStreamingPolicyCommonEncryptionCbcsEnabledProtocols],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1f1b13db911520be88377e7a65308d43898860c66ba03d141aa2c83c663337(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc579000a5aa76493f51ea936530d93c896241a795afb830eaebf1658e2cab3(
    value: typing.Optional[MediaStreamingPolicyCommonEncryptionCbcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df29267f26859d504dd3a49915c66d747218279c77bb061c01f0e4915caeb732(
    *,
    default_content_key: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCencDefaultContentKey, typing.Dict[builtins.str, typing.Any]]] = None,
    drm_playready: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCencDrmPlayready, typing.Dict[builtins.str, typing.Any]]] = None,
    drm_widevine_custom_license_acquisition_url_template: typing.Optional[builtins.str] = None,
    enabled_protocols: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCencEnabledProtocols, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3853958f59dba38974fce1224f059072240ec78ad75374837e8ce7214d36797e(
    *,
    label: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4efef38efa531147056a619b8885d276abebcce8dd666191fccf7e40960e33e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d533a5812e4d27fd6f3c75f7731990e44edd7d77a43377d7e5899f4eb61da6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ba5a8438ae3f2140e0007cc666be8fb5aebaa88dc08125fa5218463c1b1ca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693978bf058aae51a1211ff26551943b154c86bd260ef228b7d301c15a5a309b(
    value: typing.Optional[MediaStreamingPolicyCommonEncryptionCencDefaultContentKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd053b9c0cf786dd29ec64c2403e20da7a062060fb4d28235b6e45d5fd5cd4a(
    *,
    custom_attributes: typing.Optional[builtins.str] = None,
    custom_license_acquisition_url_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c730cac1e5d5ba96f3eac29fd7db2bad91c727880f0f108ea16e4c0b24c17c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f81b22ae3d4b4eeee8f29302a5f199102babbfeeac878b18b26c28cec92286(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda5a43db3e9deff6dcbc04dcee89e003f8add169fdbb9c769a8aa04421eca48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90d6e7b999d3c281d3e00e14481fca2b6e928f04d6bd16c1c014c127626c513(
    value: typing.Optional[MediaStreamingPolicyCommonEncryptionCencDrmPlayready],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09af986d6ac2499aedb220d3b8daec7897d9e7ae8ffc812249f1f96149a306d(
    *,
    dash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0ffff93f4a33e9bdf699c4b0da83a58e1e35fb6ca5faa120132bccb9e98ced(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937729370b28437bf6c69443173c9ead21f327b646bd7839bceca2949437c6eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6123f542cb33a5bf58c46e8a6c9ed0fed427cc00350781cc3c0ef057c610f77(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e404ef10d056b6a8c117ab9b2374a04c35276ec8bd08591c48c4b99e0bee2837(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9074ac3b8289533f75eeeeecc5352c1779cfd13019a3ca5c883f1bf7331ed5a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86eee1014fd79ccecd826e4bab205431539bed119d4b6fbc66eb8e9eae416d68(
    value: typing.Optional[MediaStreamingPolicyCommonEncryptionCencEnabledProtocols],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23bb54baa8204ad7a37438c701807627e2d5ebaac190251b4fb75acb577a2c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2dd59fd2ec10680d56ab27119a4f6c25f59afc9c2384783981261fd51d31a1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5904c93fe96e8f068d4f5a8832df3f24b189f2d79bc34bb84535ac135860046(
    value: typing.Optional[MediaStreamingPolicyCommonEncryptionCenc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4878ea4131a87d6d60113eddadf694d41b21b62e1465ce6346541ff147d60e0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    media_services_account_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    common_encryption_cbcs: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCbcs, typing.Dict[builtins.str, typing.Any]]] = None,
    common_encryption_cenc: typing.Optional[typing.Union[MediaStreamingPolicyCommonEncryptionCenc, typing.Dict[builtins.str, typing.Any]]] = None,
    default_content_key_policy_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    no_encryption_enabled_protocols: typing.Optional[typing.Union[MediaStreamingPolicyNoEncryptionEnabledProtocols, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MediaStreamingPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f083587dd133afccaa6be026dc81882afcc768870d89a0a2d44f6468b78108dc(
    *,
    dash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d2665195eba89e489e69054cb7937e793854448cf8607cd5d54174e1b2ba5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13ed9d75a632d7896c7b641967584095cd66b9224f9b0aff861e3fa32c68ecb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e818d3b051fbe60a96bee37254798b5fa9278d290f5aabd67ffd5506964f22b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e555f99f25b511c676e200f8aa90d8f2b4e962d5d02720d73d0242d556050dc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b452c41d75701c3b696306783c8fe3df95647b45f70b6fb8199a3143262490f4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66bb6b94ce85b074c94d4ff456c77755111286089ade97fb874a415867501b94(
    value: typing.Optional[MediaStreamingPolicyNoEncryptionEnabledProtocols],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c45c8637f6ce20fd4230f054db64bbefda9a4ad734f3da73d6eb2e3d479693(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090e66135f5e1c317dbc9a7660d407266f0432c7e2543ae1aa88a13603b7be58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ba4c208fe9a7b155221b7399a00011d87510bebe2cfec4be9e905e89b35b52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b463a42a5ee4a03592af84e3615f89c7db0db856f8d639ae1df843e36fe3bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e5cd9e067c7404426aff6c241112f88bb869cbaa3be8f4f973678beed920c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634394e79a20c88a5f866ee2fc9b0a85994cf73ebdc5af85f33fec236ad324fc(
    value: typing.Optional[typing.Union[MediaStreamingPolicyTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
