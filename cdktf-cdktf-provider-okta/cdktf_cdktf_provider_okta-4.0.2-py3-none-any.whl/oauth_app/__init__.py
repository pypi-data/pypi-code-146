'''
# `okta_oauth_app`

Refer to the Terraform Registory for docs: [`okta_oauth_app`](https://www.terraform.io/docs/providers/okta/r/oauth_app).
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


class OauthApp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.oauthApp.OauthApp",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/oauth_app okta_oauth_app}.'''

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
        groups_claim: typing.Optional[typing.Union["OauthAppGroupsClaim", typing.Dict[builtins.str, typing.Any]]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        jwks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OauthAppJwks", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        timeouts: typing.Optional[typing.Union["OauthAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        token_endpoint_auth_method: typing.Optional[builtins.str] = None,
        tos_uri: typing.Optional[builtins.str] = None,
        user_name_template: typing.Optional[builtins.str] = None,
        user_name_template_push_status: typing.Optional[builtins.str] = None,
        user_name_template_suffix: typing.Optional[builtins.str] = None,
        user_name_template_type: typing.Optional[builtins.str] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OauthAppUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        wildcard_redirect: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/oauth_app okta_oauth_app} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#label OauthApp#label}
        :param type: The type of client application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#type OauthApp#type}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#accessibility_error_redirect_url OauthApp#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#accessibility_login_redirect_url OauthApp#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#accessibility_self_service OauthApp#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#admin_note OauthApp#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#app_links_json OauthApp#app_links_json}
        :param app_settings_json: Application settings in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#app_settings_json OauthApp#app_settings_json}
        :param authentication_policy: Id of this apps authentication policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#authentication_policy OauthApp#authentication_policy}
        :param auto_key_rotation: Requested key rotation mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#auto_key_rotation OauthApp#auto_key_rotation}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#auto_submit_toolbar OauthApp#auto_submit_toolbar}
        :param client_basic_secret: OAuth client secret key, this can be set when token_endpoint_auth_method is client_secret_basic. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#client_basic_secret OauthApp#client_basic_secret}
        :param client_id: OAuth client ID. If set during creation, app is created with this id. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#client_id OauthApp#client_id}
        :param client_uri: URI to a web page providing information about the client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#client_uri OauthApp#client_uri}
        :param consent_method: *Early Access Property*. Indicates whether user consent is required or implicit. Valid values: REQUIRED, TRUSTED. Default value is TRUSTED. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#consent_method OauthApp#consent_method}
        :param custom_client_id: **Deprecated** This property allows you to set your client_id during creation. NOTE: updating after creation will be a no-op, use client_id for that behavior instead. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#custom_client_id OauthApp#custom_client_id}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#enduser_note OauthApp#enduser_note}
        :param grant_types: List of OAuth 2.0 grant types. Conditional validation params found here https://developer.okta.com/docs/api/resources/apps#credentials-settings-details. Defaults to minimum requirements per app type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#grant_types OauthApp#grant_types}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#groups OauthApp#groups}
        :param groups_claim: groups_claim block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#groups_claim OauthApp#groups_claim}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#hide_ios OauthApp#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#hide_web OauthApp#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#id OauthApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param implicit_assignment: *Early Access Property*. Enable Federation Broker Mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#implicit_assignment OauthApp#implicit_assignment}
        :param issuer_mode: *Early Access Property*. Indicates whether the Okta Authorization Server uses the original Okta org domain URL or a custom domain URL as the issuer of ID token for this client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#issuer_mode OauthApp#issuer_mode}
        :param jwks: jwks block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#jwks OauthApp#jwks}
        :param login_mode: The type of Idp-Initiated login that the client supports, if any. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#login_mode OauthApp#login_mode}
        :param login_scopes: List of scopes to use for the request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#login_scopes OauthApp#login_scopes}
        :param login_uri: URI that initiates login. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#login_uri OauthApp#login_uri}
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#logo OauthApp#logo}
        :param logo_uri: URI that references a logo for the client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#logo_uri OauthApp#logo_uri}
        :param omit_secret: This tells the provider not to persist the application's secret to state. If this is ever changes from true => false your app will be recreated. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#omit_secret OauthApp#omit_secret}
        :param pkce_required: Require Proof Key for Code Exchange (PKCE) for additional verification key rotation mode. See: https://developer.okta.com/docs/reference/api/apps/#oauth-credential-object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#pkce_required OauthApp#pkce_required}
        :param policy_uri: URI to web page providing client policy document. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#policy_uri OauthApp#policy_uri}
        :param post_logout_redirect_uris: List of URIs for redirection after logout. Note: see okta_app_oauth_post_logout_redirect_uri for appending to this list in a decentralized way. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#post_logout_redirect_uris OauthApp#post_logout_redirect_uris}
        :param profile: Custom JSON that represents an OAuth application's profile. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#profile OauthApp#profile}
        :param redirect_uris: List of URIs for use in the redirect-based flow. This is required for all application types except service. Note: see okta_app_oauth_redirect_uri for appending to this list in a decentralized way. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#redirect_uris OauthApp#redirect_uris}
        :param refresh_token_leeway: *Early Access Property* Grace period for token rotation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#refresh_token_leeway OauthApp#refresh_token_leeway}
        :param refresh_token_rotation: *Early Access Property* Refresh token rotation behavior. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#refresh_token_rotation OauthApp#refresh_token_rotation}
        :param response_types: List of OAuth 2.0 response type strings. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#response_types OauthApp#response_types}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#skip_groups OauthApp#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#skip_users OauthApp#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#status OauthApp#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#timeouts OauthApp#timeouts}
        :param token_endpoint_auth_method: Requested authentication method for the token endpoint. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#token_endpoint_auth_method OauthApp#token_endpoint_auth_method}
        :param tos_uri: URI to web page providing client tos (terms of service). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#tos_uri OauthApp#tos_uri}
        :param user_name_template: Username template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template OauthApp#user_name_template}
        :param user_name_template_push_status: Push username on update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template_push_status OauthApp#user_name_template_push_status}
        :param user_name_template_suffix: Username template suffix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template_suffix OauthApp#user_name_template_suffix}
        :param user_name_template_type: Username template type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template_type OauthApp#user_name_template_type}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#users OauthApp#users}
        :param wildcard_redirect: *Early Access Property*. Indicates if the client is allowed to use wildcard matching of redirect_uris. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#wildcard_redirect OauthApp#wildcard_redirect}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bb82e6b09a30230fb162da78a640e793a72edeb0d106934c19a7eac7c9a04e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OauthAppConfig(
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
        :param name: Name of the claim that will be used in the token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#name OauthApp#name}
        :param type: Groups claim type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#type OauthApp#type}
        :param value: Value of the claim. Can be an Okta Expression Language statement that evaluates at the time the token is minted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#value OauthApp#value}
        :param filter_type: Groups claim filter. Can only be set if type is FILTER. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#filter_type OauthApp#filter_type}
        '''
        value_ = OauthAppGroupsClaim(
            name=name, type=type, value=value, filter_type=filter_type
        )

        return typing.cast(None, jsii.invoke(self, "putGroupsClaim", [value_]))

    @jsii.member(jsii_name="putJwks")
    def put_jwks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OauthAppJwks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816ef7a3375c863b529492086ebb4b5a776b5fc32c5fa592980a94bf587121e9)
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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#create OauthApp#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#read OauthApp#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#update OauthApp#update}.
        '''
        value = OauthAppTimeouts(create=create, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUsers")
    def put_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OauthAppUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c67735c572102874f7842a5cbadd5e69f550f3b3993064d7ec2cd316514a334)
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
    def groups_claim(self) -> "OauthAppGroupsClaimOutputReference":
        return typing.cast("OauthAppGroupsClaimOutputReference", jsii.get(self, "groupsClaim"))

    @builtins.property
    @jsii.member(jsii_name="jwks")
    def jwks(self) -> "OauthAppJwksList":
        return typing.cast("OauthAppJwksList", jsii.get(self, "jwks"))

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
    def timeouts(self) -> "OauthAppTimeoutsOutputReference":
        return typing.cast("OauthAppTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> "OauthAppUsersList":
        return typing.cast("OauthAppUsersList", jsii.get(self, "users"))

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
    def groups_claim_input(self) -> typing.Optional["OauthAppGroupsClaim"]:
        return typing.cast(typing.Optional["OauthAppGroupsClaim"], jsii.get(self, "groupsClaimInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OauthAppJwks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OauthAppJwks"]]], jsii.get(self, "jwksInput"))

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
    ) -> typing.Optional[typing.Union["OauthAppTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["OauthAppTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OauthAppUsers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OauthAppUsers"]]], jsii.get(self, "usersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0dc5ded48d1e5ee20af9180b4a3972216549d3bdac62a1d054745d0e561e34d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilityErrorRedirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="accessibilityLoginRedirectUrl")
    def accessibility_login_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityLoginRedirectUrl"))

    @accessibility_login_redirect_url.setter
    def accessibility_login_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec735b44dc2b2a5e199b5bdfdaf2271d9ec239136a9ab25825b1c7158f84b8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e5f5c32366fa334dc721bed599d1c5386e9d8edb2008454ccc47400b18f4773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilitySelfService", value)

    @builtins.property
    @jsii.member(jsii_name="adminNote")
    def admin_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminNote"))

    @admin_note.setter
    def admin_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e486729f9cf211b89d455dbe851c2def8a25ecf46e2e4163a09f6432e3b04a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminNote", value)

    @builtins.property
    @jsii.member(jsii_name="appLinksJson")
    def app_links_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLinksJson"))

    @app_links_json.setter
    def app_links_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e2b840d3567724b832a39d512dee16efceb42ba72b0fe0ae667927b80552d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLinksJson", value)

    @builtins.property
    @jsii.member(jsii_name="appSettingsJson")
    def app_settings_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSettingsJson"))

    @app_settings_json.setter
    def app_settings_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b821394d426aeff83d07c18a117b251c4aa8b8ee7790370780605a7cc35e7298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSettingsJson", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationPolicy")
    def authentication_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationPolicy"))

    @authentication_policy.setter
    def authentication_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea6ff213f0335545f9d93abe320420106a00a1cdb189c81d600ed48df803bae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7ae556162623518cee8d5f755d4b03e6d2ad29e4884eee0408f151ed9c93462)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89f88ac98ba44bd623153b1075e4f00b2dd9e3b10f3c6388086d8de79a6b1a55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubmitToolbar", value)

    @builtins.property
    @jsii.member(jsii_name="clientBasicSecret")
    def client_basic_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientBasicSecret"))

    @client_basic_secret.setter
    def client_basic_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65cb2bd5b13b9fa4787ec263aece752d18bf3534bc76897b3376641a38707e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientBasicSecret", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4545c06c4e79637adffe39ac32a8ecfa4fd8c135c6231ae091364a8c3b60cbda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientUri")
    def client_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientUri"))

    @client_uri.setter
    def client_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2ff2b25faac9f24074c93843841fa99fc604d7a3a71c57fa6c066f85aef6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientUri", value)

    @builtins.property
    @jsii.member(jsii_name="consentMethod")
    def consent_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consentMethod"))

    @consent_method.setter
    def consent_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca9ae584c7a8356625aed08daaab82124024a7eb3aeb264b9e0ac882dc2701a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consentMethod", value)

    @builtins.property
    @jsii.member(jsii_name="customClientId")
    def custom_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customClientId"))

    @custom_client_id.setter
    def custom_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270eafde0b4084c2611d6b90da036da9d8ff3c479b426195bf6078bca4d651d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customClientId", value)

    @builtins.property
    @jsii.member(jsii_name="enduserNote")
    def enduser_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enduserNote"))

    @enduser_note.setter
    def enduser_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ffc3b0455b082748f361439dc054e144d05d2b67992fcca56fd955ae4ace501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enduserNote", value)

    @builtins.property
    @jsii.member(jsii_name="grantTypes")
    def grant_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "grantTypes"))

    @grant_types.setter
    def grant_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b828e6c3119ccec1a2b988206d4218956928745add2bacf68d53285e4e3afc6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grantTypes", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7209afa29fbb73ba3279ddfccc03a99f0b7c94c4c95f2933c014094f89b6a40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b44c8e41d7f47b99b11f85a50950daa94c9f0c64615c8ac06abbbb627ab5fa25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51fe395d57de707704cdaef6dcac753313cbec0948523224a6ad55a6d60668cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hideWeb", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235c29aea34694dc0d5eb4912d09c4a29c9a5b65b9e455acc67ab627c20c1283)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6df8f0b9b43807d859dfd1a9b2d4a09dbb45d4e7bd97d3c60521b77efedaf46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "implicitAssignment", value)

    @builtins.property
    @jsii.member(jsii_name="issuerMode")
    def issuer_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerMode"))

    @issuer_mode.setter
    def issuer_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5d750757fc3e06c2516d1337f1c5a926422e6126a5d3f0e6e6b1f8ea8ad9d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerMode", value)

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d790dbd906985bae7bc98981ea57e4b0dc1aa60932c1af274bc11c006c4080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="loginMode")
    def login_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginMode"))

    @login_mode.setter
    def login_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b971292b9d6c10cb9e9c92ca7553c7cb613b12848e2dd5e58ac15e282265678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginMode", value)

    @builtins.property
    @jsii.member(jsii_name="loginScopes")
    def login_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginScopes"))

    @login_scopes.setter
    def login_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf886b2709e3d96f9af429b2a7c5a5ac274808ed99d200d3ba93b56bc8733d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginScopes", value)

    @builtins.property
    @jsii.member(jsii_name="loginUri")
    def login_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginUri"))

    @login_uri.setter
    def login_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0292380a635c51ab6eed3f243db1c8980671960276a0741ef766ab08a8fc71dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginUri", value)

    @builtins.property
    @jsii.member(jsii_name="logo")
    def logo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logo"))

    @logo.setter
    def logo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a869c2782335c33cc9168e24fd05aae6d38146a6bd9b65f460aa7fb6811fd0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logo", value)

    @builtins.property
    @jsii.member(jsii_name="logoUri")
    def logo_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoUri"))

    @logo_uri.setter
    def logo_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb4eda5a3b620f8591c43b47ba10f50cf1e2cd9ac0e6abd46a0893e48330ccf5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ccdd44186f33c6b247cf4511acc03f1c15767a1e4f14e36b946d2739dc0cfb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__070e2bb65aab8869db167ff2dfe4018524fbadce13a810d7518c473429617142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pkceRequired", value)

    @builtins.property
    @jsii.member(jsii_name="policyUri")
    def policy_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyUri"))

    @policy_uri.setter
    def policy_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c7e2946917319fd1cd2e1f7a0e0d8056f74fcfd91d1e1086a0ad48034c09fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyUri", value)

    @builtins.property
    @jsii.member(jsii_name="postLogoutRedirectUris")
    def post_logout_redirect_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "postLogoutRedirectUris"))

    @post_logout_redirect_uris.setter
    def post_logout_redirect_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d864e1df6ebb0cd2482e720b00068007bfe563d889d6eb5ac9bc0016f27a599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postLogoutRedirectUris", value)

    @builtins.property
    @jsii.member(jsii_name="profile")
    def profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profile"))

    @profile.setter
    def profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d153fd3ad31f7c76cf51cf421e4faaf23736da811a2f25e9f8cdff5b707e0da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profile", value)

    @builtins.property
    @jsii.member(jsii_name="redirectUris")
    def redirect_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "redirectUris"))

    @redirect_uris.setter
    def redirect_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02880391c445880c26a90b54a5170c4fa270d042b715925c8369b435ce8046a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUris", value)

    @builtins.property
    @jsii.member(jsii_name="refreshTokenLeeway")
    def refresh_token_leeway(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "refreshTokenLeeway"))

    @refresh_token_leeway.setter
    def refresh_token_leeway(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d6d5ed4b2823ef4f51b45c183750034c5aa79e3b33f1b696678e5290ac44ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshTokenLeeway", value)

    @builtins.property
    @jsii.member(jsii_name="refreshTokenRotation")
    def refresh_token_rotation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshTokenRotation"))

    @refresh_token_rotation.setter
    def refresh_token_rotation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9e18b18a5690fede742e53fe496c1a65a205ddb33a17181066a09aa28aa700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshTokenRotation", value)

    @builtins.property
    @jsii.member(jsii_name="responseTypes")
    def response_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "responseTypes"))

    @response_types.setter
    def response_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee45b93f90fa1ec19af3987be691c135d5573a97e23353af23fcb95550cce9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__101af90fcd76f7af992101c389480e47eb4d941751cdfd480bf5cae0dd8f2c46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a29e3834a035a8d01a51a4c22f28f97645f8fdfb1e12bbddc99f3df6f4ff8bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipUsers", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edcc77f3e1bf9bd40457a39edf1cfcf0181e95f2452b2308abb6953a85f24cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="tokenEndpointAuthMethod")
    def token_endpoint_auth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpointAuthMethod"))

    @token_endpoint_auth_method.setter
    def token_endpoint_auth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62b7943a02c7e8c81ceb4c2b0d53f8588f304e659d1d7d2f654fec88ce1dcf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpointAuthMethod", value)

    @builtins.property
    @jsii.member(jsii_name="tosUri")
    def tos_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tosUri"))

    @tos_uri.setter
    def tos_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5826ad27628a3914c424d9aa3565278e79eee96ab6ae28ff68deef1672f38d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tosUri", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848d8def1467669e6ba2b245cb9417816b7975284be9f22a4faee4bce47e20af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplate")
    def user_name_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplate"))

    @user_name_template.setter
    def user_name_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28927c5818d947f697524d7792dcc1a59deb283003551519cc67f41da094e7f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplatePushStatus")
    def user_name_template_push_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplatePushStatus"))

    @user_name_template_push_status.setter
    def user_name_template_push_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4356f7d0e886e2d5aeef97e9f7c1fcc021ce4c04e17723a1b694b556cbf48ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplatePushStatus", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateSuffix")
    def user_name_template_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplateSuffix"))

    @user_name_template_suffix.setter
    def user_name_template_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4369108607e240d35adaf258f9d3d6f3d11c50d8c59eb78892e943bb8d1349bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplateSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateType")
    def user_name_template_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplateType"))

    @user_name_template_type.setter
    def user_name_template_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996d0ba0c7a2a02757c49fbf336a8b146302b3070304a53f1cf0c9b5b230b140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplateType", value)

    @builtins.property
    @jsii.member(jsii_name="wildcardRedirect")
    def wildcard_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wildcardRedirect"))

    @wildcard_redirect.setter
    def wildcard_redirect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e203f2018b0cc812f3b099310228948452d727cf22217a88de0e44f5043c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wildcardRedirect", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.oauthApp.OauthAppConfig",
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
class OauthAppConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        groups_claim: typing.Optional[typing.Union["OauthAppGroupsClaim", typing.Dict[builtins.str, typing.Any]]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issuer_mode: typing.Optional[builtins.str] = None,
        jwks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OauthAppJwks", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        timeouts: typing.Optional[typing.Union["OauthAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        token_endpoint_auth_method: typing.Optional[builtins.str] = None,
        tos_uri: typing.Optional[builtins.str] = None,
        user_name_template: typing.Optional[builtins.str] = None,
        user_name_template_push_status: typing.Optional[builtins.str] = None,
        user_name_template_suffix: typing.Optional[builtins.str] = None,
        user_name_template_type: typing.Optional[builtins.str] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OauthAppUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#label OauthApp#label}
        :param type: The type of client application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#type OauthApp#type}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#accessibility_error_redirect_url OauthApp#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#accessibility_login_redirect_url OauthApp#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#accessibility_self_service OauthApp#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#admin_note OauthApp#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#app_links_json OauthApp#app_links_json}
        :param app_settings_json: Application settings in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#app_settings_json OauthApp#app_settings_json}
        :param authentication_policy: Id of this apps authentication policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#authentication_policy OauthApp#authentication_policy}
        :param auto_key_rotation: Requested key rotation mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#auto_key_rotation OauthApp#auto_key_rotation}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#auto_submit_toolbar OauthApp#auto_submit_toolbar}
        :param client_basic_secret: OAuth client secret key, this can be set when token_endpoint_auth_method is client_secret_basic. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#client_basic_secret OauthApp#client_basic_secret}
        :param client_id: OAuth client ID. If set during creation, app is created with this id. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#client_id OauthApp#client_id}
        :param client_uri: URI to a web page providing information about the client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#client_uri OauthApp#client_uri}
        :param consent_method: *Early Access Property*. Indicates whether user consent is required or implicit. Valid values: REQUIRED, TRUSTED. Default value is TRUSTED. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#consent_method OauthApp#consent_method}
        :param custom_client_id: **Deprecated** This property allows you to set your client_id during creation. NOTE: updating after creation will be a no-op, use client_id for that behavior instead. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#custom_client_id OauthApp#custom_client_id}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#enduser_note OauthApp#enduser_note}
        :param grant_types: List of OAuth 2.0 grant types. Conditional validation params found here https://developer.okta.com/docs/api/resources/apps#credentials-settings-details. Defaults to minimum requirements per app type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#grant_types OauthApp#grant_types}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#groups OauthApp#groups}
        :param groups_claim: groups_claim block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#groups_claim OauthApp#groups_claim}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#hide_ios OauthApp#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#hide_web OauthApp#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#id OauthApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param implicit_assignment: *Early Access Property*. Enable Federation Broker Mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#implicit_assignment OauthApp#implicit_assignment}
        :param issuer_mode: *Early Access Property*. Indicates whether the Okta Authorization Server uses the original Okta org domain URL or a custom domain URL as the issuer of ID token for this client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#issuer_mode OauthApp#issuer_mode}
        :param jwks: jwks block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#jwks OauthApp#jwks}
        :param login_mode: The type of Idp-Initiated login that the client supports, if any. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#login_mode OauthApp#login_mode}
        :param login_scopes: List of scopes to use for the request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#login_scopes OauthApp#login_scopes}
        :param login_uri: URI that initiates login. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#login_uri OauthApp#login_uri}
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#logo OauthApp#logo}
        :param logo_uri: URI that references a logo for the client. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#logo_uri OauthApp#logo_uri}
        :param omit_secret: This tells the provider not to persist the application's secret to state. If this is ever changes from true => false your app will be recreated. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#omit_secret OauthApp#omit_secret}
        :param pkce_required: Require Proof Key for Code Exchange (PKCE) for additional verification key rotation mode. See: https://developer.okta.com/docs/reference/api/apps/#oauth-credential-object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#pkce_required OauthApp#pkce_required}
        :param policy_uri: URI to web page providing client policy document. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#policy_uri OauthApp#policy_uri}
        :param post_logout_redirect_uris: List of URIs for redirection after logout. Note: see okta_app_oauth_post_logout_redirect_uri for appending to this list in a decentralized way. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#post_logout_redirect_uris OauthApp#post_logout_redirect_uris}
        :param profile: Custom JSON that represents an OAuth application's profile. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#profile OauthApp#profile}
        :param redirect_uris: List of URIs for use in the redirect-based flow. This is required for all application types except service. Note: see okta_app_oauth_redirect_uri for appending to this list in a decentralized way. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#redirect_uris OauthApp#redirect_uris}
        :param refresh_token_leeway: *Early Access Property* Grace period for token rotation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#refresh_token_leeway OauthApp#refresh_token_leeway}
        :param refresh_token_rotation: *Early Access Property* Refresh token rotation behavior. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#refresh_token_rotation OauthApp#refresh_token_rotation}
        :param response_types: List of OAuth 2.0 response type strings. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#response_types OauthApp#response_types}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#skip_groups OauthApp#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#skip_users OauthApp#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#status OauthApp#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#timeouts OauthApp#timeouts}
        :param token_endpoint_auth_method: Requested authentication method for the token endpoint. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#token_endpoint_auth_method OauthApp#token_endpoint_auth_method}
        :param tos_uri: URI to web page providing client tos (terms of service). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#tos_uri OauthApp#tos_uri}
        :param user_name_template: Username template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template OauthApp#user_name_template}
        :param user_name_template_push_status: Push username on update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template_push_status OauthApp#user_name_template_push_status}
        :param user_name_template_suffix: Username template suffix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template_suffix OauthApp#user_name_template_suffix}
        :param user_name_template_type: Username template type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template_type OauthApp#user_name_template_type}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#users OauthApp#users}
        :param wildcard_redirect: *Early Access Property*. Indicates if the client is allowed to use wildcard matching of redirect_uris. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#wildcard_redirect OauthApp#wildcard_redirect}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(groups_claim, dict):
            groups_claim = OauthAppGroupsClaim(**groups_claim)
        if isinstance(timeouts, dict):
            timeouts = OauthAppTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6feb754a5eab1d84a82ab6e0ecab310be23e380fe008da3189dc49ff85191ffe)
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#label OauthApp#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of client application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#type OauthApp#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accessibility_error_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom error page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#accessibility_error_redirect_url OauthApp#accessibility_error_redirect_url}
        '''
        result = self._values.get("accessibility_error_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_login_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom login page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#accessibility_login_redirect_url OauthApp#accessibility_login_redirect_url}
        '''
        result = self._values.get("accessibility_login_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_self_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable self service.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#accessibility_self_service OauthApp#accessibility_self_service}
        '''
        result = self._values.get("accessibility_self_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def admin_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for admins.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#admin_note OauthApp#admin_note}
        '''
        result = self._values.get("admin_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_links_json(self) -> typing.Optional[builtins.str]:
        '''Displays specific appLinks for the app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#app_links_json OauthApp#app_links_json}
        '''
        result = self._values.get("app_links_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_settings_json(self) -> typing.Optional[builtins.str]:
        '''Application settings in JSON format.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#app_settings_json OauthApp#app_settings_json}
        '''
        result = self._values.get("app_settings_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_policy(self) -> typing.Optional[builtins.str]:
        '''Id of this apps authentication policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#authentication_policy OauthApp#authentication_policy}
        '''
        result = self._values.get("authentication_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_key_rotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Requested key rotation mode.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#auto_key_rotation OauthApp#auto_key_rotation}
        '''
        result = self._values.get("auto_key_rotation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_submit_toolbar(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Display auto submit toolbar.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#auto_submit_toolbar OauthApp#auto_submit_toolbar}
        '''
        result = self._values.get("auto_submit_toolbar")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_basic_secret(self) -> typing.Optional[builtins.str]:
        '''OAuth client secret key, this can be set when token_endpoint_auth_method is client_secret_basic.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#client_basic_secret OauthApp#client_basic_secret}
        '''
        result = self._values.get("client_basic_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''OAuth client ID. If set during creation, app is created with this id.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#client_id OauthApp#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_uri(self) -> typing.Optional[builtins.str]:
        '''URI to a web page providing information about the client.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#client_uri OauthApp#client_uri}
        '''
        result = self._values.get("client_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consent_method(self) -> typing.Optional[builtins.str]:
        '''*Early Access Property*. Indicates whether user consent is required or implicit. Valid values: REQUIRED, TRUSTED. Default value is TRUSTED.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#consent_method OauthApp#consent_method}
        '''
        result = self._values.get("consent_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_client_id(self) -> typing.Optional[builtins.str]:
        '''**Deprecated** This property allows you to set your client_id during creation.

        NOTE: updating after creation will be a no-op, use client_id for that behavior instead.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#custom_client_id OauthApp#custom_client_id}
        '''
        result = self._values.get("custom_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enduser_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for end users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#enduser_note OauthApp#enduser_note}
        '''
        result = self._values.get("enduser_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grant_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of OAuth 2.0 grant types. Conditional validation params found here https://developer.okta.com/docs/api/resources/apps#credentials-settings-details. Defaults to minimum requirements per app type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#grant_types OauthApp#grant_types}
        '''
        result = self._values.get("grant_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Groups associated with the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#groups OauthApp#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def groups_claim(self) -> typing.Optional["OauthAppGroupsClaim"]:
        '''groups_claim block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#groups_claim OauthApp#groups_claim}
        '''
        result = self._values.get("groups_claim")
        return typing.cast(typing.Optional["OauthAppGroupsClaim"], result)

    @builtins.property
    def hide_ios(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon on mobile app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#hide_ios OauthApp#hide_ios}
        '''
        result = self._values.get("hide_ios")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hide_web(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon to users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#hide_web OauthApp#hide_web}
        '''
        result = self._values.get("hide_web")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#id OauthApp#id}.

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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#implicit_assignment OauthApp#implicit_assignment}
        '''
        result = self._values.get("implicit_assignment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def issuer_mode(self) -> typing.Optional[builtins.str]:
        '''*Early Access Property*.

        Indicates whether the Okta Authorization Server uses the original Okta org domain URL or a custom domain URL as the issuer of ID token for this client.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#issuer_mode OauthApp#issuer_mode}
        '''
        result = self._values.get("issuer_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jwks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OauthAppJwks"]]]:
        '''jwks block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#jwks OauthApp#jwks}
        '''
        result = self._values.get("jwks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OauthAppJwks"]]], result)

    @builtins.property
    def login_mode(self) -> typing.Optional[builtins.str]:
        '''The type of Idp-Initiated login that the client supports, if any.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#login_mode OauthApp#login_mode}
        '''
        result = self._values.get("login_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of scopes to use for the request.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#login_scopes OauthApp#login_scopes}
        '''
        result = self._values.get("login_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_uri(self) -> typing.Optional[builtins.str]:
        '''URI that initiates login.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#login_uri OauthApp#login_uri}
        '''
        result = self._values.get("login_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo(self) -> typing.Optional[builtins.str]:
        '''Local path to logo of the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#logo OauthApp#logo}
        '''
        result = self._values.get("logo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo_uri(self) -> typing.Optional[builtins.str]:
        '''URI that references a logo for the client.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#logo_uri OauthApp#logo_uri}
        '''
        result = self._values.get("logo_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def omit_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This tells the provider not to persist the application's secret to state.

        If this is ever changes from true => false your app will be recreated.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#omit_secret OauthApp#omit_secret}
        '''
        result = self._values.get("omit_secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pkce_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require Proof Key for Code Exchange (PKCE) for additional verification key rotation mode. See: https://developer.okta.com/docs/reference/api/apps/#oauth-credential-object.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#pkce_required OauthApp#pkce_required}
        '''
        result = self._values.get("pkce_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policy_uri(self) -> typing.Optional[builtins.str]:
        '''URI to web page providing client policy document.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#policy_uri OauthApp#policy_uri}
        '''
        result = self._values.get("policy_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_logout_redirect_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of URIs for redirection after logout. Note: see okta_app_oauth_post_logout_redirect_uri for appending to this list in a decentralized way.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#post_logout_redirect_uris OauthApp#post_logout_redirect_uris}
        '''
        result = self._values.get("post_logout_redirect_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''Custom JSON that represents an OAuth application's profile.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#profile OauthApp#profile}
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of URIs for use in the redirect-based flow.

        This is required for all application types except service. Note: see okta_app_oauth_redirect_uri for appending to this list in a decentralized way.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#redirect_uris OauthApp#redirect_uris}
        '''
        result = self._values.get("redirect_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def refresh_token_leeway(self) -> typing.Optional[jsii.Number]:
        '''*Early Access Property* Grace period for token rotation.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#refresh_token_leeway OauthApp#refresh_token_leeway}
        '''
        result = self._values.get("refresh_token_leeway")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def refresh_token_rotation(self) -> typing.Optional[builtins.str]:
        '''*Early Access Property* Refresh token rotation behavior.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#refresh_token_rotation OauthApp#refresh_token_rotation}
        '''
        result = self._values.get("refresh_token_rotation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of OAuth 2.0 response type strings.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#response_types OauthApp#response_types}
        '''
        result = self._values.get("response_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#skip_groups OauthApp#skip_groups}
        '''
        result = self._values.get("skip_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_users(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#skip_users OauthApp#skip_users}
        '''
        result = self._values.get("skip_users")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#status OauthApp#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OauthAppTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#timeouts OauthApp#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OauthAppTimeouts"], result)

    @builtins.property
    def token_endpoint_auth_method(self) -> typing.Optional[builtins.str]:
        '''Requested authentication method for the token endpoint.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#token_endpoint_auth_method OauthApp#token_endpoint_auth_method}
        '''
        result = self._values.get("token_endpoint_auth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tos_uri(self) -> typing.Optional[builtins.str]:
        '''URI to web page providing client tos (terms of service).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#tos_uri OauthApp#tos_uri}
        '''
        result = self._values.get("tos_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template(self) -> typing.Optional[builtins.str]:
        '''Username template.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template OauthApp#user_name_template}
        '''
        result = self._values.get("user_name_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_push_status(self) -> typing.Optional[builtins.str]:
        '''Push username on update.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template_push_status OauthApp#user_name_template_push_status}
        '''
        result = self._values.get("user_name_template_push_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_suffix(self) -> typing.Optional[builtins.str]:
        '''Username template suffix.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template_suffix OauthApp#user_name_template_suffix}
        '''
        result = self._values.get("user_name_template_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_type(self) -> typing.Optional[builtins.str]:
        '''Username template type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#user_name_template_type OauthApp#user_name_template_type}
        '''
        result = self._values.get("user_name_template_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OauthAppUsers"]]]:
        '''users block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#users OauthApp#users}
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OauthAppUsers"]]], result)

    @builtins.property
    def wildcard_redirect(self) -> typing.Optional[builtins.str]:
        '''*Early Access Property*. Indicates if the client is allowed to use wildcard matching of redirect_uris.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#wildcard_redirect OauthApp#wildcard_redirect}
        '''
        result = self._values.get("wildcard_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthAppConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.oauthApp.OauthAppGroupsClaim",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "value": "value",
        "filter_type": "filterType",
    },
)
class OauthAppGroupsClaim:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        value: builtins.str,
        filter_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the claim that will be used in the token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#name OauthApp#name}
        :param type: Groups claim type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#type OauthApp#type}
        :param value: Value of the claim. Can be an Okta Expression Language statement that evaluates at the time the token is minted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#value OauthApp#value}
        :param filter_type: Groups claim filter. Can only be set if type is FILTER. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#filter_type OauthApp#filter_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f062d45803c67e94a52d6ec4a493119df26185fc29df33fadd1cffe181b7d5)
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#name OauthApp#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Groups claim type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#type OauthApp#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the claim.

        Can be an Okta Expression Language statement that evaluates at the time the token is minted.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#value OauthApp#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_type(self) -> typing.Optional[builtins.str]:
        '''Groups claim filter. Can only be set if type is FILTER.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#filter_type OauthApp#filter_type}
        '''
        result = self._values.get("filter_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthAppGroupsClaim(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthAppGroupsClaimOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.oauthApp.OauthAppGroupsClaimOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b1ab119fdfe466a0daeff5f46fbd748acdd9e22441bbe52aad2cbdc43e95e7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5da72bb8bbc2dd87824f9cb6200ee96d196dca12bdc5deecf7eb31e4fba0aa53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06518dd36b95190392ff7ceec6f63c78b11c8e84eb438ab05945e713ea2a8af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2120b06b5a1e4a387460bc8c74641dbc4c141ee467c8b41181ef8c19294509b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c467158d42438ea6d1c71e35d671936870b24baeba686734e6044b944750d978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OauthAppGroupsClaim]:
        return typing.cast(typing.Optional[OauthAppGroupsClaim], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OauthAppGroupsClaim]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de49a52508c56c109e6731b2129893995f1cabd45d7747740a7c430d34495f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.oauthApp.OauthAppJwks",
    jsii_struct_bases=[],
    name_mapping={"kid": "kid", "kty": "kty", "e": "e", "n": "n"},
)
class OauthAppJwks:
    def __init__(
        self,
        *,
        kid: builtins.str,
        kty: builtins.str,
        e: typing.Optional[builtins.str] = None,
        n: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kid: Key ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#kid OauthApp#kid}
        :param kty: Key type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#kty OauthApp#kty}
        :param e: RSA Exponent. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#e OauthApp#e}
        :param n: RSA Modulus. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#n OauthApp#n}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec601990ba50be93b6ddf6acf47af46a0727e1130a365ed7f90f5f2137e0c564)
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#kid OauthApp#kid}
        '''
        result = self._values.get("kid")
        assert result is not None, "Required property 'kid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kty(self) -> builtins.str:
        '''Key type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#kty OauthApp#kty}
        '''
        result = self._values.get("kty")
        assert result is not None, "Required property 'kty' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def e(self) -> typing.Optional[builtins.str]:
        '''RSA Exponent.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#e OauthApp#e}
        '''
        result = self._values.get("e")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def n(self) -> typing.Optional[builtins.str]:
        '''RSA Modulus.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#n OauthApp#n}
        '''
        result = self._values.get("n")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthAppJwks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthAppJwksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.oauthApp.OauthAppJwksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__161429a1e9d12ee20c946a8a72a67da46ccb9190b01e981658c1423982fd7e18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OauthAppJwksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c078375fea7008164eee9a866239a39a98da38a5bd8c649c7833db9db4817e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthAppJwksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9ba6e3824f564e35fe9ac006c64cb7c04522e1ec43485770f91c2f399a1456)
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
            type_hints = typing.get_type_hints(_typecheckingstub__114f85a41114d4938d6327ea84a4cda6c415715f636a33f0184df87bfce88c79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4772c3fca26a2e2d970d572d37558ff5b2852e2bd10246e26cf472271107d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OauthAppJwks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OauthAppJwks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OauthAppJwks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c68515d6b7116bcb235abd0941d937133858b4eb6ff8b98efa90ada9d93119f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OauthAppJwksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.oauthApp.OauthAppJwksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f3334cff711fd88cb5dcdfd5fbe25c60b505afe5702ac30ed4d31167a24037d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08bde445fbe6c097c73a8e757248eada259c6e244a7da5ef49eb69f8a919ce84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "e", value)

    @builtins.property
    @jsii.member(jsii_name="kid")
    def kid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kid"))

    @kid.setter
    def kid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e495dc00887c594dc4983d7ab072ae559a5104c3b78c25a1b0da6bc9cf2be589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kid", value)

    @builtins.property
    @jsii.member(jsii_name="kty")
    def kty(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kty"))

    @kty.setter
    def kty(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a779cbba28e731f10b8c141acc8679e2aa3f6694a53bfb78780abae1ea90f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kty", value)

    @builtins.property
    @jsii.member(jsii_name="n")
    def n(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "n"))

    @n.setter
    def n(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c136b6d8da37381ad475fffeeeafc8635431f08bf72aed20bda3c950a884da2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "n", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OauthAppJwks, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OauthAppJwks, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OauthAppJwks, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5381bb6138368f081d3629cce25791a3db32623852832e6524dc05113d4468c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.oauthApp.OauthAppTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "read": "read", "update": "update"},
)
class OauthAppTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#create OauthApp#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#read OauthApp#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#update OauthApp#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73d516296c3d3b9f0a3e16d5f560c4accf64b7b3651c0ec1504b641d93a88035)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#create OauthApp#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#read OauthApp#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#update OauthApp#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthAppTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthAppTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.oauthApp.OauthAppTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8477fed0906f76748c54d5b98d9177d64a915aea13654a24f1f83610f084af9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92e25f58601834b6ae401de232cb53c4b6556c0e98ae3102c6eb1085b07e2e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fed3d013689b0efabcfad909b3b6d9d8dad07f0cabc1270b23013b486b8e33c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8befaafaea8ad90b8e2cafae8730cc9a84de136d2ee8a27c722fe0201601589e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OauthAppTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OauthAppTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OauthAppTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc779cf9f804d209321ceea63c90ebd1d5b41d282e7326f744f27ba4f79d760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.oauthApp.OauthAppUsers",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "password": "password", "username": "username"},
)
class OauthAppUsers:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: User ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#id OauthApp#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password: Password for user application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#password OauthApp#password}
        :param username: Username for user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#username OauthApp#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25777810cac85fc12fbf7d7faf281cb8d64eb933931bebfe62abe27cb1e8bdfa)
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#id OauthApp#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for user application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#password OauthApp#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/oauth_app#username OauthApp#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthAppUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthAppUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.oauthApp.OauthAppUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8090335a78fe6bf3c31417fbcf2a397453fc5b1e759d530f4e2a28b29708c497)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OauthAppUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__780a9ada5f080c7eb38eefbef09d4a853fbba8c7d0b3ab3f9f92bbe6b1985e99)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OauthAppUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2229abd6394fd478054db8291237922989500fa9787fdb27a16f4aecc4aad44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__128f9598d0a45c59f0b86b3a03c88733b0f6fb7a1dc24e5073fcddb6a91c5a40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09622a3c892c89ac913e542614796bce82a4f36d457a57b65671bdfe1cb3089a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OauthAppUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OauthAppUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OauthAppUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7572b8c10f4996716eab21427bced393f6901e7702f0d8c0f9ac8f59543f7a32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OauthAppUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.oauthApp.OauthAppUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64b4ec27ce90e7238bcb99b354c8758070ab2b6351e2088a726826d92c709287)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2e15c58ccb7f63cfe43ff61b771e4c75454fc2fc79233b5a2d068152eec346b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccde3b1b779414d6ced51c948c7af44c0fc66a6a23a373daaf655f463c827c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38fc01de64a7183a979b28cc49dc4ca65a7922b43420fea74e061483123939c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OauthAppUsers, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OauthAppUsers, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OauthAppUsers, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c682001b929719a9cf6d864816a9b012b80a99a73188737676a491ba034c4e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OauthApp",
    "OauthAppConfig",
    "OauthAppGroupsClaim",
    "OauthAppGroupsClaimOutputReference",
    "OauthAppJwks",
    "OauthAppJwksList",
    "OauthAppJwksOutputReference",
    "OauthAppTimeouts",
    "OauthAppTimeoutsOutputReference",
    "OauthAppUsers",
    "OauthAppUsersList",
    "OauthAppUsersOutputReference",
]

publication.publish()

def _typecheckingstub__b1bb82e6b09a30230fb162da78a640e793a72edeb0d106934c19a7eac7c9a04e(
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
    groups_claim: typing.Optional[typing.Union[OauthAppGroupsClaim, typing.Dict[builtins.str, typing.Any]]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    jwks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OauthAppJwks, typing.Dict[builtins.str, typing.Any]]]]] = None,
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
    timeouts: typing.Optional[typing.Union[OauthAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    token_endpoint_auth_method: typing.Optional[builtins.str] = None,
    tos_uri: typing.Optional[builtins.str] = None,
    user_name_template: typing.Optional[builtins.str] = None,
    user_name_template_push_status: typing.Optional[builtins.str] = None,
    user_name_template_suffix: typing.Optional[builtins.str] = None,
    user_name_template_type: typing.Optional[builtins.str] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OauthAppUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__816ef7a3375c863b529492086ebb4b5a776b5fc32c5fa592980a94bf587121e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OauthAppJwks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c67735c572102874f7842a5cbadd5e69f550f3b3993064d7ec2cd316514a334(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OauthAppUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc5ded48d1e5ee20af9180b4a3972216549d3bdac62a1d054745d0e561e34d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec735b44dc2b2a5e199b5bdfdaf2271d9ec239136a9ab25825b1c7158f84b8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5f5c32366fa334dc721bed599d1c5386e9d8edb2008454ccc47400b18f4773(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e486729f9cf211b89d455dbe851c2def8a25ecf46e2e4163a09f6432e3b04a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e2b840d3567724b832a39d512dee16efceb42ba72b0fe0ae667927b80552d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b821394d426aeff83d07c18a117b251c4aa8b8ee7790370780605a7cc35e7298(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea6ff213f0335545f9d93abe320420106a00a1cdb189c81d600ed48df803bae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ae556162623518cee8d5f755d4b03e6d2ad29e4884eee0408f151ed9c93462(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f88ac98ba44bd623153b1075e4f00b2dd9e3b10f3c6388086d8de79a6b1a55(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cb2bd5b13b9fa4787ec263aece752d18bf3534bc76897b3376641a38707e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4545c06c4e79637adffe39ac32a8ecfa4fd8c135c6231ae091364a8c3b60cbda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2ff2b25faac9f24074c93843841fa99fc604d7a3a71c57fa6c066f85aef6f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca9ae584c7a8356625aed08daaab82124024a7eb3aeb264b9e0ac882dc2701a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270eafde0b4084c2611d6b90da036da9d8ff3c479b426195bf6078bca4d651d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffc3b0455b082748f361439dc054e144d05d2b67992fcca56fd955ae4ace501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b828e6c3119ccec1a2b988206d4218956928745add2bacf68d53285e4e3afc6c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7209afa29fbb73ba3279ddfccc03a99f0b7c94c4c95f2933c014094f89b6a40(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44c8e41d7f47b99b11f85a50950daa94c9f0c64615c8ac06abbbb627ab5fa25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51fe395d57de707704cdaef6dcac753313cbec0948523224a6ad55a6d60668cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235c29aea34694dc0d5eb4912d09c4a29c9a5b65b9e455acc67ab627c20c1283(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6df8f0b9b43807d859dfd1a9b2d4a09dbb45d4e7bd97d3c60521b77efedaf46(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d750757fc3e06c2516d1337f1c5a926422e6126a5d3f0e6e6b1f8ea8ad9d45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d790dbd906985bae7bc98981ea57e4b0dc1aa60932c1af274bc11c006c4080(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b971292b9d6c10cb9e9c92ca7553c7cb613b12848e2dd5e58ac15e282265678(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf886b2709e3d96f9af429b2a7c5a5ac274808ed99d200d3ba93b56bc8733d9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0292380a635c51ab6eed3f243db1c8980671960276a0741ef766ab08a8fc71dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a869c2782335c33cc9168e24fd05aae6d38146a6bd9b65f460aa7fb6811fd0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4eda5a3b620f8591c43b47ba10f50cf1e2cd9ac0e6abd46a0893e48330ccf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccdd44186f33c6b247cf4511acc03f1c15767a1e4f14e36b946d2739dc0cfb3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070e2bb65aab8869db167ff2dfe4018524fbadce13a810d7518c473429617142(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c7e2946917319fd1cd2e1f7a0e0d8056f74fcfd91d1e1086a0ad48034c09fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d864e1df6ebb0cd2482e720b00068007bfe563d889d6eb5ac9bc0016f27a599(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d153fd3ad31f7c76cf51cf421e4faaf23736da811a2f25e9f8cdff5b707e0da0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02880391c445880c26a90b54a5170c4fa270d042b715925c8369b435ce8046a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d6d5ed4b2823ef4f51b45c183750034c5aa79e3b33f1b696678e5290ac44ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9e18b18a5690fede742e53fe496c1a65a205ddb33a17181066a09aa28aa700(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee45b93f90fa1ec19af3987be691c135d5573a97e23353af23fcb95550cce9b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101af90fcd76f7af992101c389480e47eb4d941751cdfd480bf5cae0dd8f2c46(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a29e3834a035a8d01a51a4c22f28f97645f8fdfb1e12bbddc99f3df6f4ff8bf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edcc77f3e1bf9bd40457a39edf1cfcf0181e95f2452b2308abb6953a85f24cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62b7943a02c7e8c81ceb4c2b0d53f8588f304e659d1d7d2f654fec88ce1dcf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5826ad27628a3914c424d9aa3565278e79eee96ab6ae28ff68deef1672f38d59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848d8def1467669e6ba2b245cb9417816b7975284be9f22a4faee4bce47e20af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28927c5818d947f697524d7792dcc1a59deb283003551519cc67f41da094e7f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4356f7d0e886e2d5aeef97e9f7c1fcc021ce4c04e17723a1b694b556cbf48ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4369108607e240d35adaf258f9d3d6f3d11c50d8c59eb78892e943bb8d1349bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996d0ba0c7a2a02757c49fbf336a8b146302b3070304a53f1cf0c9b5b230b140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e203f2018b0cc812f3b099310228948452d727cf22217a88de0e44f5043c19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6feb754a5eab1d84a82ab6e0ecab310be23e380fe008da3189dc49ff85191ffe(
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
    groups_claim: typing.Optional[typing.Union[OauthAppGroupsClaim, typing.Dict[builtins.str, typing.Any]]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issuer_mode: typing.Optional[builtins.str] = None,
    jwks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OauthAppJwks, typing.Dict[builtins.str, typing.Any]]]]] = None,
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
    timeouts: typing.Optional[typing.Union[OauthAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    token_endpoint_auth_method: typing.Optional[builtins.str] = None,
    tos_uri: typing.Optional[builtins.str] = None,
    user_name_template: typing.Optional[builtins.str] = None,
    user_name_template_push_status: typing.Optional[builtins.str] = None,
    user_name_template_suffix: typing.Optional[builtins.str] = None,
    user_name_template_type: typing.Optional[builtins.str] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OauthAppUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    wildcard_redirect: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f062d45803c67e94a52d6ec4a493119df26185fc29df33fadd1cffe181b7d5(
    *,
    name: builtins.str,
    type: builtins.str,
    value: builtins.str,
    filter_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1ab119fdfe466a0daeff5f46fbd748acdd9e22441bbe52aad2cbdc43e95e7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da72bb8bbc2dd87824f9cb6200ee96d196dca12bdc5deecf7eb31e4fba0aa53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06518dd36b95190392ff7ceec6f63c78b11c8e84eb438ab05945e713ea2a8af2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2120b06b5a1e4a387460bc8c74641dbc4c141ee467c8b41181ef8c19294509b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c467158d42438ea6d1c71e35d671936870b24baeba686734e6044b944750d978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de49a52508c56c109e6731b2129893995f1cabd45d7747740a7c430d34495f5a(
    value: typing.Optional[OauthAppGroupsClaim],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec601990ba50be93b6ddf6acf47af46a0727e1130a365ed7f90f5f2137e0c564(
    *,
    kid: builtins.str,
    kty: builtins.str,
    e: typing.Optional[builtins.str] = None,
    n: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161429a1e9d12ee20c946a8a72a67da46ccb9190b01e981658c1423982fd7e18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c078375fea7008164eee9a866239a39a98da38a5bd8c649c7833db9db4817e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9ba6e3824f564e35fe9ac006c64cb7c04522e1ec43485770f91c2f399a1456(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114f85a41114d4938d6327ea84a4cda6c415715f636a33f0184df87bfce88c79(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4772c3fca26a2e2d970d572d37558ff5b2852e2bd10246e26cf472271107d79(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c68515d6b7116bcb235abd0941d937133858b4eb6ff8b98efa90ada9d93119f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OauthAppJwks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3334cff711fd88cb5dcdfd5fbe25c60b505afe5702ac30ed4d31167a24037d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bde445fbe6c097c73a8e757248eada259c6e244a7da5ef49eb69f8a919ce84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e495dc00887c594dc4983d7ab072ae559a5104c3b78c25a1b0da6bc9cf2be589(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a779cbba28e731f10b8c141acc8679e2aa3f6694a53bfb78780abae1ea90f08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c136b6d8da37381ad475fffeeeafc8635431f08bf72aed20bda3c950a884da2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5381bb6138368f081d3629cce25791a3db32623852832e6524dc05113d4468c6(
    value: typing.Optional[typing.Union[OauthAppJwks, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d516296c3d3b9f0a3e16d5f560c4accf64b7b3651c0ec1504b641d93a88035(
    *,
    create: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8477fed0906f76748c54d5b98d9177d64a915aea13654a24f1f83610f084af9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e25f58601834b6ae401de232cb53c4b6556c0e98ae3102c6eb1085b07e2e04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fed3d013689b0efabcfad909b3b6d9d8dad07f0cabc1270b23013b486b8e33c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8befaafaea8ad90b8e2cafae8730cc9a84de136d2ee8a27c722fe0201601589e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc779cf9f804d209321ceea63c90ebd1d5b41d282e7326f744f27ba4f79d760(
    value: typing.Optional[typing.Union[OauthAppTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25777810cac85fc12fbf7d7faf281cb8d64eb933931bebfe62abe27cb1e8bdfa(
    *,
    id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8090335a78fe6bf3c31417fbcf2a397453fc5b1e759d530f4e2a28b29708c497(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780a9ada5f080c7eb38eefbef09d4a853fbba8c7d0b3ab3f9f92bbe6b1985e99(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2229abd6394fd478054db8291237922989500fa9787fdb27a16f4aecc4aad44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128f9598d0a45c59f0b86b3a03c88733b0f6fb7a1dc24e5073fcddb6a91c5a40(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09622a3c892c89ac913e542614796bce82a4f36d457a57b65671bdfe1cb3089a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7572b8c10f4996716eab21427bced393f6901e7702f0d8c0f9ac8f59543f7a32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OauthAppUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b4ec27ce90e7238bcb99b354c8758070ab2b6351e2088a726826d92c709287(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e15c58ccb7f63cfe43ff61b771e4c75454fc2fc79233b5a2d068152eec346b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccde3b1b779414d6ced51c948c7af44c0fc66a6a23a373daaf655f463c827c4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38fc01de64a7183a979b28cc49dc4ca65a7922b43420fea74e061483123939c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c682001b929719a9cf6d864816a9b012b80a99a73188737676a491ba034c4e8c(
    value: typing.Optional[typing.Union[OauthAppUsers, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
