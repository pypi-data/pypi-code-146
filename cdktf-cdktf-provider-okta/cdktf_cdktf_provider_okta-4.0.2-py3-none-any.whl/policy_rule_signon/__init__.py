'''
# `okta_policy_rule_signon`

Refer to the Terraform Registory for docs: [`okta_policy_rule_signon`](https://www.terraform.io/docs/providers/okta/r/policy_rule_signon).
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


class PolicyRuleSignon(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleSignon.PolicyRuleSignon",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon okta_policy_rule_signon}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        access: typing.Optional[builtins.str] = None,
        authtype: typing.Optional[builtins.str] = None,
        behaviors: typing.Optional[typing.Sequence[builtins.str]] = None,
        factor_sequence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleSignonFactorSequence", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity_provider: typing.Optional[builtins.str] = None,
        identity_provider_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        mfa_lifetime: typing.Optional[jsii.Number] = None,
        mfa_prompt: typing.Optional[builtins.str] = None,
        mfa_remember_device: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mfa_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        policyid: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
        primary_factor: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        risc_level: typing.Optional[builtins.str] = None,
        session_idle: typing.Optional[jsii.Number] = None,
        session_lifetime: typing.Optional[jsii.Number] = None,
        session_persistent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon okta_policy_rule_signon} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#name PolicyRuleSignon#name}
        :param access: Allow or deny access based on the rule conditions: ALLOW, DENY or CHALLENGE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#access PolicyRuleSignon#access}
        :param authtype: Authentication entrypoint: ANY, RADIUS or LDAP_INTERFACE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#authtype PolicyRuleSignon#authtype}
        :param behaviors: List of behavior IDs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#behaviors PolicyRuleSignon#behaviors}
        :param factor_sequence: factor_sequence block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#factor_sequence PolicyRuleSignon#factor_sequence}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#id PolicyRuleSignon#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_provider: Apply rule based on the IdP used: ANY, OKTA or SPECIFIC_IDP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#identity_provider PolicyRuleSignon#identity_provider}
        :param identity_provider_ids: When identity_provider is SPECIFIC_IDP then this is the list of IdP IDs to apply the rule on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#identity_provider_ids PolicyRuleSignon#identity_provider_ids}
        :param mfa_lifetime: Elapsed time before the next MFA challenge. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_lifetime PolicyRuleSignon#mfa_lifetime}
        :param mfa_prompt: Prompt for MFA based on the device used, a factor session lifetime, or every sign-on attempt: DEVICE, SESSION or ALWAYS. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_prompt PolicyRuleSignon#mfa_prompt}
        :param mfa_remember_device: Remember MFA device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_remember_device PolicyRuleSignon#mfa_remember_device}
        :param mfa_required: Require MFA. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_required PolicyRuleSignon#mfa_required}
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#network_connection PolicyRuleSignon#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#network_excludes PolicyRuleSignon#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#network_includes PolicyRuleSignon#network_includes}
        :param policyid: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#policyid PolicyRuleSignon#policyid}
        :param policy_id: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#policy_id PolicyRuleSignon#policy_id}
        :param primary_factor: Primary factor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#primary_factor PolicyRuleSignon#primary_factor}
        :param priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#priority PolicyRuleSignon#priority}
        :param risc_level: Risc level: ANY, LOW, MEDIUM or HIGH. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#risc_level PolicyRuleSignon#risc_level}
        :param session_idle: Max minutes a session can be idle. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#session_idle PolicyRuleSignon#session_idle}
        :param session_lifetime: Max minutes a session is active: Disable = 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#session_lifetime PolicyRuleSignon#session_lifetime}
        :param session_persistent: Whether session cookies will last across browser sessions. Okta Administrators can never have persistent session cookies. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#session_persistent PolicyRuleSignon#session_persistent}
        :param status: Policy Rule Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#status PolicyRuleSignon#status}
        :param users_excluded: Set of User IDs to Exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#users_excluded PolicyRuleSignon#users_excluded}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c7dab4c858bb5fcb91fbce5de2897ecd43f20622a2a7348ad760d180600d655)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PolicyRuleSignonConfig(
            name=name,
            access=access,
            authtype=authtype,
            behaviors=behaviors,
            factor_sequence=factor_sequence,
            id=id,
            identity_provider=identity_provider,
            identity_provider_ids=identity_provider_ids,
            mfa_lifetime=mfa_lifetime,
            mfa_prompt=mfa_prompt,
            mfa_remember_device=mfa_remember_device,
            mfa_required=mfa_required,
            network_connection=network_connection,
            network_excludes=network_excludes,
            network_includes=network_includes,
            policyid=policyid,
            policy_id=policy_id,
            primary_factor=primary_factor,
            priority=priority,
            risc_level=risc_level,
            session_idle=session_idle,
            session_lifetime=session_lifetime,
            session_persistent=session_persistent,
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

    @jsii.member(jsii_name="putFactorSequence")
    def put_factor_sequence(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleSignonFactorSequence", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4544907223bf4380c1095e612e25358e16c325ffe5e61c53e669f297a003873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFactorSequence", [value]))

    @jsii.member(jsii_name="resetAccess")
    def reset_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccess", []))

    @jsii.member(jsii_name="resetAuthtype")
    def reset_authtype(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthtype", []))

    @jsii.member(jsii_name="resetBehaviors")
    def reset_behaviors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBehaviors", []))

    @jsii.member(jsii_name="resetFactorSequence")
    def reset_factor_sequence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFactorSequence", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentityProvider")
    def reset_identity_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProvider", []))

    @jsii.member(jsii_name="resetIdentityProviderIds")
    def reset_identity_provider_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderIds", []))

    @jsii.member(jsii_name="resetMfaLifetime")
    def reset_mfa_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMfaLifetime", []))

    @jsii.member(jsii_name="resetMfaPrompt")
    def reset_mfa_prompt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMfaPrompt", []))

    @jsii.member(jsii_name="resetMfaRememberDevice")
    def reset_mfa_remember_device(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMfaRememberDevice", []))

    @jsii.member(jsii_name="resetMfaRequired")
    def reset_mfa_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMfaRequired", []))

    @jsii.member(jsii_name="resetNetworkConnection")
    def reset_network_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConnection", []))

    @jsii.member(jsii_name="resetNetworkExcludes")
    def reset_network_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkExcludes", []))

    @jsii.member(jsii_name="resetNetworkIncludes")
    def reset_network_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkIncludes", []))

    @jsii.member(jsii_name="resetPolicyid")
    def reset_policyid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyid", []))

    @jsii.member(jsii_name="resetPolicyId")
    def reset_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyId", []))

    @jsii.member(jsii_name="resetPrimaryFactor")
    def reset_primary_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryFactor", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetRiscLevel")
    def reset_risc_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRiscLevel", []))

    @jsii.member(jsii_name="resetSessionIdle")
    def reset_session_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionIdle", []))

    @jsii.member(jsii_name="resetSessionLifetime")
    def reset_session_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionLifetime", []))

    @jsii.member(jsii_name="resetSessionPersistent")
    def reset_session_persistent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionPersistent", []))

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
    @jsii.member(jsii_name="factorSequence")
    def factor_sequence(self) -> "PolicyRuleSignonFactorSequenceList":
        return typing.cast("PolicyRuleSignonFactorSequenceList", jsii.get(self, "factorSequence"))

    @builtins.property
    @jsii.member(jsii_name="accessInput")
    def access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessInput"))

    @builtins.property
    @jsii.member(jsii_name="authtypeInput")
    def authtype_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authtypeInput"))

    @builtins.property
    @jsii.member(jsii_name="behaviorsInput")
    def behaviors_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "behaviorsInput"))

    @builtins.property
    @jsii.member(jsii_name="factorSequenceInput")
    def factor_sequence_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleSignonFactorSequence"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleSignonFactorSequence"]]], jsii.get(self, "factorSequenceInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdsInput")
    def identity_provider_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityProviderIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderInput")
    def identity_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mfaLifetimeInput")
    def mfa_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mfaLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="mfaPromptInput")
    def mfa_prompt_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mfaPromptInput"))

    @builtins.property
    @jsii.member(jsii_name="mfaRememberDeviceInput")
    def mfa_remember_device_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mfaRememberDeviceInput"))

    @builtins.property
    @jsii.member(jsii_name="mfaRequiredInput")
    def mfa_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mfaRequiredInput"))

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
    @jsii.member(jsii_name="policyidInput")
    def policyid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyidInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryFactorInput")
    def primary_factor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="riscLevelInput")
    def risc_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "riscLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionIdleInput")
    def session_idle_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionIdleInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionLifetimeInput")
    def session_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionPersistentInput")
    def session_persistent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sessionPersistentInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="usersExcludedInput")
    def users_excluded_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersExcludedInput"))

    @builtins.property
    @jsii.member(jsii_name="access")
    def access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "access"))

    @access.setter
    def access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056e808cc46b6d12a753e27ff5efdad15c6af4fdccb173e54f756c50838b1e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "access", value)

    @builtins.property
    @jsii.member(jsii_name="authtype")
    def authtype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authtype"))

    @authtype.setter
    def authtype(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53db46318bf02055b28679869842400045637065a50adf1d419c1633ed1eb2f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authtype", value)

    @builtins.property
    @jsii.member(jsii_name="behaviors")
    def behaviors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "behaviors"))

    @behaviors.setter
    def behaviors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d411844117af646e085530bdf26caa834468b76e6f89d2202e75e5482a333947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behaviors", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59716bd2160a1cf8dec878a487fb6985f74a2a1963df42a633152cda95aee581)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="identityProvider")
    def identity_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProvider"))

    @identity_provider.setter
    def identity_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a22ef93fce4294dcf837d53018663d7d3b871200ccdb62f1fb77d3934b761fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProvider", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderIds")
    def identity_provider_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityProviderIds"))

    @identity_provider_ids.setter
    def identity_provider_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1334a4d52a19b0b8d5b38e6cf44a2de965599f3756d13e507b62f0cdb2097648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderIds", value)

    @builtins.property
    @jsii.member(jsii_name="mfaLifetime")
    def mfa_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mfaLifetime"))

    @mfa_lifetime.setter
    def mfa_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75e685970f951104813180afe74d704c45ed1f3953f77cc0c2d51df42086ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mfaLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="mfaPrompt")
    def mfa_prompt(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mfaPrompt"))

    @mfa_prompt.setter
    def mfa_prompt(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f75bbc087898b75faad185c2fca39ad1ed5d348cafce89c970a7001f6ea227b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mfaPrompt", value)

    @builtins.property
    @jsii.member(jsii_name="mfaRememberDevice")
    def mfa_remember_device(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mfaRememberDevice"))

    @mfa_remember_device.setter
    def mfa_remember_device(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e912d518e019e32ec1c45f3c91b7356b0b0e6ac730d91d66dff15778b29cc793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mfaRememberDevice", value)

    @builtins.property
    @jsii.member(jsii_name="mfaRequired")
    def mfa_required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mfaRequired"))

    @mfa_required.setter
    def mfa_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d48902396621df7eb256770d1fa018097662ca6ddd2500e508ed0906ffbda08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mfaRequired", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc41e5e676fa5c46df94b0d0a5447f2c7f2f4887ad9a24f22e82683ee5a7e012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkConnection")
    def network_connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkConnection"))

    @network_connection.setter
    def network_connection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9dee707503898ba3d85a22bfbb4d4c38d98e85b96bd6b1dbeb747f129805906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConnection", value)

    @builtins.property
    @jsii.member(jsii_name="networkExcludes")
    def network_excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkExcludes"))

    @network_excludes.setter
    def network_excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4072cfa8085ccc224de3b88a86ef0c46dc4317900d34205b73142c0c2a023bb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkExcludes", value)

    @builtins.property
    @jsii.member(jsii_name="networkIncludes")
    def network_includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkIncludes"))

    @network_includes.setter
    def network_includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df629e4d68015d0e477f358788234ea92551859bb64fe61e8dc6ec1279a00d33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIncludes", value)

    @builtins.property
    @jsii.member(jsii_name="policyid")
    def policyid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyid"))

    @policyid.setter
    def policyid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abc4ce1260927b35d5a0705fd5cf8551bfd67d41d40377abb4d6e49e8796fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyid", value)

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da392f0c6c491dbd7c0624d22bd08f2f40179614b63b717d8fad13ab96ca2c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value)

    @builtins.property
    @jsii.member(jsii_name="primaryFactor")
    def primary_factor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryFactor"))

    @primary_factor.setter
    def primary_factor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed69b2f2ce384a44e8e88bbbbd7c7d0892faf9c63e4548d892666191bb905064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryFactor", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3217f23b9b3e876ae5f88a3ee29990e4c09a275948fd209bf38d7ef7b1314c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="riscLevel")
    def risc_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "riscLevel"))

    @risc_level.setter
    def risc_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca4052b5d4271ba97960fb6f1f7ce2c5141cd488604da85f58be4f9ca60ea90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "riscLevel", value)

    @builtins.property
    @jsii.member(jsii_name="sessionIdle")
    def session_idle(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionIdle"))

    @session_idle.setter
    def session_idle(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a26f871adaba6a8e2028e906dca55e12373d7e38434aa8bb06269a0aea209a24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionIdle", value)

    @builtins.property
    @jsii.member(jsii_name="sessionLifetime")
    def session_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionLifetime"))

    @session_lifetime.setter
    def session_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10b4e5be38e0940abb0cf385b3ea25ea5bfe5679119171ef6ca5142c8c6b620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="sessionPersistent")
    def session_persistent(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sessionPersistent"))

    @session_persistent.setter
    def session_persistent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aebe1d82b34958c88b2b6621b39d8eae60206643e0ad248b7313904792f4765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionPersistent", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b70a5bbde347b3c785c54fff7901c9e9dae125f59486281d6571ad0f4a5e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="usersExcluded")
    def users_excluded(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "usersExcluded"))

    @users_excluded.setter
    def users_excluded(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efef70694a0d61d2fd47d5dad5798d69c51c68a420f8722d3da7a2ad73aa89c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usersExcluded", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleSignon.PolicyRuleSignonConfig",
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
        "access": "access",
        "authtype": "authtype",
        "behaviors": "behaviors",
        "factor_sequence": "factorSequence",
        "id": "id",
        "identity_provider": "identityProvider",
        "identity_provider_ids": "identityProviderIds",
        "mfa_lifetime": "mfaLifetime",
        "mfa_prompt": "mfaPrompt",
        "mfa_remember_device": "mfaRememberDevice",
        "mfa_required": "mfaRequired",
        "network_connection": "networkConnection",
        "network_excludes": "networkExcludes",
        "network_includes": "networkIncludes",
        "policyid": "policyid",
        "policy_id": "policyId",
        "primary_factor": "primaryFactor",
        "priority": "priority",
        "risc_level": "riscLevel",
        "session_idle": "sessionIdle",
        "session_lifetime": "sessionLifetime",
        "session_persistent": "sessionPersistent",
        "status": "status",
        "users_excluded": "usersExcluded",
    },
)
class PolicyRuleSignonConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access: typing.Optional[builtins.str] = None,
        authtype: typing.Optional[builtins.str] = None,
        behaviors: typing.Optional[typing.Sequence[builtins.str]] = None,
        factor_sequence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleSignonFactorSequence", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity_provider: typing.Optional[builtins.str] = None,
        identity_provider_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        mfa_lifetime: typing.Optional[jsii.Number] = None,
        mfa_prompt: typing.Optional[builtins.str] = None,
        mfa_remember_device: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mfa_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        policyid: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
        primary_factor: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        risc_level: typing.Optional[builtins.str] = None,
        session_idle: typing.Optional[jsii.Number] = None,
        session_lifetime: typing.Optional[jsii.Number] = None,
        session_persistent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#name PolicyRuleSignon#name}
        :param access: Allow or deny access based on the rule conditions: ALLOW, DENY or CHALLENGE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#access PolicyRuleSignon#access}
        :param authtype: Authentication entrypoint: ANY, RADIUS or LDAP_INTERFACE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#authtype PolicyRuleSignon#authtype}
        :param behaviors: List of behavior IDs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#behaviors PolicyRuleSignon#behaviors}
        :param factor_sequence: factor_sequence block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#factor_sequence PolicyRuleSignon#factor_sequence}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#id PolicyRuleSignon#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_provider: Apply rule based on the IdP used: ANY, OKTA or SPECIFIC_IDP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#identity_provider PolicyRuleSignon#identity_provider}
        :param identity_provider_ids: When identity_provider is SPECIFIC_IDP then this is the list of IdP IDs to apply the rule on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#identity_provider_ids PolicyRuleSignon#identity_provider_ids}
        :param mfa_lifetime: Elapsed time before the next MFA challenge. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_lifetime PolicyRuleSignon#mfa_lifetime}
        :param mfa_prompt: Prompt for MFA based on the device used, a factor session lifetime, or every sign-on attempt: DEVICE, SESSION or ALWAYS. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_prompt PolicyRuleSignon#mfa_prompt}
        :param mfa_remember_device: Remember MFA device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_remember_device PolicyRuleSignon#mfa_remember_device}
        :param mfa_required: Require MFA. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_required PolicyRuleSignon#mfa_required}
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#network_connection PolicyRuleSignon#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#network_excludes PolicyRuleSignon#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#network_includes PolicyRuleSignon#network_includes}
        :param policyid: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#policyid PolicyRuleSignon#policyid}
        :param policy_id: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#policy_id PolicyRuleSignon#policy_id}
        :param primary_factor: Primary factor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#primary_factor PolicyRuleSignon#primary_factor}
        :param priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#priority PolicyRuleSignon#priority}
        :param risc_level: Risc level: ANY, LOW, MEDIUM or HIGH. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#risc_level PolicyRuleSignon#risc_level}
        :param session_idle: Max minutes a session can be idle. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#session_idle PolicyRuleSignon#session_idle}
        :param session_lifetime: Max minutes a session is active: Disable = 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#session_lifetime PolicyRuleSignon#session_lifetime}
        :param session_persistent: Whether session cookies will last across browser sessions. Okta Administrators can never have persistent session cookies. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#session_persistent PolicyRuleSignon#session_persistent}
        :param status: Policy Rule Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#status PolicyRuleSignon#status}
        :param users_excluded: Set of User IDs to Exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#users_excluded PolicyRuleSignon#users_excluded}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31b7f5599a10e276cb87a4d984a0f314565f233da6af910a5528435513cee1e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument authtype", value=authtype, expected_type=type_hints["authtype"])
            check_type(argname="argument behaviors", value=behaviors, expected_type=type_hints["behaviors"])
            check_type(argname="argument factor_sequence", value=factor_sequence, expected_type=type_hints["factor_sequence"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity_provider", value=identity_provider, expected_type=type_hints["identity_provider"])
            check_type(argname="argument identity_provider_ids", value=identity_provider_ids, expected_type=type_hints["identity_provider_ids"])
            check_type(argname="argument mfa_lifetime", value=mfa_lifetime, expected_type=type_hints["mfa_lifetime"])
            check_type(argname="argument mfa_prompt", value=mfa_prompt, expected_type=type_hints["mfa_prompt"])
            check_type(argname="argument mfa_remember_device", value=mfa_remember_device, expected_type=type_hints["mfa_remember_device"])
            check_type(argname="argument mfa_required", value=mfa_required, expected_type=type_hints["mfa_required"])
            check_type(argname="argument network_connection", value=network_connection, expected_type=type_hints["network_connection"])
            check_type(argname="argument network_excludes", value=network_excludes, expected_type=type_hints["network_excludes"])
            check_type(argname="argument network_includes", value=network_includes, expected_type=type_hints["network_includes"])
            check_type(argname="argument policyid", value=policyid, expected_type=type_hints["policyid"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument primary_factor", value=primary_factor, expected_type=type_hints["primary_factor"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument risc_level", value=risc_level, expected_type=type_hints["risc_level"])
            check_type(argname="argument session_idle", value=session_idle, expected_type=type_hints["session_idle"])
            check_type(argname="argument session_lifetime", value=session_lifetime, expected_type=type_hints["session_lifetime"])
            check_type(argname="argument session_persistent", value=session_persistent, expected_type=type_hints["session_persistent"])
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
        if access is not None:
            self._values["access"] = access
        if authtype is not None:
            self._values["authtype"] = authtype
        if behaviors is not None:
            self._values["behaviors"] = behaviors
        if factor_sequence is not None:
            self._values["factor_sequence"] = factor_sequence
        if id is not None:
            self._values["id"] = id
        if identity_provider is not None:
            self._values["identity_provider"] = identity_provider
        if identity_provider_ids is not None:
            self._values["identity_provider_ids"] = identity_provider_ids
        if mfa_lifetime is not None:
            self._values["mfa_lifetime"] = mfa_lifetime
        if mfa_prompt is not None:
            self._values["mfa_prompt"] = mfa_prompt
        if mfa_remember_device is not None:
            self._values["mfa_remember_device"] = mfa_remember_device
        if mfa_required is not None:
            self._values["mfa_required"] = mfa_required
        if network_connection is not None:
            self._values["network_connection"] = network_connection
        if network_excludes is not None:
            self._values["network_excludes"] = network_excludes
        if network_includes is not None:
            self._values["network_includes"] = network_includes
        if policyid is not None:
            self._values["policyid"] = policyid
        if policy_id is not None:
            self._values["policy_id"] = policy_id
        if primary_factor is not None:
            self._values["primary_factor"] = primary_factor
        if priority is not None:
            self._values["priority"] = priority
        if risc_level is not None:
            self._values["risc_level"] = risc_level
        if session_idle is not None:
            self._values["session_idle"] = session_idle
        if session_lifetime is not None:
            self._values["session_lifetime"] = session_lifetime
        if session_persistent is not None:
            self._values["session_persistent"] = session_persistent
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#name PolicyRuleSignon#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access(self) -> typing.Optional[builtins.str]:
        '''Allow or deny access based on the rule conditions: ALLOW, DENY or CHALLENGE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#access PolicyRuleSignon#access}
        '''
        result = self._values.get("access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authtype(self) -> typing.Optional[builtins.str]:
        '''Authentication entrypoint: ANY, RADIUS or LDAP_INTERFACE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#authtype PolicyRuleSignon#authtype}
        '''
        result = self._values.get("authtype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def behaviors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of behavior IDs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#behaviors PolicyRuleSignon#behaviors}
        '''
        result = self._values.get("behaviors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def factor_sequence(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleSignonFactorSequence"]]]:
        '''factor_sequence block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#factor_sequence PolicyRuleSignon#factor_sequence}
        '''
        result = self._values.get("factor_sequence")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleSignonFactorSequence"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#id PolicyRuleSignon#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider(self) -> typing.Optional[builtins.str]:
        '''Apply rule based on the IdP used: ANY, OKTA or SPECIFIC_IDP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#identity_provider PolicyRuleSignon#identity_provider}
        '''
        result = self._values.get("identity_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When identity_provider is SPECIFIC_IDP then this is the list of IdP IDs to apply the rule on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#identity_provider_ids PolicyRuleSignon#identity_provider_ids}
        '''
        result = self._values.get("identity_provider_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mfa_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Elapsed time before the next MFA challenge.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_lifetime PolicyRuleSignon#mfa_lifetime}
        '''
        result = self._values.get("mfa_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mfa_prompt(self) -> typing.Optional[builtins.str]:
        '''Prompt for MFA based on the device used, a factor session lifetime, or every sign-on attempt: DEVICE, SESSION or ALWAYS.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_prompt PolicyRuleSignon#mfa_prompt}
        '''
        result = self._values.get("mfa_prompt")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mfa_remember_device(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Remember MFA device.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_remember_device PolicyRuleSignon#mfa_remember_device}
        '''
        result = self._values.get("mfa_remember_device")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mfa_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require MFA.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#mfa_required PolicyRuleSignon#mfa_required}
        '''
        result = self._values.get("mfa_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network_connection(self) -> typing.Optional[builtins.str]:
        '''Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#network_connection PolicyRuleSignon#network_connection}
        '''
        result = self._values.get("network_connection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#network_excludes PolicyRuleSignon#network_excludes}
        '''
        result = self._values.get("network_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#network_includes PolicyRuleSignon#network_includes}
        '''
        result = self._values.get("network_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def policyid(self) -> typing.Optional[builtins.str]:
        '''Policy ID of the Rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#policyid PolicyRuleSignon#policyid}
        '''
        result = self._values.get("policyid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''Policy ID of the Rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#policy_id PolicyRuleSignon#policy_id}
        '''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_factor(self) -> typing.Optional[builtins.str]:
        '''Primary factor.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#primary_factor PolicyRuleSignon#primary_factor}
        '''
        result = self._values.get("primary_factor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Policy Rule Priority, this attribute can be set to a valid priority.

        To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#priority PolicyRuleSignon#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def risc_level(self) -> typing.Optional[builtins.str]:
        '''Risc level: ANY, LOW, MEDIUM or HIGH.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#risc_level PolicyRuleSignon#risc_level}
        '''
        result = self._values.get("risc_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_idle(self) -> typing.Optional[jsii.Number]:
        '''Max minutes a session can be idle.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#session_idle PolicyRuleSignon#session_idle}
        '''
        result = self._values.get("session_idle")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def session_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Max minutes a session is active: Disable = 0.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#session_lifetime PolicyRuleSignon#session_lifetime}
        '''
        result = self._values.get("session_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def session_persistent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether session cookies will last across browser sessions. Okta Administrators can never have persistent session cookies.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#session_persistent PolicyRuleSignon#session_persistent}
        '''
        result = self._values.get("session_persistent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Policy Rule Status: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#status PolicyRuleSignon#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users_excluded(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of User IDs to Exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#users_excluded PolicyRuleSignon#users_excluded}
        '''
        result = self._values.get("users_excluded")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleSignonConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleSignon.PolicyRuleSignonFactorSequence",
    jsii_struct_bases=[],
    name_mapping={
        "primary_criteria_factor_type": "primaryCriteriaFactorType",
        "primary_criteria_provider": "primaryCriteriaProvider",
        "secondary_criteria": "secondaryCriteria",
    },
)
class PolicyRuleSignonFactorSequence:
    def __init__(
        self,
        *,
        primary_criteria_factor_type: builtins.str,
        primary_criteria_provider: builtins.str,
        secondary_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleSignonFactorSequenceSecondaryCriteria", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param primary_criteria_factor_type: Type of a Factor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#primary_criteria_factor_type PolicyRuleSignon#primary_criteria_factor_type}
        :param primary_criteria_provider: Factor provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#primary_criteria_provider PolicyRuleSignon#primary_criteria_provider}
        :param secondary_criteria: secondary_criteria block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#secondary_criteria PolicyRuleSignon#secondary_criteria}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edbb389c663a05a3fe1f1842c210baaa70ac8cdaf53ae539c840c7647e2ccd43)
            check_type(argname="argument primary_criteria_factor_type", value=primary_criteria_factor_type, expected_type=type_hints["primary_criteria_factor_type"])
            check_type(argname="argument primary_criteria_provider", value=primary_criteria_provider, expected_type=type_hints["primary_criteria_provider"])
            check_type(argname="argument secondary_criteria", value=secondary_criteria, expected_type=type_hints["secondary_criteria"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "primary_criteria_factor_type": primary_criteria_factor_type,
            "primary_criteria_provider": primary_criteria_provider,
        }
        if secondary_criteria is not None:
            self._values["secondary_criteria"] = secondary_criteria

    @builtins.property
    def primary_criteria_factor_type(self) -> builtins.str:
        '''Type of a Factor.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#primary_criteria_factor_type PolicyRuleSignon#primary_criteria_factor_type}
        '''
        result = self._values.get("primary_criteria_factor_type")
        assert result is not None, "Required property 'primary_criteria_factor_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_criteria_provider(self) -> builtins.str:
        '''Factor provider.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#primary_criteria_provider PolicyRuleSignon#primary_criteria_provider}
        '''
        result = self._values.get("primary_criteria_provider")
        assert result is not None, "Required property 'primary_criteria_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secondary_criteria(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleSignonFactorSequenceSecondaryCriteria"]]]:
        '''secondary_criteria block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#secondary_criteria PolicyRuleSignon#secondary_criteria}
        '''
        result = self._values.get("secondary_criteria")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleSignonFactorSequenceSecondaryCriteria"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleSignonFactorSequence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyRuleSignonFactorSequenceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleSignon.PolicyRuleSignonFactorSequenceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67f39ed6cf21365b9cf9b65ceeb53dfca641ff514c7665198f582c4511db8486)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PolicyRuleSignonFactorSequenceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70ac22bfdd4ce74699e61730e738c895c396b28918a766552c022d55949596e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PolicyRuleSignonFactorSequenceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f1b74008051c7c0b51990fd53fc0e4cfb33df376232e7030574e6a457ff4b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee1b47666172053b40d0c40ed02872433a91e665958c212acb4c5ec4e6db97d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c1fca3a8001df73e502db8f55d2eebbaa8eefb332e64fb4d448a4be68bbb397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleSignonFactorSequence]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleSignonFactorSequence]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleSignonFactorSequence]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99dd90885fb9766e9d3405fa93b1bf17076bd0196a1a2174f947089a8fdbce2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class PolicyRuleSignonFactorSequenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleSignon.PolicyRuleSignonFactorSequenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c649578f50283d8525bc87f18ff079304de4f8efac38d4f2247688bccb475fea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSecondaryCriteria")
    def put_secondary_criteria(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleSignonFactorSequenceSecondaryCriteria", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e271a9f215a3bc9bca84f3cead66ce68c59d3bbe9ef23a86b87b1ae1b93ee567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecondaryCriteria", [value]))

    @jsii.member(jsii_name="resetSecondaryCriteria")
    def reset_secondary_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryCriteria", []))

    @builtins.property
    @jsii.member(jsii_name="secondaryCriteria")
    def secondary_criteria(
        self,
    ) -> "PolicyRuleSignonFactorSequenceSecondaryCriteriaList":
        return typing.cast("PolicyRuleSignonFactorSequenceSecondaryCriteriaList", jsii.get(self, "secondaryCriteria"))

    @builtins.property
    @jsii.member(jsii_name="primaryCriteriaFactorTypeInput")
    def primary_criteria_factor_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryCriteriaFactorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryCriteriaProviderInput")
    def primary_criteria_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryCriteriaProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryCriteriaInput")
    def secondary_criteria_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleSignonFactorSequenceSecondaryCriteria"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleSignonFactorSequenceSecondaryCriteria"]]], jsii.get(self, "secondaryCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryCriteriaFactorType")
    def primary_criteria_factor_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryCriteriaFactorType"))

    @primary_criteria_factor_type.setter
    def primary_criteria_factor_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15acfda41792ff3cf89579aa4b1d547540e2c93ab89804508e52653af4a74dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryCriteriaFactorType", value)

    @builtins.property
    @jsii.member(jsii_name="primaryCriteriaProvider")
    def primary_criteria_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryCriteriaProvider"))

    @primary_criteria_provider.setter
    def primary_criteria_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__343ec3516210e074907c8c17936aaa24cd816d1bbecd72f037fbdd5f7b396749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryCriteriaProvider", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[PolicyRuleSignonFactorSequence, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[PolicyRuleSignonFactorSequence, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[PolicyRuleSignonFactorSequence, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98d56f02902d917caa6b85cff9b42df615f5522b8dc067ec31a9dca7cbf6215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleSignon.PolicyRuleSignonFactorSequenceSecondaryCriteria",
    jsii_struct_bases=[],
    name_mapping={"factor_type": "factorType", "provider": "provider"},
)
class PolicyRuleSignonFactorSequenceSecondaryCriteria:
    def __init__(self, *, factor_type: builtins.str, provider: builtins.str) -> None:
        '''
        :param factor_type: Type of a Factor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#factor_type PolicyRuleSignon#factor_type}
        :param provider: Factor provider. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#provider PolicyRuleSignon#provider}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c8d0635613dfc70ea5f2bbd0dacf127708cc16bbb6d310a7474245a0962fac)
            check_type(argname="argument factor_type", value=factor_type, expected_type=type_hints["factor_type"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "factor_type": factor_type,
            "provider": provider,
        }

    @builtins.property
    def factor_type(self) -> builtins.str:
        '''Type of a Factor.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#factor_type PolicyRuleSignon#factor_type}
        '''
        result = self._values.get("factor_type")
        assert result is not None, "Required property 'factor_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider(self) -> builtins.str:
        '''Factor provider.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_signon#provider PolicyRuleSignon#provider}
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleSignonFactorSequenceSecondaryCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyRuleSignonFactorSequenceSecondaryCriteriaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleSignon.PolicyRuleSignonFactorSequenceSecondaryCriteriaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2c033cf9e8c4fd01deea73dc3c08a1e07dd98c68fd70bc29cab5df3c470225b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PolicyRuleSignonFactorSequenceSecondaryCriteriaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea0a369696fe8410988062f34da32f784c9a68ae6bcf8c1cd648bc6148705ca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PolicyRuleSignonFactorSequenceSecondaryCriteriaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccbe0dcabb5fd389b0334a61aa4258af8115a8e4cec636c8cc24a442f253432c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2f05477e591fde2f0a2ef1f8e30c7a9291884777e09f99f14667b77579e70b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44e1f0404efe6ae9604cb067ab59f79cf20c22f9b6c9aecea9f4e9afab8549d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleSignonFactorSequenceSecondaryCriteria]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleSignonFactorSequenceSecondaryCriteria]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleSignonFactorSequenceSecondaryCriteria]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9334a2f31e9cc2b8aeb8471de8f6e05c67671b7ffd7258ebc3c168a57de3396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class PolicyRuleSignonFactorSequenceSecondaryCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleSignon.PolicyRuleSignonFactorSequenceSecondaryCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca4929603f8fa5f5cd8013397e21e5de1fd3451c44381c572f9bc397df0fb161)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="factorTypeInput")
    def factor_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "factorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="providerInput")
    def provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerInput"))

    @builtins.property
    @jsii.member(jsii_name="factorType")
    def factor_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "factorType"))

    @factor_type.setter
    def factor_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06c2f2210f74759bc98fbb7d06901cccdf1e13e6903d6203bb648c170615b35a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "factorType", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provider"))

    @provider.setter
    def provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02bc4de6a8f00f7b4c857c9c985d873ecebf013d45a2f1bfe8349db22b34836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provider", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[PolicyRuleSignonFactorSequenceSecondaryCriteria, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[PolicyRuleSignonFactorSequenceSecondaryCriteria, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[PolicyRuleSignonFactorSequenceSecondaryCriteria, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a11fb6265b8c8c5e40ca7aaf76a388c10e729f9cb966ac01e91fe0d710fda8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "PolicyRuleSignon",
    "PolicyRuleSignonConfig",
    "PolicyRuleSignonFactorSequence",
    "PolicyRuleSignonFactorSequenceList",
    "PolicyRuleSignonFactorSequenceOutputReference",
    "PolicyRuleSignonFactorSequenceSecondaryCriteria",
    "PolicyRuleSignonFactorSequenceSecondaryCriteriaList",
    "PolicyRuleSignonFactorSequenceSecondaryCriteriaOutputReference",
]

