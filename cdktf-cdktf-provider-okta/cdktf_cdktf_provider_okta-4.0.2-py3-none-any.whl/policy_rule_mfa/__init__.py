'''
# `okta_policy_rule_mfa`

Refer to the Terraform Registory for docs: [`okta_policy_rule_mfa`](https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa).
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


class PolicyRuleMfa(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleMfa.PolicyRuleMfa",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa okta_policy_rule_mfa}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        app_exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleMfaAppExclude", typing.Dict[builtins.str, typing.Any]]]]] = None,
        app_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleMfaAppInclude", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enroll: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa okta_policy_rule_mfa} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#name PolicyRuleMfa#name}
        :param app_exclude: app_exclude block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#app_exclude PolicyRuleMfa#app_exclude}
        :param app_include: app_include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#app_include PolicyRuleMfa#app_include}
        :param enroll: Should the user be enrolled the first time they LOGIN, the next time they are CHALLENGED, or NEVER? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#enroll PolicyRuleMfa#enroll}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#id PolicyRuleMfa#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#network_connection PolicyRuleMfa#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#network_excludes PolicyRuleMfa#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#network_includes PolicyRuleMfa#network_includes}
        :param policyid: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#policyid PolicyRuleMfa#policyid}
        :param policy_id: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#policy_id PolicyRuleMfa#policy_id}
        :param priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#priority PolicyRuleMfa#priority}
        :param status: Policy Rule Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#status PolicyRuleMfa#status}
        :param users_excluded: Set of User IDs to Exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#users_excluded PolicyRuleMfa#users_excluded}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4663cdd10d5c8d8aee60584a4f18da071f3c4d4fe294bcac842f043865c28a7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PolicyRuleMfaConfig(
            name=name,
            app_exclude=app_exclude,
            app_include=app_include,
            enroll=enroll,
            id=id,
            network_connection=network_connection,
            network_excludes=network_excludes,
            network_includes=network_includes,
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

    @jsii.member(jsii_name="putAppExclude")
    def put_app_exclude(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleMfaAppExclude", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108933d353dce5c8f061366533122ce1940d91a25d0497aa43bc321901564933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAppExclude", [value]))

    @jsii.member(jsii_name="putAppInclude")
    def put_app_include(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PolicyRuleMfaAppInclude", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc11a8f9890e2e06d805e26c0c96fa36fd77213a979b05acf20d555b799dcf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAppInclude", [value]))

    @jsii.member(jsii_name="resetAppExclude")
    def reset_app_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppExclude", []))

    @jsii.member(jsii_name="resetAppInclude")
    def reset_app_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppInclude", []))

    @jsii.member(jsii_name="resetEnroll")
    def reset_enroll(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnroll", []))

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
    @jsii.member(jsii_name="appExclude")
    def app_exclude(self) -> "PolicyRuleMfaAppExcludeList":
        return typing.cast("PolicyRuleMfaAppExcludeList", jsii.get(self, "appExclude"))

    @builtins.property
    @jsii.member(jsii_name="appInclude")
    def app_include(self) -> "PolicyRuleMfaAppIncludeList":
        return typing.cast("PolicyRuleMfaAppIncludeList", jsii.get(self, "appInclude"))

    @builtins.property
    @jsii.member(jsii_name="appExcludeInput")
    def app_exclude_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleMfaAppExclude"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleMfaAppExclude"]]], jsii.get(self, "appExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="appIncludeInput")
    def app_include_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleMfaAppInclude"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PolicyRuleMfaAppInclude"]]], jsii.get(self, "appIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="enrollInput")
    def enroll_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enrollInput"))

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
    @jsii.member(jsii_name="enroll")
    def enroll(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enroll"))

    @enroll.setter
    def enroll(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7943931e2dd7d90df7fae6040b0cf862e71b515a36f0f3ba92a16c44e61f40c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enroll", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b89a8efc1512f69dd277aae11d216683b9a6d368b7e7663d560947d08fb142b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139c50f7776e05ab856b9b1f959a8a8144c1f394f67a9ba006df980c7225b61a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkConnection")
    def network_connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkConnection"))

    @network_connection.setter
    def network_connection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b6a02d4266bce775bb74faa4125a0af40681cc1c65e871a13d348b512d79d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConnection", value)

    @builtins.property
    @jsii.member(jsii_name="networkExcludes")
    def network_excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkExcludes"))

    @network_excludes.setter
    def network_excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2db7aa53458ca7e9cbe35edc110ba56fd69aa07f79567fb37ede04a206db9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkExcludes", value)

    @builtins.property
    @jsii.member(jsii_name="networkIncludes")
    def network_includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkIncludes"))

    @network_includes.setter
    def network_includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76cdf6e4663891e49465f3f08701a3fa6df8eac1242e39a3477dc890f01b745d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIncludes", value)

    @builtins.property
    @jsii.member(jsii_name="policyid")
    def policyid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyid"))

    @policyid.setter
    def policyid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359217ac4ee1897602da64037dc841f99867f274bd0239bc0b802dfba02ad748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyid", value)

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84f3af5de9cea0993d73791a42a71fafba8c05e892f6e7110e7633134ba4685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446ac28238475be9a02b8b2870fa6cc552496a8138d80e903061d7925383fe54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6ab5bb9654a3a2556feadc9ec2ef8c3b4c392f6b8e5ab29410cd7fb556110b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="usersExcluded")
    def users_excluded(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "usersExcluded"))

    @users_excluded.setter
    def users_excluded(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb4ef11cd417f5ce475bccc7a0f00debb54083c59af08db72479e072b704f36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usersExcluded", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleMfa.PolicyRuleMfaAppExclude",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "id": "id", "name": "name"},
)
class PolicyRuleMfaAppExclude:
    def __init__(
        self,
        *,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#type PolicyRuleMfa#type}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#id PolicyRuleMfa#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#name PolicyRuleMfa#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08aac4277c0ba9c15944b37f94ad24d26c9275302df9bcf7c0fed4a633016280)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#type PolicyRuleMfa#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#id PolicyRuleMfa#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#name PolicyRuleMfa#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleMfaAppExclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyRuleMfaAppExcludeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleMfa.PolicyRuleMfaAppExcludeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de8e1650f2dc2d3bf317ea03b8a4967f9301223815e610ef373223ec5be29d54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "PolicyRuleMfaAppExcludeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826725eb91362874c9fad3f259c3e6742fc1b6924372eeaac350a10f7cd9d30c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PolicyRuleMfaAppExcludeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b727e8d65a639bde91ccd82ca11f4ff0addef8a02b62ec4b87cacb329f066f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__509d92b70958741864ff76b76296a00462b0580ef552fa9ca90cac7558069e31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__297526bb13fb8b66af8ce9832b5a631de570a1cec7f6be2bcd2fe91deb9ce1c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppExclude]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppExclude]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppExclude]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1270a36157a48f15374ec54331fcb3e5665e4c1825061e4c641c9881254c6b2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class PolicyRuleMfaAppExcludeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleMfa.PolicyRuleMfaAppExcludeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2206ecd39e443068957eb0ca79f3df6cd6c08acb898c038d196a012de53efc33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6e5a658852005be141af386e23853fb23049986fffc1eb1c5f91109f928709a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2fe4cf3d8a689e4cc441109473e33cd3b114cb0cc5cbe4cc28b152f3f8174b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655468f777e9ee4c1c6b20fe11c3a940e7a2538a3e2da1efec9752acbef4ad5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[PolicyRuleMfaAppExclude, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[PolicyRuleMfaAppExclude, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[PolicyRuleMfaAppExclude, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b857ef4287ce13c6b04322ef54741bceb28009bc56e124433fe1bf3eb5ecc216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleMfa.PolicyRuleMfaAppInclude",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "id": "id", "name": "name"},
)
class PolicyRuleMfaAppInclude:
    def __init__(
        self,
        *,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#type PolicyRuleMfa#type}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#id PolicyRuleMfa#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#name PolicyRuleMfa#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4645c411916f6d56291ef2c1171a5bbf12607eb6fad385652cff561a61ef1c2)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#type PolicyRuleMfa#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#id PolicyRuleMfa#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#name PolicyRuleMfa#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleMfaAppInclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyRuleMfaAppIncludeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleMfa.PolicyRuleMfaAppIncludeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6db04be9d05c1a0871c8c22d67d995b40f46c0b468a3882a8dcd05cbf562d214)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "PolicyRuleMfaAppIncludeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bd3b4594277bc5f90b420d17a15dda44a8ff3525b784f41014eacde53f0787)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PolicyRuleMfaAppIncludeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd0c52682b3243c7c7077746e8ee340261eb6922d38311bfd0db52b77f4b463)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55ef4b2efb1898d959bedc016fdb5f688830bcc7030818d499128fd412b89737)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3e1429f0d1a4316fdf56e4375239163f43cfe972b801944f75e515f8b457255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppInclude]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppInclude]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppInclude]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e65d2eea6d6f61902bbe13a1d6e2a14d91bc628c20e3806c9f9da5a2f88b090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class PolicyRuleMfaAppIncludeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleMfa.PolicyRuleMfaAppIncludeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3131108af9fe4f0dc2973471c5e76a3732c5127d1bc4a1976097cd2233483cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6776dc5bd9175f854c8b7a2a0e512249a799f28264e0b69c3c28785b1a6538f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51bdb22cf46088af63447fc09d90ef6afb0c7440350fa0c6ea76ef204786d517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b890faaff30f417be1537480af35978b347134a564ef542a6eb25db01949127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[PolicyRuleMfaAppInclude, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[PolicyRuleMfaAppInclude, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[PolicyRuleMfaAppInclude, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e09f045a6f0f74cd8b8bb324343bc713acb56f6c4bf8db9147b5c4ac376bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleMfa.PolicyRuleMfaConfig",
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
        "enroll": "enroll",
        "id": "id",
        "network_connection": "networkConnection",
        "network_excludes": "networkExcludes",
        "network_includes": "networkIncludes",
        "policyid": "policyid",
        "policy_id": "policyId",
        "priority": "priority",
        "status": "status",
        "users_excluded": "usersExcluded",
    },
)
class PolicyRuleMfaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleMfaAppExclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
        app_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleMfaAppInclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
        enroll: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#name PolicyRuleMfa#name}
        :param app_exclude: app_exclude block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#app_exclude PolicyRuleMfa#app_exclude}
        :param app_include: app_include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#app_include PolicyRuleMfa#app_include}
        :param enroll: Should the user be enrolled the first time they LOGIN, the next time they are CHALLENGED, or NEVER? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#enroll PolicyRuleMfa#enroll}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#id PolicyRuleMfa#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#network_connection PolicyRuleMfa#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#network_excludes PolicyRuleMfa#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#network_includes PolicyRuleMfa#network_includes}
        :param policyid: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#policyid PolicyRuleMfa#policyid}
        :param policy_id: Policy ID of the Rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#policy_id PolicyRuleMfa#policy_id}
        :param priority: Policy Rule Priority, this attribute can be set to a valid priority. To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#priority PolicyRuleMfa#priority}
        :param status: Policy Rule Status: ACTIVE or INACTIVE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#status PolicyRuleMfa#status}
        :param users_excluded: Set of User IDs to Exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#users_excluded PolicyRuleMfa#users_excluded}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fea0cbbbf2d87c3254a68f3d9ee1cee03aafe9f9e7ca76518c5d9d9e1fa4ad7)
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
            check_type(argname="argument enroll", value=enroll, expected_type=type_hints["enroll"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument network_connection", value=network_connection, expected_type=type_hints["network_connection"])
            check_type(argname="argument network_excludes", value=network_excludes, expected_type=type_hints["network_excludes"])
            check_type(argname="argument network_includes", value=network_includes, expected_type=type_hints["network_includes"])
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
        if app_exclude is not None:
            self._values["app_exclude"] = app_exclude
        if app_include is not None:
            self._values["app_include"] = app_include
        if enroll is not None:
            self._values["enroll"] = enroll
        if id is not None:
            self._values["id"] = id
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#name PolicyRuleMfa#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_exclude(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppExclude]]]:
        '''app_exclude block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#app_exclude PolicyRuleMfa#app_exclude}
        '''
        result = self._values.get("app_exclude")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppExclude]]], result)

    @builtins.property
    def app_include(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppInclude]]]:
        '''app_include block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#app_include PolicyRuleMfa#app_include}
        '''
        result = self._values.get("app_include")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppInclude]]], result)

    @builtins.property
    def enroll(self) -> typing.Optional[builtins.str]:
        '''Should the user be enrolled the first time they LOGIN, the next time they are CHALLENGED, or NEVER?

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#enroll PolicyRuleMfa#enroll}
        '''
        result = self._values.get("enroll")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#id PolicyRuleMfa#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_connection(self) -> typing.Optional[builtins.str]:
        '''Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#network_connection PolicyRuleMfa#network_connection}
        '''
        result = self._values.get("network_connection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#network_excludes PolicyRuleMfa#network_excludes}
        '''
        result = self._values.get("network_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#network_includes PolicyRuleMfa#network_includes}
        '''
        result = self._values.get("network_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def policyid(self) -> typing.Optional[builtins.str]:
        '''Policy ID of the Rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#policyid PolicyRuleMfa#policyid}
        '''
        result = self._values.get("policyid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''Policy ID of the Rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#policy_id PolicyRuleMfa#policy_id}
        '''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Policy Rule Priority, this attribute can be set to a valid priority.

        To avoid endless diff situation we error if an invalid priority is provided. API defaults it to the last (lowest) if not there.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#priority PolicyRuleMfa#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Policy Rule Status: ACTIVE or INACTIVE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#status PolicyRuleMfa#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users_excluded(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of User IDs to Exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_mfa#users_excluded PolicyRuleMfa#users_excluded}
        '''
        result = self._values.get("users_excluded")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleMfaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PolicyRuleMfa",
    "PolicyRuleMfaAppExclude",
    "PolicyRuleMfaAppExcludeList",
    "PolicyRuleMfaAppExcludeOutputReference",
    "PolicyRuleMfaAppInclude",
    "PolicyRuleMfaAppIncludeList",
    "PolicyRuleMfaAppIncludeOutputReference",
    "PolicyRuleMfaConfig",
]

publication.publish()

def _typecheckingstub__4663cdd10d5c8d8aee60584a4f18da071f3c4d4fe294bcac842f043865c28a7f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    app_exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleMfaAppExclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleMfaAppInclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enroll: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    network_connection: typing.Optional[builtins.str] = None,
    network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__108933d353dce5c8f061366533122ce1940d91a25d0497aa43bc321901564933(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleMfaAppExclude, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc11a8f9890e2e06d805e26c0c96fa36fd77213a979b05acf20d555b799dcf9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleMfaAppInclude, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7943931e2dd7d90df7fae6040b0cf862e71b515a36f0f3ba92a16c44e61f40c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b89a8efc1512f69dd277aae11d216683b9a6d368b7e7663d560947d08fb142b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139c50f7776e05ab856b9b1f959a8a8144c1f394f67a9ba006df980c7225b61a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b6a02d4266bce775bb74faa4125a0af40681cc1c65e871a13d348b512d79d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2db7aa53458ca7e9cbe35edc110ba56fd69aa07f79567fb37ede04a206db9bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76cdf6e4663891e49465f3f08701a3fa6df8eac1242e39a3477dc890f01b745d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359217ac4ee1897602da64037dc841f99867f274bd0239bc0b802dfba02ad748(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84f3af5de9cea0993d73791a42a71fafba8c05e892f6e7110e7633134ba4685(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446ac28238475be9a02b8b2870fa6cc552496a8138d80e903061d7925383fe54(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6ab5bb9654a3a2556feadc9ec2ef8c3b4c392f6b8e5ab29410cd7fb556110b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb4ef11cd417f5ce475bccc7a0f00debb54083c59af08db72479e072b704f36(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08aac4277c0ba9c15944b37f94ad24d26c9275302df9bcf7c0fed4a633016280(
    *,
    type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8e1650f2dc2d3bf317ea03b8a4967f9301223815e610ef373223ec5be29d54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826725eb91362874c9fad3f259c3e6742fc1b6924372eeaac350a10f7cd9d30c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b727e8d65a639bde91ccd82ca11f4ff0addef8a02b62ec4b87cacb329f066f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509d92b70958741864ff76b76296a00462b0580ef552fa9ca90cac7558069e31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297526bb13fb8b66af8ce9832b5a631de570a1cec7f6be2bcd2fe91deb9ce1c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1270a36157a48f15374ec54331fcb3e5665e4c1825061e4c641c9881254c6b2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppExclude]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2206ecd39e443068957eb0ca79f3df6cd6c08acb898c038d196a012de53efc33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e5a658852005be141af386e23853fb23049986fffc1eb1c5f91109f928709a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2fe4cf3d8a689e4cc441109473e33cd3b114cb0cc5cbe4cc28b152f3f8174b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655468f777e9ee4c1c6b20fe11c3a940e7a2538a3e2da1efec9752acbef4ad5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b857ef4287ce13c6b04322ef54741bceb28009bc56e124433fe1bf3eb5ecc216(
    value: typing.Optional[typing.Union[PolicyRuleMfaAppExclude, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4645c411916f6d56291ef2c1171a5bbf12607eb6fad385652cff561a61ef1c2(
    *,
    type: builtins.str,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db04be9d05c1a0871c8c22d67d995b40f46c0b468a3882a8dcd05cbf562d214(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bd3b4594277bc5f90b420d17a15dda44a8ff3525b784f41014eacde53f0787(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd0c52682b3243c7c7077746e8ee340261eb6922d38311bfd0db52b77f4b463(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ef4b2efb1898d959bedc016fdb5f688830bcc7030818d499128fd412b89737(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e1429f0d1a4316fdf56e4375239163f43cfe972b801944f75e515f8b457255(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e65d2eea6d6f61902bbe13a1d6e2a14d91bc628c20e3806c9f9da5a2f88b090(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PolicyRuleMfaAppInclude]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3131108af9fe4f0dc2973471c5e76a3732c5127d1bc4a1976097cd2233483cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6776dc5bd9175f854c8b7a2a0e512249a799f28264e0b69c3c28785b1a6538f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bdb22cf46088af63447fc09d90ef6afb0c7440350fa0c6ea76ef204786d517(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b890faaff30f417be1537480af35978b347134a564ef542a6eb25db01949127(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e09f045a6f0f74cd8b8bb324343bc713acb56f6c4bf8db9147b5c4ac376bf9(
    value: typing.Optional[typing.Union[PolicyRuleMfaAppInclude, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fea0cbbbf2d87c3254a68f3d9ee1cee03aafe9f9e7ca76518c5d9d9e1fa4ad7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    app_exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleMfaAppExclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_include: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PolicyRuleMfaAppInclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enroll: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    network_connection: typing.Optional[builtins.str] = None,
    network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    policyid: typing.Optional[builtins.str] = None,
    policy_id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
