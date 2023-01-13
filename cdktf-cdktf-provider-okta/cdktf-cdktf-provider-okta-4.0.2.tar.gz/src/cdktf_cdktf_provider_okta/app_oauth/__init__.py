'''
# `okta_app_oauth`

Refer to the Terraform Registory for docs: [`okta_app_oauth`](https://www.terraform.io/docs/providers/okta/r/app_oauth).
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


class AppOauth(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appOauth.AppOauth",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/app_oauth okta_app_oauth}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        label: builtins.str,
        type: builtins.str,
        accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        app_settings_json: typing.Optional[builtins.str] = None,
        authentication_policy: typing.Optional[builtins.str] = None,
        auto_key_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_basic_secret: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_uri: typing.Optional[builtins.str] = None,
        consent_method: typing.Optional[builtins.str] = None,
        custom_client_id: typing.Optional[builtins.str] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        grant_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_claim: typing.Optional[typing.Union["AppOauthGroupsClaim", typing.Dict[builtins.str, typing.Any]]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        jwks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppOauthJwks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        login_mode: typing.Optional[builtins.str] = None,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_uri: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        logo_uri: typing.Optional[builtins.str] = None,
        omit_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pkce_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_uri: typing.Optional[builtins.str] = None,
        post_logout_redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        profile: typing.Optional[builtins.str] = None,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        refresh_token_leeway: typing.Optional[jsii.Number] = None,
        refresh_token_rotation: typing.Optional[builtins.str] = None,
        response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AppOauthTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        token_endpoint_auth_method: typing.Optional[builtins.str] = None,
        tos_uri: typing.Optional[builtins.str] = None,
        user_name_template: typing.Optional[builtins.str] = None,
        user_name_template_push_status: typing.Optional[builtins.str] = None,
        user_name_template_suffix: typing.Optional[builtins.str] = None,
        user_name_template_type: typing.Optional[builtins.str] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppOauthUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        wildcard_redirect: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/app_oauth okta_app_oauth} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#label AppOauth#label}
        :param type: The type of client application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#type AppOauth#type}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#accessibility_error_redirect_url AppOauth#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#accessibility_login_redirect_url AppOauth#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#accessibility_self_service AppOauth#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#admin_note AppOauth#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#app_links_json AppOauth#app_links_json}
        :param app_settings_json: Application settings in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#app_settings_json AppOauth#app_settings_json}
        :param authentication_policy: Id of this apps authentication policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#authentication_policy AppOauth#authentication_policy}
        :param auto_key_rotation: Requested key rotation mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#auto_key_rotation AppOauth#auto_key_rotation}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#auto_submit_toolbar AppOauth#auto_submit_toolbar}
        :param client_basic_secret: OAuth client secret key, this can be set when token_endpoint_auth_method is client_secret_basic. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#client_basic_secret AppOauth#client_basic_secret}
        :param client_id: OAuth client ID. If set during creation, app is created with this id. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#client_id AppOauth#client_id}
        :param client_uri: URI to a web page providing information about the client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#client_uri AppOauth#client_uri}
        :param consent_method: *Early Access Property*. Indicates whether user consent is required or implicit. Valid values: REQUIRED, TRUSTED. Default value is TRUSTED. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#consent_method AppOauth#consent_method}
        :param custom_client_id: **Deprecated** This property allows you to set your client_id during creation. NOTE: updating after creation will be a no-op, use client_id for that behavior instead. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#custom_client_id AppOauth#custom_client_id}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#enduser_note AppOauth#enduser_note}
        :param grant_types: List of OAuth 2.0 grant types. Conditional validation params found here https://developer.okta.com/docs/api/resources/apps#credentials-settings-details. Defaults to minimum requirements per app type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#grant_types AppOauth#grant_types}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#groups AppOauth#groups}
        :param groups_claim: groups_claim block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#groups_claim AppOauth#groups_claim}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#hide_ios AppOauth#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#hide_web AppOauth#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#id AppOauth#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param implicit_assignment: *Early Access Property*. Enable Federation Broker Mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#implicit_assignment AppOauth#implicit_assignment}
        :param issuer_mode: *Early Access Property*. Indicates whether the Okta Authorization Server uses the original Okta org domain URL or a custom domain URL as the issuer of ID token for this client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#issuer_mode AppOauth#issuer_mode}
        :param jwks: jwks block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#jwks AppOauth#jwks}
        :param login_mode: The type of Idp-Initiated login that the client supports, if any. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#login_mode AppOauth#login_mode}
        :param login_scopes: List of scopes to use for the request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#login_scopes AppOauth#login_scopes}
        :param login_uri: URI that initiates login. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#login_uri AppOauth#login_uri}
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#logo AppOauth#logo}
        :param logo_uri: URI that references a logo for the client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#logo_uri AppOauth#logo_uri}
        :param omit_secret: This tells the provider not to persist the application's secret to state. If this is ever changes from true => false your app will be recreated. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#omit_secret AppOauth#omit_secret}
        :param pkce_required: Require Proof Key for Code Exchange (PKCE) for additional verification key rotation mode. See: https://developer.okta.com/docs/reference/api/apps/#oauth-credential-object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#pkce_required AppOauth#pkce_required}
        :param policy_uri: URI to web page providing client policy document. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#policy_uri AppOauth#policy_uri}
        :param post_logout_redirect_uris: List of URIs for redirection after logout. Note: see okta_app_oauth_post_logout_redirect_uri for appending to this list in a decentralized way. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#post_logout_redirect_uris AppOauth#post_logout_redirect_uris}
        :param profile: Custom JSON that represents an OAuth application's profile. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#profile AppOauth#profile}
        :param redirect_uris: List of URIs for use in the redirect-based flow. This is required for all application types except service. Note: see okta_app_oauth_redirect_uri for appending to this list in a decentralized way. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#redirect_uris AppOauth#redirect_uris}
        :param refresh_token_leeway: *Early Access Property* Grace period for token rotation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#refresh_token_leeway AppOauth#refresh_token_leeway}
        :param refresh_token_rotation: *Early Access Property* Refresh token rotation behavior. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#refresh_token_rotation AppOauth#refresh_token_rotation}
        :param response_types: List of OAuth 2.0 response type strings. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#response_types AppOauth#response_types}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#skip_groups AppOauth#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#skip_users AppOauth#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#status AppOauth#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#timeouts AppOauth#timeouts}
        :param token_endpoint_auth_method: Requested authentication method for the token endpoint. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#token_endpoint_auth_method AppOauth#token_endpoint_auth_method}
        :param tos_uri: URI to web page providing client tos (terms of service). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#tos_uri AppOauth#tos_uri}
        :param user_name_template: Username template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template AppOauth#user_name_template}
        :param user_name_template_push_status: Push username on update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template_push_status AppOauth#user_name_template_push_status}
        :param user_name_template_suffix: Username template suffix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template_suffix AppOauth#user_name_template_suffix}
        :param user_name_template_type: Username template type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template_type AppOauth#user_name_template_type}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#users AppOauth#users}
        :param wildcard_redirect: *Early Access Property*. Indicates if the client is allowed to use wildcard matching of redirect_uris. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#wildcard_redirect AppOauth#wildcard_redirect}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722860bbe40b36ca8dadfe7af7aeadfd64e57454389a7290203d05a0bea678d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppOauthConfig(
            label=label,
            type=type,
            accessibility_error_redirect_url=accessibility_error_redirect_url,
            accessibility_login_redirect_url=accessibility_login_redirect_url,
            accessibility_self_service=accessibility_self_service,
            admin_note=admin_note,
            app_links_json=app_links_json,
            app_settings_json=app_settings_json,
            authentication_policy=authentication_policy,
            auto_key_rotation=auto_key_rotation,
            auto_submit_toolbar=auto_submit_toolbar,
            client_basic_secret=client_basic_secret,
            client_id=client_id,
            client_uri=client_uri,
            consent_method=consent_method,
            custom_client_id=custom_client_id,
            enduser_note=enduser_note,
            grant_types=grant_types,
            groups=groups,
            groups_claim=groups_claim,
            hide_ios=hide_ios,
            hide_web=hide_web,
            id=id,
            implicit_assignment=implicit_assignment,
            issuer_mode=issuer_mode,
            jwks=jwks,
            login_mode=login_mode,
            login_scopes=login_scopes,
            login_uri=login_uri,
            logo=logo,
            logo_uri=logo_uri,
            omit_secret=omit_secret,
            pkce_required=pkce_required,
            policy_uri=policy_uri,
            post_logout_redirect_uris=post_logout_redirect_uris,
            profile=profile,
            redirect_uris=redirect_uris,
            refresh_token_leeway=refresh_token_leeway,
            refresh_token_rotation=refresh_token_rotation,
            response_types=response_types,
            skip_groups=skip_groups,
            skip_users=skip_users,
            status=status,
            timeouts=timeouts,
            token_endpoint_auth_method=token_endpoint_auth_method,
            tos_uri=tos_uri,
            user_name_template=user_name_template,
            user_name_template_push_status=user_name_template_push_status,
            user_name_template_suffix=user_name_template_suffix,
            user_name_template_type=user_name_template_type,
            users=users,
            wildcard_redirect=wildcard_redirect,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putGroupsClaim")
    def put_groups_claim(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        value: builtins.str,
        filter_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the claim that will be used in the token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#name AppOauth#name}
        :param type: Groups claim type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#type AppOauth#type}
        :param value: Value of the claim. Can be an Okta Expression Language statement that evaluates at the time the token is minted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#value AppOauth#value}
        :param filter_type: Groups claim filter. Can only be set if type is FILTER. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#filter_type AppOauth#filter_type}
        '''
        value_ = AppOauthGroupsClaim(
            name=name, type=type, value=value, filter_type=filter_type
        )

        return typing.cast(None, jsii.invoke(self, "putGroupsClaim", [value_]))

    @jsii.member(jsii_name="putJwks")
    def put_jwks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppOauthJwks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e81a848a5a70548b51f782b8896c63fbfa5f341f284e8157aca6342fa8599e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putJwks", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#create AppOauth#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#read AppOauth#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#update AppOauth#update}.
        '''
        value = AppOauthTimeouts(create=create, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUsers")
    def put_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppOauthUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7923c87358beeebc92e19628c1bfdf70ddb796f5fc666947734e6f0f3890889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUsers", [value]))

    @jsii.member(jsii_name="resetAccessibilityErrorRedirectUrl")
    def reset_accessibility_error_redirect_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessibilityErrorRedirectUrl", []))

    @jsii.member(jsii_name="resetAccessibilityLoginRedirectUrl")
    def reset_accessibility_login_redirect_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessibilityLoginRedirectUrl", []))

    @jsii.member(jsii_name="resetAccessibilitySelfService")
    def reset_accessibility_self_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessibilitySelfService", []))

    @jsii.member(jsii_name="resetAdminNote")
    def reset_admin_note(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminNote", []))

    @jsii.member(jsii_name="resetAppLinksJson")
    def reset_app_links_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppLinksJson", []))

    @jsii.member(jsii_name="resetAppSettingsJson")
    def reset_app_settings_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSettingsJson", []))

    @jsii.member(jsii_name="resetAuthenticationPolicy")
    def reset_authentication_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationPolicy", []))

    @jsii.member(jsii_name="resetAutoKeyRotation")
    def reset_auto_key_rotation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoKeyRotation", []))

    @jsii.member(jsii_name="resetAutoSubmitToolbar")
    def reset_auto_submit_toolbar(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoSubmitToolbar", []))

    @jsii.member(jsii_name="resetClientBasicSecret")
    def reset_client_basic_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientBasicSecret", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientUri")
    def reset_client_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientUri", []))

    @jsii.member(jsii_name="resetConsentMethod")
    def reset_consent_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsentMethod", []))

    @jsii.member(jsii_name="resetCustomClientId")
    def reset_custom_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomClientId", []))

    @jsii.member(jsii_name="resetEnduserNote")
    def reset_enduser_note(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnduserNote", []))

    @jsii.member(jsii_name="resetGrantTypes")
    def reset_grant_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrantTypes", []))

    @jsii.member(jsii_name="resetGroups")
    def reset_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroups", []))

    @jsii.member(jsii_name="resetGroupsClaim")
    def reset_groups_claim(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsClaim", []))

    @jsii.member(jsii_name="resetHideIos")
    def reset_hide_ios(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHideIos", []))

    @jsii.member(jsii_name="resetHideWeb")
    def reset_hide_web(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHideWeb", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImplicitAssignment")
    def reset_implicit_assignment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImplicitAssignment", []))

    @jsii.member(jsii_name="resetIssuerMode")
    def reset_issuer_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuerMode", []))

    @jsii.member(jsii_name="resetJwks")
    def reset_jwks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwks", []))

    @jsii.member(jsii_name="resetLoginMode")
    def reset_login_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginMode", []))

    @jsii.member(jsii_name="resetLoginScopes")
    def reset_login_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginScopes", []))

    @jsii.member(jsii_name="resetLoginUri")
    def reset_login_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginUri", []))

    @jsii.member(jsii_name="resetLogo")
    def reset_logo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogo", []))

    @jsii.member(jsii_name="resetLogoUri")
    def reset_logo_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogoUri", []))

    @jsii.member(jsii_name="resetOmitSecret")
    def reset_omit_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOmitSecret", []))

    @jsii.member(jsii_name="resetPkceRequired")
    def reset_pkce_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPkceRequired", []))

    @jsii.member(jsii_name="resetPolicyUri")
    def reset_policy_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyUri", []))

    @jsii.member(jsii_name="resetPostLogoutRedirectUris")
    def reset_post_logout_redirect_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostLogoutRedirectUris", []))

    @jsii.member(jsii_name="resetProfile")
    def reset_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfile", []))

    @jsii.member(jsii_name="resetRedirectUris")
    def reset_redirect_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUris", []))

    @jsii.member(jsii_name="resetRefreshTokenLeeway")
    def reset_refresh_token_leeway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshTokenLeeway", []))

    @jsii.member(jsii_name="resetRefreshTokenRotation")
    def reset_refresh_token_rotation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshTokenRotation", []))

    @jsii.member(jsii_name="resetResponseTypes")
    def reset_response_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseTypes", []))

    @jsii.member(jsii_name="resetSkipGroups")
    def reset_skip_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipGroups", []))

    @jsii.member(jsii_name="resetSkipUsers")
    def reset_skip_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipUsers", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTokenEndpointAuthMethod")
    def reset_token_endpoint_auth_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenEndpointAuthMethod", []))

    @jsii.member(jsii_name="resetTosUri")
    def reset_tos_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTosUri", []))

    @jsii.member(jsii_name="resetUserNameTemplate")
    def reset_user_name_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserNameTemplate", []))

    @jsii.member(jsii_name="resetUserNameTemplatePushStatus")
    def reset_user_name_template_push_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserNameTemplatePushStatus", []))

    @jsii.member(jsii_name="resetUserNameTemplateSuffix")
    def reset_user_name_template_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserNameTemplateSuffix", []))

    @jsii.member(jsii_name="resetUserNameTemplateType")
    def reset_user_name_template_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserNameTemplateType", []))

    @jsii.member(jsii_name="resetUsers")
    def reset_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsers", []))

    @jsii.member(jsii_name="resetWildcardRedirect")
    def reset_wildcard_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWildcardRedirect", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="groupsClaim")
    def groups_claim(self) -> "AppOauthGroupsClaimOutputReference":
        return typing.cast("AppOauthGroupsClaimOutputReference", jsii.get(self, "groupsClaim"))

    @builtins.property
    @jsii.member(jsii_name="jwks")
    def jwks(self) -> "AppOauthJwksList":
        return typing.cast("AppOauthJwksList", jsii.get(self, "jwks"))

    @builtins.property
    @jsii.member(jsii_name="logoUrl")
    def logo_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoUrl"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="signOnMode")
    def sign_on_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signOnMode"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AppOauthTimeoutsOutputReference":
        return typing.cast("AppOauthTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> "AppOauthUsersList":
        return typing.cast("AppOauthUsersList", jsii.get(self, "users"))

    @builtins.property
    @jsii.member(jsii_name="accessibilityErrorRedirectUrlInput")
    def accessibility_error_redirect_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessibilityErrorRedirectUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="accessibilityLoginRedirectUrlInput")
    def accessibility_login_redirect_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessibilityLoginRedirectUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="accessibilitySelfServiceInput")
    def accessibility_self_service_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessibilitySelfServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="adminNoteInput")
    def admin_note_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminNoteInput"))

    @builtins.property
    @jsii.member(jsii_name="appLinksJsonInput")
    def app_links_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appLinksJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="appSettingsJsonInput")
    def app_settings_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appSettingsJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationPolicyInput")
    def authentication_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="autoKeyRotationInput")
    def auto_key_rotation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoKeyRotationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoSubmitToolbarInput")
    def auto_submit_toolbar_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoSubmitToolbarInput"))

    @builtins.property
    @jsii.member(jsii_name="clientBasicSecretInput")
    def client_basic_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientBasicSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientUriInput")
    def client_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientUriInput"))

    @builtins.property
    @jsii.member(jsii_name="consentMethodInput")
    def consent_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consentMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="customClientIdInput")
    def custom_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enduserNoteInput")
    def enduser_note_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enduserNoteInput"))

    @builtins.property
    @jsii.member(jsii_name="grantTypesInput")
    def grant_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "grantTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsClaimInput")
    def groups_claim_input(self) -> typing.Optional["AppOauthGroupsClaim"]:
        return typing.cast(typing.Optional["AppOauthGroupsClaim"], jsii.get(self, "groupsClaimInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsInput")
    def groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsInput"))

    @builtins.property
    @jsii.member(jsii_name="hideIosInput")
    def hide_ios_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hideIosInput"))

    @builtins.property
    @jsii.member(jsii_name="hideWebInput")
    def hide_web_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hideWebInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="implicitAssignmentInput")
    def implicit_assignment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "implicitAssignmentInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerModeInput")
    def issuer_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerModeInput"))

    @builtins.property
    @jsii.member(jsii_name="jwksInput")
    def jwks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppOauthJwks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppOauthJwks"]]], jsii.get(self, "jwksInput"))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="loginModeInput")
    def login_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginModeInput"))

    @builtins.property
    @jsii.member(jsii_name="loginScopesInput")
    def login_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loginScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="loginUriInput")
    def login_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginUriInput"))

    @builtins.property
    @jsii.member(jsii_name="logoInput")
    def logo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoInput"))

    @builtins.property
    @jsii.member(jsii_name="logoUriInput")
    def logo_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoUriInput"))

    @builtins.property
    @jsii.member(jsii_name="omitSecretInput")
    def omit_secret_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "omitSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="pkceRequiredInput")
    def pkce_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pkceRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="policyUriInput")
    def policy_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyUriInput"))

    @builtins.property
    @jsii.member(jsii_name="postLogoutRedirectUrisInput")
    def post_logout_redirect_uris_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "postLogoutRedirectUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="profileInput")
    def profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUrisInput")
    def redirect_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "redirectUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenLeewayInput")
    def refresh_token_leeway_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "refreshTokenLeewayInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenRotationInput")
    def refresh_token_rotation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refreshTokenRotationInput"))

    @builtins.property
    @jsii.member(jsii_name="responseTypesInput")
    def response_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "responseTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="skipGroupsInput")
    def skip_groups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="skipUsersInput")
    def skip_users_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["AppOauthTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["AppOauthTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenEndpointAuthMethodInput")
    def token_endpoint_auth_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenEndpointAuthMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="tosUriInput")
    def tos_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tosUriInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateInput")
    def user_name_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameTemplatePushStatusInput")
    def user_name_template_push_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameTemplatePushStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateSuffixInput")
    def user_name_template_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameTemplateSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateTypeInput")
    def user_name_template_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameTemplateTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="usersInput")
    def users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppOauthUsers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppOauthUsers"]]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="wildcardRedirectInput")
    def wildcard_redirect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "wildcardRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="accessibilityErrorRedirectUrl")
    def accessibility_error_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityErrorRedirectUrl"))

    @accessibility_error_redirect_url.setter
    def accessibility_error_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ee7f724c8fbedcc75e8fd416c0c567ccfca097d9c5ead705678f88d7ae3520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilityErrorRedirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="accessibilityLoginRedirectUrl")
    def accessibility_login_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityLoginRedirectUrl"))

    @accessibility_login_redirect_url.setter
    def accessibility_login_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de9a97d04c62706c8e598f89b9237a87ebcca1e32c42c3ea966ee9d19f4853f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilityLoginRedirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="accessibilitySelfService")
    def accessibility_self_service(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessibilitySelfService"))

    @accessibility_self_service.setter
    def accessibility_self_service(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d75690049bcd5060ad3b73fcecf4162e94b3efc83276b77e07079a10685c2e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilitySelfService", value)

    @builtins.property
    @jsii.member(jsii_name="adminNote")
    def admin_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminNote"))

    @admin_note.setter
    def admin_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38d2682a7f67db439f4720cb468045bb26ff1a21c39a2c4aeb667eac9f946db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminNote", value)

    @builtins.property
    @jsii.member(jsii_name="appLinksJson")
    def app_links_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLinksJson"))

    @app_links_json.setter
    def app_links_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1de1f4558537d04350c1b875337e0030387068fbef09202768ab4e9b752cdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLinksJson", value)

    @builtins.property
    @jsii.member(jsii_name="appSettingsJson")
    def app_settings_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSettingsJson"))

    @app_settings_json.setter
    def app_settings_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9f7405ef1a24b510a6a9b21113cc8bdbe3a52e81bf88116ba8c0001025deab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSettingsJson", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationPolicy")
    def authentication_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationPolicy"))

    @authentication_policy.setter
    def authentication_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956eac9413073ed5f95bc3ced9b17c3aef6ddecaa3d9ab641637ed64515cac8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="autoKeyRotation")
    def auto_key_rotation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoKeyRotation"))

    @auto_key_rotation.setter
    def auto_key_rotation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c0d3c8b38d9686dc4f33b974a16ee799b123b090f49b84eb163700f6e51f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoKeyRotation", value)

    @builtins.property
    @jsii.member(jsii_name="autoSubmitToolbar")
    def auto_submit_toolbar(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoSubmitToolbar"))

    @auto_submit_toolbar.setter
    def auto_submit_toolbar(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6dbd8c5a5dd8ca17f2bd21c18f73d6e7ad6638825a1d875560cb558e4420471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubmitToolbar", value)

    @builtins.property
    @jsii.member(jsii_name="clientBasicSecret")
    def client_basic_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientBasicSecret"))

    @client_basic_secret.setter
    def client_basic_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd01c5d3acdac19b1b2f1854708d02798b0971ffe5b5568114e85d827e16711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientBasicSecret", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c3e988b95115f15da25e1296615249b5b75d1e86020824b570026859280aa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientUri")
    def client_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientUri"))

    @client_uri.setter
    def client_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf2754d98764095cbba4751dc13eb235ac60492ca19154cecc0da04483c07f61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientUri", value)

    @builtins.property
    @jsii.member(jsii_name="consentMethod")
    def consent_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consentMethod"))

    @consent_method.setter
    def consent_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e09ee23d732fc2796d7b1d9d9433cc36085626ded5d43c426a01f6641798ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consentMethod", value)

    @builtins.property
    @jsii.member(jsii_name="customClientId")
    def custom_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customClientId"))

    @custom_client_id.setter
    def custom_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c32f025919a6d57fc7c8d0932ea7c4b41aa1e9297a27aac918055489c669d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customClientId", value)

    @builtins.property
    @jsii.member(jsii_name="enduserNote")
    def enduser_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enduserNote"))

    @enduser_note.setter
    def enduser_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__537e34237d9b71dd20697dd050f0b646dd979c5a5ed7b8e1b77eccc469c10731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enduserNote", value)

    @builtins.property
    @jsii.member(jsii_name="grantTypes")
    def grant_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "grantTypes"))

    @grant_types.setter
    def grant_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64bf5ffd3f2e5cc786044eb487c19ed8be4863528a06eb21a45b340619d3165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grantTypes", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__651dcc3f21d19bf444ba9201f630b903040e46de3859a6cef2c91ff658546f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="hideIos")
    def hide_ios(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hideIos"))

    @hide_ios.setter
    def hide_ios(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7979647384e79065cc75411e94eeec9e789638da724dffccbf6e117c628b3c1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hideIos", value)

    @builtins.property
    @jsii.member(jsii_name="hideWeb")
    def hide_web(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hideWeb"))

    @hide_web.setter
    def hide_web(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038691f9776bb6e817d431fde6584629b8198379780c916bc3f43b26e18c660e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hideWeb", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225d84fe52cb872fd925ffe9333dc37ad7ff2dc735a3cf82c7bc4943a1107e51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="implicitAssignment")
    def implicit_assignment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "implicitAssignment"))

    @implicit_assignment.setter
    def implicit_assignment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23db0c4f688e97a49a70ef464058c0538a79aef203f5ebea0ef195d1135394de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "implicitAssignment", value)

    @builtins.property
    @jsii.member(jsii_name="issuerMode")
    def issuer_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerMode"))

    @issuer_mode.setter
    def issuer_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660374ca4610908f81b290898d0cda2bdddfeed8dd5a7dde052d5641d6531438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerMode", value)

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f5e8e9baa32a0cd7132345221919cbc3afd439ec46b3ae06114c06bc533ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="loginMode")
    def login_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginMode"))

    @login_mode.setter
    def login_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f703a4df73082ec7b8cc7f3cf2e471e270a0f2715337cbd048840cdd9e2bd96e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginMode", value)

    @builtins.property
    @jsii.member(jsii_name="loginScopes")
    def login_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginScopes"))

    @login_scopes.setter
    def login_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5def56edff0d41c23b5255c2eebd7c187db349fe0f2d195dc3f1497540dd3ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginScopes", value)

    @builtins.property
    @jsii.member(jsii_name="loginUri")
    def login_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginUri"))

    @login_uri.setter
    def login_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a73e5de358a58899c2e36c5ac115fb542ad48389d80f7bfdce5d1b710925dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginUri", value)

    @builtins.property
    @jsii.member(jsii_name="logo")
    def logo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logo"))

    @logo.setter
    def logo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899a01a787c2b83ba6400ec46bf336491c9082effc077109a9783f749c9d332e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logo", value)

    @builtins.property
    @jsii.member(jsii_name="logoUri")
    def logo_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoUri"))

    @logo_uri.setter
    def logo_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72278eba759969cf179d3eb0c18a7c549c1360a6362f8aaa652cb1641613825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoUri", value)

    @builtins.property
    @jsii.member(jsii_name="omitSecret")
    def omit_secret(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "omitSecret"))

    @omit_secret.setter
    def omit_secret(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cfb8f9244d31b421af085b1ea8aaf3ad9df2ae2dde6d0a084dd757e5b30b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "omitSecret", value)

    @builtins.property
    @jsii.member(jsii_name="pkceRequired")
    def pkce_required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pkceRequired"))

    @pkce_required.setter
    def pkce_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59115e7ea7d0bb605471362f9bec4d683b387bc0e4f4234e848f574af459ff26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pkceRequired", value)

    @builtins.property
    @jsii.member(jsii_name="policyUri")
    def policy_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyUri"))

    @policy_uri.setter
    def policy_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c216e60e65c9654e1f715b5a8cbe35e809ca1a16759df3efaf99100a0d9c660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyUri", value)

    @builtins.property
    @jsii.member(jsii_name="postLogoutRedirectUris")
    def post_logout_redirect_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "postLogoutRedirectUris"))

    @post_logout_redirect_uris.setter
    def post_logout_redirect_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34c2fe20da93b1bc3edeb8cc50058a0ed94f183b1e168e3ab1cccebcc15d269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postLogoutRedirectUris", value)

    @builtins.property
    @jsii.member(jsii_name="profile")
    def profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profile"))

    @profile.setter
    def profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3751ed033a84ceced0039b308c047aa203ba80bac340036a6a7eae7c61ac1b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profile", value)

    @builtins.property
    @jsii.member(jsii_name="redirectUris")
    def redirect_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "redirectUris"))

    @redirect_uris.setter
    def redirect_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e338cda1db38faf09167aced969daddc3a7fe060fc572111b34c9c2f2315a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUris", value)

    @builtins.property
    @jsii.member(jsii_name="refreshTokenLeeway")
    def refresh_token_leeway(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "refreshTokenLeeway"))

    @refresh_token_leeway.setter
    def refresh_token_leeway(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a2feb3af2597dcb4cfeac2697c6dfc641803fd128ef3ecb0f17828730acda1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshTokenLeeway", value)

    @builtins.property
    @jsii.member(jsii_name="refreshTokenRotation")
    def refresh_token_rotation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshTokenRotation"))

    @refresh_token_rotation.setter
    def refresh_token_rotation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ffd7effd843cd4741b32f0b50b4b20c325089c6cf152201507628132b69be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshTokenRotation", value)

    @builtins.property
    @jsii.member(jsii_name="responseTypes")
    def response_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "responseTypes"))

    @response_types.setter
    def response_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cad407e130b3a992a6d156a7ced7385682db7b5df5a3022feedeb2fb6a350c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseTypes", value)

    @builtins.property
    @jsii.member(jsii_name="skipGroups")
    def skip_groups(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipGroups"))

    @skip_groups.setter
    def skip_groups(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69e69eefc181df561722df32c3620e6486839c8b092d965c97f90f56f9bcbbe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipGroups", value)

    @builtins.property
    @jsii.member(jsii_name="skipUsers")
    def skip_users(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipUsers"))

    @skip_users.setter
    def skip_users(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0f259d79f4fe9cc617094bb8aa391ebb80f521ada65835eb91cba529cf5f7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipUsers", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd90583b001b43983c8bc09c6171edf458034484c0149d8e9e6e1e8f93f1eb61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="tokenEndpointAuthMethod")
    def token_endpoint_auth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpointAuthMethod"))

    @token_endpoint_auth_method.setter
    def token_endpoint_auth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1249c27cf137653192e1b87ef96a818444cd693498f35051a7264aead64a9b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpointAuthMethod", value)

    @builtins.property
    @jsii.member(jsii_name="tosUri")
    def tos_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tosUri"))

    @tos_uri.setter
    def tos_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ca9d72bc5241eb1d02130e99b1cff317ae6289d6608a8687c0c6916228aee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tosUri", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6061b13331273b0e05049eb2e6ae2f2a80f67e02ed4add42afc12a77450f373c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplate")
    def user_name_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplate"))

    @user_name_template.setter
    def user_name_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e590d71a642689f5f592e691e730eb4d8f74a7f02754ebe96a5d3db2d866eaa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplatePushStatus")
    def user_name_template_push_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplatePushStatus"))

    @user_name_template_push_status.setter
    def user_name_template_push_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eff9aeee4f979dc1a73f9aaad68252532a4f9dc200351324b29d83f58df783c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplatePushStatus", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateSuffix")
    def user_name_template_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplateSuffix"))

    @user_name_template_suffix.setter
    def user_name_template_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a513fe2fbc07a724091f7d23c19eda7d2443aa67feaf5e17989ec7b5453b20b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplateSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateType")
    def user_name_template_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplateType"))

    @user_name_template_type.setter
    def user_name_template_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4e34f0a7b74f4b344e245a75173a9c4595d2d0602257877c163ff813e20ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplateType", value)

    @builtins.property
    @jsii.member(jsii_name="wildcardRedirect")
    def wildcard_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wildcardRedirect"))

    @wildcard_redirect.setter
    def wildcard_redirect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b008807e00e94c64891f82433eaaff622bbfc95a931c9aa139d32e37178055c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wildcardRedirect", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appOauth.AppOauthConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "label": "label",
        "type": "type",
        "accessibility_error_redirect_url": "accessibilityErrorRedirectUrl",
        "accessibility_login_redirect_url": "accessibilityLoginRedirectUrl",
        "accessibility_self_service": "accessibilitySelfService",
        "admin_note": "adminNote",
        "app_links_json": "appLinksJson",
        "app_settings_json": "appSettingsJson",
        "authentication_policy": "authenticationPolicy",
        "auto_key_rotation": "autoKeyRotation",
        "auto_submit_toolbar": "autoSubmitToolbar",
        "client_basic_secret": "clientBasicSecret",
        "client_id": "clientId",
        "client_uri": "clientUri",
        "consent_method": "consentMethod",
        "custom_client_id": "customClientId",
        "enduser_note": "enduserNote",
        "grant_types": "grantTypes",
        "groups": "groups",
        "groups_claim": "groupsClaim",
        "hide_ios": "hideIos",
        "hide_web": "hideWeb",
        "id": "id",
        "implicit_assignment": "implicitAssignment",
        "issuer_mode": "issuerMode",
        "jwks": "jwks",
        "login_mode": "loginMode",
        "login_scopes": "loginScopes",
        "login_uri": "loginUri",
        "logo": "logo",
        "logo_uri": "logoUri",
        "omit_secret": "omitSecret",
        "pkce_required": "pkceRequired",
        "policy_uri": "policyUri",
        "post_logout_redirect_uris": "postLogoutRedirectUris",
        "profile": "profile",
        "redirect_uris": "redirectUris",
        "refresh_token_leeway": "refreshTokenLeeway",
        "refresh_token_rotation": "refreshTokenRotation",
        "response_types": "responseTypes",
        "skip_groups": "skipGroups",
        "skip_users": "skipUsers",
        "status": "status",
        "timeouts": "timeouts",
        "token_endpoint_auth_method": "tokenEndpointAuthMethod",
        "tos_uri": "tosUri",
        "user_name_template": "userNameTemplate",
        "user_name_template_push_status": "userNameTemplatePushStatus",
        "user_name_template_suffix": "userNameTemplateSuffix",
        "user_name_template_type": "userNameTemplateType",
        "users": "users",
        "wildcard_redirect": "wildcardRedirect",
    },
)
class AppOauthConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        label: builtins.str,
        type: builtins.str,
        accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        app_settings_json: typing.Optional[builtins.str] = None,
        authentication_policy: typing.Optional[builtins.str] = None,
        auto_key_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_basic_secret: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_uri: typing.Optional[builtins.str] = None,
        consent_method: typing.Optional[builtins.str] = None,
        custom_client_id: typing.Optional[builtins.str] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        grant_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_claim: typing.Optional[typing.Union["AppOauthGroupsClaim", typing.Dict[builtins.str, typing.Any]]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        jwks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppOauthJwks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        login_mode: typing.Optional[builtins.str] = None,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_uri: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        logo_uri: typing.Optional[builtins.str] = None,
        omit_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pkce_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_uri: typing.Optional[builtins.str] = None,
        post_logout_redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        profile: typing.Optional[builtins.str] = None,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        refresh_token_leeway: typing.Optional[jsii.Number] = None,
        refresh_token_rotation: typing.Optional[builtins.str] = None,
        response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AppOauthTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        token_endpoint_auth_method: typing.Optional[builtins.str] = None,
        tos_uri: typing.Optional[builtins.str] = None,
        user_name_template: typing.Optional[builtins.str] = None,
        user_name_template_push_status: typing.Optional[builtins.str] = None,
        user_name_template_suffix: typing.Optional[builtins.str] = None,
        user_name_template_type: typing.Optional[builtins.str] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppOauthUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        wildcard_redirect: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#label AppOauth#label}
        :param type: The type of client application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#type AppOauth#type}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#accessibility_error_redirect_url AppOauth#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#accessibility_login_redirect_url AppOauth#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#accessibility_self_service AppOauth#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#admin_note AppOauth#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#app_links_json AppOauth#app_links_json}
        :param app_settings_json: Application settings in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#app_settings_json AppOauth#app_settings_json}
        :param authentication_policy: Id of this apps authentication policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#authentication_policy AppOauth#authentication_policy}
        :param auto_key_rotation: Requested key rotation mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#auto_key_rotation AppOauth#auto_key_rotation}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#auto_submit_toolbar AppOauth#auto_submit_toolbar}
        :param client_basic_secret: OAuth client secret key, this can be set when token_endpoint_auth_method is client_secret_basic. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#client_basic_secret AppOauth#client_basic_secret}
        :param client_id: OAuth client ID. If set during creation, app is created with this id. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#client_id AppOauth#client_id}
        :param client_uri: URI to a web page providing information about the client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#client_uri AppOauth#client_uri}
        :param consent_method: *Early Access Property*. Indicates whether user consent is required or implicit. Valid values: REQUIRED, TRUSTED. Default value is TRUSTED. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#consent_method AppOauth#consent_method}
        :param custom_client_id: **Deprecated** This property allows you to set your client_id during creation. NOTE: updating after creation will be a no-op, use client_id for that behavior instead. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#custom_client_id AppOauth#custom_client_id}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#enduser_note AppOauth#enduser_note}
        :param grant_types: List of OAuth 2.0 grant types. Conditional validation params found here https://developer.okta.com/docs/api/resources/apps#credentials-settings-details. Defaults to minimum requirements per app type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#grant_types AppOauth#grant_types}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#groups AppOauth#groups}
        :param groups_claim: groups_claim block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#groups_claim AppOauth#groups_claim}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#hide_ios AppOauth#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#hide_web AppOauth#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#id AppOauth#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param implicit_assignment: *Early Access Property*. Enable Federation Broker Mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#implicit_assignment AppOauth#implicit_assignment}
        :param issuer_mode: *Early Access Property*. Indicates whether the Okta Authorization Server uses the original Okta org domain URL or a custom domain URL as the issuer of ID token for this client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#issuer_mode AppOauth#issuer_mode}
        :param jwks: jwks block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#jwks AppOauth#jwks}
        :param login_mode: The type of Idp-Initiated login that the client supports, if any. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#login_mode AppOauth#login_mode}
        :param login_scopes: List of scopes to use for the request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#login_scopes AppOauth#login_scopes}
        :param login_uri: URI that initiates login. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#login_uri AppOauth#login_uri}
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#logo AppOauth#logo}
        :param logo_uri: URI that references a logo for the client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#logo_uri AppOauth#logo_uri}
        :param omit_secret: This tells the provider not to persist the application's secret to state. If this is ever changes from true => false your app will be recreated. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#omit_secret AppOauth#omit_secret}
        :param pkce_required: Require Proof Key for Code Exchange (PKCE) for additional verification key rotation mode. See: https://developer.okta.com/docs/reference/api/apps/#oauth-credential-object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#pkce_required AppOauth#pkce_required}
        :param policy_uri: URI to web page providing client policy document. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#policy_uri AppOauth#policy_uri}
        :param post_logout_redirect_uris: List of URIs for redirection after logout. Note: see okta_app_oauth_post_logout_redirect_uri for appending to this list in a decentralized way. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#post_logout_redirect_uris AppOauth#post_logout_redirect_uris}
        :param profile: Custom JSON that represents an OAuth application's profile. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#profile AppOauth#profile}
        :param redirect_uris: List of URIs for use in the redirect-based flow. This is required for all application types except service. Note: see okta_app_oauth_redirect_uri for appending to this list in a decentralized way. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#redirect_uris AppOauth#redirect_uris}
        :param refresh_token_leeway: *Early Access Property* Grace period for token rotation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#refresh_token_leeway AppOauth#refresh_token_leeway}
        :param refresh_token_rotation: *Early Access Property* Refresh token rotation behavior. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#refresh_token_rotation AppOauth#refresh_token_rotation}
        :param response_types: List of OAuth 2.0 response type strings. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#response_types AppOauth#response_types}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#skip_groups AppOauth#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#skip_users AppOauth#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#status AppOauth#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#timeouts AppOauth#timeouts}
        :param token_endpoint_auth_method: Requested authentication method for the token endpoint. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#token_endpoint_auth_method AppOauth#token_endpoint_auth_method}
        :param tos_uri: URI to web page providing client tos (terms of service). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#tos_uri AppOauth#tos_uri}
        :param user_name_template: Username template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template AppOauth#user_name_template}
        :param user_name_template_push_status: Push username on update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template_push_status AppOauth#user_name_template_push_status}
        :param user_name_template_suffix: Username template suffix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template_suffix AppOauth#user_name_template_suffix}
        :param user_name_template_type: Username template type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template_type AppOauth#user_name_template_type}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#users AppOauth#users}
        :param wildcard_redirect: *Early Access Property*. Indicates if the client is allowed to use wildcard matching of redirect_uris. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#wildcard_redirect AppOauth#wildcard_redirect}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(groups_claim, dict):
            groups_claim = AppOauthGroupsClaim(**groups_claim)
        if isinstance(timeouts, dict):
            timeouts = AppOauthTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd98de39d7cec2b18e355b4b41ed7acacea24dba9f6dd92ad62038c0e4ab48ea)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument accessibility_error_redirect_url", value=accessibility_error_redirect_url, expected_type=type_hints["accessibility_error_redirect_url"])
            check_type(argname="argument accessibility_login_redirect_url", value=accessibility_login_redirect_url, expected_type=type_hints["accessibility_login_redirect_url"])
            check_type(argname="argument accessibility_self_service", value=accessibility_self_service, expected_type=type_hints["accessibility_self_service"])
            check_type(argname="argument admin_note", value=admin_note, expected_type=type_hints["admin_note"])
            check_type(argname="argument app_links_json", value=app_links_json, expected_type=type_hints["app_links_json"])
            check_type(argname="argument app_settings_json", value=app_settings_json, expected_type=type_hints["app_settings_json"])
            check_type(argname="argument authentication_policy", value=authentication_policy, expected_type=type_hints["authentication_policy"])
            check_type(argname="argument auto_key_rotation", value=auto_key_rotation, expected_type=type_hints["auto_key_rotation"])
            check_type(argname="argument auto_submit_toolbar", value=auto_submit_toolbar, expected_type=type_hints["auto_submit_toolbar"])
            check_type(argname="argument client_basic_secret", value=client_basic_secret, expected_type=type_hints["client_basic_secret"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_uri", value=client_uri, expected_type=type_hints["client_uri"])
            check_type(argname="argument consent_method", value=consent_method, expected_type=type_hints["consent_method"])
            check_type(argname="argument custom_client_id", value=custom_client_id, expected_type=type_hints["custom_client_id"])
            check_type(argname="argument enduser_note", value=enduser_note, expected_type=type_hints["enduser_note"])
            check_type(argname="argument grant_types", value=grant_types, expected_type=type_hints["grant_types"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument groups_claim", value=groups_claim, expected_type=type_hints["groups_claim"])
            check_type(argname="argument hide_ios", value=hide_ios, expected_type=type_hints["hide_ios"])
            check_type(argname="argument hide_web", value=hide_web, expected_type=type_hints["hide_web"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument implicit_assignment", value=implicit_assignment, expected_type=type_hints["implicit_assignment"])
            check_type(argname="argument issuer_mode", value=issuer_mode, expected_type=type_hints["issuer_mode"])
            check_type(argname="argument jwks", value=jwks, expected_type=type_hints["jwks"])
            check_type(argname="argument login_mode", value=login_mode, expected_type=type_hints["login_mode"])
            check_type(argname="argument login_scopes", value=login_scopes, expected_type=type_hints["login_scopes"])
            check_type(argname="argument login_uri", value=login_uri, expected_type=type_hints["login_uri"])
            check_type(argname="argument logo", value=logo, expected_type=type_hints["logo"])
            check_type(argname="argument logo_uri", value=logo_uri, expected_type=type_hints["logo_uri"])
            check_type(argname="argument omit_secret", value=omit_secret, expected_type=type_hints["omit_secret"])
            check_type(argname="argument pkce_required", value=pkce_required, expected_type=type_hints["pkce_required"])
            check_type(argname="argument policy_uri", value=policy_uri, expected_type=type_hints["policy_uri"])
            check_type(argname="argument post_logout_redirect_uris", value=post_logout_redirect_uris, expected_type=type_hints["post_logout_redirect_uris"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument redirect_uris", value=redirect_uris, expected_type=type_hints["redirect_uris"])
            check_type(argname="argument refresh_token_leeway", value=refresh_token_leeway, expected_type=type_hints["refresh_token_leeway"])
            check_type(argname="argument refresh_token_rotation", value=refresh_token_rotation, expected_type=type_hints["refresh_token_rotation"])
            check_type(argname="argument response_types", value=response_types, expected_type=type_hints["response_types"])
            check_type(argname="argument skip_groups", value=skip_groups, expected_type=type_hints["skip_groups"])
            check_type(argname="argument skip_users", value=skip_users, expected_type=type_hints["skip_users"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument token_endpoint_auth_method", value=token_endpoint_auth_method, expected_type=type_hints["token_endpoint_auth_method"])
            check_type(argname="argument tos_uri", value=tos_uri, expected_type=type_hints["tos_uri"])
            check_type(argname="argument user_name_template", value=user_name_template, expected_type=type_hints["user_name_template"])
            check_type(argname="argument user_name_template_push_status", value=user_name_template_push_status, expected_type=type_hints["user_name_template_push_status"])
            check_type(argname="argument user_name_template_suffix", value=user_name_template_suffix, expected_type=type_hints["user_name_template_suffix"])
            check_type(argname="argument user_name_template_type", value=user_name_template_type, expected_type=type_hints["user_name_template_type"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
            check_type(argname="argument wildcard_redirect", value=wildcard_redirect, expected_type=type_hints["wildcard_redirect"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label": label,
            "type": type,
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
        if accessibility_error_redirect_url is not None:
            self._values["accessibility_error_redirect_url"] = accessibility_error_redirect_url
        if accessibility_login_redirect_url is not None:
            self._values["accessibility_login_redirect_url"] = accessibility_login_redirect_url
        if accessibility_self_service is not None:
            self._values["accessibility_self_service"] = accessibility_self_service
        if admin_note is not None:
            self._values["admin_note"] = admin_note
        if app_links_json is not None:
            self._values["app_links_json"] = app_links_json
        if app_settings_json is not None:
            self._values["app_settings_json"] = app_settings_json
        if authentication_policy is not None:
            self._values["authentication_policy"] = authentication_policy
        if auto_key_rotation is not None:
            self._values["auto_key_rotation"] = auto_key_rotation
        if auto_submit_toolbar is not None:
            self._values["auto_submit_toolbar"] = auto_submit_toolbar
        if client_basic_secret is not None:
            self._values["client_basic_secret"] = client_basic_secret
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_uri is not None:
            self._values["client_uri"] = client_uri
        if consent_method is not None:
            self._values["consent_method"] = consent_method
        if custom_client_id is not None:
            self._values["custom_client_id"] = custom_client_id
        if enduser_note is not None:
            self._values["enduser_note"] = enduser_note
        if grant_types is not None:
            self._values["grant_types"] = grant_types
        if groups is not None:
            self._values["groups"] = groups
        if groups_claim is not None:
            self._values["groups_claim"] = groups_claim
        if hide_ios is not None:
            self._values["hide_ios"] = hide_ios
        if hide_web is not None:
            self._values["hide_web"] = hide_web
        if id is not None:
            self._values["id"] = id
        if implicit_assignment is not None:
            self._values["implicit_assignment"] = implicit_assignment
        if issuer_mode is not None:
            self._values["issuer_mode"] = issuer_mode
        if jwks is not None:
            self._values["jwks"] = jwks
        if login_mode is not None:
            self._values["login_mode"] = login_mode
        if login_scopes is not None:
            self._values["login_scopes"] = login_scopes
        if login_uri is not None:
            self._values["login_uri"] = login_uri
        if logo is not None:
            self._values["logo"] = logo
        if logo_uri is not None:
            self._values["logo_uri"] = logo_uri
        if omit_secret is not None:
            self._values["omit_secret"] = omit_secret
        if pkce_required is not None:
            self._values["pkce_required"] = pkce_required
        if policy_uri is not None:
            self._values["policy_uri"] = policy_uri
        if post_logout_redirect_uris is not None:
            self._values["post_logout_redirect_uris"] = post_logout_redirect_uris
        if profile is not None:
            self._values["profile"] = profile
        if redirect_uris is not None:
            self._values["redirect_uris"] = redirect_uris
        if refresh_token_leeway is not None:
            self._values["refresh_token_leeway"] = refresh_token_leeway
        if refresh_token_rotation is not None:
            self._values["refresh_token_rotation"] = refresh_token_rotation
        if response_types is not None:
            self._values["response_types"] = response_types
        if skip_groups is not None:
            self._values["skip_groups"] = skip_groups
        if skip_users is not None:
            self._values["skip_users"] = skip_users
        if status is not None:
            self._values["status"] = status
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if token_endpoint_auth_method is not None:
            self._values["token_endpoint_auth_method"] = token_endpoint_auth_method
        if tos_uri is not None:
            self._values["tos_uri"] = tos_uri
        if user_name_template is not None:
            self._values["user_name_template"] = user_name_template
        if user_name_template_push_status is not None:
            self._values["user_name_template_push_status"] = user_name_template_push_status
        if user_name_template_suffix is not None:
            self._values["user_name_template_suffix"] = user_name_template_suffix
        if user_name_template_type is not None:
            self._values["user_name_template_type"] = user_name_template_type
        if users is not None:
            self._values["users"] = users
        if wildcard_redirect is not None:
            self._values["wildcard_redirect"] = wildcard_redirect

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
    def label(self) -> builtins.str:
        '''Pretty name of app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#label AppOauth#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of client application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#type AppOauth#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accessibility_error_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom error page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#accessibility_error_redirect_url AppOauth#accessibility_error_redirect_url}
        '''
        result = self._values.get("accessibility_error_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_login_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom login page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#accessibility_login_redirect_url AppOauth#accessibility_login_redirect_url}
        '''
        result = self._values.get("accessibility_login_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_self_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable self service.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#accessibility_self_service AppOauth#accessibility_self_service}
        '''
        result = self._values.get("accessibility_self_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def admin_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for admins.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#admin_note AppOauth#admin_note}
        '''
        result = self._values.get("admin_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_links_json(self) -> typing.Optional[builtins.str]:
        '''Displays specific appLinks for the app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#app_links_json AppOauth#app_links_json}
        '''
        result = self._values.get("app_links_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_settings_json(self) -> typing.Optional[builtins.str]:
        '''Application settings in JSON format.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#app_settings_json AppOauth#app_settings_json}
        '''
        result = self._values.get("app_settings_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_policy(self) -> typing.Optional[builtins.str]:
        '''Id of this apps authentication policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#authentication_policy AppOauth#authentication_policy}
        '''
        result = self._values.get("authentication_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_key_rotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Requested key rotation mode.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#auto_key_rotation AppOauth#auto_key_rotation}
        '''
        result = self._values.get("auto_key_rotation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_submit_toolbar(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Display auto submit toolbar.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#auto_submit_toolbar AppOauth#auto_submit_toolbar}
        '''
        result = self._values.get("auto_submit_toolbar")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_basic_secret(self) -> typing.Optional[builtins.str]:
        '''OAuth client secret key, this can be set when token_endpoint_auth_method is client_secret_basic.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#client_basic_secret AppOauth#client_basic_secret}
        '''
        result = self._values.get("client_basic_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''OAuth client ID. If set during creation, app is created with this id.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#client_id AppOauth#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_uri(self) -> typing.Optional[builtins.str]:
        '''URI to a web page providing information about the client.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#client_uri AppOauth#client_uri}
        '''
        result = self._values.get("client_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consent_method(self) -> typing.Optional[builtins.str]:
        '''*Early Access Property*. Indicates whether user consent is required or implicit. Valid values: REQUIRED, TRUSTED. Default value is TRUSTED.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#consent_method AppOauth#consent_method}
        '''
        result = self._values.get("consent_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_client_id(self) -> typing.Optional[builtins.str]:
        '''**Deprecated** This property allows you to set your client_id during creation.

        NOTE: updating after creation will be a no-op, use client_id for that behavior instead.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#custom_client_id AppOauth#custom_client_id}
        '''
        result = self._values.get("custom_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enduser_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for end users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#enduser_note AppOauth#enduser_note}
        '''
        result = self._values.get("enduser_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grant_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of OAuth 2.0 grant types. Conditional validation params found here https://developer.okta.com/docs/api/resources/apps#credentials-settings-details. Defaults to minimum requirements per app type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#grant_types AppOauth#grant_types}
        '''
        result = self._values.get("grant_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Groups associated with the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#groups AppOauth#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def groups_claim(self) -> typing.Optional["AppOauthGroupsClaim"]:
        '''groups_claim block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#groups_claim AppOauth#groups_claim}
        '''
        result = self._values.get("groups_claim")
        return typing.cast(typing.Optional["AppOauthGroupsClaim"], result)

    @builtins.property
    def hide_ios(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon on mobile app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#hide_ios AppOauth#hide_ios}
        '''
        result = self._values.get("hide_ios")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hide_web(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon to users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#hide_web AppOauth#hide_web}
        '''
        result = self._values.get("hide_web")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#id AppOauth#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def implicit_assignment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''*Early Access Property*. Enable Federation Broker Mode.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#implicit_assignment AppOauth#implicit_assignment}
        '''
        result = self._values.get("implicit_assignment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def issuer_mode(self) -> typing.Optional[builtins.str]:
        '''*Early Access Property*.

        Indicates whether the Okta Authorization Server uses the original Okta org domain URL or a custom domain URL as the issuer of ID token for this client.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#issuer_mode AppOauth#issuer_mode}
        '''
        result = self._values.get("issuer_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jwks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppOauthJwks"]]]:
        '''jwks block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#jwks AppOauth#jwks}
        '''
        result = self._values.get("jwks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppOauthJwks"]]], result)

    @builtins.property
    def login_mode(self) -> typing.Optional[builtins.str]:
        '''The type of Idp-Initiated login that the client supports, if any.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#login_mode AppOauth#login_mode}
        '''
        result = self._values.get("login_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of scopes to use for the request.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#login_scopes AppOauth#login_scopes}
        '''
        result = self._values.get("login_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_uri(self) -> typing.Optional[builtins.str]:
        '''URI that initiates login.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#login_uri AppOauth#login_uri}
        '''
        result = self._values.get("login_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo(self) -> typing.Optional[builtins.str]:
        '''Local path to logo of the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#logo AppOauth#logo}
        '''
        result = self._values.get("logo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo_uri(self) -> typing.Optional[builtins.str]:
        '''URI that references a logo for the client.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#logo_uri AppOauth#logo_uri}
        '''
        result = self._values.get("logo_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def omit_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This tells the provider not to persist the application's secret to state.

        If this is ever changes from true => false your app will be recreated.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#omit_secret AppOauth#omit_secret}
        '''
        result = self._values.get("omit_secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pkce_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require Proof Key for Code Exchange (PKCE) for additional verification key rotation mode. See: https://developer.okta.com/docs/reference/api/apps/#oauth-credential-object.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#pkce_required AppOauth#pkce_required}
        '''
        result = self._values.get("pkce_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policy_uri(self) -> typing.Optional[builtins.str]:
        '''URI to web page providing client policy document.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#policy_uri AppOauth#policy_uri}
        '''
        result = self._values.get("policy_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_logout_redirect_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of URIs for redirection after logout. Note: see okta_app_oauth_post_logout_redirect_uri for appending to this list in a decentralized way.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#post_logout_redirect_uris AppOauth#post_logout_redirect_uris}
        '''
        result = self._values.get("post_logout_redirect_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''Custom JSON that represents an OAuth application's profile.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#profile AppOauth#profile}
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of URIs for use in the redirect-based flow.

        This is required for all application types except service. Note: see okta_app_oauth_redirect_uri for appending to this list in a decentralized way.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#redirect_uris AppOauth#redirect_uris}
        '''
        result = self._values.get("redirect_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def refresh_token_leeway(self) -> typing.Optional[jsii.Number]:
        '''*Early Access Property* Grace period for token rotation.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#refresh_token_leeway AppOauth#refresh_token_leeway}
        '''
        result = self._values.get("refresh_token_leeway")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def refresh_token_rotation(self) -> typing.Optional[builtins.str]:
        '''*Early Access Property* Refresh token rotation behavior.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#refresh_token_rotation AppOauth#refresh_token_rotation}
        '''
        result = self._values.get("refresh_token_rotation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of OAuth 2.0 response type strings.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#response_types AppOauth#response_types}
        '''
        result = self._values.get("response_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#skip_groups AppOauth#skip_groups}
        '''
        result = self._values.get("skip_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_users(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#skip_users AppOauth#skip_users}
        '''
        result = self._values.get("skip_users")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#status AppOauth#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AppOauthTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#timeouts AppOauth#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AppOauthTimeouts"], result)

    @builtins.property
    def token_endpoint_auth_method(self) -> typing.Optional[builtins.str]:
        '''Requested authentication method for the token endpoint.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#token_endpoint_auth_method AppOauth#token_endpoint_auth_method}
        '''
        result = self._values.get("token_endpoint_auth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tos_uri(self) -> typing.Optional[builtins.str]:
        '''URI to web page providing client tos (terms of service).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#tos_uri AppOauth#tos_uri}
        '''
        result = self._values.get("tos_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template(self) -> typing.Optional[builtins.str]:
        '''Username template.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template AppOauth#user_name_template}
        '''
        result = self._values.get("user_name_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_push_status(self) -> typing.Optional[builtins.str]:
        '''Push username on update.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template_push_status AppOauth#user_name_template_push_status}
        '''
        result = self._values.get("user_name_template_push_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_suffix(self) -> typing.Optional[builtins.str]:
        '''Username template suffix.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template_suffix AppOauth#user_name_template_suffix}
        '''
        result = self._values.get("user_name_template_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_type(self) -> typing.Optional[builtins.str]:
        '''Username template type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#user_name_template_type AppOauth#user_name_template_type}
        '''
        result = self._values.get("user_name_template_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppOauthUsers"]]]:
        '''users block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#users AppOauth#users}
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppOauthUsers"]]], result)

    @builtins.property
    def wildcard_redirect(self) -> typing.Optional[builtins.str]:
        '''*Early Access Property*. Indicates if the client is allowed to use wildcard matching of redirect_uris.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#wildcard_redirect AppOauth#wildcard_redirect}
        '''
        result = self._values.get("wildcard_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppOauthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appOauth.AppOauthGroupsClaim",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "value": "value",
        "filter_type": "filterType",
    },
)
class AppOauthGroupsClaim:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        value: builtins.str,
        filter_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the claim that will be used in the token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#name AppOauth#name}
        :param type: Groups claim type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#type AppOauth#type}
        :param value: Value of the claim. Can be an Okta Expression Language statement that evaluates at the time the token is minted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#value AppOauth#value}
        :param filter_type: Groups claim filter. Can only be set if type is FILTER. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#filter_type AppOauth#filter_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb4869669d83d3c76a28bea2a2bc2077291d8bd5935cb9caef0ebc517e0e9053)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
            "value": value,
        }
        if filter_type is not None:
            self._values["filter_type"] = filter_type

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the claim that will be used in the token.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#name AppOauth#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Groups claim type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#type AppOauth#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the claim.

        Can be an Okta Expression Language statement that evaluates at the time the token is minted.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#value AppOauth#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_type(self) -> typing.Optional[builtins.str]:
        '''Groups claim filter. Can only be set if type is FILTER.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#filter_type AppOauth#filter_type}
        '''
        result = self._values.get("filter_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppOauthGroupsClaim(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppOauthGroupsClaimOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appOauth.AppOauthGroupsClaimOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef2c225c1011059821da172f3f1e89b262c20b997b4e4d264da1c9decc6aa7fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilterType")
    def reset_filter_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterType", []))

    @builtins.property
    @jsii.member(jsii_name="issuerMode")
    def issuer_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerMode"))

    @builtins.property
    @jsii.member(jsii_name="filterTypeInput")
    def filter_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="filterType")
    def filter_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterType"))

    @filter_type.setter
    def filter_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ec33cb6e159e078dfa943d5407fef63db30bf6698613954ac2f67ebfa26408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8956ab9219efaffa0b6a2d5fcfd0ce669c694a4889ae8cb824f1e89c9b55699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28c8c44a15421053f549d60ad839c939587e9ee0137b32969ee5a4747ead627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf7932dc60af6e0d95e1c62b1fa383d91527623327109f7b2ab6d1266a15d3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppOauthGroupsClaim]:
        return typing.cast(typing.Optional[AppOauthGroupsClaim], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppOauthGroupsClaim]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e0e58a53aa0455b79924dfb4ed0fc1eabf9d128fb7fc51816d87a7705fba60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appOauth.AppOauthJwks",
    jsii_struct_bases=[],
    name_mapping={"kid": "kid", "kty": "kty", "e": "e", "n": "n"},
)
class AppOauthJwks:
    def __init__(
        self,
        *,
        kid: builtins.str,
        kty: builtins.str,
        e: typing.Optional[builtins.str] = None,
        n: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kid: Key ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#kid AppOauth#kid}
        :param kty: Key type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#kty AppOauth#kty}
        :param e: RSA Exponent. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#e AppOauth#e}
        :param n: RSA Modulus. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#n AppOauth#n}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5742606248534cdfcfe4b5e83784c85dbc079eaeacdfd1f4827311350b266a0c)
            check_type(argname="argument kid", value=kid, expected_type=type_hints["kid"])
            check_type(argname="argument kty", value=kty, expected_type=type_hints["kty"])
            check_type(argname="argument e", value=e, expected_type=type_hints["e"])
            check_type(argname="argument n", value=n, expected_type=type_hints["n"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kid": kid,
            "kty": kty,
        }
        if e is not None:
            self._values["e"] = e
        if n is not None:
            self._values["n"] = n

    @builtins.property
    def kid(self) -> builtins.str:
        '''Key ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#kid AppOauth#kid}
        '''
        result = self._values.get("kid")
        assert result is not None, "Required property 'kid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kty(self) -> builtins.str:
        '''Key type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#kty AppOauth#kty}
        '''
        result = self._values.get("kty")
        assert result is not None, "Required property 'kty' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def e(self) -> typing.Optional[builtins.str]:
        '''RSA Exponent.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#e AppOauth#e}
        '''
        result = self._values.get("e")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def n(self) -> typing.Optional[builtins.str]:
        '''RSA Modulus.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#n AppOauth#n}
        '''
        result = self._values.get("n")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppOauthJwks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppOauthJwksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appOauth.AppOauthJwksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fedc6adc10b30e7e60237066c16659803bdf987bc9e35f311e308285d69e0f15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppOauthJwksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a038e155738e3dbe52cd9cdccdad0b80d61bef36afa5bf087552a04a64b763d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppOauthJwksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efdcc398f4064f371fdaadc6cf4ccc090c5274300407421f8a59f6b7276c763e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ab3f223ede381f7a41317725c4fe0003556e40f42ad20aa582919e6ecdbe8f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3706e407d5ac9b0d2917ddaffb50881f4ee8f34b4b14fb64814ef7e88e5c2db5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppOauthJwks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppOauthJwks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppOauthJwks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8ff52b2ff4ea2733df1bce38fdea0806b23c80f29a37316c115a5133b64807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppOauthJwksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appOauth.AppOauthJwksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8359c58875664b88ed08e8645ccc59f3c13cdfdbfeca7a013790c1ce2f43a5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetE")
    def reset_e(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetE", []))

    @jsii.member(jsii_name="resetN")
    def reset_n(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetN", []))

    @builtins.property
    @jsii.member(jsii_name="eInput")
    def e_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eInput"))

    @builtins.property
    @jsii.member(jsii_name="kidInput")
    def kid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kidInput"))

    @builtins.property
    @jsii.member(jsii_name="ktyInput")
    def kty_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ktyInput"))

    @builtins.property
    @jsii.member(jsii_name="nInput")
    def n_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nInput"))

    @builtins.property
    @jsii.member(jsii_name="e")
    def e(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "e"))

    @e.setter
    def e(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a497eb81b593456dfe05a79103ea84ea96078420cb10a2a589261cf2090062cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "e", value)

    @builtins.property
    @jsii.member(jsii_name="kid")
    def kid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kid"))

    @kid.setter
    def kid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c7aed3a948dbdbf87d26263e80ba1d5f1db83c835c385f085be4bde6f1533b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kid", value)

    @builtins.property
    @jsii.member(jsii_name="kty")
    def kty(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kty"))

    @kty.setter
    def kty(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57db7aafc13ebe72bd01f53aed137d0f614d6356e061d60e35c1cf6ad6c24de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kty", value)

    @builtins.property
    @jsii.member(jsii_name="n")
    def n(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "n"))

    @n.setter
    def n(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa47337ede59aaaaf925d4777c758bdf7c7b2c522d519017f855e4cd820aadb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "n", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppOauthJwks, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppOauthJwks, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppOauthJwks, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f70533dec1a7f45ab7360a84cd8bf6abd098a62d504d99068fcf582400797bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appOauth.AppOauthTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "read": "read", "update": "update"},
)
class AppOauthTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#create AppOauth#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#read AppOauth#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#update AppOauth#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f094e477c81be4db862d68715e9f5ebc779499bde559b8205df272d188206aa)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#create AppOauth#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#read AppOauth#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#update AppOauth#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppOauthTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppOauthTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appOauth.AppOauthTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83dfc93d9e8194952c38fc41830e2a096d74d99fa10595205558ee8482dbd5bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7be3a48c165c3a5f57b1ba0c710c69a068950c761948221c8ad10c0dadcd575e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93cd44a11c54ad1be07409e593cffaca9164d55a6da6cf241ab5a308537876fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af09d487494096bedd6b3fb92a16b19c05f14ddfff53fe8679ae2cfcd644b1dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppOauthTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppOauthTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppOauthTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437e81479362d49bac9334367fc92da005a0d349f02678c6a81157113f62ae4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appOauth.AppOauthUsers",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "password": "password", "username": "username"},
)
class AppOauthUsers:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: User ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#id AppOauth#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password: Password for user application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#password AppOauth#password}
        :param username: Username for user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#username AppOauth#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3a362a0d469de61218cb12573181afd2c24b27a648bfe07d541b706628a06a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''User ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#id AppOauth#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for user application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#password AppOauth#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_oauth#username AppOauth#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppOauthUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppOauthUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appOauth.AppOauthUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__443d03b9c43cf5e59834eb3b0eaa9b54897df45b5c7aa7522a9aee7dce934d0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppOauthUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbfd2c27b8a72b2869f3cf54452fcf4fd5f48123c5ffa9b4da782dd4dd752a6a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppOauthUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0641522f480a776e0c7de27e7d48087c6b788bb5fd9735ca1b529f127ee30af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf222e5bf16f4ae2ec45f5fe175a39d22cfc84eb8f4068616ee82bcb562f137d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__291f2d1fb926551db819f8204093543075ccf08d844ac24a0ec5a022c94c2eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppOauthUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppOauthUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppOauthUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8186bbfdfb9283c662dab9b5318f384d00a678bf5b6e90a8198a3761b7bcc171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppOauthUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appOauth.AppOauthUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fc10798aa527639dfec61063627416b68d43d37309677cc4ba1ebe5f529b606)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd0cc65731063abe90b0f5bde1a4b89be273e9bbb903a88810ab8c1f4ecb570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d269521e988acc25fa3c7cd3a7764be8d08f4339162ee0667bb514f6b17f80ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42ef02459c2879de3dacee629187b242fd4a6cbfd9892e89f654506689601ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppOauthUsers, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppOauthUsers, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppOauthUsers, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05fa507e6f647a23f8f42dbe547df513666990c6a832b8a38a9267ff3d77159e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AppOauth",
    "AppOauthConfig",
    "AppOauthGroupsClaim",
    "AppOauthGroupsClaimOutputReference",
    "AppOauthJwks",
    "AppOauthJwksList",
    "AppOauthJwksOutputReference",
    "AppOauthTimeouts",
    "AppOauthTimeoutsOutputReference",
    "AppOauthUsers",
    "AppOauthUsersList",
    "AppOauthUsersOutputReference",
]

publication.publish()

def _typecheckingstub__722860bbe40b36ca8dadfe7af7aeadfd64e57454389a7290203d05a0bea678d4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    label: builtins.str,
    type: builtins.str,
    accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    app_settings_json: typing.Optional[builtins.str] = None,
    authentication_policy: typing.Optional[builtins.str] = None,
    auto_key_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_basic_secret: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_uri: typing.Optional[builtins.str] = None,
    consent_method: typing.Optional[builtins.str] = None,
    custom_client_id: typing.Optional[builtins.str] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    grant_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_claim: typing.Optional[typing.Union[AppOauthGroupsClaim, typing.Dict[builtins.str, typing.Any]]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    jwks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppOauthJwks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    login_mode: typing.Optional[builtins.str] = None,
    login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_uri: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    logo_uri: typing.Optional[builtins.str] = None,
    omit_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pkce_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_uri: typing.Optional[builtins.str] = None,
    post_logout_redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    profile: typing.Optional[builtins.str] = None,
    redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    refresh_token_leeway: typing.Optional[jsii.Number] = None,
    refresh_token_rotation: typing.Optional[builtins.str] = None,
    response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AppOauthTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    token_endpoint_auth_method: typing.Optional[builtins.str] = None,
    tos_uri: typing.Optional[builtins.str] = None,
    user_name_template: typing.Optional[builtins.str] = None,
    user_name_template_push_status: typing.Optional[builtins.str] = None,
    user_name_template_suffix: typing.Optional[builtins.str] = None,
    user_name_template_type: typing.Optional[builtins.str] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppOauthUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    wildcard_redirect: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__3e81a848a5a70548b51f782b8896c63fbfa5f341f284e8157aca6342fa8599e4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppOauthJwks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7923c87358beeebc92e19628c1bfdf70ddb796f5fc666947734e6f0f3890889(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppOauthUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ee7f724c8fbedcc75e8fd416c0c567ccfca097d9c5ead705678f88d7ae3520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de9a97d04c62706c8e598f89b9237a87ebcca1e32c42c3ea966ee9d19f4853f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d75690049bcd5060ad3b73fcecf4162e94b3efc83276b77e07079a10685c2e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38d2682a7f67db439f4720cb468045bb26ff1a21c39a2c4aeb667eac9f946db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1de1f4558537d04350c1b875337e0030387068fbef09202768ab4e9b752cdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9f7405ef1a24b510a6a9b21113cc8bdbe3a52e81bf88116ba8c0001025deab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956eac9413073ed5f95bc3ced9b17c3aef6ddecaa3d9ab641637ed64515cac8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c0d3c8b38d9686dc4f33b974a16ee799b123b090f49b84eb163700f6e51f0e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6dbd8c5a5dd8ca17f2bd21c18f73d6e7ad6638825a1d875560cb558e4420471(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd01c5d3acdac19b1b2f1854708d02798b0971ffe5b5568114e85d827e16711(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c3e988b95115f15da25e1296615249b5b75d1e86020824b570026859280aa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2754d98764095cbba4751dc13eb235ac60492ca19154cecc0da04483c07f61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e09ee23d732fc2796d7b1d9d9433cc36085626ded5d43c426a01f6641798ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c32f025919a6d57fc7c8d0932ea7c4b41aa1e9297a27aac918055489c669d4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537e34237d9b71dd20697dd050f0b646dd979c5a5ed7b8e1b77eccc469c10731(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64bf5ffd3f2e5cc786044eb487c19ed8be4863528a06eb21a45b340619d3165(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651dcc3f21d19bf444ba9201f630b903040e46de3859a6cef2c91ff658546f4c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7979647384e79065cc75411e94eeec9e789638da724dffccbf6e117c628b3c1c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038691f9776bb6e817d431fde6584629b8198379780c916bc3f43b26e18c660e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225d84fe52cb872fd925ffe9333dc37ad7ff2dc735a3cf82c7bc4943a1107e51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23db0c4f688e97a49a70ef464058c0538a79aef203f5ebea0ef195d1135394de(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660374ca4610908f81b290898d0cda2bdddfeed8dd5a7dde052d5641d6531438(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f5e8e9baa32a0cd7132345221919cbc3afd439ec46b3ae06114c06bc533ff0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f703a4df73082ec7b8cc7f3cf2e471e270a0f2715337cbd048840cdd9e2bd96e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5def56edff0d41c23b5255c2eebd7c187db349fe0f2d195dc3f1497540dd3ea7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a73e5de358a58899c2e36c5ac115fb542ad48389d80f7bfdce5d1b710925dd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899a01a787c2b83ba6400ec46bf336491c9082effc077109a9783f749c9d332e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72278eba759969cf179d3eb0c18a7c549c1360a6362f8aaa652cb1641613825(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cfb8f9244d31b421af085b1ea8aaf3ad9df2ae2dde6d0a084dd757e5b30b85(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59115e7ea7d0bb605471362f9bec4d683b387bc0e4f4234e848f574af459ff26(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c216e60e65c9654e1f715b5a8cbe35e809ca1a16759df3efaf99100a0d9c660(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34c2fe20da93b1bc3edeb8cc50058a0ed94f183b1e168e3ab1cccebcc15d269(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3751ed033a84ceced0039b308c047aa203ba80bac340036a6a7eae7c61ac1b52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e338cda1db38faf09167aced969daddc3a7fe060fc572111b34c9c2f2315a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a2feb3af2597dcb4cfeac2697c6dfc641803fd128ef3ecb0f17828730acda1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ffd7effd843cd4741b32f0b50b4b20c325089c6cf152201507628132b69be5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cad407e130b3a992a6d156a7ced7385682db7b5df5a3022feedeb2fb6a350c9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e69eefc181df561722df32c3620e6486839c8b092d965c97f90f56f9bcbbe5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0f259d79f4fe9cc617094bb8aa391ebb80f521ada65835eb91cba529cf5f7e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd90583b001b43983c8bc09c6171edf458034484c0149d8e9e6e1e8f93f1eb61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1249c27cf137653192e1b87ef96a818444cd693498f35051a7264aead64a9b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ca9d72bc5241eb1d02130e99b1cff317ae6289d6608a8687c0c6916228aee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6061b13331273b0e05049eb2e6ae2f2a80f67e02ed4add42afc12a77450f373c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e590d71a642689f5f592e691e730eb4d8f74a7f02754ebe96a5d3db2d866eaa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eff9aeee4f979dc1a73f9aaad68252532a4f9dc200351324b29d83f58df783c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a513fe2fbc07a724091f7d23c19eda7d2443aa67feaf5e17989ec7b5453b20b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4e34f0a7b74f4b344e245a75173a9c4595d2d0602257877c163ff813e20ca9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b008807e00e94c64891f82433eaaff622bbfc95a931c9aa139d32e37178055c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd98de39d7cec2b18e355b4b41ed7acacea24dba9f6dd92ad62038c0e4ab48ea(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    label: builtins.str,
    type: builtins.str,
    accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    app_settings_json: typing.Optional[builtins.str] = None,
    authentication_policy: typing.Optional[builtins.str] = None,
    auto_key_rotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_basic_secret: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_uri: typing.Optional[builtins.str] = None,
    consent_method: typing.Optional[builtins.str] = None,
    custom_client_id: typing.Optional[builtins.str] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    grant_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_claim: typing.Optional[typing.Union[AppOauthGroupsClaim, typing.Dict[builtins.str, typing.Any]]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    jwks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppOauthJwks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    login_mode: typing.Optional[builtins.str] = None,
    login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_uri: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    logo_uri: typing.Optional[builtins.str] = None,
    omit_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pkce_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_uri: typing.Optional[builtins.str] = None,
    post_logout_redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    profile: typing.Optional[builtins.str] = None,
    redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    refresh_token_leeway: typing.Optional[jsii.Number] = None,
    refresh_token_rotation: typing.Optional[builtins.str] = None,
    response_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AppOauthTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    token_endpoint_auth_method: typing.Optional[builtins.str] = None,
    tos_uri: typing.Optional[builtins.str] = None,
    user_name_template: typing.Optional[builtins.str] = None,
    user_name_template_push_status: typing.Optional[builtins.str] = None,
    user_name_template_suffix: typing.Optional[builtins.str] = None,
    user_name_template_type: typing.Optional[builtins.str] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppOauthUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    wildcard_redirect: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb4869669d83d3c76a28bea2a2bc2077291d8bd5935cb9caef0ebc517e0e9053(
    *,
    name: builtins.str,
    type: builtins.str,
    value: builtins.str,
    filter_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2c225c1011059821da172f3f1e89b262c20b997b4e4d264da1c9decc6aa7fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ec33cb6e159e078dfa943d5407fef63db30bf6698613954ac2f67ebfa26408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8956ab9219efaffa0b6a2d5fcfd0ce669c694a4889ae8cb824f1e89c9b55699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28c8c44a15421053f549d60ad839c939587e9ee0137b32969ee5a4747ead627(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf7932dc60af6e0d95e1c62b1fa383d91527623327109f7b2ab6d1266a15d3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e0e58a53aa0455b79924dfb4ed0fc1eabf9d128fb7fc51816d87a7705fba60(
    value: typing.Optional[AppOauthGroupsClaim],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5742606248534cdfcfe4b5e83784c85dbc079eaeacdfd1f4827311350b266a0c(
    *,
    kid: builtins.str,
    kty: builtins.str,
    e: typing.Optional[builtins.str] = None,
    n: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedc6adc10b30e7e60237066c16659803bdf987bc9e35f311e308285d69e0f15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a038e155738e3dbe52cd9cdccdad0b80d61bef36afa5bf087552a04a64b763d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdcc398f4064f371fdaadc6cf4ccc090c5274300407421f8a59f6b7276c763e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab3f223ede381f7a41317725c4fe0003556e40f42ad20aa582919e6ecdbe8f0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3706e407d5ac9b0d2917ddaffb50881f4ee8f34b4b14fb64814ef7e88e5c2db5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8ff52b2ff4ea2733df1bce38fdea0806b23c80f29a37316c115a5133b64807(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppOauthJwks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8359c58875664b88ed08e8645ccc59f3c13cdfdbfeca7a013790c1ce2f43a5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a497eb81b593456dfe05a79103ea84ea96078420cb10a2a589261cf2090062cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c7aed3a948dbdbf87d26263e80ba1d5f1db83c835c385f085be4bde6f1533b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57db7aafc13ebe72bd01f53aed137d0f614d6356e061d60e35c1cf6ad6c24de6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa47337ede59aaaaf925d4777c758bdf7c7b2c522d519017f855e4cd820aadb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f70533dec1a7f45ab7360a84cd8bf6abd098a62d504d99068fcf582400797bb(
    value: typing.Optional[typing.Union[AppOauthJwks, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f094e477c81be4db862d68715e9f5ebc779499bde559b8205df272d188206aa(
    *,
    create: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83dfc93d9e8194952c38fc41830e2a096d74d99fa10595205558ee8482dbd5bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be3a48c165c3a5f57b1ba0c710c69a068950c761948221c8ad10c0dadcd575e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cd44a11c54ad1be07409e593cffaca9164d55a6da6cf241ab5a308537876fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af09d487494096bedd6b3fb92a16b19c05f14ddfff53fe8679ae2cfcd644b1dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437e81479362d49bac9334367fc92da005a0d349f02678c6a81157113f62ae4b(
    value: typing.Optional[typing.Union[AppOauthTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3a362a0d469de61218cb12573181afd2c24b27a648bfe07d541b706628a06a(
    *,
    id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443d03b9c43cf5e59834eb3b0eaa9b54897df45b5c7aa7522a9aee7dce934d0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfd2c27b8a72b2869f3cf54452fcf4fd5f48123c5ffa9b4da782dd4dd752a6a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0641522f480a776e0c7de27e7d48087c6b788bb5fd9735ca1b529f127ee30af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf222e5bf16f4ae2ec45f5fe175a39d22cfc84eb8f4068616ee82bcb562f137d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291f2d1fb926551db819f8204093543075ccf08d844ac24a0ec5a022c94c2eea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8186bbfdfb9283c662dab9b5318f384d00a678bf5b6e90a8198a3761b7bcc171(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppOauthUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc10798aa527639dfec61063627416b68d43d37309677cc4ba1ebe5f529b606(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd0cc65731063abe90b0f5bde1a4b89be273e9bbb903a88810ab8c1f4ecb570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d269521e988acc25fa3c7cd3a7764be8d08f4339162ee0667bb514f6b17f80ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42ef02459c2879de3dacee629187b242fd4a6cbfd9892e89f654506689601ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fa507e6f647a23f8f42dbe547df513666990c6a832b8a38a9267ff3d77159e(
    value: typing.Optional[typing.Union[AppOauthUsers, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
