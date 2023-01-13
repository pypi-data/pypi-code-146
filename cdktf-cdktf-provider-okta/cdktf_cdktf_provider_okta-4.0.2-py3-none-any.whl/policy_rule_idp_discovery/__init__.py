'''
# `okta_policy_rule_idp_discovery`

Refer to the Terraform Registory for docs: [`okta_policy_rule_idp_discovery`](https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery).
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


class PolicyRuleIdpDiscovery(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscovery",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery okta_policy_rule_idp_discovery}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        app_exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleIdpDiscoveryAppExclude", typing.Dict[builtins.str, typing.Any]]]]] = None,
        app_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleIdpDiscoveryAppInclude", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        idp_id: typing.Optional[builtins.str] = None,
        idp_type: typing.Optional[builtins.str] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        platform_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleIdpDiscoveryPlatformInclude", typing.Dict[builtins.str, typing.Any]]]]] = None,
        policyid: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        user_identifier_attribute: typing.Optional[builtins.str] = None,
        user_identifier_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleIdpDiscoveryUserIdentifierPatterns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        user_identifier_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery okta_policy_rule_idp_discovery} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#name PolicyRuleIdpDiscovery#name}
        :param app_exclude: app_exclude block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#app_exclude PolicyRuleIdpDiscovery#app_exclude}
        :param app_include: app_include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#app_include PolicyRuleIdpDiscovery#app_include}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#id PolicyRuleIdpDiscovery#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idp_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#idp_id PolicyRuleIdpDiscovery#idp_id}.
        :param idp_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#idp_type PolicyRuleIdpDiscovery#idp_type}.
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#network_connection PolicyRuleIdpDiscovery#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#network_excludes PolicyRuleIdpDiscovery#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#network_includes PolicyRuleIdpDiscovery#network_includes}
        :param platform_include: platform_include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#platform_include PolicyRuleIdpDiscovery#platform_include}
        :param policyid: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#policyid PolicyRuleIdpDiscovery#policyid}
        :param policy_id: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#policy_id PolicyRuleIdpDiscovery#policy_id}
        :param priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#priority PolicyRuleIdpDiscovery#priority}
        :param status: Policy Rule Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#status PolicyRuleIdpDiscovery#status}
        :param user_identifier_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#user_identifier_attribute PolicyRuleIdpDiscovery#user_identifier_attribute}.
        :param user_identifier_patterns: user_identifier_patterns block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#user_identifier_patterns PolicyRuleIdpDiscovery#user_identifier_patterns}
        :param user_identifier_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#user_identifier_type PolicyRuleIdpDiscovery#user_identifier_type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c78decd6dec0eeb7765c396dde464f85b6a31152cbca3449a190d9f0d9f00a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PolicyRuleIdpDiscoveryConfig(
            name=name,
            app_exclude=app_exclude,
            app_include=app_include,
            id=id,
            idp_id=idp_id,
            idp_type=idp_type,
            network_connection=network_connection,
            network_excludes=network_excludes,
            network_includes=network_includes,
            platform_include=platform_include,
            policyid=policyid,
            policy_id=policy_id,
            priority=priority,
            status=status,
            user_identifier_attribute=user_identifier_attribute,
            user_identifier_patterns=user_identifier_patterns,
            user_identifier_type=user_identifier_type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAppExclude")
    def put_app_exclude(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleIdpDiscoveryAppExclude", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1730bb1666ec36f050deae0531218cfe0219876c489b34c9d181dc782075d99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAppExclude", [value]))

    @jsii.member(jsii_name="putAppInclude")
    def put_app_include(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleIdpDiscoveryAppInclude", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183a0fd51bf52e63b295443ea7ca2e78738c20ed41e0bfe25e4890298b9f58a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAppInclude", [value]))

    @jsii.member(jsii_name="putPlatformInclude")
    def put_platform_include(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleIdpDiscoveryPlatformInclude", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa411b8ec838ca4410f39d43d9777b0fc5d83b4a4bec30c091909c3462e4fcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlatformInclude", [value]))

    @jsii.member(jsii_name="putUserIdentifierPatterns")
    def put_user_identifier_patterns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleIdpDiscoveryUserIdentifierPatterns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9942d4f50e6780b0cdbd213a57d6b617e8142bd6ef339d93419e1a5cefae65ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUserIdentifierPatterns", [value]))

    @jsii.member(jsii_name="resetAppExclude")
    def reset_app_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppExclude", []))

    @jsii.member(jsii_name="resetAppInclude")
    def reset_app_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppInclude", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdpId")
    def reset_idp_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdpId", []))

    @jsii.member(jsii_name="resetIdpType")
    def reset_idp_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdpType", []))

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

    @jsii.member(jsii_name="resetUserIdentifierAttribute")
    def reset_user_identifier_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserIdentifierAttribute", []))

    @jsii.member(jsii_name="resetUserIdentifierPatterns")
    def reset_user_identifier_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserIdentifierPatterns", []))

    @jsii.member(jsii_name="resetUserIdentifierType")
    def reset_user_identifier_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserIdentifierType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="appExclude")
    def app_exclude(self) -> "PolicyRuleIdpDiscoveryAppExcludeList":
        return typing.cast("PolicyRuleIdpDiscoveryAppExcludeList", jsii.get(self, "appExclude"))

    @builtins.property
    @jsii.member(jsii_name="appInclude")
    def app_include(self) -> "PolicyRuleIdpDiscoveryAppIncludeList":
        return typing.cast("PolicyRuleIdpDiscoveryAppIncludeList", jsii.get(self, "appInclude"))

    @builtins.property
    @jsii.member(jsii_name="platformInclude")
    def platform_include(self) -> "PolicyRuleIdpDiscoveryPlatformIncludeList":
        return typing.cast("PolicyRuleIdpDiscoveryPlatformIncludeList", jsii.get(self, "platformInclude"))

    @builtins.property
    @jsii.member(jsii_name="userIdentifierPatterns")
    def user_identifier_patterns(
        self,
    ) -> "PolicyRuleIdpDiscoveryUserIdentifierPatternsList":
        return typing.cast("PolicyRuleIdpDiscoveryUserIdentifierPatternsList", jsii.get(self, "userIdentifierPatterns"))

    @builtins.property
    @jsii.member(jsii_name="appExcludeInput")
    def app_exclude_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryAppExclude"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryAppExclude"]]], jsii.get(self, "appExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="appIncludeInput")
    def app_include_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryAppInclude"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryAppInclude"]]], jsii.get(self, "appIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="idpIdInput")
    def idp_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idpIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idpTypeInput")
    def idp_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idpTypeInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryPlatformInclude"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryPlatformInclude"]]], jsii.get(self, "platformIncludeInput"))

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
    @jsii.member(jsii_name="userIdentifierAttributeInput")
    def user_identifier_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdentifierAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdentifierPatternsInput")
    def user_identifier_patterns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryUserIdentifierPatterns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryUserIdentifierPatterns"]]], jsii.get(self, "userIdentifierPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdentifierTypeInput")
    def user_identifier_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdentifierTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf4e89e12c74ef478e1bc4db58aafb79cddd4ab0944a547c059a87d7ad885cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="idpId")
    def idp_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idpId"))

    @idp_id.setter
    def idp_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1e92672f5eb46866c16ceda48c7ee124b8c17d471425142abe50f31f6a3511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpId", value)

    @builtins.property
    @jsii.member(jsii_name="idpType")
    def idp_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idpType"))

    @idp_type.setter
    def idp_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb83c21d0202e634a81f0673b382299681618b9e6bfbc99974c9d5e67ee98a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d011a2186d77dc416d78e9e2caa7e68738b576bb2cf8741f6d650ce83d8da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkConnection")
    def network_connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkConnection"))

    @network_connection.setter
    def network_connection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c713839595c81e3cc20cb9f8a3a1895118a22598fd689a619ed578fc0d403638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConnection", value)

    @builtins.property
    @jsii.member(jsii_name="networkExcludes")
    def network_excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkExcludes"))

    @network_excludes.setter
    def network_excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f719d695e06bcac8497ba3ddab916d059dc3ace7a46240b8e7be444cd1106560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkExcludes", value)

    @builtins.property
    @jsii.member(jsii_name="networkIncludes")
    def network_includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkIncludes"))

    @network_includes.setter
    def network_includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ed80a9c3cf139067c45d8a408c16b2b913b208fb975bd50637c87014df007a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIncludes", value)

    @builtins.property
    @jsii.member(jsii_name="policyid")
    def policyid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyid"))

    @policyid.setter
    def policyid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8417acf47f3ef46ee21941782f5828a6e18c3afd3c11b4c6c08738bbfa6d5c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyid", value)

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca1eef397fe2066fb879a75f0a2018dcebda163b2f62a0630fdb16a65c43afec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea4a1970a61eb0dda7a387e20577f77bc02c96b2a7ddaccfb4e4d4cc79c1fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc23d3469fba6e574ceb7ac8a4c53f9d565d8ac2a982b02c1e725d87be2d3026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="userIdentifierAttribute")
    def user_identifier_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userIdentifierAttribute"))

    @user_identifier_attribute.setter
    def user_identifier_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf1a8f284c05ceff6c04bb73924ec33e5de6efe6f0bd43883ed14773b3796da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userIdentifierAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="userIdentifierType")
    def user_identifier_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userIdentifierType"))

    @user_identifier_type.setter
    def user_identifier_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447670623c02208dc494d87769c5acf9253adc0217680dd4699f8ce9e764939e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userIdentifierType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryAppExclude",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "id": "id", "name": "name"},
)
class PolicyRuleIdpDiscoveryAppExclude:
    def __init__(
        self,
        *,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#type PolicyRuleIdpDiscovery#type}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#id PolicyRuleIdpDiscovery#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#name PolicyRuleIdpDiscovery#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f08462840f5816346b3e8c8cd934067622f69d5496723a162e324e244439eb2)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#type PolicyRuleIdpDiscovery#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#id PolicyRuleIdpDiscovery#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#name PolicyRuleIdpDiscovery#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleIdpDiscoveryAppExclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyRuleIdpDiscoveryAppExcludeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryAppExcludeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a590603ce6ed1ec4da2302bcc60ef4e97dd045ab379310fe12edb858b2584b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PolicyRuleIdpDiscoveryAppExcludeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b089a06555c47fc4f11fd52fda58ca70eddb36fe20670abe464aad63a806401)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PolicyRuleIdpDiscoveryAppExcludeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e25a7e21d4b10d6cee9aa57ec45416f464afc4d1db30ccb86a752aecc0283e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1a0b96d02cf41f04dd36f8a3d5d6ea46704102e026741a554569bd82f7452fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bc7ab3c6ddfeae3f862d99b730a6895f4e3fdd7bfd7cbfbf728a6b2a7dc71f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppExclude]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppExclude]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppExclude]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__719278acc6c751642355e36c82528e0c59896745f15bb5a2e8aa81f3f64ee451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class PolicyRuleIdpDiscoveryAppExcludeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryAppExcludeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__103e74c05d71a3fd0eb5574a7543d781b72505f25b9f6b84a5675430df1f88cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def6867a42d6ebf15b256c5884cfdfe7e450e05463c8a260dbcf5ea0fa8c48da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__563ad12b6d1ce96cfb1ca4db3a8cb9c239e498b81b3e438d924b6a850bf18c82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba6f635344a7e3561c9962fed870ac303f2c34611331247393ebc23763f5c21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[PolicyRuleIdpDiscoveryAppExclude, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[PolicyRuleIdpDiscoveryAppExclude, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[PolicyRuleIdpDiscoveryAppExclude, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e9b687aaf0ebf4f8eae7768de605837e0d0037a3e7daaaa722a3a3cfeb1e782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryAppInclude",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "id": "id", "name": "name"},
)
class PolicyRuleIdpDiscoveryAppInclude:
    def __init__(
        self,
        *,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#type PolicyRuleIdpDiscovery#type}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#id PolicyRuleIdpDiscovery#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#name PolicyRuleIdpDiscovery#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1bd5b4e003ce87c7dd39ef8f5263395d181d7b9a327873273266290ccd3d53)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#type PolicyRuleIdpDiscovery#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#id PolicyRuleIdpDiscovery#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#name PolicyRuleIdpDiscovery#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleIdpDiscoveryAppInclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyRuleIdpDiscoveryAppIncludeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryAppIncludeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ab16a4f708340aa0dfdc053c58f3e3ce008137c7c7c30f097106ebbf6217ef7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PolicyRuleIdpDiscoveryAppIncludeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b3c083c692fdfb7cb087abdfab29fbd2a1b2fa78472284adf8569ba2af8223)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PolicyRuleIdpDiscoveryAppIncludeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47ea964d5d678882488f7debf594f05d36258ed0297ea8676b678cbc2818082)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9fc594971b9170167044c50600c0fb3cf89c7b412b1069c07e0dafbafea625c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0ac8d95d9a329bb3635a5a1f81eaf344f35ed58d958869d937ff85fceecdb68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppInclude]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppInclude]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppInclude]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ca24661159303338791a48e4488b371a79f038446e87ed5c2c9d913aa8cf46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class PolicyRuleIdpDiscoveryAppIncludeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryAppIncludeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b456d43de4c51b1a7b30506cfefc100c7c1b57324ca0187f87d72b2d9483e9a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff509b66023de4ceca46df932c56ce28fd131eee3a0bd51e01724b514030373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f9b81f9498abf3f8fe658342971e6f4798edee236ed4fb2268cb174ac990ab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd78971bc73d63eb1c1b44a6302ec1a539506dcae23283d4792eae2e96f5bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[PolicyRuleIdpDiscoveryAppInclude, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[PolicyRuleIdpDiscoveryAppInclude, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[PolicyRuleIdpDiscoveryAppInclude, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c8a2c89abd74849199257ccc43b34d04e8ee2725a78e8ef20681c72a1076b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryConfig",
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
        "app_exclude": "appExclude",
        "app_include": "appInclude",
        "id": "id",
        "idp_id": "idpId",
        "idp_type": "idpType",
        "network_connection": "networkConnection",
        "network_excludes": "networkExcludes",
        "network_includes": "networkIncludes",
        "platform_include": "platformInclude",
        "policyid": "policyid",
        "policy_id": "policyId",
        "priority": "priority",
        "status": "status",
        "user_identifier_attribute": "userIdentifierAttribute",
        "user_identifier_patterns": "userIdentifierPatterns",
        "user_identifier_type": "userIdentifierType",
    },
)
class PolicyRuleIdpDiscoveryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryAppExclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
        app_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryAppInclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        idp_id: typing.Optional[builtins.str] = None,
        idp_type: typing.Optional[builtins.str] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        platform_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleIdpDiscoveryPlatformInclude", typing.Dict[builtins.str, typing.Any]]]]] = None,
        policyid: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        user_identifier_attribute: typing.Optional[builtins.str] = None,
        user_identifier_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleIdpDiscoveryUserIdentifierPatterns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        user_identifier_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#name PolicyRuleIdpDiscovery#name}
        :param app_exclude: app_exclude block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#app_exclude PolicyRuleIdpDiscovery#app_exclude}
        :param app_include: app_include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#app_include PolicyRuleIdpDiscovery#app_include}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#id PolicyRuleIdpDiscovery#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idp_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#idp_id PolicyRuleIdpDiscovery#idp_id}.
        :param idp_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#idp_type PolicyRuleIdpDiscovery#idp_type}.
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#network_connection PolicyRuleIdpDiscovery#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#network_excludes PolicyRuleIdpDiscovery#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#network_includes PolicyRuleIdpDiscovery#network_includes}
        :param platform_include: platform_include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#platform_include PolicyRuleIdpDiscovery#platform_include}
        :param policyid: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#policyid PolicyRuleIdpDiscovery#policyid}
        :param policy_id: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#policy_id PolicyRuleIdpDiscovery#policy_id}
        :param priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#priority PolicyRuleIdpDiscovery#priority}
        :param status: Policy Rule Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#status PolicyRuleIdpDiscovery#status}
        :param user_identifier_attribute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#user_identifier_attribute PolicyRuleIdpDiscovery#user_identifier_attribute}.
        :param user_identifier_patterns: user_identifier_patterns block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#user_identifier_patterns PolicyRuleIdpDiscovery#user_identifier_patterns}
        :param user_identifier_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#user_identifier_type PolicyRuleIdpDiscovery#user_identifier_type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6925eb94d0a759a64fe2b357118f266667abd9221a979ded8f454aa4cef0d7df)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument app_exclude", value=app_exclude, expected_type=type_hints["app_exclude"])
            check_type(argname="argument app_include", value=app_include, expected_type=type_hints["app_include"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument idp_id", value=idp_id, expected_type=type_hints["idp_id"])
            check_type(argname="argument idp_type", value=idp_type, expected_type=type_hints["idp_type"])
            check_type(argname="argument network_connection", value=network_connection, expected_type=type_hints["network_connection"])
            check_type(argname="argument network_excludes", value=network_excludes, expected_type=type_hints["network_excludes"])
            check_type(argname="argument network_includes", value=network_includes, expected_type=type_hints["network_includes"])
            check_type(argname="argument platform_include", value=platform_include, expected_type=type_hints["platform_include"])
            check_type(argname="argument policyid", value=policyid, expected_type=type_hints["policyid"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument user_identifier_attribute", value=user_identifier_attribute, expected_type=type_hints["user_identifier_attribute"])
            check_type(argname="argument user_identifier_patterns", value=user_identifier_patterns, expected_type=type_hints["user_identifier_patterns"])
            check_type(argname="argument user_identifier_type", value=user_identifier_type, expected_type=type_hints["user_identifier_type"])
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
        if app_exclude is not None:
            self._values["app_exclude"] = app_exclude
        if app_include is not None:
            self._values["app_include"] = app_include
        if id is not None:
            self._values["id"] = id
        if idp_id is not None:
            self._values["idp_id"] = idp_id
        if idp_type is not None:
            self._values["idp_type"] = idp_type
        if network_connection is not None:
            self._values["network_connection"] = network_connection
        if network_excludes is not None:
            self._values["network_excludes"] = network_excludes
        if network_includes is not None:
            self._values["network_includes"] = network_includes
        if platform_include is not None:
            self._values["platform_include"] = platform_include
        if policyid is not None:
            self._values["policyid"] = policyid
        if policy_id is not None:
            self._values["policy_id"] = policy_id
        if priority is not None:
            self._values["priority"] = priority
        if status is not None:
            self._values["status"] = status
        if user_identifier_attribute is not None:
            self._values["user_identifier_attribute"] = user_identifier_attribute
        if user_identifier_patterns is not None:
            self._values["user_identifier_patterns"] = user_identifier_patterns
        if user_identifier_type is not None:
            self._values["user_identifier_type"] = user_identifier_type

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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#name PolicyRuleIdpDiscovery#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_exclude(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppExclude]]]:
        '''app_exclude block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#app_exclude PolicyRuleIdpDiscovery#app_exclude}
        '''
        result = self._values.get("app_exclude")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppExclude]]], result)

    @builtins.property
    def app_include(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppInclude]]]:
        '''app_include block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#app_include PolicyRuleIdpDiscovery#app_include}
        '''
        result = self._values.get("app_include")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppInclude]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#id PolicyRuleIdpDiscovery#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idp_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#idp_id PolicyRuleIdpDiscovery#idp_id}.'''
        result = self._values.get("idp_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idp_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#idp_type PolicyRuleIdpDiscovery#idp_type}.'''
        result = self._values.get("idp_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_connection(self) -> typing.Optional[builtins.str]:
        '''Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#network_connection PolicyRuleIdpDiscovery#network_connection}
        '''
        result = self._values.get("network_connection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#network_excludes PolicyRuleIdpDiscovery#network_excludes}
        '''
        result = self._values.get("network_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#network_includes PolicyRuleIdpDiscovery#network_includes}
        '''
        result = self._values.get("network_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def platform_include(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryPlatformInclude"]]]:
        '''platform_include block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#platform_include PolicyRuleIdpDiscovery#platform_include}
        '''
        result = self._values.get("platform_include")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryPlatformInclude"]]], result)

    @builtins.property
    def policyid(self) -> typing.Optional[builtins.str]:
        '''Policy ID of the Rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#policyid PolicyRuleIdpDiscovery#policyid}
        '''
        result = self._values.get("policyid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''Policy ID of the Rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#policy_id PolicyRuleIdpDiscovery#policy_id}
        '''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Policy Rule Priority, this attribute can be set to a valid priority.

        To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#priority PolicyRuleIdpDiscovery#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Policy Rule Status: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#status PolicyRuleIdpDiscovery#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_identifier_attribute(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#user_identifier_attribute PolicyRuleIdpDiscovery#user_identifier_attribute}.'''
        result = self._values.get("user_identifier_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_identifier_patterns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryUserIdentifierPatterns"]]]:
        '''user_identifier_patterns block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#user_identifier_patterns PolicyRuleIdpDiscovery#user_identifier_patterns}
        '''
        result = self._values.get("user_identifier_patterns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleIdpDiscoveryUserIdentifierPatterns"]]], result)

    @builtins.property
    def user_identifier_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#user_identifier_type PolicyRuleIdpDiscovery#user_identifier_type}.'''
        result = self._values.get("user_identifier_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleIdpDiscoveryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryPlatformInclude",
    jsii_struct_bases=[],
    name_mapping={
        "os_expression": "osExpression",
        "os_type": "osType",
        "type": "type",
    },
)
class PolicyRuleIdpDiscoveryPlatformInclude:
    def __init__(
        self,
        *,
        os_expression: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_expression: Only available with OTHER OS type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#os_expression PolicyRuleIdpDiscovery#os_expression}
        :param os_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#os_type PolicyRuleIdpDiscovery#os_type}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#type PolicyRuleIdpDiscovery#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7940b3c32cc76941a4dcaa9b9eadc06d285b143b846911a09d69f2505e7a4076)
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#os_expression PolicyRuleIdpDiscovery#os_expression}
        '''
        result = self._values.get("os_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#os_type PolicyRuleIdpDiscovery#os_type}.'''
        result = self._values.get("os_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#type PolicyRuleIdpDiscovery#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleIdpDiscoveryPlatformInclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyRuleIdpDiscoveryPlatformIncludeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryPlatformIncludeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2462133a752bcdba6216f070c0f6ac66e59044384fea5a99beb8c0fe782b86e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PolicyRuleIdpDiscoveryPlatformIncludeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2117a9ce8fedafbf0134107b2174eded8211535353de599307e5a722b5b480de)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PolicyRuleIdpDiscoveryPlatformIncludeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f80ed75bf763ee83011c0efe4f283cf35b47775c513257ebd8d0303281aba882)
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
            type_hints = typing.get_type_hints(_typecheckingstub__906d7e1bb704c07a6919484fdabfec5899ea8a608a31cf4ed12324f1adad0195)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dee8d6d2916a1e6d2d8c816f64d57255e12d82769d68698a9ac501eae2d5a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryPlatformInclude]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryPlatformInclude]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryPlatformInclude]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66aa0e751e7b9b7201c59c8ddcd41fc78d31394e8ad9f487f6829707e0e4417f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class PolicyRuleIdpDiscoveryPlatformIncludeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryPlatformIncludeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fd5c6b7a4e64a43149b7b5431b328313b6187f95df2b891699c1f479151e904)
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
            type_hints = typing.get_type_hints(_typecheckingstub__888bedd103b5f34cf232c3fa94e6a89dc0dd9cef593195753969ff0b3aa8f33f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osExpression", value)

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0426da8351c046555b093eb04762ccf80bac32233c1f7d5e041b6c60f2040426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b0d12a7509a8cd1bca1724db0d321436be19aabbda836b920211e7c9d08ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[PolicyRuleIdpDiscoveryPlatformInclude, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[PolicyRuleIdpDiscoveryPlatformInclude, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[PolicyRuleIdpDiscoveryPlatformInclude, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b19942b0e581a3874533f099fef01a05337cc057126f4285e837c13b23343f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryUserIdentifierPatterns",
    jsii_struct_bases=[],
    name_mapping={"match_type": "matchType", "value": "value"},
)
class PolicyRuleIdpDiscoveryUserIdentifierPatterns:
    def __init__(
        self,
        *,
        match_type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#match_type PolicyRuleIdpDiscovery#match_type}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#value PolicyRuleIdpDiscovery#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae9f353d116fa796d4bb200c764bbf9c1881eb2cd0674db2911dfc9239cb09c)
            check_type(argname="argument match_type", value=match_type, expected_type=type_hints["match_type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_type is not None:
            self._values["match_type"] = match_type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def match_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#match_type PolicyRuleIdpDiscovery#match_type}.'''
        result = self._values.get("match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_idp_discovery#value PolicyRuleIdpDiscovery#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleIdpDiscoveryUserIdentifierPatterns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyRuleIdpDiscoveryUserIdentifierPatternsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryUserIdentifierPatternsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68db5036fe290ab2f65f75f497c8a5a5f604d7eccfe45928bc2033db61895261)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PolicyRuleIdpDiscoveryUserIdentifierPatternsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61b4d3bf8a3277b6b54cd543c61470a5621075f7adf8b2de3bc39f26ac2e864)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PolicyRuleIdpDiscoveryUserIdentifierPatternsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__948409fe84cb2756f4b4107806454b04921e84d9272ec8598c184f45248c08d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d27f4ba761ba8fb10a50a3e4e75b6f3468608594b0c0d8771d8ed17c1982ea6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f883d8c7af7babb41064efdd349a993f753a889cd8cc6725767b16056f6c1e6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryUserIdentifierPatterns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryUserIdentifierPatterns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryUserIdentifierPatterns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671211ad9bd1e9cc89595d0e475ee0c5bb6e2232c7e7367ecd0dc960dfad497c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class PolicyRuleIdpDiscoveryUserIdentifierPatternsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleIdpDiscovery.PolicyRuleIdpDiscoveryUserIdentifierPatternsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90afbce2f1418424fab8e1ee8ad034c0d29c0056ce45449efc70f35c562288f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchType")
    def reset_match_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="matchTypeInput")
    def match_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="matchType")
    def match_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchType"))

    @match_type.setter
    def match_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c0262b61d85d9de4782d7303670bea1fb986d55265692c33ac2a215dff25ad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchType", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dcaacdec8d148d39e05d778a98325a01d78ad2f67c1b37a383aa12aa4e8dd78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[PolicyRuleIdpDiscoveryUserIdentifierPatterns, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[PolicyRuleIdpDiscoveryUserIdentifierPatterns, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[PolicyRuleIdpDiscoveryUserIdentifierPatterns, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57462a95b00ac191d52ae918e5d886bd190913e5001a0f214aa6b7d339d97480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "PolicyRuleIdpDiscovery",
    "PolicyRuleIdpDiscoveryAppExclude",
    "PolicyRuleIdpDiscoveryAppExcludeList",
    "PolicyRuleIdpDiscoveryAppExcludeOutputReference",
    "PolicyRuleIdpDiscoveryAppInclude",
    "PolicyRuleIdpDiscoveryAppIncludeList",
    "PolicyRuleIdpDiscoveryAppIncludeOutputReference",
    "PolicyRuleIdpDiscoveryConfig",
    "PolicyRuleIdpDiscoveryPlatformInclude",
    "PolicyRuleIdpDiscoveryPlatformIncludeList",
    "PolicyRuleIdpDiscoveryPlatformIncludeOutputReference",
    "PolicyRuleIdpDiscoveryUserIdentifierPatterns",
    "PolicyRuleIdpDiscoveryUserIdentifierPatternsList",
    "PolicyRuleIdpDiscoveryUserIdentifierPatternsOutputReference",
]

publication.publish()

def _typecheckingstub__40c78decd6dec0eeb7765c396dde464f85b6a31152cbca3449a190d9f0d9f00a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    app_exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryAppExclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryAppInclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    idp_id: typing.Optional[builtins.str] = None,
    idp_type: typing.Optional[builtins.str] = None,
    network_connection: typing.Optional[builtins.str] = None,
    network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    platform_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryPlatformInclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    policyid: typing.Optional[builtins.str] = None,
    policy_id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    user_identifier_attribute: typing.Optional[builtins.str] = None,
    user_identifier_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryUserIdentifierPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    user_identifier_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b1730bb1666ec36f050deae0531218cfe0219876c489b34c9d181dc782075d99(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryAppExclude, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183a0fd51bf52e63b295443ea7ca2e78738c20ed41e0bfe25e4890298b9f58a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryAppInclude, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa411b8ec838ca4410f39d43d9777b0fc5d83b4a4bec30c091909c3462e4fcc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryPlatformInclude, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9942d4f50e6780b0cdbd213a57d6b617e8142bd6ef339d93419e1a5cefae65ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryUserIdentifierPatterns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf4e89e12c74ef478e1bc4db58aafb79cddd4ab0944a547c059a87d7ad885cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1e92672f5eb46866c16ceda48c7ee124b8c17d471425142abe50f31f6a3511(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb83c21d0202e634a81f0673b382299681618b9e6bfbc99974c9d5e67ee98a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d011a2186d77dc416d78e9e2caa7e68738b576bb2cf8741f6d650ce83d8da5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c713839595c81e3cc20cb9f8a3a1895118a22598fd689a619ed578fc0d403638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f719d695e06bcac8497ba3ddab916d059dc3ace7a46240b8e7be444cd1106560(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ed80a9c3cf139067c45d8a408c16b2b913b208fb975bd50637c87014df007a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8417acf47f3ef46ee21941782f5828a6e18c3afd3c11b4c6c08738bbfa6d5c52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1eef397fe2066fb879a75f0a2018dcebda163b2f62a0630fdb16a65c43afec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea4a1970a61eb0dda7a387e20577f77bc02c96b2a7ddaccfb4e4d4cc79c1fcf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc23d3469fba6e574ceb7ac8a4c53f9d565d8ac2a982b02c1e725d87be2d3026(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf1a8f284c05ceff6c04bb73924ec33e5de6efe6f0bd43883ed14773b3796da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447670623c02208dc494d87769c5acf9253adc0217680dd4699f8ce9e764939e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f08462840f5816346b3e8c8cd934067622f69d5496723a162e324e244439eb2(
    *,
    type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a590603ce6ed1ec4da2302bcc60ef4e97dd045ab379310fe12edb858b2584b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b089a06555c47fc4f11fd52fda58ca70eddb36fe20670abe464aad63a806401(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e25a7e21d4b10d6cee9aa57ec45416f464afc4d1db30ccb86a752aecc0283e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a0b96d02cf41f04dd36f8a3d5d6ea46704102e026741a554569bd82f7452fb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc7ab3c6ddfeae3f862d99b730a6895f4e3fdd7bfd7cbfbf728a6b2a7dc71f0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719278acc6c751642355e36c82528e0c59896745f15bb5a2e8aa81f3f64ee451(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppExclude]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103e74c05d71a3fd0eb5574a7543d781b72505f25b9f6b84a5675430df1f88cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def6867a42d6ebf15b256c5884cfdfe7e450e05463c8a260dbcf5ea0fa8c48da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__563ad12b6d1ce96cfb1ca4db3a8cb9c239e498b81b3e438d924b6a850bf18c82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba6f635344a7e3561c9962fed870ac303f2c34611331247393ebc23763f5c21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9b687aaf0ebf4f8eae7768de605837e0d0037a3e7daaaa722a3a3cfeb1e782(
    value: typing.Optional[typing.Union[PolicyRuleIdpDiscoveryAppExclude, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1bd5b4e003ce87c7dd39ef8f5263395d181d7b9a327873273266290ccd3d53(
    *,
    type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab16a4f708340aa0dfdc053c58f3e3ce008137c7c7c30f097106ebbf6217ef7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b3c083c692fdfb7cb087abdfab29fbd2a1b2fa78472284adf8569ba2af8223(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47ea964d5d678882488f7debf594f05d36258ed0297ea8676b678cbc2818082(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fc594971b9170167044c50600c0fb3cf89c7b412b1069c07e0dafbafea625c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ac8d95d9a329bb3635a5a1f81eaf344f35ed58d958869d937ff85fceecdb68(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ca24661159303338791a48e4488b371a79f038446e87ed5c2c9d913aa8cf46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryAppInclude]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b456d43de4c51b1a7b30506cfefc100c7c1b57324ca0187f87d72b2d9483e9a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff509b66023de4ceca46df932c56ce28fd131eee3a0bd51e01724b514030373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9b81f9498abf3f8fe658342971e6f4798edee236ed4fb2268cb174ac990ab8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd78971bc73d63eb1c1b44a6302ec1a539506dcae23283d4792eae2e96f5bf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c8a2c89abd74849199257ccc43b34d04e8ee2725a78e8ef20681c72a1076b0(
    value: typing.Optional[typing.Union[PolicyRuleIdpDiscoveryAppInclude, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6925eb94d0a759a64fe2b357118f266667abd9221a979ded8f454aa4cef0d7df(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    app_exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryAppExclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryAppInclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    idp_id: typing.Optional[builtins.str] = None,
    idp_type: typing.Optional[builtins.str] = None,
    network_connection: typing.Optional[builtins.str] = None,
    network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    platform_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryPlatformInclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    policyid: typing.Optional[builtins.str] = None,
    policy_id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    user_identifier_attribute: typing.Optional[builtins.str] = None,
    user_identifier_patterns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleIdpDiscoveryUserIdentifierPatterns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    user_identifier_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7940b3c32cc76941a4dcaa9b9eadc06d285b143b846911a09d69f2505e7a4076(
    *,
    os_expression: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2462133a752bcdba6216f070c0f6ac66e59044384fea5a99beb8c0fe782b86e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2117a9ce8fedafbf0134107b2174eded8211535353de599307e5a722b5b480de(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80ed75bf763ee83011c0efe4f283cf35b47775c513257ebd8d0303281aba882(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906d7e1bb704c07a6919484fdabfec5899ea8a608a31cf4ed12324f1adad0195(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dee8d6d2916a1e6d2d8c816f64d57255e12d82769d68698a9ac501eae2d5a47(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66aa0e751e7b9b7201c59c8ddcd41fc78d31394e8ad9f487f6829707e0e4417f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryPlatformInclude]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd5c6b7a4e64a43149b7b5431b328313b6187f95df2b891699c1f479151e904(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888bedd103b5f34cf232c3fa94e6a89dc0dd9cef593195753969ff0b3aa8f33f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0426da8351c046555b093eb04762ccf80bac32233c1f7d5e041b6c60f2040426(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b0d12a7509a8cd1bca1724db0d321436be19aabbda836b920211e7c9d08ae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b19942b0e581a3874533f099fef01a05337cc057126f4285e837c13b23343f(
    value: typing.Optional[typing.Union[PolicyRuleIdpDiscoveryPlatformInclude, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae9f353d116fa796d4bb200c764bbf9c1881eb2cd0674db2911dfc9239cb09c(
    *,
    match_type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68db5036fe290ab2f65f75f497c8a5a5f604d7eccfe45928bc2033db61895261(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61b4d3bf8a3277b6b54cd543c61470a5621075f7adf8b2de3bc39f26ac2e864(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948409fe84cb2756f4b4107806454b04921e84d9272ec8598c184f45248c08d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d27f4ba761ba8fb10a50a3e4e75b6f3468608594b0c0d8771d8ed17c1982ea6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f883d8c7af7babb41064efdd349a993f753a889cd8cc6725767b16056f6c1e6c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671211ad9bd1e9cc89595d0e475ee0c5bb6e2232c7e7367ecd0dc960dfad497c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleIdpDiscoveryUserIdentifierPatterns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90afbce2f1418424fab8e1ee8ad034c0d29c0056ce45449efc70f35c562288f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c0262b61d85d9de4782d7303670bea1fb986d55265692c33ac2a215dff25ad7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dcaacdec8d148d39e05d778a98325a01d78ad2f67c1b37a383aa12aa4e8dd78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57462a95b00ac191d52ae918e5d886bd190913e5001a0f214aa6b7d339d97480(
    value: typing.Optional[typing.Union[PolicyRuleIdpDiscoveryUserIdentifierPatterns, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
