'''
# `azurerm_media_streaming_endpoint`

Refer to the Terraform Registory for docs: [`azurerm_media_streaming_endpoint`](https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint).
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


class MediaStreamingEndpoint(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpoint",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint azurerm_media_streaming_endpoint}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        media_services_account_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        scale_units: jsii.Number,
        access_control: typing.Optional[typing.Union["MediaStreamingEndpointAccessControl", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_start_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cdn_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cdn_profile: typing.Optional[builtins.str] = None,
        cdn_provider: typing.Optional[builtins.str] = None,
        cross_site_access_policy: typing.Optional[typing.Union["MediaStreamingEndpointCrossSiteAccessPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_host_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_cache_age_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MediaStreamingEndpointTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint azurerm_media_streaming_endpoint} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#location MediaStreamingEndpoint#location}.
        :param media_services_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#media_services_account_name MediaStreamingEndpoint#media_services_account_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#name MediaStreamingEndpoint#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#resource_group_name MediaStreamingEndpoint#resource_group_name}.
        :param scale_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#scale_units MediaStreamingEndpoint#scale_units}.
        :param access_control: access_control block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#access_control MediaStreamingEndpoint#access_control}
        :param auto_start_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#auto_start_enabled MediaStreamingEndpoint#auto_start_enabled}.
        :param cdn_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cdn_enabled MediaStreamingEndpoint#cdn_enabled}.
        :param cdn_profile: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cdn_profile MediaStreamingEndpoint#cdn_profile}.
        :param cdn_provider: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cdn_provider MediaStreamingEndpoint#cdn_provider}.
        :param cross_site_access_policy: cross_site_access_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cross_site_access_policy MediaStreamingEndpoint#cross_site_access_policy}
        :param custom_host_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#custom_host_names MediaStreamingEndpoint#custom_host_names}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#description MediaStreamingEndpoint#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#id MediaStreamingEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_cache_age_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#max_cache_age_seconds MediaStreamingEndpoint#max_cache_age_seconds}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#tags MediaStreamingEndpoint#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#timeouts MediaStreamingEndpoint#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5559914ab0448cda0e109183333b079a3a42445c608b1640a2a5296a74e9c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MediaStreamingEndpointConfig(
            location=location,
            media_services_account_name=media_services_account_name,
            name=name,
            resource_group_name=resource_group_name,
            scale_units=scale_units,
            access_control=access_control,
            auto_start_enabled=auto_start_enabled,
            cdn_enabled=cdn_enabled,
            cdn_profile=cdn_profile,
            cdn_provider=cdn_provider,
            cross_site_access_policy=cross_site_access_policy,
            custom_host_names=custom_host_names,
            description=description,
            id=id,
            max_cache_age_seconds=max_cache_age_seconds,
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

    @jsii.member(jsii_name="putAccessControl")
    def put_access_control(
        self,
        *,
        akamai_signature_header_authentication_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_allow: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaStreamingEndpointAccessControlIpAllow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param akamai_signature_header_authentication_key: akamai_signature_header_authentication_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#akamai_signature_header_authentication_key MediaStreamingEndpoint#akamai_signature_header_authentication_key}
        :param ip_allow: ip_allow block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#ip_allow MediaStreamingEndpoint#ip_allow}
        '''
        value = MediaStreamingEndpointAccessControl(
            akamai_signature_header_authentication_key=akamai_signature_header_authentication_key,
            ip_allow=ip_allow,
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControl", [value]))

    @jsii.member(jsii_name="putCrossSiteAccessPolicy")
    def put_cross_site_access_policy(
        self,
        *,
        client_access_policy: typing.Optional[builtins.str] = None,
        cross_domain_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_access_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#client_access_policy MediaStreamingEndpoint#client_access_policy}.
        :param cross_domain_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cross_domain_policy MediaStreamingEndpoint#cross_domain_policy}.
        '''
        value = MediaStreamingEndpointCrossSiteAccessPolicy(
            client_access_policy=client_access_policy,
            cross_domain_policy=cross_domain_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putCrossSiteAccessPolicy", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#create MediaStreamingEndpoint#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#delete MediaStreamingEndpoint#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#read MediaStreamingEndpoint#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#update MediaStreamingEndpoint#update}.
        '''
        value = MediaStreamingEndpointTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessControl")
    def reset_access_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessControl", []))

    @jsii.member(jsii_name="resetAutoStartEnabled")
    def reset_auto_start_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoStartEnabled", []))

    @jsii.member(jsii_name="resetCdnEnabled")
    def reset_cdn_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCdnEnabled", []))

    @jsii.member(jsii_name="resetCdnProfile")
    def reset_cdn_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCdnProfile", []))

    @jsii.member(jsii_name="resetCdnProvider")
    def reset_cdn_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCdnProvider", []))

    @jsii.member(jsii_name="resetCrossSiteAccessPolicy")
    def reset_cross_site_access_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossSiteAccessPolicy", []))

    @jsii.member(jsii_name="resetCustomHostNames")
    def reset_custom_host_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomHostNames", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxCacheAgeSeconds")
    def reset_max_cache_age_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxCacheAgeSeconds", []))

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
    @jsii.member(jsii_name="accessControl")
    def access_control(self) -> "MediaStreamingEndpointAccessControlOutputReference":
        return typing.cast("MediaStreamingEndpointAccessControlOutputReference", jsii.get(self, "accessControl"))

    @builtins.property
    @jsii.member(jsii_name="crossSiteAccessPolicy")
    def cross_site_access_policy(
        self,
    ) -> "MediaStreamingEndpointCrossSiteAccessPolicyOutputReference":
        return typing.cast("MediaStreamingEndpointCrossSiteAccessPolicyOutputReference", jsii.get(self, "crossSiteAccessPolicy"))

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MediaStreamingEndpointTimeoutsOutputReference":
        return typing.cast("MediaStreamingEndpointTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessControlInput")
    def access_control_input(
        self,
    ) -> typing.Optional["MediaStreamingEndpointAccessControl"]:
        return typing.cast(typing.Optional["MediaStreamingEndpointAccessControl"], jsii.get(self, "accessControlInput"))

    @builtins.property
    @jsii.member(jsii_name="autoStartEnabledInput")
    def auto_start_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoStartEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnEnabledInput")
    def cdn_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cdnEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnProfileInput")
    def cdn_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cdnProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnProviderInput")
    def cdn_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cdnProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="crossSiteAccessPolicyInput")
    def cross_site_access_policy_input(
        self,
    ) -> typing.Optional["MediaStreamingEndpointCrossSiteAccessPolicy"]:
        return typing.cast(typing.Optional["MediaStreamingEndpointCrossSiteAccessPolicy"], jsii.get(self, "crossSiteAccessPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="customHostNamesInput")
    def custom_host_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customHostNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxCacheAgeSecondsInput")
    def max_cache_age_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxCacheAgeSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="mediaServicesAccountNameInput")
    def media_services_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mediaServicesAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleUnitsInput")
    def scale_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MediaStreamingEndpointTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MediaStreamingEndpointTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__09be9c428bf29e420db94c79735e63e5c307d84464b682c618f0e72dd87abcce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoStartEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cdnEnabled")
    def cdn_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cdnEnabled"))

    @cdn_enabled.setter
    def cdn_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18fcf6da9ecee5458c63a245104582d101193ce9a7f24aa80a016eb7260e6373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cdnProfile")
    def cdn_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cdnProfile"))

    @cdn_profile.setter
    def cdn_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd40cba644f8abd562842c99a9451b1c6b3b2c0d0db373f2e84ee8b52890349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnProfile", value)

    @builtins.property
    @jsii.member(jsii_name="cdnProvider")
    def cdn_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cdnProvider"))

    @cdn_provider.setter
    def cdn_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2ba85a213c5be9d3541f0b0c0cf147dfb5b49ecf815e98d251cceaa4e1dddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnProvider", value)

    @builtins.property
    @jsii.member(jsii_name="customHostNames")
    def custom_host_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customHostNames"))

    @custom_host_names.setter
    def custom_host_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8d5556d655ea54419751b9f538d342f0457c66f91c64e09ec00d9f966e0788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customHostNames", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c9f9b112226124f0b58d5007ebbccb9581176b553654d222d1c99ae6ea51e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b5f0ce37fd60a702c7f544c6a9c361852b7ee47f94f208823ef945b25ff1b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d313a97ded0fd3f0e962bf3b36fc1842e11ce5238ba8110f751b267188ebaa76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="maxCacheAgeSeconds")
    def max_cache_age_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxCacheAgeSeconds"))

    @max_cache_age_seconds.setter
    def max_cache_age_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a466d63c15d198586635bb8ee7b3f841077cddef9f2691f9e959cc2d9aa757f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxCacheAgeSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="mediaServicesAccountName")
    def media_services_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mediaServicesAccountName"))

    @media_services_account_name.setter
    def media_services_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee59665997a5b41f68d3025ad0b226b1591f3a9d01282d8dc3c7800d19b2acf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mediaServicesAccountName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28b03cfa3f3f268029cc9fea27030b0dee83626d4d444df3295e198c521398a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82258a59609ab5bb217f168f6c56b5618a916f1a717e53cd8a7620b7378cafd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="scaleUnits")
    def scale_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleUnits"))

    @scale_units.setter
    def scale_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037a19a5f40d8965a72922287b9402dfb53bb37a08dd1ecec54e98d0cb37e891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleUnits", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aef087797f1b3327f04f92986b9b1431938700aedf35bfeab90caef37d48d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointAccessControl",
    jsii_struct_bases=[],
    name_mapping={
        "akamai_signature_header_authentication_key": "akamaiSignatureHeaderAuthenticationKey",
        "ip_allow": "ipAllow",
    },
)
class MediaStreamingEndpointAccessControl:
    def __init__(
        self,
        *,
        akamai_signature_header_authentication_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_allow: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MediaStreamingEndpointAccessControlIpAllow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param akamai_signature_header_authentication_key: akamai_signature_header_authentication_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#akamai_signature_header_authentication_key MediaStreamingEndpoint#akamai_signature_header_authentication_key}
        :param ip_allow: ip_allow block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#ip_allow MediaStreamingEndpoint#ip_allow}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f632a027c09a32b32740b93c3e980c9a99ef225cd8b35d019ba25022c3a0f2f2)
            check_type(argname="argument akamai_signature_header_authentication_key", value=akamai_signature_header_authentication_key, expected_type=type_hints["akamai_signature_header_authentication_key"])
            check_type(argname="argument ip_allow", value=ip_allow, expected_type=type_hints["ip_allow"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if akamai_signature_header_authentication_key is not None:
            self._values["akamai_signature_header_authentication_key"] = akamai_signature_header_authentication_key
        if ip_allow is not None:
            self._values["ip_allow"] = ip_allow

    @builtins.property
    def akamai_signature_header_authentication_key(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey"]]]:
        '''akamai_signature_header_authentication_key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#akamai_signature_header_authentication_key MediaStreamingEndpoint#akamai_signature_header_authentication_key}
        '''
        result = self._values.get("akamai_signature_header_authentication_key")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey"]]], result)

    @builtins.property
    def ip_allow(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaStreamingEndpointAccessControlIpAllow"]]]:
        '''ip_allow block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#ip_allow MediaStreamingEndpoint#ip_allow}
        '''
        result = self._values.get("ip_allow")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MediaStreamingEndpointAccessControlIpAllow"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingEndpointAccessControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey",
    jsii_struct_bases=[],
    name_mapping={
        "base64_key": "base64Key",
        "expiration": "expiration",
        "identifier": "identifier",
    },
)
class MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey:
    def __init__(
        self,
        *,
        base64_key: typing.Optional[builtins.str] = None,
        expiration: typing.Optional[builtins.str] = None,
        identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param base64_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#base64_key MediaStreamingEndpoint#base64_key}.
        :param expiration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#expiration MediaStreamingEndpoint#expiration}.
        :param identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#identifier MediaStreamingEndpoint#identifier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7b28388190577765472b51512f72c8f30bbe42b4c1f60cbea91abf1d22156d)
            check_type(argname="argument base64_key", value=base64_key, expected_type=type_hints["base64_key"])
            check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base64_key is not None:
            self._values["base64_key"] = base64_key
        if expiration is not None:
            self._values["expiration"] = expiration
        if identifier is not None:
            self._values["identifier"] = identifier

    @builtins.property
    def base64_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#base64_key MediaStreamingEndpoint#base64_key}.'''
        result = self._values.get("base64_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#expiration MediaStreamingEndpoint#expiration}.'''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#identifier MediaStreamingEndpoint#identifier}.'''
        result = self._values.get("identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec552d3b540e5279ebf30988f7486244d76af0e1db5592fc543183d449fa87c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f4a841f0e1dd0766412aa8f6ab5c30e23f7a5ec3e479ec5e7b8af5becf1e91)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf4ddad9feb969605e309f41bac595e84da4e48346ce5c51208d48efced88ba1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bd94346416cd038239f84c7b1fc084f62c4bdf3db0643d5f8071849ff47e0fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79e7bbaaf75c75fa6473412533f27ba2503fa1b84a0559e196c597de9ffa02b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da2cf95b8dd7af2eea17a566248c3da03fcc6a235ca66e0689475c30ad7c152c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3499900a93b932be9fd7b56576ac38456b2f96e278fe4e9f727e655b5aeed6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBase64Key")
    def reset_base64_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBase64Key", []))

    @jsii.member(jsii_name="resetExpiration")
    def reset_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiration", []))

    @jsii.member(jsii_name="resetIdentifier")
    def reset_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentifier", []))

    @builtins.property
    @jsii.member(jsii_name="base64KeyInput")
    def base64_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "base64KeyInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationInput")
    def expiration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationInput"))

    @builtins.property
    @jsii.member(jsii_name="identifierInput")
    def identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identifierInput"))

    @builtins.property
    @jsii.member(jsii_name="base64Key")
    def base64_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "base64Key"))

    @base64_key.setter
    def base64_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed4fbe6d9dabbf320bb3c1abc83b623997525f310e56f9fe01ea7e7535eebc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "base64Key", value)

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiration"))

    @expiration.setter
    def expiration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501a343e09284046269c16a2518b0994f284012fe26dffce2353f44b46fcc370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiration", value)

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifier"))

    @identifier.setter
    def identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87aa568188b1ee92ba6940145b5d5bb7be1f1bc137d72da719324e94a6253aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identifier", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3686aa0f0bf587ddd0603e2193a5d93355d2d9833d633c8fa82fa5f82f4abbee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointAccessControlIpAllow",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "name": "name",
        "subnet_prefix_length": "subnetPrefixLength",
    },
)
class MediaStreamingEndpointAccessControlIpAllow:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        subnet_prefix_length: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#address MediaStreamingEndpoint#address}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#name MediaStreamingEndpoint#name}.
        :param subnet_prefix_length: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#subnet_prefix_length MediaStreamingEndpoint#subnet_prefix_length}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f4f0971f3996a54003d2021e7d5980040d6e5889dd21910d7325a841ee5c26)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#address MediaStreamingEndpoint#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#name MediaStreamingEndpoint#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_prefix_length(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#subnet_prefix_length MediaStreamingEndpoint#subnet_prefix_length}.'''
        result = self._values.get("subnet_prefix_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingEndpointAccessControlIpAllow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingEndpointAccessControlIpAllowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointAccessControlIpAllowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1e7f8301e6d9b7f53f04e46d2b2f4fc1ea3a3a3fdf8261f7f54501a020f9b05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MediaStreamingEndpointAccessControlIpAllowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e21233e52b0eb79b9e1c3dff1c441caf8902d829818392c976a08c0ef9d6c5c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MediaStreamingEndpointAccessControlIpAllowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac96e119308057f9f8746ea812a61ad9d13543e35f5efc82e356d45fa7a5a85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecec4f9da7db682384167bc843bbcd4eb86d0e5f0143ebfcef1670e76e8ccdf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea80490ce2bec67ce68bdffa59ec0380196685e390c6a7f3f97d8428f345e39f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlIpAllow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlIpAllow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlIpAllow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3ec92b5cf5887c156d319fe85194e25eefb4f914d858fa8896967fdc5b9e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaStreamingEndpointAccessControlIpAllowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointAccessControlIpAllowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d91de97a16ccdd102377047248bf3d8262c7454b1f6069c75784b1b94c98e625)
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
            type_hints = typing.get_type_hints(_typecheckingstub__371d5a16997afad21e50a89552bea9b26bf5fe7f680513759a683f5ce68952de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a66794d1077c8667ffa9bce8392ed2d860ee2fbc7c20ee5f3a927c4bcf04ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="subnetPrefixLength")
    def subnet_prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "subnetPrefixLength"))

    @subnet_prefix_length.setter
    def subnet_prefix_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f8497ad5e3ecd3d03d573d4dca2fefa8d88a857704e0246f2e2f692165c6f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetPrefixLength", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaStreamingEndpointAccessControlIpAllow, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaStreamingEndpointAccessControlIpAllow, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaStreamingEndpointAccessControlIpAllow, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171aa09b9822fe2ca5ba23874f91a2702c656cbc1f5d3aa90deb887c4297e0db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MediaStreamingEndpointAccessControlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointAccessControlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e01233bbd7e622fa5c016b4ca4d4237e223f5db1bc56159d3062f952db6655c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAkamaiSignatureHeaderAuthenticationKey")
    def put_akamai_signature_header_authentication_key(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98ed0e3c061d7ba57b1d77009e69d985c9566aaff01b9eaf223afbdc6aead7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAkamaiSignatureHeaderAuthenticationKey", [value]))

    @jsii.member(jsii_name="putIpAllow")
    def put_ip_allow(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaStreamingEndpointAccessControlIpAllow, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e7064c66051672159913d15132d37ed3182f7109632645b1e495ec7d0568ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpAllow", [value]))

    @jsii.member(jsii_name="resetAkamaiSignatureHeaderAuthenticationKey")
    def reset_akamai_signature_header_authentication_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAkamaiSignatureHeaderAuthenticationKey", []))

    @jsii.member(jsii_name="resetIpAllow")
    def reset_ip_allow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAllow", []))

    @builtins.property
    @jsii.member(jsii_name="akamaiSignatureHeaderAuthenticationKey")
    def akamai_signature_header_authentication_key(
        self,
    ) -> MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKeyList:
        return typing.cast(MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKeyList, jsii.get(self, "akamaiSignatureHeaderAuthenticationKey"))

    @builtins.property
    @jsii.member(jsii_name="ipAllow")
    def ip_allow(self) -> MediaStreamingEndpointAccessControlIpAllowList:
        return typing.cast(MediaStreamingEndpointAccessControlIpAllowList, jsii.get(self, "ipAllow"))

    @builtins.property
    @jsii.member(jsii_name="akamaiSignatureHeaderAuthenticationKeyInput")
    def akamai_signature_header_authentication_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey]]], jsii.get(self, "akamaiSignatureHeaderAuthenticationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAllowInput")
    def ip_allow_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlIpAllow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlIpAllow]]], jsii.get(self, "ipAllowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MediaStreamingEndpointAccessControl]:
        return typing.cast(typing.Optional[MediaStreamingEndpointAccessControl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaStreamingEndpointAccessControl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f99979464a7345377960398564e418f111a41dba50c9a4f87937502461ae5dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "media_services_account_name": "mediaServicesAccountName",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "scale_units": "scaleUnits",
        "access_control": "accessControl",
        "auto_start_enabled": "autoStartEnabled",
        "cdn_enabled": "cdnEnabled",
        "cdn_profile": "cdnProfile",
        "cdn_provider": "cdnProvider",
        "cross_site_access_policy": "crossSiteAccessPolicy",
        "custom_host_names": "customHostNames",
        "description": "description",
        "id": "id",
        "max_cache_age_seconds": "maxCacheAgeSeconds",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MediaStreamingEndpointConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        media_services_account_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        scale_units: jsii.Number,
        access_control: typing.Optional[typing.Union[MediaStreamingEndpointAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_start_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cdn_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cdn_profile: typing.Optional[builtins.str] = None,
        cdn_provider: typing.Optional[builtins.str] = None,
        cross_site_access_policy: typing.Optional[typing.Union["MediaStreamingEndpointCrossSiteAccessPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_host_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_cache_age_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MediaStreamingEndpointTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#location MediaStreamingEndpoint#location}.
        :param media_services_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#media_services_account_name MediaStreamingEndpoint#media_services_account_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#name MediaStreamingEndpoint#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#resource_group_name MediaStreamingEndpoint#resource_group_name}.
        :param scale_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#scale_units MediaStreamingEndpoint#scale_units}.
        :param access_control: access_control block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#access_control MediaStreamingEndpoint#access_control}
        :param auto_start_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#auto_start_enabled MediaStreamingEndpoint#auto_start_enabled}.
        :param cdn_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cdn_enabled MediaStreamingEndpoint#cdn_enabled}.
        :param cdn_profile: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cdn_profile MediaStreamingEndpoint#cdn_profile}.
        :param cdn_provider: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cdn_provider MediaStreamingEndpoint#cdn_provider}.
        :param cross_site_access_policy: cross_site_access_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cross_site_access_policy MediaStreamingEndpoint#cross_site_access_policy}
        :param custom_host_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#custom_host_names MediaStreamingEndpoint#custom_host_names}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#description MediaStreamingEndpoint#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#id MediaStreamingEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_cache_age_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#max_cache_age_seconds MediaStreamingEndpoint#max_cache_age_seconds}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#tags MediaStreamingEndpoint#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#timeouts MediaStreamingEndpoint#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(access_control, dict):
            access_control = MediaStreamingEndpointAccessControl(**access_control)
        if isinstance(cross_site_access_policy, dict):
            cross_site_access_policy = MediaStreamingEndpointCrossSiteAccessPolicy(**cross_site_access_policy)
        if isinstance(timeouts, dict):
            timeouts = MediaStreamingEndpointTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374b9b292eb31dfeece4d6f11950e4005c2304e449be710c5591edd993d5ef6e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument media_services_account_name", value=media_services_account_name, expected_type=type_hints["media_services_account_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument scale_units", value=scale_units, expected_type=type_hints["scale_units"])
            check_type(argname="argument access_control", value=access_control, expected_type=type_hints["access_control"])
            check_type(argname="argument auto_start_enabled", value=auto_start_enabled, expected_type=type_hints["auto_start_enabled"])
            check_type(argname="argument cdn_enabled", value=cdn_enabled, expected_type=type_hints["cdn_enabled"])
            check_type(argname="argument cdn_profile", value=cdn_profile, expected_type=type_hints["cdn_profile"])
            check_type(argname="argument cdn_provider", value=cdn_provider, expected_type=type_hints["cdn_provider"])
            check_type(argname="argument cross_site_access_policy", value=cross_site_access_policy, expected_type=type_hints["cross_site_access_policy"])
            check_type(argname="argument custom_host_names", value=custom_host_names, expected_type=type_hints["custom_host_names"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_cache_age_seconds", value=max_cache_age_seconds, expected_type=type_hints["max_cache_age_seconds"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "media_services_account_name": media_services_account_name,
            "name": name,
            "resource_group_name": resource_group_name,
            "scale_units": scale_units,
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
        if access_control is not None:
            self._values["access_control"] = access_control
        if auto_start_enabled is not None:
            self._values["auto_start_enabled"] = auto_start_enabled
        if cdn_enabled is not None:
            self._values["cdn_enabled"] = cdn_enabled
        if cdn_profile is not None:
            self._values["cdn_profile"] = cdn_profile
        if cdn_provider is not None:
            self._values["cdn_provider"] = cdn_provider
        if cross_site_access_policy is not None:
            self._values["cross_site_access_policy"] = cross_site_access_policy
        if custom_host_names is not None:
            self._values["custom_host_names"] = custom_host_names
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if max_cache_age_seconds is not None:
            self._values["max_cache_age_seconds"] = max_cache_age_seconds
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#location MediaStreamingEndpoint#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def media_services_account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#media_services_account_name MediaStreamingEndpoint#media_services_account_name}.'''
        result = self._values.get("media_services_account_name")
        assert result is not None, "Required property 'media_services_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#name MediaStreamingEndpoint#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#resource_group_name MediaStreamingEndpoint#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scale_units(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#scale_units MediaStreamingEndpoint#scale_units}.'''
        result = self._values.get("scale_units")
        assert result is not None, "Required property 'scale_units' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def access_control(self) -> typing.Optional[MediaStreamingEndpointAccessControl]:
        '''access_control block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#access_control MediaStreamingEndpoint#access_control}
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[MediaStreamingEndpointAccessControl], result)

    @builtins.property
    def auto_start_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#auto_start_enabled MediaStreamingEndpoint#auto_start_enabled}.'''
        result = self._values.get("auto_start_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cdn_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cdn_enabled MediaStreamingEndpoint#cdn_enabled}.'''
        result = self._values.get("cdn_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cdn_profile(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cdn_profile MediaStreamingEndpoint#cdn_profile}.'''
        result = self._values.get("cdn_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cdn_provider(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cdn_provider MediaStreamingEndpoint#cdn_provider}.'''
        result = self._values.get("cdn_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_site_access_policy(
        self,
    ) -> typing.Optional["MediaStreamingEndpointCrossSiteAccessPolicy"]:
        '''cross_site_access_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cross_site_access_policy MediaStreamingEndpoint#cross_site_access_policy}
        '''
        result = self._values.get("cross_site_access_policy")
        return typing.cast(typing.Optional["MediaStreamingEndpointCrossSiteAccessPolicy"], result)

    @builtins.property
    def custom_host_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#custom_host_names MediaStreamingEndpoint#custom_host_names}.'''
        result = self._values.get("custom_host_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#description MediaStreamingEndpoint#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#id MediaStreamingEndpoint#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_cache_age_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#max_cache_age_seconds MediaStreamingEndpoint#max_cache_age_seconds}.'''
        result = self._values.get("max_cache_age_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#tags MediaStreamingEndpoint#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MediaStreamingEndpointTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#timeouts MediaStreamingEndpoint#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MediaStreamingEndpointTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointCrossSiteAccessPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "client_access_policy": "clientAccessPolicy",
        "cross_domain_policy": "crossDomainPolicy",
    },
)
class MediaStreamingEndpointCrossSiteAccessPolicy:
    def __init__(
        self,
        *,
        client_access_policy: typing.Optional[builtins.str] = None,
        cross_domain_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_access_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#client_access_policy MediaStreamingEndpoint#client_access_policy}.
        :param cross_domain_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cross_domain_policy MediaStreamingEndpoint#cross_domain_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf645d34b1b29827f6e35f2f3ac9477ef8a200333f519cc7a3d6710ecf1e171)
            check_type(argname="argument client_access_policy", value=client_access_policy, expected_type=type_hints["client_access_policy"])
            check_type(argname="argument cross_domain_policy", value=cross_domain_policy, expected_type=type_hints["cross_domain_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_access_policy is not None:
            self._values["client_access_policy"] = client_access_policy
        if cross_domain_policy is not None:
            self._values["cross_domain_policy"] = cross_domain_policy

    @builtins.property
    def client_access_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#client_access_policy MediaStreamingEndpoint#client_access_policy}.'''
        result = self._values.get("client_access_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_domain_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#cross_domain_policy MediaStreamingEndpoint#cross_domain_policy}.'''
        result = self._values.get("cross_domain_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingEndpointCrossSiteAccessPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingEndpointCrossSiteAccessPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointCrossSiteAccessPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae806974ebd75b0c2184b9f259739725ce42dff8ef1634c908673dc366c9d184)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7516c90b82e80d519d2d02da9294fdd0ae4f9ffdd9dc59521787e4423ffe264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientAccessPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="crossDomainPolicy")
    def cross_domain_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossDomainPolicy"))

    @cross_domain_policy.setter
    def cross_domain_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aeefd9b742aedc08a50332a179fc25207fbf173bd1fe4704cb27e04116abfa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossDomainPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MediaStreamingEndpointCrossSiteAccessPolicy]:
        return typing.cast(typing.Optional[MediaStreamingEndpointCrossSiteAccessPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MediaStreamingEndpointCrossSiteAccessPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23799c580632a1b6f6b5245c2b64ba8c69f5aa2ac131adb95ae8a9e47a57f6bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MediaStreamingEndpointTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#create MediaStreamingEndpoint#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#delete MediaStreamingEndpoint#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#read MediaStreamingEndpoint#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#update MediaStreamingEndpoint#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d01097e75b91dac4639b859e7b0f8cb79b4597b11d2a1f476bbcc20592c5f6)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#create MediaStreamingEndpoint#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#delete MediaStreamingEndpoint#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#read MediaStreamingEndpoint#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/media_streaming_endpoint#update MediaStreamingEndpoint#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MediaStreamingEndpointTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MediaStreamingEndpointTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mediaStreamingEndpoint.MediaStreamingEndpointTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b16705ce32c9b2a703b8c79e441851aabf89d5fd1a2a64e80abbafc49135a36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f19219ee9aab3c64279f777a1995bf88a4650f7b0c580f7a590d51acbf537dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ed4f2326c16c275289b3500dae6cc649f2051db2341871d03e4f4810e4d807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32bdaa3ab813e417bee37cd3416ab438d89d8db43656640ce8ade66799c1731f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c17e283da10048f6ecbf9bde376f3283c17a0b1dd665727dee936354d6d852e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MediaStreamingEndpointTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MediaStreamingEndpointTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MediaStreamingEndpointTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b84b2252989e491452aace40ee4f7709771748c393da7c2a57e30a708fe988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MediaStreamingEndpoint",
    "MediaStreamingEndpointAccessControl",
    "MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey",
    "MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKeyList",
    "MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKeyOutputReference",
    "MediaStreamingEndpointAccessControlIpAllow",
    "MediaStreamingEndpointAccessControlIpAllowList",
    "MediaStreamingEndpointAccessControlIpAllowOutputReference",
    "MediaStreamingEndpointAccessControlOutputReference",
    "MediaStreamingEndpointConfig",
    "MediaStreamingEndpointCrossSiteAccessPolicy",
    "MediaStreamingEndpointCrossSiteAccessPolicyOutputReference",
    "MediaStreamingEndpointTimeouts",
    "MediaStreamingEndpointTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ab5559914ab0448cda0e109183333b079a3a42445c608b1640a2a5296a74e9c2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    media_services_account_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    scale_units: jsii.Number,
    access_control: typing.Optional[typing.Union[MediaStreamingEndpointAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_start_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cdn_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cdn_profile: typing.Optional[builtins.str] = None,
    cdn_provider: typing.Optional[builtins.str] = None,
    cross_site_access_policy: typing.Optional[typing.Union[MediaStreamingEndpointCrossSiteAccessPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_host_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_cache_age_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MediaStreamingEndpointTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__09be9c428bf29e420db94c79735e63e5c307d84464b682c618f0e72dd87abcce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fcf6da9ecee5458c63a245104582d101193ce9a7f24aa80a016eb7260e6373(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd40cba644f8abd562842c99a9451b1c6b3b2c0d0db373f2e84ee8b52890349(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2ba85a213c5be9d3541f0b0c0cf147dfb5b49ecf815e98d251cceaa4e1dddc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8d5556d655ea54419751b9f538d342f0457c66f91c64e09ec00d9f966e0788(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c9f9b112226124f0b58d5007ebbccb9581176b553654d222d1c99ae6ea51e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b5f0ce37fd60a702c7f544c6a9c361852b7ee47f94f208823ef945b25ff1b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d313a97ded0fd3f0e962bf3b36fc1842e11ce5238ba8110f751b267188ebaa76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a466d63c15d198586635bb8ee7b3f841077cddef9f2691f9e959cc2d9aa757f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee59665997a5b41f68d3025ad0b226b1591f3a9d01282d8dc3c7800d19b2acf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28b03cfa3f3f268029cc9fea27030b0dee83626d4d444df3295e198c521398a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82258a59609ab5bb217f168f6c56b5618a916f1a717e53cd8a7620b7378cafd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037a19a5f40d8965a72922287b9402dfb53bb37a08dd1ecec54e98d0cb37e891(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aef087797f1b3327f04f92986b9b1431938700aedf35bfeab90caef37d48d35(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f632a027c09a32b32740b93c3e980c9a99ef225cd8b35d019ba25022c3a0f2f2(
    *,
    akamai_signature_header_authentication_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_allow: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaStreamingEndpointAccessControlIpAllow, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7b28388190577765472b51512f72c8f30bbe42b4c1f60cbea91abf1d22156d(
    *,
    base64_key: typing.Optional[builtins.str] = None,
    expiration: typing.Optional[builtins.str] = None,
    identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec552d3b540e5279ebf30988f7486244d76af0e1db5592fc543183d449fa87c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f4a841f0e1dd0766412aa8f6ab5c30e23f7a5ec3e479ec5e7b8af5becf1e91(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf4ddad9feb969605e309f41bac595e84da4e48346ce5c51208d48efced88ba1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd94346416cd038239f84c7b1fc084f62c4bdf3db0643d5f8071849ff47e0fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e7bbaaf75c75fa6473412533f27ba2503fa1b84a0559e196c597de9ffa02b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2cf95b8dd7af2eea17a566248c3da03fcc6a235ca66e0689475c30ad7c152c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3499900a93b932be9fd7b56576ac38456b2f96e278fe4e9f727e655b5aeed6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed4fbe6d9dabbf320bb3c1abc83b623997525f310e56f9fe01ea7e7535eebc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501a343e09284046269c16a2518b0994f284012fe26dffce2353f44b46fcc370(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87aa568188b1ee92ba6940145b5d5bb7be1f1bc137d72da719324e94a6253aec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3686aa0f0bf587ddd0603e2193a5d93355d2d9833d633c8fa82fa5f82f4abbee(
    value: typing.Optional[typing.Union[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f4f0971f3996a54003d2021e7d5980040d6e5889dd21910d7325a841ee5c26(
    *,
    address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    subnet_prefix_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e7f8301e6d9b7f53f04e46d2b2f4fc1ea3a3a3fdf8261f7f54501a020f9b05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e21233e52b0eb79b9e1c3dff1c441caf8902d829818392c976a08c0ef9d6c5c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac96e119308057f9f8746ea812a61ad9d13543e35f5efc82e356d45fa7a5a85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecec4f9da7db682384167bc843bbcd4eb86d0e5f0143ebfcef1670e76e8ccdf2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea80490ce2bec67ce68bdffa59ec0380196685e390c6a7f3f97d8428f345e39f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3ec92b5cf5887c156d319fe85194e25eefb4f914d858fa8896967fdc5b9e3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MediaStreamingEndpointAccessControlIpAllow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91de97a16ccdd102377047248bf3d8262c7454b1f6069c75784b1b94c98e625(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371d5a16997afad21e50a89552bea9b26bf5fe7f680513759a683f5ce68952de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a66794d1077c8667ffa9bce8392ed2d860ee2fbc7c20ee5f3a927c4bcf04ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8497ad5e3ecd3d03d573d4dca2fefa8d88a857704e0246f2e2f692165c6f75(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171aa09b9822fe2ca5ba23874f91a2702c656cbc1f5d3aa90deb887c4297e0db(
    value: typing.Optional[typing.Union[MediaStreamingEndpointAccessControlIpAllow, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e01233bbd7e622fa5c016b4ca4d4237e223f5db1bc56159d3062f952db6655c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98ed0e3c061d7ba57b1d77009e69d985c9566aaff01b9eaf223afbdc6aead7a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaStreamingEndpointAccessControlAkamaiSignatureHeaderAuthenticationKey, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e7064c66051672159913d15132d37ed3182f7109632645b1e495ec7d0568ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MediaStreamingEndpointAccessControlIpAllow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99979464a7345377960398564e418f111a41dba50c9a4f87937502461ae5dca(
    value: typing.Optional[MediaStreamingEndpointAccessControl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374b9b292eb31dfeece4d6f11950e4005c2304e449be710c5591edd993d5ef6e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    media_services_account_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    scale_units: jsii.Number,
    access_control: typing.Optional[typing.Union[MediaStreamingEndpointAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_start_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cdn_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cdn_profile: typing.Optional[builtins.str] = None,
    cdn_provider: typing.Optional[builtins.str] = None,
    cross_site_access_policy: typing.Optional[typing.Union[MediaStreamingEndpointCrossSiteAccessPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_host_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_cache_age_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MediaStreamingEndpointTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf645d34b1b29827f6e35f2f3ac9477ef8a200333f519cc7a3d6710ecf1e171(
    *,
    client_access_policy: typing.Optional[builtins.str] = None,
    cross_domain_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae806974ebd75b0c2184b9f259739725ce42dff8ef1634c908673dc366c9d184(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7516c90b82e80d519d2d02da9294fdd0ae4f9ffdd9dc59521787e4423ffe264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aeefd9b742aedc08a50332a179fc25207fbf173bd1fe4704cb27e04116abfa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23799c580632a1b6f6b5245c2b64ba8c69f5aa2ac131adb95ae8a9e47a57f6bb(
    value: typing.Optional[MediaStreamingEndpointCrossSiteAccessPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d01097e75b91dac4639b859e7b0f8cb79b4597b11d2a1f476bbcc20592c5f6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b16705ce32c9b2a703b8c79e441851aabf89d5fd1a2a64e80abbafc49135a36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f19219ee9aab3c64279f777a1995bf88a4650f7b0c580f7a590d51acbf537dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ed4f2326c16c275289b3500dae6cc649f2051db2341871d03e4f4810e4d807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32bdaa3ab813e417bee37cd3416ab438d89d8db43656640ce8ade66799c1731f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c17e283da10048f6ecbf9bde376f3283c17a0b1dd665727dee936354d6d852e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b84b2252989e491452aace40ee4f7709771748c393da7c2a57e30a708fe988(
    value: typing.Optional[typing.Union[MediaStreamingEndpointTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
