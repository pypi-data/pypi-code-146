'''
# `okta_bookmark_app`

Refer to the Terraform Registory for docs: [`okta_bookmark_app`](https://www.terraform.io/docs/providers/okta/r/bookmark_app).
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


class BookmarkApp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.bookmarkApp.BookmarkApp",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app okta_bookmark_app}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        label: builtins.str,
        url: builtins.str,
        accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        authentication_policy: typing.Optional[builtins.str] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        request_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BookmarkAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BookmarkAppUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app okta_bookmark_app} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#label BookmarkApp#label}
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#url BookmarkApp#url}.
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#accessibility_error_redirect_url BookmarkApp#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#accessibility_login_redirect_url BookmarkApp#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#accessibility_self_service BookmarkApp#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#admin_note BookmarkApp#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#app_links_json BookmarkApp#app_links_json}
        :param authentication_policy: Id of this apps authentication policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#authentication_policy BookmarkApp#authentication_policy}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#auto_submit_toolbar BookmarkApp#auto_submit_toolbar}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#enduser_note BookmarkApp#enduser_note}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#groups BookmarkApp#groups}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#hide_ios BookmarkApp#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#hide_web BookmarkApp#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#id BookmarkApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#logo BookmarkApp#logo}
        :param request_integration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#request_integration BookmarkApp#request_integration}.
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#skip_groups BookmarkApp#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#skip_users BookmarkApp#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#status BookmarkApp#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#timeouts BookmarkApp#timeouts}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#users BookmarkApp#users}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25e30bff5d9c333ec2086228e3db31071cb348b5c48f6f201b3efb987abb245)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BookmarkAppConfig(
            label=label,
            url=url,
            accessibility_error_redirect_url=accessibility_error_redirect_url,
            accessibility_login_redirect_url=accessibility_login_redirect_url,
            accessibility_self_service=accessibility_self_service,
            admin_note=admin_note,
            app_links_json=app_links_json,
            authentication_policy=authentication_policy,
            auto_submit_toolbar=auto_submit_toolbar,
            enduser_note=enduser_note,
            groups=groups,
            hide_ios=hide_ios,
            hide_web=hide_web,
            id=id,
            logo=logo,
            request_integration=request_integration,
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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#create BookmarkApp#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#read BookmarkApp#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#update BookmarkApp#update}.
        '''
        value = BookmarkAppTimeouts(create=create, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUsers")
    def put_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BookmarkAppUsers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b865f27f8ebedfb0503876b1d96b1c255f8d5456501a41879903e65b9db8275)
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

    @jsii.member(jsii_name="resetAuthenticationPolicy")
    def reset_authentication_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationPolicy", []))

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

    @jsii.member(jsii_name="resetRequestIntegration")
    def reset_request_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestIntegration", []))

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
    def timeouts(self) -> "BookmarkAppTimeoutsOutputReference":
        return typing.cast("BookmarkAppTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> "BookmarkAppUsersList":
        return typing.cast("BookmarkAppUsersList", jsii.get(self, "users"))

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
    @jsii.member(jsii_name="authenticationPolicyInput")
    def authentication_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationPolicyInput"))

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
    @jsii.member(jsii_name="requestIntegrationInput")
    def request_integration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requestIntegrationInput"))

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
    ) -> typing.Optional[typing.Union["BookmarkAppTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["BookmarkAppTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="usersInput")
    def users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BookmarkAppUsers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BookmarkAppUsers"]]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="accessibilityErrorRedirectUrl")
    def accessibility_error_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityErrorRedirectUrl"))

    @accessibility_error_redirect_url.setter
    def accessibility_error_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e88caf5c4cfb6e9aba56c230f9eeb499bdd3371a988e664f27003796fd05a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilityErrorRedirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="accessibilityLoginRedirectUrl")
    def accessibility_login_redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessibilityLoginRedirectUrl"))

    @accessibility_login_redirect_url.setter
    def accessibility_login_redirect_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d77f8214f859714047c17d318074e9762c4fce58445bea712195f050df7234)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1cb352e337555bd8a4af711dc6429a38fbb54497dbe2168dd5c0034af907c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessibilitySelfService", value)

    @builtins.property
    @jsii.member(jsii_name="adminNote")
    def admin_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminNote"))

    @admin_note.setter
    def admin_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1078db8215ddb172f0c737c4ff90f22209794b0d47f75ebdfcd21f25debb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminNote", value)

    @builtins.property
    @jsii.member(jsii_name="appLinksJson")
    def app_links_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLinksJson"))

    @app_links_json.setter
    def app_links_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d778867aed14c30989098830b6639c70aaf758e73c2e71d0a9de95d0f84e45e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLinksJson", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationPolicy")
    def authentication_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationPolicy"))

    @authentication_policy.setter
    def authentication_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188167a787e41923360ca6cbfeceaafb94c01c3a77d1bf88b1a530ad0bffed64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationPolicy", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__dccb71229860a580f9e97b9414b68953b0cbe347f8e7f779891f2af3ca62dd53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubmitToolbar", value)

    @builtins.property
    @jsii.member(jsii_name="enduserNote")
    def enduser_note(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enduserNote"))

    @enduser_note.setter
    def enduser_note(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd225d984b90c734840130483828c216498f2a2c259af2d9dcef65b0dabf7198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enduserNote", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9ee8f38ded8edc90f2d39138f8bef92275d865d15e9fc039b8e271e5905b23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a597eb5e5891b94431db8f6c5d2b3bcf373d09ce3a1223c9f92e30a491e719a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ec8e30a7de74298ffee251d37177f371fee9ef5d6fcbc139e4d07de50b7cfbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hideWeb", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d87a5cb5f10fb7909a8b109174a46f27d03b183f9401296de7f02341a4a77a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d661934221d5ebebbb90d8f46f782cfabf1a6e42df0b879ead94487b8382288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="logo")
    def logo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logo"))

    @logo.setter
    def logo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9fd9e13f471b0f40adb13b074c896f90e75ce3fcf24b65d197ed6af3eb5a8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logo", value)

    @builtins.property
    @jsii.member(jsii_name="requestIntegration")
    def request_integration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requestIntegration"))

    @request_integration.setter
    def request_integration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc9cb1a63e530d1e5a2edd8e1cbb431bf97333a52246433a540468dd4697e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestIntegration", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__cb0991223d707976801e855cbd9617778f3a935a1b6af0d0e4f0836bbb23c903)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7445c03110ef463457d252885d4896881775363f0d7099243ce1c438ac6552b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipUsers", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5ca2cf2dac8c9e5f5ca77be021ff9e6a610626503127e5c35f53a95b59bf01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642dab04c678dd1b008bb7c909612e2a313c60a1f61aeded1dd232de5a97e37a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.bookmarkApp.BookmarkAppConfig",
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
        "url": "url",
        "accessibility_error_redirect_url": "accessibilityErrorRedirectUrl",
        "accessibility_login_redirect_url": "accessibilityLoginRedirectUrl",
        "accessibility_self_service": "accessibilitySelfService",
        "admin_note": "adminNote",
        "app_links_json": "appLinksJson",
        "authentication_policy": "authenticationPolicy",
        "auto_submit_toolbar": "autoSubmitToolbar",
        "enduser_note": "enduserNote",
        "groups": "groups",
        "hide_ios": "hideIos",
        "hide_web": "hideWeb",
        "id": "id",
        "logo": "logo",
        "request_integration": "requestIntegration",
        "skip_groups": "skipGroups",
        "skip_users": "skipUsers",
        "status": "status",
        "timeouts": "timeouts",
        "users": "users",
    },
)
class BookmarkAppConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        url: builtins.str,
        accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
        accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        admin_note: typing.Optional[builtins.str] = None,
        app_links_json: typing.Optional[builtins.str] = None,
        authentication_policy: typing.Optional[builtins.str] = None,
        auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enduser_note: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logo: typing.Optional[builtins.str] = None,
        request_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BookmarkAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BookmarkAppUsers", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param label: Pretty name of app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#label BookmarkApp#label}
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#url BookmarkApp#url}.
        :param accessibility_error_redirect_url: Custom error page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#accessibility_error_redirect_url BookmarkApp#accessibility_error_redirect_url}
        :param accessibility_login_redirect_url: Custom login page URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#accessibility_login_redirect_url BookmarkApp#accessibility_login_redirect_url}
        :param accessibility_self_service: Enable self service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#accessibility_self_service BookmarkApp#accessibility_self_service}
        :param admin_note: Application notes for admins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#admin_note BookmarkApp#admin_note}
        :param app_links_json: Displays specific appLinks for the app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#app_links_json BookmarkApp#app_links_json}
        :param authentication_policy: Id of this apps authentication policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#authentication_policy BookmarkApp#authentication_policy}
        :param auto_submit_toolbar: Display auto submit toolbar. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#auto_submit_toolbar BookmarkApp#auto_submit_toolbar}
        :param enduser_note: Application notes for end users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#enduser_note BookmarkApp#enduser_note}
        :param groups: Groups associated with the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#groups BookmarkApp#groups}
        :param hide_ios: Do not display application icon on mobile app. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#hide_ios BookmarkApp#hide_ios}
        :param hide_web: Do not display application icon to users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#hide_web BookmarkApp#hide_web}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#id BookmarkApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logo: Local path to logo of the application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#logo BookmarkApp#logo}
        :param request_integration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#request_integration BookmarkApp#request_integration}.
        :param skip_groups: Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#skip_groups BookmarkApp#skip_groups}
        :param skip_users: Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#skip_users BookmarkApp#skip_users}
        :param status: Status of application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#status BookmarkApp#status}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#timeouts BookmarkApp#timeouts}
        :param users: users block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#users BookmarkApp#users}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = BookmarkAppTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39d9f42ec53a7bb8f0411ac2b7b3ea0d4ca25e4c363e639861cb3d5f9c32326)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument accessibility_error_redirect_url", value=accessibility_error_redirect_url, expected_type=type_hints["accessibility_error_redirect_url"])
            check_type(argname="argument accessibility_login_redirect_url", value=accessibility_login_redirect_url, expected_type=type_hints["accessibility_login_redirect_url"])
            check_type(argname="argument accessibility_self_service", value=accessibility_self_service, expected_type=type_hints["accessibility_self_service"])
            check_type(argname="argument admin_note", value=admin_note, expected_type=type_hints["admin_note"])
            check_type(argname="argument app_links_json", value=app_links_json, expected_type=type_hints["app_links_json"])
            check_type(argname="argument authentication_policy", value=authentication_policy, expected_type=type_hints["authentication_policy"])
            check_type(argname="argument auto_submit_toolbar", value=auto_submit_toolbar, expected_type=type_hints["auto_submit_toolbar"])
            check_type(argname="argument enduser_note", value=enduser_note, expected_type=type_hints["enduser_note"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument hide_ios", value=hide_ios, expected_type=type_hints["hide_ios"])
            check_type(argname="argument hide_web", value=hide_web, expected_type=type_hints["hide_web"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logo", value=logo, expected_type=type_hints["logo"])
            check_type(argname="argument request_integration", value=request_integration, expected_type=type_hints["request_integration"])
            check_type(argname="argument skip_groups", value=skip_groups, expected_type=type_hints["skip_groups"])
            check_type(argname="argument skip_users", value=skip_users, expected_type=type_hints["skip_users"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if authentication_policy is not None:
            self._values["authentication_policy"] = authentication_policy
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
        if request_integration is not None:
            self._values["request_integration"] = request_integration
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
    def label(self) -> builtins.str:
        '''Pretty name of app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#label BookmarkApp#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#url BookmarkApp#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accessibility_error_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom error page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#accessibility_error_redirect_url BookmarkApp#accessibility_error_redirect_url}
        '''
        result = self._values.get("accessibility_error_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_login_redirect_url(self) -> typing.Optional[builtins.str]:
        '''Custom login page URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#accessibility_login_redirect_url BookmarkApp#accessibility_login_redirect_url}
        '''
        result = self._values.get("accessibility_login_redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accessibility_self_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable self service.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#accessibility_self_service BookmarkApp#accessibility_self_service}
        '''
        result = self._values.get("accessibility_self_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def admin_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for admins.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#admin_note BookmarkApp#admin_note}
        '''
        result = self._values.get("admin_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_links_json(self) -> typing.Optional[builtins.str]:
        '''Displays specific appLinks for the app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#app_links_json BookmarkApp#app_links_json}
        '''
        result = self._values.get("app_links_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_policy(self) -> typing.Optional[builtins.str]:
        '''Id of this apps authentication policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#authentication_policy BookmarkApp#authentication_policy}
        '''
        result = self._values.get("authentication_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_submit_toolbar(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Display auto submit toolbar.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#auto_submit_toolbar BookmarkApp#auto_submit_toolbar}
        '''
        result = self._values.get("auto_submit_toolbar")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enduser_note(self) -> typing.Optional[builtins.str]:
        '''Application notes for end users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#enduser_note BookmarkApp#enduser_note}
        '''
        result = self._values.get("enduser_note")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Groups associated with the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#groups BookmarkApp#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def hide_ios(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon on mobile app.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#hide_ios BookmarkApp#hide_ios}
        '''
        result = self._values.get("hide_ios")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hide_web(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display application icon to users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#hide_web BookmarkApp#hide_web}
        '''
        result = self._values.get("hide_web")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#id BookmarkApp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo(self) -> typing.Optional[builtins.str]:
        '''Local path to logo of the application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#logo BookmarkApp#logo}
        '''
        result = self._values.get("logo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_integration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#request_integration BookmarkApp#request_integration}.'''
        result = self._values.get("request_integration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore groups sync. This is a temporary solution until 'groups' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#skip_groups BookmarkApp#skip_groups}
        '''
        result = self._values.get("skip_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_users(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Ignore users sync. This is a temporary solution until 'users' field is supported in all the app-like resources.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#skip_users BookmarkApp#skip_users}
        '''
        result = self._values.get("skip_users")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#status BookmarkApp#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BookmarkAppTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#timeouts BookmarkApp#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BookmarkAppTimeouts"], result)

    @builtins.property
    def users(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BookmarkAppUsers"]]]:
        '''users block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#users BookmarkApp#users}
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BookmarkAppUsers"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BookmarkAppConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.bookmarkApp.BookmarkAppTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "read": "read", "update": "update"},
)
class BookmarkAppTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#create BookmarkApp#create}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#read BookmarkApp#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#update BookmarkApp#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85349d547b58220ca5b9db0a31cbf0dc8f648c983d035bc21d949c145c30037e)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#create BookmarkApp#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#read BookmarkApp#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#update BookmarkApp#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BookmarkAppTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BookmarkAppTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.bookmarkApp.BookmarkAppTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e9cafb4ea229d5e3d274257a55b1aff6fe9d516cf0d18e573f57a93e48b6e02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d53fd9f87dbbf420d1886840e3db0f59b30e71152bc03b686ccc8735cc38a42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e1c8c69838cd2207fde13de8519e425e28da78b48bd9ccd1eb45388fd3eb80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78bdb11abaf185c463d950bdebb464081051e097e32df049d1e2bc513256c084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[BookmarkAppTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BookmarkAppTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BookmarkAppTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eac63a3c3455ce8cd7e35477a72909d83fa090577629eb9446b864baab0904b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.bookmarkApp.BookmarkAppUsers",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "password": "password", "username": "username"},
)
class BookmarkAppUsers:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: User ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#id BookmarkApp#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param password: Password for user application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#password BookmarkApp#password}
        :param username: Username for user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#username BookmarkApp#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__745459941194085a305c0116b4ad14563718e256c30fdef663c6b2172cdc9e95)
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#id BookmarkApp#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for user application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#password BookmarkApp#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/bookmark_app#username BookmarkApp#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BookmarkAppUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BookmarkAppUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.bookmarkApp.BookmarkAppUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d6c7f8a39a31fc9d464e95985ff9b64ddee6ef74f0f794d3b15b3d9023fc617)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BookmarkAppUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f285759e0ba0e7b5e7b0926dbd361f141fb72ee7da5ad7cc1343ccfbb7e83fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BookmarkAppUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f302e262a1e94188d4e914367d7157b2d60aea384b0e38b8929d0f14323fbf1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__927970bb424e58e8749a64b7f94e19933507b1199c45706701a344a0b366abe3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f23f52ff521e3ce55b4e312f51badb2a394eb2ed6a80fc3cccfe6954aba86205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BookmarkAppUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BookmarkAppUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BookmarkAppUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaaf330dd97ddd96f4c1ce36e291842e04899d0e270d569d0ed2ddb6d5823850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BookmarkAppUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.bookmarkApp.BookmarkAppUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1d13fc7ba50761dc7ddf26b5449456520777b45b847091ffbda4e396877a191)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e70c28a616d7c0e2c24779caac8946671911c84c305ec2e9f9ecc85433bc471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f036b3ab93f16d5fc0a34ab8c7460c1a3ba230d6a61d7b18405b3a5f54511f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7efce7ed4150f904000dee233929b126114428d7e9af653fd1e057d923387a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[BookmarkAppUsers, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BookmarkAppUsers, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BookmarkAppUsers, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500149d4483e121d94eb111f81a1649af1e96d7b9c7e7f5d49ecae2dd5379dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "BookmarkApp",
    "BookmarkAppConfig",
    "BookmarkAppTimeouts",
    "BookmarkAppTimeoutsOutputReference",
    "BookmarkAppUsers",
    "BookmarkAppUsersList",
    "BookmarkAppUsersOutputReference",
]

publication.publish()

def _typecheckingstub__e25e30bff5d9c333ec2086228e3db31071cb348b5c48f6f201b3efb987abb245(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    label: builtins.str,
    url: builtins.str,
    accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    authentication_policy: typing.Optional[builtins.str] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    request_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BookmarkAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BookmarkAppUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__7b865f27f8ebedfb0503876b1d96b1c255f8d5456501a41879903e65b9db8275(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BookmarkAppUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e88caf5c4cfb6e9aba56c230f9eeb499bdd3371a988e664f27003796fd05a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d77f8214f859714047c17d318074e9762c4fce58445bea712195f050df7234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1cb352e337555bd8a4af711dc6429a38fbb54497dbe2168dd5c0034af907c64(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1078db8215ddb172f0c737c4ff90f22209794b0d47f75ebdfcd21f25debb71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d778867aed14c30989098830b6639c70aaf758e73c2e71d0a9de95d0f84e45e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188167a787e41923360ca6cbfeceaafb94c01c3a77d1bf88b1a530ad0bffed64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccb71229860a580f9e97b9414b68953b0cbe347f8e7f779891f2af3ca62dd53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd225d984b90c734840130483828c216498f2a2c259af2d9dcef65b0dabf7198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9ee8f38ded8edc90f2d39138f8bef92275d865d15e9fc039b8e271e5905b23(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a597eb5e5891b94431db8f6c5d2b3bcf373d09ce3a1223c9f92e30a491e719a1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec8e30a7de74298ffee251d37177f371fee9ef5d6fcbc139e4d07de50b7cfbc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d87a5cb5f10fb7909a8b109174a46f27d03b183f9401296de7f02341a4a77a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d661934221d5ebebbb90d8f46f782cfabf1a6e42df0b879ead94487b8382288(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9fd9e13f471b0f40adb13b074c896f90e75ce3fcf24b65d197ed6af3eb5a8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc9cb1a63e530d1e5a2edd8e1cbb431bf97333a52246433a540468dd4697e22(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0991223d707976801e855cbd9617778f3a935a1b6af0d0e4f0836bbb23c903(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7445c03110ef463457d252885d4896881775363f0d7099243ce1c438ac6552b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5ca2cf2dac8c9e5f5ca77be021ff9e6a610626503127e5c35f53a95b59bf01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642dab04c678dd1b008bb7c909612e2a313c60a1f61aeded1dd232de5a97e37a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39d9f42ec53a7bb8f0411ac2b7b3ea0d4ca25e4c363e639861cb3d5f9c32326(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    label: builtins.str,
    url: builtins.str,
    accessibility_error_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_login_redirect_url: typing.Optional[builtins.str] = None,
    accessibility_self_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    admin_note: typing.Optional[builtins.str] = None,
    app_links_json: typing.Optional[builtins.str] = None,
    authentication_policy: typing.Optional[builtins.str] = None,
    auto_submit_toolbar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enduser_note: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    hide_ios: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hide_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logo: typing.Optional[builtins.str] = None,
    request_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BookmarkAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    users: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BookmarkAppUsers, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85349d547b58220ca5b9db0a31cbf0dc8f648c983d035bc21d949c145c30037e(
    *,
    create: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9cafb4ea229d5e3d274257a55b1aff6fe9d516cf0d18e573f57a93e48b6e02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53fd9f87dbbf420d1886840e3db0f59b30e71152bc03b686ccc8735cc38a42b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e1c8c69838cd2207fde13de8519e425e28da78b48bd9ccd1eb45388fd3eb80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78bdb11abaf185c463d950bdebb464081051e097e32df049d1e2bc513256c084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eac63a3c3455ce8cd7e35477a72909d83fa090577629eb9446b864baab0904b(
    value: typing.Optional[typing.Union[BookmarkAppTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__745459941194085a305c0116b4ad14563718e256c30fdef663c6b2172cdc9e95(
    *,
    id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d6c7f8a39a31fc9d464e95985ff9b64ddee6ef74f0f794d3b15b3d9023fc617(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f285759e0ba0e7b5e7b0926dbd361f141fb72ee7da5ad7cc1343ccfbb7e83fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f302e262a1e94188d4e914367d7157b2d60aea384b0e38b8929d0f14323fbf1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927970bb424e58e8749a64b7f94e19933507b1199c45706701a344a0b366abe3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23f52ff521e3ce55b4e312f51badb2a394eb2ed6a80fc3cccfe6954aba86205(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaaf330dd97ddd96f4c1ce36e291842e04899d0e270d569d0ed2ddb6d5823850(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BookmarkAppUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d13fc7ba50761dc7ddf26b5449456520777b45b847091ffbda4e396877a191(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e70c28a616d7c0e2c24779caac8946671911c84c305ec2e9f9ecc85433bc471(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f036b3ab93f16d5fc0a34ab8c7460c1a3ba230d6a61d7b18405b3a5f54511f5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7efce7ed4150f904000dee233929b126114428d7e9af653fd1e057d923387a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500149d4483e121d94eb111f81a1649af1e96d7b9c7e7f5d49ecae2dd5379dac(
    value: typing.Optional[typing.Union[BookmarkAppUsers, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
