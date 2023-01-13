'''
# `okta_auto_login_app`

Refer to the Terraform Registory for docs: [`okta_auto_login_app`](https://www.terraform.io/docs/providers/okta/r/auto_login_app).
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


class AutoLoginApp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.autoLoginApp.AutoLoginApp",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app okta_auto_login_app}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        label: builtins.str,
        accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        app_settings_json: typing.Optional[builtins.str] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        credentials_scheme: typing.Optional[builtins.str] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        preconfigured_app: typing.Optional[builtins.str] = None,
        reveal_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_password: typing.Optional[builtins.str] = None,
        shared_username: typing.Optional[builtins.str] = None,
        sign_on_redirect_url: typing.Optional[builtins.str] = None,
        sign_on_url: typing.Optional[builtins.str] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AutoLoginAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_name_template: typing.Optional[builtins.str] = None,
        user_name_template_push_status: typing.Optional[builtins.str] = None,
        user_name_template_suffix: typing.Optional[builtins.str] = None,
        user_name_template_type: typing.Optional[builtins.str] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AutoLoginAppUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app okta_auto_login_app} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#label AutoLoginApp#label}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#accessibility_error_redirect_url AutoLoginApp#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#accessibility_login_redirect_url AutoLoginApp#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#accessibility_self_service AutoLoginApp#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#admin_note AutoLoginApp#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#app_links_json AutoLoginApp#app_links_json}
        :param app_settings_json: Application settings in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#app_settings_json AutoLoginApp#app_settings_json}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#auto_submit_toolbar AutoLoginApp#auto_submit_toolbar}
        :param credentials_scheme: Application credentials scheme. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#credentials_scheme AutoLoginApp#credentials_scheme}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#enduser_note AutoLoginApp#enduser_note}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#groups AutoLoginApp#groups}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#hide_ios AutoLoginApp#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#hide_web AutoLoginApp#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#id AutoLoginApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#logo AutoLoginApp#logo}
        :param preconfigured_app: Preconfigured app name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#preconfigured_app AutoLoginApp#preconfigured_app}
        :param reveal_password: Allow user to reveal password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#reveal_password AutoLoginApp#reveal_password}
        :param shared_password: Shared password, required for certain schemes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#shared_password AutoLoginApp#shared_password}
        :param shared_username: Shared username, required for certain schemes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#shared_username AutoLoginApp#shared_username}
        :param sign_on_redirect_url: Post login redirect URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#sign_on_redirect_url AutoLoginApp#sign_on_redirect_url}
        :param sign_on_url: Login URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#sign_on_url AutoLoginApp#sign_on_url}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#skip_groups AutoLoginApp#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#skip_users AutoLoginApp#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#status AutoLoginApp#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#timeouts AutoLoginApp#timeouts}
        :param user_name_template: Username template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template AutoLoginApp#user_name_template}
        :param user_name_template_push_status: Push username on update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template_push_status AutoLoginApp#user_name_template_push_status}
        :param user_name_template_suffix: Username template suffix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template_suffix AutoLoginApp#user_name_template_suffix}
        :param user_name_template_type: Username template type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template_type AutoLoginApp#user_name_template_type}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#users AutoLoginApp#users}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac074dc9e0296a4adccb88d16413b01c0f1ea095dfb3182d78bb516b9c8ab19e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AutoLoginAppConfig(
            label=label,
            accessibility_error_redirect_url=accessibility_error_redirect_url,
            accessibility_login_redirect_url=accessibility_login_redirect_url,
            accessibility_self_service=accessibility_self_service,
            admin_note=admin_note,
            app_links_json=app_links_json,
            app_settings_json=app_settings_json,
            auto_submit_toolbar=auto_submit_toolbar,
            credentials_scheme=credentials_scheme,
            enduser_note=enduser_note,
            groups=groups,
            hide_ios=hide_ios,
            hide_web=hide_web,
            id=id,
            logo=logo,
            preconfigured_app=preconfigured_app,
            reveal_password=reveal_password,
            shared_password=shared_password,
            shared_username=shared_username,
            sign_on_redirect_url=sign_on_redirect_url,
            sign_on_url=sign_on_url,
            skip_groups=skip_groups,
            skip_users=skip_users,
            status=status,
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

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#create AutoLoginApp#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#read AutoLoginApp#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#update AutoLoginApp#update}.
        '''
        value = AutoLoginAppTimeouts(create=create, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUsers")
    def put_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AutoLoginAppUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe410fb234ed84ffe6156fa4fb87627fdf1f5e0821906e730e6e77339c1e29e)
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

    @jsii.member(jsii_name="resetAutoSubmitToolbar")
    def reset_auto_submit_toolbar(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoSubmitToolbar", []))

    @jsii.member(jsii_name="resetCredentialsScheme")
    def reset_credentials_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialsScheme", []))

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

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogo")
    def reset_logo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogo", []))

    @jsii.member(jsii_name="resetPreconfiguredApp")
    def reset_preconfigured_app(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreconfiguredApp", []))

    @jsii.member(jsii_name="resetRevealPassword")
    def reset_reveal_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevealPassword", []))

    @jsii.member(jsii_name="resetSharedPassword")
    def reset_shared_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedPassword", []))

    @jsii.member(jsii_name="resetSharedUsername")
    def reset_shared_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedUsername", []))

    @jsii.member(jsii_name="resetSignOnRedirectUrl")
    def reset_sign_on_redirect_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignOnRedirectUrl", []))

    @jsii.member(jsii_name="resetSignOnUrl")
    def reset_sign_on_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignOnUrl", []))

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
    def timeouts(self) -> "AutoLoginAppTimeoutsOutputReference":
        return typing.cast("AutoLoginAppTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> "AutoLoginAppUsersList":
        return typing.cast("AutoLoginAppUsersList", jsii.get(self, "users"))

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
    @jsii.member(jsii_name="autoSubmitToolbarInput")
    def auto_submit_toolbar_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoSubmitToolbarInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsSchemeInput")
    def credentials_scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsSchemeInput"))

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
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="revealPasswordInput")
    def reveal_password_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "revealPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedPasswordInput")
    def shared_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedUsernameInput")
    def shared_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="signOnRedirectUrlInput")
    def sign_on_redirect_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signOnRedirectUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="signOnUrlInput")
    def sign_on_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signOnUrlInput"))

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
    ) -> typing.Optional[typing.Union["AutoLoginAppTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["AutoLoginAppTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutoLoginAppUsers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutoLoginAppUsers"]]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="accessibilityErrorRedirectUrl")
    def accessibility_error_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityErrorRedirectUrl"))

    @accessibility_error_redirect_url.setter
    def accessibility_error_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b98668a1fb86d4909585ffbfbe5c8b8d6381392cd3402951972d4265310147d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilityErrorRedirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="accessibilityLoginRedirectUrl")
    def accessibility_login_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityLoginRedirectUrl"))

    @accessibility_login_redirect_url.setter
    def accessibility_login_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37cbef9e24de2c1cdc92b087c372d6899792064e2be6dfc948a249973c504194)
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
            type_hints = typing.get_type_hints(_typecheckingstub__859a7f3885da26d2247ab2c02b02ec12b4cbaf169c0fd7f9fa158d58e1b83abe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilitySelfService", value)

    @builtins.property
    @jsii.member(jsii_name="adminNote")
    def admin_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminNote"))

    @admin_note.setter
    def admin_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f23198c15d5dad9801463f7adb2b8d0ef92346e84e065c80651920b86229e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminNote", value)

    @builtins.property
    @jsii.member(jsii_name="appLinksJson")
    def app_links_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLinksJson"))

    @app_links_json.setter
    def app_links_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce07e6287fcde33c7cc96986a013b21677c1c54258478d9c958d00e8c007a737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLinksJson", value)

    @builtins.property
    @jsii.member(jsii_name="appSettingsJson")
    def app_settings_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSettingsJson"))

    @app_settings_json.setter
    def app_settings_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f97ebf6b80922809305b3ede957e77bbb7d8e2a1ac7f91bf42a78160cd266b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSettingsJson", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__07ce1d496272781a6cb6f39a9816762db5487aab2b9de0aaedd3c8ed87790ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubmitToolbar", value)

    @builtins.property
    @jsii.member(jsii_name="credentialsScheme")
    def credentials_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialsScheme"))

    @credentials_scheme.setter
    def credentials_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a6900e27b85df041a3f6e9df4ad0b6ce98522e5d7665cf217d6e15c8617a54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialsScheme", value)

    @builtins.property
    @jsii.member(jsii_name="enduserNote")
    def enduser_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enduserNote"))

    @enduser_note.setter
    def enduser_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bf6471dbe212368a8722134e60ded0256bd5c6f0c886edded72a7104a16a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enduserNote", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd968a0ba892adead821222f7b5823aee199a4c680a9e279190d4c27bfdb692)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93081ea82b3f2b95362dbd7d06cbf4618478e95d898c8ebe3f7c7262c2e10f3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c00a857f6e31df4118d54695773c89c35196613f739a02ebbc26220042951dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hideWeb", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4975b7bb261fca7f5a97c8f7650028d1e2d5a39885673eb492784be13c2178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6757e9e87fc99c01b2b2cd5e756682bb16c12299ea5b1e886aa6ac7a2df48553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="logo")
    def logo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logo"))

    @logo.setter
    def logo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a6a6e90370c80f3532708bc08ab8b26742e61184ada431116ac31e31432f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logo", value)

    @builtins.property
    @jsii.member(jsii_name="preconfiguredApp")
    def preconfigured_app(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preconfiguredApp"))

    @preconfigured_app.setter
    def preconfigured_app(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b9c96414d6e05b4be7877f8e912f4e1978953e4fe4e35a4b6002960b8dfc88b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preconfiguredApp", value)

    @builtins.property
    @jsii.member(jsii_name="revealPassword")
    def reveal_password(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "revealPassword"))

    @reveal_password.setter
    def reveal_password(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86668ab9f4bdae4adcf11e373c72f6ccebed472420847e5200269120f84ce59b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revealPassword", value)

    @builtins.property
    @jsii.member(jsii_name="sharedPassword")
    def shared_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedPassword"))

    @shared_password.setter
    def shared_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9265ade8b70089f12c0577a9c1fe01ee5bb8e3f70414e3190c760030bbf427d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedPassword", value)

    @builtins.property
    @jsii.member(jsii_name="sharedUsername")
    def shared_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedUsername"))

    @shared_username.setter
    def shared_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12570b4f948cc5b2f2654ec931a67d934792ab8bd68798ada0399412802fb9eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedUsername", value)

    @builtins.property
    @jsii.member(jsii_name="signOnRedirectUrl")
    def sign_on_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signOnRedirectUrl"))

    @sign_on_redirect_url.setter
    def sign_on_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee60b168a7db9124fa08d5dcfdd18ecb379b09f14fa9e2dfd470847ede630ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signOnRedirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="signOnUrl")
    def sign_on_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signOnUrl"))

    @sign_on_url.setter
    def sign_on_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7472fcc76ea6ff5a44e6c1d900bd09bfc5f9799af11f1cdbbf55b328350822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signOnUrl", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__37d55c2342354a662aa6bb4cbad8d6d096e3bc9174ae43fa80480dcb0eb31f01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d6fb75a044e408ca74f99d0b949d08ab0c95bcf33932ec5e83edc28367effdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipUsers", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aacd8ebeece22cd313faf183d93ac96fd7d98975488238b4d72311ac31c516b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplate")
    def user_name_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplate"))

    @user_name_template.setter
    def user_name_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9b67300c5dc9a4ce0606ae63694844d75e66e271f67376bd8be1801a45a3c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplatePushStatus")
    def user_name_template_push_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplatePushStatus"))

    @user_name_template_push_status.setter
    def user_name_template_push_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add0b789eb48585585885beb24ceac2c2b1f2d7c7ce552da35bac7e1c2ec0f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplatePushStatus", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateSuffix")
    def user_name_template_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplateSuffix"))

    @user_name_template_suffix.setter
    def user_name_template_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff60769730c68a62e83d365cd6ab0f980a9743c377d5629111df2f165a1f844b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplateSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateType")
    def user_name_template_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplateType"))

    @user_name_template_type.setter
    def user_name_template_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5760e7bcf914cec439425ce804cdc193f1683e5d89a03b68e02df0db6ee2903)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplateType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.autoLoginApp.AutoLoginAppConfig",
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
        "admin_note": "adminNote",
        "app_links_json": "appLinksJson",
        "app_settings_json": "appSettingsJson",
        "auto_submit_toolbar": "autoSubmitToolbar",
        "credentials_scheme": "credentialsScheme",
        "enduser_note": "enduserNote",
        "groups": "groups",
        "hide_ios": "hideIos",
        "hide_web": "hideWeb",
        "id": "id",
        "logo": "logo",
        "preconfigured_app": "preconfiguredApp",
        "reveal_password": "revealPassword",
        "shared_password": "sharedPassword",
        "shared_username": "sharedUsername",
        "sign_on_redirect_url": "signOnRedirectUrl",
        "sign_on_url": "signOnUrl",
        "skip_groups": "skipGroups",
        "skip_users": "skipUsers",
        "status": "status",
        "timeouts": "timeouts",
        "user_name_template": "userNameTemplate",
        "user_name_template_push_status": "userNameTemplatePushStatus",
        "user_name_template_suffix": "userNameTemplateSuffix",
        "user_name_template_type": "userNameTemplateType",
        "users": "users",
    },
)
class AutoLoginAppConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        app_settings_json: typing.Optional[builtins.str] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        credentials_scheme: typing.Optional[builtins.str] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        preconfigured_app: typing.Optional[builtins.str] = None,
        reveal_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_password: typing.Optional[builtins.str] = None,
        shared_username: typing.Optional[builtins.str] = None,
        sign_on_redirect_url: typing.Optional[builtins.str] = None,
        sign_on_url: typing.Optional[builtins.str] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AutoLoginAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_name_template: typing.Optional[builtins.str] = None,
        user_name_template_push_status: typing.Optional[builtins.str] = None,
        user_name_template_suffix: typing.Optional[builtins.str] = None,
        user_name_template_type: typing.Optional[builtins.str] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AutoLoginAppUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#label AutoLoginApp#label}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#accessibility_error_redirect_url AutoLoginApp#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#accessibility_login_redirect_url AutoLoginApp#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#accessibility_self_service AutoLoginApp#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#admin_note AutoLoginApp#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#app_links_json AutoLoginApp#app_links_json}
        :param app_settings_json: Application settings in JSON format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#app_settings_json AutoLoginApp#app_settings_json}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#auto_submit_toolbar AutoLoginApp#auto_submit_toolbar}
        :param credentials_scheme: Application credentials scheme. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#credentials_scheme AutoLoginApp#credentials_scheme}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#enduser_note AutoLoginApp#enduser_note}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#groups AutoLoginApp#groups}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#hide_ios AutoLoginApp#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#hide_web AutoLoginApp#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#id AutoLoginApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#logo AutoLoginApp#logo}
        :param preconfigured_app: Preconfigured app name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#preconfigured_app AutoLoginApp#preconfigured_app}
        :param reveal_password: Allow user to reveal password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#reveal_password AutoLoginApp#reveal_password}
        :param shared_password: Shared password, required for certain schemes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#shared_password AutoLoginApp#shared_password}
        :param shared_username: Shared username, required for certain schemes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#shared_username AutoLoginApp#shared_username}
        :param sign_on_redirect_url: Post login redirect URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#sign_on_redirect_url AutoLoginApp#sign_on_redirect_url}
        :param sign_on_url: Login URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#sign_on_url AutoLoginApp#sign_on_url}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#skip_groups AutoLoginApp#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#skip_users AutoLoginApp#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#status AutoLoginApp#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#timeouts AutoLoginApp#timeouts}
        :param user_name_template: Username template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template AutoLoginApp#user_name_template}
        :param user_name_template_push_status: Push username on update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template_push_status AutoLoginApp#user_name_template_push_status}
        :param user_name_template_suffix: Username template suffix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template_suffix AutoLoginApp#user_name_template_suffix}
        :param user_name_template_type: Username template type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template_type AutoLoginApp#user_name_template_type}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#users AutoLoginApp#users}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = AutoLoginAppTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa00c7a53504b97c23df4f4afdb806c933c8160422bf9950371f45a1afeadce)
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
            check_type(argname="argument admin_note", value=admin_note, expected_type=type_hints["admin_note"])
            check_type(argname="argument app_links_json", value=app_links_json, expected_type=type_hints["app_links_json"])
            check_type(argname="argument app_settings_json", value=app_settings_json, expected_type=type_hints["app_settings_json"])
            check_type(argname="argument auto_submit_toolbar", value=auto_submit_toolbar, expected_type=type_hints["auto_submit_toolbar"])
            check_type(argname="argument credentials_scheme", value=credentials_scheme, expected_type=type_hints["credentials_scheme"])
            check_type(argname="argument enduser_note", value=enduser_note, expected_type=type_hints["enduser_note"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument hide_ios", value=hide_ios, expected_type=type_hints["hide_ios"])
            check_type(argname="argument hide_web", value=hide_web, expected_type=type_hints["hide_web"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logo", value=logo, expected_type=type_hints["logo"])
            check_type(argname="argument preconfigured_app", value=preconfigured_app, expected_type=type_hints["preconfigured_app"])
            check_type(argname="argument reveal_password", value=reveal_password, expected_type=type_hints["reveal_password"])
            check_type(argname="argument shared_password", value=shared_password, expected_type=type_hints["shared_password"])
            check_type(argname="argument shared_username", value=shared_username, expected_type=type_hints["shared_username"])
            check_type(argname="argument sign_on_redirect_url", value=sign_on_redirect_url, expected_type=type_hints["sign_on_redirect_url"])
            check_type(argname="argument sign_on_url", value=sign_on_url, expected_type=type_hints["sign_on_url"])
            check_type(argname="argument skip_groups", value=skip_groups, expected_type=type_hints["skip_groups"])
            check_type(argname="argument skip_users", value=skip_users, expected_type=type_hints["skip_users"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
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
        if admin_note is not None:
            self._values["admin_note"] = admin_note
        if app_links_json is not None:
            self._values["app_links_json"] = app_links_json
        if app_settings_json is not None:
            self._values["app_settings_json"] = app_settings_json
        if auto_submit_toolbar is not None:
            self._values["auto_submit_toolbar"] = auto_submit_toolbar
        if credentials_scheme is not None:
            self._values["credentials_scheme"] = credentials_scheme
        if enduser_note is not None:
            self._values["enduser_note"] = enduser_note
        if groups is not None:
            self._values["groups"] = groups
        if hide_ios is not None:
            self._values["hide_ios"] = hide_ios
        if hide_web is not None:
            self._values["hide_web"] = hide_web
        if id is not None:
            self._values["id"] = id
        if logo is not None:
            self._values["logo"] = logo
        if preconfigured_app is not None:
            self._values["preconfigured_app"] = preconfigured_app
        if reveal_password is not None:
            self._values["reveal_password"] = reveal_password
        if shared_password is not None:
            self._values["shared_password"] = shared_password
        if shared_username is not None:
            self._values["shared_username"] = shared_username
        if sign_on_redirect_url is not None:
            self._values["sign_on_redirect_url"] = sign_on_redirect_url
        if sign_on_url is not None:
            self._values["sign_on_url"] = sign_on_url
        if skip_groups is not None:
            self._values["skip_groups"] = skip_groups
        if skip_users is not None:
            self._values["skip_users"] = skip_users
        if status is not None:
            self._values["status"] = status
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#label AutoLoginApp#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accessibility_error_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom error page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#accessibility_error_redirect_url AutoLoginApp#accessibility_error_redirect_url}
        '''
        result = self._values.get("accessibility_error_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_login_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom login page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#accessibility_login_redirect_url AutoLoginApp#accessibility_login_redirect_url}
        '''
        result = self._values.get("accessibility_login_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_self_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable self service.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#accessibility_self_service AutoLoginApp#accessibility_self_service}
        '''
        result = self._values.get("accessibility_self_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def admin_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for admins.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#admin_note AutoLoginApp#admin_note}
        '''
        result = self._values.get("admin_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_links_json(self) -> typing.Optional[builtins.str]:
        '''Displays specific appLinks for the app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#app_links_json AutoLoginApp#app_links_json}
        '''
        result = self._values.get("app_links_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_settings_json(self) -> typing.Optional[builtins.str]:
        '''Application settings in JSON format.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#app_settings_json AutoLoginApp#app_settings_json}
        '''
        result = self._values.get("app_settings_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_submit_toolbar(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Display auto submit toolbar.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#auto_submit_toolbar AutoLoginApp#auto_submit_toolbar}
        '''
        result = self._values.get("auto_submit_toolbar")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def credentials_scheme(self) -> typing.Optional[builtins.str]:
        '''Application credentials scheme.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#credentials_scheme AutoLoginApp#credentials_scheme}
        '''
        result = self._values.get("credentials_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enduser_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for end users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#enduser_note AutoLoginApp#enduser_note}
        '''
        result = self._values.get("enduser_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Groups associated with the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#groups AutoLoginApp#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def hide_ios(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon on mobile app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#hide_ios AutoLoginApp#hide_ios}
        '''
        result = self._values.get("hide_ios")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hide_web(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon to users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#hide_web AutoLoginApp#hide_web}
        '''
        result = self._values.get("hide_web")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#id AutoLoginApp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo(self) -> typing.Optional[builtins.str]:
        '''Local path to logo of the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#logo AutoLoginApp#logo}
        '''
        result = self._values.get("logo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preconfigured_app(self) -> typing.Optional[builtins.str]:
        '''Preconfigured app name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#preconfigured_app AutoLoginApp#preconfigured_app}
        '''
        result = self._values.get("preconfigured_app")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reveal_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow user to reveal password.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#reveal_password AutoLoginApp#reveal_password}
        '''
        result = self._values.get("reveal_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def shared_password(self) -> typing.Optional[builtins.str]:
        '''Shared password, required for certain schemes.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#shared_password AutoLoginApp#shared_password}
        '''
        result = self._values.get("shared_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_username(self) -> typing.Optional[builtins.str]:
        '''Shared username, required for certain schemes.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#shared_username AutoLoginApp#shared_username}
        '''
        result = self._values.get("shared_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sign_on_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Post login redirect URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#sign_on_redirect_url AutoLoginApp#sign_on_redirect_url}
        '''
        result = self._values.get("sign_on_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sign_on_url(self) -> typing.Optional[builtins.str]:
        '''Login URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#sign_on_url AutoLoginApp#sign_on_url}
        '''
        result = self._values.get("sign_on_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#skip_groups AutoLoginApp#skip_groups}
        '''
        result = self._values.get("skip_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_users(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#skip_users AutoLoginApp#skip_users}
        '''
        result = self._values.get("skip_users")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#status AutoLoginApp#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AutoLoginAppTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#timeouts AutoLoginApp#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AutoLoginAppTimeouts"], result)

    @builtins.property
    def user_name_template(self) -> typing.Optional[builtins.str]:
        '''Username template.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template AutoLoginApp#user_name_template}
        '''
        result = self._values.get("user_name_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_push_status(self) -> typing.Optional[builtins.str]:
        '''Push username on update.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template_push_status AutoLoginApp#user_name_template_push_status}
        '''
        result = self._values.get("user_name_template_push_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_suffix(self) -> typing.Optional[builtins.str]:
        '''Username template suffix.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template_suffix AutoLoginApp#user_name_template_suffix}
        '''
        result = self._values.get("user_name_template_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_type(self) -> typing.Optional[builtins.str]:
        '''Username template type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#user_name_template_type AutoLoginApp#user_name_template_type}
        '''
        result = self._values.get("user_name_template_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutoLoginAppUsers"]]]:
        '''users block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#users AutoLoginApp#users}
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AutoLoginAppUsers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoLoginAppConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.autoLoginApp.AutoLoginAppTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "read": "read", "update": "update"},
)
class AutoLoginAppTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#create AutoLoginApp#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#read AutoLoginApp#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#update AutoLoginApp#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0de11f025816880329fd29a2e1b5beafb36089e293fd557396f7a1fa0d91bff)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#create AutoLoginApp#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#read AutoLoginApp#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#update AutoLoginApp#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoLoginAppTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutoLoginAppTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.autoLoginApp.AutoLoginAppTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f13e6ff7ee9559877e7673e477f3478ce29766f7d2441e16b9dfee8baa8e3129)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f9d6c74e2cb3934b95e88447d94ec0da0b3d1b66cfced72a05646a013cb3fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f5d1f9b2659d4b23522c679ddbca48b942a192c52bd1544921dceb35ab37f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d228ee1b424e929593a851e0ce593950a305092910d31d0cc076a2624f172483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AutoLoginAppTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AutoLoginAppTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AutoLoginAppTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0b91026a77d7eb5c0c03e973c6a3cb2e3f3d4dc60f74eadf78ebf20536a080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.autoLoginApp.AutoLoginAppUsers",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "password": "password", "username": "username"},
)
class AutoLoginAppUsers:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: User ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#id AutoLoginApp#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password: Password for user application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#password AutoLoginApp#password}
        :param username: Username for user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#username AutoLoginApp#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66872691dddcfe02e2e19fe4b1a080bf1a43bd11f218ef6fc7609f980ca716d5)
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#id AutoLoginApp#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for user application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#password AutoLoginApp#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auto_login_app#username AutoLoginApp#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoLoginAppUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutoLoginAppUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.autoLoginApp.AutoLoginAppUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__596baa89b7b0920633dcc5d293a6c959aa88bd3c1ddd8466acc7f0da35aa0e97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AutoLoginAppUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58e188df86687febd89227185032302bb625281e8edd9d34f28065db6dc2494)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AutoLoginAppUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc5bce23e13cf15b12cc40da771f0e249e7dc881f58e79d19ebedf58402c58e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a76d4af605d33ceb2c12afbbed67396ba206ea8e98d345e50b05ce3b52a547be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59abe8723503e9e653338a611de5532d1fd32d6ae2a1b14274e006bbed3e35f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutoLoginAppUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutoLoginAppUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutoLoginAppUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7f088f962132a627ed617c48370f79f93b44e48940af046355b592b90534d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AutoLoginAppUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.autoLoginApp.AutoLoginAppUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e4fdf8651209002359e2b19063a0185c1ad03d1a2d1f4b9e8ff38c9a11d1fad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eed551e971e159311b11ecfa499e8e352b83b588680886e2931a22f115f24364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a879f9279e1fe90fff9803cf83e7c75e217418ab30d71df033e9310779b4999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff956bb18db78acc6cdf32a85d48afa555fa4862898c9b2e8d3fda1e139b76f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AutoLoginAppUsers, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AutoLoginAppUsers, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AutoLoginAppUsers, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96986318086d386bad4bd865d219b3dd70701e97d373992ebe692d4b733f4c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AutoLoginApp",
    "AutoLoginAppConfig",
    "AutoLoginAppTimeouts",
    "AutoLoginAppTimeoutsOutputReference",
    "AutoLoginAppUsers",
    "AutoLoginAppUsersList",
    "AutoLoginAppUsersOutputReference",
]

publication.publish()

def _typecheckingstub__ac074dc9e0296a4adccb88d16413b01c0f1ea095dfb3182d78bb516b9c8ab19e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    label: builtins.str,
    accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    app_settings_json: typing.Optional[builtins.str] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    credentials_scheme: typing.Optional[builtins.str] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    preconfigured_app: typing.Optional[builtins.str] = None,
    reveal_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    shared_password: typing.Optional[builtins.str] = None,
    shared_username: typing.Optional[builtins.str] = None,
    sign_on_redirect_url: typing.Optional[builtins.str] = None,
    sign_on_url: typing.Optional[builtins.str] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AutoLoginAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_name_template: typing.Optional[builtins.str] = None,
    user_name_template_push_status: typing.Optional[builtins.str] = None,
    user_name_template_suffix: typing.Optional[builtins.str] = None,
    user_name_template_type: typing.Optional[builtins.str] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AutoLoginAppUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__abe410fb234ed84ffe6156fa4fb87627fdf1f5e0821906e730e6e77339c1e29e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AutoLoginAppUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b98668a1fb86d4909585ffbfbe5c8b8d6381392cd3402951972d4265310147d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37cbef9e24de2c1cdc92b087c372d6899792064e2be6dfc948a249973c504194(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859a7f3885da26d2247ab2c02b02ec12b4cbaf169c0fd7f9fa158d58e1b83abe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f23198c15d5dad9801463f7adb2b8d0ef92346e84e065c80651920b86229e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce07e6287fcde33c7cc96986a013b21677c1c54258478d9c958d00e8c007a737(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f97ebf6b80922809305b3ede957e77bbb7d8e2a1ac7f91bf42a78160cd266b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ce1d496272781a6cb6f39a9816762db5487aab2b9de0aaedd3c8ed87790ff0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a6900e27b85df041a3f6e9df4ad0b6ce98522e5d7665cf217d6e15c8617a54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bf6471dbe212368a8722134e60ded0256bd5c6f0c886edded72a7104a16a74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd968a0ba892adead821222f7b5823aee199a4c680a9e279190d4c27bfdb692(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93081ea82b3f2b95362dbd7d06cbf4618478e95d898c8ebe3f7c7262c2e10f3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00a857f6e31df4118d54695773c89c35196613f739a02ebbc26220042951dc2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4975b7bb261fca7f5a97c8f7650028d1e2d5a39885673eb492784be13c2178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6757e9e87fc99c01b2b2cd5e756682bb16c12299ea5b1e886aa6ac7a2df48553(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a6a6e90370c80f3532708bc08ab8b26742e61184ada431116ac31e31432f0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9c96414d6e05b4be7877f8e912f4e1978953e4fe4e35a4b6002960b8dfc88b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86668ab9f4bdae4adcf11e373c72f6ccebed472420847e5200269120f84ce59b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9265ade8b70089f12c0577a9c1fe01ee5bb8e3f70414e3190c760030bbf427d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12570b4f948cc5b2f2654ec931a67d934792ab8bd68798ada0399412802fb9eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee60b168a7db9124fa08d5dcfdd18ecb379b09f14fa9e2dfd470847ede630ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7472fcc76ea6ff5a44e6c1d900bd09bfc5f9799af11f1cdbbf55b328350822(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d55c2342354a662aa6bb4cbad8d6d096e3bc9174ae43fa80480dcb0eb31f01(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6fb75a044e408ca74f99d0b949d08ab0c95bcf33932ec5e83edc28367effdb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aacd8ebeece22cd313faf183d93ac96fd7d98975488238b4d72311ac31c516b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9b67300c5dc9a4ce0606ae63694844d75e66e271f67376bd8be1801a45a3c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add0b789eb48585585885beb24ceac2c2b1f2d7c7ce552da35bac7e1c2ec0f6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff60769730c68a62e83d365cd6ab0f980a9743c377d5629111df2f165a1f844b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5760e7bcf914cec439425ce804cdc193f1683e5d89a03b68e02df0db6ee2903(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa00c7a53504b97c23df4f4afdb806c933c8160422bf9950371f45a1afeadce(
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
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    app_settings_json: typing.Optional[builtins.str] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    credentials_scheme: typing.Optional[builtins.str] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    preconfigured_app: typing.Optional[builtins.str] = None,
    reveal_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    shared_password: typing.Optional[builtins.str] = None,
    shared_username: typing.Optional[builtins.str] = None,
    sign_on_redirect_url: typing.Optional[builtins.str] = None,
    sign_on_url: typing.Optional[builtins.str] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AutoLoginAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_name_template: typing.Optional[builtins.str] = None,
    user_name_template_push_status: typing.Optional[builtins.str] = None,
    user_name_template_suffix: typing.Optional[builtins.str] = None,
    user_name_template_type: typing.Optional[builtins.str] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AutoLoginAppUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0de11f025816880329fd29a2e1b5beafb36089e293fd557396f7a1fa0d91bff(
    *,
    create: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13e6ff7ee9559877e7673e477f3478ce29766f7d2441e16b9dfee8baa8e3129(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9d6c74e2cb3934b95e88447d94ec0da0b3d1b66cfced72a05646a013cb3fc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5d1f9b2659d4b23522c679ddbca48b942a192c52bd1544921dceb35ab37f01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d228ee1b424e929593a851e0ce593950a305092910d31d0cc076a2624f172483(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0b91026a77d7eb5c0c03e973c6a3cb2e3f3d4dc60f74eadf78ebf20536a080(
    value: typing.Optional[typing.Union[AutoLoginAppTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66872691dddcfe02e2e19fe4b1a080bf1a43bd11f218ef6fc7609f980ca716d5(
    *,
    id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596baa89b7b0920633dcc5d293a6c959aa88bd3c1ddd8466acc7f0da35aa0e97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58e188df86687febd89227185032302bb625281e8edd9d34f28065db6dc2494(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5bce23e13cf15b12cc40da771f0e249e7dc881f58e79d19ebedf58402c58e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76d4af605d33ceb2c12afbbed67396ba206ea8e98d345e50b05ce3b52a547be(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59abe8723503e9e653338a611de5532d1fd32d6ae2a1b14274e006bbed3e35f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7f088f962132a627ed617c48370f79f93b44e48940af046355b592b90534d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AutoLoginAppUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4fdf8651209002359e2b19063a0185c1ad03d1a2d1f4b9e8ff38c9a11d1fad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed551e971e159311b11ecfa499e8e352b83b588680886e2931a22f115f24364(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a879f9279e1fe90fff9803cf83e7c75e217418ab30d71df033e9310779b4999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff956bb18db78acc6cdf32a85d48afa555fa4862898c9b2e8d3fda1e139b76f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96986318086d386bad4bd865d219b3dd70701e97d373992ebe692d4b733f4c5(
    value: typing.Optional[typing.Union[AutoLoginAppUsers, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
