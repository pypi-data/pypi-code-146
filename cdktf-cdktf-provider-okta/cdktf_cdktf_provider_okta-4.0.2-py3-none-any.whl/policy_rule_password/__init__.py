'''
# `okta_policy_rule_password`

Refer to the Terraform Registory for docs: [`okta_policy_rule_password`](https://www.terraform.io/docs/providers/okta/r/policy_rule_password).
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


class PolicyRulePassword(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRulePassword.PolicyRulePassword",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password okta_policy_rule_password}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        password_change: typing.Optional[builtins.str] = None,
        password_reset: typing.Optional[builtins.str] = None,
        password_unlock: typing.Optional[builtins.str] = None,
        policyid: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password okta_policy_rule_password} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#name PolicyRulePassword#name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#id PolicyRulePassword#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#network_connection PolicyRulePassword#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#network_excludes PolicyRulePassword#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#network_includes PolicyRulePassword#network_includes}
        :param password_change: Allow or deny a user to change their password: ALLOW or DENY. Default = ALLOW. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#password_change PolicyRulePassword#password_change}
        :param password_reset: Allow or deny a user to reset their password: ALLOW or DENY. Default = ALLOW. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#password_reset PolicyRulePassword#password_reset}
        :param password_unlock: Allow or deny a user to unlock. Default = DENY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#password_unlock PolicyRulePassword#password_unlock}
        :param policyid: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#policyid PolicyRulePassword#policyid}
        :param policy_id: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#policy_id PolicyRulePassword#policy_id}
        :param priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#priority PolicyRulePassword#priority}
        :param status: Policy Rule Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#status PolicyRulePassword#status}
        :param users_excluded: Set of User IDs to Exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#users_excluded PolicyRulePassword#users_excluded}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76951079a41383a1578167df423e053f9c0053036e931ae97dd9d8c6bd55e363)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PolicyRulePasswordConfig(
            name=name,
            id=id,
            network_connection=network_connection,
            network_excludes=network_excludes,
            network_includes=network_includes,
            password_change=password_change,
            password_reset=password_reset,
            password_unlock=password_unlock,
            policyid=policyid,
            policy_id=policy_id,
            priority=priority,
            status=status,
            users_excluded=users_excluded,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNetworkConnection")
    def reset_network_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConnection", []))

    @jsii.member(jsii_name="resetNetworkExcludes")
    def reset_network_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkExcludes", []))

    @jsii.member(jsii_name="resetNetworkIncludes")
    def reset_network_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkIncludes", []))

    @jsii.member(jsii_name="resetPasswordChange")
    def reset_password_change(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordChange", []))

    @jsii.member(jsii_name="resetPasswordReset")
    def reset_password_reset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordReset", []))

    @jsii.member(jsii_name="resetPasswordUnlock")
    def reset_password_unlock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordUnlock", []))

    @jsii.member(jsii_name="resetPolicyid")
    def reset_policyid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyid", []))

    @jsii.member(jsii_name="resetPolicyId")
    def reset_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyId", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetUsersExcluded")
    def reset_users_excluded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsersExcluded", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConnectionInput")
    def network_connection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="networkExcludesInput")
    def network_excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkExcludesInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIncludesInput")
    def network_includes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkIncludesInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordChangeInput")
    def password_change_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordChangeInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordResetInput")
    def password_reset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordResetInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordUnlockInput")
    def password_unlock_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordUnlockInput"))

    @builtins.property
    @jsii.member(jsii_name="policyidInput")
    def policyid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyidInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="usersExcludedInput")
    def users_excluded_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersExcludedInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68be1dacb8508ac556c570017067d8a5405a965caa6e482a5694b0cf478129cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28590d223e2824d5235a2c1ef8650f1e286d95a4c3c096cbf11e425dff0f3150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkConnection")
    def network_connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkConnection"))

    @network_connection.setter
    def network_connection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2594b5bfb299e9d989ac99d2bc1844421c70fd41244017f84b20a64d1fdf4066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConnection", value)

    @builtins.property
    @jsii.member(jsii_name="networkExcludes")
    def network_excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkExcludes"))

    @network_excludes.setter
    def network_excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2421e36f1cb3f9cbdfdeaad42c80340ba554421d7037679b1fcf570c57edb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkExcludes", value)

    @builtins.property
    @jsii.member(jsii_name="networkIncludes")
    def network_includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkIncludes"))

    @network_includes.setter
    def network_includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b06af223cf736b1039b917d56cecf3b10ca581bea7b32b0b85ca213b6cc9c640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIncludes", value)

    @builtins.property
    @jsii.member(jsii_name="passwordChange")
    def password_change(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordChange"))

    @password_change.setter
    def password_change(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f096be21b9652e134e6a1f7eb3b277a2dddadcf724f46204088f96d0511a8ee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordChange", value)

    @builtins.property
    @jsii.member(jsii_name="passwordReset")
    def password_reset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordReset"))

    @password_reset.setter
    def password_reset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934b080ed276098e7e24cf5deb8873a1fc35049baec14838a4d2fc4f3b7224a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordReset", value)

    @builtins.property
    @jsii.member(jsii_name="passwordUnlock")
    def password_unlock(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordUnlock"))

    @password_unlock.setter
    def password_unlock(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8826e9a8a97c1552c183f048e5a5c541a2c1303b9ab3b7c78a14a0074ebf4a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordUnlock", value)

    @builtins.property
    @jsii.member(jsii_name="policyid")
    def policyid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyid"))

    @policyid.setter
    def policyid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa66e9b8db33c3d1faf35834d7661fde19bf8d3d0d2df037a0c9e2047b7532c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyid", value)

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9c8d130ed9966981822c588a560fc57636c310e57b978370491d74e6d8da77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d589d9b252a910476eae18269f6bd62dc110ce9c15b7bd284ffee4ddcf5f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8307b386247ebe9900649dfa8571fb3dce926eb6bf4833bb07756ab47813a461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="usersExcluded")
    def users_excluded(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "usersExcluded"))

    @users_excluded.setter
    def users_excluded(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ffe952aa90ee09b2b63e41a521fdce99e56af59d30ea3b0edf1819cec3e55c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usersExcluded", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRulePassword.PolicyRulePasswordConfig",
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
        "id": "id",
        "network_connection": "networkConnection",
        "network_excludes": "networkExcludes",
        "network_includes": "networkIncludes",
        "password_change": "passwordChange",
        "password_reset": "passwordReset",
        "password_unlock": "passwordUnlock",
        "policyid": "policyid",
        "policy_id": "policyId",
        "priority": "priority",
        "status": "status",
        "users_excluded": "usersExcluded",
    },
)
class PolicyRulePasswordConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        password_change: typing.Optional[builtins.str] = None,
        password_reset: typing.Optional[builtins.str] = None,
        password_unlock: typing.Optional[builtins.str] = None,
        policyid: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#name PolicyRulePassword#name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#id PolicyRulePassword#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#network_connection PolicyRulePassword#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#network_excludes PolicyRulePassword#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#network_includes PolicyRulePassword#network_includes}
        :param password_change: Allow or deny a user to change their password: ALLOW or DENY. Default = ALLOW. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#password_change PolicyRulePassword#password_change}
        :param password_reset: Allow or deny a user to reset their password: ALLOW or DENY. Default = ALLOW. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#password_reset PolicyRulePassword#password_reset}
        :param password_unlock: Allow or deny a user to unlock. Default = DENY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#password_unlock PolicyRulePassword#password_unlock}
        :param policyid: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#policyid PolicyRulePassword#policyid}
        :param policy_id: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#policy_id PolicyRulePassword#policy_id}
        :param priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#priority PolicyRulePassword#priority}
        :param status: Policy Rule Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#status PolicyRulePassword#status}
        :param users_excluded: Set of User IDs to Exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#users_excluded PolicyRulePassword#users_excluded}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b067ab25cf94d9babf5b30b73d4531971c60d18ae5bbacebf3d86344e6273fbe)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument network_connection", value=network_connection, expected_type=type_hints["network_connection"])
            check_type(argname="argument network_excludes", value=network_excludes, expected_type=type_hints["network_excludes"])
            check_type(argname="argument network_includes", value=network_includes, expected_type=type_hints["network_includes"])
            check_type(argname="argument password_change", value=password_change, expected_type=type_hints["password_change"])
            check_type(argname="argument password_reset", value=password_reset, expected_type=type_hints["password_reset"])
            check_type(argname="argument password_unlock", value=password_unlock, expected_type=type_hints["password_unlock"])
            check_type(argname="argument policyid", value=policyid, expected_type=type_hints["policyid"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument users_excluded", value=users_excluded, expected_type=type_hints["users_excluded"])
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
        if id is not None:
            self._values["id"] = id
        if network_connection is not None:
            self._values["network_connection"] = network_connection
        if network_excludes is not None:
            self._values["network_excludes"] = network_excludes
        if network_includes is not None:
            self._values["network_includes"] = network_includes
        if password_change is not None:
            self._values["password_change"] = password_change
        if password_reset is not None:
            self._values["password_reset"] = password_reset
        if password_unlock is not None:
            self._values["password_unlock"] = password_unlock
        if policyid is not None:
            self._values["policyid"] = policyid
        if policy_id is not None:
            self._values["policy_id"] = policy_id
        if priority is not None:
            self._values["priority"] = priority
        if status is not None:
            self._values["status"] = status
        if users_excluded is not None:
            self._values["users_excluded"] = users_excluded

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
        '''Policy Rule Name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#name PolicyRulePassword#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#id PolicyRulePassword#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_connection(self) -> typing.Optional[builtins.str]:
        '''Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#network_connection PolicyRulePassword#network_connection}
        '''
        result = self._values.get("network_connection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#network_excludes PolicyRulePassword#network_excludes}
        '''
        result = self._values.get("network_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#network_includes PolicyRulePassword#network_includes}
        '''
        result = self._values.get("network_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def password_change(self) -> typing.Optional[builtins.str]:
        '''Allow or deny a user to change their password: ALLOW or DENY. Default = ALLOW.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#password_change PolicyRulePassword#password_change}
        '''
        result = self._values.get("password_change")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_reset(self) -> typing.Optional[builtins.str]:
        '''Allow or deny a user to reset their password: ALLOW or DENY. Default = ALLOW.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#password_reset PolicyRulePassword#password_reset}
        '''
        result = self._values.get("password_reset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_unlock(self) -> typing.Optional[builtins.str]:
        '''Allow or deny a user to unlock. Default = DENY.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#password_unlock PolicyRulePassword#password_unlock}
        '''
        result = self._values.get("password_unlock")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policyid(self) -> typing.Optional[builtins.str]:
        '''Policy ID of the Rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#policyid PolicyRulePassword#policyid}
        '''
        result = self._values.get("policyid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''Policy ID of the Rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#policy_id PolicyRulePassword#policy_id}
        '''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Policy Rule Priority, this attribute can be set to a valid priority.

        To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#priority PolicyRulePassword#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Policy Rule Status: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#status PolicyRulePassword#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users_excluded(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of User IDs to Exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_password#users_excluded PolicyRulePassword#users_excluded}
        '''
        result = self._values.get("users_excluded")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRulePasswordConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PolicyRulePassword",
    "PolicyRulePasswordConfig",
]

publication.publish()

def _typecheckingstub__76951079a41383a1578167df423e053f9c0053036e931ae97dd9d8c6bd55e363(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    network_connection: typing.Optional[builtins.str] = None,
    network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    password_change: typing.Optional[builtins.str] = None,
    password_reset: typing.Optional[builtins.str] = None,
    password_unlock: typing.Optional[builtins.str] = None,
    policyid: typing.Optional[builtins.str] = None,
    policy_id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__68be1dacb8508ac556c570017067d8a5405a965caa6e482a5694b0cf478129cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28590d223e2824d5235a2c1ef8650f1e286d95a4c3c096cbf11e425dff0f3150(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2594b5bfb299e9d989ac99d2bc1844421c70fd41244017f84b20a64d1fdf4066(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2421e36f1cb3f9cbdfdeaad42c80340ba554421d7037679b1fcf570c57edb9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06af223cf736b1039b917d56cecf3b10ca581bea7b32b0b85ca213b6cc9c640(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f096be21b9652e134e6a1f7eb3b277a2dddadcf724f46204088f96d0511a8ee2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934b080ed276098e7e24cf5deb8873a1fc35049baec14838a4d2fc4f3b7224a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8826e9a8a97c1552c183f048e5a5c541a2c1303b9ab3b7c78a14a0074ebf4a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa66e9b8db33c3d1faf35834d7661fde19bf8d3d0d2df037a0c9e2047b7532c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9c8d130ed9966981822c588a560fc57636c310e57b978370491d74e6d8da77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d589d9b252a910476eae18269f6bd62dc110ce9c15b7bd284ffee4ddcf5f17(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8307b386247ebe9900649dfa8571fb3dce926eb6bf4833bb07756ab47813a461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ffe952aa90ee09b2b63e41a521fdce99e56af59d30ea3b0edf1819cec3e55c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b067ab25cf94d9babf5b30b73d4531971c60d18ae5bbacebf3d86344e6273fbe(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    network_connection: typing.Optional[builtins.str] = None,
    network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    password_change: typing.Optional[builtins.str] = None,
    password_reset: typing.Optional[builtins.str] = None,
    password_unlock: typing.Optional[builtins.str] = None,
    policyid: typing.Optional[builtins.str] = None,
    policy_id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
