'''
# `okta_app_basic_auth`

Refer to the Terraform Registory for docs: [`okta_app_basic_auth`](https://www.terraform.io/docs/providers/okta/r/app_basic_auth).
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


class AppBasicAuth(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appBasicAuth.AppBasicAuth",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth okta_app_basic_auth}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        auth_url: builtins.str,
        label: builtins.str,
        url: builtins.str,
        accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AppBasicAuthTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppBasicAuthUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth okta_app_basic_auth} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auth_url: Login button field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#auth_url AppBasicAuth#auth_url}
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#label AppBasicAuth#label}
        :param url: Login password field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#url AppBasicAuth#url}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#accessibility_error_redirect_url AppBasicAuth#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#accessibility_login_redirect_url AppBasicAuth#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#accessibility_self_service AppBasicAuth#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#admin_note AppBasicAuth#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#app_links_json AppBasicAuth#app_links_json}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#auto_submit_toolbar AppBasicAuth#auto_submit_toolbar}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#enduser_note AppBasicAuth#enduser_note}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#groups AppBasicAuth#groups}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#hide_ios AppBasicAuth#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#hide_web AppBasicAuth#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#id AppBasicAuth#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#logo AppBasicAuth#logo}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#skip_groups AppBasicAuth#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#skip_users AppBasicAuth#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#status AppBasicAuth#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#timeouts AppBasicAuth#timeouts}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#users AppBasicAuth#users}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a6dc01dbca2fe8ade4393b2af8bb27527a7e01bf7efb3f5a7f043da78f87d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppBasicAuthConfig(
            auth_url=auth_url,
            label=label,
            url=url,
            accessibility_error_redirect_url=accessibility_error_redirect_url,
            accessibility_login_redirect_url=accessibility_login_redirect_url,
            accessibility_self_service=accessibility_self_service,
            admin_note=admin_note,
            app_links_json=app_links_json,
            auto_submit_toolbar=auto_submit_toolbar,
            enduser_note=enduser_note,
            groups=groups,
            hide_ios=hide_ios,
            hide_web=hide_web,
            id=id,
            logo=logo,
            skip_groups=skip_groups,
            skip_users=skip_users,
            status=status,
            timeouts=timeouts,
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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#create AppBasicAuth#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#read AppBasicAuth#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#update AppBasicAuth#update}.
        '''
        value = AppBasicAuthTimeouts(create=create, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUsers")
    def put_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppBasicAuthUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d72e89a0df2e3de50199ec32a055c1679dbe130c5759b891260ec4a1d672eeee)
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
    def timeouts(self) -> "AppBasicAuthTimeoutsOutputReference":
        return typing.cast("AppBasicAuthTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> "AppBasicAuthUsersList":
        return typing.cast("AppBasicAuthUsersList", jsii.get(self, "users"))

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
    @jsii.member(jsii_name="authUrlInput")
    def auth_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="autoSubmitToolbarInput")
    def auto_submit_toolbar_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoSubmitToolbarInput"))

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
    ) -> typing.Optional[typing.Union["AppBasicAuthTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["AppBasicAuthTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="usersInput")
    def users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppBasicAuthUsers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppBasicAuthUsers"]]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="accessibilityErrorRedirectUrl")
    def accessibility_error_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityErrorRedirectUrl"))

    @accessibility_error_redirect_url.setter
    def accessibility_error_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81de75f5fc88bf58a91cb85a8ef752810b16f52281d070702ee7cd1571ddd584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilityErrorRedirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="accessibilityLoginRedirectUrl")
    def accessibility_login_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityLoginRedirectUrl"))

    @accessibility_login_redirect_url.setter
    def accessibility_login_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b85e40b6c2a0ae4f8bae66fccdef7278b184b467be724e0b78984f5195c406a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__412a987b2564ef87593151c1a9a632dbdf7eaa6967a041a2dcdc22fbd4530fb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilitySelfService", value)

    @builtins.property
    @jsii.member(jsii_name="adminNote")
    def admin_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminNote"))

    @admin_note.setter
    def admin_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72bb99c90f893aa0c6347c795793a5f77fca5e40703e83c7b4d46003d4516a6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminNote", value)

    @builtins.property
    @jsii.member(jsii_name="appLinksJson")
    def app_links_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLinksJson"))

    @app_links_json.setter
    def app_links_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea833fed17651953baa9422d3e13662069e0b59a5b96c5f3cbc5607a96e6edfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLinksJson", value)

    @builtins.property
    @jsii.member(jsii_name="authUrl")
    def auth_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authUrl"))

    @auth_url.setter
    def auth_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf5c1ef78968fcdca92e14d661d691ec0f9501c276985b795a7036dba966a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authUrl", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__46f1fd7b5bea0214b9971a6fc03bdb05112fc631f210ed296606dafdf8fc4a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubmitToolbar", value)

    @builtins.property
    @jsii.member(jsii_name="enduserNote")
    def enduser_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enduserNote"))

    @enduser_note.setter
    def enduser_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94189fbf3cc9aff2c36765ab2a18da7b58e9c7fc7b810ea35d3d98815a55cb36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enduserNote", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eccbca078150d27d36ddf948d325b687cd7353447c31ca0401c9ce98ad0c8d0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e029841679cb5827c33027e8bd0a424b671ae22da90ece8cb66d663ba98cd664)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fb8df8f8c2bcaf1e763c79a0a58293d3678da3644eb1d0f20f954f50f3e4005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hideWeb", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d88271aa65676cc3f4236653859973621f3b634b26da1002ba4dfba7af2b9fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363317d8de2a1cfca65b33c0c4f9e5e1ef98723b5da39b0233e9d7c8f6716ab4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="logo")
    def logo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logo"))

    @logo.setter
    def logo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a60c42008d0eb03afc37ce41afc4e2cc68736de4a88b46ac93507d07b8ddf399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logo", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__aa774e62387a549ef23e5760f4e2b15c2afc42f714ee46754e8788ea386eba01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23ba0a70e3058d10bbf9797dbff38a4e10da06a5470e5ceb62d542e7514ced6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipUsers", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d825a8e3196e6683246b21ae832e6f6d6019e4c80b54a7f66f4e1a8533bab96a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f3f59b5984634de47114c0b845effbfb25f985f2437f39a6d1a70f82fecd93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appBasicAuth.AppBasicAuthConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "auth_url": "authUrl",
        "label": "label",
        "url": "url",
        "accessibility_error_redirect_url": "accessibilityErrorRedirectUrl",
        "accessibility_login_redirect_url": "accessibilityLoginRedirectUrl",
        "accessibility_self_service": "accessibilitySelfService",
        "admin_note": "adminNote",
        "app_links_json": "appLinksJson",
        "auto_submit_toolbar": "autoSubmitToolbar",
        "enduser_note": "enduserNote",
        "groups": "groups",
        "hide_ios": "hideIos",
        "hide_web": "hideWeb",
        "id": "id",
        "logo": "logo",
        "skip_groups": "skipGroups",
        "skip_users": "skipUsers",
        "status": "status",
        "timeouts": "timeouts",
        "users": "users",
    },
)
class AppBasicAuthConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auth_url: builtins.str,
        label: builtins.str,
        url: builtins.str,
        accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AppBasicAuthTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppBasicAuthUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param auth_url: Login button field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#auth_url AppBasicAuth#auth_url}
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#label AppBasicAuth#label}
        :param url: Login password field. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#url AppBasicAuth#url}
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#accessibility_error_redirect_url AppBasicAuth#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#accessibility_login_redirect_url AppBasicAuth#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#accessibility_self_service AppBasicAuth#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#admin_note AppBasicAuth#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#app_links_json AppBasicAuth#app_links_json}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#auto_submit_toolbar AppBasicAuth#auto_submit_toolbar}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#enduser_note AppBasicAuth#enduser_note}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#groups AppBasicAuth#groups}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#hide_ios AppBasicAuth#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#hide_web AppBasicAuth#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#id AppBasicAuth#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#logo AppBasicAuth#logo}
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#skip_groups AppBasicAuth#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#skip_users AppBasicAuth#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#status AppBasicAuth#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#timeouts AppBasicAuth#timeouts}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#users AppBasicAuth#users}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = AppBasicAuthTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a1b1e2f148023064aa0d2fb20c214954f54adc3073f93ef95ed215a55ff18a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument auth_url", value=auth_url, expected_type=type_hints["auth_url"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument accessibility_error_redirect_url", value=accessibility_error_redirect_url, expected_type=type_hints["accessibility_error_redirect_url"])
            check_type(argname="argument accessibility_login_redirect_url", value=accessibility_login_redirect_url, expected_type=type_hints["accessibility_login_redirect_url"])
            check_type(argname="argument accessibility_self_service", value=accessibility_self_service, expected_type=type_hints["accessibility_self_service"])
            check_type(argname="argument admin_note", value=admin_note, expected_type=type_hints["admin_note"])
            check_type(argname="argument app_links_json", value=app_links_json, expected_type=type_hints["app_links_json"])
            check_type(argname="argument auto_submit_toolbar", value=auto_submit_toolbar, expected_type=type_hints["auto_submit_toolbar"])
            check_type(argname="argument enduser_note", value=enduser_note, expected_type=type_hints["enduser_note"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument hide_ios", value=hide_ios, expected_type=type_hints["hide_ios"])
            check_type(argname="argument hide_web", value=hide_web, expected_type=type_hints["hide_web"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logo", value=logo, expected_type=type_hints["logo"])
            check_type(argname="argument skip_groups", value=skip_groups, expected_type=type_hints["skip_groups"])
            check_type(argname="argument skip_users", value=skip_users, expected_type=type_hints["skip_users"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_url": auth_url,
            "label": label,
            "url": url,
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
        if skip_groups is not None:
            self._values["skip_groups"] = skip_groups
        if skip_users is not None:
            self._values["skip_users"] = skip_users
        if status is not None:
            self._values["status"] = status
        if timeouts is not None:
            self._values["timeouts"] = timeouts
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
    def auth_url(self) -> builtins.str:
        '''Login button field.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#auth_url AppBasicAuth#auth_url}
        '''
        result = self._values.get("auth_url")
        assert result is not None, "Required property 'auth_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def label(self) -> builtins.str:
        '''Pretty name of app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#label AppBasicAuth#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Login password field.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#url AppBasicAuth#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accessibility_error_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom error page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#accessibility_error_redirect_url AppBasicAuth#accessibility_error_redirect_url}
        '''
        result = self._values.get("accessibility_error_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_login_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom login page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#accessibility_login_redirect_url AppBasicAuth#accessibility_login_redirect_url}
        '''
        result = self._values.get("accessibility_login_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_self_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable self service.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#accessibility_self_service AppBasicAuth#accessibility_self_service}
        '''
        result = self._values.get("accessibility_self_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def admin_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for admins.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#admin_note AppBasicAuth#admin_note}
        '''
        result = self._values.get("admin_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_links_json(self) -> typing.Optional[builtins.str]:
        '''Displays specific appLinks for the app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#app_links_json AppBasicAuth#app_links_json}
        '''
        result = self._values.get("app_links_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_submit_toolbar(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Display auto submit toolbar.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#auto_submit_toolbar AppBasicAuth#auto_submit_toolbar}
        '''
        result = self._values.get("auto_submit_toolbar")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enduser_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for end users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#enduser_note AppBasicAuth#enduser_note}
        '''
        result = self._values.get("enduser_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Groups associated with the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#groups AppBasicAuth#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def hide_ios(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon on mobile app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#hide_ios AppBasicAuth#hide_ios}
        '''
        result = self._values.get("hide_ios")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hide_web(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon to users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#hide_web AppBasicAuth#hide_web}
        '''
        result = self._values.get("hide_web")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#id AppBasicAuth#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo(self) -> typing.Optional[builtins.str]:
        '''Local path to logo of the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#logo AppBasicAuth#logo}
        '''
        result = self._values.get("logo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#skip_groups AppBasicAuth#skip_groups}
        '''
        result = self._values.get("skip_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_users(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#skip_users AppBasicAuth#skip_users}
        '''
        result = self._values.get("skip_users")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#status AppBasicAuth#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AppBasicAuthTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#timeouts AppBasicAuth#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AppBasicAuthTimeouts"], result)

    @builtins.property
    def users(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppBasicAuthUsers"]]]:
        '''users block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#users AppBasicAuth#users}
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppBasicAuthUsers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppBasicAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appBasicAuth.AppBasicAuthTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "read": "read", "update": "update"},
)
class AppBasicAuthTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#create AppBasicAuth#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#read AppBasicAuth#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#update AppBasicAuth#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38857adcd5046c32b3c0049010c48a93cfe90e41d70d3160c1e279b96aa3ea1)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#create AppBasicAuth#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#read AppBasicAuth#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#update AppBasicAuth#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppBasicAuthTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppBasicAuthTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appBasicAuth.AppBasicAuthTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec97e60e57d71a7322638d0ceb03afa4f437be72127b33c88e06fdb493ec7942)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc3197108160d75437ff13722b916f4557bb9d7b7cd3c5042f6ae83b229cbc44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76b03aaaa40df02194dc9712861df20d5de5a57b22698e126500e867e976158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1aadc0814b9f471ca1fee52a0f51fbf5705dd6458b1f117901b483c004d9ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppBasicAuthTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppBasicAuthTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppBasicAuthTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85172e1e2cb3766108f1102f5790335313c2f5572e1fd697c09099dcb867443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appBasicAuth.AppBasicAuthUsers",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "password": "password", "username": "username"},
)
class AppBasicAuthUsers:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: User ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#id AppBasicAuth#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password: Password for user application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#password AppBasicAuth#password}
        :param username: Username for user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#username AppBasicAuth#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a742dea9d478a9ac44edc90cb837ce14d2a64d74efede9959c9731ee6c973b41)
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#id AppBasicAuth#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for user application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#password AppBasicAuth#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_basic_auth#username AppBasicAuth#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppBasicAuthUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppBasicAuthUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appBasicAuth.AppBasicAuthUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59a9fd88cc1682e85d5066a5a6d3aa9e4b999b8af6a7a5a9a8797b0b26a20f84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppBasicAuthUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a4cfa5294767d19fd25728e990c7ab2ea696ddbef918de14df9031fafb1745e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppBasicAuthUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72408f201da2149d91a19369ac91d153a484d839bbe5d5f03d265e9cc09a8bfe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39d944028e5809de4c6feb08f364c69389db86ec8bc7588629aa2059e048960d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__631d60c820c0b0b72736bd2ac1a553a65fd6d9c9cad7d1ff3087fe140809012b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppBasicAuthUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppBasicAuthUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppBasicAuthUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4fdacc987139b5ffe90129b1f9697abb67bda83c479cfd4cd022808cda1ef52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppBasicAuthUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appBasicAuth.AppBasicAuthUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97bba848d74ce82a927463758a98c396c3a55e3627ce88ebd8597fd9735e945f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__306ef663c428a8f171441758c3a445b26f9abdd0de1ba95df84bbfe051ef5b12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ae09a0201e62135664b3e7c80b64ee206269314020cacc1a24bd23f9ae58f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974e92b00145fbda6689e34053355afa5c9d2d88ab0847aa0e750fdce05d70da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppBasicAuthUsers, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppBasicAuthUsers, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppBasicAuthUsers, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0048246b5d3d21e1db009a72d19291f7f7af15a94b162104812a7b17bfdda84c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AppBasicAuth",
    "AppBasicAuthConfig",
    "AppBasicAuthTimeouts",
    "AppBasicAuthTimeoutsOutputReference",
    "AppBasicAuthUsers",
    "AppBasicAuthUsersList",
    "AppBasicAuthUsersOutputReference",
]

publication.publish()

def _typecheckingstub__15a6dc01dbca2fe8ade4393b2af8bb27527a7e01bf7efb3f5a7f043da78f87d9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    auth_url: builtins.str,
    label: builtins.str,
    url: builtins.str,
    accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AppBasicAuthTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppBasicAuthUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__d72e89a0df2e3de50199ec32a055c1679dbe130c5759b891260ec4a1d672eeee(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppBasicAuthUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81de75f5fc88bf58a91cb85a8ef752810b16f52281d070702ee7cd1571ddd584(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b85e40b6c2a0ae4f8bae66fccdef7278b184b467be724e0b78984f5195c406a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412a987b2564ef87593151c1a9a632dbdf7eaa6967a041a2dcdc22fbd4530fb4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bb99c90f893aa0c6347c795793a5f77fca5e40703e83c7b4d46003d4516a6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea833fed17651953baa9422d3e13662069e0b59a5b96c5f3cbc5607a96e6edfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf5c1ef78968fcdca92e14d661d691ec0f9501c276985b795a7036dba966a9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f1fd7b5bea0214b9971a6fc03bdb05112fc631f210ed296606dafdf8fc4a1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94189fbf3cc9aff2c36765ab2a18da7b58e9c7fc7b810ea35d3d98815a55cb36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccbca078150d27d36ddf948d325b687cd7353447c31ca0401c9ce98ad0c8d0d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e029841679cb5827c33027e8bd0a424b671ae22da90ece8cb66d663ba98cd664(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb8df8f8c2bcaf1e763c79a0a58293d3678da3644eb1d0f20f954f50f3e4005(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d88271aa65676cc3f4236653859973621f3b634b26da1002ba4dfba7af2b9fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363317d8de2a1cfca65b33c0c4f9e5e1ef98723b5da39b0233e9d7c8f6716ab4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60c42008d0eb03afc37ce41afc4e2cc68736de4a88b46ac93507d07b8ddf399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa774e62387a549ef23e5760f4e2b15c2afc42f714ee46754e8788ea386eba01(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ba0a70e3058d10bbf9797dbff38a4e10da06a5470e5ceb62d542e7514ced6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d825a8e3196e6683246b21ae832e6f6d6019e4c80b54a7f66f4e1a8533bab96a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f3f59b5984634de47114c0b845effbfb25f985f2437f39a6d1a70f82fecd93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a1b1e2f148023064aa0d2fb20c214954f54adc3073f93ef95ed215a55ff18a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_url: builtins.str,
    label: builtins.str,
    url: builtins.str,
    accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AppBasicAuthTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppBasicAuthUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38857adcd5046c32b3c0049010c48a93cfe90e41d70d3160c1e279b96aa3ea1(
    *,
    create: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec97e60e57d71a7322638d0ceb03afa4f437be72127b33c88e06fdb493ec7942(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3197108160d75437ff13722b916f4557bb9d7b7cd3c5042f6ae83b229cbc44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76b03aaaa40df02194dc9712861df20d5de5a57b22698e126500e867e976158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1aadc0814b9f471ca1fee52a0f51fbf5705dd6458b1f117901b483c004d9ed2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85172e1e2cb3766108f1102f5790335313c2f5572e1fd697c09099dcb867443(
    value: typing.Optional[typing.Union[AppBasicAuthTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a742dea9d478a9ac44edc90cb837ce14d2a64d74efede9959c9731ee6c973b41(
    *,
    id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a9fd88cc1682e85d5066a5a6d3aa9e4b999b8af6a7a5a9a8797b0b26a20f84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4cfa5294767d19fd25728e990c7ab2ea696ddbef918de14df9031fafb1745e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72408f201da2149d91a19369ac91d153a484d839bbe5d5f03d265e9cc09a8bfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d944028e5809de4c6feb08f364c69389db86ec8bc7588629aa2059e048960d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631d60c820c0b0b72736bd2ac1a553a65fd6d9c9cad7d1ff3087fe140809012b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4fdacc987139b5ffe90129b1f9697abb67bda83c479cfd4cd022808cda1ef52(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppBasicAuthUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97bba848d74ce82a927463758a98c396c3a55e3627ce88ebd8597fd9735e945f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306ef663c428a8f171441758c3a445b26f9abdd0de1ba95df84bbfe051ef5b12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ae09a0201e62135664b3e7c80b64ee206269314020cacc1a24bd23f9ae58f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974e92b00145fbda6689e34053355afa5c9d2d88ab0847aa0e750fdce05d70da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0048246b5d3d21e1db009a72d19291f7f7af15a94b162104812a7b17bfdda84c(
    value: typing.Optional[typing.Union[AppBasicAuthUsers, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
