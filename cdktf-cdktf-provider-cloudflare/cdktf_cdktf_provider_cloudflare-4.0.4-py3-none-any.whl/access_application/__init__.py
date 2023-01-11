'''
# `cloudflare_access_application`

Refer to the Terraform Registory for docs: [`cloudflare_access_application`](https://www.terraform.io/docs/providers/cloudflare/r/access_application).
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


class AccessApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplication",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application cloudflare_access_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        allowed_idps: typing.Optional[typing.Sequence[builtins.str]] = None,
        app_launcher_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_redirect_to_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationCorsHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_deny_message: typing.Optional[builtins.str] = None,
        custom_deny_url: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logo_url: typing.Optional[builtins.str] = None,
        saas_app: typing.Optional[typing.Union["AccessApplicationSaasApp", typing.Dict[builtins.str, typing.Any]]] = None,
        same_site_cookie_attribute: typing.Optional[builtins.str] = None,
        service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_duration: typing.Optional[builtins.str] = None,
        skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        type: typing.Optional[builtins.str] = None,
        zone_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application cloudflare_access_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Friendly name of the Access Application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#name AccessApplication#name}
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#account_id AccessApplication#account_id}
        :param allowed_idps: The identity providers selected for the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allowed_idps AccessApplication#allowed_idps}
        :param app_launcher_visible: Option to show/hide applications in App Launcher. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#app_launcher_visible AccessApplication#app_launcher_visible}
        :param auto_redirect_to_identity: Option to skip identity provider selection if only one is configured in ``allowed_idps``. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#auto_redirect_to_identity AccessApplication#auto_redirect_to_identity}
        :param cors_headers: cors_headers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#cors_headers AccessApplication#cors_headers}
        :param custom_deny_message: Option that returns a custom error message when a user is denied access to the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#custom_deny_message AccessApplication#custom_deny_message}
        :param custom_deny_url: Option that redirects to a custom URL when a user is denied access to the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#custom_deny_url AccessApplication#custom_deny_url}
        :param domain: The complete URL of the asset you wish to put Cloudflare Access in front of. Can include subdomains or paths. Or both. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#domain AccessApplication#domain}
        :param enable_binding_cookie: Option to provide increased security against compromised authorization tokens and CSRF attacks by requiring an additional "binding" cookie on requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#enable_binding_cookie AccessApplication#enable_binding_cookie}
        :param http_only_cookie_attribute: Option to add the ``HttpOnly`` cookie flag to access tokens. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#http_only_cookie_attribute AccessApplication#http_only_cookie_attribute}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#id AccessApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo_url: Image URL for the logo shown in the app launcher dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#logo_url AccessApplication#logo_url}
        :param saas_app: saas_app block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#saas_app AccessApplication#saas_app}
        :param same_site_cookie_attribute: Defines the same-site cookie setting for access tokens. Available values: ``none``, ``lax``, ``strict``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#same_site_cookie_attribute AccessApplication#same_site_cookie_attribute}
        :param service_auth401_redirect: Option to return a 401 status code in service authentication rules on failed requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#service_auth_401_redirect AccessApplication#service_auth_401_redirect}
        :param session_duration: How often a user will be forced to re-authorise. Must be in the format ``48h`` or ``2h45m``. Defaults to ``24h``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#session_duration AccessApplication#session_duration}
        :param skip_interstitial: Option to skip the authorization interstitial when using the CLI. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#skip_interstitial AccessApplication#skip_interstitial}
        :param type: The application type. Available values: ``app_launcher``, ``bookmark``, ``biso``, ``dash_sso``, ``saas``, ``self_hosted``, ``ssh``, ``vnc``, ``warp``. Defaults to ``self_hosted``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#type AccessApplication#type}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#zone_id AccessApplication#zone_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b2963f98659b9017b97318b2a37e45b5084f4b60cafaa3bcd97429790c8eb1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessApplicationConfig(
            name=name,
            account_id=account_id,
            allowed_idps=allowed_idps,
            app_launcher_visible=app_launcher_visible,
            auto_redirect_to_identity=auto_redirect_to_identity,
            cors_headers=cors_headers,
            custom_deny_message=custom_deny_message,
            custom_deny_url=custom_deny_url,
            domain=domain,
            enable_binding_cookie=enable_binding_cookie,
            http_only_cookie_attribute=http_only_cookie_attribute,
            id=id,
            logo_url=logo_url,
            saas_app=saas_app,
            same_site_cookie_attribute=same_site_cookie_attribute,
            service_auth401_redirect=service_auth401_redirect,
            session_duration=session_duration,
            skip_interstitial=skip_interstitial,
            type=type,
            zone_id=zone_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putCorsHeaders")
    def put_cors_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationCorsHeaders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0c9359a2094e6a5d995e98fae21fbe1877ef3aca4c5f09eb4d19306fa8750c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCorsHeaders", [value]))

    @jsii.member(jsii_name="putSaasApp")
    def put_saas_app(
        self,
        *,
        consumer_service_url: builtins.str,
        sp_entity_id: builtins.str,
        name_id_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_service_url: The service provider's endpoint that is responsible for receiving and parsing a SAML assertion. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#consumer_service_url AccessApplication#consumer_service_url}
        :param sp_entity_id: A globally unique name for an identity or service provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#sp_entity_id AccessApplication#sp_entity_id}
        :param name_id_format: The format of the name identifier sent to the SaaS application. Defaults to ``email``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#name_id_format AccessApplication#name_id_format}
        '''
        value = AccessApplicationSaasApp(
            consumer_service_url=consumer_service_url,
            sp_entity_id=sp_entity_id,
            name_id_format=name_id_format,
        )

        return typing.cast(None, jsii.invoke(self, "putSaasApp", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetAllowedIdps")
    def reset_allowed_idps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedIdps", []))

    @jsii.member(jsii_name="resetAppLauncherVisible")
    def reset_app_launcher_visible(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppLauncherVisible", []))

    @jsii.member(jsii_name="resetAutoRedirectToIdentity")
    def reset_auto_redirect_to_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRedirectToIdentity", []))

    @jsii.member(jsii_name="resetCorsHeaders")
    def reset_cors_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsHeaders", []))

    @jsii.member(jsii_name="resetCustomDenyMessage")
    def reset_custom_deny_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDenyMessage", []))

    @jsii.member(jsii_name="resetCustomDenyUrl")
    def reset_custom_deny_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDenyUrl", []))

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetEnableBindingCookie")
    def reset_enable_binding_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableBindingCookie", []))

    @jsii.member(jsii_name="resetHttpOnlyCookieAttribute")
    def reset_http_only_cookie_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpOnlyCookieAttribute", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogoUrl")
    def reset_logo_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogoUrl", []))

    @jsii.member(jsii_name="resetSaasApp")
    def reset_saas_app(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaasApp", []))

    @jsii.member(jsii_name="resetSameSiteCookieAttribute")
    def reset_same_site_cookie_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSameSiteCookieAttribute", []))

    @jsii.member(jsii_name="resetServiceAuth401Redirect")
    def reset_service_auth401_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAuth401Redirect", []))

    @jsii.member(jsii_name="resetSessionDuration")
    def reset_session_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionDuration", []))

    @jsii.member(jsii_name="resetSkipInterstitial")
    def reset_skip_interstitial(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipInterstitial", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetZoneId")
    def reset_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="aud")
    def aud(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aud"))

    @builtins.property
    @jsii.member(jsii_name="corsHeaders")
    def cors_headers(self) -> "AccessApplicationCorsHeadersList":
        return typing.cast("AccessApplicationCorsHeadersList", jsii.get(self, "corsHeaders"))

    @builtins.property
    @jsii.member(jsii_name="saasApp")
    def saas_app(self) -> "AccessApplicationSaasAppOutputReference":
        return typing.cast("AccessApplicationSaasAppOutputReference", jsii.get(self, "saasApp"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedIdpsInput")
    def allowed_idps_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedIdpsInput"))

    @builtins.property
    @jsii.member(jsii_name="appLauncherVisibleInput")
    def app_launcher_visible_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "appLauncherVisibleInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRedirectToIdentityInput")
    def auto_redirect_to_identity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoRedirectToIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="corsHeadersInput")
    def cors_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationCorsHeaders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationCorsHeaders"]]], jsii.get(self, "corsHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="customDenyMessageInput")
    def custom_deny_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDenyMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="customDenyUrlInput")
    def custom_deny_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDenyUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="enableBindingCookieInput")
    def enable_binding_cookie_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableBindingCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="httpOnlyCookieAttributeInput")
    def http_only_cookie_attribute_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpOnlyCookieAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logoUrlInput")
    def logo_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="saasAppInput")
    def saas_app_input(self) -> typing.Optional["AccessApplicationSaasApp"]:
        return typing.cast(typing.Optional["AccessApplicationSaasApp"], jsii.get(self, "saasAppInput"))

    @builtins.property
    @jsii.member(jsii_name="sameSiteCookieAttributeInput")
    def same_site_cookie_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sameSiteCookieAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAuth401RedirectInput")
    def service_auth401_redirect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "serviceAuth401RedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionDurationInput")
    def session_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="skipInterstitialInput")
    def skip_interstitial_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipInterstitialInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81fb38f689b4bf068fc2e8ba83e0a3ec1a53465fe9ca9bf20ef28753a9f80251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="allowedIdps")
    def allowed_idps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedIdps"))

    @allowed_idps.setter
    def allowed_idps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daff490d3a8108f46fe8affbe607ed3bfce7f0caa97c3a01158863a2d9b81e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIdps", value)

    @builtins.property
    @jsii.member(jsii_name="appLauncherVisible")
    def app_launcher_visible(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "appLauncherVisible"))

    @app_launcher_visible.setter
    def app_launcher_visible(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74fe33b6a3e0de6c5d2332cddc4e94399f81b3f96589f00d5cea096ca5c90e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLauncherVisible", value)

    @builtins.property
    @jsii.member(jsii_name="autoRedirectToIdentity")
    def auto_redirect_to_identity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoRedirectToIdentity"))

    @auto_redirect_to_identity.setter
    def auto_redirect_to_identity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02da31929754ab70993542e7f44f5e3b8ff2a4113ea0e7fc09dccad505e190e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRedirectToIdentity", value)

    @builtins.property
    @jsii.member(jsii_name="customDenyMessage")
    def custom_deny_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDenyMessage"))

    @custom_deny_message.setter
    def custom_deny_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7394b2b4e1199550fbe6375395d12db57b5a15a49a4d5b7355d6ce5ad25636e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDenyMessage", value)

    @builtins.property
    @jsii.member(jsii_name="customDenyUrl")
    def custom_deny_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDenyUrl"))

    @custom_deny_url.setter
    def custom_deny_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bda6e3a2399b050e18d5c2bc8f4883cf54b73d8211f3d0847551f970d6b384e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDenyUrl", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bcbe163ed94bb0a50cb8b1b9b52ea152aa192b9bd50115601e6ab1b87eaf861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="enableBindingCookie")
    def enable_binding_cookie(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableBindingCookie"))

    @enable_binding_cookie.setter
    def enable_binding_cookie(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ffea86ba305f92fcd8ef5768d2698c4bf9c262d3a7e35de9c4bbf7711be2159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableBindingCookie", value)

    @builtins.property
    @jsii.member(jsii_name="httpOnlyCookieAttribute")
    def http_only_cookie_attribute(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpOnlyCookieAttribute"))

    @http_only_cookie_attribute.setter
    def http_only_cookie_attribute(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b7a56cc0c2523d37beeaca9d4af0ffe258c84ad7cd8666034d44c91b2c0a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpOnlyCookieAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cee610faa04b0d8e65aad04b0e960f1a472af48d19258d665b5edfc30e57e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="logoUrl")
    def logo_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoUrl"))

    @logo_url.setter
    def logo_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94205b9b871f765a94dff73949e655473bf7b6ffab02f41b2a507b924040f1a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoUrl", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408052199c5db90c8698c809b74ffc55459b674605e439d3b3bfd8a083255a13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sameSiteCookieAttribute")
    def same_site_cookie_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sameSiteCookieAttribute"))

    @same_site_cookie_attribute.setter
    def same_site_cookie_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a95c47163bc493ca9389335db25497d901b8dedf1f1549f91f1f323ea93a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sameSiteCookieAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="serviceAuth401Redirect")
    def service_auth401_redirect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "serviceAuth401Redirect"))

    @service_auth401_redirect.setter
    def service_auth401_redirect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad3bbb24317d5f07a9fb5037e763a244642bebdc8fa18f8d948e52201c04187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAuth401Redirect", value)

    @builtins.property
    @jsii.member(jsii_name="sessionDuration")
    def session_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionDuration"))

    @session_duration.setter
    def session_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adfb91cb0ee9996051ba552f920aa96e9da21960ed72cf49353e36a46107d982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionDuration", value)

    @builtins.property
    @jsii.member(jsii_name="skipInterstitial")
    def skip_interstitial(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipInterstitial"))

    @skip_interstitial.setter
    def skip_interstitial(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b86799f85043068c1b6ac6d68b67ebdd5dc15341cb709a8eeccbecf097cf147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipInterstitial", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ac6df2597f216a2f0ef7d91eff615dd9bd4f92bf47b2a9e51dec9e2a97df20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f33c40394937d1eb21e9c367c96d3212115f53970a6ffb9db1ab2ecac777b19f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationConfig",
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
        "account_id": "accountId",
        "allowed_idps": "allowedIdps",
        "app_launcher_visible": "appLauncherVisible",
        "auto_redirect_to_identity": "autoRedirectToIdentity",
        "cors_headers": "corsHeaders",
        "custom_deny_message": "customDenyMessage",
        "custom_deny_url": "customDenyUrl",
        "domain": "domain",
        "enable_binding_cookie": "enableBindingCookie",
        "http_only_cookie_attribute": "httpOnlyCookieAttribute",
        "id": "id",
        "logo_url": "logoUrl",
        "saas_app": "saasApp",
        "same_site_cookie_attribute": "sameSiteCookieAttribute",
        "service_auth401_redirect": "serviceAuth401Redirect",
        "session_duration": "sessionDuration",
        "skip_interstitial": "skipInterstitial",
        "type": "type",
        "zone_id": "zoneId",
    },
)
class AccessApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_id: typing.Optional[builtins.str] = None,
        allowed_idps: typing.Optional[typing.Sequence[builtins.str]] = None,
        app_launcher_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_redirect_to_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationCorsHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_deny_message: typing.Optional[builtins.str] = None,
        custom_deny_url: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logo_url: typing.Optional[builtins.str] = None,
        saas_app: typing.Optional[typing.Union["AccessApplicationSaasApp", typing.Dict[builtins.str, typing.Any]]] = None,
        same_site_cookie_attribute: typing.Optional[builtins.str] = None,
        service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_duration: typing.Optional[builtins.str] = None,
        skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        type: typing.Optional[builtins.str] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Friendly name of the Access Application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#name AccessApplication#name}
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#account_id AccessApplication#account_id}
        :param allowed_idps: The identity providers selected for the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allowed_idps AccessApplication#allowed_idps}
        :param app_launcher_visible: Option to show/hide applications in App Launcher. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#app_launcher_visible AccessApplication#app_launcher_visible}
        :param auto_redirect_to_identity: Option to skip identity provider selection if only one is configured in ``allowed_idps``. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#auto_redirect_to_identity AccessApplication#auto_redirect_to_identity}
        :param cors_headers: cors_headers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#cors_headers AccessApplication#cors_headers}
        :param custom_deny_message: Option that returns a custom error message when a user is denied access to the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#custom_deny_message AccessApplication#custom_deny_message}
        :param custom_deny_url: Option that redirects to a custom URL when a user is denied access to the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#custom_deny_url AccessApplication#custom_deny_url}
        :param domain: The complete URL of the asset you wish to put Cloudflare Access in front of. Can include subdomains or paths. Or both. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#domain AccessApplication#domain}
        :param enable_binding_cookie: Option to provide increased security against compromised authorization tokens and CSRF attacks by requiring an additional "binding" cookie on requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#enable_binding_cookie AccessApplication#enable_binding_cookie}
        :param http_only_cookie_attribute: Option to add the ``HttpOnly`` cookie flag to access tokens. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#http_only_cookie_attribute AccessApplication#http_only_cookie_attribute}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#id AccessApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo_url: Image URL for the logo shown in the app launcher dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#logo_url AccessApplication#logo_url}
        :param saas_app: saas_app block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#saas_app AccessApplication#saas_app}
        :param same_site_cookie_attribute: Defines the same-site cookie setting for access tokens. Available values: ``none``, ``lax``, ``strict``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#same_site_cookie_attribute AccessApplication#same_site_cookie_attribute}
        :param service_auth401_redirect: Option to return a 401 status code in service authentication rules on failed requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#service_auth_401_redirect AccessApplication#service_auth_401_redirect}
        :param session_duration: How often a user will be forced to re-authorise. Must be in the format ``48h`` or ``2h45m``. Defaults to ``24h``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#session_duration AccessApplication#session_duration}
        :param skip_interstitial: Option to skip the authorization interstitial when using the CLI. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#skip_interstitial AccessApplication#skip_interstitial}
        :param type: The application type. Available values: ``app_launcher``, ``bookmark``, ``biso``, ``dash_sso``, ``saas``, ``self_hosted``, ``ssh``, ``vnc``, ``warp``. Defaults to ``self_hosted``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#type AccessApplication#type}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#zone_id AccessApplication#zone_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(saas_app, dict):
            saas_app = AccessApplicationSaasApp(**saas_app)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f785d33e1451f1cf27417eb2776a2d793dff777b28167e528be38cf2a13a8faa)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument allowed_idps", value=allowed_idps, expected_type=type_hints["allowed_idps"])
            check_type(argname="argument app_launcher_visible", value=app_launcher_visible, expected_type=type_hints["app_launcher_visible"])
            check_type(argname="argument auto_redirect_to_identity", value=auto_redirect_to_identity, expected_type=type_hints["auto_redirect_to_identity"])
            check_type(argname="argument cors_headers", value=cors_headers, expected_type=type_hints["cors_headers"])
            check_type(argname="argument custom_deny_message", value=custom_deny_message, expected_type=type_hints["custom_deny_message"])
            check_type(argname="argument custom_deny_url", value=custom_deny_url, expected_type=type_hints["custom_deny_url"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument enable_binding_cookie", value=enable_binding_cookie, expected_type=type_hints["enable_binding_cookie"])
            check_type(argname="argument http_only_cookie_attribute", value=http_only_cookie_attribute, expected_type=type_hints["http_only_cookie_attribute"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logo_url", value=logo_url, expected_type=type_hints["logo_url"])
            check_type(argname="argument saas_app", value=saas_app, expected_type=type_hints["saas_app"])
            check_type(argname="argument same_site_cookie_attribute", value=same_site_cookie_attribute, expected_type=type_hints["same_site_cookie_attribute"])
            check_type(argname="argument service_auth401_redirect", value=service_auth401_redirect, expected_type=type_hints["service_auth401_redirect"])
            check_type(argname="argument session_duration", value=session_duration, expected_type=type_hints["session_duration"])
            check_type(argname="argument skip_interstitial", value=skip_interstitial, expected_type=type_hints["skip_interstitial"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if allowed_idps is not None:
            self._values["allowed_idps"] = allowed_idps
        if app_launcher_visible is not None:
            self._values["app_launcher_visible"] = app_launcher_visible
        if auto_redirect_to_identity is not None:
            self._values["auto_redirect_to_identity"] = auto_redirect_to_identity
        if cors_headers is not None:
            self._values["cors_headers"] = cors_headers
        if custom_deny_message is not None:
            self._values["custom_deny_message"] = custom_deny_message
        if custom_deny_url is not None:
            self._values["custom_deny_url"] = custom_deny_url
        if domain is not None:
            self._values["domain"] = domain
        if enable_binding_cookie is not None:
            self._values["enable_binding_cookie"] = enable_binding_cookie
        if http_only_cookie_attribute is not None:
            self._values["http_only_cookie_attribute"] = http_only_cookie_attribute
        if id is not None:
            self._values["id"] = id
        if logo_url is not None:
            self._values["logo_url"] = logo_url
        if saas_app is not None:
            self._values["saas_app"] = saas_app
        if same_site_cookie_attribute is not None:
            self._values["same_site_cookie_attribute"] = same_site_cookie_attribute
        if service_auth401_redirect is not None:
            self._values["service_auth401_redirect"] = service_auth401_redirect
        if session_duration is not None:
            self._values["session_duration"] = session_duration
        if skip_interstitial is not None:
            self._values["skip_interstitial"] = skip_interstitial
        if type is not None:
            self._values["type"] = type
        if zone_id is not None:
            self._values["zone_id"] = zone_id

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
        '''Friendly name of the Access Application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#name AccessApplication#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource. Conflicts with ``zone_id``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#account_id AccessApplication#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allowed_idps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identity providers selected for the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allowed_idps AccessApplication#allowed_idps}
        '''
        result = self._values.get("allowed_idps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def app_launcher_visible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to show/hide applications in App Launcher. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#app_launcher_visible AccessApplication#app_launcher_visible}
        '''
        result = self._values.get("app_launcher_visible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_redirect_to_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to skip identity provider selection if only one is configured in ``allowed_idps``. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#auto_redirect_to_identity AccessApplication#auto_redirect_to_identity}
        '''
        result = self._values.get("auto_redirect_to_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cors_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationCorsHeaders"]]]:
        '''cors_headers block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#cors_headers AccessApplication#cors_headers}
        '''
        result = self._values.get("cors_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationCorsHeaders"]]], result)

    @builtins.property
    def custom_deny_message(self) -> typing.Optional[builtins.str]:
        '''Option that returns a custom error message when a user is denied access to the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#custom_deny_message AccessApplication#custom_deny_message}
        '''
        result = self._values.get("custom_deny_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_deny_url(self) -> typing.Optional[builtins.str]:
        '''Option that redirects to a custom URL when a user is denied access to the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#custom_deny_url AccessApplication#custom_deny_url}
        '''
        result = self._values.get("custom_deny_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The complete URL of the asset you wish to put Cloudflare Access in front of.

        Can include subdomains or paths. Or both.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#domain AccessApplication#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_binding_cookie(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to provide increased security against compromised authorization tokens and CSRF attacks by requiring an additional "binding" cookie on requests.

        Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#enable_binding_cookie AccessApplication#enable_binding_cookie}
        '''
        result = self._values.get("enable_binding_cookie")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_only_cookie_attribute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to add the ``HttpOnly`` cookie flag to access tokens.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#http_only_cookie_attribute AccessApplication#http_only_cookie_attribute}
        '''
        result = self._values.get("http_only_cookie_attribute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#id AccessApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo_url(self) -> typing.Optional[builtins.str]:
        '''Image URL for the logo shown in the app launcher dashboard.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#logo_url AccessApplication#logo_url}
        '''
        result = self._values.get("logo_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saas_app(self) -> typing.Optional["AccessApplicationSaasApp"]:
        '''saas_app block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#saas_app AccessApplication#saas_app}
        '''
        result = self._values.get("saas_app")
        return typing.cast(typing.Optional["AccessApplicationSaasApp"], result)

    @builtins.property
    def same_site_cookie_attribute(self) -> typing.Optional[builtins.str]:
        '''Defines the same-site cookie setting for access tokens. Available values: ``none``, ``lax``, ``strict``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#same_site_cookie_attribute AccessApplication#same_site_cookie_attribute}
        '''
        result = self._values.get("same_site_cookie_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_auth401_redirect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to return a 401 status code in service authentication rules on failed requests. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#service_auth_401_redirect AccessApplication#service_auth_401_redirect}
        '''
        result = self._values.get("service_auth401_redirect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def session_duration(self) -> typing.Optional[builtins.str]:
        '''How often a user will be forced to re-authorise.

        Must be in the format ``48h`` or ``2h45m``. Defaults to ``24h``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#session_duration AccessApplication#session_duration}
        '''
        result = self._values.get("session_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_interstitial(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to skip the authorization interstitial when using the CLI. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#skip_interstitial AccessApplication#skip_interstitial}
        '''
        result = self._values.get("skip_interstitial")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The application type. Available values: ``app_launcher``, ``bookmark``, ``biso``, ``dash_sso``, ``saas``, ``self_hosted``, ``ssh``, ``vnc``, ``warp``. Defaults to ``self_hosted``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#type AccessApplication#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''The zone identifier to target for the resource. Conflicts with ``account_id``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#zone_id AccessApplication#zone_id}
        '''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationCorsHeaders",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all_headers": "allowAllHeaders",
        "allow_all_methods": "allowAllMethods",
        "allow_all_origins": "allowAllOrigins",
        "allow_credentials": "allowCredentials",
        "allowed_headers": "allowedHeaders",
        "allowed_methods": "allowedMethods",
        "allowed_origins": "allowedOrigins",
        "max_age": "maxAge",
    },
)
class AccessApplicationCorsHeaders:
    def __init__(
        self,
        *,
        allow_all_headers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_all_methods: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_all_origins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_age: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allow_all_headers: Value to determine whether all HTTP headers are exposed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allow_all_headers AccessApplication#allow_all_headers}
        :param allow_all_methods: Value to determine whether all methods are exposed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allow_all_methods AccessApplication#allow_all_methods}
        :param allow_all_origins: Value to determine whether all origins are permitted to make CORS requests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allow_all_origins AccessApplication#allow_all_origins}
        :param allow_credentials: Value to determine if credentials (cookies, authorization headers, or TLS client certificates) are included with requests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allow_credentials AccessApplication#allow_credentials}
        :param allowed_headers: List of HTTP headers to expose via CORS. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allowed_headers AccessApplication#allowed_headers}
        :param allowed_methods: List of methods to expose via CORS. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allowed_methods AccessApplication#allowed_methods}
        :param allowed_origins: List of origins permitted to make CORS requests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allowed_origins AccessApplication#allowed_origins}
        :param max_age: The maximum time a preflight request will be cached. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#max_age AccessApplication#max_age}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae525a77bbd533b13658910162a82a7ed82713ce55fbce6efb2802432bd142ee)
            check_type(argname="argument allow_all_headers", value=allow_all_headers, expected_type=type_hints["allow_all_headers"])
            check_type(argname="argument allow_all_methods", value=allow_all_methods, expected_type=type_hints["allow_all_methods"])
            check_type(argname="argument allow_all_origins", value=allow_all_origins, expected_type=type_hints["allow_all_origins"])
            check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
            check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_all_headers is not None:
            self._values["allow_all_headers"] = allow_all_headers
        if allow_all_methods is not None:
            self._values["allow_all_methods"] = allow_all_methods
        if allow_all_origins is not None:
            self._values["allow_all_origins"] = allow_all_origins
        if allow_credentials is not None:
            self._values["allow_credentials"] = allow_credentials
        if allowed_headers is not None:
            self._values["allowed_headers"] = allowed_headers
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if allowed_origins is not None:
            self._values["allowed_origins"] = allowed_origins
        if max_age is not None:
            self._values["max_age"] = max_age

    @builtins.property
    def allow_all_headers(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Value to determine whether all HTTP headers are exposed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allow_all_headers AccessApplication#allow_all_headers}
        '''
        result = self._values.get("allow_all_headers")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_all_methods(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Value to determine whether all methods are exposed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allow_all_methods AccessApplication#allow_all_methods}
        '''
        result = self._values.get("allow_all_methods")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_all_origins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Value to determine whether all origins are permitted to make CORS requests.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allow_all_origins AccessApplication#allow_all_origins}
        '''
        result = self._values.get("allow_all_origins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Value to determine if credentials (cookies, authorization headers, or TLS client certificates) are included with requests.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allow_credentials AccessApplication#allow_credentials}
        '''
        result = self._values.get("allow_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of HTTP headers to expose via CORS.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allowed_headers AccessApplication#allowed_headers}
        '''
        result = self._values.get("allowed_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of methods to expose via CORS.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allowed_methods AccessApplication#allowed_methods}
        '''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of origins permitted to make CORS requests.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#allowed_origins AccessApplication#allowed_origins}
        '''
        result = self._values.get("allowed_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_age(self) -> typing.Optional[jsii.Number]:
        '''The maximum time a preflight request will be cached.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#max_age AccessApplication#max_age}
        '''
        result = self._values.get("max_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationCorsHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationCorsHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationCorsHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa79530a53dc744124aeaa81632fbdff14a0c4535f89c37afd43ab415cf95406)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessApplicationCorsHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9b295611563f5e8579389c0b30ac3bf53a4e5471f1f6906f361865e1f6d68f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessApplicationCorsHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f63511a0bcc23c92f8a3b522588cef9af4c9489d92aa783dbc643495ee3a006)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5991c119e726e4e5bae94364d64d111ba5d06dc1fd9a77feeef6241923a1b94c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fed799de136d9a06f6402f513b16198e0f010bfa196b8637c9b9f3a949842696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationCorsHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationCorsHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationCorsHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f784385a2e46f6e296c6f09c5dd838571dd28c3c939ef8fe647709d9c6b0fbef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessApplicationCorsHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationCorsHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c91640a7618248ee2dfbc3c623b9f3d2ccaf579d2752459b82e8c1069a4b359b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowAllHeaders")
    def reset_allow_all_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAllHeaders", []))

    @jsii.member(jsii_name="resetAllowAllMethods")
    def reset_allow_all_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAllMethods", []))

    @jsii.member(jsii_name="resetAllowAllOrigins")
    def reset_allow_all_origins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAllOrigins", []))

    @jsii.member(jsii_name="resetAllowCredentials")
    def reset_allow_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowCredentials", []))

    @jsii.member(jsii_name="resetAllowedHeaders")
    def reset_allowed_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedHeaders", []))

    @jsii.member(jsii_name="resetAllowedMethods")
    def reset_allowed_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedMethods", []))

    @jsii.member(jsii_name="resetAllowedOrigins")
    def reset_allowed_origins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedOrigins", []))

    @jsii.member(jsii_name="resetMaxAge")
    def reset_max_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAge", []))

    @builtins.property
    @jsii.member(jsii_name="allowAllHeadersInput")
    def allow_all_headers_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAllMethodsInput")
    def allow_all_methods_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAllOriginsInput")
    def allow_all_origins_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowCredentialsInput")
    def allow_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHeadersInput")
    def allowed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInput")
    def max_age_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAllHeaders")
    def allow_all_headers(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAllHeaders"))

    @allow_all_headers.setter
    def allow_all_headers(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3400b2ef69eb057e299d971eff385016e19ae0c0fb70f69517fb2389bf4455f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllHeaders", value)

    @builtins.property
    @jsii.member(jsii_name="allowAllMethods")
    def allow_all_methods(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAllMethods"))

    @allow_all_methods.setter
    def allow_all_methods(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe554ac39141e522d8cea4b0d84ca98b7e0c53123791c7cdc321b0a2a08c5f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllMethods", value)

    @builtins.property
    @jsii.member(jsii_name="allowAllOrigins")
    def allow_all_origins(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAllOrigins"))

    @allow_all_origins.setter
    def allow_all_origins(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791c3f6bfef6cb602668374e7ae4047e3cfe4fc8175da1ef5ef7b9f90146a893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllOrigins", value)

    @builtins.property
    @jsii.member(jsii_name="allowCredentials")
    def allow_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowCredentials"))

    @allow_credentials.setter
    def allow_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0cb5c457ec28d6691034d2841ed4bb6cde403ab39fc573324082e69e28e0ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCredentials", value)

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d5f5968daf5e6d30f2140162a6148b40fadf726eae33a4a24238a304102543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value)

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19571719f469919945233bc1181996c44217f31151077b2376da3c869255841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value)

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9790848826046a2cbfaf9752da2eac0aaf648d202e86c384d87ff3c8a5f41d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value)

    @builtins.property
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAge"))

    @max_age.setter
    def max_age(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6437b4b77a62619bca135ac9848d2ea144d0abbfa730ca8b0efe1bb71cae125d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAge", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessApplicationCorsHeaders, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessApplicationCorsHeaders, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessApplicationCorsHeaders, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f6f5c209667b44cb9092177c7fc64e8a78842aad5f7b1d5d1deb26e1c660cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasApp",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_service_url": "consumerServiceUrl",
        "sp_entity_id": "spEntityId",
        "name_id_format": "nameIdFormat",
    },
)
class AccessApplicationSaasApp:
    def __init__(
        self,
        *,
        consumer_service_url: builtins.str,
        sp_entity_id: builtins.str,
        name_id_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_service_url: The service provider's endpoint that is responsible for receiving and parsing a SAML assertion. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#consumer_service_url AccessApplication#consumer_service_url}
        :param sp_entity_id: A globally unique name for an identity or service provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#sp_entity_id AccessApplication#sp_entity_id}
        :param name_id_format: The format of the name identifier sent to the SaaS application. Defaults to ``email``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#name_id_format AccessApplication#name_id_format}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cefbcedc5818578827cb55f910f5dea7e97d62fc19dd39c031f17cb5f5aab3)
            check_type(argname="argument consumer_service_url", value=consumer_service_url, expected_type=type_hints["consumer_service_url"])
            check_type(argname="argument sp_entity_id", value=sp_entity_id, expected_type=type_hints["sp_entity_id"])
            check_type(argname="argument name_id_format", value=name_id_format, expected_type=type_hints["name_id_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_service_url": consumer_service_url,
            "sp_entity_id": sp_entity_id,
        }
        if name_id_format is not None:
            self._values["name_id_format"] = name_id_format

    @builtins.property
    def consumer_service_url(self) -> builtins.str:
        '''The service provider's endpoint that is responsible for receiving and parsing a SAML assertion.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#consumer_service_url AccessApplication#consumer_service_url}
        '''
        result = self._values.get("consumer_service_url")
        assert result is not None, "Required property 'consumer_service_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sp_entity_id(self) -> builtins.str:
        '''A globally unique name for an identity or service provider.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#sp_entity_id AccessApplication#sp_entity_id}
        '''
        result = self._values.get("sp_entity_id")
        assert result is not None, "Required property 'sp_entity_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_id_format(self) -> typing.Optional[builtins.str]:
        '''The format of the name identifier sent to the SaaS application. Defaults to ``email``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_application#name_id_format AccessApplication#name_id_format}
        '''
        result = self._values.get("name_id_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationSaasApp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationSaasAppOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49168f3c8353cfd81f0c05971d66ca3a23f81a2cb09b93d61892c2ae6a801eb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNameIdFormat")
    def reset_name_id_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameIdFormat", []))

    @builtins.property
    @jsii.member(jsii_name="consumerServiceUrlInput")
    def consumer_service_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerServiceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="nameIdFormatInput")
    def name_id_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameIdFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="spEntityIdInput")
    def sp_entity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spEntityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerServiceUrl")
    def consumer_service_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerServiceUrl"))

    @consumer_service_url.setter
    def consumer_service_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e94a2c28088cf7cc662f244a3f800bf1bf54bac516d83076959956f11517c51c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerServiceUrl", value)

    @builtins.property
    @jsii.member(jsii_name="nameIdFormat")
    def name_id_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameIdFormat"))

    @name_id_format.setter
    def name_id_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e605787461dbd21e4a28b56ec15784c6ac133b55608b68e396120360939e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameIdFormat", value)

    @builtins.property
    @jsii.member(jsii_name="spEntityId")
    def sp_entity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spEntityId"))

    @sp_entity_id.setter
    def sp_entity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e2db75ff078ba5cfb1e5cc189d0cc7fd9055c50ea203b8f89249c650476a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spEntityId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccessApplicationSaasApp]:
        return typing.cast(typing.Optional[AccessApplicationSaasApp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AccessApplicationSaasApp]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c590519c61fb7e78a61063bc0819ff040f76e71d44e537d2447a1a19229fc1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AccessApplication",
    "AccessApplicationConfig",
    "AccessApplicationCorsHeaders",
    "AccessApplicationCorsHeadersList",
    "AccessApplicationCorsHeadersOutputReference",
    "AccessApplicationSaasApp",
    "AccessApplicationSaasAppOutputReference",
]

publication.publish()

def _typecheckingstub__c1b2963f98659b9017b97318b2a37e45b5084f4b60cafaa3bcd97429790c8eb1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    allowed_idps: typing.Optional[typing.Sequence[builtins.str]] = None,
    app_launcher_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_redirect_to_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationCorsHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_deny_message: typing.Optional[builtins.str] = None,
    custom_deny_url: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logo_url: typing.Optional[builtins.str] = None,
    saas_app: typing.Optional[typing.Union[AccessApplicationSaasApp, typing.Dict[builtins.str, typing.Any]]] = None,
    same_site_cookie_attribute: typing.Optional[builtins.str] = None,
    service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_duration: typing.Optional[builtins.str] = None,
    skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
    zone_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__1f0c9359a2094e6a5d995e98fae21fbe1877ef3aca4c5f09eb4d19306fa8750c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationCorsHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81fb38f689b4bf068fc2e8ba83e0a3ec1a53465fe9ca9bf20ef28753a9f80251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daff490d3a8108f46fe8affbe607ed3bfce7f0caa97c3a01158863a2d9b81e73(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fe33b6a3e0de6c5d2332cddc4e94399f81b3f96589f00d5cea096ca5c90e89(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02da31929754ab70993542e7f44f5e3b8ff2a4113ea0e7fc09dccad505e190e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7394b2b4e1199550fbe6375395d12db57b5a15a49a4d5b7355d6ce5ad25636e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bda6e3a2399b050e18d5c2bc8f4883cf54b73d8211f3d0847551f970d6b384e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcbe163ed94bb0a50cb8b1b9b52ea152aa192b9bd50115601e6ab1b87eaf861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffea86ba305f92fcd8ef5768d2698c4bf9c262d3a7e35de9c4bbf7711be2159(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b7a56cc0c2523d37beeaca9d4af0ffe258c84ad7cd8666034d44c91b2c0a5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cee610faa04b0d8e65aad04b0e960f1a472af48d19258d665b5edfc30e57e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94205b9b871f765a94dff73949e655473bf7b6ffab02f41b2a507b924040f1a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408052199c5db90c8698c809b74ffc55459b674605e439d3b3bfd8a083255a13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a95c47163bc493ca9389335db25497d901b8dedf1f1549f91f1f323ea93a62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad3bbb24317d5f07a9fb5037e763a244642bebdc8fa18f8d948e52201c04187(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adfb91cb0ee9996051ba552f920aa96e9da21960ed72cf49353e36a46107d982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b86799f85043068c1b6ac6d68b67ebdd5dc15341cb709a8eeccbecf097cf147(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ac6df2597f216a2f0ef7d91eff615dd9bd4f92bf47b2a9e51dec9e2a97df20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f33c40394937d1eb21e9c367c96d3212115f53970a6ffb9db1ab2ecac777b19f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f785d33e1451f1cf27417eb2776a2d793dff777b28167e528be38cf2a13a8faa(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    allowed_idps: typing.Optional[typing.Sequence[builtins.str]] = None,
    app_launcher_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_redirect_to_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationCorsHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_deny_message: typing.Optional[builtins.str] = None,
    custom_deny_url: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logo_url: typing.Optional[builtins.str] = None,
    saas_app: typing.Optional[typing.Union[AccessApplicationSaasApp, typing.Dict[builtins.str, typing.Any]]] = None,
    same_site_cookie_attribute: typing.Optional[builtins.str] = None,
    service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_duration: typing.Optional[builtins.str] = None,
    skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae525a77bbd533b13658910162a82a7ed82713ce55fbce6efb2802432bd142ee(
    *,
    allow_all_headers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_all_methods: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_all_origins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_age: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa79530a53dc744124aeaa81632fbdff14a0c4535f89c37afd43ab415cf95406(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9b295611563f5e8579389c0b30ac3bf53a4e5471f1f6906f361865e1f6d68f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f63511a0bcc23c92f8a3b522588cef9af4c9489d92aa783dbc643495ee3a006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5991c119e726e4e5bae94364d64d111ba5d06dc1fd9a77feeef6241923a1b94c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed799de136d9a06f6402f513b16198e0f010bfa196b8637c9b9f3a949842696(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f784385a2e46f6e296c6f09c5dd838571dd28c3c939ef8fe647709d9c6b0fbef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationCorsHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91640a7618248ee2dfbc3c623b9f3d2ccaf579d2752459b82e8c1069a4b359b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3400b2ef69eb057e299d971eff385016e19ae0c0fb70f69517fb2389bf4455f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe554ac39141e522d8cea4b0d84ca98b7e0c53123791c7cdc321b0a2a08c5f1e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791c3f6bfef6cb602668374e7ae4047e3cfe4fc8175da1ef5ef7b9f90146a893(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0cb5c457ec28d6691034d2841ed4bb6cde403ab39fc573324082e69e28e0ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d5f5968daf5e6d30f2140162a6148b40fadf726eae33a4a24238a304102543(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19571719f469919945233bc1181996c44217f31151077b2376da3c869255841(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9790848826046a2cbfaf9752da2eac0aaf648d202e86c384d87ff3c8a5f41d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6437b4b77a62619bca135ac9848d2ea144d0abbfa730ca8b0efe1bb71cae125d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f6f5c209667b44cb9092177c7fc64e8a78842aad5f7b1d5d1deb26e1c660cf(
    value: typing.Optional[typing.Union[AccessApplicationCorsHeaders, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cefbcedc5818578827cb55f910f5dea7e97d62fc19dd39c031f17cb5f5aab3(
    *,
    consumer_service_url: builtins.str,
    sp_entity_id: builtins.str,
    name_id_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49168f3c8353cfd81f0c05971d66ca3a23f81a2cb09b93d61892c2ae6a801eb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e94a2c28088cf7cc662f244a3f800bf1bf54bac516d83076959956f11517c51c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e605787461dbd21e4a28b56ec15784c6ac133b55608b68e396120360939e14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e2db75ff078ba5cfb1e5cc189d0cc7fd9055c50ea203b8f89249c650476a6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c590519c61fb7e78a61063bc0819ff040f76e71d44e537d2447a1a19229fc1d(
    value: typing.Optional[AccessApplicationSaasApp],
) -> None:
    """Type checking stubs"""
    pass
