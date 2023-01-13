'''
# `okta_three_field_app`

Refer to the Terraform Registory for docs: [`okta_three_field_app`](https://www.terraform.io/docs/providers/okta/r/three_field_app).
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


class ThreeFieldApp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.threeFieldApp.ThreeFieldApp",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/three_field_app okta_three_field_app}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        button_selector: builtins.str,
        extra_field_selector: builtins.str,
        extra_field_value: builtins.str,
        label: builtins.str,
        password_selector: builtins.str,
        url: builtins.str,
        username_selector: builtins.str,
        accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        credentials_scheme: typing.Optional[builtins.str] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        reveal_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_password: typing.Optional[builtins.str] = None,
        shared_username: typing.Optional[builtins.str] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ThreeFieldAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        url_regex: typing.Optional[builtins.str] = None,
        user_name_template: typing.Optional[builtins.str] = None,
        user_name_template_push_status: typing.Optional[builtins.str] = None,
        user_name_template_suffix: typing.Optional[builtins.str] = None,
        user_name_template_type: typing.Optional[builtins.str] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ThreeFieldAppUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/three_field_app okta_three_field_app} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param button_selector: Login button field CSS selector. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#button_selector ThreeFieldApp#button_selector}
        :param extra_field_selector: Extra field CSS selector. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#extra_field_selector ThreeFieldApp#extra_field_selector}
        :param extra_field_value: Value for extra form field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#extra_field_value ThreeFieldApp#extra_field_value}
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#label ThreeFieldApp#label}
        :param password_selector: Login password field CSS selector. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#password_selector ThreeFieldApp#password_selector}
        :param url: Login URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#url ThreeFieldApp#url}
        :param username_selector: Login username field CSS selector. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#username_selector ThreeFieldApp#username_selector}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#accessibility_error_redirect_url ThreeFieldApp#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#accessibility_login_redirect_url ThreeFieldApp#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#accessibility_self_service ThreeFieldApp#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#admin_note ThreeFieldApp#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#app_links_json ThreeFieldApp#app_links_json}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#auto_submit_toolbar ThreeFieldApp#auto_submit_toolbar}
        :param credentials_scheme: Application credentials scheme. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#credentials_scheme ThreeFieldApp#credentials_scheme}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#enduser_note ThreeFieldApp#enduser_note}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#groups ThreeFieldApp#groups}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#hide_ios ThreeFieldApp#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#hide_web ThreeFieldApp#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#id ThreeFieldApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#logo ThreeFieldApp#logo}
        :param reveal_password: Allow user to reveal password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#reveal_password ThreeFieldApp#reveal_password}
        :param shared_password: Shared password, required for certain schemes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#shared_password ThreeFieldApp#shared_password}
        :param shared_username: Shared username, required for certain schemes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#shared_username ThreeFieldApp#shared_username}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#skip_groups ThreeFieldApp#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#skip_users ThreeFieldApp#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#status ThreeFieldApp#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#timeouts ThreeFieldApp#timeouts}
        :param url_regex: A regex that further restricts URL to the specified regex. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#url_regex ThreeFieldApp#url_regex}
        :param user_name_template: Username template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template ThreeFieldApp#user_name_template}
        :param user_name_template_push_status: Push username on update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template_push_status ThreeFieldApp#user_name_template_push_status}
        :param user_name_template_suffix: Username template suffix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template_suffix ThreeFieldApp#user_name_template_suffix}
        :param user_name_template_type: Username template type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template_type ThreeFieldApp#user_name_template_type}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#users ThreeFieldApp#users}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33db50f1757e1d5e7b6ac5bfe98ce1a7979665c5d59086cc0c0e4cb900df5277)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ThreeFieldAppConfig(
            button_selector=button_selector,
            extra_field_selector=extra_field_selector,
            extra_field_value=extra_field_value,
            label=label,
            password_selector=password_selector,
            url=url,
            username_selector=username_selector,
            accessibility_error_redirect_url=accessibility_error_redirect_url,
            accessibility_login_redirect_url=accessibility_login_redirect_url,
            accessibility_self_service=accessibility_self_service,
            admin_note=admin_note,
            app_links_json=app_links_json,
            auto_submit_toolbar=auto_submit_toolbar,
            credentials_scheme=credentials_scheme,
            enduser_note=enduser_note,
            groups=groups,
            hide_ios=hide_ios,
            hide_web=hide_web,
            id=id,
            logo=logo,
            reveal_password=reveal_password,
            shared_password=shared_password,
            shared_username=shared_username,
            skip_groups=skip_groups,
            skip_users=skip_users,
            status=status,
            timeouts=timeouts,
            url_regex=url_regex,
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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#create ThreeFieldApp#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#read ThreeFieldApp#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#update ThreeFieldApp#update}.
        '''
        value = ThreeFieldAppTimeouts(create=create, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUsers")
    def put_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ThreeFieldAppUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7daae552f9bc2e0e1da16adf29c499a1c3614d41950f77c1e05e058887249446)
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

    @jsii.member(jsii_name="resetRevealPassword")
    def reset_reveal_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevealPassword", []))

    @jsii.member(jsii_name="resetSharedPassword")
    def reset_shared_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedPassword", []))

    @jsii.member(jsii_name="resetSharedUsername")
    def reset_shared_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedUsername", []))

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

    @jsii.member(jsii_name="resetUrlRegex")
    def reset_url_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRegex", []))

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
    def timeouts(self) -> "ThreeFieldAppTimeoutsOutputReference":
        return typing.cast("ThreeFieldAppTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> "ThreeFieldAppUsersList":
        return typing.cast("ThreeFieldAppUsersList", jsii.get(self, "users"))

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
    @jsii.member(jsii_name="autoSubmitToolbarInput")
    def auto_submit_toolbar_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoSubmitToolbarInput"))

    @builtins.property
    @jsii.member(jsii_name="buttonSelectorInput")
    def button_selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buttonSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsSchemeInput")
    def credentials_scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsSchemeInput"))

    @builtins.property
    @jsii.member(jsii_name="enduserNoteInput")
    def enduser_note_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enduserNoteInput"))

    @builtins.property
    @jsii.member(jsii_name="extraFieldSelectorInput")
    def extra_field_selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extraFieldSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="extraFieldValueInput")
    def extra_field_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extraFieldValueInput"))

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
    @jsii.member(jsii_name="passwordSelectorInput")
    def password_selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordSelectorInput"))

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
    ) -> typing.Optional[typing.Union["ThreeFieldAppTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ThreeFieldAppTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRegexInput")
    def url_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameSelectorInput")
    def username_selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameSelectorInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ThreeFieldAppUsers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ThreeFieldAppUsers"]]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="accessibilityErrorRedirectUrl")
    def accessibility_error_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityErrorRedirectUrl"))

    @accessibility_error_redirect_url.setter
    def accessibility_error_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b172547602c25d2fea4a4af493c0a56b3cdee940c99a2060abbb696b8c39b063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilityErrorRedirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="accessibilityLoginRedirectUrl")
    def accessibility_login_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityLoginRedirectUrl"))

    @accessibility_login_redirect_url.setter
    def accessibility_login_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61bfa1e5b7ae5869fa273fea4394d7977ba9517986f5092a4e41b70c9b7a041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7889c2ba464e23de8295b36798e359f591c2032592c46579446a411abe5cb072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilitySelfService", value)

    @builtins.property
    @jsii.member(jsii_name="adminNote")
    def admin_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminNote"))

    @admin_note.setter
    def admin_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e629b0a366425a92a66549ba3efc0d8838238e3e53c974524bbaad338f6ee441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminNote", value)

    @builtins.property
    @jsii.member(jsii_name="appLinksJson")
    def app_links_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLinksJson"))

    @app_links_json.setter
    def app_links_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac41fe6b0f91bd49dce65d9af3dcde76ffc3f64ba2ca788d28e8e97de850e330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLinksJson", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__99345cea63623b1ff100e0800ad374fa9c7de579746c51d9455e3d114302a5e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubmitToolbar", value)

    @builtins.property
    @jsii.member(jsii_name="buttonSelector")
    def button_selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buttonSelector"))

    @button_selector.setter
    def button_selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9197a6d893a2eb05d08f2e99a428354c7e8796f9dd9164a33933d87afb0aec17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buttonSelector", value)

    @builtins.property
    @jsii.member(jsii_name="credentialsScheme")
    def credentials_scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialsScheme"))

    @credentials_scheme.setter
    def credentials_scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0353e428eb3c9b6a2ed7c2a656f9d9b339712edb77eae09b55678d32937b24ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialsScheme", value)

    @builtins.property
    @jsii.member(jsii_name="enduserNote")
    def enduser_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enduserNote"))

    @enduser_note.setter
    def enduser_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c37d7d3fcb2ee81b7a481fa43c793cef857565c9db760dec83326c4f9819368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enduserNote", value)

    @builtins.property
    @jsii.member(jsii_name="extraFieldSelector")
    def extra_field_selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extraFieldSelector"))

    @extra_field_selector.setter
    def extra_field_selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a20ec2f353cce5f2393f404eeaf1e6df49abcee9bdebb1a1033fbfcb78bf5e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraFieldSelector", value)

    @builtins.property
    @jsii.member(jsii_name="extraFieldValue")
    def extra_field_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extraFieldValue"))

    @extra_field_value.setter
    def extra_field_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841bbc449d6548d993fd1b6947fcf90085c67d5d5d7c89993aded83c71a1d9e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraFieldValue", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a1d6d57de985669765cb173a75778a732a38de63e5f2d4baf99d7452b283c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d65c2f4778aaed7521b3e20aa34e9ebc8e9fefca8f0b790c2cc4266892ff8b75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4edad7738b7c1184a6986a9e8a055ecfe5b9b0f078d6537e6dc3a33dcab5a7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hideWeb", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ddca1f1448ffb07f85fc46366314b42c6525705dc5f7068ed77189ebcb1804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__550d299e4db1c2c32dcc599e0bb1640ee336d631a024ac5e2f9bd296df2966a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="logo")
    def logo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logo"))

    @logo.setter
    def logo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94435dc82c6530c2220758c427ea6a856b706f1b9f2d4e0aeba2e3d8aff0e4c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logo", value)

    @builtins.property
    @jsii.member(jsii_name="passwordSelector")
    def password_selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordSelector"))

    @password_selector.setter
    def password_selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9dd3adbe259f36552586fa33aba3d038a05844a016a034415f5a30e607b3a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordSelector", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a5514899586f04447646c4010ea0c28fe1a28d52b15e9330106fb90abd6e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revealPassword", value)

    @builtins.property
    @jsii.member(jsii_name="sharedPassword")
    def shared_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedPassword"))

    @shared_password.setter
    def shared_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07e7541857bc1a52ee575adc53d12fa33d2dbdcf1ba34c51fa1ad2d9a2f312f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedPassword", value)

    @builtins.property
    @jsii.member(jsii_name="sharedUsername")
    def shared_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedUsername"))

    @shared_username.setter
    def shared_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a76a3a9aa594f36037a288310393700f4f2a5552acebf58cb2df105476de9db4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedUsername", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__68c9c48d4bfa6b4921d2242a5dcb27bf496a2939b8ecf1747a4e307b3ed3576d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd668342bdfcc7b84df888330fbfc90efdc8f03616c03af05d11b88332b3864e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipUsers", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c232e152a8259d63ddb7922bd517d349a624631f8047d6794c63bdf417f02782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c1518f35ce95192a1c87f804af3753fe183bac7b66b4a32c0e5362042adb1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="urlRegex")
    def url_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlRegex"))

    @url_regex.setter
    def url_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7334351dda52b02e3a215f680f603bf1c0a5fb406848322a06625f70e6dad2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlRegex", value)

    @builtins.property
    @jsii.member(jsii_name="usernameSelector")
    def username_selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameSelector"))

    @username_selector.setter
    def username_selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c43156c92a05928ce8f757e5006d0b9bbf1024f40784f68f77e95d6ebb01a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameSelector", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplate")
    def user_name_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplate"))

    @user_name_template.setter
    def user_name_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a082d6e427b7ddc68f07894d6f007f52bc6a47260e6b74a93604eac11861e721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplatePushStatus")
    def user_name_template_push_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplatePushStatus"))

    @user_name_template_push_status.setter
    def user_name_template_push_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b30090718ccdd15c97ea474e1f4d7361e47c40fba2c6b208ab5cdc3e0f652b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplatePushStatus", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateSuffix")
    def user_name_template_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplateSuffix"))

    @user_name_template_suffix.setter
    def user_name_template_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc58b3a57fc76f06896e79e8b55cdaa74418141d94c0e3aca446dc133fbac70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplateSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="userNameTemplateType")
    def user_name_template_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userNameTemplateType"))

    @user_name_template_type.setter
    def user_name_template_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4a531e89ff0db5202dbfb9bbcdc6876bd1081f415c2143d1fdc5eb7ff0f2a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNameTemplateType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.threeFieldApp.ThreeFieldAppConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "button_selector": "buttonSelector",
        "extra_field_selector": "extraFieldSelector",
        "extra_field_value": "extraFieldValue",
        "label": "label",
        "password_selector": "passwordSelector",
        "url": "url",
        "username_selector": "usernameSelector",
        "accessibility_error_redirect_url": "accessibilityErrorRedirectUrl",
        "accessibility_login_redirect_url": "accessibilityLoginRedirectUrl",
        "accessibility_self_service": "accessibilitySelfService",
        "admin_note": "adminNote",
        "app_links_json": "appLinksJson",
        "auto_submit_toolbar": "autoSubmitToolbar",
        "credentials_scheme": "credentialsScheme",
        "enduser_note": "enduserNote",
        "groups": "groups",
        "hide_ios": "hideIos",
        "hide_web": "hideWeb",
        "id": "id",
        "logo": "logo",
        "reveal_password": "revealPassword",
        "shared_password": "sharedPassword",
        "shared_username": "sharedUsername",
        "skip_groups": "skipGroups",
        "skip_users": "skipUsers",
        "status": "status",
        "timeouts": "timeouts",
        "url_regex": "urlRegex",
        "user_name_template": "userNameTemplate",
        "user_name_template_push_status": "userNameTemplatePushStatus",
        "user_name_template_suffix": "userNameTemplateSuffix",
        "user_name_template_type": "userNameTemplateType",
        "users": "users",
    },
)
class ThreeFieldAppConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        button_selector: builtins.str,
        extra_field_selector: builtins.str,
        extra_field_value: builtins.str,
        label: builtins.str,
        password_selector: builtins.str,
        url: builtins.str,
        username_selector: builtins.str,
        accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        credentials_scheme: typing.Optional[builtins.str] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        reveal_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_password: typing.Optional[builtins.str] = None,
        shared_username: typing.Optional[builtins.str] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ThreeFieldAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        url_regex: typing.Optional[builtins.str] = None,
        user_name_template: typing.Optional[builtins.str] = None,
        user_name_template_push_status: typing.Optional[builtins.str] = None,
        user_name_template_suffix: typing.Optional[builtins.str] = None,
        user_name_template_type: typing.Optional[builtins.str] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ThreeFieldAppUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param button_selector: Login button field CSS selector. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#button_selector ThreeFieldApp#button_selector}
        :param extra_field_selector: Extra field CSS selector. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#extra_field_selector ThreeFieldApp#extra_field_selector}
        :param extra_field_value: Value for extra form field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#extra_field_value ThreeFieldApp#extra_field_value}
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#label ThreeFieldApp#label}
        :param password_selector: Login password field CSS selector. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#password_selector ThreeFieldApp#password_selector}
        :param url: Login URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#url ThreeFieldApp#url}
        :param username_selector: Login username field CSS selector. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#username_selector ThreeFieldApp#username_selector}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#accessibility_error_redirect_url ThreeFieldApp#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#accessibility_login_redirect_url ThreeFieldApp#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#accessibility_self_service ThreeFieldApp#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#admin_note ThreeFieldApp#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#app_links_json ThreeFieldApp#app_links_json}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#auto_submit_toolbar ThreeFieldApp#auto_submit_toolbar}
        :param credentials_scheme: Application credentials scheme. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#credentials_scheme ThreeFieldApp#credentials_scheme}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#enduser_note ThreeFieldApp#enduser_note}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#groups ThreeFieldApp#groups}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#hide_ios ThreeFieldApp#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#hide_web ThreeFieldApp#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#id ThreeFieldApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#logo ThreeFieldApp#logo}
        :param reveal_password: Allow user to reveal password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#reveal_password ThreeFieldApp#reveal_password}
        :param shared_password: Shared password, required for certain schemes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#shared_password ThreeFieldApp#shared_password}
        :param shared_username: Shared username, required for certain schemes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#shared_username ThreeFieldApp#shared_username}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#skip_groups ThreeFieldApp#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#skip_users ThreeFieldApp#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#status ThreeFieldApp#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#timeouts ThreeFieldApp#timeouts}
        :param url_regex: A regex that further restricts URL to the specified regex. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#url_regex ThreeFieldApp#url_regex}
        :param user_name_template: Username template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template ThreeFieldApp#user_name_template}
        :param user_name_template_push_status: Push username on update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template_push_status ThreeFieldApp#user_name_template_push_status}
        :param user_name_template_suffix: Username template suffix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template_suffix ThreeFieldApp#user_name_template_suffix}
        :param user_name_template_type: Username template type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template_type ThreeFieldApp#user_name_template_type}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#users ThreeFieldApp#users}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ThreeFieldAppTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab53e518fa070713724f5188d295dd754aecf6ad0e5e62a7ea0b999dacecad13)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument button_selector", value=button_selector, expected_type=type_hints["button_selector"])
            check_type(argname="argument extra_field_selector", value=extra_field_selector, expected_type=type_hints["extra_field_selector"])
            check_type(argname="argument extra_field_value", value=extra_field_value, expected_type=type_hints["extra_field_value"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument password_selector", value=password_selector, expected_type=type_hints["password_selector"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument username_selector", value=username_selector, expected_type=type_hints["username_selector"])
            check_type(argname="argument accessibility_error_redirect_url", value=accessibility_error_redirect_url, expected_type=type_hints["accessibility_error_redirect_url"])
            check_type(argname="argument accessibility_login_redirect_url", value=accessibility_login_redirect_url, expected_type=type_hints["accessibility_login_redirect_url"])
            check_type(argname="argument accessibility_self_service", value=accessibility_self_service, expected_type=type_hints["accessibility_self_service"])
            check_type(argname="argument admin_note", value=admin_note, expected_type=type_hints["admin_note"])
            check_type(argname="argument app_links_json", value=app_links_json, expected_type=type_hints["app_links_json"])
            check_type(argname="argument auto_submit_toolbar", value=auto_submit_toolbar, expected_type=type_hints["auto_submit_toolbar"])
            check_type(argname="argument credentials_scheme", value=credentials_scheme, expected_type=type_hints["credentials_scheme"])
            check_type(argname="argument enduser_note", value=enduser_note, expected_type=type_hints["enduser_note"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument hide_ios", value=hide_ios, expected_type=type_hints["hide_ios"])
            check_type(argname="argument hide_web", value=hide_web, expected_type=type_hints["hide_web"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logo", value=logo, expected_type=type_hints["logo"])
            check_type(argname="argument reveal_password", value=reveal_password, expected_type=type_hints["reveal_password"])
            check_type(argname="argument shared_password", value=shared_password, expected_type=type_hints["shared_password"])
            check_type(argname="argument shared_username", value=shared_username, expected_type=type_hints["shared_username"])
            check_type(argname="argument skip_groups", value=skip_groups, expected_type=type_hints["skip_groups"])
            check_type(argname="argument skip_users", value=skip_users, expected_type=type_hints["skip_users"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument url_regex", value=url_regex, expected_type=type_hints["url_regex"])
            check_type(argname="argument user_name_template", value=user_name_template, expected_type=type_hints["user_name_template"])
            check_type(argname="argument user_name_template_push_status", value=user_name_template_push_status, expected_type=type_hints["user_name_template_push_status"])
            check_type(argname="argument user_name_template_suffix", value=user_name_template_suffix, expected_type=type_hints["user_name_template_suffix"])
            check_type(argname="argument user_name_template_type", value=user_name_template_type, expected_type=type_hints["user_name_template_type"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "button_selector": button_selector,
            "extra_field_selector": extra_field_selector,
            "extra_field_value": extra_field_value,
            "label": label,
            "password_selector": password_selector,
            "url": url,
            "username_selector": username_selector,
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
        if reveal_password is not None:
            self._values["reveal_password"] = reveal_password
        if shared_password is not None:
            self._values["shared_password"] = shared_password
        if shared_username is not None:
            self._values["shared_username"] = shared_username
        if skip_groups is not None:
            self._values["skip_groups"] = skip_groups
        if skip_users is not None:
            self._values["skip_users"] = skip_users
        if status is not None:
            self._values["status"] = status
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if url_regex is not None:
            self._values["url_regex"] = url_regex
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
    def button_selector(self) -> builtins.str:
        '''Login button field CSS selector.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#button_selector ThreeFieldApp#button_selector}
        '''
        result = self._values.get("button_selector")
        assert result is not None, "Required property 'button_selector' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def extra_field_selector(self) -> builtins.str:
        '''Extra field CSS selector.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#extra_field_selector ThreeFieldApp#extra_field_selector}
        '''
        result = self._values.get("extra_field_selector")
        assert result is not None, "Required property 'extra_field_selector' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def extra_field_value(self) -> builtins.str:
        '''Value for extra form field.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#extra_field_value ThreeFieldApp#extra_field_value}
        '''
        result = self._values.get("extra_field_value")
        assert result is not None, "Required property 'extra_field_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def label(self) -> builtins.str:
        '''Pretty name of app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#label ThreeFieldApp#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password_selector(self) -> builtins.str:
        '''Login password field CSS selector.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#password_selector ThreeFieldApp#password_selector}
        '''
        result = self._values.get("password_selector")
        assert result is not None, "Required property 'password_selector' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Login URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#url ThreeFieldApp#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username_selector(self) -> builtins.str:
        '''Login username field CSS selector.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#username_selector ThreeFieldApp#username_selector}
        '''
        result = self._values.get("username_selector")
        assert result is not None, "Required property 'username_selector' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accessibility_error_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom error page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#accessibility_error_redirect_url ThreeFieldApp#accessibility_error_redirect_url}
        '''
        result = self._values.get("accessibility_error_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_login_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom login page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#accessibility_login_redirect_url ThreeFieldApp#accessibility_login_redirect_url}
        '''
        result = self._values.get("accessibility_login_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_self_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable self service.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#accessibility_self_service ThreeFieldApp#accessibility_self_service}
        '''
        result = self._values.get("accessibility_self_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def admin_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for admins.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#admin_note ThreeFieldApp#admin_note}
        '''
        result = self._values.get("admin_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_links_json(self) -> typing.Optional[builtins.str]:
        '''Displays specific appLinks for the app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#app_links_json ThreeFieldApp#app_links_json}
        '''
        result = self._values.get("app_links_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_submit_toolbar(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Display auto submit toolbar.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#auto_submit_toolbar ThreeFieldApp#auto_submit_toolbar}
        '''
        result = self._values.get("auto_submit_toolbar")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def credentials_scheme(self) -> typing.Optional[builtins.str]:
        '''Application credentials scheme.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#credentials_scheme ThreeFieldApp#credentials_scheme}
        '''
        result = self._values.get("credentials_scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enduser_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for end users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#enduser_note ThreeFieldApp#enduser_note}
        '''
        result = self._values.get("enduser_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Groups associated with the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#groups ThreeFieldApp#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def hide_ios(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon on mobile app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#hide_ios ThreeFieldApp#hide_ios}
        '''
        result = self._values.get("hide_ios")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hide_web(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon to users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#hide_web ThreeFieldApp#hide_web}
        '''
        result = self._values.get("hide_web")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#id ThreeFieldApp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo(self) -> typing.Optional[builtins.str]:
        '''Local path to logo of the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#logo ThreeFieldApp#logo}
        '''
        result = self._values.get("logo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reveal_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow user to reveal password.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#reveal_password ThreeFieldApp#reveal_password}
        '''
        result = self._values.get("reveal_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def shared_password(self) -> typing.Optional[builtins.str]:
        '''Shared password, required for certain schemes.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#shared_password ThreeFieldApp#shared_password}
        '''
        result = self._values.get("shared_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_username(self) -> typing.Optional[builtins.str]:
        '''Shared username, required for certain schemes.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#shared_username ThreeFieldApp#shared_username}
        '''
        result = self._values.get("shared_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#skip_groups ThreeFieldApp#skip_groups}
        '''
        result = self._values.get("skip_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_users(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#skip_users ThreeFieldApp#skip_users}
        '''
        result = self._values.get("skip_users")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#status ThreeFieldApp#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ThreeFieldAppTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#timeouts ThreeFieldApp#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ThreeFieldAppTimeouts"], result)

    @builtins.property
    def url_regex(self) -> typing.Optional[builtins.str]:
        '''A regex that further restricts URL to the specified regex.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#url_regex ThreeFieldApp#url_regex}
        '''
        result = self._values.get("url_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template(self) -> typing.Optional[builtins.str]:
        '''Username template.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template ThreeFieldApp#user_name_template}
        '''
        result = self._values.get("user_name_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_push_status(self) -> typing.Optional[builtins.str]:
        '''Push username on update.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template_push_status ThreeFieldApp#user_name_template_push_status}
        '''
        result = self._values.get("user_name_template_push_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_suffix(self) -> typing.Optional[builtins.str]:
        '''Username template suffix.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template_suffix ThreeFieldApp#user_name_template_suffix}
        '''
        result = self._values.get("user_name_template_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name_template_type(self) -> typing.Optional[builtins.str]:
        '''Username template type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#user_name_template_type ThreeFieldApp#user_name_template_type}
        '''
        result = self._values.get("user_name_template_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ThreeFieldAppUsers"]]]:
        '''users block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#users ThreeFieldApp#users}
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ThreeFieldAppUsers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThreeFieldAppConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.threeFieldApp.ThreeFieldAppTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "read": "read", "update": "update"},
)
class ThreeFieldAppTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#create ThreeFieldApp#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#read ThreeFieldApp#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#update ThreeFieldApp#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4314d99bb41aebdf1ffe03ed88de148c84770c217db23bf852c4b7e43a8b79c7)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#create ThreeFieldApp#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#read ThreeFieldApp#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#update ThreeFieldApp#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThreeFieldAppTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ThreeFieldAppTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.threeFieldApp.ThreeFieldAppTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a03ebfa32b8ea39fcc8e07f051dff4f9a543d86bdead176828aef9a96356090)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aae19a75f11efa5195a9f66987c5bc836c8c2067cf32d20232180aa78dd2ddc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d367e44ee65931f8e9fb9ddba1d52f0a4d50418056abb4079de46272f3320b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2967ad632bafa8788ff6b05d37b9800f879acd176530f766380a6c2f2fa268f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ThreeFieldAppTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ThreeFieldAppTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ThreeFieldAppTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49da1a76e9d391d4634050fec3e946d66d742dbe272d16ec532d6b4f64a3450c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.threeFieldApp.ThreeFieldAppUsers",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "password": "password", "username": "username"},
)
class ThreeFieldAppUsers:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: User ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#id ThreeFieldApp#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password: Password for user application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#password ThreeFieldApp#password}
        :param username: Username for user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#username ThreeFieldApp#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cfde363140005773673325e4b424a2dd8b7e389135d8dc1f2937be10c7fbb7d)
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#id ThreeFieldApp#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for user application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#password ThreeFieldApp#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/three_field_app#username ThreeFieldApp#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThreeFieldAppUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ThreeFieldAppUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.threeFieldApp.ThreeFieldAppUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a7756268c74c613241fa0c91d5bef237a493a3e56b3204065df85ec930821c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ThreeFieldAppUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17555cc54b2cfc5dcb65b7bf1aaec53ad4b5cbc7ce85903c37bacc64c1ac7c93)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ThreeFieldAppUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38851b59d02c2c06c200d2a68aa1d51589d2c9daa92e211ff7ce327c23cfa7bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fce0c305c2f922bd086c2fe5494a26deda61a63bd8d7f6605f7d8e39d182916)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5df5f23119c2a869ed76a259383bf9001a4dbf2dcaa64105a63d656de78d6f64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ThreeFieldAppUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ThreeFieldAppUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ThreeFieldAppUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5328269d190a50aabd39cd32e6a60318c32d34e4e9e22bf48845392557db15e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ThreeFieldAppUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.threeFieldApp.ThreeFieldAppUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a609da6d4d9a4662b7e4911412f09a694815cda4736927cab1d1f660dd952528)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9b9ced7bf198e2ea50bbcb25065c6415b4287602d923798c32e33e40da360df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e39a01f725523f2c5126e30f0082f89a6c954f5b878b2c4f9421601324d2a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0e76547f0c4c9c34b76dd87ae3b22ba08a364b23948f6d789b9794dab299156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ThreeFieldAppUsers, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ThreeFieldAppUsers, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ThreeFieldAppUsers, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eacf21e6c6ad666e986e407efdb2d08ea6c81c927fa1eb5d544d1c26d675913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ThreeFieldApp",
    "ThreeFieldAppConfig",
    "ThreeFieldAppTimeouts",
    "ThreeFieldAppTimeoutsOutputReference",
    "ThreeFieldAppUsers",
    "ThreeFieldAppUsersList",
    "ThreeFieldAppUsersOutputReference",
]

publication.publish()

def _typecheckingstub__33db50f1757e1d5e7b6ac5bfe98ce1a7979665c5d59086cc0c0e4cb900df5277(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    button_selector: builtins.str,
    extra_field_selector: builtins.str,
    extra_field_value: builtins.str,
    label: builtins.str,
    password_selector: builtins.str,
    url: builtins.str,
    username_selector: builtins.str,
    accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    credentials_scheme: typing.Optional[builtins.str] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    reveal_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    shared_password: typing.Optional[builtins.str] = None,
    shared_username: typing.Optional[builtins.str] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ThreeFieldAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    url_regex: typing.Optional[builtins.str] = None,
    user_name_template: typing.Optional[builtins.str] = None,
    user_name_template_push_status: typing.Optional[builtins.str] = None,
    user_name_template_suffix: typing.Optional[builtins.str] = None,
    user_name_template_type: typing.Optional[builtins.str] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ThreeFieldAppUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__7daae552f9bc2e0e1da16adf29c499a1c3614d41950f77c1e05e058887249446(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ThreeFieldAppUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b172547602c25d2fea4a4af493c0a56b3cdee940c99a2060abbb696b8c39b063(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61bfa1e5b7ae5869fa273fea4394d7977ba9517986f5092a4e41b70c9b7a041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7889c2ba464e23de8295b36798e359f591c2032592c46579446a411abe5cb072(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e629b0a366425a92a66549ba3efc0d8838238e3e53c974524bbaad338f6ee441(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac41fe6b0f91bd49dce65d9af3dcde76ffc3f64ba2ca788d28e8e97de850e330(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99345cea63623b1ff100e0800ad374fa9c7de579746c51d9455e3d114302a5e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9197a6d893a2eb05d08f2e99a428354c7e8796f9dd9164a33933d87afb0aec17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0353e428eb3c9b6a2ed7c2a656f9d9b339712edb77eae09b55678d32937b24ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c37d7d3fcb2ee81b7a481fa43c793cef857565c9db760dec83326c4f9819368(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a20ec2f353cce5f2393f404eeaf1e6df49abcee9bdebb1a1033fbfcb78bf5e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841bbc449d6548d993fd1b6947fcf90085c67d5d5d7c89993aded83c71a1d9e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a1d6d57de985669765cb173a75778a732a38de63e5f2d4baf99d7452b283c1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65c2f4778aaed7521b3e20aa34e9ebc8e9fefca8f0b790c2cc4266892ff8b75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4edad7738b7c1184a6986a9e8a055ecfe5b9b0f078d6537e6dc3a33dcab5a7c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ddca1f1448ffb07f85fc46366314b42c6525705dc5f7068ed77189ebcb1804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550d299e4db1c2c32dcc599e0bb1640ee336d631a024ac5e2f9bd296df2966a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94435dc82c6530c2220758c427ea6a856b706f1b9f2d4e0aeba2e3d8aff0e4c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9dd3adbe259f36552586fa33aba3d038a05844a016a034415f5a30e607b3a0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a5514899586f04447646c4010ea0c28fe1a28d52b15e9330106fb90abd6e7f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07e7541857bc1a52ee575adc53d12fa33d2dbdcf1ba34c51fa1ad2d9a2f312f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76a3a9aa594f36037a288310393700f4f2a5552acebf58cb2df105476de9db4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c9c48d4bfa6b4921d2242a5dcb27bf496a2939b8ecf1747a4e307b3ed3576d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd668342bdfcc7b84df888330fbfc90efdc8f03616c03af05d11b88332b3864e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c232e152a8259d63ddb7922bd517d349a624631f8047d6794c63bdf417f02782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c1518f35ce95192a1c87f804af3753fe183bac7b66b4a32c0e5362042adb1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7334351dda52b02e3a215f680f603bf1c0a5fb406848322a06625f70e6dad2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c43156c92a05928ce8f757e5006d0b9bbf1024f40784f68f77e95d6ebb01a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a082d6e427b7ddc68f07894d6f007f52bc6a47260e6b74a93604eac11861e721(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b30090718ccdd15c97ea474e1f4d7361e47c40fba2c6b208ab5cdc3e0f652b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc58b3a57fc76f06896e79e8b55cdaa74418141d94c0e3aca446dc133fbac70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4a531e89ff0db5202dbfb9bbcdc6876bd1081f415c2143d1fdc5eb7ff0f2a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab53e518fa070713724f5188d295dd754aecf6ad0e5e62a7ea0b999dacecad13(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    button_selector: builtins.str,
    extra_field_selector: builtins.str,
    extra_field_value: builtins.str,
    label: builtins.str,
    password_selector: builtins.str,
    url: builtins.str,
    username_selector: builtins.str,
    accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    credentials_scheme: typing.Optional[builtins.str] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    reveal_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    shared_password: typing.Optional[builtins.str] = None,
    shared_username: typing.Optional[builtins.str] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ThreeFieldAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    url_regex: typing.Optional[builtins.str] = None,
    user_name_template: typing.Optional[builtins.str] = None,
    user_name_template_push_status: typing.Optional[builtins.str] = None,
    user_name_template_suffix: typing.Optional[builtins.str] = None,
    user_name_template_type: typing.Optional[builtins.str] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ThreeFieldAppUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4314d99bb41aebdf1ffe03ed88de148c84770c217db23bf852c4b7e43a8b79c7(
    *,
    create: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a03ebfa32b8ea39fcc8e07f051dff4f9a543d86bdead176828aef9a96356090(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae19a75f11efa5195a9f66987c5bc836c8c2067cf32d20232180aa78dd2ddc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d367e44ee65931f8e9fb9ddba1d52f0a4d50418056abb4079de46272f3320b5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2967ad632bafa8788ff6b05d37b9800f879acd176530f766380a6c2f2fa268f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49da1a76e9d391d4634050fec3e946d66d742dbe272d16ec532d6b4f64a3450c(
    value: typing.Optional[typing.Union[ThreeFieldAppTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cfde363140005773673325e4b424a2dd8b7e389135d8dc1f2937be10c7fbb7d(
    *,
    id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7756268c74c613241fa0c91d5bef237a493a3e56b3204065df85ec930821c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17555cc54b2cfc5dcb65b7bf1aaec53ad4b5cbc7ce85903c37bacc64c1ac7c93(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38851b59d02c2c06c200d2a68aa1d51589d2c9daa92e211ff7ce327c23cfa7bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fce0c305c2f922bd086c2fe5494a26deda61a63bd8d7f6605f7d8e39d182916(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df5f23119c2a869ed76a259383bf9001a4dbf2dcaa64105a63d656de78d6f64(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5328269d190a50aabd39cd32e6a60318c32d34e4e9e22bf48845392557db15e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ThreeFieldAppUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a609da6d4d9a4662b7e4911412f09a694815cda4736927cab1d1f660dd952528(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b9ced7bf198e2ea50bbcb25065c6415b4287602d923798c32e33e40da360df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e39a01f725523f2c5126e30f0082f89a6c954f5b878b2c4f9421601324d2a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e76547f0c4c9c34b76dd87ae3b22ba08a364b23948f6d789b9794dab299156(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eacf21e6c6ad666e986e407efdb2d08ea6c81c927fa1eb5d544d1c26d675913(
    value: typing.Optional[typing.Union[ThreeFieldAppUsers, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
