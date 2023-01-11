'''
# `cloudflare_zone_settings_override`

Refer to the Terraform Registory for docs: [`cloudflare_zone_settings_override`](https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override).
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


class ZoneSettingsOverride(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverride",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override cloudflare_zone_settings_override}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        zone_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        settings: typing.Optional[typing.Union["ZoneSettingsOverrideSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override cloudflare_zone_settings_override} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#zone_id ZoneSettingsOverride#zone_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#id ZoneSettingsOverride#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param settings: settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#settings ZoneSettingsOverride#settings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c10c6800a751edbd8a6c1b901cba3fbd670290a746be2a4007c60f4f4d8b705)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ZoneSettingsOverrideConfig(
            zone_id=zone_id,
            id=id,
            settings=settings,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        *,
        always_online: typing.Optional[builtins.str] = None,
        always_use_https: typing.Optional[builtins.str] = None,
        automatic_https_rewrites: typing.Optional[builtins.str] = None,
        binary_ast: typing.Optional[builtins.str] = None,
        brotli: typing.Optional[builtins.str] = None,
        browser_cache_ttl: typing.Optional[jsii.Number] = None,
        browser_check: typing.Optional[builtins.str] = None,
        cache_level: typing.Optional[builtins.str] = None,
        challenge_ttl: typing.Optional[jsii.Number] = None,
        ciphers: typing.Optional[typing.Sequence[builtins.str]] = None,
        cname_flattening: typing.Optional[builtins.str] = None,
        development_mode: typing.Optional[builtins.str] = None,
        early_hints: typing.Optional[builtins.str] = None,
        email_obfuscation: typing.Optional[builtins.str] = None,
        filter_logs_to_cloudflare: typing.Optional[builtins.str] = None,
        h2_prioritization: typing.Optional[builtins.str] = None,
        hotlink_protection: typing.Optional[builtins.str] = None,
        http2: typing.Optional[builtins.str] = None,
        http3: typing.Optional[builtins.str] = None,
        image_resizing: typing.Optional[builtins.str] = None,
        ip_geolocation: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[builtins.str] = None,
        log_to_cloudflare: typing.Optional[builtins.str] = None,
        max_upload: typing.Optional[jsii.Number] = None,
        minify: typing.Optional[typing.Union["ZoneSettingsOverrideSettingsMinify", typing.Dict[builtins.str, typing.Any]]] = None,
        min_tls_version: typing.Optional[builtins.str] = None,
        mirage: typing.Optional[builtins.str] = None,
        mobile_redirect: typing.Optional[typing.Union["ZoneSettingsOverrideSettingsMobileRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
        opportunistic_encryption: typing.Optional[builtins.str] = None,
        opportunistic_onion: typing.Optional[builtins.str] = None,
        orange_to_orange: typing.Optional[builtins.str] = None,
        origin_error_page_pass_thru: typing.Optional[builtins.str] = None,
        origin_max_http_version: typing.Optional[builtins.str] = None,
        polish: typing.Optional[builtins.str] = None,
        prefetch_preload: typing.Optional[builtins.str] = None,
        privacy_pass: typing.Optional[builtins.str] = None,
        proxy_read_timeout: typing.Optional[builtins.str] = None,
        pseudo_ipv4: typing.Optional[builtins.str] = None,
        response_buffering: typing.Optional[builtins.str] = None,
        rocket_loader: typing.Optional[builtins.str] = None,
        security_header: typing.Optional[typing.Union["ZoneSettingsOverrideSettingsSecurityHeader", typing.Dict[builtins.str, typing.Any]]] = None,
        security_level: typing.Optional[builtins.str] = None,
        server_side_exclude: typing.Optional[builtins.str] = None,
        sort_query_string_for_cache: typing.Optional[builtins.str] = None,
        ssl: typing.Optional[builtins.str] = None,
        tls12_only: typing.Optional[builtins.str] = None,
        tls13: typing.Optional[builtins.str] = None,
        tls_client_auth: typing.Optional[builtins.str] = None,
        true_client_ip_header: typing.Optional[builtins.str] = None,
        universal_ssl: typing.Optional[builtins.str] = None,
        visitor_ip: typing.Optional[builtins.str] = None,
        waf: typing.Optional[builtins.str] = None,
        webp: typing.Optional[builtins.str] = None,
        websockets: typing.Optional[builtins.str] = None,
        zero_rtt: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param always_online: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#always_online ZoneSettingsOverride#always_online}.
        :param always_use_https: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#always_use_https ZoneSettingsOverride#always_use_https}.
        :param automatic_https_rewrites: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#automatic_https_rewrites ZoneSettingsOverride#automatic_https_rewrites}.
        :param binary_ast: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#binary_ast ZoneSettingsOverride#binary_ast}.
        :param brotli: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#brotli ZoneSettingsOverride#brotli}.
        :param browser_cache_ttl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#browser_cache_ttl ZoneSettingsOverride#browser_cache_ttl}.
        :param browser_check: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#browser_check ZoneSettingsOverride#browser_check}.
        :param cache_level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#cache_level ZoneSettingsOverride#cache_level}.
        :param challenge_ttl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#challenge_ttl ZoneSettingsOverride#challenge_ttl}.
        :param ciphers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ciphers ZoneSettingsOverride#ciphers}.
        :param cname_flattening: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#cname_flattening ZoneSettingsOverride#cname_flattening}.
        :param development_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#development_mode ZoneSettingsOverride#development_mode}.
        :param early_hints: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#early_hints ZoneSettingsOverride#early_hints}.
        :param email_obfuscation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#email_obfuscation ZoneSettingsOverride#email_obfuscation}.
        :param filter_logs_to_cloudflare: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#filter_logs_to_cloudflare ZoneSettingsOverride#filter_logs_to_cloudflare}.
        :param h2_prioritization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#h2_prioritization ZoneSettingsOverride#h2_prioritization}.
        :param hotlink_protection: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#hotlink_protection ZoneSettingsOverride#hotlink_protection}.
        :param http2: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#http2 ZoneSettingsOverride#http2}.
        :param http3: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#http3 ZoneSettingsOverride#http3}.
        :param image_resizing: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#image_resizing ZoneSettingsOverride#image_resizing}.
        :param ip_geolocation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ip_geolocation ZoneSettingsOverride#ip_geolocation}.
        :param ipv6: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ipv6 ZoneSettingsOverride#ipv6}.
        :param log_to_cloudflare: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#log_to_cloudflare ZoneSettingsOverride#log_to_cloudflare}.
        :param max_upload: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#max_upload ZoneSettingsOverride#max_upload}.
        :param minify: minify block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#minify ZoneSettingsOverride#minify}
        :param min_tls_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#min_tls_version ZoneSettingsOverride#min_tls_version}.
        :param mirage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#mirage ZoneSettingsOverride#mirage}.
        :param mobile_redirect: mobile_redirect block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#mobile_redirect ZoneSettingsOverride#mobile_redirect}
        :param opportunistic_encryption: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#opportunistic_encryption ZoneSettingsOverride#opportunistic_encryption}.
        :param opportunistic_onion: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#opportunistic_onion ZoneSettingsOverride#opportunistic_onion}.
        :param orange_to_orange: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#orange_to_orange ZoneSettingsOverride#orange_to_orange}.
        :param origin_error_page_pass_thru: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#origin_error_page_pass_thru ZoneSettingsOverride#origin_error_page_pass_thru}.
        :param origin_max_http_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#origin_max_http_version ZoneSettingsOverride#origin_max_http_version}.
        :param polish: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#polish ZoneSettingsOverride#polish}.
        :param prefetch_preload: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#prefetch_preload ZoneSettingsOverride#prefetch_preload}.
        :param privacy_pass: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#privacy_pass ZoneSettingsOverride#privacy_pass}.
        :param proxy_read_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#proxy_read_timeout ZoneSettingsOverride#proxy_read_timeout}.
        :param pseudo_ipv4: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#pseudo_ipv4 ZoneSettingsOverride#pseudo_ipv4}.
        :param response_buffering: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#response_buffering ZoneSettingsOverride#response_buffering}.
        :param rocket_loader: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#rocket_loader ZoneSettingsOverride#rocket_loader}.
        :param security_header: security_header block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#security_header ZoneSettingsOverride#security_header}
        :param security_level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#security_level ZoneSettingsOverride#security_level}.
        :param server_side_exclude: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#server_side_exclude ZoneSettingsOverride#server_side_exclude}.
        :param sort_query_string_for_cache: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#sort_query_string_for_cache ZoneSettingsOverride#sort_query_string_for_cache}.
        :param ssl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ssl ZoneSettingsOverride#ssl}.
        :param tls12_only: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#tls_1_2_only ZoneSettingsOverride#tls_1_2_only}.
        :param tls13: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#tls_1_3 ZoneSettingsOverride#tls_1_3}.
        :param tls_client_auth: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#tls_client_auth ZoneSettingsOverride#tls_client_auth}.
        :param true_client_ip_header: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#true_client_ip_header ZoneSettingsOverride#true_client_ip_header}.
        :param universal_ssl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#universal_ssl ZoneSettingsOverride#universal_ssl}.
        :param visitor_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#visitor_ip ZoneSettingsOverride#visitor_ip}.
        :param waf: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#waf ZoneSettingsOverride#waf}.
        :param webp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#webp ZoneSettingsOverride#webp}.
        :param websockets: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#websockets ZoneSettingsOverride#websockets}.
        :param zero_rtt: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#zero_rtt ZoneSettingsOverride#zero_rtt}.
        '''
        value = ZoneSettingsOverrideSettings(
            always_online=always_online,
            always_use_https=always_use_https,
            automatic_https_rewrites=automatic_https_rewrites,
            binary_ast=binary_ast,
            brotli=brotli,
            browser_cache_ttl=browser_cache_ttl,
            browser_check=browser_check,
            cache_level=cache_level,
            challenge_ttl=challenge_ttl,
            ciphers=ciphers,
            cname_flattening=cname_flattening,
            development_mode=development_mode,
            early_hints=early_hints,
            email_obfuscation=email_obfuscation,
            filter_logs_to_cloudflare=filter_logs_to_cloudflare,
            h2_prioritization=h2_prioritization,
            hotlink_protection=hotlink_protection,
            http2=http2,
            http3=http3,
            image_resizing=image_resizing,
            ip_geolocation=ip_geolocation,
            ipv6=ipv6,
            log_to_cloudflare=log_to_cloudflare,
            max_upload=max_upload,
            minify=minify,
            min_tls_version=min_tls_version,
            mirage=mirage,
            mobile_redirect=mobile_redirect,
            opportunistic_encryption=opportunistic_encryption,
            opportunistic_onion=opportunistic_onion,
            orange_to_orange=orange_to_orange,
            origin_error_page_pass_thru=origin_error_page_pass_thru,
            origin_max_http_version=origin_max_http_version,
            polish=polish,
            prefetch_preload=prefetch_preload,
            privacy_pass=privacy_pass,
            proxy_read_timeout=proxy_read_timeout,
            pseudo_ipv4=pseudo_ipv4,
            response_buffering=response_buffering,
            rocket_loader=rocket_loader,
            security_header=security_header,
            security_level=security_level,
            server_side_exclude=server_side_exclude,
            sort_query_string_for_cache=sort_query_string_for_cache,
            ssl=ssl,
            tls12_only=tls12_only,
            tls13=tls13,
            tls_client_auth=tls_client_auth,
            true_client_ip_header=true_client_ip_header,
            universal_ssl=universal_ssl,
            visitor_ip=visitor_ip,
            waf=waf,
            webp=webp,
            websockets=websockets,
            zero_rtt=zero_rtt,
        )

        return typing.cast(None, jsii.invoke(self, "putSettings", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="initialSettings")
    def initial_settings(self) -> "ZoneSettingsOverrideInitialSettingsList":
        return typing.cast("ZoneSettingsOverrideInitialSettingsList", jsii.get(self, "initialSettings"))

    @builtins.property
    @jsii.member(jsii_name="initialSettingsReadAt")
    def initial_settings_read_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initialSettingsReadAt"))

    @builtins.property
    @jsii.member(jsii_name="readonlySettings")
    def readonly_settings(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "readonlySettings"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "ZoneSettingsOverrideSettingsOutputReference":
        return typing.cast("ZoneSettingsOverrideSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="zoneStatus")
    def zone_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneStatus"))

    @builtins.property
    @jsii.member(jsii_name="zoneType")
    def zone_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneType"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(self) -> typing.Optional["ZoneSettingsOverrideSettings"]:
        return typing.cast(typing.Optional["ZoneSettingsOverrideSettings"], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333d8f50b4c3b29d844894530b1f39e71ee6a864d39f20438f63487f973bd101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc314ab95e37bd3a23b70005373101bc9e1edef2944c7ea133116e48a141518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "zone_id": "zoneId",
        "id": "id",
        "settings": "settings",
    },
)
class ZoneSettingsOverrideConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        zone_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        settings: typing.Optional[typing.Union["ZoneSettingsOverrideSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#zone_id ZoneSettingsOverride#zone_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#id ZoneSettingsOverride#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param settings: settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#settings ZoneSettingsOverride#settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(settings, dict):
            settings = ZoneSettingsOverrideSettings(**settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce340b9b59b16072eaa592860129ffb73bb9b7317b889d85378405d7cdf1b593)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if id is not None:
            self._values["id"] = id
        if settings is not None:
            self._values["settings"] = settings

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
    def zone_id(self) -> builtins.str:
        '''The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#zone_id ZoneSettingsOverride#zone_id}
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#id ZoneSettingsOverride#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def settings(self) -> typing.Optional["ZoneSettingsOverrideSettings"]:
        '''settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#settings ZoneSettingsOverride#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["ZoneSettingsOverrideSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneSettingsOverrideConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettings",
    jsii_struct_bases=[],
    name_mapping={},
)
class ZoneSettingsOverrideInitialSettings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneSettingsOverrideInitialSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZoneSettingsOverrideInitialSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d34cb3ae19588347c59c496121c2321e28274054a07e8a5901607a4ef8b79429)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZoneSettingsOverrideInitialSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86305045a06e67ccde7f2b3eb589f5c8ce9e3171ad234caa1f9a37abba02639)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZoneSettingsOverrideInitialSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c60d057a1f9dddcec7cea1b4053e6652d727731a84be428cc615965e2b67b86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ecbd5cbbf560f48cbd81330694cca3970365f33e4d8e101bd699165bbfdbebe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1d41b4bab6144747141f92096e20db2130da1110cab4ac8c2e10e7a5c1a4242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettingsMinify",
    jsii_struct_bases=[],
    name_mapping={},
)
class ZoneSettingsOverrideInitialSettingsMinify:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneSettingsOverrideInitialSettingsMinify(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZoneSettingsOverrideInitialSettingsMinifyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettingsMinifyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e55d308bd9ab7df6b3c618fc2e7084ae2e5b1bfd763b809c2d084e4bf67afad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZoneSettingsOverrideInitialSettingsMinifyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f5c60fab9c364a78669a3fbfa6c3e051fb267df64d4092071fbd01ab0901e4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZoneSettingsOverrideInitialSettingsMinifyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e8e49ade9834b6905096e663380f4aca58564217ce0cdbcc97c33267528e2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98357c2761f7484eff52e26be457c6d2296fee31188eca7ac52981592eb58605)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef1e7e03528c36bfbd25eca7997516bc5d48e2a36d2e64d4cb196f72d6369e46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ZoneSettingsOverrideInitialSettingsMinifyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettingsMinifyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df512b2f2a4bb9e95a3a0d2dd9d6ed59aa7a7b498345ec0318c12740d82ffe6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="css")
    def css(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "css"))

    @builtins.property
    @jsii.member(jsii_name="html")
    def html(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "html"))

    @builtins.property
    @jsii.member(jsii_name="js")
    def js(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "js"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZoneSettingsOverrideInitialSettingsMinify]:
        return typing.cast(typing.Optional[ZoneSettingsOverrideInitialSettingsMinify], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZoneSettingsOverrideInitialSettingsMinify],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0be52c34596e8d0980ba01b629c51370a52f9421f20bbb1b824efc84f376aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettingsMobileRedirect",
    jsii_struct_bases=[],
    name_mapping={},
)
class ZoneSettingsOverrideInitialSettingsMobileRedirect:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneSettingsOverrideInitialSettingsMobileRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZoneSettingsOverrideInitialSettingsMobileRedirectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettingsMobileRedirectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e94ef511f9d59c10fb77c98f80f7d82822b0dc4462870c33b7a093c63e6f82ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZoneSettingsOverrideInitialSettingsMobileRedirectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18ae254d74f9bfb9e933f687f743454e9055d6a3c72d8e41184ebd30b01cb8e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZoneSettingsOverrideInitialSettingsMobileRedirectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d5f6732eb3f8b361ea1b360c66a75477e5167d9c9382fe308fcef6779166a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__023fdd4a6a0ec74aca2ae76e7861bb527f6817179bbbbf671911413f59e63798)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9be06876e7724498b5900a86ba1328c0976904fd22f57fed6f9b35bcb4544013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ZoneSettingsOverrideInitialSettingsMobileRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettingsMobileRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3fceef8de5940bac0f63847b1766d19f5cdd76fe8c6ef87271d8c2ec66b0db8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="mobileSubdomain")
    def mobile_subdomain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobileSubdomain"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="stripUri")
    def strip_uri(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "stripUri"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZoneSettingsOverrideInitialSettingsMobileRedirect]:
        return typing.cast(typing.Optional[ZoneSettingsOverrideInitialSettingsMobileRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZoneSettingsOverrideInitialSettingsMobileRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c783dbaa86c65b1409ad7fd13872f0fd5f1faed9dd755288be2936d5178e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ZoneSettingsOverrideInitialSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29b256e8200b9beabd76ddd80a04a6da2a0914025b2d27c8c23a30bd68b5d7b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="alwaysOnline")
    def always_online(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alwaysOnline"))

    @builtins.property
    @jsii.member(jsii_name="alwaysUseHttps")
    def always_use_https(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alwaysUseHttps"))

    @builtins.property
    @jsii.member(jsii_name="automaticHttpsRewrites")
    def automatic_https_rewrites(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "automaticHttpsRewrites"))

    @builtins.property
    @jsii.member(jsii_name="binaryAst")
    def binary_ast(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryAst"))

    @builtins.property
    @jsii.member(jsii_name="brotli")
    def brotli(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "brotli"))

    @builtins.property
    @jsii.member(jsii_name="browserCacheTtl")
    def browser_cache_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "browserCacheTtl"))

    @builtins.property
    @jsii.member(jsii_name="browserCheck")
    def browser_check(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "browserCheck"))

    @builtins.property
    @jsii.member(jsii_name="cacheLevel")
    def cache_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheLevel"))

    @builtins.property
    @jsii.member(jsii_name="challengeTtl")
    def challenge_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "challengeTtl"))

    @builtins.property
    @jsii.member(jsii_name="ciphers")
    def ciphers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ciphers"))

    @builtins.property
    @jsii.member(jsii_name="cnameFlattening")
    def cname_flattening(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cnameFlattening"))

    @builtins.property
    @jsii.member(jsii_name="developmentMode")
    def development_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "developmentMode"))

    @builtins.property
    @jsii.member(jsii_name="earlyHints")
    def early_hints(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "earlyHints"))

    @builtins.property
    @jsii.member(jsii_name="emailObfuscation")
    def email_obfuscation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailObfuscation"))

    @builtins.property
    @jsii.member(jsii_name="filterLogsToCloudflare")
    def filter_logs_to_cloudflare(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterLogsToCloudflare"))

    @builtins.property
    @jsii.member(jsii_name="h2Prioritization")
    def h2_prioritization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "h2Prioritization"))

    @builtins.property
    @jsii.member(jsii_name="hotlinkProtection")
    def hotlink_protection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hotlinkProtection"))

    @builtins.property
    @jsii.member(jsii_name="http2")
    def http2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "http2"))

    @builtins.property
    @jsii.member(jsii_name="http3")
    def http3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "http3"))

    @builtins.property
    @jsii.member(jsii_name="imageResizing")
    def image_resizing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageResizing"))

    @builtins.property
    @jsii.member(jsii_name="ipGeolocation")
    def ip_geolocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipGeolocation"))

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6"))

    @builtins.property
    @jsii.member(jsii_name="logToCloudflare")
    def log_to_cloudflare(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logToCloudflare"))

    @builtins.property
    @jsii.member(jsii_name="maxUpload")
    def max_upload(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUpload"))

    @builtins.property
    @jsii.member(jsii_name="minify")
    def minify(self) -> ZoneSettingsOverrideInitialSettingsMinifyList:
        return typing.cast(ZoneSettingsOverrideInitialSettingsMinifyList, jsii.get(self, "minify"))

    @builtins.property
    @jsii.member(jsii_name="minTlsVersion")
    def min_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minTlsVersion"))

    @builtins.property
    @jsii.member(jsii_name="mirage")
    def mirage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mirage"))

    @builtins.property
    @jsii.member(jsii_name="mobileRedirect")
    def mobile_redirect(self) -> ZoneSettingsOverrideInitialSettingsMobileRedirectList:
        return typing.cast(ZoneSettingsOverrideInitialSettingsMobileRedirectList, jsii.get(self, "mobileRedirect"))

    @builtins.property
    @jsii.member(jsii_name="opportunisticEncryption")
    def opportunistic_encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "opportunisticEncryption"))

    @builtins.property
    @jsii.member(jsii_name="opportunisticOnion")
    def opportunistic_onion(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "opportunisticOnion"))

    @builtins.property
    @jsii.member(jsii_name="orangeToOrange")
    def orange_to_orange(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orangeToOrange"))

    @builtins.property
    @jsii.member(jsii_name="originErrorPagePassThru")
    def origin_error_page_pass_thru(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originErrorPagePassThru"))

    @builtins.property
    @jsii.member(jsii_name="originMaxHttpVersion")
    def origin_max_http_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originMaxHttpVersion"))

    @builtins.property
    @jsii.member(jsii_name="polish")
    def polish(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "polish"))

    @builtins.property
    @jsii.member(jsii_name="prefetchPreload")
    def prefetch_preload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefetchPreload"))

    @builtins.property
    @jsii.member(jsii_name="privacyPass")
    def privacy_pass(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privacyPass"))

    @builtins.property
    @jsii.member(jsii_name="proxyReadTimeout")
    def proxy_read_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyReadTimeout"))

    @builtins.property
    @jsii.member(jsii_name="pseudoIpv4")
    def pseudo_ipv4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pseudoIpv4"))

    @builtins.property
    @jsii.member(jsii_name="responseBuffering")
    def response_buffering(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseBuffering"))

    @builtins.property
    @jsii.member(jsii_name="rocketLoader")
    def rocket_loader(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rocketLoader"))

    @builtins.property
    @jsii.member(jsii_name="securityHeader")
    def security_header(
        self,
    ) -> "ZoneSettingsOverrideInitialSettingsSecurityHeaderList":
        return typing.cast("ZoneSettingsOverrideInitialSettingsSecurityHeaderList", jsii.get(self, "securityHeader"))

    @builtins.property
    @jsii.member(jsii_name="securityLevel")
    def security_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityLevel"))

    @builtins.property
    @jsii.member(jsii_name="serverSideExclude")
    def server_side_exclude(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverSideExclude"))

    @builtins.property
    @jsii.member(jsii_name="sortQueryStringForCache")
    def sort_query_string_for_cache(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sortQueryStringForCache"))

    @builtins.property
    @jsii.member(jsii_name="ssl")
    def ssl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssl"))

    @builtins.property
    @jsii.member(jsii_name="tls12Only")
    def tls12_only(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tls12Only"))

    @builtins.property
    @jsii.member(jsii_name="tls13")
    def tls13(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tls13"))

    @builtins.property
    @jsii.member(jsii_name="tlsClientAuth")
    def tls_client_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsClientAuth"))

    @builtins.property
    @jsii.member(jsii_name="trueClientIpHeader")
    def true_client_ip_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trueClientIpHeader"))

    @builtins.property
    @jsii.member(jsii_name="universalSsl")
    def universal_ssl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "universalSsl"))

    @builtins.property
    @jsii.member(jsii_name="visitorIp")
    def visitor_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visitorIp"))

    @builtins.property
    @jsii.member(jsii_name="waf")
    def waf(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "waf"))

    @builtins.property
    @jsii.member(jsii_name="webp")
    def webp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webp"))

    @builtins.property
    @jsii.member(jsii_name="websockets")
    def websockets(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "websockets"))

    @builtins.property
    @jsii.member(jsii_name="zeroRtt")
    def zero_rtt(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zeroRtt"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZoneSettingsOverrideInitialSettings]:
        return typing.cast(typing.Optional[ZoneSettingsOverrideInitialSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZoneSettingsOverrideInitialSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebea9a100d1c96723de2ce8cdf85467eea1bad64c6b6ff441fb6f1982d24bdf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettingsSecurityHeader",
    jsii_struct_bases=[],
    name_mapping={},
)
class ZoneSettingsOverrideInitialSettingsSecurityHeader:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneSettingsOverrideInitialSettingsSecurityHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZoneSettingsOverrideInitialSettingsSecurityHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettingsSecurityHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50a48bd9db836a276982cade7cf0faa27e936d806b50adb92b06c887dfd03239)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZoneSettingsOverrideInitialSettingsSecurityHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a92f8ab861c4576c5a0800b71208d7f79ea5c091e5e7530be1c1ca0acdaad97)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZoneSettingsOverrideInitialSettingsSecurityHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2290be03209fdddfef506a307d53863c0407dc9b4989297923826a561d4f5fda)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41fd9853196db05055ffed5a49ff6cb0fb22e9429840381b861a3f14cd7c7261)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e5a2043491ef903b076e01efe3b02bd4fdd504f2b3842ff65ad3b7ef07d6505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ZoneSettingsOverrideInitialSettingsSecurityHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideInitialSettingsSecurityHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b393dc63afdc47cc33e8d9c22b4ff52fbbafd1f5e7d5fc8069ce96740e91f9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="includeSubdomains")
    def include_subdomains(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "includeSubdomains"))

    @builtins.property
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAge"))

    @builtins.property
    @jsii.member(jsii_name="nosniff")
    def nosniff(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "nosniff"))

    @builtins.property
    @jsii.member(jsii_name="preload")
    def preload(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "preload"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZoneSettingsOverrideInitialSettingsSecurityHeader]:
        return typing.cast(typing.Optional[ZoneSettingsOverrideInitialSettingsSecurityHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZoneSettingsOverrideInitialSettingsSecurityHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11710c016294dc1dd75b179e68a1be1df9c53c1cc676cf6668ae665c39b130eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideSettings",
    jsii_struct_bases=[],
    name_mapping={
        "always_online": "alwaysOnline",
        "always_use_https": "alwaysUseHttps",
        "automatic_https_rewrites": "automaticHttpsRewrites",
        "binary_ast": "binaryAst",
        "brotli": "brotli",
        "browser_cache_ttl": "browserCacheTtl",
        "browser_check": "browserCheck",
        "cache_level": "cacheLevel",
        "challenge_ttl": "challengeTtl",
        "ciphers": "ciphers",
        "cname_flattening": "cnameFlattening",
        "development_mode": "developmentMode",
        "early_hints": "earlyHints",
        "email_obfuscation": "emailObfuscation",
        "filter_logs_to_cloudflare": "filterLogsToCloudflare",
        "h2_prioritization": "h2Prioritization",
        "hotlink_protection": "hotlinkProtection",
        "http2": "http2",
        "http3": "http3",
        "image_resizing": "imageResizing",
        "ip_geolocation": "ipGeolocation",
        "ipv6": "ipv6",
        "log_to_cloudflare": "logToCloudflare",
        "max_upload": "maxUpload",
        "minify": "minify",
        "min_tls_version": "minTlsVersion",
        "mirage": "mirage",
        "mobile_redirect": "mobileRedirect",
        "opportunistic_encryption": "opportunisticEncryption",
        "opportunistic_onion": "opportunisticOnion",
        "orange_to_orange": "orangeToOrange",
        "origin_error_page_pass_thru": "originErrorPagePassThru",
        "origin_max_http_version": "originMaxHttpVersion",
        "polish": "polish",
        "prefetch_preload": "prefetchPreload",
        "privacy_pass": "privacyPass",
        "proxy_read_timeout": "proxyReadTimeout",
        "pseudo_ipv4": "pseudoIpv4",
        "response_buffering": "responseBuffering",
        "rocket_loader": "rocketLoader",
        "security_header": "securityHeader",
        "security_level": "securityLevel",
        "server_side_exclude": "serverSideExclude",
        "sort_query_string_for_cache": "sortQueryStringForCache",
        "ssl": "ssl",
        "tls12_only": "tls12Only",
        "tls13": "tls13",
        "tls_client_auth": "tlsClientAuth",
        "true_client_ip_header": "trueClientIpHeader",
        "universal_ssl": "universalSsl",
        "visitor_ip": "visitorIp",
        "waf": "waf",
        "webp": "webp",
        "websockets": "websockets",
        "zero_rtt": "zeroRtt",
    },
)
class ZoneSettingsOverrideSettings:
    def __init__(
        self,
        *,
        always_online: typing.Optional[builtins.str] = None,
        always_use_https: typing.Optional[builtins.str] = None,
        automatic_https_rewrites: typing.Optional[builtins.str] = None,
        binary_ast: typing.Optional[builtins.str] = None,
        brotli: typing.Optional[builtins.str] = None,
        browser_cache_ttl: typing.Optional[jsii.Number] = None,
        browser_check: typing.Optional[builtins.str] = None,
        cache_level: typing.Optional[builtins.str] = None,
        challenge_ttl: typing.Optional[jsii.Number] = None,
        ciphers: typing.Optional[typing.Sequence[builtins.str]] = None,
        cname_flattening: typing.Optional[builtins.str] = None,
        development_mode: typing.Optional[builtins.str] = None,
        early_hints: typing.Optional[builtins.str] = None,
        email_obfuscation: typing.Optional[builtins.str] = None,
        filter_logs_to_cloudflare: typing.Optional[builtins.str] = None,
        h2_prioritization: typing.Optional[builtins.str] = None,
        hotlink_protection: typing.Optional[builtins.str] = None,
        http2: typing.Optional[builtins.str] = None,
        http3: typing.Optional[builtins.str] = None,
        image_resizing: typing.Optional[builtins.str] = None,
        ip_geolocation: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[builtins.str] = None,
        log_to_cloudflare: typing.Optional[builtins.str] = None,
        max_upload: typing.Optional[jsii.Number] = None,
        minify: typing.Optional[typing.Union["ZoneSettingsOverrideSettingsMinify", typing.Dict[builtins.str, typing.Any]]] = None,
        min_tls_version: typing.Optional[builtins.str] = None,
        mirage: typing.Optional[builtins.str] = None,
        mobile_redirect: typing.Optional[typing.Union["ZoneSettingsOverrideSettingsMobileRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
        opportunistic_encryption: typing.Optional[builtins.str] = None,
        opportunistic_onion: typing.Optional[builtins.str] = None,
        orange_to_orange: typing.Optional[builtins.str] = None,
        origin_error_page_pass_thru: typing.Optional[builtins.str] = None,
        origin_max_http_version: typing.Optional[builtins.str] = None,
        polish: typing.Optional[builtins.str] = None,
        prefetch_preload: typing.Optional[builtins.str] = None,
        privacy_pass: typing.Optional[builtins.str] = None,
        proxy_read_timeout: typing.Optional[builtins.str] = None,
        pseudo_ipv4: typing.Optional[builtins.str] = None,
        response_buffering: typing.Optional[builtins.str] = None,
        rocket_loader: typing.Optional[builtins.str] = None,
        security_header: typing.Optional[typing.Union["ZoneSettingsOverrideSettingsSecurityHeader", typing.Dict[builtins.str, typing.Any]]] = None,
        security_level: typing.Optional[builtins.str] = None,
        server_side_exclude: typing.Optional[builtins.str] = None,
        sort_query_string_for_cache: typing.Optional[builtins.str] = None,
        ssl: typing.Optional[builtins.str] = None,
        tls12_only: typing.Optional[builtins.str] = None,
        tls13: typing.Optional[builtins.str] = None,
        tls_client_auth: typing.Optional[builtins.str] = None,
        true_client_ip_header: typing.Optional[builtins.str] = None,
        universal_ssl: typing.Optional[builtins.str] = None,
        visitor_ip: typing.Optional[builtins.str] = None,
        waf: typing.Optional[builtins.str] = None,
        webp: typing.Optional[builtins.str] = None,
        websockets: typing.Optional[builtins.str] = None,
        zero_rtt: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param always_online: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#always_online ZoneSettingsOverride#always_online}.
        :param always_use_https: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#always_use_https ZoneSettingsOverride#always_use_https}.
        :param automatic_https_rewrites: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#automatic_https_rewrites ZoneSettingsOverride#automatic_https_rewrites}.
        :param binary_ast: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#binary_ast ZoneSettingsOverride#binary_ast}.
        :param brotli: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#brotli ZoneSettingsOverride#brotli}.
        :param browser_cache_ttl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#browser_cache_ttl ZoneSettingsOverride#browser_cache_ttl}.
        :param browser_check: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#browser_check ZoneSettingsOverride#browser_check}.
        :param cache_level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#cache_level ZoneSettingsOverride#cache_level}.
        :param challenge_ttl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#challenge_ttl ZoneSettingsOverride#challenge_ttl}.
        :param ciphers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ciphers ZoneSettingsOverride#ciphers}.
        :param cname_flattening: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#cname_flattening ZoneSettingsOverride#cname_flattening}.
        :param development_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#development_mode ZoneSettingsOverride#development_mode}.
        :param early_hints: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#early_hints ZoneSettingsOverride#early_hints}.
        :param email_obfuscation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#email_obfuscation ZoneSettingsOverride#email_obfuscation}.
        :param filter_logs_to_cloudflare: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#filter_logs_to_cloudflare ZoneSettingsOverride#filter_logs_to_cloudflare}.
        :param h2_prioritization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#h2_prioritization ZoneSettingsOverride#h2_prioritization}.
        :param hotlink_protection: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#hotlink_protection ZoneSettingsOverride#hotlink_protection}.
        :param http2: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#http2 ZoneSettingsOverride#http2}.
        :param http3: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#http3 ZoneSettingsOverride#http3}.
        :param image_resizing: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#image_resizing ZoneSettingsOverride#image_resizing}.
        :param ip_geolocation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ip_geolocation ZoneSettingsOverride#ip_geolocation}.
        :param ipv6: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ipv6 ZoneSettingsOverride#ipv6}.
        :param log_to_cloudflare: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#log_to_cloudflare ZoneSettingsOverride#log_to_cloudflare}.
        :param max_upload: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#max_upload ZoneSettingsOverride#max_upload}.
        :param minify: minify block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#minify ZoneSettingsOverride#minify}
        :param min_tls_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#min_tls_version ZoneSettingsOverride#min_tls_version}.
        :param mirage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#mirage ZoneSettingsOverride#mirage}.
        :param mobile_redirect: mobile_redirect block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#mobile_redirect ZoneSettingsOverride#mobile_redirect}
        :param opportunistic_encryption: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#opportunistic_encryption ZoneSettingsOverride#opportunistic_encryption}.
        :param opportunistic_onion: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#opportunistic_onion ZoneSettingsOverride#opportunistic_onion}.
        :param orange_to_orange: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#orange_to_orange ZoneSettingsOverride#orange_to_orange}.
        :param origin_error_page_pass_thru: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#origin_error_page_pass_thru ZoneSettingsOverride#origin_error_page_pass_thru}.
        :param origin_max_http_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#origin_max_http_version ZoneSettingsOverride#origin_max_http_version}.
        :param polish: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#polish ZoneSettingsOverride#polish}.
        :param prefetch_preload: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#prefetch_preload ZoneSettingsOverride#prefetch_preload}.
        :param privacy_pass: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#privacy_pass ZoneSettingsOverride#privacy_pass}.
        :param proxy_read_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#proxy_read_timeout ZoneSettingsOverride#proxy_read_timeout}.
        :param pseudo_ipv4: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#pseudo_ipv4 ZoneSettingsOverride#pseudo_ipv4}.
        :param response_buffering: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#response_buffering ZoneSettingsOverride#response_buffering}.
        :param rocket_loader: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#rocket_loader ZoneSettingsOverride#rocket_loader}.
        :param security_header: security_header block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#security_header ZoneSettingsOverride#security_header}
        :param security_level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#security_level ZoneSettingsOverride#security_level}.
        :param server_side_exclude: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#server_side_exclude ZoneSettingsOverride#server_side_exclude}.
        :param sort_query_string_for_cache: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#sort_query_string_for_cache ZoneSettingsOverride#sort_query_string_for_cache}.
        :param ssl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ssl ZoneSettingsOverride#ssl}.
        :param tls12_only: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#tls_1_2_only ZoneSettingsOverride#tls_1_2_only}.
        :param tls13: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#tls_1_3 ZoneSettingsOverride#tls_1_3}.
        :param tls_client_auth: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#tls_client_auth ZoneSettingsOverride#tls_client_auth}.
        :param true_client_ip_header: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#true_client_ip_header ZoneSettingsOverride#true_client_ip_header}.
        :param universal_ssl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#universal_ssl ZoneSettingsOverride#universal_ssl}.
        :param visitor_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#visitor_ip ZoneSettingsOverride#visitor_ip}.
        :param waf: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#waf ZoneSettingsOverride#waf}.
        :param webp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#webp ZoneSettingsOverride#webp}.
        :param websockets: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#websockets ZoneSettingsOverride#websockets}.
        :param zero_rtt: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#zero_rtt ZoneSettingsOverride#zero_rtt}.
        '''
        if isinstance(minify, dict):
            minify = ZoneSettingsOverrideSettingsMinify(**minify)
        if isinstance(mobile_redirect, dict):
            mobile_redirect = ZoneSettingsOverrideSettingsMobileRedirect(**mobile_redirect)
        if isinstance(security_header, dict):
            security_header = ZoneSettingsOverrideSettingsSecurityHeader(**security_header)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458332e0a6cc8bd4dc90e0e73f6df6be2ebaab3530e33bc4eebfd1fd982bdfb3)
            check_type(argname="argument always_online", value=always_online, expected_type=type_hints["always_online"])
            check_type(argname="argument always_use_https", value=always_use_https, expected_type=type_hints["always_use_https"])
            check_type(argname="argument automatic_https_rewrites", value=automatic_https_rewrites, expected_type=type_hints["automatic_https_rewrites"])
            check_type(argname="argument binary_ast", value=binary_ast, expected_type=type_hints["binary_ast"])
            check_type(argname="argument brotli", value=brotli, expected_type=type_hints["brotli"])
            check_type(argname="argument browser_cache_ttl", value=browser_cache_ttl, expected_type=type_hints["browser_cache_ttl"])
            check_type(argname="argument browser_check", value=browser_check, expected_type=type_hints["browser_check"])
            check_type(argname="argument cache_level", value=cache_level, expected_type=type_hints["cache_level"])
            check_type(argname="argument challenge_ttl", value=challenge_ttl, expected_type=type_hints["challenge_ttl"])
            check_type(argname="argument ciphers", value=ciphers, expected_type=type_hints["ciphers"])
            check_type(argname="argument cname_flattening", value=cname_flattening, expected_type=type_hints["cname_flattening"])
            check_type(argname="argument development_mode", value=development_mode, expected_type=type_hints["development_mode"])
            check_type(argname="argument early_hints", value=early_hints, expected_type=type_hints["early_hints"])
            check_type(argname="argument email_obfuscation", value=email_obfuscation, expected_type=type_hints["email_obfuscation"])
            check_type(argname="argument filter_logs_to_cloudflare", value=filter_logs_to_cloudflare, expected_type=type_hints["filter_logs_to_cloudflare"])
            check_type(argname="argument h2_prioritization", value=h2_prioritization, expected_type=type_hints["h2_prioritization"])
            check_type(argname="argument hotlink_protection", value=hotlink_protection, expected_type=type_hints["hotlink_protection"])
            check_type(argname="argument http2", value=http2, expected_type=type_hints["http2"])
            check_type(argname="argument http3", value=http3, expected_type=type_hints["http3"])
            check_type(argname="argument image_resizing", value=image_resizing, expected_type=type_hints["image_resizing"])
            check_type(argname="argument ip_geolocation", value=ip_geolocation, expected_type=type_hints["ip_geolocation"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
            check_type(argname="argument log_to_cloudflare", value=log_to_cloudflare, expected_type=type_hints["log_to_cloudflare"])
            check_type(argname="argument max_upload", value=max_upload, expected_type=type_hints["max_upload"])
            check_type(argname="argument minify", value=minify, expected_type=type_hints["minify"])
            check_type(argname="argument min_tls_version", value=min_tls_version, expected_type=type_hints["min_tls_version"])
            check_type(argname="argument mirage", value=mirage, expected_type=type_hints["mirage"])
            check_type(argname="argument mobile_redirect", value=mobile_redirect, expected_type=type_hints["mobile_redirect"])
            check_type(argname="argument opportunistic_encryption", value=opportunistic_encryption, expected_type=type_hints["opportunistic_encryption"])
            check_type(argname="argument opportunistic_onion", value=opportunistic_onion, expected_type=type_hints["opportunistic_onion"])
            check_type(argname="argument orange_to_orange", value=orange_to_orange, expected_type=type_hints["orange_to_orange"])
            check_type(argname="argument origin_error_page_pass_thru", value=origin_error_page_pass_thru, expected_type=type_hints["origin_error_page_pass_thru"])
            check_type(argname="argument origin_max_http_version", value=origin_max_http_version, expected_type=type_hints["origin_max_http_version"])
            check_type(argname="argument polish", value=polish, expected_type=type_hints["polish"])
            check_type(argname="argument prefetch_preload", value=prefetch_preload, expected_type=type_hints["prefetch_preload"])
            check_type(argname="argument privacy_pass", value=privacy_pass, expected_type=type_hints["privacy_pass"])
            check_type(argname="argument proxy_read_timeout", value=proxy_read_timeout, expected_type=type_hints["proxy_read_timeout"])
            check_type(argname="argument pseudo_ipv4", value=pseudo_ipv4, expected_type=type_hints["pseudo_ipv4"])
            check_type(argname="argument response_buffering", value=response_buffering, expected_type=type_hints["response_buffering"])
            check_type(argname="argument rocket_loader", value=rocket_loader, expected_type=type_hints["rocket_loader"])
            check_type(argname="argument security_header", value=security_header, expected_type=type_hints["security_header"])
            check_type(argname="argument security_level", value=security_level, expected_type=type_hints["security_level"])
            check_type(argname="argument server_side_exclude", value=server_side_exclude, expected_type=type_hints["server_side_exclude"])
            check_type(argname="argument sort_query_string_for_cache", value=sort_query_string_for_cache, expected_type=type_hints["sort_query_string_for_cache"])
            check_type(argname="argument ssl", value=ssl, expected_type=type_hints["ssl"])
            check_type(argname="argument tls12_only", value=tls12_only, expected_type=type_hints["tls12_only"])
            check_type(argname="argument tls13", value=tls13, expected_type=type_hints["tls13"])
            check_type(argname="argument tls_client_auth", value=tls_client_auth, expected_type=type_hints["tls_client_auth"])
            check_type(argname="argument true_client_ip_header", value=true_client_ip_header, expected_type=type_hints["true_client_ip_header"])
            check_type(argname="argument universal_ssl", value=universal_ssl, expected_type=type_hints["universal_ssl"])
            check_type(argname="argument visitor_ip", value=visitor_ip, expected_type=type_hints["visitor_ip"])
            check_type(argname="argument waf", value=waf, expected_type=type_hints["waf"])
            check_type(argname="argument webp", value=webp, expected_type=type_hints["webp"])
            check_type(argname="argument websockets", value=websockets, expected_type=type_hints["websockets"])
            check_type(argname="argument zero_rtt", value=zero_rtt, expected_type=type_hints["zero_rtt"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if always_online is not None:
            self._values["always_online"] = always_online
        if always_use_https is not None:
            self._values["always_use_https"] = always_use_https
        if automatic_https_rewrites is not None:
            self._values["automatic_https_rewrites"] = automatic_https_rewrites
        if binary_ast is not None:
            self._values["binary_ast"] = binary_ast
        if brotli is not None:
            self._values["brotli"] = brotli
        if browser_cache_ttl is not None:
            self._values["browser_cache_ttl"] = browser_cache_ttl
        if browser_check is not None:
            self._values["browser_check"] = browser_check
        if cache_level is not None:
            self._values["cache_level"] = cache_level
        if challenge_ttl is not None:
            self._values["challenge_ttl"] = challenge_ttl
        if ciphers is not None:
            self._values["ciphers"] = ciphers
        if cname_flattening is not None:
            self._values["cname_flattening"] = cname_flattening
        if development_mode is not None:
            self._values["development_mode"] = development_mode
        if early_hints is not None:
            self._values["early_hints"] = early_hints
        if email_obfuscation is not None:
            self._values["email_obfuscation"] = email_obfuscation
        if filter_logs_to_cloudflare is not None:
            self._values["filter_logs_to_cloudflare"] = filter_logs_to_cloudflare
        if h2_prioritization is not None:
            self._values["h2_prioritization"] = h2_prioritization
        if hotlink_protection is not None:
            self._values["hotlink_protection"] = hotlink_protection
        if http2 is not None:
            self._values["http2"] = http2
        if http3 is not None:
            self._values["http3"] = http3
        if image_resizing is not None:
            self._values["image_resizing"] = image_resizing
        if ip_geolocation is not None:
            self._values["ip_geolocation"] = ip_geolocation
        if ipv6 is not None:
            self._values["ipv6"] = ipv6
        if log_to_cloudflare is not None:
            self._values["log_to_cloudflare"] = log_to_cloudflare
        if max_upload is not None:
            self._values["max_upload"] = max_upload
        if minify is not None:
            self._values["minify"] = minify
        if min_tls_version is not None:
            self._values["min_tls_version"] = min_tls_version
        if mirage is not None:
            self._values["mirage"] = mirage
        if mobile_redirect is not None:
            self._values["mobile_redirect"] = mobile_redirect
        if opportunistic_encryption is not None:
            self._values["opportunistic_encryption"] = opportunistic_encryption
        if opportunistic_onion is not None:
            self._values["opportunistic_onion"] = opportunistic_onion
        if orange_to_orange is not None:
            self._values["orange_to_orange"] = orange_to_orange
        if origin_error_page_pass_thru is not None:
            self._values["origin_error_page_pass_thru"] = origin_error_page_pass_thru
        if origin_max_http_version is not None:
            self._values["origin_max_http_version"] = origin_max_http_version
        if polish is not None:
            self._values["polish"] = polish
        if prefetch_preload is not None:
            self._values["prefetch_preload"] = prefetch_preload
        if privacy_pass is not None:
            self._values["privacy_pass"] = privacy_pass
        if proxy_read_timeout is not None:
            self._values["proxy_read_timeout"] = proxy_read_timeout
        if pseudo_ipv4 is not None:
            self._values["pseudo_ipv4"] = pseudo_ipv4
        if response_buffering is not None:
            self._values["response_buffering"] = response_buffering
        if rocket_loader is not None:
            self._values["rocket_loader"] = rocket_loader
        if security_header is not None:
            self._values["security_header"] = security_header
        if security_level is not None:
            self._values["security_level"] = security_level
        if server_side_exclude is not None:
            self._values["server_side_exclude"] = server_side_exclude
        if sort_query_string_for_cache is not None:
            self._values["sort_query_string_for_cache"] = sort_query_string_for_cache
        if ssl is not None:
            self._values["ssl"] = ssl
        if tls12_only is not None:
            self._values["tls12_only"] = tls12_only
        if tls13 is not None:
            self._values["tls13"] = tls13
        if tls_client_auth is not None:
            self._values["tls_client_auth"] = tls_client_auth
        if true_client_ip_header is not None:
            self._values["true_client_ip_header"] = true_client_ip_header
        if universal_ssl is not None:
            self._values["universal_ssl"] = universal_ssl
        if visitor_ip is not None:
            self._values["visitor_ip"] = visitor_ip
        if waf is not None:
            self._values["waf"] = waf
        if webp is not None:
            self._values["webp"] = webp
        if websockets is not None:
            self._values["websockets"] = websockets
        if zero_rtt is not None:
            self._values["zero_rtt"] = zero_rtt

    @builtins.property
    def always_online(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#always_online ZoneSettingsOverride#always_online}.'''
        result = self._values.get("always_online")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def always_use_https(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#always_use_https ZoneSettingsOverride#always_use_https}.'''
        result = self._values.get("always_use_https")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automatic_https_rewrites(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#automatic_https_rewrites ZoneSettingsOverride#automatic_https_rewrites}.'''
        result = self._values.get("automatic_https_rewrites")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_ast(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#binary_ast ZoneSettingsOverride#binary_ast}.'''
        result = self._values.get("binary_ast")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def brotli(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#brotli ZoneSettingsOverride#brotli}.'''
        result = self._values.get("brotli")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def browser_cache_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#browser_cache_ttl ZoneSettingsOverride#browser_cache_ttl}.'''
        result = self._values.get("browser_cache_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def browser_check(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#browser_check ZoneSettingsOverride#browser_check}.'''
        result = self._values.get("browser_check")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#cache_level ZoneSettingsOverride#cache_level}.'''
        result = self._values.get("cache_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def challenge_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#challenge_ttl ZoneSettingsOverride#challenge_ttl}.'''
        result = self._values.get("challenge_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ciphers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ciphers ZoneSettingsOverride#ciphers}.'''
        result = self._values.get("ciphers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cname_flattening(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#cname_flattening ZoneSettingsOverride#cname_flattening}.'''
        result = self._values.get("cname_flattening")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def development_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#development_mode ZoneSettingsOverride#development_mode}.'''
        result = self._values.get("development_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def early_hints(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#early_hints ZoneSettingsOverride#early_hints}.'''
        result = self._values.get("early_hints")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_obfuscation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#email_obfuscation ZoneSettingsOverride#email_obfuscation}.'''
        result = self._values.get("email_obfuscation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_logs_to_cloudflare(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#filter_logs_to_cloudflare ZoneSettingsOverride#filter_logs_to_cloudflare}.'''
        result = self._values.get("filter_logs_to_cloudflare")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def h2_prioritization(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#h2_prioritization ZoneSettingsOverride#h2_prioritization}.'''
        result = self._values.get("h2_prioritization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hotlink_protection(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#hotlink_protection ZoneSettingsOverride#hotlink_protection}.'''
        result = self._values.get("hotlink_protection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http2(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#http2 ZoneSettingsOverride#http2}.'''
        result = self._values.get("http2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http3(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#http3 ZoneSettingsOverride#http3}.'''
        result = self._values.get("http3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_resizing(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#image_resizing ZoneSettingsOverride#image_resizing}.'''
        result = self._values.get("image_resizing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_geolocation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ip_geolocation ZoneSettingsOverride#ip_geolocation}.'''
        result = self._values.get("ip_geolocation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ipv6 ZoneSettingsOverride#ipv6}.'''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_to_cloudflare(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#log_to_cloudflare ZoneSettingsOverride#log_to_cloudflare}.'''
        result = self._values.get("log_to_cloudflare")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_upload(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#max_upload ZoneSettingsOverride#max_upload}.'''
        result = self._values.get("max_upload")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minify(self) -> typing.Optional["ZoneSettingsOverrideSettingsMinify"]:
        '''minify block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#minify ZoneSettingsOverride#minify}
        '''
        result = self._values.get("minify")
        return typing.cast(typing.Optional["ZoneSettingsOverrideSettingsMinify"], result)

    @builtins.property
    def min_tls_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#min_tls_version ZoneSettingsOverride#min_tls_version}.'''
        result = self._values.get("min_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mirage(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#mirage ZoneSettingsOverride#mirage}.'''
        result = self._values.get("mirage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mobile_redirect(
        self,
    ) -> typing.Optional["ZoneSettingsOverrideSettingsMobileRedirect"]:
        '''mobile_redirect block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#mobile_redirect ZoneSettingsOverride#mobile_redirect}
        '''
        result = self._values.get("mobile_redirect")
        return typing.cast(typing.Optional["ZoneSettingsOverrideSettingsMobileRedirect"], result)

    @builtins.property
    def opportunistic_encryption(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#opportunistic_encryption ZoneSettingsOverride#opportunistic_encryption}.'''
        result = self._values.get("opportunistic_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def opportunistic_onion(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#opportunistic_onion ZoneSettingsOverride#opportunistic_onion}.'''
        result = self._values.get("opportunistic_onion")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def orange_to_orange(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#orange_to_orange ZoneSettingsOverride#orange_to_orange}.'''
        result = self._values.get("orange_to_orange")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_error_page_pass_thru(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#origin_error_page_pass_thru ZoneSettingsOverride#origin_error_page_pass_thru}.'''
        result = self._values.get("origin_error_page_pass_thru")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_max_http_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#origin_max_http_version ZoneSettingsOverride#origin_max_http_version}.'''
        result = self._values.get("origin_max_http_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def polish(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#polish ZoneSettingsOverride#polish}.'''
        result = self._values.get("polish")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefetch_preload(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#prefetch_preload ZoneSettingsOverride#prefetch_preload}.'''
        result = self._values.get("prefetch_preload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def privacy_pass(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#privacy_pass ZoneSettingsOverride#privacy_pass}.'''
        result = self._values.get("privacy_pass")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_read_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#proxy_read_timeout ZoneSettingsOverride#proxy_read_timeout}.'''
        result = self._values.get("proxy_read_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pseudo_ipv4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#pseudo_ipv4 ZoneSettingsOverride#pseudo_ipv4}.'''
        result = self._values.get("pseudo_ipv4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_buffering(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#response_buffering ZoneSettingsOverride#response_buffering}.'''
        result = self._values.get("response_buffering")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rocket_loader(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#rocket_loader ZoneSettingsOverride#rocket_loader}.'''
        result = self._values.get("rocket_loader")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_header(
        self,
    ) -> typing.Optional["ZoneSettingsOverrideSettingsSecurityHeader"]:
        '''security_header block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#security_header ZoneSettingsOverride#security_header}
        '''
        result = self._values.get("security_header")
        return typing.cast(typing.Optional["ZoneSettingsOverrideSettingsSecurityHeader"], result)

    @builtins.property
    def security_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#security_level ZoneSettingsOverride#security_level}.'''
        result = self._values.get("security_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_exclude(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#server_side_exclude ZoneSettingsOverride#server_side_exclude}.'''
        result = self._values.get("server_side_exclude")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort_query_string_for_cache(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#sort_query_string_for_cache ZoneSettingsOverride#sort_query_string_for_cache}.'''
        result = self._values.get("sort_query_string_for_cache")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#ssl ZoneSettingsOverride#ssl}.'''
        result = self._values.get("ssl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls12_only(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#tls_1_2_only ZoneSettingsOverride#tls_1_2_only}.'''
        result = self._values.get("tls12_only")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls13(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#tls_1_3 ZoneSettingsOverride#tls_1_3}.'''
        result = self._values.get("tls13")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_client_auth(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#tls_client_auth ZoneSettingsOverride#tls_client_auth}.'''
        result = self._values.get("tls_client_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def true_client_ip_header(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#true_client_ip_header ZoneSettingsOverride#true_client_ip_header}.'''
        result = self._values.get("true_client_ip_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def universal_ssl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#universal_ssl ZoneSettingsOverride#universal_ssl}.'''
        result = self._values.get("universal_ssl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visitor_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#visitor_ip ZoneSettingsOverride#visitor_ip}.'''
        result = self._values.get("visitor_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def waf(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#waf ZoneSettingsOverride#waf}.'''
        result = self._values.get("waf")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#webp ZoneSettingsOverride#webp}.'''
        result = self._values.get("webp")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def websockets(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#websockets ZoneSettingsOverride#websockets}.'''
        result = self._values.get("websockets")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zero_rtt(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#zero_rtt ZoneSettingsOverride#zero_rtt}.'''
        result = self._values.get("zero_rtt")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneSettingsOverrideSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideSettingsMinify",
    jsii_struct_bases=[],
    name_mapping={"css": "css", "html": "html", "js": "js"},
)
class ZoneSettingsOverrideSettingsMinify:
    def __init__(
        self,
        *,
        css: builtins.str,
        html: builtins.str,
        js: builtins.str,
    ) -> None:
        '''
        :param css: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#css ZoneSettingsOverride#css}.
        :param html: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#html ZoneSettingsOverride#html}.
        :param js: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#js ZoneSettingsOverride#js}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0550b681c744a96b12f003b698673d43bbdb7bbedfcfbe3f2f4266c3f051fe)
            check_type(argname="argument css", value=css, expected_type=type_hints["css"])
            check_type(argname="argument html", value=html, expected_type=type_hints["html"])
            check_type(argname="argument js", value=js, expected_type=type_hints["js"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "css": css,
            "html": html,
            "js": js,
        }

    @builtins.property
    def css(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#css ZoneSettingsOverride#css}.'''
        result = self._values.get("css")
        assert result is not None, "Required property 'css' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def html(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#html ZoneSettingsOverride#html}.'''
        result = self._values.get("html")
        assert result is not None, "Required property 'html' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def js(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#js ZoneSettingsOverride#js}.'''
        result = self._values.get("js")
        assert result is not None, "Required property 'js' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneSettingsOverrideSettingsMinify(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZoneSettingsOverrideSettingsMinifyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideSettingsMinifyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3de227cf63aa5c0429da46a86995b52d7cb26582d2e6a2e190b030a8f688db7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cssInput")
    def css_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cssInput"))

    @builtins.property
    @jsii.member(jsii_name="htmlInput")
    def html_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "htmlInput"))

    @builtins.property
    @jsii.member(jsii_name="jsInput")
    def js_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsInput"))

    @builtins.property
    @jsii.member(jsii_name="css")
    def css(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "css"))

    @css.setter
    def css(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfcf58f1ce4e92017ea77ea312c8af5e5a08a1c72d95b4f7a8f67cd6cadd873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "css", value)

    @builtins.property
    @jsii.member(jsii_name="html")
    def html(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "html"))

    @html.setter
    def html(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368149c638da8c149a1456bb0272806634daa55fd21b5f7c85b068bf3640256f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "html", value)

    @builtins.property
    @jsii.member(jsii_name="js")
    def js(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "js"))

    @js.setter
    def js(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d7b3fd85408e62986f4859e3bb2d2a2d31d68640fec4a1d112a56c648926ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "js", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZoneSettingsOverrideSettingsMinify]:
        return typing.cast(typing.Optional[ZoneSettingsOverrideSettingsMinify], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZoneSettingsOverrideSettingsMinify],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63baca054ad4577774a83376f9967468da472ae4348bde0e8babe50d1b9a4a7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideSettingsMobileRedirect",
    jsii_struct_bases=[],
    name_mapping={
        "mobile_subdomain": "mobileSubdomain",
        "status": "status",
        "strip_uri": "stripUri",
    },
)
class ZoneSettingsOverrideSettingsMobileRedirect:
    def __init__(
        self,
        *,
        mobile_subdomain: builtins.str,
        status: builtins.str,
        strip_uri: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param mobile_subdomain: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#mobile_subdomain ZoneSettingsOverride#mobile_subdomain}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#status ZoneSettingsOverride#status}.
        :param strip_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#strip_uri ZoneSettingsOverride#strip_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__461a93c655947e4d5a1d714ce53d00ad33a9a5ddaed83bf776ed1246f0ce5eb3)
            check_type(argname="argument mobile_subdomain", value=mobile_subdomain, expected_type=type_hints["mobile_subdomain"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument strip_uri", value=strip_uri, expected_type=type_hints["strip_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mobile_subdomain": mobile_subdomain,
            "status": status,
            "strip_uri": strip_uri,
        }

    @builtins.property
    def mobile_subdomain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#mobile_subdomain ZoneSettingsOverride#mobile_subdomain}.'''
        result = self._values.get("mobile_subdomain")
        assert result is not None, "Required property 'mobile_subdomain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#status ZoneSettingsOverride#status}.'''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def strip_uri(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#strip_uri ZoneSettingsOverride#strip_uri}.'''
        result = self._values.get("strip_uri")
        assert result is not None, "Required property 'strip_uri' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneSettingsOverrideSettingsMobileRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZoneSettingsOverrideSettingsMobileRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideSettingsMobileRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__172f040b1cf49bbf74b6a6126a3f1c230a4cde737f6f9b5da59d1060ba4f5bcc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="mobileSubdomainInput")
    def mobile_subdomain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mobileSubdomainInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="stripUriInput")
    def strip_uri_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stripUriInput"))

    @builtins.property
    @jsii.member(jsii_name="mobileSubdomain")
    def mobile_subdomain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobileSubdomain"))

    @mobile_subdomain.setter
    def mobile_subdomain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2f2bd63b3beafcf7648da3b6404851fb0228548488d81f2ab650970ca7e448)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobileSubdomain", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9beb8933d006650dd30421ba595f199f7c797ae8b8bb0e608f71f21bf4e5a060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="stripUri")
    def strip_uri(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stripUri"))

    @strip_uri.setter
    def strip_uri(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cfdd3e1368590ee6a9c0b31d102fa51fa8c1cefc0397bfca5e3a849450ee40c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stripUri", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZoneSettingsOverrideSettingsMobileRedirect]:
        return typing.cast(typing.Optional[ZoneSettingsOverrideSettingsMobileRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZoneSettingsOverrideSettingsMobileRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c205307d441da8cbadacc11f077c226662ea86815557e218b1f970ba1127a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ZoneSettingsOverrideSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27f583bec6b045d6b82e435e739d30238299ec942448fd53042ed9daed24f380)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMinify")
    def put_minify(
        self,
        *,
        css: builtins.str,
        html: builtins.str,
        js: builtins.str,
    ) -> None:
        '''
        :param css: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#css ZoneSettingsOverride#css}.
        :param html: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#html ZoneSettingsOverride#html}.
        :param js: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#js ZoneSettingsOverride#js}.
        '''
        value = ZoneSettingsOverrideSettingsMinify(css=css, html=html, js=js)

        return typing.cast(None, jsii.invoke(self, "putMinify", [value]))

    @jsii.member(jsii_name="putMobileRedirect")
    def put_mobile_redirect(
        self,
        *,
        mobile_subdomain: builtins.str,
        status: builtins.str,
        strip_uri: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param mobile_subdomain: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#mobile_subdomain ZoneSettingsOverride#mobile_subdomain}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#status ZoneSettingsOverride#status}.
        :param strip_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#strip_uri ZoneSettingsOverride#strip_uri}.
        '''
        value = ZoneSettingsOverrideSettingsMobileRedirect(
            mobile_subdomain=mobile_subdomain, status=status, strip_uri=strip_uri
        )

        return typing.cast(None, jsii.invoke(self, "putMobileRedirect", [value]))

    @jsii.member(jsii_name="putSecurityHeader")
    def put_security_header(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_age: typing.Optional[jsii.Number] = None,
        nosniff: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#enabled ZoneSettingsOverride#enabled}.
        :param include_subdomains: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#include_subdomains ZoneSettingsOverride#include_subdomains}.
        :param max_age: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#max_age ZoneSettingsOverride#max_age}.
        :param nosniff: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#nosniff ZoneSettingsOverride#nosniff}.
        :param preload: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#preload ZoneSettingsOverride#preload}.
        '''
        value = ZoneSettingsOverrideSettingsSecurityHeader(
            enabled=enabled,
            include_subdomains=include_subdomains,
            max_age=max_age,
            nosniff=nosniff,
            preload=preload,
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityHeader", [value]))

    @jsii.member(jsii_name="resetAlwaysOnline")
    def reset_always_online(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlwaysOnline", []))

    @jsii.member(jsii_name="resetAlwaysUseHttps")
    def reset_always_use_https(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlwaysUseHttps", []))

    @jsii.member(jsii_name="resetAutomaticHttpsRewrites")
    def reset_automatic_https_rewrites(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticHttpsRewrites", []))

    @jsii.member(jsii_name="resetBinaryAst")
    def reset_binary_ast(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryAst", []))

    @jsii.member(jsii_name="resetBrotli")
    def reset_brotli(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrotli", []))

    @jsii.member(jsii_name="resetBrowserCacheTtl")
    def reset_browser_cache_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrowserCacheTtl", []))

    @jsii.member(jsii_name="resetBrowserCheck")
    def reset_browser_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrowserCheck", []))

    @jsii.member(jsii_name="resetCacheLevel")
    def reset_cache_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheLevel", []))

    @jsii.member(jsii_name="resetChallengeTtl")
    def reset_challenge_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChallengeTtl", []))

    @jsii.member(jsii_name="resetCiphers")
    def reset_ciphers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCiphers", []))

    @jsii.member(jsii_name="resetCnameFlattening")
    def reset_cname_flattening(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCnameFlattening", []))

    @jsii.member(jsii_name="resetDevelopmentMode")
    def reset_development_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevelopmentMode", []))

    @jsii.member(jsii_name="resetEarlyHints")
    def reset_early_hints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEarlyHints", []))

    @jsii.member(jsii_name="resetEmailObfuscation")
    def reset_email_obfuscation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailObfuscation", []))

    @jsii.member(jsii_name="resetFilterLogsToCloudflare")
    def reset_filter_logs_to_cloudflare(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterLogsToCloudflare", []))

    @jsii.member(jsii_name="resetH2Prioritization")
    def reset_h2_prioritization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetH2Prioritization", []))

    @jsii.member(jsii_name="resetHotlinkProtection")
    def reset_hotlink_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHotlinkProtection", []))

    @jsii.member(jsii_name="resetHttp2")
    def reset_http2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2", []))

    @jsii.member(jsii_name="resetHttp3")
    def reset_http3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp3", []))

    @jsii.member(jsii_name="resetImageResizing")
    def reset_image_resizing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageResizing", []))

    @jsii.member(jsii_name="resetIpGeolocation")
    def reset_ip_geolocation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpGeolocation", []))

    @jsii.member(jsii_name="resetIpv6")
    def reset_ipv6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6", []))

    @jsii.member(jsii_name="resetLogToCloudflare")
    def reset_log_to_cloudflare(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogToCloudflare", []))

    @jsii.member(jsii_name="resetMaxUpload")
    def reset_max_upload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUpload", []))

    @jsii.member(jsii_name="resetMinify")
    def reset_minify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinify", []))

    @jsii.member(jsii_name="resetMinTlsVersion")
    def reset_min_tls_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTlsVersion", []))

    @jsii.member(jsii_name="resetMirage")
    def reset_mirage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMirage", []))

    @jsii.member(jsii_name="resetMobileRedirect")
    def reset_mobile_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMobileRedirect", []))

    @jsii.member(jsii_name="resetOpportunisticEncryption")
    def reset_opportunistic_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpportunisticEncryption", []))

    @jsii.member(jsii_name="resetOpportunisticOnion")
    def reset_opportunistic_onion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpportunisticOnion", []))

    @jsii.member(jsii_name="resetOrangeToOrange")
    def reset_orange_to_orange(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrangeToOrange", []))

    @jsii.member(jsii_name="resetOriginErrorPagePassThru")
    def reset_origin_error_page_pass_thru(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginErrorPagePassThru", []))

    @jsii.member(jsii_name="resetOriginMaxHttpVersion")
    def reset_origin_max_http_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginMaxHttpVersion", []))

    @jsii.member(jsii_name="resetPolish")
    def reset_polish(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolish", []))

    @jsii.member(jsii_name="resetPrefetchPreload")
    def reset_prefetch_preload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefetchPreload", []))

    @jsii.member(jsii_name="resetPrivacyPass")
    def reset_privacy_pass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivacyPass", []))

    @jsii.member(jsii_name="resetProxyReadTimeout")
    def reset_proxy_read_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyReadTimeout", []))

    @jsii.member(jsii_name="resetPseudoIpv4")
    def reset_pseudo_ipv4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPseudoIpv4", []))

    @jsii.member(jsii_name="resetResponseBuffering")
    def reset_response_buffering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseBuffering", []))

    @jsii.member(jsii_name="resetRocketLoader")
    def reset_rocket_loader(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRocketLoader", []))

    @jsii.member(jsii_name="resetSecurityHeader")
    def reset_security_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityHeader", []))

    @jsii.member(jsii_name="resetSecurityLevel")
    def reset_security_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityLevel", []))

    @jsii.member(jsii_name="resetServerSideExclude")
    def reset_server_side_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerSideExclude", []))

    @jsii.member(jsii_name="resetSortQueryStringForCache")
    def reset_sort_query_string_for_cache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSortQueryStringForCache", []))

    @jsii.member(jsii_name="resetSsl")
    def reset_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsl", []))

    @jsii.member(jsii_name="resetTls12Only")
    def reset_tls12_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls12Only", []))

    @jsii.member(jsii_name="resetTls13")
    def reset_tls13(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls13", []))

    @jsii.member(jsii_name="resetTlsClientAuth")
    def reset_tls_client_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsClientAuth", []))

    @jsii.member(jsii_name="resetTrueClientIpHeader")
    def reset_true_client_ip_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrueClientIpHeader", []))

    @jsii.member(jsii_name="resetUniversalSsl")
    def reset_universal_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniversalSsl", []))

    @jsii.member(jsii_name="resetVisitorIp")
    def reset_visitor_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisitorIp", []))

    @jsii.member(jsii_name="resetWaf")
    def reset_waf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaf", []))

    @jsii.member(jsii_name="resetWebp")
    def reset_webp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebp", []))

    @jsii.member(jsii_name="resetWebsockets")
    def reset_websockets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebsockets", []))

    @jsii.member(jsii_name="resetZeroRtt")
    def reset_zero_rtt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZeroRtt", []))

    @builtins.property
    @jsii.member(jsii_name="minify")
    def minify(self) -> ZoneSettingsOverrideSettingsMinifyOutputReference:
        return typing.cast(ZoneSettingsOverrideSettingsMinifyOutputReference, jsii.get(self, "minify"))

    @builtins.property
    @jsii.member(jsii_name="mobileRedirect")
    def mobile_redirect(
        self,
    ) -> ZoneSettingsOverrideSettingsMobileRedirectOutputReference:
        return typing.cast(ZoneSettingsOverrideSettingsMobileRedirectOutputReference, jsii.get(self, "mobileRedirect"))

    @builtins.property
    @jsii.member(jsii_name="securityHeader")
    def security_header(
        self,
    ) -> "ZoneSettingsOverrideSettingsSecurityHeaderOutputReference":
        return typing.cast("ZoneSettingsOverrideSettingsSecurityHeaderOutputReference", jsii.get(self, "securityHeader"))

    @builtins.property
    @jsii.member(jsii_name="alwaysOnlineInput")
    def always_online_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alwaysOnlineInput"))

    @builtins.property
    @jsii.member(jsii_name="alwaysUseHttpsInput")
    def always_use_https_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alwaysUseHttpsInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticHttpsRewritesInput")
    def automatic_https_rewrites_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "automaticHttpsRewritesInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryAstInput")
    def binary_ast_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "binaryAstInput"))

    @builtins.property
    @jsii.member(jsii_name="brotliInput")
    def brotli_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "brotliInput"))

    @builtins.property
    @jsii.member(jsii_name="browserCacheTtlInput")
    def browser_cache_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "browserCacheTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="browserCheckInput")
    def browser_check_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "browserCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheLevelInput")
    def cache_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="challengeTtlInput")
    def challenge_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "challengeTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="ciphersInput")
    def ciphers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ciphersInput"))

    @builtins.property
    @jsii.member(jsii_name="cnameFlatteningInput")
    def cname_flattening_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cnameFlatteningInput"))

    @builtins.property
    @jsii.member(jsii_name="developmentModeInput")
    def development_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "developmentModeInput"))

    @builtins.property
    @jsii.member(jsii_name="earlyHintsInput")
    def early_hints_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "earlyHintsInput"))

    @builtins.property
    @jsii.member(jsii_name="emailObfuscationInput")
    def email_obfuscation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailObfuscationInput"))

    @builtins.property
    @jsii.member(jsii_name="filterLogsToCloudflareInput")
    def filter_logs_to_cloudflare_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterLogsToCloudflareInput"))

    @builtins.property
    @jsii.member(jsii_name="h2PrioritizationInput")
    def h2_prioritization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "h2PrioritizationInput"))

    @builtins.property
    @jsii.member(jsii_name="hotlinkProtectionInput")
    def hotlink_protection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hotlinkProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="http2Input")
    def http2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "http2Input"))

    @builtins.property
    @jsii.member(jsii_name="http3Input")
    def http3_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "http3Input"))

    @builtins.property
    @jsii.member(jsii_name="imageResizingInput")
    def image_resizing_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageResizingInput"))

    @builtins.property
    @jsii.member(jsii_name="ipGeolocationInput")
    def ip_geolocation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipGeolocationInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Input")
    def ipv6_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6Input"))

    @builtins.property
    @jsii.member(jsii_name="logToCloudflareInput")
    def log_to_cloudflare_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logToCloudflareInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUploadInput")
    def max_upload_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUploadInput"))

    @builtins.property
    @jsii.member(jsii_name="minifyInput")
    def minify_input(self) -> typing.Optional[ZoneSettingsOverrideSettingsMinify]:
        return typing.cast(typing.Optional[ZoneSettingsOverrideSettingsMinify], jsii.get(self, "minifyInput"))

    @builtins.property
    @jsii.member(jsii_name="minTlsVersionInput")
    def min_tls_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minTlsVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="mirageInput")
    def mirage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mirageInput"))

    @builtins.property
    @jsii.member(jsii_name="mobileRedirectInput")
    def mobile_redirect_input(
        self,
    ) -> typing.Optional[ZoneSettingsOverrideSettingsMobileRedirect]:
        return typing.cast(typing.Optional[ZoneSettingsOverrideSettingsMobileRedirect], jsii.get(self, "mobileRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="opportunisticEncryptionInput")
    def opportunistic_encryption_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "opportunisticEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="opportunisticOnionInput")
    def opportunistic_onion_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "opportunisticOnionInput"))

    @builtins.property
    @jsii.member(jsii_name="orangeToOrangeInput")
    def orange_to_orange_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orangeToOrangeInput"))

    @builtins.property
    @jsii.member(jsii_name="originErrorPagePassThruInput")
    def origin_error_page_pass_thru_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originErrorPagePassThruInput"))

    @builtins.property
    @jsii.member(jsii_name="originMaxHttpVersionInput")
    def origin_max_http_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originMaxHttpVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="polishInput")
    def polish_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "polishInput"))

    @builtins.property
    @jsii.member(jsii_name="prefetchPreloadInput")
    def prefetch_preload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefetchPreloadInput"))

    @builtins.property
    @jsii.member(jsii_name="privacyPassInput")
    def privacy_pass_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privacyPassInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyReadTimeoutInput")
    def proxy_read_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyReadTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="pseudoIpv4Input")
    def pseudo_ipv4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pseudoIpv4Input"))

    @builtins.property
    @jsii.member(jsii_name="responseBufferingInput")
    def response_buffering_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseBufferingInput"))

    @builtins.property
    @jsii.member(jsii_name="rocketLoaderInput")
    def rocket_loader_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rocketLoaderInput"))

    @builtins.property
    @jsii.member(jsii_name="securityHeaderInput")
    def security_header_input(
        self,
    ) -> typing.Optional["ZoneSettingsOverrideSettingsSecurityHeader"]:
        return typing.cast(typing.Optional["ZoneSettingsOverrideSettingsSecurityHeader"], jsii.get(self, "securityHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="securityLevelInput")
    def security_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="serverSideExcludeInput")
    def server_side_exclude_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverSideExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="sortQueryStringForCacheInput")
    def sort_query_string_for_cache_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortQueryStringForCacheInput"))

    @builtins.property
    @jsii.member(jsii_name="sslInput")
    def ssl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslInput"))

    @builtins.property
    @jsii.member(jsii_name="tls12OnlyInput")
    def tls12_only_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tls12OnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="tls13Input")
    def tls13_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tls13Input"))

    @builtins.property
    @jsii.member(jsii_name="tlsClientAuthInput")
    def tls_client_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsClientAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="trueClientIpHeaderInput")
    def true_client_ip_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trueClientIpHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="universalSslInput")
    def universal_ssl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "universalSslInput"))

    @builtins.property
    @jsii.member(jsii_name="visitorIpInput")
    def visitor_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visitorIpInput"))

    @builtins.property
    @jsii.member(jsii_name="wafInput")
    def waf_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "wafInput"))

    @builtins.property
    @jsii.member(jsii_name="webpInput")
    def webp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webpInput"))

    @builtins.property
    @jsii.member(jsii_name="websocketsInput")
    def websockets_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "websocketsInput"))

    @builtins.property
    @jsii.member(jsii_name="zeroRttInput")
    def zero_rtt_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zeroRttInput"))

    @builtins.property
    @jsii.member(jsii_name="alwaysOnline")
    def always_online(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alwaysOnline"))

    @always_online.setter
    def always_online(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178b0817d8340cc2ccc897361f0e7c3b29edd827f7ca5ca7a005b4c688cca065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysOnline", value)

    @builtins.property
    @jsii.member(jsii_name="alwaysUseHttps")
    def always_use_https(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alwaysUseHttps"))

    @always_use_https.setter
    def always_use_https(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb017378eaacd5f50e2af6acc296fce63e6f8f7507cd023f0e28d49452c8270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysUseHttps", value)

    @builtins.property
    @jsii.member(jsii_name="automaticHttpsRewrites")
    def automatic_https_rewrites(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "automaticHttpsRewrites"))

    @automatic_https_rewrites.setter
    def automatic_https_rewrites(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97275e879309815c97d229a088ead98ac0fd1de6b3c0891bdea9891c0458d44f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticHttpsRewrites", value)

    @builtins.property
    @jsii.member(jsii_name="binaryAst")
    def binary_ast(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryAst"))

    @binary_ast.setter
    def binary_ast(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5a54b555a06718df0dc7e655c3a82d0960bf04852e1ed0f431d13d59bddf2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryAst", value)

    @builtins.property
    @jsii.member(jsii_name="brotli")
    def brotli(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "brotli"))

    @brotli.setter
    def brotli(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__708b806be1daba1cf6337c4f9fc1ed99efc667251840c8cce8b3afba8ba526c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "brotli", value)

    @builtins.property
    @jsii.member(jsii_name="browserCacheTtl")
    def browser_cache_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "browserCacheTtl"))

    @browser_cache_ttl.setter
    def browser_cache_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02336c296fdd0b11bf02eac2221923d0aa38b75c888d3c8b209a2d283e14a82c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "browserCacheTtl", value)

    @builtins.property
    @jsii.member(jsii_name="browserCheck")
    def browser_check(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "browserCheck"))

    @browser_check.setter
    def browser_check(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5dc4ae60f2aca66669f2924745c827f8211bdc3808b4b27b1d1763974a5b9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "browserCheck", value)

    @builtins.property
    @jsii.member(jsii_name="cacheLevel")
    def cache_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheLevel"))

    @cache_level.setter
    def cache_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eed5dc74407d87c939b17cbda6199f8f6fb2ecf888d6385af68de965d0e969f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheLevel", value)

    @builtins.property
    @jsii.member(jsii_name="challengeTtl")
    def challenge_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "challengeTtl"))

    @challenge_ttl.setter
    def challenge_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c2db5e0b593b123e2e73aaf18fefe91a9ac38cee184368f892d2ede72bd92cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "challengeTtl", value)

    @builtins.property
    @jsii.member(jsii_name="ciphers")
    def ciphers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ciphers"))

    @ciphers.setter
    def ciphers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5824de6be9d8ffed4727c61e06cf05dec649746bb117bc3c9d4902002528b736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ciphers", value)

    @builtins.property
    @jsii.member(jsii_name="cnameFlattening")
    def cname_flattening(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cnameFlattening"))

    @cname_flattening.setter
    def cname_flattening(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa51957b0c0401498061acd4ec51105dc8d9346dd45c1d2681bd5202e383fa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cnameFlattening", value)

    @builtins.property
    @jsii.member(jsii_name="developmentMode")
    def development_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "developmentMode"))

    @development_mode.setter
    def development_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e799815dead9a81f8b3476e222e38b14c5585ceadff3a4383aff5763fac091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developmentMode", value)

    @builtins.property
    @jsii.member(jsii_name="earlyHints")
    def early_hints(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "earlyHints"))

    @early_hints.setter
    def early_hints(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc6905f432003c92e5d77d6aedc73bfbd69937fc167dde4add0d7b9054fe572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "earlyHints", value)

    @builtins.property
    @jsii.member(jsii_name="emailObfuscation")
    def email_obfuscation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailObfuscation"))

    @email_obfuscation.setter
    def email_obfuscation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40e36ff85839d1a4a06f4ceba02fed650134a6dc2f4b88c03e095f645c76a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailObfuscation", value)

    @builtins.property
    @jsii.member(jsii_name="filterLogsToCloudflare")
    def filter_logs_to_cloudflare(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterLogsToCloudflare"))

    @filter_logs_to_cloudflare.setter
    def filter_logs_to_cloudflare(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4e949073d14ce3595c660b1d5dccddb365e461c779764fccb327eee1864c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterLogsToCloudflare", value)

    @builtins.property
    @jsii.member(jsii_name="h2Prioritization")
    def h2_prioritization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "h2Prioritization"))

    @h2_prioritization.setter
    def h2_prioritization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1eca2bb9fe73623bed2102dd8392536c8757e87da0381f0f2387219b4bbef20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "h2Prioritization", value)

    @builtins.property
    @jsii.member(jsii_name="hotlinkProtection")
    def hotlink_protection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hotlinkProtection"))

    @hotlink_protection.setter
    def hotlink_protection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb56a359fe89cdf28f40693ce44ab103c9c6a600103aee2e89cced1fb687d089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hotlinkProtection", value)

    @builtins.property
    @jsii.member(jsii_name="http2")
    def http2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "http2"))

    @http2.setter
    def http2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bcef4ec36a6148efafdd3a93b014b06b4372a3875e937840a6f47e4c8a9da8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "http2", value)

    @builtins.property
    @jsii.member(jsii_name="http3")
    def http3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "http3"))

    @http3.setter
    def http3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8289ece65f7370fb653a45b301939d07390cd297bccf15710a82aa9790635aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "http3", value)

    @builtins.property
    @jsii.member(jsii_name="imageResizing")
    def image_resizing(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageResizing"))

    @image_resizing.setter
    def image_resizing(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10552b56fddb294067344bb5dcb673b324d565fc83333c46d0443b8ecbbb1c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageResizing", value)

    @builtins.property
    @jsii.member(jsii_name="ipGeolocation")
    def ip_geolocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipGeolocation"))

    @ip_geolocation.setter
    def ip_geolocation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d94a2a0423b9733a9a7f4df9e58f502c67873722ad592cc6deb1b85170d3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipGeolocation", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6"))

    @ipv6.setter
    def ipv6(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c472caf7aa28f9118fc252085e7e4fba8ee56b4a9bcc7536608e1fce67318f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6", value)

    @builtins.property
    @jsii.member(jsii_name="logToCloudflare")
    def log_to_cloudflare(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logToCloudflare"))

    @log_to_cloudflare.setter
    def log_to_cloudflare(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f992cb4baa56c40b066100a35a1224b8f638e6da4ac1b3a9aed2ccb6a397047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logToCloudflare", value)

    @builtins.property
    @jsii.member(jsii_name="maxUpload")
    def max_upload(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUpload"))

    @max_upload.setter
    def max_upload(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37603ca2b27a2dd5f2d7d408b3e3d16bccbb98b065672eba58bf3edadf156ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUpload", value)

    @builtins.property
    @jsii.member(jsii_name="minTlsVersion")
    def min_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minTlsVersion"))

    @min_tls_version.setter
    def min_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46bf8142ca948d8a51b5b8970e6a7986e7c2febd8761c103a06eb2ec1fce7741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTlsVersion", value)

    @builtins.property
    @jsii.member(jsii_name="mirage")
    def mirage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mirage"))

    @mirage.setter
    def mirage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43084affddec7b1a91909f59cbc662fc335257761cecb4ae35589e8726e77e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirage", value)

    @builtins.property
    @jsii.member(jsii_name="opportunisticEncryption")
    def opportunistic_encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "opportunisticEncryption"))

    @opportunistic_encryption.setter
    def opportunistic_encryption(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0bf48a86b240d4d5ba31cc3ac86f66297d12080eb72f3f4e235bc1dab2a23a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "opportunisticEncryption", value)

    @builtins.property
    @jsii.member(jsii_name="opportunisticOnion")
    def opportunistic_onion(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "opportunisticOnion"))

    @opportunistic_onion.setter
    def opportunistic_onion(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa4d44082417e62abed860c6fffc6295bedf7c6c9a120787af1e7a2398599f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "opportunisticOnion", value)

    @builtins.property
    @jsii.member(jsii_name="orangeToOrange")
    def orange_to_orange(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orangeToOrange"))

    @orange_to_orange.setter
    def orange_to_orange(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6203b15b06780711a6fe08451c971cbac89dbc276ea8e7f7f2cb7481a093930c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orangeToOrange", value)

    @builtins.property
    @jsii.member(jsii_name="originErrorPagePassThru")
    def origin_error_page_pass_thru(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originErrorPagePassThru"))

    @origin_error_page_pass_thru.setter
    def origin_error_page_pass_thru(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5964858f6a8acd7b9d594334505a479c364a0c722bee0e53af9b0c831a1fc61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originErrorPagePassThru", value)

    @builtins.property
    @jsii.member(jsii_name="originMaxHttpVersion")
    def origin_max_http_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originMaxHttpVersion"))

    @origin_max_http_version.setter
    def origin_max_http_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6700984e6509d62a8ec65740644cf2b4fbfd516839525c4ffd0d8bce2e145cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originMaxHttpVersion", value)

    @builtins.property
    @jsii.member(jsii_name="polish")
    def polish(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "polish"))

    @polish.setter
    def polish(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed619f88bbd2c75e78b1eef9ba6e701d88f5d4c4a1eafa90ee7b4ad7d8a5554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "polish", value)

    @builtins.property
    @jsii.member(jsii_name="prefetchPreload")
    def prefetch_preload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefetchPreload"))

    @prefetch_preload.setter
    def prefetch_preload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f3c6fb6d1dcd31b8aa9d0214ca0c95c8ef2edcc9749d8d367f6fc6a203dbfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefetchPreload", value)

    @builtins.property
    @jsii.member(jsii_name="privacyPass")
    def privacy_pass(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privacyPass"))

    @privacy_pass.setter
    def privacy_pass(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f7fb4eb55e4fc0a52bf771a682efccebbb66c5ec84138abf3714f803e68fb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privacyPass", value)

    @builtins.property
    @jsii.member(jsii_name="proxyReadTimeout")
    def proxy_read_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyReadTimeout"))

    @proxy_read_timeout.setter
    def proxy_read_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b633b1b6fcb9215a595c9cd2f877bbf07456188ec49c2883f44bb50bef7cb42d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyReadTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="pseudoIpv4")
    def pseudo_ipv4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pseudoIpv4"))

    @pseudo_ipv4.setter
    def pseudo_ipv4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813aaa38999ad92002f36ad2cd8374ae316066f9091752bd0c3002807b84027e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pseudoIpv4", value)

    @builtins.property
    @jsii.member(jsii_name="responseBuffering")
    def response_buffering(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseBuffering"))

    @response_buffering.setter
    def response_buffering(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d6260bcb26bbb98768a3bd6b8d89742d43c2bf8e367a25306aa3dbf6011e7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseBuffering", value)

    @builtins.property
    @jsii.member(jsii_name="rocketLoader")
    def rocket_loader(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rocketLoader"))

    @rocket_loader.setter
    def rocket_loader(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d266b80877d645697fadca35de85cc0a81d9bd27c3d32706343c1008d6807e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rocketLoader", value)

    @builtins.property
    @jsii.member(jsii_name="securityLevel")
    def security_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityLevel"))

    @security_level.setter
    def security_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e97ad07535b85e265ab3e831a0b23e6f3aa83f905acf5324f5481eead059c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityLevel", value)

    @builtins.property
    @jsii.member(jsii_name="serverSideExclude")
    def server_side_exclude(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverSideExclude"))

    @server_side_exclude.setter
    def server_side_exclude(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c732884c1f450ea81231872396890cce77ee6aa8a9c0adcf05662fcabe5243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverSideExclude", value)

    @builtins.property
    @jsii.member(jsii_name="sortQueryStringForCache")
    def sort_query_string_for_cache(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sortQueryStringForCache"))

    @sort_query_string_for_cache.setter
    def sort_query_string_for_cache(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901984c0f3a328d7a09ce0ef6a414e571864465546f6d2c00e1323812dcbb047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sortQueryStringForCache", value)

    @builtins.property
    @jsii.member(jsii_name="ssl")
    def ssl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssl"))

    @ssl.setter
    def ssl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e764764eade0efd634d5929d9f9d11c37e1ea9bff7158fb43319bd98fd4e8cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssl", value)

    @builtins.property
    @jsii.member(jsii_name="tls12Only")
    def tls12_only(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tls12Only"))

    @tls12_only.setter
    def tls12_only(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b84d16a85e212fe4d811535eab99afc4b151ef644c8f216f41d3fa5be66caaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls12Only", value)

    @builtins.property
    @jsii.member(jsii_name="tls13")
    def tls13(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tls13"))

    @tls13.setter
    def tls13(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e1138bf8afadbfa4a116adb9e10e2b71f119b56386726a0311c2f6695128f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls13", value)

    @builtins.property
    @jsii.member(jsii_name="tlsClientAuth")
    def tls_client_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsClientAuth"))

    @tls_client_auth.setter
    def tls_client_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b67955c91418592dbff5b50075d10c47aa615a9458ae91beaec8117ddf3859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsClientAuth", value)

    @builtins.property
    @jsii.member(jsii_name="trueClientIpHeader")
    def true_client_ip_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trueClientIpHeader"))

    @true_client_ip_header.setter
    def true_client_ip_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee3020cce66c605ff81d3de9b4b630fa2af6b85d3bdf7cc31010cdb662438dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trueClientIpHeader", value)

    @builtins.property
    @jsii.member(jsii_name="universalSsl")
    def universal_ssl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "universalSsl"))

    @universal_ssl.setter
    def universal_ssl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a0091f5ec66baca77ce1460977c29a67f199812731de7c0720d1c75c65f2d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "universalSsl", value)

    @builtins.property
    @jsii.member(jsii_name="visitorIp")
    def visitor_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visitorIp"))

    @visitor_ip.setter
    def visitor_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb90ccd5c88289d9ea0308ac4702d57b2abd50195fc58bdea65836c70d3fe312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visitorIp", value)

    @builtins.property
    @jsii.member(jsii_name="waf")
    def waf(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "waf"))

    @waf.setter
    def waf(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b498adc81d8acf6b82202c231ea3a3f4b54ab29f5040aeb0910b1507755b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waf", value)

    @builtins.property
    @jsii.member(jsii_name="webp")
    def webp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webp"))

    @webp.setter
    def webp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c57732cd2331b530b7bf42b58ce6706f3c7e137a377f6b5ec38f335a1d28274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webp", value)

    @builtins.property
    @jsii.member(jsii_name="websockets")
    def websockets(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "websockets"))

    @websockets.setter
    def websockets(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a594894643f13634f0f93f7a98d486ae66fd7ff7fd555f142f5df7d4fc0c0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "websockets", value)

    @builtins.property
    @jsii.member(jsii_name="zeroRtt")
    def zero_rtt(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zeroRtt"))

    @zero_rtt.setter
    def zero_rtt(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfa1f172147491d5b9ec44abb7c1a2afde5dc7972d7d676bf2ebfefc9859a200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zeroRtt", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZoneSettingsOverrideSettings]:
        return typing.cast(typing.Optional[ZoneSettingsOverrideSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZoneSettingsOverrideSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee30e9cbcb5cb28b92569d2cb9141cbc6401d7ae1d6ce05b1cdfe6f9b5e49dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideSettingsSecurityHeader",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "include_subdomains": "includeSubdomains",
        "max_age": "maxAge",
        "nosniff": "nosniff",
        "preload": "preload",
    },
)
class ZoneSettingsOverrideSettingsSecurityHeader:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_age: typing.Optional[jsii.Number] = None,
        nosniff: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#enabled ZoneSettingsOverride#enabled}.
        :param include_subdomains: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#include_subdomains ZoneSettingsOverride#include_subdomains}.
        :param max_age: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#max_age ZoneSettingsOverride#max_age}.
        :param nosniff: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#nosniff ZoneSettingsOverride#nosniff}.
        :param preload: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#preload ZoneSettingsOverride#preload}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacd5f40cab7e0565fe2ae27f92a1d04bef0c29ea38bcc38336945d07d493c6f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument include_subdomains", value=include_subdomains, expected_type=type_hints["include_subdomains"])
            check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            check_type(argname="argument nosniff", value=nosniff, expected_type=type_hints["nosniff"])
            check_type(argname="argument preload", value=preload, expected_type=type_hints["preload"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if include_subdomains is not None:
            self._values["include_subdomains"] = include_subdomains
        if max_age is not None:
            self._values["max_age"] = max_age
        if nosniff is not None:
            self._values["nosniff"] = nosniff
        if preload is not None:
            self._values["preload"] = preload

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#enabled ZoneSettingsOverride#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_subdomains(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#include_subdomains ZoneSettingsOverride#include_subdomains}.'''
        result = self._values.get("include_subdomains")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_age(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#max_age ZoneSettingsOverride#max_age}.'''
        result = self._values.get("max_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nosniff(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#nosniff ZoneSettingsOverride#nosniff}.'''
        result = self._values.get("nosniff")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def preload(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_settings_override#preload ZoneSettingsOverride#preload}.'''
        result = self._values.get("preload")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneSettingsOverrideSettingsSecurityHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZoneSettingsOverrideSettingsSecurityHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneSettingsOverride.ZoneSettingsOverrideSettingsSecurityHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d964664dc01f3dc3f0a7d231bc045a65d027d2dc0f878a7d8afde21b0b554698)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetIncludeSubdomains")
    def reset_include_subdomains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeSubdomains", []))

    @jsii.member(jsii_name="resetMaxAge")
    def reset_max_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAge", []))

    @jsii.member(jsii_name="resetNosniff")
    def reset_nosniff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNosniff", []))

    @jsii.member(jsii_name="resetPreload")
    def reset_preload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreload", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSubdomainsInput")
    def include_subdomains_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeSubdomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInput")
    def max_age_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="nosniffInput")
    def nosniff_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nosniffInput"))

    @builtins.property
    @jsii.member(jsii_name="preloadInput")
    def preload_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preloadInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__87692fd1ceb0bd5c091b1aba24053c7aa4676b8e2ce9d09147794a0de41cd396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="includeSubdomains")
    def include_subdomains(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeSubdomains"))

    @include_subdomains.setter
    def include_subdomains(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d2b73a1d8ac43601a269bbbb21cb792f832122d0626aec66975b78df0618fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeSubdomains", value)

    @builtins.property
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAge"))

    @max_age.setter
    def max_age(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__276a470fe73cacf9127295caab6f60392b87174cd9ec4da0e3ec50204898be9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAge", value)

    @builtins.property
    @jsii.member(jsii_name="nosniff")
    def nosniff(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nosniff"))

    @nosniff.setter
    def nosniff(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648cb48294efbeb87b1212e628493922510f10364de744c6ea494d60bb84f3fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nosniff", value)

    @builtins.property
    @jsii.member(jsii_name="preload")
    def preload(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preload"))

    @preload.setter
    def preload(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391bdf482d894bdd8e7a41072f81dcea6a324418af57a1ddf555c9fe08de6aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preload", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZoneSettingsOverrideSettingsSecurityHeader]:
        return typing.cast(typing.Optional[ZoneSettingsOverrideSettingsSecurityHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZoneSettingsOverrideSettingsSecurityHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__747e7e35d5936f4678b9b9bf186be0e1528b7b7d89fe3befc5a618550b4387c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ZoneSettingsOverride",
    "ZoneSettingsOverrideConfig",
    "ZoneSettingsOverrideInitialSettings",
    "ZoneSettingsOverrideInitialSettingsList",
    "ZoneSettingsOverrideInitialSettingsMinify",
    "ZoneSettingsOverrideInitialSettingsMinifyList",
    "ZoneSettingsOverrideInitialSettingsMinifyOutputReference",
    "ZoneSettingsOverrideInitialSettingsMobileRedirect",
    "ZoneSettingsOverrideInitialSettingsMobileRedirectList",
    "ZoneSettingsOverrideInitialSettingsMobileRedirectOutputReference",
    "ZoneSettingsOverrideInitialSettingsOutputReference",
    "ZoneSettingsOverrideInitialSettingsSecurityHeader",
    "ZoneSettingsOverrideInitialSettingsSecurityHeaderList",
    "ZoneSettingsOverrideInitialSettingsSecurityHeaderOutputReference",
    "ZoneSettingsOverrideSettings",
    "ZoneSettingsOverrideSettingsMinify",
    "ZoneSettingsOverrideSettingsMinifyOutputReference",
    "ZoneSettingsOverrideSettingsMobileRedirect",
    "ZoneSettingsOverrideSettingsMobileRedirectOutputReference",
    "ZoneSettingsOverrideSettingsOutputReference",
    "ZoneSettingsOverrideSettingsSecurityHeader",
    "ZoneSettingsOverrideSettingsSecurityHeaderOutputReference",
]

publication.publish()

def _typecheckingstub__1c10c6800a751edbd8a6c1b901cba3fbd670290a746be2a4007c60f4f4d8b705(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    zone_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    settings: typing.Optional[typing.Union[ZoneSettingsOverrideSettings, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__333d8f50b4c3b29d844894530b1f39e71ee6a864d39f20438f63487f973bd101(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc314ab95e37bd3a23b70005373101bc9e1edef2944c7ea133116e48a141518(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce340b9b59b16072eaa592860129ffb73bb9b7317b889d85378405d7cdf1b593(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zone_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    settings: typing.Optional[typing.Union[ZoneSettingsOverrideSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34cb3ae19588347c59c496121c2321e28274054a07e8a5901607a4ef8b79429(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86305045a06e67ccde7f2b3eb589f5c8ce9e3171ad234caa1f9a37abba02639(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c60d057a1f9dddcec7cea1b4053e6652d727731a84be428cc615965e2b67b86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecbd5cbbf560f48cbd81330694cca3970365f33e4d8e101bd699165bbfdbebe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d41b4bab6144747141f92096e20db2130da1110cab4ac8c2e10e7a5c1a4242(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e55d308bd9ab7df6b3c618fc2e7084ae2e5b1bfd763b809c2d084e4bf67afad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f5c60fab9c364a78669a3fbfa6c3e051fb267df64d4092071fbd01ab0901e4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e8e49ade9834b6905096e663380f4aca58564217ce0cdbcc97c33267528e2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98357c2761f7484eff52e26be457c6d2296fee31188eca7ac52981592eb58605(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1e7e03528c36bfbd25eca7997516bc5d48e2a36d2e64d4cb196f72d6369e46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df512b2f2a4bb9e95a3a0d2dd9d6ed59aa7a7b498345ec0318c12740d82ffe6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0be52c34596e8d0980ba01b629c51370a52f9421f20bbb1b824efc84f376aaf(
    value: typing.Optional[ZoneSettingsOverrideInitialSettingsMinify],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e94ef511f9d59c10fb77c98f80f7d82822b0dc4462870c33b7a093c63e6f82ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18ae254d74f9bfb9e933f687f743454e9055d6a3c72d8e41184ebd30b01cb8e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d5f6732eb3f8b361ea1b360c66a75477e5167d9c9382fe308fcef6779166a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__023fdd4a6a0ec74aca2ae76e7861bb527f6817179bbbbf671911413f59e63798(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9be06876e7724498b5900a86ba1328c0976904fd22f57fed6f9b35bcb4544013(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fceef8de5940bac0f63847b1766d19f5cdd76fe8c6ef87271d8c2ec66b0db8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c783dbaa86c65b1409ad7fd13872f0fd5f1faed9dd755288be2936d5178e19(
    value: typing.Optional[ZoneSettingsOverrideInitialSettingsMobileRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b256e8200b9beabd76ddd80a04a6da2a0914025b2d27c8c23a30bd68b5d7b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebea9a100d1c96723de2ce8cdf85467eea1bad64c6b6ff441fb6f1982d24bdf8(
    value: typing.Optional[ZoneSettingsOverrideInitialSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a48bd9db836a276982cade7cf0faa27e936d806b50adb92b06c887dfd03239(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a92f8ab861c4576c5a0800b71208d7f79ea5c091e5e7530be1c1ca0acdaad97(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2290be03209fdddfef506a307d53863c0407dc9b4989297923826a561d4f5fda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41fd9853196db05055ffed5a49ff6cb0fb22e9429840381b861a3f14cd7c7261(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5a2043491ef903b076e01efe3b02bd4fdd504f2b3842ff65ad3b7ef07d6505(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b393dc63afdc47cc33e8d9c22b4ff52fbbafd1f5e7d5fc8069ce96740e91f9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11710c016294dc1dd75b179e68a1be1df9c53c1cc676cf6668ae665c39b130eb(
    value: typing.Optional[ZoneSettingsOverrideInitialSettingsSecurityHeader],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458332e0a6cc8bd4dc90e0e73f6df6be2ebaab3530e33bc4eebfd1fd982bdfb3(
    *,
    always_online: typing.Optional[builtins.str] = None,
    always_use_https: typing.Optional[builtins.str] = None,
    automatic_https_rewrites: typing.Optional[builtins.str] = None,
    binary_ast: typing.Optional[builtins.str] = None,
    brotli: typing.Optional[builtins.str] = None,
    browser_cache_ttl: typing.Optional[jsii.Number] = None,
    browser_check: typing.Optional[builtins.str] = None,
    cache_level: typing.Optional[builtins.str] = None,
    challenge_ttl: typing.Optional[jsii.Number] = None,
    ciphers: typing.Optional[typing.Sequence[builtins.str]] = None,
    cname_flattening: typing.Optional[builtins.str] = None,
    development_mode: typing.Optional[builtins.str] = None,
    early_hints: typing.Optional[builtins.str] = None,
    email_obfuscation: typing.Optional[builtins.str] = None,
    filter_logs_to_cloudflare: typing.Optional[builtins.str] = None,
    h2_prioritization: typing.Optional[builtins.str] = None,
    hotlink_protection: typing.Optional[builtins.str] = None,
    http2: typing.Optional[builtins.str] = None,
    http3: typing.Optional[builtins.str] = None,
    image_resizing: typing.Optional[builtins.str] = None,
    ip_geolocation: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[builtins.str] = None,
    log_to_cloudflare: typing.Optional[builtins.str] = None,
    max_upload: typing.Optional[jsii.Number] = None,
    minify: typing.Optional[typing.Union[ZoneSettingsOverrideSettingsMinify, typing.Dict[builtins.str, typing.Any]]] = None,
    min_tls_version: typing.Optional[builtins.str] = None,
    mirage: typing.Optional[builtins.str] = None,
    mobile_redirect: typing.Optional[typing.Union[ZoneSettingsOverrideSettingsMobileRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
    opportunistic_encryption: typing.Optional[builtins.str] = None,
    opportunistic_onion: typing.Optional[builtins.str] = None,
    orange_to_orange: typing.Optional[builtins.str] = None,
    origin_error_page_pass_thru: typing.Optional[builtins.str] = None,
    origin_max_http_version: typing.Optional[builtins.str] = None,
    polish: typing.Optional[builtins.str] = None,
    prefetch_preload: typing.Optional[builtins.str] = None,
    privacy_pass: typing.Optional[builtins.str] = None,
    proxy_read_timeout: typing.Optional[builtins.str] = None,
    pseudo_ipv4: typing.Optional[builtins.str] = None,
    response_buffering: typing.Optional[builtins.str] = None,
    rocket_loader: typing.Optional[builtins.str] = None,
    security_header: typing.Optional[typing.Union[ZoneSettingsOverrideSettingsSecurityHeader, typing.Dict[builtins.str, typing.Any]]] = None,
    security_level: typing.Optional[builtins.str] = None,
    server_side_exclude: typing.Optional[builtins.str] = None,
    sort_query_string_for_cache: typing.Optional[builtins.str] = None,
    ssl: typing.Optional[builtins.str] = None,
    tls12_only: typing.Optional[builtins.str] = None,
    tls13: typing.Optional[builtins.str] = None,
    tls_client_auth: typing.Optional[builtins.str] = None,
    true_client_ip_header: typing.Optional[builtins.str] = None,
    universal_ssl: typing.Optional[builtins.str] = None,
    visitor_ip: typing.Optional[builtins.str] = None,
    waf: typing.Optional[builtins.str] = None,
    webp: typing.Optional[builtins.str] = None,
    websockets: typing.Optional[builtins.str] = None,
    zero_rtt: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0550b681c744a96b12f003b698673d43bbdb7bbedfcfbe3f2f4266c3f051fe(
    *,
    css: builtins.str,
    html: builtins.str,
    js: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de227cf63aa5c0429da46a86995b52d7cb26582d2e6a2e190b030a8f688db7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfcf58f1ce4e92017ea77ea312c8af5e5a08a1c72d95b4f7a8f67cd6cadd873(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368149c638da8c149a1456bb0272806634daa55fd21b5f7c85b068bf3640256f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d7b3fd85408e62986f4859e3bb2d2a2d31d68640fec4a1d112a56c648926ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63baca054ad4577774a83376f9967468da472ae4348bde0e8babe50d1b9a4a7c(
    value: typing.Optional[ZoneSettingsOverrideSettingsMinify],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461a93c655947e4d5a1d714ce53d00ad33a9a5ddaed83bf776ed1246f0ce5eb3(
    *,
    mobile_subdomain: builtins.str,
    status: builtins.str,
    strip_uri: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172f040b1cf49bbf74b6a6126a3f1c230a4cde737f6f9b5da59d1060ba4f5bcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2f2bd63b3beafcf7648da3b6404851fb0228548488d81f2ab650970ca7e448(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9beb8933d006650dd30421ba595f199f7c797ae8b8bb0e608f71f21bf4e5a060(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfdd3e1368590ee6a9c0b31d102fa51fa8c1cefc0397bfca5e3a849450ee40c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c205307d441da8cbadacc11f077c226662ea86815557e218b1f970ba1127a9c(
    value: typing.Optional[ZoneSettingsOverrideSettingsMobileRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f583bec6b045d6b82e435e739d30238299ec942448fd53042ed9daed24f380(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178b0817d8340cc2ccc897361f0e7c3b29edd827f7ca5ca7a005b4c688cca065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb017378eaacd5f50e2af6acc296fce63e6f8f7507cd023f0e28d49452c8270(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97275e879309815c97d229a088ead98ac0fd1de6b3c0891bdea9891c0458d44f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5a54b555a06718df0dc7e655c3a82d0960bf04852e1ed0f431d13d59bddf2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708b806be1daba1cf6337c4f9fc1ed99efc667251840c8cce8b3afba8ba526c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02336c296fdd0b11bf02eac2221923d0aa38b75c888d3c8b209a2d283e14a82c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5dc4ae60f2aca66669f2924745c827f8211bdc3808b4b27b1d1763974a5b9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eed5dc74407d87c939b17cbda6199f8f6fb2ecf888d6385af68de965d0e969f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2db5e0b593b123e2e73aaf18fefe91a9ac38cee184368f892d2ede72bd92cd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5824de6be9d8ffed4727c61e06cf05dec649746bb117bc3c9d4902002528b736(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa51957b0c0401498061acd4ec51105dc8d9346dd45c1d2681bd5202e383fa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e799815dead9a81f8b3476e222e38b14c5585ceadff3a4383aff5763fac091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc6905f432003c92e5d77d6aedc73bfbd69937fc167dde4add0d7b9054fe572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40e36ff85839d1a4a06f4ceba02fed650134a6dc2f4b88c03e095f645c76a03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4e949073d14ce3595c660b1d5dccddb365e461c779764fccb327eee1864c79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1eca2bb9fe73623bed2102dd8392536c8757e87da0381f0f2387219b4bbef20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb56a359fe89cdf28f40693ce44ab103c9c6a600103aee2e89cced1fb687d089(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bcef4ec36a6148efafdd3a93b014b06b4372a3875e937840a6f47e4c8a9da8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8289ece65f7370fb653a45b301939d07390cd297bccf15710a82aa9790635aec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10552b56fddb294067344bb5dcb673b324d565fc83333c46d0443b8ecbbb1c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d94a2a0423b9733a9a7f4df9e58f502c67873722ad592cc6deb1b85170d3e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c472caf7aa28f9118fc252085e7e4fba8ee56b4a9bcc7536608e1fce67318f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f992cb4baa56c40b066100a35a1224b8f638e6da4ac1b3a9aed2ccb6a397047(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37603ca2b27a2dd5f2d7d408b3e3d16bccbb98b065672eba58bf3edadf156ed0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46bf8142ca948d8a51b5b8970e6a7986e7c2febd8761c103a06eb2ec1fce7741(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43084affddec7b1a91909f59cbc662fc335257761cecb4ae35589e8726e77e23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bf48a86b240d4d5ba31cc3ac86f66297d12080eb72f3f4e235bc1dab2a23a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa4d44082417e62abed860c6fffc6295bedf7c6c9a120787af1e7a2398599f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6203b15b06780711a6fe08451c971cbac89dbc276ea8e7f7f2cb7481a093930c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5964858f6a8acd7b9d594334505a479c364a0c722bee0e53af9b0c831a1fc61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6700984e6509d62a8ec65740644cf2b4fbfd516839525c4ffd0d8bce2e145cef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed619f88bbd2c75e78b1eef9ba6e701d88f5d4c4a1eafa90ee7b4ad7d8a5554(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f3c6fb6d1dcd31b8aa9d0214ca0c95c8ef2edcc9749d8d367f6fc6a203dbfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f7fb4eb55e4fc0a52bf771a682efccebbb66c5ec84138abf3714f803e68fb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b633b1b6fcb9215a595c9cd2f877bbf07456188ec49c2883f44bb50bef7cb42d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813aaa38999ad92002f36ad2cd8374ae316066f9091752bd0c3002807b84027e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d6260bcb26bbb98768a3bd6b8d89742d43c2bf8e367a25306aa3dbf6011e7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d266b80877d645697fadca35de85cc0a81d9bd27c3d32706343c1008d6807e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e97ad07535b85e265ab3e831a0b23e6f3aa83f905acf5324f5481eead059c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c732884c1f450ea81231872396890cce77ee6aa8a9c0adcf05662fcabe5243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901984c0f3a328d7a09ce0ef6a414e571864465546f6d2c00e1323812dcbb047(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e764764eade0efd634d5929d9f9d11c37e1ea9bff7158fb43319bd98fd4e8cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b84d16a85e212fe4d811535eab99afc4b151ef644c8f216f41d3fa5be66caaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e1138bf8afadbfa4a116adb9e10e2b71f119b56386726a0311c2f6695128f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b67955c91418592dbff5b50075d10c47aa615a9458ae91beaec8117ddf3859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee3020cce66c605ff81d3de9b4b630fa2af6b85d3bdf7cc31010cdb662438dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a0091f5ec66baca77ce1460977c29a67f199812731de7c0720d1c75c65f2d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb90ccd5c88289d9ea0308ac4702d57b2abd50195fc58bdea65836c70d3fe312(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b498adc81d8acf6b82202c231ea3a3f4b54ab29f5040aeb0910b1507755b6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c57732cd2331b530b7bf42b58ce6706f3c7e137a377f6b5ec38f335a1d28274(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a594894643f13634f0f93f7a98d486ae66fd7ff7fd555f142f5df7d4fc0c0c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa1f172147491d5b9ec44abb7c1a2afde5dc7972d7d676bf2ebfefc9859a200(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee30e9cbcb5cb28b92569d2cb9141cbc6401d7ae1d6ce05b1cdfe6f9b5e49dd(
    value: typing.Optional[ZoneSettingsOverrideSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacd5f40cab7e0565fe2ae27f92a1d04bef0c29ea38bcc38336945d07d493c6f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_subdomains: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_age: typing.Optional[jsii.Number] = None,
    nosniff: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    preload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d964664dc01f3dc3f0a7d231bc045a65d027d2dc0f878a7d8afde21b0b554698(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87692fd1ceb0bd5c091b1aba24053c7aa4676b8e2ce9d09147794a0de41cd396(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d2b73a1d8ac43601a269bbbb21cb792f832122d0626aec66975b78df0618fe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276a470fe73cacf9127295caab6f60392b87174cd9ec4da0e3ec50204898be9b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648cb48294efbeb87b1212e628493922510f10364de744c6ea494d60bb84f3fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391bdf482d894bdd8e7a41072f81dcea6a324418af57a1ddf555c9fe08de6aec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747e7e35d5936f4678b9b9bf186be0e1528b7b7d89fe3befc5a618550b4387c8(
    value: typing.Optional[ZoneSettingsOverrideSettingsSecurityHeader],
) -> None:
    """Type checking stubs"""
    pass