publication.publish()

def _typecheckingstub__3c7dab4c858bb5fcb91fbce5de2897ecd43f20622a2a7348ad760d180600d655(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    access: typing.Optional[builtins.str] = None,
    authtype: typing.Optional[builtins.str] = None,
    behaviors: typing.Optional[typing.Sequence[builtins.str]] = None,
    factor_sequence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleSignonFactorSequence, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity_provider: typing.Optional[builtins.str] = None,
    identity_provider_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    mfa_lifetime: typing.Optional[jsii.Number] = None,
    mfa_prompt: typing.Optional[builtins.str] = None,
    mfa_remember_device: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mfa_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_connection: typing.Optional[builtins.str] = None,
    network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    policyid: typing.Optional[builtins.str] = None,
    policy_id: typing.Optional[builtins.str] = None,
    primary_factor: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    risc_level: typing.Optional[builtins.str] = None,
    session_idle: typing.Optional[jsii.Number] = None,
    session_lifetime: typing.Optional[jsii.Number] = None,
    session_persistent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__f4544907223bf4380c1095e612e25358e16c325ffe5e61c53e669f297a003873(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleSignonFactorSequence, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056e808cc46b6d12a753e27ff5efdad15c6af4fdccb173e54f756c50838b1e5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53db46318bf02055b28679869842400045637065a50adf1d419c1633ed1eb2f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d411844117af646e085530bdf26caa834468b76e6f89d2202e75e5482a333947(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59716bd2160a1cf8dec878a487fb6985f74a2a1963df42a633152cda95aee581(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a22ef93fce4294dcf837d53018663d7d3b871200ccdb62f1fb77d3934b761fd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1334a4d52a19b0b8d5b38e6cf44a2de965599f3756d13e507b62f0cdb2097648(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75e685970f951104813180afe74d704c45ed1f3953f77cc0c2d51df42086ac9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75bbc087898b75faad185c2fca39ad1ed5d348cafce89c970a7001f6ea227b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e912d518e019e32ec1c45f3c91b7356b0b0e6ac730d91d66dff15778b29cc793(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d48902396621df7eb256770d1fa018097662ca6ddd2500e508ed0906ffbda08(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc41e5e676fa5c46df94b0d0a5447f2c7f2f4887ad9a24f22e82683ee5a7e012(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9dee707503898ba3d85a22bfbb4d4c38d98e85b96bd6b1dbeb747f129805906(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4072cfa8085ccc224de3b88a86ef0c46dc4317900d34205b73142c0c2a023bb7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df629e4d68015d0e477f358788234ea92551859bb64fe61e8dc6ec1279a00d33(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abc4ce1260927b35d5a0705fd5cf8551bfd67d41d40377abb4d6e49e8796fa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da392f0c6c491dbd7c0624d22bd08f2f40179614b63b717d8fad13ab96ca2c9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed69b2f2ce384a44e8e88bbbbd7c7d0892faf9c63e4548d892666191bb905064(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3217f23b9b3e876ae5f88a3ee29990e4c09a275948fd209bf38d7ef7b1314c64(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca4052b5d4271ba97960fb6f1f7ce2c5141cd488604da85f58be4f9ca60ea90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26f871adaba6a8e2028e906dca55e12373d7e38434aa8bb06269a0aea209a24(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10b4e5be38e0940abb0cf385b3ea25ea5bfe5679119171ef6ca5142c8c6b620(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aebe1d82b34958c88b2b6621b39d8eae60206643e0ad248b7313904792f4765(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b70a5bbde347b3c785c54fff7901c9e9dae125f59486281d6571ad0f4a5e0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efef70694a0d61d2fd47d5dad5798d69c51c68a420f8722d3da7a2ad73aa89c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31b7f5599a10e276cb87a4d984a0f314565f233da6af910a5528435513cee1e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    access: typing.Optional[builtins.str] = None,
    authtype: typing.Optional[builtins.str] = None,
    behaviors: typing.Optional[typing.Sequence[builtins.str]] = None,
    factor_sequence: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleSignonFactorSequence, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity_provider: typing.Optional[builtins.str] = None,
    identity_provider_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    mfa_lifetime: typing.Optional[jsii.Number] = None,
    mfa_prompt: typing.Optional[builtins.str] = None,
    mfa_remember_device: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mfa_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_connection: typing.Optional[builtins.str] = None,
    network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    policyid: typing.Optional[builtins.str] = None,
    policy_id: typing.Optional[builtins.str] = None,
    primary_factor: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    risc_level: typing.Optional[builtins.str] = None,
    session_idle: typing.Optional[jsii.Number] = None,
    session_lifetime: typing.Optional[jsii.Number] = None,
    session_persistent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edbb389c663a05a3fe1f1842c210baaa70ac8cdaf53ae539c840c7647e2ccd43(
    *,
    primary_criteria_factor_type: builtins.str,
    primary_criteria_provider: builtins.str,
    secondary_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleSignonFactorSequenceSecondaryCriteria, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f39ed6cf21365b9cf9b65ceeb53dfca641ff514c7665198f582c4511db8486(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70ac22bfdd4ce74699e61730e738c895c396b28918a766552c022d55949596e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f1b74008051c7c0b51990fd53fc0e4cfb33df376232e7030574e6a457ff4b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1b47666172053b40d0c40ed02872433a91e665958c212acb4c5ec4e6db97d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1fca3a8001df73e502db8f55d2eebbaa8eefb332e64fb4d448a4be68bbb397(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99dd90885fb9766e9d3405fa93b1bf17076bd0196a1a2174f947089a8fdbce2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleSignonFactorSequence]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c649578f50283d8525bc87f18ff079304de4f8efac38d4f2247688bccb475fea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e271a9f215a3bc9bca84f3cead66ce68c59d3bbe9ef23a86b87b1ae1b93ee567(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleSignonFactorSequenceSecondaryCriteria, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15acfda41792ff3cf89579aa4b1d547540e2c93ab89804508e52653af4a74dc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343ec3516210e074907c8c17936aaa24cd816d1bbecd72f037fbdd5f7b396749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98d56f02902d917caa6b85cff9b42df615f5522b8dc067ec31a9dca7cbf6215(
    value: typing.Optional[typing.Union[PolicyRuleSignonFactorSequence, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c8d0635613dfc70ea5f2bbd0dacf127708cc16bbb6d310a7474245a0962fac(
    *,
    factor_type: builtins.str,
    provider: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c033cf9e8c4fd01deea73dc3c08a1e07dd98c68fd70bc29cab5df3c470225b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea0a369696fe8410988062f34da32f784c9a68ae6bcf8c1cd648bc6148705ca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbe0dcabb5fd389b0334a61aa4258af8115a8e4cec636c8cc24a442f253432c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f05477e591fde2f0a2ef1f8e30c7a9291884777e09f99f14667b77579e70b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e1f0404efe6ae9604cb067ab59f79cf20c22f9b6c9aecea9f4e9afab8549d3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9334a2f31e9cc2b8aeb8471de8f6e05c67671b7ffd7258ebc3c168a57de3396(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleSignonFactorSequenceSecondaryCriteria]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4929603f8fa5f5cd8013397e21e5de1fd3451c44381c572f9bc397df0fb161(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c2f2210f74759bc98fbb7d06901cccdf1e13e6903d6203bb648c170615b35a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02bc4de6a8f00f7b4c857c9c985d873ecebf013d45a2f1bfe8349db22b34836(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a11fb6265b8c8c5e40ca7aaf76a388c10e729f9cb966ac01e91fe0d710fda8(
    value: typing.Optional[typing.Union[PolicyRuleSignonFactorSequenceSecondaryCriteria, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
