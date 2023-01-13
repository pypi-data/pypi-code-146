'''
# `okta_auth_server_policy_rule`

Refer to the Terraform Registory for docs: [`okta_auth_server_policy_rule`](https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule).
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


class AuthServerPolicyRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.authServerPolicyRule.AuthServerPolicyRule",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule okta_auth_server_policy_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        auth_server_id: builtins.str,
        grant_type_whitelist: typing.Sequence[builtins.str],
        name: builtins.str,
        policy_id: builtins.str,
        priority: jsii.Number,
        access_token_lifetime_minutes: typing.Optional[jsii.Number] = None,
        group_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        inline_hook_id: typing.Optional[builtins.str] = None,
        refresh_token_lifetime_minutes: typing.Optional[jsii.Number] = None,
        refresh_token_window_minutes: typing.Optional[jsii.Number] = None,
        scope_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        user_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule okta_auth_server_policy_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auth_server_id: Auth server ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#auth_server_id AuthServerPolicyRule#auth_server_id}
        :param grant_type_whitelist: Accepted grant type values: authorization_code, implicit, password, client_credentials. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#grant_type_whitelist AuthServerPolicyRule#grant_type_whitelist}
        :param name: Auth server policy rule name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#name AuthServerPolicyRule#name}
        :param policy_id: Auth server policy ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#policy_id AuthServerPolicyRule#policy_id}
        :param priority: Priority of the auth server policy rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#priority AuthServerPolicyRule#priority}
        :param access_token_lifetime_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#access_token_lifetime_minutes AuthServerPolicyRule#access_token_lifetime_minutes}.
        :param group_blacklist: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#group_blacklist AuthServerPolicyRule#group_blacklist}.
        :param group_whitelist: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#group_whitelist AuthServerPolicyRule#group_whitelist}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#id AuthServerPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inline_hook_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#inline_hook_id AuthServerPolicyRule#inline_hook_id}.
        :param refresh_token_lifetime_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#refresh_token_lifetime_minutes AuthServerPolicyRule#refresh_token_lifetime_minutes}.
        :param refresh_token_window_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#refresh_token_window_minutes AuthServerPolicyRule#refresh_token_window_minutes}.
        :param scope_whitelist: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#scope_whitelist AuthServerPolicyRule#scope_whitelist}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#status AuthServerPolicyRule#status}.
        :param type: Auth server policy rule type, unlikely this will be anything other then the default. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#type AuthServerPolicyRule#type}
        :param user_blacklist: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#user_blacklist AuthServerPolicyRule#user_blacklist}.
        :param user_whitelist: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#user_whitelist AuthServerPolicyRule#user_whitelist}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f491c178b43542b2cc9690eea1b40bab32aee1fd957197ff00e93309da96e739)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AuthServerPolicyRuleConfig(
            auth_server_id=auth_server_id,
            grant_type_whitelist=grant_type_whitelist,
            name=name,
            policy_id=policy_id,
            priority=priority,
            access_token_lifetime_minutes=access_token_lifetime_minutes,
            group_blacklist=group_blacklist,
            group_whitelist=group_whitelist,
            id=id,
            inline_hook_id=inline_hook_id,
            refresh_token_lifetime_minutes=refresh_token_lifetime_minutes,
            refresh_token_window_minutes=refresh_token_window_minutes,
            scope_whitelist=scope_whitelist,
            status=status,
            type=type,
            user_blacklist=user_blacklist,
            user_whitelist=user_whitelist,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAccessTokenLifetimeMinutes")
    def reset_access_token_lifetime_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessTokenLifetimeMinutes", []))

    @jsii.member(jsii_name="resetGroupBlacklist")
    def reset_group_blacklist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupBlacklist", []))

    @jsii.member(jsii_name="resetGroupWhitelist")
    def reset_group_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupWhitelist", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInlineHookId")
    def reset_inline_hook_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInlineHookId", []))

    @jsii.member(jsii_name="resetRefreshTokenLifetimeMinutes")
    def reset_refresh_token_lifetime_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshTokenLifetimeMinutes", []))

    @jsii.member(jsii_name="resetRefreshTokenWindowMinutes")
    def reset_refresh_token_window_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshTokenWindowMinutes", []))

    @jsii.member(jsii_name="resetScopeWhitelist")
    def reset_scope_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopeWhitelist", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUserBlacklist")
    def reset_user_blacklist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserBlacklist", []))

    @jsii.member(jsii_name="resetUserWhitelist")
    def reset_user_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserWhitelist", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenLifetimeMinutesInput")
    def access_token_lifetime_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accessTokenLifetimeMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="authServerIdInput")
    def auth_server_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authServerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="grantTypeWhitelistInput")
    def grant_type_whitelist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "grantTypeWhitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="groupBlacklistInput")
    def group_blacklist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupBlacklistInput"))

    @builtins.property
    @jsii.member(jsii_name="groupWhitelistInput")
    def group_whitelist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupWhitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inlineHookIdInput")
    def inline_hook_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inlineHookIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenLifetimeMinutesInput")
    def refresh_token_lifetime_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "refreshTokenLifetimeMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenWindowMinutesInput")
    def refresh_token_window_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "refreshTokenWindowMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeWhitelistInput")
    def scope_whitelist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopeWhitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userBlacklistInput")
    def user_blacklist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userBlacklistInput"))

    @builtins.property
    @jsii.member(jsii_name="userWhitelistInput")
    def user_whitelist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userWhitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenLifetimeMinutes")
    def access_token_lifetime_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accessTokenLifetimeMinutes"))

    @access_token_lifetime_minutes.setter
    def access_token_lifetime_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f1c68af8833ebc31babb52bfa8c21b87abd2a720801dfa851276d41630feed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessTokenLifetimeMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="authServerId")
    def auth_server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authServerId"))

    @auth_server_id.setter
    def auth_server_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353eb6e6741c6526ac1cbe86f9e6d2de05260bd95238cf62a2c152e899524930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authServerId", value)

    @builtins.property
    @jsii.member(jsii_name="grantTypeWhitelist")
    def grant_type_whitelist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "grantTypeWhitelist"))

    @grant_type_whitelist.setter
    def grant_type_whitelist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36be65d34c7f21bbb920a2fee80645158c4708a1f965fb9a833b5e74518814ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grantTypeWhitelist", value)

    @builtins.property
    @jsii.member(jsii_name="groupBlacklist")
    def group_blacklist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupBlacklist"))

    @group_blacklist.setter
    def group_blacklist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3930e82b5ef38123e28b8ad4f1ffdc2430e81dc5fe736d044132416b8d47acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupBlacklist", value)

    @builtins.property
    @jsii.member(jsii_name="groupWhitelist")
    def group_whitelist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupWhitelist"))

    @group_whitelist.setter
    def group_whitelist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c3d2bbf5728378fbd5c336d054a441a9951a5d3a3b092fab8fe2bc317b5bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupWhitelist", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6a210ad9956217f2f5ace61d92ba605309950c8c6cc1cea6efd56b4a4309bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="inlineHookId")
    def inline_hook_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inlineHookId"))

    @inline_hook_id.setter
    def inline_hook_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21dde854f1b183bd92fa987b1b8e2188390fc270c97b51b598a135ba6038e99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inlineHookId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25bfe309d0ffc70175c0e5816a24a8e3926d59357a26f4fe7d94dba46dc7e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c721a2ad21dae63ccef6ba73b28f6dc60779e90d89e3b0a18c91d8b13cb792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b612f6cddde5f8024063f1eb682edd62cf73c90b00a670a0ba4ef37bdb35ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="refreshTokenLifetimeMinutes")
    def refresh_token_lifetime_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "refreshTokenLifetimeMinutes"))

    @refresh_token_lifetime_minutes.setter
    def refresh_token_lifetime_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0697ece5bddb6ae3999e55f90a1c238f3510b887bedc9cb6818f57ffa558b900)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshTokenLifetimeMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="refreshTokenWindowMinutes")
    def refresh_token_window_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "refreshTokenWindowMinutes"))

    @refresh_token_window_minutes.setter
    def refresh_token_window_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332a3fdc6bbc84761a4b0d0667d20d0a6d5526f492251e4fb02f6b21a4c5d261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshTokenWindowMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="scopeWhitelist")
    def scope_whitelist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopeWhitelist"))

    @scope_whitelist.setter
    def scope_whitelist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e38da81a7677517559f7d87d2c02bf909fc40c22a5e067e7516576d68367e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeWhitelist", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5196583c1f82fa59abaa6f01121b6dabde7aff0d30e9e7d71c128bbea2a5bd8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0b647d084e64622ab0b945c943c7238c9ac5196dc57b342b63c1a8749a50910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="userBlacklist")
    def user_blacklist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userBlacklist"))

    @user_blacklist.setter
    def user_blacklist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6cca68bcb0a7125a8077dd54874542778ba920184aba4e35788b3c41526b9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userBlacklist", value)

    @builtins.property
    @jsii.member(jsii_name="userWhitelist")
    def user_whitelist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userWhitelist"))

    @user_whitelist.setter
    def user_whitelist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4fb999c0446d3f186de00d65960174678fc7e020bdd9b4d81d60e056838a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userWhitelist", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.authServerPolicyRule.AuthServerPolicyRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "auth_server_id": "authServerId",
        "grant_type_whitelist": "grantTypeWhitelist",
        "name": "name",
        "policy_id": "policyId",
        "priority": "priority",
        "access_token_lifetime_minutes": "accessTokenLifetimeMinutes",
        "group_blacklist": "groupBlacklist",
        "group_whitelist": "groupWhitelist",
        "id": "id",
        "inline_hook_id": "inlineHookId",
        "refresh_token_lifetime_minutes": "refreshTokenLifetimeMinutes",
        "refresh_token_window_minutes": "refreshTokenWindowMinutes",
        "scope_whitelist": "scopeWhitelist",
        "status": "status",
        "type": "type",
        "user_blacklist": "userBlacklist",
        "user_whitelist": "userWhitelist",
    },
)
class AuthServerPolicyRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auth_server_id: builtins.str,
        grant_type_whitelist: typing.Sequence[builtins.str],
        name: builtins.str,
        policy_id: builtins.str,
        priority: jsii.Number,
        access_token_lifetime_minutes: typing.Optional[jsii.Number] = None,
        group_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        inline_hook_id: typing.Optional[builtins.str] = None,
        refresh_token_lifetime_minutes: typing.Optional[jsii.Number] = None,
        refresh_token_window_minutes: typing.Optional[jsii.Number] = None,
        scope_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        user_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param auth_server_id: Auth server ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#auth_server_id AuthServerPolicyRule#auth_server_id}
        :param grant_type_whitelist: Accepted grant type values: authorization_code, implicit, password, client_credentials. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#grant_type_whitelist AuthServerPolicyRule#grant_type_whitelist}
        :param name: Auth server policy rule name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#name AuthServerPolicyRule#name}
        :param policy_id: Auth server policy ID. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#policy_id AuthServerPolicyRule#policy_id}
        :param priority: Priority of the auth server policy rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#priority AuthServerPolicyRule#priority}
        :param access_token_lifetime_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#access_token_lifetime_minutes AuthServerPolicyRule#access_token_lifetime_minutes}.
        :param group_blacklist: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#group_blacklist AuthServerPolicyRule#group_blacklist}.
        :param group_whitelist: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#group_whitelist AuthServerPolicyRule#group_whitelist}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#id AuthServerPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inline_hook_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#inline_hook_id AuthServerPolicyRule#inline_hook_id}.
        :param refresh_token_lifetime_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#refresh_token_lifetime_minutes AuthServerPolicyRule#refresh_token_lifetime_minutes}.
        :param refresh_token_window_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#refresh_token_window_minutes AuthServerPolicyRule#refresh_token_window_minutes}.
        :param scope_whitelist: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#scope_whitelist AuthServerPolicyRule#scope_whitelist}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#status AuthServerPolicyRule#status}.
        :param type: Auth server policy rule type, unlikely this will be anything other then the default. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#type AuthServerPolicyRule#type}
        :param user_blacklist: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#user_blacklist AuthServerPolicyRule#user_blacklist}.
        :param user_whitelist: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#user_whitelist AuthServerPolicyRule#user_whitelist}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b8e0bcfb4bd482d0904ca992643ca3cd64f49ee705d4ff7275b913c9c8cb36)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument auth_server_id", value=auth_server_id, expected_type=type_hints["auth_server_id"])
            check_type(argname="argument grant_type_whitelist", value=grant_type_whitelist, expected_type=type_hints["grant_type_whitelist"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument access_token_lifetime_minutes", value=access_token_lifetime_minutes, expected_type=type_hints["access_token_lifetime_minutes"])
            check_type(argname="argument group_blacklist", value=group_blacklist, expected_type=type_hints["group_blacklist"])
            check_type(argname="argument group_whitelist", value=group_whitelist, expected_type=type_hints["group_whitelist"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inline_hook_id", value=inline_hook_id, expected_type=type_hints["inline_hook_id"])
            check_type(argname="argument refresh_token_lifetime_minutes", value=refresh_token_lifetime_minutes, expected_type=type_hints["refresh_token_lifetime_minutes"])
            check_type(argname="argument refresh_token_window_minutes", value=refresh_token_window_minutes, expected_type=type_hints["refresh_token_window_minutes"])
            check_type(argname="argument scope_whitelist", value=scope_whitelist, expected_type=type_hints["scope_whitelist"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_blacklist", value=user_blacklist, expected_type=type_hints["user_blacklist"])
            check_type(argname="argument user_whitelist", value=user_whitelist, expected_type=type_hints["user_whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_server_id": auth_server_id,
            "grant_type_whitelist": grant_type_whitelist,
            "name": name,
            "policy_id": policy_id,
            "priority": priority,
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
        if access_token_lifetime_minutes is not None:
            self._values["access_token_lifetime_minutes"] = access_token_lifetime_minutes
        if group_blacklist is not None:
            self._values["group_blacklist"] = group_blacklist
        if group_whitelist is not None:
            self._values["group_whitelist"] = group_whitelist
        if id is not None:
            self._values["id"] = id
        if inline_hook_id is not None:
            self._values["inline_hook_id"] = inline_hook_id
        if refresh_token_lifetime_minutes is not None:
            self._values["refresh_token_lifetime_minutes"] = refresh_token_lifetime_minutes
        if refresh_token_window_minutes is not None:
            self._values["refresh_token_window_minutes"] = refresh_token_window_minutes
        if scope_whitelist is not None:
            self._values["scope_whitelist"] = scope_whitelist
        if status is not None:
            self._values["status"] = status
        if type is not None:
            self._values["type"] = type
        if user_blacklist is not None:
            self._values["user_blacklist"] = user_blacklist
        if user_whitelist is not None:
            self._values["user_whitelist"] = user_whitelist

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
    def auth_server_id(self) -> builtins.str:
        '''Auth server ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#auth_server_id AuthServerPolicyRule#auth_server_id}
        '''
        result = self._values.get("auth_server_id")
        assert result is not None, "Required property 'auth_server_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def grant_type_whitelist(self) -> typing.List[builtins.str]:
        '''Accepted grant type values: authorization_code, implicit, password, client_credentials.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#grant_type_whitelist AuthServerPolicyRule#grant_type_whitelist}
        '''
        result = self._values.get("grant_type_whitelist")
        assert result is not None, "Required property 'grant_type_whitelist' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Auth server policy rule name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#name AuthServerPolicyRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''Auth server policy ID.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#policy_id AuthServerPolicyRule#policy_id}
        '''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Priority of the auth server policy rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#priority AuthServerPolicyRule#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def access_token_lifetime_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#access_token_lifetime_minutes AuthServerPolicyRule#access_token_lifetime_minutes}.'''
        result = self._values.get("access_token_lifetime_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def group_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#group_blacklist AuthServerPolicyRule#group_blacklist}.'''
        result = self._values.get("group_blacklist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def group_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#group_whitelist AuthServerPolicyRule#group_whitelist}.'''
        result = self._values.get("group_whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#id AuthServerPolicyRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_hook_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#inline_hook_id AuthServerPolicyRule#inline_hook_id}.'''
        result = self._values.get("inline_hook_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def refresh_token_lifetime_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#refresh_token_lifetime_minutes AuthServerPolicyRule#refresh_token_lifetime_minutes}.'''
        result = self._values.get("refresh_token_lifetime_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def refresh_token_window_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#refresh_token_window_minutes AuthServerPolicyRule#refresh_token_window_minutes}.'''
        result = self._values.get("refresh_token_window_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scope_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#scope_whitelist AuthServerPolicyRule#scope_whitelist}.'''
        result = self._values.get("scope_whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#status AuthServerPolicyRule#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Auth server policy rule type, unlikely this will be anything other then the default.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#type AuthServerPolicyRule#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_blacklist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#user_blacklist AuthServerPolicyRule#user_blacklist}.'''
        result = self._values.get("user_blacklist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/auth_server_policy_rule#user_whitelist AuthServerPolicyRule#user_whitelist}.'''
        result = self._values.get("user_whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthServerPolicyRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AuthServerPolicyRule",
    "AuthServerPolicyRuleConfig",
]

publication.publish()

def _typecheckingstub__f491c178b43542b2cc9690eea1b40bab32aee1fd957197ff00e93309da96e739(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    auth_server_id: builtins.str,
    grant_type_whitelist: typing.Sequence[builtins.str],
    name: builtins.str,
    policy_id: builtins.str,
    priority: jsii.Number,
    access_token_lifetime_minutes: typing.Optional[jsii.Number] = None,
    group_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    inline_hook_id: typing.Optional[builtins.str] = None,
    refresh_token_lifetime_minutes: typing.Optional[jsii.Number] = None,
    refresh_token_window_minutes: typing.Optional[jsii.Number] = None,
    scope_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__42f1c68af8833ebc31babb52bfa8c21b87abd2a720801dfa851276d41630feed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353eb6e6741c6526ac1cbe86f9e6d2de05260bd95238cf62a2c152e899524930(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36be65d34c7f21bbb920a2fee80645158c4708a1f965fb9a833b5e74518814ce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3930e82b5ef38123e28b8ad4f1ffdc2430e81dc5fe736d044132416b8d47acb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c3d2bbf5728378fbd5c336d054a441a9951a5d3a3b092fab8fe2bc317b5bc5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6a210ad9956217f2f5ace61d92ba605309950c8c6cc1cea6efd56b4a4309bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21dde854f1b183bd92fa987b1b8e2188390fc270c97b51b598a135ba6038e99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25bfe309d0ffc70175c0e5816a24a8e3926d59357a26f4fe7d94dba46dc7e7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c721a2ad21dae63ccef6ba73b28f6dc60779e90d89e3b0a18c91d8b13cb792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b612f6cddde5f8024063f1eb682edd62cf73c90b00a670a0ba4ef37bdb35ac7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0697ece5bddb6ae3999e55f90a1c238f3510b887bedc9cb6818f57ffa558b900(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332a3fdc6bbc84761a4b0d0667d20d0a6d5526f492251e4fb02f6b21a4c5d261(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e38da81a7677517559f7d87d2c02bf909fc40c22a5e067e7516576d68367e0e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5196583c1f82fa59abaa6f01121b6dabde7aff0d30e9e7d71c128bbea2a5bd8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b647d084e64622ab0b945c943c7238c9ac5196dc57b342b63c1a8749a50910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6cca68bcb0a7125a8077dd54874542778ba920184aba4e35788b3c41526b9e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4fb999c0446d3f186de00d65960174678fc7e020bdd9b4d81d60e056838a7b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b8e0bcfb4bd482d0904ca992643ca3cd64f49ee705d4ff7275b913c9c8cb36(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_server_id: builtins.str,
    grant_type_whitelist: typing.Sequence[builtins.str],
    name: builtins.str,
    policy_id: builtins.str,
    priority: jsii.Number,
    access_token_lifetime_minutes: typing.Optional[jsii.Number] = None,
    group_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    inline_hook_id: typing.Optional[builtins.str] = None,
    refresh_token_lifetime_minutes: typing.Optional[jsii.Number] = None,
    refresh_token_window_minutes: typing.Optional[jsii.Number] = None,
    scope_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_blacklist: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
