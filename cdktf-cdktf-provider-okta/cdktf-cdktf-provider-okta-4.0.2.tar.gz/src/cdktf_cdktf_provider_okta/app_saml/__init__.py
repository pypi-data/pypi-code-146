'''
# `okta_app_saml`

Refer to the Terraform Registory for docs: [`okta_app_saml`](https://www.terraform.io/docs/providers/okta/r/app_saml).
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


class AppSaml(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSaml.AppSaml",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/app_saml okta_app_saml}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        label: builtins.str,
        accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        acs_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        app_settings_json: typing.Optional[builtins.str] = None,
        assertion_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        attribute_statements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppSamlAttributeStatements", typing.Dict[builtins.str, typing.Any]]]]] = None,
        audience: typing.Optional[builtins.str] = None,
        authentication_policy: typing.Optional[builtins.str] = None,
        authn_context_class_ref: typing.Optional[builtins.str] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_relay_state: typing.Optional[builtins.str] = None,
        destination: typing.Optional[builtins.str] = None,
        digest_algorithm: typing.Optional[builtins.str] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        honor_force_authn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        idp_issuer: typing.Optional[builtins.str] = None,
        implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inline_hook_id: typing.Optional[builtins.str] = None,
        key_name: typing.Optional[builtins.str] = None,
        key_years_valid: typing.Optional[jsii.Number] = None,
        logo: typing.Optional[builtins.str] = None,
        preconfigured_app: typing.Optional[builtins.str] = None,
        recipient: typing.Optional[builtins.str] = None,
        request_compressed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        response_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        saml_version: typing.Optional[builtins.str] = None,
        signature_algorithm: typing.Optional[builtins.str] = None,
        single_logout_certificate: typing.Optional[builtins.str] = None,
        single_logout_issuer: typing.Optional[builtins.str] = None,
        single_logout_url: typing.Optional[builtins.str] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sp_issuer: typing.Optional[builtins.str] = None,
        sso_url: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        subject_name_id_format: typing.Optional[builtins.str] = None,
        subject_name_id_template: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AppSamlTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_name_template: typing.Optional[builtins.str] = None,
        user_name_template_push_status: typing.Optional[builtins.str] = None,
        user_name_template_suffix: typing.Optional[builtins.str] = None,
        user_name_template_type: typing.Optional[builtins.str] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppSamlUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/app_saml okta_app_saml} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#label AppSaml#label}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#accessibility_error_redirect_url AppSaml#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#accessibility_login_redirect_url AppSaml#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#accessibility_self_service AppSaml#accessibility_self_service}
        :param acs_endpoints: List of ACS endpoints for this SAML application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#acs_endpoints AppSaml#acs_endpoints}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#admin_note AppSaml#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#app_links_json AppSaml#app_links_json}
        :param app_settings_json: Application settings in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#app_settings_json AppSaml#app_settings_json}
        :param assertion_signed: Determines whether the SAML assertion is digitally signed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#assertion_signed AppSaml#assertion_signed}
        :param attribute_statements: attribute_statements block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#attribute_statements AppSaml#attribute_statements}
        :param audience: Audience Restriction. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#audience AppSaml#audience}
        :param authentication_policy: Id of this apps authentication policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#authentication_policy AppSaml#authentication_policy}
        :param authn_context_class_ref: Identifies the SAML authentication context class for the assertion’s authentication statement. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#authn_context_class_ref AppSaml#authn_context_class_ref}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#auto_submit_toolbar AppSaml#auto_submit_toolbar}
        :param default_relay_state: Identifies a specific application resource in an IDP initiated SSO scenario. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#default_relay_state AppSaml#default_relay_state}
        :param destination: Identifies the location where the SAML response is intended to be sent inside of the SAML assertion. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#destination AppSaml#destination}
        :param digest_algorithm: Determines the digest algorithm used to digitally sign the SAML assertion and response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#digest_algorithm AppSaml#digest_algorithm}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#enduser_note AppSaml#enduser_note}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#groups AppSaml#groups}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#hide_ios AppSaml#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#hide_web AppSaml#hide_web}
        :param honor_force_authn: Prompt user to re-authenticate if SP asks for it. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#honor_force_authn AppSaml#honor_force_authn}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#id AppSaml#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idp_issuer: SAML issuer ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#idp_issuer AppSaml#idp_issuer}
        :param implicit_assignment: *Early Access Property*. Enable Federation Broker Mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#implicit_assignment AppSaml#implicit_assignment}
        :param inline_hook_id: Saml Inline Hook setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#inline_hook_id AppSaml#inline_hook_id}
        :param key_name: Certificate name. This modulates the rotation of keys. New name == new key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#key_name AppSaml#key_name}
        :param key_years_valid: Number of years the certificate is valid. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#key_years_valid AppSaml#key_years_valid}
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#logo AppSaml#logo}
        :param preconfigured_app: Name of preexisting SAML application. For instance 'slack'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#preconfigured_app AppSaml#preconfigured_app}
        :param recipient: The location where the app may present the SAML assertion. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#recipient AppSaml#recipient}
        :param request_compressed: Denotes whether the request is compressed or not. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#request_compressed AppSaml#request_compressed}
        :param response_signed: Determines whether the SAML auth response message is digitally signed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#response_signed AppSaml#response_signed}
        :param saml_version: SAML version for the app's sign-on mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#saml_version AppSaml#saml_version}
        :param signature_algorithm: Signature algorithm used ot digitally sign the assertion and response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#signature_algorithm AppSaml#signature_algorithm}
        :param single_logout_certificate: x509 encoded certificate that the Service Provider uses to sign Single Logout requests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#single_logout_certificate AppSaml#single_logout_certificate}
        :param single_logout_issuer: The issuer of the Service Provider that generates the Single Logout request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#single_logout_issuer AppSaml#single_logout_issuer}
        :param single_logout_url: The location where the logout response is sent. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#single_logout_url AppSaml#single_logout_url}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#skip_groups AppSaml#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#skip_users AppSaml#skip_users}
        :param sp_issuer: SAML SP issuer ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#sp_issuer AppSaml#sp_issuer}
        :param sso_url: Single Sign On URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#sso_url AppSaml#sso_url}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#status AppSaml#status}
        :param subject_name_id_format: Identifies the SAML processing rules. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#subject_name_id_format AppSaml#subject_name_id_format}
        :param subject_name_id_template: Template for app user's username when a user is assigned to the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#subject_name_id_template AppSaml#subject_name_id_template}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#timeouts AppSaml#timeouts}
        :param user_name_template: Username template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template AppSaml#user_name_template}
        :param user_name_template_push_status: Push username on update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template_push_status AppSaml#user_name_template_push_status}
        :param user_name_template_suffix: Username template suffix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template_suffix AppSaml#user_name_template_suffix}
        :param user_name_template_type: Username template type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template_type AppSaml#user_name_template_type}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#users AppSaml#users}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7bd16c3cc972083e789d5d0452f975c66798009c6d99851ae704aa139a6fc0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppSamlConfig(
            label=label,
            accessibility_error_redirect_url=accessibility_error_redirect_url,
            accessibility_login_redirect_url=accessibility_login_redirect_url,
            accessibility_self_service=accessibility_self_service,
            acs_endpoints=acs_endpoints,
            admin_note=admin_note,
            app_links_json=app_links_json,
            app_settings_json=app_settings_json,
            assertion_signed=assertion_signed,
            attribute_statements=attribute_statements,
            audience=audience,
            authentication_policy=authentication_policy,
            authn_context_class_ref=authn_context_class_ref,
            auto_submit_toolbar=auto_submit_toolbar,
            default_relay_state=default_relay_state,
            destination=destination,
            digest_algorithm=digest_algorithm,
            enduser_note=enduser_note,
            groups=groups,
            hide_ios=hide_ios,
            hide_web=hide_web,
            honor_force_authn=honor_force_authn,
            id=id,
            idp_issuer=idp_issuer,
            implicit_assignment=implicit_assignment,
            inline_hook_id=inline_hook_id,
            key_name=key_name,
            key_years_valid=key_years_valid,
            logo=logo,
            preconfigured_app=preconfigured_app,
            recipient=recipient,
            request_compressed=request_compressed,
            response_signed=response_signed,
            saml_version=saml_version,
            signature_algorithm=signature_algorithm,
            single_logout_certificate=single_logout_certificate,
            single_logout_issuer=single_logout_issuer,
            single_logout_url=single_logout_url,
            skip_groups=skip_groups,
            skip_users=skip_users,
            sp_issuer=sp_issuer,
            sso_url=sso_url,
            status=status,
            subject_name_id_format=subject_name_id_format,
            subject_name_id_template=subject_name_id_template,
            timeouts=timeouts,
            user_name_template=user_name_template,
            user_name_template_push_status=user_name_template_push_status,
            user_name_template_suffix=user_name_template_suffix,
            user_name_template_type=user_name_template_type,
            users=users,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAttributeStatements")
    def put_attribute_statements(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppSamlAttributeStatements", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ab677544d08857d919dfff2511ef678486d10120aa3e859c813b4b042bdc25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAttributeStatements", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#create AppSaml#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#read AppSaml#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#update AppSaml#update}.
        '''
        value = AppSamlTimeouts(create=create, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUsers")
    def put_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppSamlUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ef99e87e67ff0f788157e55468205ce2d8faab80fe75426689c503811cc6e8)
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

    @jsii.member(jsii_name="resetAcsEndpoints")
    def reset_acs_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcsEndpoints", []))

    @jsii.member(jsii_name="resetAdminNote")
    def reset_admin_note(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminNote", []))

    @jsii.member(jsii_name="resetAppLinksJson")
    def reset_app_links_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppLinksJson", []))

    @jsii.member(jsii_name="resetAppSettingsJson")
    def reset_app_settings_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSettingsJson", []))

    @jsii.member(jsii_name="resetAssertionSigned")
    def reset_assertion_signed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssertionSigned", []))

    @jsii.member(jsii_name="resetAttributeStatements")
    def reset_attribute_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeStatements", []))

    @jsii.member(jsii_name="resetAudience")
    def reset_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudience", []))

    @jsii.member(jsii_name="resetAuthenticationPolicy")
    def reset_authentication_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationPolicy", []))

    @jsii.member(jsii_name="resetAuthnContextClassRef")
    def reset_authn_context_class_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthnContextClassRef", []))

    @jsii.member(jsii_name="resetAutoSubmitToolbar")
    def reset_auto_submit_toolbar(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoSubmitToolbar", []))

    @jsii.member(jsii_name="resetDefaultRelayState")
    def reset_default_relay_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultRelayState", []))

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @jsii.member(jsii_name="resetDigestAlgorithm")
    def reset_digest_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigestAlgorithm", []))

    @jsii.member(jsii_name="resetEnduserNote")
    def reset_enduser_note(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnduserNote", []))

    @jsii.member(jsii_name="resetGroups")
    def reset_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroups", []))

    @jsii.member(jsii_name="resetHideIos")
    def reset_hide_ios(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHideIos", []))

    @jsii.member(jsii_name="resetHideWeb")
    def reset_hide_web(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHideWeb", []))

    @jsii.member(jsii_name="resetHonorForceAuthn")
    def reset_honor_force_authn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHonorForceAuthn", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdpIssuer")
    def reset_idp_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdpIssuer", []))

    @jsii.member(jsii_name="resetImplicitAssignment")
    def reset_implicit_assignment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImplicitAssignment", []))

    @jsii.member(jsii_name="resetInlineHookId")
    def reset_inline_hook_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInlineHookId", []))

    @jsii.member(jsii_name="resetKeyName")
    def reset_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyName", []))

    @jsii.member(jsii_name="resetKeyYearsValid")
    def reset_key_years_valid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyYearsValid", []))

    @jsii.member(jsii_name="resetLogo")
    def reset_logo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogo", []))

    @jsii.member(jsii_name="resetPreconfiguredApp")
    def reset_preconfigured_app(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreconfiguredApp", []))

    @jsii.member(jsii_name="resetRecipient")
    def reset_recipient(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecipient", []))

    @jsii.member(jsii_name="resetRequestCompressed")
    def reset_request_compressed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestCompressed", []))

    @jsii.member(jsii_name="resetResponseSigned")
    def reset_response_signed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseSigned", []))

    @jsii.member(jsii_name="resetSamlVersion")
    def reset_saml_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamlVersion", []))

    @jsii.member(jsii_name="resetSignatureAlgorithm")
    def reset_signature_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignatureAlgorithm", []))

    @jsii.member(jsii_name="resetSingleLogoutCertificate")
    def reset_single_logout_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleLogoutCertificate", []))

    @jsii.member(jsii_name="resetSingleLogoutIssuer")
    def reset_single_logout_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleLogoutIssuer", []))

    @jsii.member(jsii_name="resetSingleLogoutUrl")
    def reset_single_logout_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleLogoutUrl", []))

    @jsii.member(jsii_name="resetSkipGroups")
    def reset_skip_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipGroups", []))

    @jsii.member(jsii_name="resetSkipUsers")
    def reset_skip_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipUsers", []))

    @jsii.member(jsii_name="resetSpIssuer")
    def reset_sp_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpIssuer", []))

    @jsii.member(jsii_name="resetSsoUrl")
    def reset_sso_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsoUrl", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetSubjectNameIdFormat")
    def reset_subject_name_id_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectNameIdFormat", []))

    @jsii.member(jsii_name="resetSubjectNameIdTemplate")
    def reset_subject_name_id_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectNameIdTemplate", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="attributeStatements")
    def attribute_statements(self) -> "AppSamlAttributeStatementsList":
        return typing.cast("AppSamlAttributeStatementsList", jsii.get(self, "attributeStatements"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="embedUrl")
    def embed_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "embedUrl"))

    @builtins.property
    @jsii.member(jsii_name="entityKey")
    def entity_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityKey"))

    @builtins.property
    @jsii.member(jsii_name="entityUrl")
    def entity_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityUrl"))

    @builtins.property
    @jsii.member(jsii_name="features")
    def features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "features"))

    @builtins.property
    @jsii.member(jsii_name="httpPostBinding")
    def http_post_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpPostBinding"))

    @builtins.property
    @jsii.member(jsii_name="httpRedirectBinding")
    def http_redirect_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpRedirectBinding"))

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @builtins.property
    @jsii.member(jsii_name="keys")
    def keys(self) -> "AppSamlKeysList":
        return typing.cast("AppSamlKeysList", jsii.get(self, "keys"))

    @builtins.property
    @jsii.member(jsii_name="logoUrl")
    def logo_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoUrl"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="metadataUrl")
    def metadata_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataUrl"))

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
    def timeouts(self) -> "AppSamlTimeoutsOutputReference":
        return typing.cast("AppSamlTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> "AppSamlUsersList":
        return typing.cast("AppSamlUsersList", jsii.get(self, "users"))

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
    @jsii.member(jsii_name="acsEndpointsInput")
    def acs_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "acsEndpointsInput"))

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
    @jsii.member(jsii_name="assertionSignedInput")
    def assertion_signed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "assertionSignedInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeStatementsInput")
    def attribute_statements_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppSamlAttributeStatements"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppSamlAttributeStatements"]]], jsii.get(self, "attributeStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="audienceInput")
    def audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audienceInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationPolicyInput")
    def authentication_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="authnContextClassRefInput")
    def authn_context_class_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authnContextClassRefInput"))

    @builtins.property
    @jsii.member(jsii_name="autoSubmitToolbarInput")
    def auto_submit_toolbar_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoSubmitToolbarInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRelayStateInput")
    def default_relay_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultRelayStateInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="digestAlgorithmInput")
    def digest_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "digestAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="enduserNoteInput")
    def enduser_note_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enduserNoteInput"))

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
    @jsii.member(jsii_name="honorForceAuthnInput")
    def honor_force_authn_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "honorForceAuthnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="idpIssuerInput")
    def idp_issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idpIssuerInput"))

    @builtins.property
    @jsii.member(jsii_name="implicitAssignmentInput")
    def implicit_assignment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "implicitAssignmentInput"))

    @builtins.property
    @jsii.member(jsii_name="inlineHookIdInput")
    def inline_hook_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inlineHookIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyNameInput")
    def key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyYearsValidInput")
    def key_years_valid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keyYearsValidInput"))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="logoInput")
    def logo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoInput"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredAppInput")
    def preconfigured_app_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preconfiguredAppInput"))

    @builtins.property
    @jsii.member(jsii_name="recipientInput")
    def recipient_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recipientInput"))

    @builtins.property
    @jsii.member(jsii_name="requestCompressedInput")
    def request_compressed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requestCompressedInput"))

    @builtins.property
    @jsii.member(jsii_name="responseSignedInput")
    def response_signed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "responseSignedInput"))

    @builtins.property
    @jsii.member(jsii_name="samlVersionInput")
    def saml_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "samlVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="signatureAlgorithmInput")
    def signature_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signatureAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="singleLogoutCertificateInput")
    def single_logout_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "singleLogoutCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="singleLogoutIssuerInput")
    def single_logout_issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "singleLogoutIssuerInput"))

    @builtins.property
    @jsii.member(jsii_name="singleLogoutUrlInput")
    def single_logout_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "singleLogoutUrlInput"))

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
    @jsii.member(jsii_name="spIssuerInput")
    def sp_issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spIssuerInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoUrlInput")
    def sso_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssoUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectNameIdFormatInput")
    def subject_name_id_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectNameIdFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectNameIdTemplateInput")
    def subject_name_id_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectNameIdTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["AppSamlTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["AppSamlTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppSamlUsers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppSamlUsers"]]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="accessibilityErrorRedirectUrl")
    def accessibility_error_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityErrorRedirectUrl"))

    @accessibility_error_redirect_url.setter
    def accessibility_error_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3543191f120288efaf94e6b76d304448f1f0f801b9fc0e5307886fdd0d710d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilityErrorRedirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="accessibilityLoginRedirectUrl")
    def accessibility_login_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityLoginRedirectUrl"))

    @accessibility_login_redirect_url.setter
    def accessibility_login_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97bf3c13c706bc6e44b6ccc74fafa6051df06e792aaa481d03181472f822e473)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46362c0f8e4a463d63ad6d5850ac9220c24520ec87b0e5bdaae00ad50bdc1615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilitySelfService", value)

    @builtins.property
    @jsii.member(jsii_name="acsEndpoints")
    def acs_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "acsEndpoints"))

    @acs_endpoints.setter
    def acs_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18ffe6e879d890753136fb7b99a5eabbd848ef6d2fe2b987bdd50c98db207e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acsEndpoints", value)

    @builtins.property
    @jsii.member(jsii_name="adminNote")
    def admin_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminNote"))

    @admin_note.setter
    def admin_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d976932cb540bdd7d6ee8de141b8173a850cdfb3fbc8bd1c989c51ab43cef3f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminNote", value)

    @builtins.property
    @jsii.member(jsii_name="appLinksJson")
    def app_links_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLinksJson"))

    @app_links_json.setter
    def app_links_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057acdd3149f21346cdf1c84825d5af2f35217ea1a891732e41687ad58c71cff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLinksJson", value)

    @builtins.property
    @jsii.member(jsii_name="appSettingsJson")
    def app_settings_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSettingsJson"))

    @app_settings_json.setter
    def app_settings_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bdd17e9515e565921721ffbf8109fec89489a38da56524430f912a6e24fd3fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSettingsJson", value)

    @builtins.property
    @jsii.member(jsii_name="assertionSigned")
    def assertion_signed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "assertionSigned"))

    @assertion_signed.setter
    def assertion_signed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce220cf0a572aa64fb667ef45aff9b0419e0a686effbcfafdcf83fdbb7b00abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assertionSigned", value)

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__929e0ef2f87eae3ed310872d11876ae4ccdce61dcfed7d0815dd994bb28bc7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationPolicy")
    def authentication_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationPolicy"))

    @authentication_policy.setter
    def authentication_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ffe0f33fb41b09293d56a0bcb6848bc67f856b8687a5c330679308d9c4c548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="authnContextClassRef")
    def authn_context_class_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authnContextClassRef"))

    @authn_context_class_ref.setter
    def authn_context_class_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6e10096b5b3a9f9a5505c92c9f3683594b20f822a9ee33b5fd4b6cf0e0d760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authnContextClassRef", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__0e885dd21a379425a889f65ee1c7c5fd61d861023fa0c600da4eee148fa698a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubmitToolbar", value)

    @builtins.property
    @jsii.member(jsii_name="defaultRelayState")
    def default_relay_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRelayState"))

    @default_relay_state.setter
    def default_relay_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b31d68a669612e23c6f1bbaf2c2800232e8448736738ef76c3602617b468dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRelayState", value)

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1534065a0444583bcb59c85081a3b04277c4a5e8a3b3b0e0e2f7d281f5f34a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value)

    @builtins.property
    @jsii.member(jsii_name="digestAlgorithm")
    def digest_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "digestAlgorithm"))

    @digest_algorithm.setter
    def digest_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac44f44bda775152aa0485ed163b19c2ae383b4a17687a21fa11a9fc281eb3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digestAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="enduserNote")
    def enduser_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enduserNote"))

    @enduser_note.setter
    def enduser_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5682c788878c644e3e2e12e9276df8b0d113399f8b854ddc0c1ba0deef42b28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enduserNote", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da89ac7a6365a58314cdfc5c895a154a5be01bdfd927b73333d63bd6b89fb9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dc5b1a30337b0bf041db8785e5a1fe2f22ee32a5ba3ed4a976d09fb39eb14dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c51cfa0774ea2e8d633dea780f94ef8171c83935b74d7aef7e3b0fcc65f48584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hideWeb", value)

    @builtins.property
    @jsii.member(jsii_name="honorForceAuthn")
    def honor_force_authn(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "honorForceAuthn"))

    @honor_force_authn.setter
    def honor_force_authn(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347d93ccbfe930edd368a9d2b9d2f0a9f10214d0cfd6c8f0ddc4d82b4de338b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "honorForceAuthn", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd1fbbeb5c20eeb304bf0d2fed299ed1c3b36d8668464cb38446ce241a6b1045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="idpIssuer")
    def idp_issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idpIssuer"))

    @idp_issuer.setter
    def idp_issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5315c22ede92438101bd060218c02b404298321677e3fbd0c2ae034be2cc4122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpIssuer", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__73ce81a4fde63d940dcdbb4a39f44b030f729b0b167bf65f1c71b5c70d9bb125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "implicitAssignment", value)

    @builtins.property
    @jsii.member(jsii_name="inlineHookId")
    def inline_hook_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inlineHookId"))

    @inline_hook_id.setter
    def inline_hook_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abf4f2ab14745e1ebc76a9f78112cdff530cdd8bb71c2b33f262db43d2b1886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inlineHookId", value)

    @builtins.property
    @jsii.member(jsii_name="keyName")
    def key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyName"))

    @key_name.setter
    def key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9690c9f010047b08c131422b28d0bd37b2382a3d6dc15b8c0ec3aa830d3faf30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyName", value)

    @builtins.property
    @jsii.member(jsii_name="keyYearsValid")
    def key_years_valid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyYearsValid"))

    @key_years_valid.setter
    def key_years_valid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc047a5cfba7b1d1e22017447d5938ef98e98e8a0b9838718c21ec38c54f34b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyYearsValid", value)

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19c9e12a23b64af1c0d162f12e3bbd0baa0c55420e3d0fec7d462163eeab8eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="logo")
    def logo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logo"))

    @logo.setter
    def logo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895ff994bd25258ba3dba9b86f34b7d9b1294b8fdccfb4ef11b7116f35a0da6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logo", value)

    @builtins.property
    @jsii.member(jsii_name="preconfiguredApp")
    def preconfigured_app(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preconfiguredApp"))

    @preconfigured_app.setter
    def preconfigured_app(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07c41ad76ff26c878946236693788143e9b0247b25e8d422d17c25e6bf5e8f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preconfiguredApp", value)

    @builtins.property
    @jsii.member(jsii_name="recipient")
    def recipient(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recipient"))

    @recipient.setter
    def recipient(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e13ba8fcd2df93f14cf45461f497614cef290247eb46eae5262a4364dc658b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recipient", value)

    @builtins.property
    @jsii.member(jsii_name="requestCompressed")
    def request_compressed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requestCompressed"))

    @request_compressed.setter
    def request_compressed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75cfdc82ea76630a2cbfaaa87d3ac8c0c86c5ad97f11fc6d51044a9a4e269553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestCompressed", value)

    @builtins.property
    @jsii.member(jsii_name="responseSigned")
    def response_signed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "responseSigned"))

    @response_signed.setter
    def response_signed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614d68bd6e00e6699f7f8e74336ab52de5f30895b7d17b00b1030ae01adf8d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseSigned", value)

    @builtins.property
    @jsii.member(jsii_name="samlVersion")
    def saml_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "samlVersion"))

    @saml_version.setter
    def saml_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2befef2c45745086e004ce9abe4ee7334d1d0e7029f15c55e4224588cc7ba624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlVersion", value)

    @builtins.property
    @jsii.member(jsii_name="signatureAlgorithm")
    def signature_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signatureAlgorithm"))

    @signature_algorithm.setter
    def signature_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262ca624d0ff6f67b9581aae4869effbfe797be938a5ca86e84703dab103aad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signatureAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="singleLogoutCertificate")
    def single_logout_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singleLogoutCertificate"))

    @single_logout_certificate.setter
    def single_logout_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf885cb21f203ad8474d50557815f8f7d50c2514961f6ae5ac29b9524e8a274f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleLogoutCertificate", value)

    @builtins.property
    @jsii.member(jsii_name="singleLogoutIssuer")
    def single_logout_issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singleLogoutIssuer"))

    @single_logout_issuer.setter
    def single_logout_issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f531ee73893ed55393625417b333f8f547af85232a14ba0dd3f1b9a5f0fd3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleLogoutIssuer", value)

    @builtins.property
    @jsii.member(jsii_name="singleLogoutUrl")
    def single_logout_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singleLogoutUrl"))

    @single_logout_url.setter
    def single_logout_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7f1eaa019b9cb12edaf0660d14de2b851a441c9d5e4ae68e56c9e7bf3248e36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleLogoutUrl", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__b7835a9906176217413b8c62bb2158aa8f0c76ab3454142906b9de379222d676)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab5a23477b410dd1546d99cae23fa8c89f805b6430f49db8ced96311300f1d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipUsers", value)

    @builtins.property
    @jsii.member(jsii_name="spIssuer")
    def sp_issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spIssuer"))

    @sp_issuer.setter
    def sp_issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beded40bdbabc8274255c6d614df24cc7745f25fbafec6fa7a6cdae191f12006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spIssuer", value)

    @builtins.property
    @jsii.member(jsii_name="ssoUrl")
    def sso_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoUrl"))

    @sso_url.setter
    def sso_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6559a8548a4b16f9317bed8745b449684045c24da55bbae8aa781eb327fcc1c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoUrl", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef499c51a8d3f8c647c3b488bc38565e176b5b7d065a51ef7fac2283a54360a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="subjectNameIdFormat")
    def subject_name_id_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectNameIdFormat"))

    @subject_name_id_format.setter
    def subject_name_id_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60af137a5275335280295efa9296bd6788973d21eaedcef4204a641ed960e1c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectNameIdFormat", value)

    @builtins.property
    @jsii.member(jsii_name="subjectNameIdTemplate")
    def subject_name_id_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectNameIdTemplate"))

    @subject_name_id_template.setter
    def subject_name_id_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249ac8f56cce2bc933974a8046c99ba4f12af205010e7899a32bb75a50670915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectNameIdTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplate")
    def user_name_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplate"))

    @user_name_template.setter
    def user_name_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda4fd29690af86a8b33f00e431240009b14fc9401a2e7ac116202659d63b6cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplatePushStatus")
    def user_name_template_push_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplatePushStatus"))

    @user_name_template_push_status.setter
    def user_name_template_push_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91292296945f9b0e589734e9c8be1abf03a2fd3b1f7ad2561526e40b94952abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplatePushStatus", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateSuffix")
    def user_name_template_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplateSuffix"))

    @user_name_template_suffix.setter
    def user_name_template_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758e98c8f60cdc4259b7b6f1cc9ac2aac2540c6866c39ad6800c5de927be87ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplateSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateType")
    def user_name_template_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplateType"))

    @user_name_template_type.setter
    def user_name_template_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff19d16fda4ff130b76db94a95d8ee1c4c8bbbda7ea04a4065b85892a5c693b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplateType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlAttributeStatements",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "filter_type": "filterType",
        "filter_value": "filterValue",
        "namespace": "namespace",
        "type": "type",
        "values": "values",
    },
)
class AppSamlAttributeStatements:
    def __init__(
        self,
        *,
        name: builtins.str,
        filter_type: typing.Optional[builtins.str] = None,
        filter_value: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: The reference name of the attribute statement. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#name AppSaml#name}
        :param filter_type: Type of group attribute filter. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#filter_type AppSaml#filter_type}
        :param filter_value: Filter value to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#filter_value AppSaml#filter_value}
        :param namespace: The name format of the attribute. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#namespace AppSaml#namespace}
        :param type: The type of attribute statements object. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#type AppSaml#type}
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#values AppSaml#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee1bfdc331b5f25567acb8488149b5b5b87b054e2b7327de5eb6fd77dcec318)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
            check_type(argname="argument filter_value", value=filter_value, expected_type=type_hints["filter_value"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if filter_type is not None:
            self._values["filter_type"] = filter_type
        if filter_value is not None:
            self._values["filter_value"] = filter_value
        if namespace is not None:
            self._values["namespace"] = namespace
        if type is not None:
            self._values["type"] = type
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def name(self) -> builtins.str:
        '''The reference name of the attribute statement.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#name AppSaml#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_type(self) -> typing.Optional[builtins.str]:
        '''Type of group attribute filter.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#filter_type AppSaml#filter_type}
        '''
        result = self._values.get("filter_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_value(self) -> typing.Optional[builtins.str]:
        '''Filter value to use.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#filter_value AppSaml#filter_value}
        '''
        result = self._values.get("filter_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The name format of the attribute.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#namespace AppSaml#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of attribute statements object.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#type AppSaml#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#values AppSaml#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSamlAttributeStatements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppSamlAttributeStatementsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlAttributeStatementsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37612281c4d8f39f712f3556f41e274a51322d3e1f636fdb0950d4a351e007d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppSamlAttributeStatementsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892405b1f745014de95d27a4074a59e7b0870867580d9dfa9106a92f03f3d94b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppSamlAttributeStatementsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bcd9cfec9c9f3c498fe7e5f89ede8214abe5269a217094e7c2d1cfbda417695)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5fa474b6e5a0a325d77c176d28d82715d1547b6672a7997a1b1ad8b463dd540)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c05d22465a8466b38b1f28a5efae1179b1e1586f5d9b20449fe45407dbe7363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSamlAttributeStatements]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSamlAttributeStatements]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSamlAttributeStatements]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49bbf78e3e2faaa0290c67a386e86e3c49f49b1aa0a92f580249775da9665f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppSamlAttributeStatementsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlAttributeStatementsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__836508cdc6ea09fd8bca1612db9a48bfab87279a22c0459de4132ac8e00ef3d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFilterType")
    def reset_filter_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterType", []))

    @jsii.member(jsii_name="resetFilterValue")
    def reset_filter_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterValue", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="filterTypeInput")
    def filter_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="filterValueInput")
    def filter_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterValueInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="filterType")
    def filter_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterType"))

    @filter_type.setter
    def filter_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aee3a95ca9f322407f952d4c8df5b1da310f305407c067a72736e8c895a18c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterType", value)

    @builtins.property
    @jsii.member(jsii_name="filterValue")
    def filter_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterValue"))

    @filter_value.setter
    def filter_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2afdb15f2eccca4d3dfa1198a24d47d9c9fbc231ae308d99ede5718473e254f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterValue", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8da6b7a5dff069424162b4117cba8ea90700253378d97f1e34ac6fbba89b2dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d94db9b957d8fa38848c538d77d15c68015503ac7b087285eccef8a29dfa51c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__751c710d496926188ba6f7986002003b1410520f447788eb36e394e69799aaff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e444b43e5d071af99b7757d1eaacaa136782d59e145adb78f22e4b2d200030d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppSamlAttributeStatements, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppSamlAttributeStatements, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppSamlAttributeStatements, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc306beed53e5acbc8dbf957503e311d6b069e1ce4db1e7cb942d23cb066b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlConfig",
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
        "accessibility_error_redirect_url": "accessibilityErrorRedirectUrl",
        "accessibility_login_redirect_url": "accessibilityLoginRedirectUrl",
        "accessibility_self_service": "accessibilitySelfService",
        "acs_endpoints": "acsEndpoints",
        "admin_note": "adminNote",
        "app_links_json": "appLinksJson",
        "app_settings_json": "appSettingsJson",
        "assertion_signed": "assertionSigned",
        "attribute_statements": "attributeStatements",
        "audience": "audience",
        "authentication_policy": "authenticationPolicy",
        "authn_context_class_ref": "authnContextClassRef",
        "auto_submit_toolbar": "autoSubmitToolbar",
        "default_relay_state": "defaultRelayState",
        "destination": "destination",
        "digest_algorithm": "digestAlgorithm",
        "enduser_note": "enduserNote",
        "groups": "groups",
        "hide_ios": "hideIos",
        "hide_web": "hideWeb",
        "honor_force_authn": "honorForceAuthn",
        "id": "id",
        "idp_issuer": "idpIssuer",
        "implicit_assignment": "implicitAssignment",
        "inline_hook_id": "inlineHookId",
        "key_name": "keyName",
        "key_years_valid": "keyYearsValid",
        "logo": "logo",
        "preconfigured_app": "preconfiguredApp",
        "recipient": "recipient",
        "request_compressed": "requestCompressed",
        "response_signed": "responseSigned",
        "saml_version": "samlVersion",
        "signature_algorithm": "signatureAlgorithm",
        "single_logout_certificate": "singleLogoutCertificate",
        "single_logout_issuer": "singleLogoutIssuer",
        "single_logout_url": "singleLogoutUrl",
        "skip_groups": "skipGroups",
        "skip_users": "skipUsers",
        "sp_issuer": "spIssuer",
        "sso_url": "ssoUrl",
        "status": "status",
        "subject_name_id_format": "subjectNameIdFormat",
        "subject_name_id_template": "subjectNameIdTemplate",
        "timeouts": "timeouts",
        "user_name_template": "userNameTemplate",
        "user_name_template_push_status": "userNameTemplatePushStatus",
        "user_name_template_suffix": "userNameTemplateSuffix",
        "user_name_template_type": "userNameTemplateType",
        "users": "users",
    },
)
class AppSamlConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        acs_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        app_settings_json: typing.Optional[builtins.str] = None,
        assertion_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        attribute_statements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppSamlAttributeStatements, typing.Dict[builtins.str, typing.Any]]]]] = None,
        audience: typing.Optional[builtins.str] = None,
        authentication_policy: typing.Optional[builtins.str] = None,
        authn_context_class_ref: typing.Optional[builtins.str] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_relay_state: typing.Optional[builtins.str] = None,
        destination: typing.Optional[builtins.str] = None,
        digest_algorithm: typing.Optional[builtins.str] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        honor_force_authn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        idp_issuer: typing.Optional[builtins.str] = None,
        implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inline_hook_id: typing.Optional[builtins.str] = None,
        key_name: typing.Optional[builtins.str] = None,
        key_years_valid: typing.Optional[jsii.Number] = None,
        logo: typing.Optional[builtins.str] = None,
        preconfigured_app: typing.Optional[builtins.str] = None,
        recipient: typing.Optional[builtins.str] = None,
        request_compressed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        response_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        saml_version: typing.Optional[builtins.str] = None,
        signature_algorithm: typing.Optional[builtins.str] = None,
        single_logout_certificate: typing.Optional[builtins.str] = None,
        single_logout_issuer: typing.Optional[builtins.str] = None,
        single_logout_url: typing.Optional[builtins.str] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sp_issuer: typing.Optional[builtins.str] = None,
        sso_url: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        subject_name_id_format: typing.Optional[builtins.str] = None,
        subject_name_id_template: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AppSamlTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_name_template: typing.Optional[builtins.str] = None,
        user_name_template_push_status: typing.Optional[builtins.str] = None,
        user_name_template_suffix: typing.Optional[builtins.str] = None,
        user_name_template_type: typing.Optional[builtins.str] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppSamlUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#label AppSaml#label}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#accessibility_error_redirect_url AppSaml#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#accessibility_login_redirect_url AppSaml#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#accessibility_self_service AppSaml#accessibility_self_service}
        :param acs_endpoints: List of ACS endpoints for this SAML application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#acs_endpoints AppSaml#acs_endpoints}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#admin_note AppSaml#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#app_links_json AppSaml#app_links_json}
        :param app_settings_json: Application settings in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#app_settings_json AppSaml#app_settings_json}
        :param assertion_signed: Determines whether the SAML assertion is digitally signed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#assertion_signed AppSaml#assertion_signed}
        :param attribute_statements: attribute_statements block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#attribute_statements AppSaml#attribute_statements}
        :param audience: Audience Restriction. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#audience AppSaml#audience}
        :param authentication_policy: Id of this apps authentication policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#authentication_policy AppSaml#authentication_policy}
        :param authn_context_class_ref: Identifies the SAML authentication context class for the assertion’s authentication statement. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#authn_context_class_ref AppSaml#authn_context_class_ref}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#auto_submit_toolbar AppSaml#auto_submit_toolbar}
        :param default_relay_state: Identifies a specific application resource in an IDP initiated SSO scenario. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#default_relay_state AppSaml#default_relay_state}
        :param destination: Identifies the location where the SAML response is intended to be sent inside of the SAML assertion. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#destination AppSaml#destination}
        :param digest_algorithm: Determines the digest algorithm used to digitally sign the SAML assertion and response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#digest_algorithm AppSaml#digest_algorithm}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#enduser_note AppSaml#enduser_note}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#groups AppSaml#groups}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#hide_ios AppSaml#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#hide_web AppSaml#hide_web}
        :param honor_force_authn: Prompt user to re-authenticate if SP asks for it. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#honor_force_authn AppSaml#honor_force_authn}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#id AppSaml#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idp_issuer: SAML issuer ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#idp_issuer AppSaml#idp_issuer}
        :param implicit_assignment: *Early Access Property*. Enable Federation Broker Mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#implicit_assignment AppSaml#implicit_assignment}
        :param inline_hook_id: Saml Inline Hook setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#inline_hook_id AppSaml#inline_hook_id}
        :param key_name: Certificate name. This modulates the rotation of keys. New name == new key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#key_name AppSaml#key_name}
        :param key_years_valid: Number of years the certificate is valid. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#key_years_valid AppSaml#key_years_valid}
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#logo AppSaml#logo}
        :param preconfigured_app: Name of preexisting SAML application. For instance 'slack'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#preconfigured_app AppSaml#preconfigured_app}
        :param recipient: The location where the app may present the SAML assertion. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#recipient AppSaml#recipient}
        :param request_compressed: Denotes whether the request is compressed or not. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#request_compressed AppSaml#request_compressed}
        :param response_signed: Determines whether the SAML auth response message is digitally signed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#response_signed AppSaml#response_signed}
        :param saml_version: SAML version for the app's sign-on mode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#saml_version AppSaml#saml_version}
        :param signature_algorithm: Signature algorithm used ot digitally sign the assertion and response. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#signature_algorithm AppSaml#signature_algorithm}
        :param single_logout_certificate: x509 encoded certificate that the Service Provider uses to sign Single Logout requests. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#single_logout_certificate AppSaml#single_logout_certificate}
        :param single_logout_issuer: The issuer of the Service Provider that generates the Single Logout request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#single_logout_issuer AppSaml#single_logout_issuer}
        :param single_logout_url: The location where the logout response is sent. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#single_logout_url AppSaml#single_logout_url}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#skip_groups AppSaml#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#skip_users AppSaml#skip_users}
        :param sp_issuer: SAML SP issuer ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#sp_issuer AppSaml#sp_issuer}
        :param sso_url: Single Sign On URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#sso_url AppSaml#sso_url}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#status AppSaml#status}
        :param subject_name_id_format: Identifies the SAML processing rules. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#subject_name_id_format AppSaml#subject_name_id_format}
        :param subject_name_id_template: Template for app user's username when a user is assigned to the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#subject_name_id_template AppSaml#subject_name_id_template}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#timeouts AppSaml#timeouts}
        :param user_name_template: Username template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template AppSaml#user_name_template}
        :param user_name_template_push_status: Push username on update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template_push_status AppSaml#user_name_template_push_status}
        :param user_name_template_suffix: Username template suffix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template_suffix AppSaml#user_name_template_suffix}
        :param user_name_template_type: Username template type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template_type AppSaml#user_name_template_type}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#users AppSaml#users}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = AppSamlTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57e17e576729b01b2e0754774196cc1d0054b4365a294aad8d08ded459a19d0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument accessibility_error_redirect_url", value=accessibility_error_redirect_url, expected_type=type_hints["accessibility_error_redirect_url"])
            check_type(argname="argument accessibility_login_redirect_url", value=accessibility_login_redirect_url, expected_type=type_hints["accessibility_login_redirect_url"])
            check_type(argname="argument accessibility_self_service", value=accessibility_self_service, expected_type=type_hints["accessibility_self_service"])
            check_type(argname="argument acs_endpoints", value=acs_endpoints, expected_type=type_hints["acs_endpoints"])
            check_type(argname="argument admin_note", value=admin_note, expected_type=type_hints["admin_note"])
            check_type(argname="argument app_links_json", value=app_links_json, expected_type=type_hints["app_links_json"])
            check_type(argname="argument app_settings_json", value=app_settings_json, expected_type=type_hints["app_settings_json"])
            check_type(argname="argument assertion_signed", value=assertion_signed, expected_type=type_hints["assertion_signed"])
            check_type(argname="argument attribute_statements", value=attribute_statements, expected_type=type_hints["attribute_statements"])
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
            check_type(argname="argument authentication_policy", value=authentication_policy, expected_type=type_hints["authentication_policy"])
            check_type(argname="argument authn_context_class_ref", value=authn_context_class_ref, expected_type=type_hints["authn_context_class_ref"])
            check_type(argname="argument auto_submit_toolbar", value=auto_submit_toolbar, expected_type=type_hints["auto_submit_toolbar"])
            check_type(argname="argument default_relay_state", value=default_relay_state, expected_type=type_hints["default_relay_state"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument digest_algorithm", value=digest_algorithm, expected_type=type_hints["digest_algorithm"])
            check_type(argname="argument enduser_note", value=enduser_note, expected_type=type_hints["enduser_note"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument hide_ios", value=hide_ios, expected_type=type_hints["hide_ios"])
            check_type(argname="argument hide_web", value=hide_web, expected_type=type_hints["hide_web"])
            check_type(argname="argument honor_force_authn", value=honor_force_authn, expected_type=type_hints["honor_force_authn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument idp_issuer", value=idp_issuer, expected_type=type_hints["idp_issuer"])
            check_type(argname="argument implicit_assignment", value=implicit_assignment, expected_type=type_hints["implicit_assignment"])
            check_type(argname="argument inline_hook_id", value=inline_hook_id, expected_type=type_hints["inline_hook_id"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument key_years_valid", value=key_years_valid, expected_type=type_hints["key_years_valid"])
            check_type(argname="argument logo", value=logo, expected_type=type_hints["logo"])
            check_type(argname="argument preconfigured_app", value=preconfigured_app, expected_type=type_hints["preconfigured_app"])
            check_type(argname="argument recipient", value=recipient, expected_type=type_hints["recipient"])
            check_type(argname="argument request_compressed", value=request_compressed, expected_type=type_hints["request_compressed"])
            check_type(argname="argument response_signed", value=response_signed, expected_type=type_hints["response_signed"])
            check_type(argname="argument saml_version", value=saml_version, expected_type=type_hints["saml_version"])
            check_type(argname="argument signature_algorithm", value=signature_algorithm, expected_type=type_hints["signature_algorithm"])
            check_type(argname="argument single_logout_certificate", value=single_logout_certificate, expected_type=type_hints["single_logout_certificate"])
            check_type(argname="argument single_logout_issuer", value=single_logout_issuer, expected_type=type_hints["single_logout_issuer"])
            check_type(argname="argument single_logout_url", value=single_logout_url, expected_type=type_hints["single_logout_url"])
            check_type(argname="argument skip_groups", value=skip_groups, expected_type=type_hints["skip_groups"])
            check_type(argname="argument skip_users", value=skip_users, expected_type=type_hints["skip_users"])
            check_type(argname="argument sp_issuer", value=sp_issuer, expected_type=type_hints["sp_issuer"])
            check_type(argname="argument sso_url", value=sso_url, expected_type=type_hints["sso_url"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument subject_name_id_format", value=subject_name_id_format, expected_type=type_hints["subject_name_id_format"])
            check_type(argname="argument subject_name_id_template", value=subject_name_id_template, expected_type=type_hints["subject_name_id_template"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_name_template", value=user_name_template, expected_type=type_hints["user_name_template"])
            check_type(argname="argument user_name_template_push_status", value=user_name_template_push_status, expected_type=type_hints["user_name_template_push_status"])
            check_type(argname="argument user_name_template_suffix", value=user_name_template_suffix, expected_type=type_hints["user_name_template_suffix"])
            check_type(argname="argument user_name_template_type", value=user_name_template_type, expected_type=type_hints["user_name_template_type"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label": label,
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
        if acs_endpoints is not None:
            self._values["acs_endpoints"] = acs_endpoints
        if admin_note is not None:
            self._values["admin_note"] = admin_note
        if app_links_json is not None:
            self._values["app_links_json"] = app_links_json
        if app_settings_json is not None:
            self._values["app_settings_json"] = app_settings_json
        if assertion_signed is not None:
            self._values["assertion_signed"] = assertion_signed
        if attribute_statements is not None:
            self._values["attribute_statements"] = attribute_statements
        if audience is not None:
            self._values["audience"] = audience
        if authentication_policy is not None:
            self._values["authentication_policy"] = authentication_policy
        if authn_context_class_ref is not None:
            self._values["authn_context_class_ref"] = authn_context_class_ref
        if auto_submit_toolbar is not None:
            self._values["auto_submit_toolbar"] = auto_submit_toolbar
        if default_relay_state is not None:
            self._values["default_relay_state"] = default_relay_state
        if destination is not None:
            self._values["destination"] = destination
        if digest_algorithm is not None:
            self._values["digest_algorithm"] = digest_algorithm
        if enduser_note is not None:
            self._values["enduser_note"] = enduser_note
        if groups is not None:
            self._values["groups"] = groups
        if hide_ios is not None:
            self._values["hide_ios"] = hide_ios
        if hide_web is not None:
            self._values["hide_web"] = hide_web
        if honor_force_authn is not None:
            self._values["honor_force_authn"] = honor_force_authn
        if id is not None:
            self._values["id"] = id
        if idp_issuer is not None:
            self._values["idp_issuer"] = idp_issuer
        if implicit_assignment is not None:
            self._values["implicit_assignment"] = implicit_assignment
        if inline_hook_id is not None:
            self._values["inline_hook_id"] = inline_hook_id
        if key_name is not None:
            self._values["key_name"] = key_name
        if key_years_valid is not None:
            self._values["key_years_valid"] = key_years_valid
        if logo is not None:
            self._values["logo"] = logo
        if preconfigured_app is not None:
            self._values["preconfigured_app"] = preconfigured_app
        if recipient is not None:
            self._values["recipient"] = recipient
        if request_compressed is not None:
            self._values["request_compressed"] = request_compressed
        if response_signed is not None:
            self._values["response_signed"] = response_signed
        if saml_version is not None:
            self._values["saml_version"] = saml_version
        if signature_algorithm is not None:
            self._values["signature_algorithm"] = signature_algorithm
        if single_logout_certificate is not None:
            self._values["single_logout_certificate"] = single_logout_certificate
        if single_logout_issuer is not None:
            self._values["single_logout_issuer"] = single_logout_issuer
        if single_logout_url is not None:
            self._values["single_logout_url"] = single_logout_url
        if skip_groups is not None:
            self._values["skip_groups"] = skip_groups
        if skip_users is not None:
            self._values["skip_users"] = skip_users
        if sp_issuer is not None:
            self._values["sp_issuer"] = sp_issuer
        if sso_url is not None:
            self._values["sso_url"] = sso_url
        if status is not None:
            self._values["status"] = status
        if subject_name_id_format is not None:
            self._values["subject_name_id_format"] = subject_name_id_format
        if subject_name_id_template is not None:
            self._values["subject_name_id_template"] = subject_name_id_template
        if timeouts is not None:
            self._values["timeouts"] = timeouts
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#label AppSaml#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accessibility_error_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom error page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#accessibility_error_redirect_url AppSaml#accessibility_error_redirect_url}
        '''
        result = self._values.get("accessibility_error_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_login_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom login page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#accessibility_login_redirect_url AppSaml#accessibility_login_redirect_url}
        '''
        result = self._values.get("accessibility_login_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_self_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable self service.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#accessibility_self_service AppSaml#accessibility_self_service}
        '''
        result = self._values.get("accessibility_self_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def acs_endpoints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of ACS endpoints for this SAML application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#acs_endpoints AppSaml#acs_endpoints}
        '''
        result = self._values.get("acs_endpoints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def admin_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for admins.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#admin_note AppSaml#admin_note}
        '''
        result = self._values.get("admin_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_links_json(self) -> typing.Optional[builtins.str]:
        '''Displays specific appLinks for the app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#app_links_json AppSaml#app_links_json}
        '''
        result = self._values.get("app_links_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_settings_json(self) -> typing.Optional[builtins.str]:
        '''Application settings in JSON format.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#app_settings_json AppSaml#app_settings_json}
        '''
        result = self._values.get("app_settings_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assertion_signed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether the SAML assertion is digitally signed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#assertion_signed AppSaml#assertion_signed}
        '''
        result = self._values.get("assertion_signed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def attribute_statements(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSamlAttributeStatements]]]:
        '''attribute_statements block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#attribute_statements AppSaml#attribute_statements}
        '''
        result = self._values.get("attribute_statements")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSamlAttributeStatements]]], result)

    @builtins.property
    def audience(self) -> typing.Optional[builtins.str]:
        '''Audience Restriction.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#audience AppSaml#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_policy(self) -> typing.Optional[builtins.str]:
        '''Id of this apps authentication policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#authentication_policy AppSaml#authentication_policy}
        '''
        result = self._values.get("authentication_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authn_context_class_ref(self) -> typing.Optional[builtins.str]:
        '''Identifies the SAML authentication context class for the assertion’s authentication statement.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#authn_context_class_ref AppSaml#authn_context_class_ref}
        '''
        result = self._values.get("authn_context_class_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_submit_toolbar(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Display auto submit toolbar.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#auto_submit_toolbar AppSaml#auto_submit_toolbar}
        '''
        result = self._values.get("auto_submit_toolbar")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_relay_state(self) -> typing.Optional[builtins.str]:
        '''Identifies a specific application resource in an IDP initiated SSO scenario.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#default_relay_state AppSaml#default_relay_state}
        '''
        result = self._values.get("default_relay_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''Identifies the location where the SAML response is intended to be sent inside of the SAML assertion.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#destination AppSaml#destination}
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def digest_algorithm(self) -> typing.Optional[builtins.str]:
        '''Determines the digest algorithm used to digitally sign the SAML assertion and response.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#digest_algorithm AppSaml#digest_algorithm}
        '''
        result = self._values.get("digest_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enduser_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for end users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#enduser_note AppSaml#enduser_note}
        '''
        result = self._values.get("enduser_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Groups associated with the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#groups AppSaml#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def hide_ios(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon on mobile app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#hide_ios AppSaml#hide_ios}
        '''
        result = self._values.get("hide_ios")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hide_web(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon to users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#hide_web AppSaml#hide_web}
        '''
        result = self._values.get("hide_web")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def honor_force_authn(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prompt user to re-authenticate if SP asks for it.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#honor_force_authn AppSaml#honor_force_authn}
        '''
        result = self._values.get("honor_force_authn")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#id AppSaml#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idp_issuer(self) -> typing.Optional[builtins.str]:
        '''SAML issuer ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#idp_issuer AppSaml#idp_issuer}
        '''
        result = self._values.get("idp_issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def implicit_assignment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''*Early Access Property*. Enable Federation Broker Mode.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#implicit_assignment AppSaml#implicit_assignment}
        '''
        result = self._values.get("implicit_assignment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def inline_hook_id(self) -> typing.Optional[builtins.str]:
        '''Saml Inline Hook setting.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#inline_hook_id AppSaml#inline_hook_id}
        '''
        result = self._values.get("inline_hook_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''Certificate name. This modulates the rotation of keys. New name == new key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#key_name AppSaml#key_name}
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_years_valid(self) -> typing.Optional[jsii.Number]:
        '''Number of years the certificate is valid.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#key_years_valid AppSaml#key_years_valid}
        '''
        result = self._values.get("key_years_valid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def logo(self) -> typing.Optional[builtins.str]:
        '''Local path to logo of the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#logo AppSaml#logo}
        '''
        result = self._values.get("logo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preconfigured_app(self) -> typing.Optional[builtins.str]:
        '''Name of preexisting SAML application. For instance 'slack'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#preconfigured_app AppSaml#preconfigured_app}
        '''
        result = self._values.get("preconfigured_app")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipient(self) -> typing.Optional[builtins.str]:
        '''The location where the app may present the SAML assertion.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#recipient AppSaml#recipient}
        '''
        result = self._values.get("recipient")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_compressed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Denotes whether the request is compressed or not.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#request_compressed AppSaml#request_compressed}
        '''
        result = self._values.get("request_compressed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def response_signed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether the SAML auth response message is digitally signed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#response_signed AppSaml#response_signed}
        '''
        result = self._values.get("response_signed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def saml_version(self) -> typing.Optional[builtins.str]:
        '''SAML version for the app's sign-on mode.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#saml_version AppSaml#saml_version}
        '''
        result = self._values.get("saml_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signature_algorithm(self) -> typing.Optional[builtins.str]:
        '''Signature algorithm used ot digitally sign the assertion and response.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#signature_algorithm AppSaml#signature_algorithm}
        '''
        result = self._values.get("signature_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_logout_certificate(self) -> typing.Optional[builtins.str]:
        '''x509 encoded certificate that the Service Provider uses to sign Single Logout requests.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#single_logout_certificate AppSaml#single_logout_certificate}
        '''
        result = self._values.get("single_logout_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_logout_issuer(self) -> typing.Optional[builtins.str]:
        '''The issuer of the Service Provider that generates the Single Logout request.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#single_logout_issuer AppSaml#single_logout_issuer}
        '''
        result = self._values.get("single_logout_issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_logout_url(self) -> typing.Optional[builtins.str]:
        '''The location where the logout response is sent.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#single_logout_url AppSaml#single_logout_url}
        '''
        result = self._values.get("single_logout_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#skip_groups AppSaml#skip_groups}
        '''
        result = self._values.get("skip_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_users(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#skip_users AppSaml#skip_users}
        '''
        result = self._values.get("skip_users")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sp_issuer(self) -> typing.Optional[builtins.str]:
        '''SAML SP issuer ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#sp_issuer AppSaml#sp_issuer}
        '''
        result = self._values.get("sp_issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sso_url(self) -> typing.Optional[builtins.str]:
        '''Single Sign On URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#sso_url AppSaml#sso_url}
        '''
        result = self._values.get("sso_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#status AppSaml#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_name_id_format(self) -> typing.Optional[builtins.str]:
        '''Identifies the SAML processing rules.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#subject_name_id_format AppSaml#subject_name_id_format}
        '''
        result = self._values.get("subject_name_id_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_name_id_template(self) -> typing.Optional[builtins.str]:
        '''Template for app user's username when a user is assigned to the app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#subject_name_id_template AppSaml#subject_name_id_template}
        '''
        result = self._values.get("subject_name_id_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AppSamlTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#timeouts AppSaml#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AppSamlTimeouts"], result)

    @builtins.property
    def user_name_template(self) -> typing.Optional[builtins.str]:
        '''Username template.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template AppSaml#user_name_template}
        '''
        result = self._values.get("user_name_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_push_status(self) -> typing.Optional[builtins.str]:
        '''Push username on update.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template_push_status AppSaml#user_name_template_push_status}
        '''
        result = self._values.get("user_name_template_push_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_suffix(self) -> typing.Optional[builtins.str]:
        '''Username template suffix.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template_suffix AppSaml#user_name_template_suffix}
        '''
        result = self._values.get("user_name_template_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_type(self) -> typing.Optional[builtins.str]:
        '''Username template type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#user_name_template_type AppSaml#user_name_template_type}
        '''
        result = self._values.get("user_name_template_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppSamlUsers"]]]:
        '''users block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#users AppSaml#users}
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppSamlUsers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSamlConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlKeys",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppSamlKeys:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSamlKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppSamlKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlKeysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cae5e19cb9e75b754fba105ce547829021349282e72e7002fc121de62aa1dfb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppSamlKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef75f3880028136516d0795b05097bdc79010eed86085026a6d98a5ab3b40533)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppSamlKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8612392dd0d083360828def2167274863c3ae69818d4aa0ac6d8ce3f913f9ee8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__635c331cee52b1f9eb2cc7880bc72720abd44b4ef5563d99f2518cae40b134dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ae6998cb9aeeec6f016608b7a81c793ee186e0d5a7be8a1b86791b167c4e190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class AppSamlKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99d45b7645794f57375988ce0826bff4d92b946855fac55f14405b64ac3165fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="e")
    def e(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "e"))

    @builtins.property
    @jsii.member(jsii_name="expiresAt")
    def expires_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiresAt"))

    @builtins.property
    @jsii.member(jsii_name="kid")
    def kid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kid"))

    @builtins.property
    @jsii.member(jsii_name="kty")
    def kty(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kty"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdated")
    def last_updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdated"))

    @builtins.property
    @jsii.member(jsii_name="n")
    def n(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "n"))

    @builtins.property
    @jsii.member(jsii_name="use")
    def use(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "use"))

    @builtins.property
    @jsii.member(jsii_name="x5C")
    def x5_c(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "x5C"))

    @builtins.property
    @jsii.member(jsii_name="x5TS256")
    def x5_ts256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "x5TS256"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppSamlKeys]:
        return typing.cast(typing.Optional[AppSamlKeys], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppSamlKeys]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b781186d5e52118bb6133e41be7f7f56f2398f3b04727774a7c600225543d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "read": "read", "update": "update"},
)
class AppSamlTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#create AppSaml#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#read AppSaml#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#update AppSaml#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0af0921536fc5288aa4fe76e1a6260630775282ef8a7e0648e92e6beaccdb6e)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#create AppSaml#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#read AppSaml#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#update AppSaml#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSamlTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppSamlTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a6c5b716a68d3e85490f9bf793c07a80703b93c7e069871da0c4507539df686)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72bf6fefb1a4984ea1a982ff5d230be7a78f673b103bcbedcd341be91d432c33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c3ee3865bf0626cda75af07607ebb59e5901a6cf85dc3fb9b76463a8931f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c63d5c6e7708dbeb92c8eb6b790b6dbdc4d38c7e1d25ebc7ea71ec33ed79c520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppSamlTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppSamlTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppSamlTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09008875994305e3d1c5338a9d1f05d3c94eb72d90fb54e4aed6da7344816647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlUsers",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "password": "password", "username": "username"},
)
class AppSamlUsers:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: User ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#id AppSaml#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password: Password for user application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#password AppSaml#password}
        :param username: Username for user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#username AppSaml#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b6ea05c13c3efda29fda2368e244da4c40811be73e4b43a93fed57ce9f25fd)
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#id AppSaml#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for user application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#password AppSaml#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_saml#username AppSaml#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSamlUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppSamlUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e583c3605d4182fd9caec9e78b7b89d742c2de1eae0dc211b6f9ee945b1425c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppSamlUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39dce7f39735ce178c3d489e3b9b650765bc84f32a1d70ff23e83fa8f675d237)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppSamlUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957a1f390276da3ade4fa8a54aa10b1f34e51fee654d1ea0d39483b067f7c99f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ecef7cf6c2917bc9c17823a136675f9ab187ea24e7ca3b778fbebd032d67ca1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61eef1ac8b0f0bc145eddf05f8193003ef3ed9a5fe9beaa2971b25edbe5f288f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSamlUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSamlUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSamlUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5fc14c6bbc2a0489a4b05321ef6d5dcc13a8feb7fa603b8f756d32b8ec8db83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppSamlUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSaml.AppSamlUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f48ef58e41878a1258df9328dcbf4c2cc96ad469b6f97daa4fcfd9f17f16fff0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9daf0ab795fe2dbc172f9e6af4ee3f7d742c45ed4d300b47ca1520d8528cac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f2c500355ebf630b60b6075f184cb43b3059f36c0e4457fa62ecc386ff7bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8628144069bddcddb2369081ca770f5555d13329dda173db99dcdb7d247ccd72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppSamlUsers, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppSamlUsers, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppSamlUsers, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e229d98a08475db9c1279e37234fa77239010e89ea7e691705f6ade1758a555b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AppSaml",
    "AppSamlAttributeStatements",
    "AppSamlAttributeStatementsList",
    "AppSamlAttributeStatementsOutputReference",
    "AppSamlConfig",
    "AppSamlKeys",
    "AppSamlKeysList",
    "AppSamlKeysOutputReference",
    "AppSamlTimeouts",
    "AppSamlTimeoutsOutputReference",
    "AppSamlUsers",
    "AppSamlUsersList",
    "AppSamlUsersOutputReference",
]

publication.publish()

def _typecheckingstub__db7bd16c3cc972083e789d5d0452f975c66798009c6d99851ae704aa139a6fc0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    label: builtins.str,
    accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    acs_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    app_settings_json: typing.Optional[builtins.str] = None,
    assertion_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    attribute_statements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppSamlAttributeStatements, typing.Dict[builtins.str, typing.Any]]]]] = None,
    audience: typing.Optional[builtins.str] = None,
    authentication_policy: typing.Optional[builtins.str] = None,
    authn_context_class_ref: typing.Optional[builtins.str] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_relay_state: typing.Optional[builtins.str] = None,
    destination: typing.Optional[builtins.str] = None,
    digest_algorithm: typing.Optional[builtins.str] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    honor_force_authn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    idp_issuer: typing.Optional[builtins.str] = None,
    implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    inline_hook_id: typing.Optional[builtins.str] = None,
    key_name: typing.Optional[builtins.str] = None,
    key_years_valid: typing.Optional[jsii.Number] = None,
    logo: typing.Optional[builtins.str] = None,
    preconfigured_app: typing.Optional[builtins.str] = None,
    recipient: typing.Optional[builtins.str] = None,
    request_compressed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    response_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    saml_version: typing.Optional[builtins.str] = None,
    signature_algorithm: typing.Optional[builtins.str] = None,
    single_logout_certificate: typing.Optional[builtins.str] = None,
    single_logout_issuer: typing.Optional[builtins.str] = None,
    single_logout_url: typing.Optional[builtins.str] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sp_issuer: typing.Optional[builtins.str] = None,
    sso_url: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    subject_name_id_format: typing.Optional[builtins.str] = None,
    subject_name_id_template: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AppSamlTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_name_template: typing.Optional[builtins.str] = None,
    user_name_template_push_status: typing.Optional[builtins.str] = None,
    user_name_template_suffix: typing.Optional[builtins.str] = None,
    user_name_template_type: typing.Optional[builtins.str] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppSamlUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__a9ab677544d08857d919dfff2511ef678486d10120aa3e859c813b4b042bdc25(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppSamlAttributeStatements, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ef99e87e67ff0f788157e55468205ce2d8faab80fe75426689c503811cc6e8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppSamlUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3543191f120288efaf94e6b76d304448f1f0f801b9fc0e5307886fdd0d710d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97bf3c13c706bc6e44b6ccc74fafa6051df06e792aaa481d03181472f822e473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46362c0f8e4a463d63ad6d5850ac9220c24520ec87b0e5bdaae00ad50bdc1615(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18ffe6e879d890753136fb7b99a5eabbd848ef6d2fe2b987bdd50c98db207e0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d976932cb540bdd7d6ee8de141b8173a850cdfb3fbc8bd1c989c51ab43cef3f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057acdd3149f21346cdf1c84825d5af2f35217ea1a891732e41687ad58c71cff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdd17e9515e565921721ffbf8109fec89489a38da56524430f912a6e24fd3fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce220cf0a572aa64fb667ef45aff9b0419e0a686effbcfafdcf83fdbb7b00abd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929e0ef2f87eae3ed310872d11876ae4ccdce61dcfed7d0815dd994bb28bc7e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ffe0f33fb41b09293d56a0bcb6848bc67f856b8687a5c330679308d9c4c548(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6e10096b5b3a9f9a5505c92c9f3683594b20f822a9ee33b5fd4b6cf0e0d760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e885dd21a379425a889f65ee1c7c5fd61d861023fa0c600da4eee148fa698a0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b31d68a669612e23c6f1bbaf2c2800232e8448736738ef76c3602617b468dbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1534065a0444583bcb59c85081a3b04277c4a5e8a3b3b0e0e2f7d281f5f34a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac44f44bda775152aa0485ed163b19c2ae383b4a17687a21fa11a9fc281eb3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5682c788878c644e3e2e12e9276df8b0d113399f8b854ddc0c1ba0deef42b28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da89ac7a6365a58314cdfc5c895a154a5be01bdfd927b73333d63bd6b89fb9c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc5b1a30337b0bf041db8785e5a1fe2f22ee32a5ba3ed4a976d09fb39eb14dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51cfa0774ea2e8d633dea780f94ef8171c83935b74d7aef7e3b0fcc65f48584(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347d93ccbfe930edd368a9d2b9d2f0a9f10214d0cfd6c8f0ddc4d82b4de338b9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1fbbeb5c20eeb304bf0d2fed299ed1c3b36d8668464cb38446ce241a6b1045(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5315c22ede92438101bd060218c02b404298321677e3fbd0c2ae034be2cc4122(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ce81a4fde63d940dcdbb4a39f44b030f729b0b167bf65f1c71b5c70d9bb125(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abf4f2ab14745e1ebc76a9f78112cdff530cdd8bb71c2b33f262db43d2b1886(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9690c9f010047b08c131422b28d0bd37b2382a3d6dc15b8c0ec3aa830d3faf30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc047a5cfba7b1d1e22017447d5938ef98e98e8a0b9838718c21ec38c54f34b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19c9e12a23b64af1c0d162f12e3bbd0baa0c55420e3d0fec7d462163eeab8eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895ff994bd25258ba3dba9b86f34b7d9b1294b8fdccfb4ef11b7116f35a0da6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07c41ad76ff26c878946236693788143e9b0247b25e8d422d17c25e6bf5e8f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13ba8fcd2df93f14cf45461f497614cef290247eb46eae5262a4364dc658b76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75cfdc82ea76630a2cbfaaa87d3ac8c0c86c5ad97f11fc6d51044a9a4e269553(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614d68bd6e00e6699f7f8e74336ab52de5f30895b7d17b00b1030ae01adf8d95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2befef2c45745086e004ce9abe4ee7334d1d0e7029f15c55e4224588cc7ba624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262ca624d0ff6f67b9581aae4869effbfe797be938a5ca86e84703dab103aad1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf885cb21f203ad8474d50557815f8f7d50c2514961f6ae5ac29b9524e8a274f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f531ee73893ed55393625417b333f8f547af85232a14ba0dd3f1b9a5f0fd3a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f1eaa019b9cb12edaf0660d14de2b851a441c9d5e4ae68e56c9e7bf3248e36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7835a9906176217413b8c62bb2158aa8f0c76ab3454142906b9de379222d676(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5a23477b410dd1546d99cae23fa8c89f805b6430f49db8ced96311300f1d75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beded40bdbabc8274255c6d614df24cc7745f25fbafec6fa7a6cdae191f12006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6559a8548a4b16f9317bed8745b449684045c24da55bbae8aa781eb327fcc1c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef499c51a8d3f8c647c3b488bc38565e176b5b7d065a51ef7fac2283a54360a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60af137a5275335280295efa9296bd6788973d21eaedcef4204a641ed960e1c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249ac8f56cce2bc933974a8046c99ba4f12af205010e7899a32bb75a50670915(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda4fd29690af86a8b33f00e431240009b14fc9401a2e7ac116202659d63b6cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91292296945f9b0e589734e9c8be1abf03a2fd3b1f7ad2561526e40b94952abd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758e98c8f60cdc4259b7b6f1cc9ac2aac2540c6866c39ad6800c5de927be87ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff19d16fda4ff130b76db94a95d8ee1c4c8bbbda7ea04a4065b85892a5c693b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee1bfdc331b5f25567acb8488149b5b5b87b054e2b7327de5eb6fd77dcec318(
    *,
    name: builtins.str,
    filter_type: typing.Optional[builtins.str] = None,
    filter_value: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37612281c4d8f39f712f3556f41e274a51322d3e1f636fdb0950d4a351e007d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892405b1f745014de95d27a4074a59e7b0870867580d9dfa9106a92f03f3d94b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bcd9cfec9c9f3c498fe7e5f89ede8214abe5269a217094e7c2d1cfbda417695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fa474b6e5a0a325d77c176d28d82715d1547b6672a7997a1b1ad8b463dd540(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c05d22465a8466b38b1f28a5efae1179b1e1586f5d9b20449fe45407dbe7363(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49bbf78e3e2faaa0290c67a386e86e3c49f49b1aa0a92f580249775da9665f8d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSamlAttributeStatements]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836508cdc6ea09fd8bca1612db9a48bfab87279a22c0459de4132ac8e00ef3d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aee3a95ca9f322407f952d4c8df5b1da310f305407c067a72736e8c895a18c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2afdb15f2eccca4d3dfa1198a24d47d9c9fbc231ae308d99ede5718473e254f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8da6b7a5dff069424162b4117cba8ea90700253378d97f1e34ac6fbba89b2dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d94db9b957d8fa38848c538d77d15c68015503ac7b087285eccef8a29dfa51c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751c710d496926188ba6f7986002003b1410520f447788eb36e394e69799aaff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e444b43e5d071af99b7757d1eaacaa136782d59e145adb78f22e4b2d200030d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc306beed53e5acbc8dbf957503e311d6b069e1ce4db1e7cb942d23cb066b31(
    value: typing.Optional[typing.Union[AppSamlAttributeStatements, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57e17e576729b01b2e0754774196cc1d0054b4365a294aad8d08ded459a19d0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    label: builtins.str,
    accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    acs_endpoints: typing.Optional[typing.Sequence[builtins.str]] = None,
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    app_settings_json: typing.Optional[builtins.str] = None,
    assertion_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    attribute_statements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppSamlAttributeStatements, typing.Dict[builtins.str, typing.Any]]]]] = None,
    audience: typing.Optional[builtins.str] = None,
    authentication_policy: typing.Optional[builtins.str] = None,
    authn_context_class_ref: typing.Optional[builtins.str] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_relay_state: typing.Optional[builtins.str] = None,
    destination: typing.Optional[builtins.str] = None,
    digest_algorithm: typing.Optional[builtins.str] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    honor_force_authn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    idp_issuer: typing.Optional[builtins.str] = None,
    implicit_assignment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    inline_hook_id: typing.Optional[builtins.str] = None,
    key_name: typing.Optional[builtins.str] = None,
    key_years_valid: typing.Optional[jsii.Number] = None,
    logo: typing.Optional[builtins.str] = None,
    preconfigured_app: typing.Optional[builtins.str] = None,
    recipient: typing.Optional[builtins.str] = None,
    request_compressed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    response_signed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    saml_version: typing.Optional[builtins.str] = None,
    signature_algorithm: typing.Optional[builtins.str] = None,
    single_logout_certificate: typing.Optional[builtins.str] = None,
    single_logout_issuer: typing.Optional[builtins.str] = None,
    single_logout_url: typing.Optional[builtins.str] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sp_issuer: typing.Optional[builtins.str] = None,
    sso_url: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    subject_name_id_format: typing.Optional[builtins.str] = None,
    subject_name_id_template: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AppSamlTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_name_template: typing.Optional[builtins.str] = None,
    user_name_template_push_status: typing.Optional[builtins.str] = None,
    user_name_template_suffix: typing.Optional[builtins.str] = None,
    user_name_template_type: typing.Optional[builtins.str] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppSamlUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae5e19cb9e75b754fba105ce547829021349282e72e7002fc121de62aa1dfb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef75f3880028136516d0795b05097bdc79010eed86085026a6d98a5ab3b40533(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8612392dd0d083360828def2167274863c3ae69818d4aa0ac6d8ce3f913f9ee8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635c331cee52b1f9eb2cc7880bc72720abd44b4ef5563d99f2518cae40b134dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae6998cb9aeeec6f016608b7a81c793ee186e0d5a7be8a1b86791b167c4e190(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d45b7645794f57375988ce0826bff4d92b946855fac55f14405b64ac3165fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b781186d5e52118bb6133e41be7f7f56f2398f3b04727774a7c600225543d4(
    value: typing.Optional[AppSamlKeys],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0af0921536fc5288aa4fe76e1a6260630775282ef8a7e0648e92e6beaccdb6e(
    *,
    create: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6c5b716a68d3e85490f9bf793c07a80703b93c7e069871da0c4507539df686(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bf6fefb1a4984ea1a982ff5d230be7a78f673b103bcbedcd341be91d432c33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c3ee3865bf0626cda75af07607ebb59e5901a6cf85dc3fb9b76463a8931f03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63d5c6e7708dbeb92c8eb6b790b6dbdc4d38c7e1d25ebc7ea71ec33ed79c520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09008875994305e3d1c5338a9d1f05d3c94eb72d90fb54e4aed6da7344816647(
    value: typing.Optional[typing.Union[AppSamlTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b6ea05c13c3efda29fda2368e244da4c40811be73e4b43a93fed57ce9f25fd(
    *,
    id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e583c3605d4182fd9caec9e78b7b89d742c2de1eae0dc211b6f9ee945b1425c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39dce7f39735ce178c3d489e3b9b650765bc84f32a1d70ff23e83fa8f675d237(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957a1f390276da3ade4fa8a54aa10b1f34e51fee654d1ea0d39483b067f7c99f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecef7cf6c2917bc9c17823a136675f9ab187ea24e7ca3b778fbebd032d67ca1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61eef1ac8b0f0bc145eddf05f8193003ef3ed9a5fe9beaa2971b25edbe5f288f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5fc14c6bbc2a0489a4b05321ef6d5dcc13a8feb7fa603b8f756d32b8ec8db83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSamlUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48ef58e41878a1258df9328dcbf4c2cc96ad469b6f97daa4fcfd9f17f16fff0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9daf0ab795fe2dbc172f9e6af4ee3f7d742c45ed4d300b47ca1520d8528cac2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f2c500355ebf630b60b6075f184cb43b3059f36c0e4457fa62ecc386ff7bf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8628144069bddcddb2369081ca770f5555d13329dda173db99dcdb7d247ccd72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e229d98a08475db9c1279e37234fa77239010e89ea7e691705f6ade1758a555b(
    value: typing.Optional[typing.Union[AppSamlUsers, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
