'''
# `okta_app_signon_policy_rule`

Refer to the Terraform Registory for docs: [`okta_app_signon_policy_rule`](https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule).
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


class AppSignonPolicyRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSignonPolicyRule.AppSignonPolicyRule",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule okta_app_signon_policy_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        policy_id: builtins.str,
        access: typing.Optional[builtins.str] = None,
        constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_expression: typing.Optional[builtins.str] = None,
        device_is_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        device_is_registered: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        factor_mode: typing.Optional[builtins.str] = None,
        groups_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        inactivity_period: typing.Optional[builtins.str] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        platform_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppSignonPolicyRulePlatformInclude", typing.Dict[builtins.str, typing.Any]]]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        re_authentication_frequency: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        users_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_types_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_types_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule okta_app_signon_policy_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#name AppSignonPolicyRule#name}
        :param policy_id: ID of the policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#policy_id AppSignonPolicyRule#policy_id}
        :param access: Allow or deny access based on the rule conditions: ALLOW or DENY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#access AppSignonPolicyRule#access}
        :param constraints: An array that contains nested Authenticator Constraint objects that are organized by the Authenticator class. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#constraints AppSignonPolicyRule#constraints}
        :param custom_expression: This is an optional advanced setting. If the expression is formatted incorrectly or conflicts with conditions set above, the rule may not match any users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#custom_expression AppSignonPolicyRule#custom_expression}
        :param device_is_managed: If the device is managed. A device is managed if it's managed by a device management system. When managed is passed, registered must also be included and must be set to true. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_managed AppSignonPolicyRule#device_is_managed}
        :param device_is_registered: If the device is registered. A device is registered if the User enrolls with Okta Verify that is installed on the device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_registered AppSignonPolicyRule#device_is_registered}
        :param factor_mode: The number of factors required to satisfy this assurance level. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#factor_mode AppSignonPolicyRule#factor_mode}
        :param groups_excluded: List of group IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_excluded AppSignonPolicyRule#groups_excluded}
        :param groups_included: List of group IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_included AppSignonPolicyRule#groups_included}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#id AppSignonPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inactivity_period: The inactivity duration after which the end user must re-authenticate. Use the ISO 8601 Period format for recurring time intervals. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#inactivity_period AppSignonPolicyRule#inactivity_period}
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_connection AppSignonPolicyRule#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_excludes AppSignonPolicyRule#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_includes AppSignonPolicyRule#network_includes}
        :param platform_include: platform_include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#platform_include AppSignonPolicyRule#platform_include}
        :param priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#priority AppSignonPolicyRule#priority}.
        :param re_authentication_frequency: The duration after which the end user must re-authenticate, regardless of user activity. Use the ISO 8601 Period format for recurring time intervals. PT0S - Every sign-in attempt, PT43800H - Once per session Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#re_authentication_frequency AppSignonPolicyRule#re_authentication_frequency}
        :param status: Status of the rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#status AppSignonPolicyRule#status}
        :param type: The Verification Method type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#type AppSignonPolicyRule#type}
        :param users_excluded: Set of User IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_excluded AppSignonPolicyRule#users_excluded}
        :param users_included: Set of User IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_included AppSignonPolicyRule#users_included}
        :param user_types_excluded: Set of User Type IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_excluded AppSignonPolicyRule#user_types_excluded}
        :param user_types_included: Set of User Type IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_included AppSignonPolicyRule#user_types_included}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f2250bbc9a1a35b0d133a37bed12bcdb52489261a0da800b35926b7c934f80)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppSignonPolicyRuleConfig(
            name=name,
            policy_id=policy_id,
            access=access,
            constraints=constraints,
            custom_expression=custom_expression,
            device_is_managed=device_is_managed,
            device_is_registered=device_is_registered,
            factor_mode=factor_mode,
            groups_excluded=groups_excluded,
            groups_included=groups_included,
            id=id,
            inactivity_period=inactivity_period,
            network_connection=network_connection,
            network_excludes=network_excludes,
            network_includes=network_includes,
            platform_include=platform_include,
            priority=priority,
            re_authentication_frequency=re_authentication_frequency,
            status=status,
            type=type,
            users_excluded=users_excluded,
            users_included=users_included,
            user_types_excluded=user_types_excluded,
            user_types_included=user_types_included,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPlatformInclude")
    def put_platform_include(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppSignonPolicyRulePlatformInclude", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__070449af63cf6596bc67a9ce4e85b6289012b6b311219f7a9d885803912e9c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlatformInclude", [value]))

    @jsii.member(jsii_name="resetAccess")
    def reset_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccess", []))

    @jsii.member(jsii_name="resetConstraints")
    def reset_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConstraints", []))

    @jsii.member(jsii_name="resetCustomExpression")
    def reset_custom_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomExpression", []))

    @jsii.member(jsii_name="resetDeviceIsManaged")
    def reset_device_is_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceIsManaged", []))

    @jsii.member(jsii_name="resetDeviceIsRegistered")
    def reset_device_is_registered(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceIsRegistered", []))

    @jsii.member(jsii_name="resetFactorMode")
    def reset_factor_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFactorMode", []))

    @jsii.member(jsii_name="resetGroupsExcluded")
    def reset_groups_excluded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsExcluded", []))

    @jsii.member(jsii_name="resetGroupsIncluded")
    def reset_groups_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsIncluded", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInactivityPeriod")
    def reset_inactivity_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInactivityPeriod", []))

    @jsii.member(jsii_name="resetNetworkConnection")
    def reset_network_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConnection", []))

    @jsii.member(jsii_name="resetNetworkExcludes")
    def reset_network_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkExcludes", []))

    @jsii.member(jsii_name="resetNetworkIncludes")
    def reset_network_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkIncludes", []))

    @jsii.member(jsii_name="resetPlatformInclude")
    def reset_platform_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformInclude", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetReAuthenticationFrequency")
    def reset_re_authentication_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReAuthenticationFrequency", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUsersExcluded")
    def reset_users_excluded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsersExcluded", []))

    @jsii.member(jsii_name="resetUsersIncluded")
    def reset_users_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsersIncluded", []))

    @jsii.member(jsii_name="resetUserTypesExcluded")
    def reset_user_types_excluded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTypesExcluded", []))

    @jsii.member(jsii_name="resetUserTypesIncluded")
    def reset_user_types_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTypesIncluded", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="platformInclude")
    def platform_include(self) -> "AppSignonPolicyRulePlatformIncludeList":
        return typing.cast("AppSignonPolicyRulePlatformIncludeList", jsii.get(self, "platformInclude"))

    @builtins.property
    @jsii.member(jsii_name="accessInput")
    def access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessInput"))

    @builtins.property
    @jsii.member(jsii_name="constraintsInput")
    def constraints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "constraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="customExpressionInput")
    def custom_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceIsManagedInput")
    def device_is_managed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deviceIsManagedInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceIsRegisteredInput")
    def device_is_registered_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deviceIsRegisteredInput"))

    @builtins.property
    @jsii.member(jsii_name="factorModeInput")
    def factor_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "factorModeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsExcludedInput")
    def groups_excluded_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsExcludedInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsIncludedInput")
    def groups_included_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsIncludedInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inactivityPeriodInput")
    def inactivity_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inactivityPeriodInput"))

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
    @jsii.member(jsii_name="platformIncludeInput")
    def platform_include_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppSignonPolicyRulePlatformInclude"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppSignonPolicyRulePlatformInclude"]]], jsii.get(self, "platformIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="reAuthenticationFrequencyInput")
    def re_authentication_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reAuthenticationFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="usersExcludedInput")
    def users_excluded_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersExcludedInput"))

    @builtins.property
    @jsii.member(jsii_name="usersIncludedInput")
    def users_included_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersIncludedInput"))

    @builtins.property
    @jsii.member(jsii_name="userTypesExcludedInput")
    def user_types_excluded_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userTypesExcludedInput"))

    @builtins.property
    @jsii.member(jsii_name="userTypesIncludedInput")
    def user_types_included_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userTypesIncludedInput"))

    @builtins.property
    @jsii.member(jsii_name="access")
    def access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "access"))

    @access.setter
    def access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd8a7cb7541eb8d2d38261e48c239b78c2078785de5a40c6f37706666eea6d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "access", value)

    @builtins.property
    @jsii.member(jsii_name="constraints")
    def constraints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "constraints"))

    @constraints.setter
    def constraints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050b24e6d2c1a44c3bfc4b5ccd837a763dc6f6b8709be088bba4ccf2adc72f23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraints", value)

    @builtins.property
    @jsii.member(jsii_name="customExpression")
    def custom_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customExpression"))

    @custom_expression.setter
    def custom_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84057c93f670c9685b6602b4d5433ed4c93bccfcdd4965fc49791a6f4f575e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customExpression", value)

    @builtins.property
    @jsii.member(jsii_name="deviceIsManaged")
    def device_is_managed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deviceIsManaged"))

    @device_is_managed.setter
    def device_is_managed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13dafa53e93129e8a4f5e2ef9535416d8abde69a4277eb2cf65250ab48ca8670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceIsManaged", value)

    @builtins.property
    @jsii.member(jsii_name="deviceIsRegistered")
    def device_is_registered(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deviceIsRegistered"))

    @device_is_registered.setter
    def device_is_registered(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab0553f87df11c5588e93deb39b1f6485634e9cda167fefe597248b5cfa7518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceIsRegistered", value)

    @builtins.property
    @jsii.member(jsii_name="factorMode")
    def factor_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "factorMode"))

    @factor_mode.setter
    def factor_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1c90e28bba9caa312b79498eaaea5f8c685df27544e2d78a68fc528d769bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "factorMode", value)

    @builtins.property
    @jsii.member(jsii_name="groupsExcluded")
    def groups_excluded(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsExcluded"))

    @groups_excluded.setter
    def groups_excluded(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b68bd0cdd5d910bc0fc19c425812a88018441b97fa8264bff9e31d0a98082af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsExcluded", value)

    @builtins.property
    @jsii.member(jsii_name="groupsIncluded")
    def groups_included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsIncluded"))

    @groups_included.setter
    def groups_included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f633a7d1f2d7e17d07bdf52565865fa89f313c5dbb1236e9c110d01c549c29e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsIncluded", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d4e38b411e05bcb08ce6f5848f48a758e40df455beae66825bf2f84efaeddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="inactivityPeriod")
    def inactivity_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inactivityPeriod"))

    @inactivity_period.setter
    def inactivity_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31abb9701d7eeadb18d1eb41528af91e4eef4ebe2dd897180d4f519fe97434c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inactivityPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84faee875f57e69f32bd82e2766832c6e0c004b368711bb37d40f9f4d942cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkConnection")
    def network_connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkConnection"))

    @network_connection.setter
    def network_connection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3869f88bbf7c3cfd879c8378db9513a444fc125fd8c076e8754486c7268a467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConnection", value)

    @builtins.property
    @jsii.member(jsii_name="networkExcludes")
    def network_excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkExcludes"))

    @network_excludes.setter
    def network_excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a12b18719a7062bdf67a901d3e9c6d0409d65767dbd9b35b9a3ef656db9d9db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkExcludes", value)

    @builtins.property
    @jsii.member(jsii_name="networkIncludes")
    def network_includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkIncludes"))

    @network_includes.setter
    def network_includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe394ceaad67bc7d68854ac598040cc2e6c5f7c50cea4c25a3d31dc787e7e01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIncludes", value)

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3731a9633033aa964eea9a3c449ba37b1614ba766f8101c9b8411d1e9a98c817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58546a311b7549649f2ba158ef20b20472d134faae15b568ffec2807d56e51d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="reAuthenticationFrequency")
    def re_authentication_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reAuthenticationFrequency"))

    @re_authentication_frequency.setter
    def re_authentication_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1998ebd06595664fa9316ea88211cb900af49c6b8af7488019c9c554a69d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reAuthenticationFrequency", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1057793dee050d79de2c5e5808a50d0d161777c4cf89c600a05bfa7a2adafd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bed9b832d6cf12954a83d8a0d2e564151636b1c079b542189ce4f890d737b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="usersExcluded")
    def users_excluded(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "usersExcluded"))

    @users_excluded.setter
    def users_excluded(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ccdae612788471878134f547d8419bef5b6ac01cd937a517e0dd15c8326efe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usersExcluded", value)

    @builtins.property
    @jsii.member(jsii_name="usersIncluded")
    def users_included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "usersIncluded"))

    @users_included.setter
    def users_included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f245ebdd66ed73594013ee29735ac9e6e066e43da815d34fe92e96c2f0bb9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usersIncluded", value)

    @builtins.property
    @jsii.member(jsii_name="userTypesExcluded")
    def user_types_excluded(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userTypesExcluded"))

    @user_types_excluded.setter
    def user_types_excluded(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54812b7f9eb8de0f7c6200dce1916b14e4a05c282b77134743465370297e07b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTypesExcluded", value)

    @builtins.property
    @jsii.member(jsii_name="userTypesIncluded")
    def user_types_included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userTypesIncluded"))

    @user_types_included.setter
    def user_types_included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbcef7d6a8ad3110e4b6149e9d58b055d1cfcfde9f7b1f696f776ad121a93de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTypesIncluded", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appSignonPolicyRule.AppSignonPolicyRuleConfig",
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
        "policy_id": "policyId",
        "access": "access",
        "constraints": "constraints",
        "custom_expression": "customExpression",
        "device_is_managed": "deviceIsManaged",
        "device_is_registered": "deviceIsRegistered",
        "factor_mode": "factorMode",
        "groups_excluded": "groupsExcluded",
        "groups_included": "groupsIncluded",
        "id": "id",
        "inactivity_period": "inactivityPeriod",
        "network_connection": "networkConnection",
        "network_excludes": "networkExcludes",
        "network_includes": "networkIncludes",
        "platform_include": "platformInclude",
        "priority": "priority",
        "re_authentication_frequency": "reAuthenticationFrequency",
        "status": "status",
        "type": "type",
        "users_excluded": "usersExcluded",
        "users_included": "usersIncluded",
        "user_types_excluded": "userTypesExcluded",
        "user_types_included": "userTypesIncluded",
    },
)
class AppSignonPolicyRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        policy_id: builtins.str,
        access: typing.Optional[builtins.str] = None,
        constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_expression: typing.Optional[builtins.str] = None,
        device_is_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        device_is_registered: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        factor_mode: typing.Optional[builtins.str] = None,
        groups_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        inactivity_period: typing.Optional[builtins.str] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        platform_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppSignonPolicyRulePlatformInclude", typing.Dict[builtins.str, typing.Any]]]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        re_authentication_frequency: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        users_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_types_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_types_included: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#name AppSignonPolicyRule#name}
        :param policy_id: ID of the policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#policy_id AppSignonPolicyRule#policy_id}
        :param access: Allow or deny access based on the rule conditions: ALLOW or DENY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#access AppSignonPolicyRule#access}
        :param constraints: An array that contains nested Authenticator Constraint objects that are organized by the Authenticator class. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#constraints AppSignonPolicyRule#constraints}
        :param custom_expression: This is an optional advanced setting. If the expression is formatted incorrectly or conflicts with conditions set above, the rule may not match any users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#custom_expression AppSignonPolicyRule#custom_expression}
        :param device_is_managed: If the device is managed. A device is managed if it's managed by a device management system. When managed is passed, registered must also be included and must be set to true. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_managed AppSignonPolicyRule#device_is_managed}
        :param device_is_registered: If the device is registered. A device is registered if the User enrolls with Okta Verify that is installed on the device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_registered AppSignonPolicyRule#device_is_registered}
        :param factor_mode: The number of factors required to satisfy this assurance level. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#factor_mode AppSignonPolicyRule#factor_mode}
        :param groups_excluded: List of group IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_excluded AppSignonPolicyRule#groups_excluded}
        :param groups_included: List of group IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_included AppSignonPolicyRule#groups_included}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#id AppSignonPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inactivity_period: The inactivity duration after which the end user must re-authenticate. Use the ISO 8601 Period format for recurring time intervals. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#inactivity_period AppSignonPolicyRule#inactivity_period}
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_connection AppSignonPolicyRule#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_excludes AppSignonPolicyRule#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_includes AppSignonPolicyRule#network_includes}
        :param platform_include: platform_include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#platform_include AppSignonPolicyRule#platform_include}
        :param priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#priority AppSignonPolicyRule#priority}.
        :param re_authentication_frequency: The duration after which the end user must re-authenticate, regardless of user activity. Use the ISO 8601 Period format for recurring time intervals. PT0S - Every sign-in attempt, PT43800H - Once per session Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#re_authentication_frequency AppSignonPolicyRule#re_authentication_frequency}
        :param status: Status of the rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#status AppSignonPolicyRule#status}
        :param type: The Verification Method type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#type AppSignonPolicyRule#type}
        :param users_excluded: Set of User IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_excluded AppSignonPolicyRule#users_excluded}
        :param users_included: Set of User IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_included AppSignonPolicyRule#users_included}
        :param user_types_excluded: Set of User Type IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_excluded AppSignonPolicyRule#user_types_excluded}
        :param user_types_included: Set of User Type IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_included AppSignonPolicyRule#user_types_included}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1ab289fb570e6ca70514a4c6d867d7057620b4bcfa5d3546628328a4eb6444)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
            check_type(argname="argument custom_expression", value=custom_expression, expected_type=type_hints["custom_expression"])
            check_type(argname="argument device_is_managed", value=device_is_managed, expected_type=type_hints["device_is_managed"])
            check_type(argname="argument device_is_registered", value=device_is_registered, expected_type=type_hints["device_is_registered"])
            check_type(argname="argument factor_mode", value=factor_mode, expected_type=type_hints["factor_mode"])
            check_type(argname="argument groups_excluded", value=groups_excluded, expected_type=type_hints["groups_excluded"])
            check_type(argname="argument groups_included", value=groups_included, expected_type=type_hints["groups_included"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inactivity_period", value=inactivity_period, expected_type=type_hints["inactivity_period"])
            check_type(argname="argument network_connection", value=network_connection, expected_type=type_hints["network_connection"])
            check_type(argname="argument network_excludes", value=network_excludes, expected_type=type_hints["network_excludes"])
            check_type(argname="argument network_includes", value=network_includes, expected_type=type_hints["network_includes"])
            check_type(argname="argument platform_include", value=platform_include, expected_type=type_hints["platform_include"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument re_authentication_frequency", value=re_authentication_frequency, expected_type=type_hints["re_authentication_frequency"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument users_excluded", value=users_excluded, expected_type=type_hints["users_excluded"])
            check_type(argname="argument users_included", value=users_included, expected_type=type_hints["users_included"])
            check_type(argname="argument user_types_excluded", value=user_types_excluded, expected_type=type_hints["user_types_excluded"])
            check_type(argname="argument user_types_included", value=user_types_included, expected_type=type_hints["user_types_included"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "policy_id": policy_id,
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
        if constraints is not None:
            self._values["constraints"] = constraints
        if custom_expression is not None:
            self._values["custom_expression"] = custom_expression
        if device_is_managed is not None:
            self._values["device_is_managed"] = device_is_managed
        if device_is_registered is not None:
            self._values["device_is_registered"] = device_is_registered
        if factor_mode is not None:
            self._values["factor_mode"] = factor_mode
        if groups_excluded is not None:
            self._values["groups_excluded"] = groups_excluded
        if groups_included is not None:
            self._values["groups_included"] = groups_included
        if id is not None:
            self._values["id"] = id
        if inactivity_period is not None:
            self._values["inactivity_period"] = inactivity_period
        if network_connection is not None:
            self._values["network_connection"] = network_connection
        if network_excludes is not None:
            self._values["network_excludes"] = network_excludes
        if network_includes is not None:
            self._values["network_includes"] = network_includes
        if platform_include is not None:
            self._values["platform_include"] = platform_include
        if priority is not None:
            self._values["priority"] = priority
        if re_authentication_frequency is not None:
            self._values["re_authentication_frequency"] = re_authentication_frequency
        if status is not None:
            self._values["status"] = status
        if type is not None:
            self._values["type"] = type
        if users_excluded is not None:
            self._values["users_excluded"] = users_excluded
        if users_included is not None:
            self._values["users_included"] = users_included
        if user_types_excluded is not None:
            self._values["user_types_excluded"] = user_types_excluded
        if user_types_included is not None:
            self._values["user_types_included"] = user_types_included

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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#name AppSignonPolicyRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''ID of the policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#policy_id AppSignonPolicyRule#policy_id}
        '''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access(self) -> typing.Optional[builtins.str]:
        '''Allow or deny access based on the rule conditions: ALLOW or DENY.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#access AppSignonPolicyRule#access}
        '''
        result = self._values.get("access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def constraints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array that contains nested Authenticator Constraint objects that are organized by the Authenticator class.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#constraints AppSignonPolicyRule#constraints}
        '''
        result = self._values.get("constraints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def custom_expression(self) -> typing.Optional[builtins.str]:
        '''This is an optional advanced setting.

        If the expression is formatted incorrectly or conflicts with conditions set above, the rule may not match any users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#custom_expression AppSignonPolicyRule#custom_expression}
        '''
        result = self._values.get("custom_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_is_managed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the device is managed.

        A device is managed if it's managed by a device management system. When managed is passed, registered must also be included and must be set to true.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_managed AppSignonPolicyRule#device_is_managed}
        '''
        result = self._values.get("device_is_managed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def device_is_registered(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the device is registered.

        A device is registered if the User enrolls with Okta Verify that is installed on the device.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_registered AppSignonPolicyRule#device_is_registered}
        '''
        result = self._values.get("device_is_registered")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def factor_mode(self) -> typing.Optional[builtins.str]:
        '''The number of factors required to satisfy this assurance level.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#factor_mode AppSignonPolicyRule#factor_mode}
        '''
        result = self._values.get("factor_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_excluded(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of group IDs to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_excluded AppSignonPolicyRule#groups_excluded}
        '''
        result = self._values.get("groups_excluded")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def groups_included(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of group IDs to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_included AppSignonPolicyRule#groups_included}
        '''
        result = self._values.get("groups_included")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#id AppSignonPolicyRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inactivity_period(self) -> typing.Optional[builtins.str]:
        '''The inactivity duration after which the end user must re-authenticate.

        Use the ISO 8601 Period format for recurring time intervals.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#inactivity_period AppSignonPolicyRule#inactivity_period}
        '''
        result = self._values.get("inactivity_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_connection(self) -> typing.Optional[builtins.str]:
        '''Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_connection AppSignonPolicyRule#network_connection}
        '''
        result = self._values.get("network_connection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_excludes AppSignonPolicyRule#network_excludes}
        '''
        result = self._values.get("network_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_includes AppSignonPolicyRule#network_includes}
        '''
        result = self._values.get("network_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def platform_include(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppSignonPolicyRulePlatformInclude"]]]:
        '''platform_include block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#platform_include AppSignonPolicyRule#platform_include}
        '''
        result = self._values.get("platform_include")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppSignonPolicyRulePlatformInclude"]]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#priority AppSignonPolicyRule#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def re_authentication_frequency(self) -> typing.Optional[builtins.str]:
        '''The duration after which the end user must re-authenticate, regardless of user activity.

        Use the ISO 8601 Period format for recurring time intervals. PT0S - Every sign-in attempt, PT43800H - Once per session

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#re_authentication_frequency AppSignonPolicyRule#re_authentication_frequency}
        '''
        result = self._values.get("re_authentication_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of the rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#status AppSignonPolicyRule#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The Verification Method type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#type AppSignonPolicyRule#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users_excluded(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of User IDs to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_excluded AppSignonPolicyRule#users_excluded}
        '''
        result = self._values.get("users_excluded")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def users_included(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of User IDs to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_included AppSignonPolicyRule#users_included}
        '''
        result = self._values.get("users_included")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_types_excluded(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of User Type IDs to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_excluded AppSignonPolicyRule#user_types_excluded}
        '''
        result = self._values.get("user_types_excluded")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_types_included(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of User Type IDs to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_included AppSignonPolicyRule#user_types_included}
        '''
        result = self._values.get("user_types_included")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSignonPolicyRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appSignonPolicyRule.AppSignonPolicyRulePlatformInclude",
    jsii_struct_bases=[],
    name_mapping={
        "os_expression": "osExpression",
        "os_type": "osType",
        "type": "type",
    },
)
class AppSignonPolicyRulePlatformInclude:
    def __init__(
        self,
        *,
        os_expression: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_expression: Only available with OTHER OS type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#os_expression AppSignonPolicyRule#os_expression}
        :param os_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#os_type AppSignonPolicyRule#os_type}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#type AppSignonPolicyRule#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c53c0e23132a37d26716f4a0cd5b5408a86e88c64a3d5d005d16889b88b3c89)
            check_type(argname="argument os_expression", value=os_expression, expected_type=type_hints["os_expression"])
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if os_expression is not None:
            self._values["os_expression"] = os_expression
        if os_type is not None:
            self._values["os_type"] = os_type
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def os_expression(self) -> typing.Optional[builtins.str]:
        '''Only available with OTHER OS type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#os_expression AppSignonPolicyRule#os_expression}
        '''
        result = self._values.get("os_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#os_type AppSignonPolicyRule#os_type}.'''
        result = self._values.get("os_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#type AppSignonPolicyRule#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSignonPolicyRulePlatformInclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppSignonPolicyRulePlatformIncludeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSignonPolicyRule.AppSignonPolicyRulePlatformIncludeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f80c574c5f2c620ea77788c4b2e56459c691ab7856bb3734a5c23bda88cc386c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppSignonPolicyRulePlatformIncludeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1c12f0b2eed8b886125853a7dbed63b0bdd0d2c487ea67bad594b409c2b604)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppSignonPolicyRulePlatformIncludeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2518eb458d27fe8bf8677b310bcbafec7c3c1695947b407d7d27c710fdee13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14f8db3ac72268ee5cb8edb258a67248b9793a0d184376e78236c3bbf240df52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b49d4d8d88028f976269c76c46dd52d26efdd8abde4fecd40f05a47662d1809e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSignonPolicyRulePlatformInclude]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSignonPolicyRulePlatformInclude]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSignonPolicyRulePlatformInclude]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe73a20d6d382212f3a66c3877e47622d10d8c54d72845744145b138c9216aaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppSignonPolicyRulePlatformIncludeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSignonPolicyRule.AppSignonPolicyRulePlatformIncludeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e08aaf8d1070c7d23648bba077f7c7055bb1c8ffcb5587499827e34d1c2a0320)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOsExpression")
    def reset_os_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsExpression", []))

    @jsii.member(jsii_name="resetOsType")
    def reset_os_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsType", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="osExpressionInput")
    def os_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="osExpression")
    def os_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osExpression"))

    @os_expression.setter
    def os_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddfec037c2627cfcc29ffe2e118c2e6cd0f3f9609bd5a8b48223a807914104e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osExpression", value)

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1de61cc587d3b5ec1a46ac9faba6fb1b8c83b69417ea544420188102845b86e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48dc6b5cda264b7b7b419a2b8421998413373d3c75731210fce31cc7f9dd2f00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppSignonPolicyRulePlatformInclude, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppSignonPolicyRulePlatformInclude, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppSignonPolicyRulePlatformInclude, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2eec6f52dc4f4a89134564999cbc2df4c955a467bae7b7e5d750225e1cc6d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AppSignonPolicyRule",
    "AppSignonPolicyRuleConfig",
    "AppSignonPolicyRulePlatformInclude",
    "AppSignonPolicyRulePlatformIncludeList",
    "AppSignonPolicyRulePlatformIncludeOutputReference",
]

publication.publish()

def _typecheckingstub__24f2250bbc9a1a35b0d133a37bed12bcdb52489261a0da800b35926b7c934f80(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    policy_id: builtins.str,
    access: typing.Optional[builtins.str] = None,
    constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_expression: typing.Optional[builtins.str] = None,
    device_is_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    device_is_registered: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    factor_mode: typing.Optional[builtins.str] = None,
    groups_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    inactivity_period: typing.Optional[builtins.str] = None,
    network_connection: typing.Optional[builtins.str] = None,
    network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    platform_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppSignonPolicyRulePlatformInclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    re_authentication_frequency: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
    users_included: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_types_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_types_included: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__070449af63cf6596bc67a9ce4e85b6289012b6b311219f7a9d885803912e9c59(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppSignonPolicyRulePlatformInclude, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd8a7cb7541eb8d2d38261e48c239b78c2078785de5a40c6f37706666eea6d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050b24e6d2c1a44c3bfc4b5ccd837a763dc6f6b8709be088bba4ccf2adc72f23(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84057c93f670c9685b6602b4d5433ed4c93bccfcdd4965fc49791a6f4f575e0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13dafa53e93129e8a4f5e2ef9535416d8abde69a4277eb2cf65250ab48ca8670(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab0553f87df11c5588e93deb39b1f6485634e9cda167fefe597248b5cfa7518(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1c90e28bba9caa312b79498eaaea5f8c685df27544e2d78a68fc528d769bcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b68bd0cdd5d910bc0fc19c425812a88018441b97fa8264bff9e31d0a98082af(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f633a7d1f2d7e17d07bdf52565865fa89f313c5dbb1236e9c110d01c549c29e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d4e38b411e05bcb08ce6f5848f48a758e40df455beae66825bf2f84efaeddb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31abb9701d7eeadb18d1eb41528af91e4eef4ebe2dd897180d4f519fe97434c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c84faee875f57e69f32bd82e2766832c6e0c004b368711bb37d40f9f4d942cd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3869f88bbf7c3cfd879c8378db9513a444fc125fd8c076e8754486c7268a467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a12b18719a7062bdf67a901d3e9c6d0409d65767dbd9b35b9a3ef656db9d9db(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe394ceaad67bc7d68854ac598040cc2e6c5f7c50cea4c25a3d31dc787e7e01(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3731a9633033aa964eea9a3c449ba37b1614ba766f8101c9b8411d1e9a98c817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58546a311b7549649f2ba158ef20b20472d134faae15b568ffec2807d56e51d0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1998ebd06595664fa9316ea88211cb900af49c6b8af7488019c9c554a69d80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1057793dee050d79de2c5e5808a50d0d161777c4cf89c600a05bfa7a2adafd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bed9b832d6cf12954a83d8a0d2e564151636b1c079b542189ce4f890d737b00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ccdae612788471878134f547d8419bef5b6ac01cd937a517e0dd15c8326efe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f245ebdd66ed73594013ee29735ac9e6e066e43da815d34fe92e96c2f0bb9a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54812b7f9eb8de0f7c6200dce1916b14e4a05c282b77134743465370297e07b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbcef7d6a8ad3110e4b6149e9d58b055d1cfcfde9f7b1f696f776ad121a93de0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1ab289fb570e6ca70514a4c6d867d7057620b4bcfa5d3546628328a4eb6444(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    policy_id: builtins.str,
    access: typing.Optional[builtins.str] = None,
    constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_expression: typing.Optional[builtins.str] = None,
    device_is_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    device_is_registered: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    factor_mode: typing.Optional[builtins.str] = None,
    groups_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
    groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    inactivity_period: typing.Optional[builtins.str] = None,
    network_connection: typing.Optional[builtins.str] = None,
    network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    platform_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppSignonPolicyRulePlatformInclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    re_authentication_frequency: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
    users_included: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_types_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_types_included: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c53c0e23132a37d26716f4a0cd5b5408a86e88c64a3d5d005d16889b88b3c89(
    *,
    os_expression: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80c574c5f2c620ea77788c4b2e56459c691ab7856bb3734a5c23bda88cc386c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1c12f0b2eed8b886125853a7dbed63b0bdd0d2c487ea67bad594b409c2b604(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2518eb458d27fe8bf8677b310bcbafec7c3c1695947b407d7d27c710fdee13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f8db3ac72268ee5cb8edb258a67248b9793a0d184376e78236c3bbf240df52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49d4d8d88028f976269c76c46dd52d26efdd8abde4fecd40f05a47662d1809e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe73a20d6d382212f3a66c3877e47622d10d8c54d72845744145b138c9216aaa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppSignonPolicyRulePlatformInclude]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08aaf8d1070c7d23648bba077f7c7055bb1c8ffcb5587499827e34d1c2a0320(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfec037c2627cfcc29ffe2e118c2e6cd0f3f9609bd5a8b48223a807914104e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1de61cc587d3b5ec1a46ac9faba6fb1b8c83b69417ea544420188102845b86e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48dc6b5cda264b7b7b419a2b8421998413373d3c75731210fce31cc7f9dd2f00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2eec6f52dc4f4a89134564999cbc2df4c955a467bae7b7e5d750225e1cc6d59(
    value: typing.Optional[typing.Union[AppSignonPolicyRulePlatformInclude, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
