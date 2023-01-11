'''
# `cloudflare_access_policy`

Refer to the Terraform Registory for docs: [`cloudflare_access_policy`](https://www.terraform.io/docs/providers/cloudflare/r/access_policy).
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


class AccessPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicy",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy cloudflare_access_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        application_id: builtins.str,
        decision: builtins.str,
        include: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyInclude", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        precedence: jsii.Number,
        account_id: typing.Optional[builtins.str] = None,
        approval_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyApprovalGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyExclude", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        purpose_justification_prompt: typing.Optional[builtins.str] = None,
        purpose_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyRequire", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zone_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy cloudflare_access_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param application_id: The ID of the application the policy is associated with. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#application_id AccessPolicy#application_id}
        :param decision: Defines the action Access will take if the policy matches the user. Available values: ``allow``, ``deny``, ``non_identity``, ``bypass``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#decision AccessPolicy#decision}
        :param include: include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#include AccessPolicy#include}
        :param name: Friendly name of the Access Policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}
        :param precedence: The unique precedence for policies on a single application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#precedence AccessPolicy#precedence}
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#account_id AccessPolicy#account_id}
        :param approval_group: approval_group block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#approval_group AccessPolicy#approval_group}
        :param approval_required: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#approval_required AccessPolicy#approval_required}.
        :param exclude: exclude block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#exclude AccessPolicy#exclude}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#id AccessPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param purpose_justification_prompt: The prompt to display to the user for a justification for accessing the resource. Required when using ``purpose_justification_required``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#purpose_justification_prompt AccessPolicy#purpose_justification_prompt}
        :param purpose_justification_required: Whether to prompt the user for a justification for accessing the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#purpose_justification_required AccessPolicy#purpose_justification_required}
        :param require: require block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#require AccessPolicy#require}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#zone_id AccessPolicy#zone_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84803941c8b0f08e7908009abe099ae89c5da91512a76b9aabbb809ef3f0da7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessPolicyConfig(
            application_id=application_id,
            decision=decision,
            include=include,
            name=name,
            precedence=precedence,
            account_id=account_id,
            approval_group=approval_group,
            approval_required=approval_required,
            exclude=exclude,
            id=id,
            purpose_justification_prompt=purpose_justification_prompt,
            purpose_justification_required=purpose_justification_required,
            require=require,
            zone_id=zone_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putApprovalGroup")
    def put_approval_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyApprovalGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa8972525155999d841f3a4393f69b729b21a9736e053534d44d89f0f8bafcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApprovalGroup", [value]))

    @jsii.member(jsii_name="putExclude")
    def put_exclude(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyExclude", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32c29944eed015f4a1350b0ab83170336fb8f8318952fd64dabe02832182b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclude", [value]))

    @jsii.member(jsii_name="putInclude")
    def put_include(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyInclude", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385e62f86ec3e627635539700ed65f7fd1f20dccfd4cada85915c4fdfa90b420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInclude", [value]))

    @jsii.member(jsii_name="putRequire")
    def put_require(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyRequire", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83433aad0de83bfa32006de2a7834ab5ec99bef96aeea7be43087442df6e08c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequire", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetApprovalGroup")
    def reset_approval_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalGroup", []))

    @jsii.member(jsii_name="resetApprovalRequired")
    def reset_approval_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalRequired", []))

    @jsii.member(jsii_name="resetExclude")
    def reset_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclude", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPurposeJustificationPrompt")
    def reset_purpose_justification_prompt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPurposeJustificationPrompt", []))

    @jsii.member(jsii_name="resetPurposeJustificationRequired")
    def reset_purpose_justification_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPurposeJustificationRequired", []))

    @jsii.member(jsii_name="resetRequire")
    def reset_require(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequire", []))

    @jsii.member(jsii_name="resetZoneId")
    def reset_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="approvalGroup")
    def approval_group(self) -> "AccessPolicyApprovalGroupList":
        return typing.cast("AccessPolicyApprovalGroupList", jsii.get(self, "approvalGroup"))

    @builtins.property
    @jsii.member(jsii_name="exclude")
    def exclude(self) -> "AccessPolicyExcludeList":
        return typing.cast("AccessPolicyExcludeList", jsii.get(self, "exclude"))

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> "AccessPolicyIncludeList":
        return typing.cast("AccessPolicyIncludeList", jsii.get(self, "include"))

    @builtins.property
    @jsii.member(jsii_name="require")
    def require(self) -> "AccessPolicyRequireList":
        return typing.cast("AccessPolicyRequireList", jsii.get(self, "require"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationIdInput")
    def application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalGroupInput")
    def approval_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyApprovalGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyApprovalGroup"]]], jsii.get(self, "approvalGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalRequiredInput")
    def approval_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "approvalRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="decisionInput")
    def decision_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "decisionInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeInput")
    def exclude_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExclude"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExclude"]]], jsii.get(self, "excludeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInput")
    def include_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyInclude"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyInclude"]]], jsii.get(self, "includeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="precedenceInput")
    def precedence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "precedenceInput"))

    @builtins.property
    @jsii.member(jsii_name="purposeJustificationPromptInput")
    def purpose_justification_prompt_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "purposeJustificationPromptInput"))

    @builtins.property
    @jsii.member(jsii_name="purposeJustificationRequiredInput")
    def purpose_justification_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "purposeJustificationRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="requireInput")
    def require_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequire"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequire"]]], jsii.get(self, "requireInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812687f01185441ed0ca5edcf80b05d1152b9618a859e6939dc7432a1186380b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a78f82e7f0edde76df3916aa2de853ec94f806616d1d7825fcddc45300b8c4f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="approvalRequired")
    def approval_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "approvalRequired"))

    @approval_required.setter
    def approval_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__104e5c974bf6f1947b572ba76e322e0a986e67826a65aa9ff3cd48883250b4ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalRequired", value)

    @builtins.property
    @jsii.member(jsii_name="decision")
    def decision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "decision"))

    @decision.setter
    def decision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c042c21bc7ef2104917e21f2ca589e4f13a2c76206c2aa1a1b4b31fef79645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "decision", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee695d28b4960c15bd09dacb7c51c6684693333fe8a0e488d8ac139cb163dcf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ed9def2ee82e4e3267f7724b1f9c27228b54b1d8dd0bf4f0894d750f5152be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="precedence")
    def precedence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precedence"))

    @precedence.setter
    def precedence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b2355c681f01799e64e4a16b1e80139548a57f3e078fe1bc14c9708f1850134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "precedence", value)

    @builtins.property
    @jsii.member(jsii_name="purposeJustificationPrompt")
    def purpose_justification_prompt(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "purposeJustificationPrompt"))

    @purpose_justification_prompt.setter
    def purpose_justification_prompt(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe7592280906da81037c8fec461aade9ce1d663f25601e4a0c7b33c649796f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "purposeJustificationPrompt", value)

    @builtins.property
    @jsii.member(jsii_name="purposeJustificationRequired")
    def purpose_justification_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "purposeJustificationRequired"))

    @purpose_justification_required.setter
    def purpose_justification_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b29d7a75d2b5be985401eec8131df6118b20b26a9ecb839a8c0745c1f12f8ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "purposeJustificationRequired", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a87d6fc4f2e1f19fface8408b9ae70b3b76ba1d966d011be8f31666c34c3ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyApprovalGroup",
    jsii_struct_bases=[],
    name_mapping={
        "approvals_needed": "approvalsNeeded",
        "email_addresses": "emailAddresses",
        "email_list_uuid": "emailListUuid",
    },
)
class AccessPolicyApprovalGroup:
    def __init__(
        self,
        *,
        approvals_needed: jsii.Number,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_list_uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param approvals_needed: Number of approvals needed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#approvals_needed AccessPolicy#approvals_needed}
        :param email_addresses: List of emails to request approval from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email_addresses AccessPolicy#email_addresses}
        :param email_list_uuid: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email_list_uuid AccessPolicy#email_list_uuid}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af12df2711fe494f597739c90c8210d6e4dec8b622742112ea742514b2cc3061)
            check_type(argname="argument approvals_needed", value=approvals_needed, expected_type=type_hints["approvals_needed"])
            check_type(argname="argument email_addresses", value=email_addresses, expected_type=type_hints["email_addresses"])
            check_type(argname="argument email_list_uuid", value=email_list_uuid, expected_type=type_hints["email_list_uuid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "approvals_needed": approvals_needed,
        }
        if email_addresses is not None:
            self._values["email_addresses"] = email_addresses
        if email_list_uuid is not None:
            self._values["email_list_uuid"] = email_list_uuid

    @builtins.property
    def approvals_needed(self) -> jsii.Number:
        '''Number of approvals needed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#approvals_needed AccessPolicy#approvals_needed}
        '''
        result = self._values.get("approvals_needed")
        assert result is not None, "Required property 'approvals_needed' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of emails to request approval from.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email_addresses AccessPolicy#email_addresses}
        '''
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_list_uuid(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email_list_uuid AccessPolicy#email_list_uuid}.'''
        result = self._values.get("email_list_uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyApprovalGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyApprovalGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyApprovalGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c01b59337d1d67a5c4a0ec0b823ebf43728835a045cecffa54b0df2227897cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyApprovalGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069af8b87306c643e9d2060d82cd973a1e0c79817f5758eb21a35c84f755c6b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyApprovalGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63635911ce44154eb320d00db2dc89fe65da7218ebd34bed65cd0f492791f8a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b003bd16123ef53c5173f00fd59090913eed2e7cccc5433543f47121f0a7999e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b41e8096a0dacd1c279a02a96c4051086ffdad22820d2696339fa6865983d894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyApprovalGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyApprovalGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyApprovalGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c237e9adc126d2764ae36ced209698f9327c4d0bf5f656ed71f27e4cb8255493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyApprovalGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyApprovalGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__401e950804cfb771af36b22864a3767285d7ccb8b9606e8a8bab7f49e7ae6abb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEmailAddresses")
    def reset_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddresses", []))

    @jsii.member(jsii_name="resetEmailListUuid")
    def reset_email_list_uuid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailListUuid", []))

    @builtins.property
    @jsii.member(jsii_name="approvalsNeededInput")
    def approvals_needed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "approvalsNeededInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddressesInput")
    def email_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="emailListUuidInput")
    def email_list_uuid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailListUuidInput"))

    @builtins.property
    @jsii.member(jsii_name="approvalsNeeded")
    def approvals_needed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "approvalsNeeded"))

    @approvals_needed.setter
    def approvals_needed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bfacab364a27b2d00942472d7e93325501e64e2802137bfd7f7cf2272f6f5fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approvalsNeeded", value)

    @builtins.property
    @jsii.member(jsii_name="emailAddresses")
    def email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddresses"))

    @email_addresses.setter
    def email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e86e938b41518c8666139198bf55e97925d68c1135fb1d0791fd8fefe9eda72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="emailListUuid")
    def email_list_uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailListUuid"))

    @email_list_uuid.setter
    def email_list_uuid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddbc533fca520b702969ac17abc93af0e00b43fb56bc9559483ed65854409d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailListUuid", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyApprovalGroup, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyApprovalGroup, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyApprovalGroup, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3051d8f46c0d8abe5093c13e1326c65e7673cda733bce29414e4807c51cfb8a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "application_id": "applicationId",
        "decision": "decision",
        "include": "include",
        "name": "name",
        "precedence": "precedence",
        "account_id": "accountId",
        "approval_group": "approvalGroup",
        "approval_required": "approvalRequired",
        "exclude": "exclude",
        "id": "id",
        "purpose_justification_prompt": "purposeJustificationPrompt",
        "purpose_justification_required": "purposeJustificationRequired",
        "require": "require",
        "zone_id": "zoneId",
    },
)
class AccessPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        application_id: builtins.str,
        decision: builtins.str,
        include: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyInclude", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        precedence: jsii.Number,
        account_id: typing.Optional[builtins.str] = None,
        approval_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyApprovalGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
        approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyExclude", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        purpose_justification_prompt: typing.Optional[builtins.str] = None,
        purpose_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyRequire", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param application_id: The ID of the application the policy is associated with. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#application_id AccessPolicy#application_id}
        :param decision: Defines the action Access will take if the policy matches the user. Available values: ``allow``, ``deny``, ``non_identity``, ``bypass``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#decision AccessPolicy#decision}
        :param include: include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#include AccessPolicy#include}
        :param name: Friendly name of the Access Policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}
        :param precedence: The unique precedence for policies on a single application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#precedence AccessPolicy#precedence}
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#account_id AccessPolicy#account_id}
        :param approval_group: approval_group block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#approval_group AccessPolicy#approval_group}
        :param approval_required: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#approval_required AccessPolicy#approval_required}.
        :param exclude: exclude block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#exclude AccessPolicy#exclude}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#id AccessPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param purpose_justification_prompt: The prompt to display to the user for a justification for accessing the resource. Required when using ``purpose_justification_required``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#purpose_justification_prompt AccessPolicy#purpose_justification_prompt}
        :param purpose_justification_required: Whether to prompt the user for a justification for accessing the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#purpose_justification_required AccessPolicy#purpose_justification_required}
        :param require: require block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#require AccessPolicy#require}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#zone_id AccessPolicy#zone_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9c6708ac3ae02816b0ebbf61a38ba2e8505af5488f2844de55cafbc4d3fc3c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument decision", value=decision, expected_type=type_hints["decision"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument precedence", value=precedence, expected_type=type_hints["precedence"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument approval_group", value=approval_group, expected_type=type_hints["approval_group"])
            check_type(argname="argument approval_required", value=approval_required, expected_type=type_hints["approval_required"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument purpose_justification_prompt", value=purpose_justification_prompt, expected_type=type_hints["purpose_justification_prompt"])
            check_type(argname="argument purpose_justification_required", value=purpose_justification_required, expected_type=type_hints["purpose_justification_required"])
            check_type(argname="argument require", value=require, expected_type=type_hints["require"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "decision": decision,
            "include": include,
            "name": name,
            "precedence": precedence,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if approval_group is not None:
            self._values["approval_group"] = approval_group
        if approval_required is not None:
            self._values["approval_required"] = approval_required
        if exclude is not None:
            self._values["exclude"] = exclude
        if id is not None:
            self._values["id"] = id
        if purpose_justification_prompt is not None:
            self._values["purpose_justification_prompt"] = purpose_justification_prompt
        if purpose_justification_required is not None:
            self._values["purpose_justification_required"] = purpose_justification_required
        if require is not None:
            self._values["require"] = require
        if zone_id is not None:
            self._values["zone_id"] = zone_id

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
    def application_id(self) -> builtins.str:
        '''The ID of the application the policy is associated with.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#application_id AccessPolicy#application_id}
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def decision(self) -> builtins.str:
        '''Defines the action Access will take if the policy matches the user. Available values: ``allow``, ``deny``, ``non_identity``, ``bypass``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#decision AccessPolicy#decision}
        '''
        result = self._values.get("decision")
        assert result is not None, "Required property 'decision' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyInclude"]]:
        '''include block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#include AccessPolicy#include}
        '''
        result = self._values.get("include")
        assert result is not None, "Required property 'include' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyInclude"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Friendly name of the Access Policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def precedence(self) -> jsii.Number:
        '''The unique precedence for policies on a single application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#precedence AccessPolicy#precedence}
        '''
        result = self._values.get("precedence")
        assert result is not None, "Required property 'precedence' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource. Conflicts with ``zone_id``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#account_id AccessPolicy#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def approval_group(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyApprovalGroup]]]:
        '''approval_group block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#approval_group AccessPolicy#approval_group}
        '''
        result = self._values.get("approval_group")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyApprovalGroup]]], result)

    @builtins.property
    def approval_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#approval_required AccessPolicy#approval_required}.'''
        result = self._values.get("approval_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclude(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExclude"]]]:
        '''exclude block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#exclude AccessPolicy#exclude}
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExclude"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#id AccessPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def purpose_justification_prompt(self) -> typing.Optional[builtins.str]:
        '''The prompt to display to the user for a justification for accessing the resource. Required when using ``purpose_justification_required``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#purpose_justification_prompt AccessPolicy#purpose_justification_prompt}
        '''
        result = self._values.get("purpose_justification_prompt")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def purpose_justification_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to prompt the user for a justification for accessing the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#purpose_justification_required AccessPolicy#purpose_justification_required}
        '''
        result = self._values.get("purpose_justification_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequire"]]]:
        '''require block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#require AccessPolicy#require}
        '''
        result = self._values.get("require")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequire"]]], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''The zone identifier to target for the resource. Conflicts with ``account_id``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#zone_id AccessPolicy#zone_id}
        '''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExclude",
    jsii_struct_bases=[],
    name_mapping={
        "any_valid_service_token": "anyValidServiceToken",
        "auth_method": "authMethod",
        "azure": "azure",
        "certificate": "certificate",
        "common_name": "commonName",
        "device_posture": "devicePosture",
        "email": "email",
        "email_domain": "emailDomain",
        "everyone": "everyone",
        "external_evaluation": "externalEvaluation",
        "geo": "geo",
        "github": "github",
        "group": "group",
        "gsuite": "gsuite",
        "ip": "ip",
        "login_method": "loginMethod",
        "okta": "okta",
        "saml": "saml",
        "service_token": "serviceToken",
    },
)
class AccessPolicyExclude:
    def __init__(
        self,
        *,
        any_valid_service_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auth_method: typing.Optional[builtins.str] = None,
        azure: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyExcludeAzure", typing.Dict[builtins.str, typing.Any]]]]] = None,
        certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        common_name: typing.Optional[builtins.str] = None,
        device_posture: typing.Optional[typing.Sequence[builtins.str]] = None,
        email: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_domain: typing.Optional[typing.Sequence[builtins.str]] = None,
        everyone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_evaluation: typing.Optional[typing.Union["AccessPolicyExcludeExternalEvaluation", typing.Dict[builtins.str, typing.Any]]] = None,
        geo: typing.Optional[typing.Sequence[builtins.str]] = None,
        github: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyExcludeGithub", typing.Dict[builtins.str, typing.Any]]]]] = None,
        group: typing.Optional[typing.Sequence[builtins.str]] = None,
        gsuite: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyExcludeGsuite", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_method: typing.Optional[typing.Sequence[builtins.str]] = None,
        okta: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyExcludeOkta", typing.Dict[builtins.str, typing.Any]]]]] = None,
        saml: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyExcludeSaml", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_token: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param any_valid_service_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#any_valid_service_token AccessPolicy#any_valid_service_token}.
        :param auth_method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#auth_method AccessPolicy#auth_method}.
        :param azure: azure block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#azure AccessPolicy#azure}
        :param certificate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#certificate AccessPolicy#certificate}.
        :param common_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#common_name AccessPolicy#common_name}.
        :param device_posture: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#device_posture AccessPolicy#device_posture}.
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.
        :param email_domain: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email_domain AccessPolicy#email_domain}.
        :param everyone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#everyone AccessPolicy#everyone}.
        :param external_evaluation: external_evaluation block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#external_evaluation AccessPolicy#external_evaluation}
        :param geo: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#geo AccessPolicy#geo}.
        :param github: github block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#github AccessPolicy#github}
        :param group: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#group AccessPolicy#group}.
        :param gsuite: gsuite block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#gsuite AccessPolicy#gsuite}
        :param ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#ip AccessPolicy#ip}.
        :param login_method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#login_method AccessPolicy#login_method}.
        :param okta: okta block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#okta AccessPolicy#okta}
        :param saml: saml block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#saml AccessPolicy#saml}
        :param service_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#service_token AccessPolicy#service_token}.
        '''
        if isinstance(external_evaluation, dict):
            external_evaluation = AccessPolicyExcludeExternalEvaluation(**external_evaluation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7bd596c6f1f8c1e33c17f2a3fad0d68580170184200c2f6a94fd70f7be40cb6)
            check_type(argname="argument any_valid_service_token", value=any_valid_service_token, expected_type=type_hints["any_valid_service_token"])
            check_type(argname="argument auth_method", value=auth_method, expected_type=type_hints["auth_method"])
            check_type(argname="argument azure", value=azure, expected_type=type_hints["azure"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
            check_type(argname="argument device_posture", value=device_posture, expected_type=type_hints["device_posture"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument email_domain", value=email_domain, expected_type=type_hints["email_domain"])
            check_type(argname="argument everyone", value=everyone, expected_type=type_hints["everyone"])
            check_type(argname="argument external_evaluation", value=external_evaluation, expected_type=type_hints["external_evaluation"])
            check_type(argname="argument geo", value=geo, expected_type=type_hints["geo"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument gsuite", value=gsuite, expected_type=type_hints["gsuite"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument login_method", value=login_method, expected_type=type_hints["login_method"])
            check_type(argname="argument okta", value=okta, expected_type=type_hints["okta"])
            check_type(argname="argument saml", value=saml, expected_type=type_hints["saml"])
            check_type(argname="argument service_token", value=service_token, expected_type=type_hints["service_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if any_valid_service_token is not None:
            self._values["any_valid_service_token"] = any_valid_service_token
        if auth_method is not None:
            self._values["auth_method"] = auth_method
        if azure is not None:
            self._values["azure"] = azure
        if certificate is not None:
            self._values["certificate"] = certificate
        if common_name is not None:
            self._values["common_name"] = common_name
        if device_posture is not None:
            self._values["device_posture"] = device_posture
        if email is not None:
            self._values["email"] = email
        if email_domain is not None:
            self._values["email_domain"] = email_domain
        if everyone is not None:
            self._values["everyone"] = everyone
        if external_evaluation is not None:
            self._values["external_evaluation"] = external_evaluation
        if geo is not None:
            self._values["geo"] = geo
        if github is not None:
            self._values["github"] = github
        if group is not None:
            self._values["group"] = group
        if gsuite is not None:
            self._values["gsuite"] = gsuite
        if ip is not None:
            self._values["ip"] = ip
        if login_method is not None:
            self._values["login_method"] = login_method
        if okta is not None:
            self._values["okta"] = okta
        if saml is not None:
            self._values["saml"] = saml
        if service_token is not None:
            self._values["service_token"] = service_token

    @builtins.property
    def any_valid_service_token(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#any_valid_service_token AccessPolicy#any_valid_service_token}.'''
        result = self._values.get("any_valid_service_token")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auth_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#auth_method AccessPolicy#auth_method}.'''
        result = self._values.get("auth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeAzure"]]]:
        '''azure block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#azure AccessPolicy#azure}
        '''
        result = self._values.get("azure")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeAzure"]]], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#certificate AccessPolicy#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def common_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#common_name AccessPolicy#common_name}.'''
        result = self._values.get("common_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_posture(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#device_posture AccessPolicy#device_posture}.'''
        result = self._values.get("device_posture")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_domain(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email_domain AccessPolicy#email_domain}.'''
        result = self._values.get("email_domain")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def everyone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#everyone AccessPolicy#everyone}.'''
        result = self._values.get("everyone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_evaluation(
        self,
    ) -> typing.Optional["AccessPolicyExcludeExternalEvaluation"]:
        '''external_evaluation block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#external_evaluation AccessPolicy#external_evaluation}
        '''
        result = self._values.get("external_evaluation")
        return typing.cast(typing.Optional["AccessPolicyExcludeExternalEvaluation"], result)

    @builtins.property
    def geo(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#geo AccessPolicy#geo}.'''
        result = self._values.get("geo")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def github(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeGithub"]]]:
        '''github block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#github AccessPolicy#github}
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeGithub"]]], result)

    @builtins.property
    def group(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#group AccessPolicy#group}.'''
        result = self._values.get("group")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def gsuite(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeGsuite"]]]:
        '''gsuite block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#gsuite AccessPolicy#gsuite}
        '''
        result = self._values.get("gsuite")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeGsuite"]]], result)

    @builtins.property
    def ip(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#ip AccessPolicy#ip}.'''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_method(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#login_method AccessPolicy#login_method}.'''
        result = self._values.get("login_method")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def okta(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeOkta"]]]:
        '''okta block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#okta AccessPolicy#okta}
        '''
        result = self._values.get("okta")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeOkta"]]], result)

    @builtins.property
    def saml(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeSaml"]]]:
        '''saml block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#saml AccessPolicy#saml}
        '''
        result = self._values.get("saml")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeSaml"]]], result)

    @builtins.property
    def service_token(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#service_token AccessPolicy#service_token}.'''
        result = self._values.get("service_token")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyExclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeAzure",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "identity_provider_id": "identityProviderId"},
)
class AccessPolicyExcludeAzure:
    def __init__(
        self,
        *,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_provider_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#id AccessPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe2352dbb106bb5d71983034609a84d021e9ebdff469dc72e5159cc2a5ec813)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id

    @builtins.property
    def id(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#id AccessPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyExcludeAzure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyExcludeAzureList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeAzureList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c74583d6d8a2269a30f1851f87c4f626b088d42352e11895c4a5e72b2ca987d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyExcludeAzureOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22db79ab2f4ffb7503ce804377491a53c4826ec887b9dae4d09eb11c0bdd3962)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyExcludeAzureOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db2a76703ee69726cbc543f5a6a65f1752f34d913b6623986f0a12c250eac876)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19528b4dc4464229dac5b73e50f3e1f4f63b75188e1e2b64682fe3f076a1aa6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1a832d84de740e1367116ae2c7dbbde3bf9885a35336a2cbea51dcdc36830b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeAzure]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeAzure]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeAzure]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec77b51c7e232fb71c13285c500ac8487232bfaf9978e72a51ee2230d0fe698c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyExcludeAzureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeAzureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4020e8b9b779a5ff9ca1f69480c317ea46af25b9e9fac5622aa193978633fd0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "id"))

    @id.setter
    def id(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8bfa76994eb2d52d8f23ca4eeca81164fd517e686aae8cfd7d09c7ca71bfea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699f783480367e127e3ac5eee51579d551082d36f9e376fcae9dabc2472daf99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyExcludeAzure, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyExcludeAzure, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyExcludeAzure, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c72a0cd934da86e1fc661ba5bb923c231bcf5f149b77ddc20e7b8900cd00555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeExternalEvaluation",
    jsii_struct_bases=[],
    name_mapping={"evaluate_url": "evaluateUrl", "keys_url": "keysUrl"},
)
class AccessPolicyExcludeExternalEvaluation:
    def __init__(
        self,
        *,
        evaluate_url: typing.Optional[builtins.str] = None,
        keys_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluate_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#evaluate_url AccessPolicy#evaluate_url}.
        :param keys_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#keys_url AccessPolicy#keys_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0708eefeb53f667c392a735574394dff4e9004f9d56c042b62018d5cf044c402)
            check_type(argname="argument evaluate_url", value=evaluate_url, expected_type=type_hints["evaluate_url"])
            check_type(argname="argument keys_url", value=keys_url, expected_type=type_hints["keys_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluate_url is not None:
            self._values["evaluate_url"] = evaluate_url
        if keys_url is not None:
            self._values["keys_url"] = keys_url

    @builtins.property
    def evaluate_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#evaluate_url AccessPolicy#evaluate_url}.'''
        result = self._values.get("evaluate_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keys_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#keys_url AccessPolicy#keys_url}.'''
        result = self._values.get("keys_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyExcludeExternalEvaluation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyExcludeExternalEvaluationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeExternalEvaluationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10c0d6ede8491c497eb534b2077288efb9b24fd5bba09234991ee972a77950da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEvaluateUrl")
    def reset_evaluate_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluateUrl", []))

    @jsii.member(jsii_name="resetKeysUrl")
    def reset_keys_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeysUrl", []))

    @builtins.property
    @jsii.member(jsii_name="evaluateUrlInput")
    def evaluate_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluateUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="keysUrlInput")
    def keys_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keysUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluateUrl")
    def evaluate_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluateUrl"))

    @evaluate_url.setter
    def evaluate_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ef8492f45d922d3a71213d7cc6da340889f1c0c6988c3070221a35137ea99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluateUrl", value)

    @builtins.property
    @jsii.member(jsii_name="keysUrl")
    def keys_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keysUrl"))

    @keys_url.setter
    def keys_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf3bee254cc20154fa5b91aef73d85e7ed1c2ca3048879710be3e866db6bb45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keysUrl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccessPolicyExcludeExternalEvaluation]:
        return typing.cast(typing.Optional[AccessPolicyExcludeExternalEvaluation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessPolicyExcludeExternalEvaluation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2dfc626f635ab8054a6d9e7108cbc3c5cbba735dada2c500ad937692632f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeGithub",
    jsii_struct_bases=[],
    name_mapping={
        "identity_provider_id": "identityProviderId",
        "name": "name",
        "teams": "teams",
    },
)
class AccessPolicyExcludeGithub:
    def __init__(
        self,
        *,
        identity_provider_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.
        :param teams: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#teams AccessPolicy#teams}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221e51c17a43211154739e44b1c48b957ad7bca748c5fc33fb2962d98c424b21)
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id
        if name is not None:
            self._values["name"] = name
        if teams is not None:
            self._values["teams"] = teams

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def teams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#teams AccessPolicy#teams}.'''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyExcludeGithub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyExcludeGithubList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeGithubList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcb42dda753b790ff7603efbe2e9d39c6801142f4514a11298ae343ef66a29e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyExcludeGithubOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab796aad987396af3d2143d29f27a9d4bff1d79f86a4d6dde1d62a7a5c87f936)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyExcludeGithubOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e466cb2b55215455d5135ed24120d48de380eacf8bdf2c3f4cf7c6b9e2e84a49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf58e8126566f565230c7a554ebeb1d070db85947f094701c224babbe3afc8d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ec8dc46ce8a58ccc77079958af9603f548bff7b035180f7c1bea2513acf3b28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGithub]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGithub]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGithub]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33975837ebc1fc161780295e4031cc0745d6ca08ef890bbb0ef70d6061646cbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyExcludeGithubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeGithubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6448e05ff747b9cefbf154906574068ff220d194c4f8195e81caf8df8e835a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetTeams")
    def reset_teams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeams", []))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa04e3d10dae4da417b756f95b17a89c173d6107778a48d88964d09340c8b13f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4b74efaba86c82260fec61cf62d8e5dd71bee16c7c80564ad336f99ca940f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "teams"))

    @teams.setter
    def teams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc4de1806c633c63db308c20b8f55371b1a77b12548394633e880c8a06da664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teams", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyExcludeGithub, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyExcludeGithub, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyExcludeGithub, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53efc3cc4cbcbbf78652a6975bea620e02d5487f3de1dc9aecf4d73ef7d30122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeGsuite",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "identity_provider_id": "identityProviderId"},
)
class AccessPolicyExcludeGsuite:
    def __init__(
        self,
        *,
        email: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_provider_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff3a53499e1a71c3d5b4f8433665416c1deee47649e4c1e12cf924a083b4acf)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id

    @builtins.property
    def email(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyExcludeGsuite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyExcludeGsuiteList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeGsuiteList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cd629be31bbf1b7278065c67da9d6657abe6ecee322a41fc1aa269e8e3ad0ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyExcludeGsuiteOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ab9db55dfe2940159c7574801ef6f77092974f766c6d6e6cd122561434ae2e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyExcludeGsuiteOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ce475968d262f67a7b280a6e3b259b80808313671fa68fd23f7beee9d0d2d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb308e73c3e8e5ce5aacbfe07ff04648b68ef77009de1ab3c88b47dd6933e159)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93b9f4a32730f819631265abd83fe9755e03bb2e751b8fe0cd99438d9f229931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGsuite]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGsuite]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGsuite]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e39ceec195e67fc419a2c947d15dcc8047628b3b32875e194cf122bb505290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyExcludeGsuiteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeGsuiteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc9697f0e25a18562bad456ea542529ddd5e9466f19f4b2da9ce8c5d6ba7b6de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "email"))

    @email.setter
    def email(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c3fd03671e0fd947b6b50383e8a03a07820d4e056c026f667d8c8bf6610e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef9eb674412811e1a079e1e7b7e73d42fc405697185c30a4dee755c92b731ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyExcludeGsuite, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyExcludeGsuite, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyExcludeGsuite, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26568adaf0fa9a476bdb968a19e0bce34644db9ac5f594f5b11185e01f2e3501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyExcludeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9de05addc01948152a823f84f62efcb43f70e62117731e3a9c9eba6afa74ca25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyExcludeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8315c74e6eefea1427621fec8ab2bbbcc3639274ecc6f345ebedcfe553c642cb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyExcludeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ae839d5ceabfc049172f2e9e47e8d644405ec9c03a9cc6566d7b3f4b741590)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0be32042fa401ccbc3fd5033e57f1c6d8d4b614a237afcb062c6b50ba0a0f2d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70adb846604236b553ed608dc405462d6fd0acbbff310263de333618cc9e6662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExclude]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExclude]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExclude]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df467676956e07b69bafdd83a9e14ddd0d3abcd4d2830901769a49f82a94887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeOkta",
    jsii_struct_bases=[],
    name_mapping={"identity_provider_id": "identityProviderId", "name": "name"},
)
class AccessPolicyExcludeOkta:
    def __init__(
        self,
        *,
        identity_provider_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c54082121ca2289d82f2d843b24a05c387479b39e1cddd0e679af0e79eb801)
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyExcludeOkta(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyExcludeOktaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeOktaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf3e2bbee26487babf21c6c2491410967f3962bac7a0a9dd9e022c3e6cff4e30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyExcludeOktaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2977bd3fd722d34bf685a9463783b0200fa04372e923e05c80a66ac35f23701d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyExcludeOktaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddcd9bf6decf0f6263aa6baad3082f18613b4c8b47ccf2f250b487241a22fd18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__938752f671052e30cac449f7e2ad1ed0970b57c637e2f12a10e1e7b32bcdbede)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d584ea8ef9adc35162cecc7a8cd09b96ef63f491023a16f1117e8460b69645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeOkta]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeOkta]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeOkta]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7646179bd32b841af52f1eada0beb9921243e74170a490173ab797a9327958cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyExcludeOktaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeOktaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__812371f9629a8c5a28ad7d84a3ca29c9b596c58dcaa090f23c38777e07c5bf0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c704ea5a346c04e3065ed5f58da67a1b3a6693a19cc4302b2e591446d8c704b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce8b757a4b2b8f5f716bff169c2dc382210bb51a2cb5cf637a8fb28ca7d1ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyExcludeOkta, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyExcludeOkta, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyExcludeOkta, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54479f44d2c8a4c4d57775224dcb2214470465cf8dd7187bf3fb5cff6750c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyExcludeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adf0e416bfe12d94850ab7b0c91a0c58c3b3289de81d11853bdb1509b4a2bd39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAzure")
    def put_azure(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeAzure, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b53dccb4f2837eecad7514db087ff0cb88d3c4dcd749eaf2c73a1dca8d71f64d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAzure", [value]))

    @jsii.member(jsii_name="putExternalEvaluation")
    def put_external_evaluation(
        self,
        *,
        evaluate_url: typing.Optional[builtins.str] = None,
        keys_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluate_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#evaluate_url AccessPolicy#evaluate_url}.
        :param keys_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#keys_url AccessPolicy#keys_url}.
        '''
        value = AccessPolicyExcludeExternalEvaluation(
            evaluate_url=evaluate_url, keys_url=keys_url
        )

        return typing.cast(None, jsii.invoke(self, "putExternalEvaluation", [value]))

    @jsii.member(jsii_name="putGithub")
    def put_github(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeGithub, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f007ad21c7899ad6ae212deaa65bce0a1b97557b5c1a92623c3e92dc002068d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGithub", [value]))

    @jsii.member(jsii_name="putGsuite")
    def put_gsuite(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeGsuite, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83fda570c2acc71a553400e50a55cbc9b151f33df8c7b16957fc58f905b7b7cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGsuite", [value]))

    @jsii.member(jsii_name="putOkta")
    def put_okta(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeOkta, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af23a5888b64021868de935ad71d6555819b305648efae52323ab422dea8fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOkta", [value]))

    @jsii.member(jsii_name="putSaml")
    def put_saml(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyExcludeSaml", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ee94a3cc9a781dfca740fcd489aa62c68cd546dafce25bcb36c397ae99d594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSaml", [value]))

    @jsii.member(jsii_name="resetAnyValidServiceToken")
    def reset_any_valid_service_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnyValidServiceToken", []))

    @jsii.member(jsii_name="resetAuthMethod")
    def reset_auth_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthMethod", []))

    @jsii.member(jsii_name="resetAzure")
    def reset_azure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzure", []))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCommonName")
    def reset_common_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonName", []))

    @jsii.member(jsii_name="resetDevicePosture")
    def reset_device_posture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevicePosture", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetEmailDomain")
    def reset_email_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailDomain", []))

    @jsii.member(jsii_name="resetEveryone")
    def reset_everyone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEveryone", []))

    @jsii.member(jsii_name="resetExternalEvaluation")
    def reset_external_evaluation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalEvaluation", []))

    @jsii.member(jsii_name="resetGeo")
    def reset_geo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeo", []))

    @jsii.member(jsii_name="resetGithub")
    def reset_github(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithub", []))

    @jsii.member(jsii_name="resetGroup")
    def reset_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroup", []))

    @jsii.member(jsii_name="resetGsuite")
    def reset_gsuite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGsuite", []))

    @jsii.member(jsii_name="resetIp")
    def reset_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIp", []))

    @jsii.member(jsii_name="resetLoginMethod")
    def reset_login_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginMethod", []))

    @jsii.member(jsii_name="resetOkta")
    def reset_okta(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOkta", []))

    @jsii.member(jsii_name="resetSaml")
    def reset_saml(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml", []))

    @jsii.member(jsii_name="resetServiceToken")
    def reset_service_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceToken", []))

    @builtins.property
    @jsii.member(jsii_name="azure")
    def azure(self) -> AccessPolicyExcludeAzureList:
        return typing.cast(AccessPolicyExcludeAzureList, jsii.get(self, "azure"))

    @builtins.property
    @jsii.member(jsii_name="externalEvaluation")
    def external_evaluation(
        self,
    ) -> AccessPolicyExcludeExternalEvaluationOutputReference:
        return typing.cast(AccessPolicyExcludeExternalEvaluationOutputReference, jsii.get(self, "externalEvaluation"))

    @builtins.property
    @jsii.member(jsii_name="github")
    def github(self) -> AccessPolicyExcludeGithubList:
        return typing.cast(AccessPolicyExcludeGithubList, jsii.get(self, "github"))

    @builtins.property
    @jsii.member(jsii_name="gsuite")
    def gsuite(self) -> AccessPolicyExcludeGsuiteList:
        return typing.cast(AccessPolicyExcludeGsuiteList, jsii.get(self, "gsuite"))

    @builtins.property
    @jsii.member(jsii_name="okta")
    def okta(self) -> AccessPolicyExcludeOktaList:
        return typing.cast(AccessPolicyExcludeOktaList, jsii.get(self, "okta"))

    @builtins.property
    @jsii.member(jsii_name="saml")
    def saml(self) -> "AccessPolicyExcludeSamlList":
        return typing.cast("AccessPolicyExcludeSamlList", jsii.get(self, "saml"))

    @builtins.property
    @jsii.member(jsii_name="anyValidServiceTokenInput")
    def any_valid_service_token_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "anyValidServiceTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="authMethodInput")
    def auth_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="azureInput")
    def azure_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeAzure]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeAzure]]], jsii.get(self, "azureInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="commonNameInput")
    def common_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="devicePostureInput")
    def device_posture_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "devicePostureInput"))

    @builtins.property
    @jsii.member(jsii_name="emailDomainInput")
    def email_domain_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="everyoneInput")
    def everyone_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "everyoneInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEvaluationInput")
    def external_evaluation_input(
        self,
    ) -> typing.Optional[AccessPolicyExcludeExternalEvaluation]:
        return typing.cast(typing.Optional[AccessPolicyExcludeExternalEvaluation], jsii.get(self, "externalEvaluationInput"))

    @builtins.property
    @jsii.member(jsii_name="geoInput")
    def geo_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "geoInput"))

    @builtins.property
    @jsii.member(jsii_name="githubInput")
    def github_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGithub]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGithub]]], jsii.get(self, "githubInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="gsuiteInput")
    def gsuite_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGsuite]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGsuite]]], jsii.get(self, "gsuiteInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="loginMethodInput")
    def login_method_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loginMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaInput")
    def okta_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeOkta]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeOkta]]], jsii.get(self, "oktaInput"))

    @builtins.property
    @jsii.member(jsii_name="samlInput")
    def saml_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeSaml"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyExcludeSaml"]]], jsii.get(self, "samlInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTokenInput")
    def service_token_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="anyValidServiceToken")
    def any_valid_service_token(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "anyValidServiceToken"))

    @any_valid_service_token.setter
    def any_valid_service_token(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0719a1e52e5e17e0882334df3df6e6e99ab05ed0011542c0fe451fb85f94c50b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anyValidServiceToken", value)

    @builtins.property
    @jsii.member(jsii_name="authMethod")
    def auth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authMethod"))

    @auth_method.setter
    def auth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf5aef3a6223af8de535a04fc764423942cfa94bde59ca86c1262577ecd7b173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authMethod", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c72ca973764cd98fbc3b9cce847f2a98f3dde6882cf38b228b47125e243bc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonName"))

    @common_name.setter
    def common_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd6bb4ba387b9ee040536a3c21db56e736d19eb63a7ac8ce874dff3995f1179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonName", value)

    @builtins.property
    @jsii.member(jsii_name="devicePosture")
    def device_posture(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "devicePosture"))

    @device_posture.setter
    def device_posture(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa67e4d5dd288c10bc2a7ef25075e6b3274b193070ac4d2aba4f20c4af695e3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "devicePosture", value)

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "email"))

    @email.setter
    def email(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7279dee33d3c2625868506d07c40ba678c1740d2dfffad9c4e386783f8cc7e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="emailDomain")
    def email_domain(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailDomain"))

    @email_domain.setter
    def email_domain(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7e724fc8eaf74d5dffb258775f0f17d6d9230f0f4bf12e27b4784483d86dbbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailDomain", value)

    @builtins.property
    @jsii.member(jsii_name="everyone")
    def everyone(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "everyone"))

    @everyone.setter
    def everyone(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aac89174bf5083e1c91b2e252fc52e34f50b12c3e27c5936e1aea98aad6fc30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "everyone", value)

    @builtins.property
    @jsii.member(jsii_name="geo")
    def geo(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "geo"))

    @geo.setter
    def geo(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90c69fcd1eab5430435a65174dcbeaecc447eb056b2abb54ce446694691fa8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geo", value)

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "group"))

    @group.setter
    def group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a40a143b2d67e812145475d298b8298c022b1dcb0e59f7df8ed5ec657a2db32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value)

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb58b061d0aa36fb81f376843d93190bfdbec75d0edb0e3e2712c4da8374917f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value)

    @builtins.property
    @jsii.member(jsii_name="loginMethod")
    def login_method(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginMethod"))

    @login_method.setter
    def login_method(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9d7932bb4ebd3c1f8540634c574ec2c47b8fc0a53687dc4f6acc9cf4c09598e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginMethod", value)

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceToken"))

    @service_token.setter
    def service_token(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7631206af465b1df4fa7f5d7e45b22c997a7bf302f5280eda153dc5eaa29fb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceToken", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyExclude, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyExclude, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyExclude, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb60ac58e733ec888306e13f3e9db32928a7ce508629c75f5cf0fb20d8a554d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeSaml",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_name": "attributeName",
        "attribute_value": "attributeValue",
        "identity_provider_id": "identityProviderId",
    },
)
class AccessPolicyExcludeSaml:
    def __init__(
        self,
        *,
        attribute_name: typing.Optional[builtins.str] = None,
        attribute_value: typing.Optional[builtins.str] = None,
        identity_provider_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attribute_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_name AccessPolicy#attribute_name}.
        :param attribute_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_value AccessPolicy#attribute_value}.
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe60fa7c5755419369967cbde726378f27ac4606e64e8493efe8052fe568a35)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
            check_type(argname="argument attribute_value", value=attribute_value, expected_type=type_hints["attribute_value"])
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_name is not None:
            self._values["attribute_name"] = attribute_name
        if attribute_value is not None:
            self._values["attribute_value"] = attribute_value
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id

    @builtins.property
    def attribute_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_name AccessPolicy#attribute_name}.'''
        result = self._values.get("attribute_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attribute_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_value AccessPolicy#attribute_value}.'''
        result = self._values.get("attribute_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyExcludeSaml(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyExcludeSamlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeSamlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c50aec812e07b0256aba0d0a9f8f6453ab807cab01d3fa86bb60d59e8b55dfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyExcludeSamlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e71f6d0afb17a628668472e9203a3d9a06c55c448a6a82b6b6005eee0f53e4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyExcludeSamlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99df21b87ed808bc75a153b7ccb9d3cee8c52c0b41063652f3140c937a838cc7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__814ad343fe49b715bd4bdf5e4c480684fab82f7007f2a18f0f957a679880eb7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2e33b836e456c82d407806573a77d9cf19268ce3525d009590e6dceb54d908c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeSaml]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeSaml]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeSaml]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d965977cc286886a7b7b23ff48dd646db8ef7215b28567f4c3eb5823f9abbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyExcludeSamlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyExcludeSamlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__823630abb8eb63e0dfcd569630fc85016136c2b310a26ccb093e708bd242c46a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAttributeName")
    def reset_attribute_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeName", []))

    @jsii.member(jsii_name="resetAttributeValue")
    def reset_attribute_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeValue", []))

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @builtins.property
    @jsii.member(jsii_name="attributeNameInput")
    def attribute_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeValueInput")
    def attribute_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeValueInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeName")
    def attribute_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeName"))

    @attribute_name.setter
    def attribute_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c44f05219745f4aad45ef6c3b553f8a66480cb69efa1c35f5e7567ec57a048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeName", value)

    @builtins.property
    @jsii.member(jsii_name="attributeValue")
    def attribute_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeValue"))

    @attribute_value.setter
    def attribute_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac057ef69a1b1c50e0a223d2957232e562e14141344090bf038223d85ae2f6c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeValue", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e04055223f996aa08c222e182243f15ab9f3da03447eff98cb0687aceb42283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyExcludeSaml, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyExcludeSaml, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyExcludeSaml, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c07d6ce963759de25a53e70107bfd1d3bca50de4b5b919eb52e4c074ee7226d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyInclude",
    jsii_struct_bases=[],
    name_mapping={
        "any_valid_service_token": "anyValidServiceToken",
        "auth_method": "authMethod",
        "azure": "azure",
        "certificate": "certificate",
        "common_name": "commonName",
        "device_posture": "devicePosture",
        "email": "email",
        "email_domain": "emailDomain",
        "everyone": "everyone",
        "external_evaluation": "externalEvaluation",
        "geo": "geo",
        "github": "github",
        "group": "group",
        "gsuite": "gsuite",
        "ip": "ip",
        "login_method": "loginMethod",
        "okta": "okta",
        "saml": "saml",
        "service_token": "serviceToken",
    },
)
class AccessPolicyInclude:
    def __init__(
        self,
        *,
        any_valid_service_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auth_method: typing.Optional[builtins.str] = None,
        azure: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyIncludeAzure", typing.Dict[builtins.str, typing.Any]]]]] = None,
        certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        common_name: typing.Optional[builtins.str] = None,
        device_posture: typing.Optional[typing.Sequence[builtins.str]] = None,
        email: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_domain: typing.Optional[typing.Sequence[builtins.str]] = None,
        everyone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_evaluation: typing.Optional[typing.Union["AccessPolicyIncludeExternalEvaluation", typing.Dict[builtins.str, typing.Any]]] = None,
        geo: typing.Optional[typing.Sequence[builtins.str]] = None,
        github: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyIncludeGithub", typing.Dict[builtins.str, typing.Any]]]]] = None,
        group: typing.Optional[typing.Sequence[builtins.str]] = None,
        gsuite: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyIncludeGsuite", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_method: typing.Optional[typing.Sequence[builtins.str]] = None,
        okta: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyIncludeOkta", typing.Dict[builtins.str, typing.Any]]]]] = None,
        saml: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyIncludeSaml", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_token: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param any_valid_service_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#any_valid_service_token AccessPolicy#any_valid_service_token}.
        :param auth_method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#auth_method AccessPolicy#auth_method}.
        :param azure: azure block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#azure AccessPolicy#azure}
        :param certificate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#certificate AccessPolicy#certificate}.
        :param common_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#common_name AccessPolicy#common_name}.
        :param device_posture: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#device_posture AccessPolicy#device_posture}.
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.
        :param email_domain: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email_domain AccessPolicy#email_domain}.
        :param everyone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#everyone AccessPolicy#everyone}.
        :param external_evaluation: external_evaluation block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#external_evaluation AccessPolicy#external_evaluation}
        :param geo: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#geo AccessPolicy#geo}.
        :param github: github block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#github AccessPolicy#github}
        :param group: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#group AccessPolicy#group}.
        :param gsuite: gsuite block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#gsuite AccessPolicy#gsuite}
        :param ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#ip AccessPolicy#ip}.
        :param login_method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#login_method AccessPolicy#login_method}.
        :param okta: okta block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#okta AccessPolicy#okta}
        :param saml: saml block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#saml AccessPolicy#saml}
        :param service_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#service_token AccessPolicy#service_token}.
        '''
        if isinstance(external_evaluation, dict):
            external_evaluation = AccessPolicyIncludeExternalEvaluation(**external_evaluation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca231b2d68c6ea34a6ec54ebedb99537b6329ce587ebca40a0163e3afed96d5f)
            check_type(argname="argument any_valid_service_token", value=any_valid_service_token, expected_type=type_hints["any_valid_service_token"])
            check_type(argname="argument auth_method", value=auth_method, expected_type=type_hints["auth_method"])
            check_type(argname="argument azure", value=azure, expected_type=type_hints["azure"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
            check_type(argname="argument device_posture", value=device_posture, expected_type=type_hints["device_posture"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument email_domain", value=email_domain, expected_type=type_hints["email_domain"])
            check_type(argname="argument everyone", value=everyone, expected_type=type_hints["everyone"])
            check_type(argname="argument external_evaluation", value=external_evaluation, expected_type=type_hints["external_evaluation"])
            check_type(argname="argument geo", value=geo, expected_type=type_hints["geo"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument gsuite", value=gsuite, expected_type=type_hints["gsuite"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument login_method", value=login_method, expected_type=type_hints["login_method"])
            check_type(argname="argument okta", value=okta, expected_type=type_hints["okta"])
            check_type(argname="argument saml", value=saml, expected_type=type_hints["saml"])
            check_type(argname="argument service_token", value=service_token, expected_type=type_hints["service_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if any_valid_service_token is not None:
            self._values["any_valid_service_token"] = any_valid_service_token
        if auth_method is not None:
            self._values["auth_method"] = auth_method
        if azure is not None:
            self._values["azure"] = azure
        if certificate is not None:
            self._values["certificate"] = certificate
        if common_name is not None:
            self._values["common_name"] = common_name
        if device_posture is not None:
            self._values["device_posture"] = device_posture
        if email is not None:
            self._values["email"] = email
        if email_domain is not None:
            self._values["email_domain"] = email_domain
        if everyone is not None:
            self._values["everyone"] = everyone
        if external_evaluation is not None:
            self._values["external_evaluation"] = external_evaluation
        if geo is not None:
            self._values["geo"] = geo
        if github is not None:
            self._values["github"] = github
        if group is not None:
            self._values["group"] = group
        if gsuite is not None:
            self._values["gsuite"] = gsuite
        if ip is not None:
            self._values["ip"] = ip
        if login_method is not None:
            self._values["login_method"] = login_method
        if okta is not None:
            self._values["okta"] = okta
        if saml is not None:
            self._values["saml"] = saml
        if service_token is not None:
            self._values["service_token"] = service_token

    @builtins.property
    def any_valid_service_token(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#any_valid_service_token AccessPolicy#any_valid_service_token}.'''
        result = self._values.get("any_valid_service_token")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auth_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#auth_method AccessPolicy#auth_method}.'''
        result = self._values.get("auth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeAzure"]]]:
        '''azure block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#azure AccessPolicy#azure}
        '''
        result = self._values.get("azure")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeAzure"]]], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#certificate AccessPolicy#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def common_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#common_name AccessPolicy#common_name}.'''
        result = self._values.get("common_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_posture(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#device_posture AccessPolicy#device_posture}.'''
        result = self._values.get("device_posture")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_domain(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email_domain AccessPolicy#email_domain}.'''
        result = self._values.get("email_domain")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def everyone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#everyone AccessPolicy#everyone}.'''
        result = self._values.get("everyone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_evaluation(
        self,
    ) -> typing.Optional["AccessPolicyIncludeExternalEvaluation"]:
        '''external_evaluation block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#external_evaluation AccessPolicy#external_evaluation}
        '''
        result = self._values.get("external_evaluation")
        return typing.cast(typing.Optional["AccessPolicyIncludeExternalEvaluation"], result)

    @builtins.property
    def geo(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#geo AccessPolicy#geo}.'''
        result = self._values.get("geo")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def github(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeGithub"]]]:
        '''github block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#github AccessPolicy#github}
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeGithub"]]], result)

    @builtins.property
    def group(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#group AccessPolicy#group}.'''
        result = self._values.get("group")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def gsuite(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeGsuite"]]]:
        '''gsuite block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#gsuite AccessPolicy#gsuite}
        '''
        result = self._values.get("gsuite")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeGsuite"]]], result)

    @builtins.property
    def ip(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#ip AccessPolicy#ip}.'''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_method(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#login_method AccessPolicy#login_method}.'''
        result = self._values.get("login_method")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def okta(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeOkta"]]]:
        '''okta block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#okta AccessPolicy#okta}
        '''
        result = self._values.get("okta")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeOkta"]]], result)

    @builtins.property
    def saml(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeSaml"]]]:
        '''saml block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#saml AccessPolicy#saml}
        '''
        result = self._values.get("saml")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeSaml"]]], result)

    @builtins.property
    def service_token(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#service_token AccessPolicy#service_token}.'''
        result = self._values.get("service_token")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyInclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeAzure",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "identity_provider_id": "identityProviderId"},
)
class AccessPolicyIncludeAzure:
    def __init__(
        self,
        *,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_provider_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#id AccessPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3934ff8bb0aa7cf88980c1a57a8d82485763f3fd8cbb39ac068681847a2e5f10)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id

    @builtins.property
    def id(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#id AccessPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyIncludeAzure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyIncludeAzureList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeAzureList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0aa05167434a2598f4ea65c78a7c0dd801fb9ca0d6c898b15c1f9bba0bb3c1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyIncludeAzureOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87e1d4becf1b0dc47a918888de762ae1dbcdca78cd47d2f5696cdf2df66f91e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyIncludeAzureOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaeb284d3ead63c5efa163567d04768592ce137a87ab1825ccd62c5d49a49851)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6953032138552c67d6430718d5202fb464ae704c4045075be7cbaaa4d84986e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c47629b63031e66530a89d72b6dde7fbdea4a17ac662db9d5c38726861bfd2d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeAzure]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeAzure]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeAzure]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a57eeee0c3bd05ea5e56753b4b6b7a2bd56ef05571f8aea5e58155179bb5f9d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyIncludeAzureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeAzureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4458ad2a53865fcbfe55b7fd8b21f87ebd5f0ed4ce0cdc49841fd348e567b705)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "id"))

    @id.setter
    def id(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e5a0068581af2b0f90d73819a72e7cc7504d07954e5ea6d4bb291821053789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230073dc79f2164d1fcec824288169d8045f524354ec02b061a1a8f99194235f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyIncludeAzure, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyIncludeAzure, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyIncludeAzure, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa46ff367be827f641a1df2cd50e559684f6029fd2a4f89d84a7476599314a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeExternalEvaluation",
    jsii_struct_bases=[],
    name_mapping={"evaluate_url": "evaluateUrl", "keys_url": "keysUrl"},
)
class AccessPolicyIncludeExternalEvaluation:
    def __init__(
        self,
        *,
        evaluate_url: typing.Optional[builtins.str] = None,
        keys_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluate_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#evaluate_url AccessPolicy#evaluate_url}.
        :param keys_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#keys_url AccessPolicy#keys_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edde7be87a8ba678fdd789315a28a1b86c6d4e88749e79c466238bcbcbf504e3)
            check_type(argname="argument evaluate_url", value=evaluate_url, expected_type=type_hints["evaluate_url"])
            check_type(argname="argument keys_url", value=keys_url, expected_type=type_hints["keys_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluate_url is not None:
            self._values["evaluate_url"] = evaluate_url
        if keys_url is not None:
            self._values["keys_url"] = keys_url

    @builtins.property
    def evaluate_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#evaluate_url AccessPolicy#evaluate_url}.'''
        result = self._values.get("evaluate_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keys_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#keys_url AccessPolicy#keys_url}.'''
        result = self._values.get("keys_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyIncludeExternalEvaluation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyIncludeExternalEvaluationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeExternalEvaluationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__731143a89fda40e3233b10bbdb626924e921eb6f8fdaea663e77583ecfb22784)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEvaluateUrl")
    def reset_evaluate_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluateUrl", []))

    @jsii.member(jsii_name="resetKeysUrl")
    def reset_keys_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeysUrl", []))

    @builtins.property
    @jsii.member(jsii_name="evaluateUrlInput")
    def evaluate_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluateUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="keysUrlInput")
    def keys_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keysUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluateUrl")
    def evaluate_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluateUrl"))

    @evaluate_url.setter
    def evaluate_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19d25126f7b0c88e2d50e51d3c7818e69cf0ab66030f18b76aa7b93e79e8813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluateUrl", value)

    @builtins.property
    @jsii.member(jsii_name="keysUrl")
    def keys_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keysUrl"))

    @keys_url.setter
    def keys_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8123a0071311fe1d701bf0d4e6d2867e0506926fc17328c100029eb02feee468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keysUrl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccessPolicyIncludeExternalEvaluation]:
        return typing.cast(typing.Optional[AccessPolicyIncludeExternalEvaluation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessPolicyIncludeExternalEvaluation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18d29491c3aee07592c3a91a5c9384842034c734ad7c0dc0c28c24bc81df1dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeGithub",
    jsii_struct_bases=[],
    name_mapping={
        "identity_provider_id": "identityProviderId",
        "name": "name",
        "teams": "teams",
    },
)
class AccessPolicyIncludeGithub:
    def __init__(
        self,
        *,
        identity_provider_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.
        :param teams: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#teams AccessPolicy#teams}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22198ae31009317a723ca1bbe62f3a31a753413bbdc28aa21c5fdc7ce01052ec)
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id
        if name is not None:
            self._values["name"] = name
        if teams is not None:
            self._values["teams"] = teams

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def teams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#teams AccessPolicy#teams}.'''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyIncludeGithub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyIncludeGithubList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeGithubList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cae97386eb42a38fb47476cc2d19a67d6e2457b66ce360ec6a146efaa469b35c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyIncludeGithubOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d1ea0cb148000de2dd291bd26e0b8ae8b0781e429d6c836bf402d8921a94c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyIncludeGithubOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7768e95f125991501fae9b84ad0f0d4f41c05f05507d808e4cd5778bc5d50d9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__257513b30c8c5a4765e63b4333845bd0a9fe6e1c1fd95f3f53e86b975e6aa741)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e88c6c3eee0cbf3e9fbc52b388ed7fc7d933c46b83abf5eb55cd297df64c80c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGithub]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGithub]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGithub]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3790ca2ed238ef071c93aed26db49851979a2fe081b2284c5d82690a6517c71e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyIncludeGithubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeGithubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2340254d2ab2bf6e14f0dbeb03719b37e056a5d58a732600c0d8e714849a54b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetTeams")
    def reset_teams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeams", []))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db5782d4c75671b766db5b047d4983217f50d0c9bae90c9c080c8e851d6f49eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb4155c7e51cef781842cadccf16b16ed1041794bf7bb6c50e46d1c0fdb77279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "teams"))

    @teams.setter
    def teams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfcbf3a282531ff5d8d79d8117ccf2ed55a7cd2df730244a792e2685f8b2b31a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teams", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyIncludeGithub, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyIncludeGithub, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyIncludeGithub, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097d0f38b868e8552d9946231ec29d078cdee42cc88376d0bfe847efe9b13014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeGsuite",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "identity_provider_id": "identityProviderId"},
)
class AccessPolicyIncludeGsuite:
    def __init__(
        self,
        *,
        email: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_provider_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dbdfc8a3d6e76921b2182aa3ab1088376de8f4cd24b441df1e6c4f4ee7debb1)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id

    @builtins.property
    def email(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyIncludeGsuite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyIncludeGsuiteList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeGsuiteList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ae80c8abcf0b5f83bc90f38803f9e074f1ca2dab3f0921ae65993b259d779e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyIncludeGsuiteOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ac8fb2c7ebb481186f6da23f3cdb84754849d4358df54d12991a6a38aa51ff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyIncludeGsuiteOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142d479600e26cb5be7393040b1ea518b271a117edbb982a4149c5f4653c70f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bca8713cfc321cb97bd47cf2f629b798f0ddc6c715c4359c5467631270365ee0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb8e02bf3ed277c570c0e2e0ba92bdf13f9f685ec7d6d0d64eb2596ad455bd58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGsuite]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGsuite]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGsuite]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2f4f26f425cea945d6b47475ba019adc83789d652806fdcfa498190f2ff561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyIncludeGsuiteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeGsuiteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7338f427af8584f2283425807f407a5b9b0e426e0173b66f112e88414c3886f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "email"))

    @email.setter
    def email(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e16a34212c127a45d08dd15dabd9ad78159d8858671ed6ae30dc60e195be20bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4c30fff648171b7b40a5776725ae6b42277f40180146a5033de95a5826a731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyIncludeGsuite, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyIncludeGsuite, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyIncludeGsuite, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9998eb01089a94bdb625db2eb187f0a89dabb3d5f1551ed4d73ac243889604d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyIncludeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae3dd568166a353ef3ec6578d829e40e28ad44672799f6f1504276ac2f921bf7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyIncludeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0ac8ca6f26bc2bfc9985db822b66814b41e74aafb4e93060f891e958c58601)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyIncludeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77829cb286e37da020695da89329b151a1d791ee73eddb81f924bcf82895fbc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57bacea9b0fede6644e06080c0b9ff298fa2708a2c705d15cbf36685356806d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d06355ba457b6955712179a0759587a7f30027f2fa17da852f8aeea46acafb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyInclude]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyInclude]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyInclude]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eeeadc0f5788c9a4a0b3eabc0508dd993bfc9f7cb57767b753ba0baa41ad1b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeOkta",
    jsii_struct_bases=[],
    name_mapping={"identity_provider_id": "identityProviderId", "name": "name"},
)
class AccessPolicyIncludeOkta:
    def __init__(
        self,
        *,
        identity_provider_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68e736525185a389784f257f6523ad7a1618bdd1c009deabb3c448ffbda116c)
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyIncludeOkta(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyIncludeOktaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeOktaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__307fe7b8a98e8231bd3b827a0d55a095a96786a0c882390312059528e12f95e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyIncludeOktaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67694ae0ff0607e465ca91efd86c3f73b37e29d2847fccfe064b74384b8bcb9b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyIncludeOktaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d6150e477f74f6e796d9944e46352de34a297a440944f70f4ebdc762080a5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6455150b51501aca494bfc3253f955a48cac67adcafe52ebc3f5552621ea8528)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9fe456bfd84ab8480554ae729ac67d75eb0c2e38da968410f047a7f7b0434e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeOkta]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeOkta]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeOkta]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae149d5791cef25d351587c1a679ed5e3a1ef26e6f0690807fda4a0b53e43f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyIncludeOktaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeOktaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__984269807a712f265fe7682cfdd7abfaf9596d7e94a9c1fd92827ffdc87aba9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa55bec9af1685b78de506123abb717afd9a196bacc4e34e4d86024e630764b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d1979574ace9ce4852e9e5df4a926924ec982a5789751f5bca6a605f872266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyIncludeOkta, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyIncludeOkta, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyIncludeOkta, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4018a89c43a2d7dec4d671f861bb4f2e5d0cd25660df1eb32f2c386c226f6627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyIncludeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f772a983e4e7937a9adc8bb112711de542bbab1d734b9e33c979b16f430b722a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAzure")
    def put_azure(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeAzure, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6496b428d419ff77386f1e0175493e47fcfec80705366dcc482b1c5cdb3c334f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAzure", [value]))

    @jsii.member(jsii_name="putExternalEvaluation")
    def put_external_evaluation(
        self,
        *,
        evaluate_url: typing.Optional[builtins.str] = None,
        keys_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluate_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#evaluate_url AccessPolicy#evaluate_url}.
        :param keys_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#keys_url AccessPolicy#keys_url}.
        '''
        value = AccessPolicyIncludeExternalEvaluation(
            evaluate_url=evaluate_url, keys_url=keys_url
        )

        return typing.cast(None, jsii.invoke(self, "putExternalEvaluation", [value]))

    @jsii.member(jsii_name="putGithub")
    def put_github(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeGithub, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd050234f83da902debed59b13b15ac75a22a67970d0850c2f62b18c7168c6f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGithub", [value]))

    @jsii.member(jsii_name="putGsuite")
    def put_gsuite(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeGsuite, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0756502e2dfb2d6abdec4ef32710e7e3a03a7fa2bceb1d2324faa45ec8ab71b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGsuite", [value]))

    @jsii.member(jsii_name="putOkta")
    def put_okta(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeOkta, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb71f46fa1eb9421affb9a106d5cdbc59b37761760df32b2aa367eec617cbc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOkta", [value]))

    @jsii.member(jsii_name="putSaml")
    def put_saml(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyIncludeSaml", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a814ff4185e2e8e611d3e90b40c8391c611ee03db55a4b0caf3d2b3e23330e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSaml", [value]))

    @jsii.member(jsii_name="resetAnyValidServiceToken")
    def reset_any_valid_service_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnyValidServiceToken", []))

    @jsii.member(jsii_name="resetAuthMethod")
    def reset_auth_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthMethod", []))

    @jsii.member(jsii_name="resetAzure")
    def reset_azure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzure", []))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCommonName")
    def reset_common_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonName", []))

    @jsii.member(jsii_name="resetDevicePosture")
    def reset_device_posture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevicePosture", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetEmailDomain")
    def reset_email_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailDomain", []))

    @jsii.member(jsii_name="resetEveryone")
    def reset_everyone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEveryone", []))

    @jsii.member(jsii_name="resetExternalEvaluation")
    def reset_external_evaluation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalEvaluation", []))

    @jsii.member(jsii_name="resetGeo")
    def reset_geo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeo", []))

    @jsii.member(jsii_name="resetGithub")
    def reset_github(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithub", []))

    @jsii.member(jsii_name="resetGroup")
    def reset_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroup", []))

    @jsii.member(jsii_name="resetGsuite")
    def reset_gsuite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGsuite", []))

    @jsii.member(jsii_name="resetIp")
    def reset_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIp", []))

    @jsii.member(jsii_name="resetLoginMethod")
    def reset_login_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginMethod", []))

    @jsii.member(jsii_name="resetOkta")
    def reset_okta(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOkta", []))

    @jsii.member(jsii_name="resetSaml")
    def reset_saml(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml", []))

    @jsii.member(jsii_name="resetServiceToken")
    def reset_service_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceToken", []))

    @builtins.property
    @jsii.member(jsii_name="azure")
    def azure(self) -> AccessPolicyIncludeAzureList:
        return typing.cast(AccessPolicyIncludeAzureList, jsii.get(self, "azure"))

    @builtins.property
    @jsii.member(jsii_name="externalEvaluation")
    def external_evaluation(
        self,
    ) -> AccessPolicyIncludeExternalEvaluationOutputReference:
        return typing.cast(AccessPolicyIncludeExternalEvaluationOutputReference, jsii.get(self, "externalEvaluation"))

    @builtins.property
    @jsii.member(jsii_name="github")
    def github(self) -> AccessPolicyIncludeGithubList:
        return typing.cast(AccessPolicyIncludeGithubList, jsii.get(self, "github"))

    @builtins.property
    @jsii.member(jsii_name="gsuite")
    def gsuite(self) -> AccessPolicyIncludeGsuiteList:
        return typing.cast(AccessPolicyIncludeGsuiteList, jsii.get(self, "gsuite"))

    @builtins.property
    @jsii.member(jsii_name="okta")
    def okta(self) -> AccessPolicyIncludeOktaList:
        return typing.cast(AccessPolicyIncludeOktaList, jsii.get(self, "okta"))

    @builtins.property
    @jsii.member(jsii_name="saml")
    def saml(self) -> "AccessPolicyIncludeSamlList":
        return typing.cast("AccessPolicyIncludeSamlList", jsii.get(self, "saml"))

    @builtins.property
    @jsii.member(jsii_name="anyValidServiceTokenInput")
    def any_valid_service_token_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "anyValidServiceTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="authMethodInput")
    def auth_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="azureInput")
    def azure_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeAzure]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeAzure]]], jsii.get(self, "azureInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="commonNameInput")
    def common_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="devicePostureInput")
    def device_posture_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "devicePostureInput"))

    @builtins.property
    @jsii.member(jsii_name="emailDomainInput")
    def email_domain_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="everyoneInput")
    def everyone_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "everyoneInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEvaluationInput")
    def external_evaluation_input(
        self,
    ) -> typing.Optional[AccessPolicyIncludeExternalEvaluation]:
        return typing.cast(typing.Optional[AccessPolicyIncludeExternalEvaluation], jsii.get(self, "externalEvaluationInput"))

    @builtins.property
    @jsii.member(jsii_name="geoInput")
    def geo_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "geoInput"))

    @builtins.property
    @jsii.member(jsii_name="githubInput")
    def github_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGithub]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGithub]]], jsii.get(self, "githubInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="gsuiteInput")
    def gsuite_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGsuite]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGsuite]]], jsii.get(self, "gsuiteInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="loginMethodInput")
    def login_method_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loginMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaInput")
    def okta_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeOkta]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeOkta]]], jsii.get(self, "oktaInput"))

    @builtins.property
    @jsii.member(jsii_name="samlInput")
    def saml_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeSaml"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyIncludeSaml"]]], jsii.get(self, "samlInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTokenInput")
    def service_token_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="anyValidServiceToken")
    def any_valid_service_token(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "anyValidServiceToken"))

    @any_valid_service_token.setter
    def any_valid_service_token(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2dba7569072c26c8ead4fc8135bc0b472e1dbf9eec8107fe9e04e5b391e99f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anyValidServiceToken", value)

    @builtins.property
    @jsii.member(jsii_name="authMethod")
    def auth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authMethod"))

    @auth_method.setter
    def auth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1440a9bb8aa242010dc7ea34223358e8e8fd42a60425fb9d3d2120449a58f792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authMethod", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470d2f6309bb91b1171bd2a86dc0c33c0fb8f255d2554bcbc7dfa465c41a54fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonName"))

    @common_name.setter
    def common_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de34861ee30d0c8a269f43753ce5fd8b42d7c192aad5b5cbd1e6ba4a992c5f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonName", value)

    @builtins.property
    @jsii.member(jsii_name="devicePosture")
    def device_posture(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "devicePosture"))

    @device_posture.setter
    def device_posture(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4fa838f2a769705159ae5841ee789f1ef4e2bb23419c3827d05e51885c6cb94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "devicePosture", value)

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "email"))

    @email.setter
    def email(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829583fb61afb5cd78b25183f44e4e481889b62cafd2e91653179f560dd9eab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="emailDomain")
    def email_domain(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailDomain"))

    @email_domain.setter
    def email_domain(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f316532ccaf3f368324b56ae019d5bbd3995687a22e28cdd398fdfc3aa742884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailDomain", value)

    @builtins.property
    @jsii.member(jsii_name="everyone")
    def everyone(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "everyone"))

    @everyone.setter
    def everyone(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443ba7868ff8a75bf9618187481914d9dd69e6e9fce32f6e5660d3d2b1100462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "everyone", value)

    @builtins.property
    @jsii.member(jsii_name="geo")
    def geo(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "geo"))

    @geo.setter
    def geo(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8b13abbcee4b8c982db96a9d22cb87a48c32d567afeb6a00aba712fc89ff19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geo", value)

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "group"))

    @group.setter
    def group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9625eef34773e43a104000cb879237f5d520cc52d3c5bd4369419d81f4887f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value)

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4994773d565590a64c8cb3b4b840c975d0327d23d55c421a1abaafee43233daf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value)

    @builtins.property
    @jsii.member(jsii_name="loginMethod")
    def login_method(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginMethod"))

    @login_method.setter
    def login_method(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71aac2f955b301fcd7622c5eb0fc16b48a97c8d2809f25a55ac0c49e34dc2f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginMethod", value)

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceToken"))

    @service_token.setter
    def service_token(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5666b1eb0c33252c5769221e832978e6183535000d4aa759795201d25fe40f4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceToken", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyInclude, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyInclude, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyInclude, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00274e393471eadab07e528bcf3332030c55d0d30890a532e70f4b15580eaa0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeSaml",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_name": "attributeName",
        "attribute_value": "attributeValue",
        "identity_provider_id": "identityProviderId",
    },
)
class AccessPolicyIncludeSaml:
    def __init__(
        self,
        *,
        attribute_name: typing.Optional[builtins.str] = None,
        attribute_value: typing.Optional[builtins.str] = None,
        identity_provider_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attribute_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_name AccessPolicy#attribute_name}.
        :param attribute_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_value AccessPolicy#attribute_value}.
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b50446c5aebaffb7b0813471069dd3e11fa4a2739f73ef076a44cd8b2491f5)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
            check_type(argname="argument attribute_value", value=attribute_value, expected_type=type_hints["attribute_value"])
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_name is not None:
            self._values["attribute_name"] = attribute_name
        if attribute_value is not None:
            self._values["attribute_value"] = attribute_value
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id

    @builtins.property
    def attribute_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_name AccessPolicy#attribute_name}.'''
        result = self._values.get("attribute_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attribute_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_value AccessPolicy#attribute_value}.'''
        result = self._values.get("attribute_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyIncludeSaml(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyIncludeSamlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeSamlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91899907563f0fb244b9323b68bcdbffe2a41626e07e5e9d5e951429318ed4a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyIncludeSamlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77dcd3ddf58736eaf632178fa12a36e3d66325f13c349e2fa5735d63e8cf0e89)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyIncludeSamlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d51a0ed8b30eac5d2817647e8edac79f5705c372a09aa66f232618b6dfe9d000)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be3c42ec8c5912108899ea01c1152ee1e2ea352d1eed0c9fa07b04cacb92d1b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__360d718fb5fe8ffdd870682fcba648e1939da510f2a9166589e3d1abfdd68be4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeSaml]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeSaml]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeSaml]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff8ea4f54e573dade9810aa8b68973829d6add29f8eb770c4f9fcc477b24773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyIncludeSamlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyIncludeSamlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebab05767071a22c21f41eeca850b650e1f127f6c60f1fdf76a8de8370edd212)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAttributeName")
    def reset_attribute_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeName", []))

    @jsii.member(jsii_name="resetAttributeValue")
    def reset_attribute_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeValue", []))

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @builtins.property
    @jsii.member(jsii_name="attributeNameInput")
    def attribute_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeValueInput")
    def attribute_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeValueInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeName")
    def attribute_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeName"))

    @attribute_name.setter
    def attribute_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c175f26e593dfd61f1a7cac525c91e23f17c4ae6ef1f78d71c7aefcfb9466e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeName", value)

    @builtins.property
    @jsii.member(jsii_name="attributeValue")
    def attribute_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeValue"))

    @attribute_value.setter
    def attribute_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9687376d518cb81c07c65645974dc58d892422a47b325a561c855dca05ea13f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeValue", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48aa0d7bc13b947da5df8bfe79b6f0ed0d94da5d83a31bf892767fcb506b7cc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyIncludeSaml, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyIncludeSaml, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyIncludeSaml, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fadae813314d360f5c9f04d80e0da414906dccba5ed891b873cfeb9cf18b11e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequire",
    jsii_struct_bases=[],
    name_mapping={
        "any_valid_service_token": "anyValidServiceToken",
        "auth_method": "authMethod",
        "azure": "azure",
        "certificate": "certificate",
        "common_name": "commonName",
        "device_posture": "devicePosture",
        "email": "email",
        "email_domain": "emailDomain",
        "everyone": "everyone",
        "external_evaluation": "externalEvaluation",
        "geo": "geo",
        "github": "github",
        "group": "group",
        "gsuite": "gsuite",
        "ip": "ip",
        "login_method": "loginMethod",
        "okta": "okta",
        "saml": "saml",
        "service_token": "serviceToken",
    },
)
class AccessPolicyRequire:
    def __init__(
        self,
        *,
        any_valid_service_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auth_method: typing.Optional[builtins.str] = None,
        azure: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyRequireAzure", typing.Dict[builtins.str, typing.Any]]]]] = None,
        certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        common_name: typing.Optional[builtins.str] = None,
        device_posture: typing.Optional[typing.Sequence[builtins.str]] = None,
        email: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_domain: typing.Optional[typing.Sequence[builtins.str]] = None,
        everyone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_evaluation: typing.Optional[typing.Union["AccessPolicyRequireExternalEvaluation", typing.Dict[builtins.str, typing.Any]]] = None,
        geo: typing.Optional[typing.Sequence[builtins.str]] = None,
        github: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyRequireGithub", typing.Dict[builtins.str, typing.Any]]]]] = None,
        group: typing.Optional[typing.Sequence[builtins.str]] = None,
        gsuite: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyRequireGsuite", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_method: typing.Optional[typing.Sequence[builtins.str]] = None,
        okta: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyRequireOkta", typing.Dict[builtins.str, typing.Any]]]]] = None,
        saml: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyRequireSaml", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_token: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param any_valid_service_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#any_valid_service_token AccessPolicy#any_valid_service_token}.
        :param auth_method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#auth_method AccessPolicy#auth_method}.
        :param azure: azure block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#azure AccessPolicy#azure}
        :param certificate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#certificate AccessPolicy#certificate}.
        :param common_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#common_name AccessPolicy#common_name}.
        :param device_posture: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#device_posture AccessPolicy#device_posture}.
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.
        :param email_domain: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email_domain AccessPolicy#email_domain}.
        :param everyone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#everyone AccessPolicy#everyone}.
        :param external_evaluation: external_evaluation block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#external_evaluation AccessPolicy#external_evaluation}
        :param geo: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#geo AccessPolicy#geo}.
        :param github: github block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#github AccessPolicy#github}
        :param group: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#group AccessPolicy#group}.
        :param gsuite: gsuite block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#gsuite AccessPolicy#gsuite}
        :param ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#ip AccessPolicy#ip}.
        :param login_method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#login_method AccessPolicy#login_method}.
        :param okta: okta block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#okta AccessPolicy#okta}
        :param saml: saml block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#saml AccessPolicy#saml}
        :param service_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#service_token AccessPolicy#service_token}.
        '''
        if isinstance(external_evaluation, dict):
            external_evaluation = AccessPolicyRequireExternalEvaluation(**external_evaluation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a1d8a8011ef7f6a05eeb4b54966d10e4df2db7c9dffd0d69a7ce9d424599d3)
            check_type(argname="argument any_valid_service_token", value=any_valid_service_token, expected_type=type_hints["any_valid_service_token"])
            check_type(argname="argument auth_method", value=auth_method, expected_type=type_hints["auth_method"])
            check_type(argname="argument azure", value=azure, expected_type=type_hints["azure"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
            check_type(argname="argument device_posture", value=device_posture, expected_type=type_hints["device_posture"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument email_domain", value=email_domain, expected_type=type_hints["email_domain"])
            check_type(argname="argument everyone", value=everyone, expected_type=type_hints["everyone"])
            check_type(argname="argument external_evaluation", value=external_evaluation, expected_type=type_hints["external_evaluation"])
            check_type(argname="argument geo", value=geo, expected_type=type_hints["geo"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument gsuite", value=gsuite, expected_type=type_hints["gsuite"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument login_method", value=login_method, expected_type=type_hints["login_method"])
            check_type(argname="argument okta", value=okta, expected_type=type_hints["okta"])
            check_type(argname="argument saml", value=saml, expected_type=type_hints["saml"])
            check_type(argname="argument service_token", value=service_token, expected_type=type_hints["service_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if any_valid_service_token is not None:
            self._values["any_valid_service_token"] = any_valid_service_token
        if auth_method is not None:
            self._values["auth_method"] = auth_method
        if azure is not None:
            self._values["azure"] = azure
        if certificate is not None:
            self._values["certificate"] = certificate
        if common_name is not None:
            self._values["common_name"] = common_name
        if device_posture is not None:
            self._values["device_posture"] = device_posture
        if email is not None:
            self._values["email"] = email
        if email_domain is not None:
            self._values["email_domain"] = email_domain
        if everyone is not None:
            self._values["everyone"] = everyone
        if external_evaluation is not None:
            self._values["external_evaluation"] = external_evaluation
        if geo is not None:
            self._values["geo"] = geo
        if github is not None:
            self._values["github"] = github
        if group is not None:
            self._values["group"] = group
        if gsuite is not None:
            self._values["gsuite"] = gsuite
        if ip is not None:
            self._values["ip"] = ip
        if login_method is not None:
            self._values["login_method"] = login_method
        if okta is not None:
            self._values["okta"] = okta
        if saml is not None:
            self._values["saml"] = saml
        if service_token is not None:
            self._values["service_token"] = service_token

    @builtins.property
    def any_valid_service_token(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#any_valid_service_token AccessPolicy#any_valid_service_token}.'''
        result = self._values.get("any_valid_service_token")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auth_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#auth_method AccessPolicy#auth_method}.'''
        result = self._values.get("auth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireAzure"]]]:
        '''azure block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#azure AccessPolicy#azure}
        '''
        result = self._values.get("azure")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireAzure"]]], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#certificate AccessPolicy#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def common_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#common_name AccessPolicy#common_name}.'''
        result = self._values.get("common_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_posture(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#device_posture AccessPolicy#device_posture}.'''
        result = self._values.get("device_posture")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_domain(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email_domain AccessPolicy#email_domain}.'''
        result = self._values.get("email_domain")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def everyone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#everyone AccessPolicy#everyone}.'''
        result = self._values.get("everyone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_evaluation(
        self,
    ) -> typing.Optional["AccessPolicyRequireExternalEvaluation"]:
        '''external_evaluation block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#external_evaluation AccessPolicy#external_evaluation}
        '''
        result = self._values.get("external_evaluation")
        return typing.cast(typing.Optional["AccessPolicyRequireExternalEvaluation"], result)

    @builtins.property
    def geo(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#geo AccessPolicy#geo}.'''
        result = self._values.get("geo")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def github(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireGithub"]]]:
        '''github block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#github AccessPolicy#github}
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireGithub"]]], result)

    @builtins.property
    def group(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#group AccessPolicy#group}.'''
        result = self._values.get("group")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def gsuite(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireGsuite"]]]:
        '''gsuite block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#gsuite AccessPolicy#gsuite}
        '''
        result = self._values.get("gsuite")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireGsuite"]]], result)

    @builtins.property
    def ip(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#ip AccessPolicy#ip}.'''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_method(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#login_method AccessPolicy#login_method}.'''
        result = self._values.get("login_method")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def okta(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireOkta"]]]:
        '''okta block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#okta AccessPolicy#okta}
        '''
        result = self._values.get("okta")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireOkta"]]], result)

    @builtins.property
    def saml(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireSaml"]]]:
        '''saml block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#saml AccessPolicy#saml}
        '''
        result = self._values.get("saml")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireSaml"]]], result)

    @builtins.property
    def service_token(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#service_token AccessPolicy#service_token}.'''
        result = self._values.get("service_token")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyRequire(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireAzure",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "identity_provider_id": "identityProviderId"},
)
class AccessPolicyRequireAzure:
    def __init__(
        self,
        *,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_provider_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#id AccessPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af178787ae750d4083934fc2b6feca8ea8351e20b9f21fa9c1d48ee08516737a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id

    @builtins.property
    def id(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#id AccessPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyRequireAzure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyRequireAzureList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireAzureList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e70560147f51a74668b36e1644beec217be38e42cf70cdd6c1e96dfc6326a652)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyRequireAzureOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f63ee78c1c1c4a4045903e2f29d44bf39af3bcc81065e3aa4c8c77997970df9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyRequireAzureOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d98c1980cb5d78119990af2dcdead5a598a3a1b9f3583cdbb8f923dac05de4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ee2749d85b07683a1605f1b4fec8d50a5d55b4a83889f82574e60474417264a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9906f6e6613e95b6e1205df02a4cd54103862c2c46274165234e6d34bbf97c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireAzure]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireAzure]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireAzure]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d7b84ffde2b1f18400fe67ea4328163dc98a557661dbf2adde1e7db365cc32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyRequireAzureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireAzureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfb8cd0309e3f0f3ef131080afc69b34bd62661de72effc00d333099ac700569)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "id"))

    @id.setter
    def id(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd0af73be81674640f8cdbf46f0994cccc2edb63f8fca984c55f6c5ad225623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417af373e0d1a759816f6d09cd4f4efe47cdaa45ddaaf5999afc91241ed2150d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyRequireAzure, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyRequireAzure, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyRequireAzure, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f67c57c52f4b9ef20d4f3318ed26ca081bba3b534f6017100d59e80f69f2ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireExternalEvaluation",
    jsii_struct_bases=[],
    name_mapping={"evaluate_url": "evaluateUrl", "keys_url": "keysUrl"},
)
class AccessPolicyRequireExternalEvaluation:
    def __init__(
        self,
        *,
        evaluate_url: typing.Optional[builtins.str] = None,
        keys_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluate_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#evaluate_url AccessPolicy#evaluate_url}.
        :param keys_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#keys_url AccessPolicy#keys_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5189490fe5cb30537b55b8815efaeb2b5ab3d87b14b64c525242f5f4cc56d30b)
            check_type(argname="argument evaluate_url", value=evaluate_url, expected_type=type_hints["evaluate_url"])
            check_type(argname="argument keys_url", value=keys_url, expected_type=type_hints["keys_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluate_url is not None:
            self._values["evaluate_url"] = evaluate_url
        if keys_url is not None:
            self._values["keys_url"] = keys_url

    @builtins.property
    def evaluate_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#evaluate_url AccessPolicy#evaluate_url}.'''
        result = self._values.get("evaluate_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keys_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#keys_url AccessPolicy#keys_url}.'''
        result = self._values.get("keys_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyRequireExternalEvaluation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyRequireExternalEvaluationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireExternalEvaluationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bf2f5a5aa1d7538d34565bdd313b3006879c3e0a9924459606e6c19fbd4391e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEvaluateUrl")
    def reset_evaluate_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluateUrl", []))

    @jsii.member(jsii_name="resetKeysUrl")
    def reset_keys_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeysUrl", []))

    @builtins.property
    @jsii.member(jsii_name="evaluateUrlInput")
    def evaluate_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluateUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="keysUrlInput")
    def keys_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keysUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluateUrl")
    def evaluate_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluateUrl"))

    @evaluate_url.setter
    def evaluate_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a304dbff6270b92ebf6564e030f55e621fc5a3de2e822670f0435ec5f52c5577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluateUrl", value)

    @builtins.property
    @jsii.member(jsii_name="keysUrl")
    def keys_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keysUrl"))

    @keys_url.setter
    def keys_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2168810e2ca23e1c6da552ff6cbadcab901aad5406e425fdb59b1c504ee1c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keysUrl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccessPolicyRequireExternalEvaluation]:
        return typing.cast(typing.Optional[AccessPolicyRequireExternalEvaluation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessPolicyRequireExternalEvaluation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8223a1b297cc20b8ad5d102df3e7c22bf60841612c51d47ca4f7619bea3452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireGithub",
    jsii_struct_bases=[],
    name_mapping={
        "identity_provider_id": "identityProviderId",
        "name": "name",
        "teams": "teams",
    },
)
class AccessPolicyRequireGithub:
    def __init__(
        self,
        *,
        identity_provider_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.
        :param teams: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#teams AccessPolicy#teams}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d1abeff207dfce282f94077f48ad839fc26b80bea39674a7efd6da13903f75)
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id
        if name is not None:
            self._values["name"] = name
        if teams is not None:
            self._values["teams"] = teams

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def teams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#teams AccessPolicy#teams}.'''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyRequireGithub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyRequireGithubList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireGithubList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0a98194246b7ee8add3040ff40204514fea2006a9e61a38409b7b020c18c5c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyRequireGithubOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865230b1a057fef6cf330af36de81b319bc76b2dbc468549703166002fcdb2a4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyRequireGithubOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6feea9da9f33889c5555adc47093e25bea5f3d0e530ccf6938ae47a751ed5dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab62fb21d8316ca57b79c5a0e8be5ce0dde1991d84f5feccf39b097e0fceeec0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d6c34579ec3f9a650fe652c3ce17eb837bf51cb5b0c21691a885ce82a3c5ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGithub]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGithub]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGithub]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906ee90812e9c2bd3184f015905efbabefbba6947080bd3740762e1646ba8206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyRequireGithubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireGithubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15bb1f322ae8b6266794da352f0e0868065f267b39bc08c747dd3319a800c82c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetTeams")
    def reset_teams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeams", []))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1393d71aeac5dad6fdf9fde1313936107183aaf993c1e274a81fdc3ff609aa17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed4fcc1a2e47da7111606a7b2f951f5b81522dd1c9267a665f907bac3b6db17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "teams"))

    @teams.setter
    def teams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c8996c6836466e55d5887a0229d102bfe03915d018b0a8087aa1aeaf7658c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teams", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyRequireGithub, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyRequireGithub, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyRequireGithub, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be7b7c0b21b8b6b0ccab72827fd6d3a41c77ef92a9c869285d10f8f4b077bdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireGsuite",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "identity_provider_id": "identityProviderId"},
)
class AccessPolicyRequireGsuite:
    def __init__(
        self,
        *,
        email: typing.Optional[typing.Sequence[builtins.str]] = None,
        identity_provider_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b88b05b5fc64d4904f6366af5cefa415986a2eed00b671871db6cdeeff591b)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id

    @builtins.property
    def email(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#email AccessPolicy#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyRequireGsuite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyRequireGsuiteList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireGsuiteList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__108f18ec63199cadcff87c25bf051be5ea6c0293b1a6832a49121eadaf857f85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyRequireGsuiteOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eadf330ebd5af6c54cc5b4ad98a8f5a533be753187fb1195a87f372edebb0540)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyRequireGsuiteOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54775d6bd3dfc9d0dc7e068146fd3eafe9a06dc988cb13fa2b22a5fad21614fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eed48bc1bd44aab28f8cc0813c5330b5a6e6d40934176f13bf061aeb3116c9ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49b781ad024b300dcff43df0b286f3d575751942023004cf475ed3abcc58b318)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGsuite]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGsuite]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGsuite]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dac2eeeb05f5aae30f45e9ed278dd084b949f9b5a19a5fb4423f1018c84ac9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyRequireGsuiteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireGsuiteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3c3a53a410c1b1fefca5844d20f817178eaed4f8a640a03f43dc62a6355cca7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "email"))

    @email.setter
    def email(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a5767aec6c9bc12edbafba9194feaa94484d8444d7a188ad53800a289a05f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163ca3cf47337fcf8a889cb8c6779869378c65adae7632a8cec4244704587d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyRequireGsuite, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyRequireGsuite, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyRequireGsuite, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c58bad664d508dd9c0a65dcc8aa31625ccd9c2ff51845b3997186025c8abce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyRequireList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed0b2e8cbf51d1d3fdb2db0ac17f39b49505a3d01b99e585f533610dfa086e36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyRequireOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bda79d7b5243c45c00a143acd0ba9a7a4f6e785250844dd187e5643d85ef682)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyRequireOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f910cb8d7cb2daf1b9aa2aee0c0eb4b7255c69d9cd2ba1b983f7b226fe8213ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__042c3e6eb5d4a3c85115066dee4a67adcb75a2f2ebdec4c3df473b8fd6820f41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffb5105feea0108b461396a8dc57b9f86f1ec4bbbdb7ee7c9a04640478486a2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequire]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequire]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequire]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421136bc24cd864892aaf19226bfbee583d86327c846f384828a9e9d01bd4063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireOkta",
    jsii_struct_bases=[],
    name_mapping={"identity_provider_id": "identityProviderId", "name": "name"},
)
class AccessPolicyRequireOkta:
    def __init__(
        self,
        *,
        identity_provider_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf465a602e6c58158e9fe7c3b4bcaffd4b9d94f1477e4e4a078ba34abf3b804)
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#name AccessPolicy#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyRequireOkta(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyRequireOktaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireOktaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce3ee18caed3713980c595f788afd78a3cadf5dcfe843bc2ad9096e66bc1b8c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyRequireOktaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4f807afadff897136c522d75640bab58c4df01bde9dd0dd1f9b5a1f9299208)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyRequireOktaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ea39277718b4dd2d401d97ce263721fce79252b6856bf39a625373ed031086)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4823230d4aa26a4ae917d1c79215451c8331653dcf5c0be80501d02827e54eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11d4c8e9ff611f44db7243e89034aa7ab6b9be7d07d7aee0a485e2b6b649263c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireOkta]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireOkta]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireOkta]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d00d9b7f40a2df9b019e54445940ca6f44ea5792f46d8da6c019ba5af7dc31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyRequireOktaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireOktaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f6f3aa9354625aa7a0d448b1b80c6dde175aacb4acf435f02138e6f518c1f6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d040244d2119974456529689ecbb19035601092b3c78a701b618efb7dc35e960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f78d1007ba4822835befa566dcb7d57654f772c1d0b37f788b1f988e2ae0799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyRequireOkta, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyRequireOkta, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyRequireOkta, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504e5db5de400b37e2218cfb2fe20778dea169a39e64ffd8a8cb9a09c4a83e65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyRequireOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16a342121f2f9fed5f9b13c6903963a90ee4b7f7e9de6021db62e4a5f7e8d847)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAzure")
    def put_azure(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireAzure, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8542a2a4e99f4ff12dd10abc36032366e06765373025a2cebb848841fea555d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAzure", [value]))

    @jsii.member(jsii_name="putExternalEvaluation")
    def put_external_evaluation(
        self,
        *,
        evaluate_url: typing.Optional[builtins.str] = None,
        keys_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluate_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#evaluate_url AccessPolicy#evaluate_url}.
        :param keys_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#keys_url AccessPolicy#keys_url}.
        '''
        value = AccessPolicyRequireExternalEvaluation(
            evaluate_url=evaluate_url, keys_url=keys_url
        )

        return typing.cast(None, jsii.invoke(self, "putExternalEvaluation", [value]))

    @jsii.member(jsii_name="putGithub")
    def put_github(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireGithub, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9bac3e7d051e0cde3805a0a4d83fd9694331fa26c840e633042a7edaaf6adb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGithub", [value]))

    @jsii.member(jsii_name="putGsuite")
    def put_gsuite(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireGsuite, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec75de26e60fddd8e0bd8ab25c7a1c1d263f80c58912640846fef2983b6e13a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGsuite", [value]))

    @jsii.member(jsii_name="putOkta")
    def put_okta(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireOkta, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8f231bb1c77c70162315b4a2c6daa183cb0248794c090561513d75a3c02569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOkta", [value]))

    @jsii.member(jsii_name="putSaml")
    def put_saml(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessPolicyRequireSaml", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b01ad3abe5cee7d1828b48922131dea7003cdc7adc3d906c4b3635f2dc89d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSaml", [value]))

    @jsii.member(jsii_name="resetAnyValidServiceToken")
    def reset_any_valid_service_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnyValidServiceToken", []))

    @jsii.member(jsii_name="resetAuthMethod")
    def reset_auth_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthMethod", []))

    @jsii.member(jsii_name="resetAzure")
    def reset_azure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzure", []))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCommonName")
    def reset_common_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonName", []))

    @jsii.member(jsii_name="resetDevicePosture")
    def reset_device_posture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevicePosture", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetEmailDomain")
    def reset_email_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailDomain", []))

    @jsii.member(jsii_name="resetEveryone")
    def reset_everyone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEveryone", []))

    @jsii.member(jsii_name="resetExternalEvaluation")
    def reset_external_evaluation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalEvaluation", []))

    @jsii.member(jsii_name="resetGeo")
    def reset_geo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeo", []))

    @jsii.member(jsii_name="resetGithub")
    def reset_github(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithub", []))

    @jsii.member(jsii_name="resetGroup")
    def reset_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroup", []))

    @jsii.member(jsii_name="resetGsuite")
    def reset_gsuite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGsuite", []))

    @jsii.member(jsii_name="resetIp")
    def reset_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIp", []))

    @jsii.member(jsii_name="resetLoginMethod")
    def reset_login_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginMethod", []))

    @jsii.member(jsii_name="resetOkta")
    def reset_okta(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOkta", []))

    @jsii.member(jsii_name="resetSaml")
    def reset_saml(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaml", []))

    @jsii.member(jsii_name="resetServiceToken")
    def reset_service_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceToken", []))

    @builtins.property
    @jsii.member(jsii_name="azure")
    def azure(self) -> AccessPolicyRequireAzureList:
        return typing.cast(AccessPolicyRequireAzureList, jsii.get(self, "azure"))

    @builtins.property
    @jsii.member(jsii_name="externalEvaluation")
    def external_evaluation(
        self,
    ) -> AccessPolicyRequireExternalEvaluationOutputReference:
        return typing.cast(AccessPolicyRequireExternalEvaluationOutputReference, jsii.get(self, "externalEvaluation"))

    @builtins.property
    @jsii.member(jsii_name="github")
    def github(self) -> AccessPolicyRequireGithubList:
        return typing.cast(AccessPolicyRequireGithubList, jsii.get(self, "github"))

    @builtins.property
    @jsii.member(jsii_name="gsuite")
    def gsuite(self) -> AccessPolicyRequireGsuiteList:
        return typing.cast(AccessPolicyRequireGsuiteList, jsii.get(self, "gsuite"))

    @builtins.property
    @jsii.member(jsii_name="okta")
    def okta(self) -> AccessPolicyRequireOktaList:
        return typing.cast(AccessPolicyRequireOktaList, jsii.get(self, "okta"))

    @builtins.property
    @jsii.member(jsii_name="saml")
    def saml(self) -> "AccessPolicyRequireSamlList":
        return typing.cast("AccessPolicyRequireSamlList", jsii.get(self, "saml"))

    @builtins.property
    @jsii.member(jsii_name="anyValidServiceTokenInput")
    def any_valid_service_token_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "anyValidServiceTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="authMethodInput")
    def auth_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="azureInput")
    def azure_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireAzure]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireAzure]]], jsii.get(self, "azureInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="commonNameInput")
    def common_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="devicePostureInput")
    def device_posture_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "devicePostureInput"))

    @builtins.property
    @jsii.member(jsii_name="emailDomainInput")
    def email_domain_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="everyoneInput")
    def everyone_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "everyoneInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEvaluationInput")
    def external_evaluation_input(
        self,
    ) -> typing.Optional[AccessPolicyRequireExternalEvaluation]:
        return typing.cast(typing.Optional[AccessPolicyRequireExternalEvaluation], jsii.get(self, "externalEvaluationInput"))

    @builtins.property
    @jsii.member(jsii_name="geoInput")
    def geo_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "geoInput"))

    @builtins.property
    @jsii.member(jsii_name="githubInput")
    def github_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGithub]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGithub]]], jsii.get(self, "githubInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="gsuiteInput")
    def gsuite_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGsuite]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGsuite]]], jsii.get(self, "gsuiteInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="loginMethodInput")
    def login_method_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loginMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaInput")
    def okta_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireOkta]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireOkta]]], jsii.get(self, "oktaInput"))

    @builtins.property
    @jsii.member(jsii_name="samlInput")
    def saml_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireSaml"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessPolicyRequireSaml"]]], jsii.get(self, "samlInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTokenInput")
    def service_token_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="anyValidServiceToken")
    def any_valid_service_token(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "anyValidServiceToken"))

    @any_valid_service_token.setter
    def any_valid_service_token(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f134f242e91265ab53a0d9fa168305f5f65ad1b56bd2d0986c4247615cb090d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anyValidServiceToken", value)

    @builtins.property
    @jsii.member(jsii_name="authMethod")
    def auth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authMethod"))

    @auth_method.setter
    def auth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5e7aceae03a9abf9f0919c7cfae51a256058e1b5a51a949b25721f362d7482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authMethod", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88bc0df710eb7d22233973da2cd941851ca68f50ace12a19e7c7ad2068e0093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonName"))

    @common_name.setter
    def common_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8da47610fc0c40817ce66448079e3f1da84357e71ff337d018870cf4e847d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonName", value)

    @builtins.property
    @jsii.member(jsii_name="devicePosture")
    def device_posture(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "devicePosture"))

    @device_posture.setter
    def device_posture(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5878f820b9ab9f244dbc276cc192c3471bf6f5381fe109c3a739f665bf9c38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "devicePosture", value)

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "email"))

    @email.setter
    def email(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282e805dbc198ed2343700ef5a746ee55677a62676c5c97caf724a9244ed5c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="emailDomain")
    def email_domain(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailDomain"))

    @email_domain.setter
    def email_domain(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf53c62f9f09ec4a67a47d7444ff461e5675ff3f1b8fa6f660935979c1747e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailDomain", value)

    @builtins.property
    @jsii.member(jsii_name="everyone")
    def everyone(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "everyone"))

    @everyone.setter
    def everyone(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783d966d008fbc9122b9b37facf4522e20b1d7d85686c99a663bfbe4a0f8f046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "everyone", value)

    @builtins.property
    @jsii.member(jsii_name="geo")
    def geo(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "geo"))

    @geo.setter
    def geo(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1766ef1c35afdd1db1ea3b7df612bbf17bfdcc0b99136617c34eb02225aa742a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geo", value)

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "group"))

    @group.setter
    def group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__befaa9a9dfb25953dee57b7a99c5fbf84102d901fa6389ca07669c0cd0852d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value)

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07666527c6d7d87439ae08602fa311310906ad050036d9e8ee028452711ca57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value)

    @builtins.property
    @jsii.member(jsii_name="loginMethod")
    def login_method(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginMethod"))

    @login_method.setter
    def login_method(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532515cf2da1cf2437a48ef89f72bed399374f3b5e2ee406a88919636a1a9181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginMethod", value)

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceToken"))

    @service_token.setter
    def service_token(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76385b23d67f8a90197a11040605e80e47c9c90afb94d0e48cead1f3ee0ea49d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceToken", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyRequire, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyRequire, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyRequire, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0564fdb2a990034ed0c8224f0edee9da190beeecf025963235a32f08f6f899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireSaml",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_name": "attributeName",
        "attribute_value": "attributeValue",
        "identity_provider_id": "identityProviderId",
    },
)
class AccessPolicyRequireSaml:
    def __init__(
        self,
        *,
        attribute_name: typing.Optional[builtins.str] = None,
        attribute_value: typing.Optional[builtins.str] = None,
        identity_provider_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attribute_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_name AccessPolicy#attribute_name}.
        :param attribute_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_value AccessPolicy#attribute_value}.
        :param identity_provider_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9cc628912e40622419e8d47faba59f6fa066c8481498ca22c467aeacfa0dd8f)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
            check_type(argname="argument attribute_value", value=attribute_value, expected_type=type_hints["attribute_value"])
            check_type(argname="argument identity_provider_id", value=identity_provider_id, expected_type=type_hints["identity_provider_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_name is not None:
            self._values["attribute_name"] = attribute_name
        if attribute_value is not None:
            self._values["attribute_value"] = attribute_value
        if identity_provider_id is not None:
            self._values["identity_provider_id"] = identity_provider_id

    @builtins.property
    def attribute_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_name AccessPolicy#attribute_name}.'''
        result = self._values.get("attribute_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attribute_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#attribute_value AccessPolicy#attribute_value}.'''
        result = self._values.get("attribute_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_policy#identity_provider_id AccessPolicy#identity_provider_id}.'''
        result = self._values.get("identity_provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPolicyRequireSaml(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessPolicyRequireSamlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireSamlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d44afc539a0b32810cab8bba8b55334a290c6a72ecb344d31d0968809423eef3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessPolicyRequireSamlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82446f270d73539b7691bb2272597e8438e17b87c99339ea23b5d164de3ee6a2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessPolicyRequireSamlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2909bc32bf0ef46e1c0eb39f6ef69e025a52f472c4dd1380c35583aa3072196)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb8a321ddbc6f614205c5862d9984d6881e27b6f8c0786a5f019be84fefb49b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d160ab14d9d80761db9fb053a9f633904da0738981e189c95efc755e3eadc9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireSaml]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireSaml]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireSaml]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f79598985429d880805af193c806eb4af55cb246da5e54f3e4370e843d014f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AccessPolicyRequireSamlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessPolicy.AccessPolicyRequireSamlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4d682643cb5ceca7009560ac9671178ec350297fe6ddd2342df6555456a2dde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAttributeName")
    def reset_attribute_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeName", []))

    @jsii.member(jsii_name="resetAttributeValue")
    def reset_attribute_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeValue", []))

    @jsii.member(jsii_name="resetIdentityProviderId")
    def reset_identity_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityProviderId", []))

    @builtins.property
    @jsii.member(jsii_name="attributeNameInput")
    def attribute_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeValueInput")
    def attribute_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeValueInput"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderIdInput")
    def identity_provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityProviderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeName")
    def attribute_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeName"))

    @attribute_name.setter
    def attribute_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968ac736e6cb9bd06a7200dcb1599adda51a9cc6a079f9fc0d1ce5afccbfcd2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeName", value)

    @builtins.property
    @jsii.member(jsii_name="attributeValue")
    def attribute_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeValue"))

    @attribute_value.setter
    def attribute_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a6d69b9f7179e0b0e20f8a276267b20b8c886def52ffdcc19abd5a3795be7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeValue", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderId")
    def identity_provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProviderId"))

    @identity_provider_id.setter
    def identity_provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0005865c9580411a34c1f329d6f79ecdf1cd83226d20414078f3db5aef8f9bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessPolicyRequireSaml, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessPolicyRequireSaml, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessPolicyRequireSaml, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c9426558d01a1155edc24659a6e2661f6cf73f8654e85d1eca3722836c6d37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AccessPolicy",
    "AccessPolicyApprovalGroup",
    "AccessPolicyApprovalGroupList",
    "AccessPolicyApprovalGroupOutputReference",
    "AccessPolicyConfig",
    "AccessPolicyExclude",
    "AccessPolicyExcludeAzure",
    "AccessPolicyExcludeAzureList",
    "AccessPolicyExcludeAzureOutputReference",
    "AccessPolicyExcludeExternalEvaluation",
    "AccessPolicyExcludeExternalEvaluationOutputReference",
    "AccessPolicyExcludeGithub",
    "AccessPolicyExcludeGithubList",
    "AccessPolicyExcludeGithubOutputReference",
    "AccessPolicyExcludeGsuite",
    "AccessPolicyExcludeGsuiteList",
    "AccessPolicyExcludeGsuiteOutputReference",
    "AccessPolicyExcludeList",
    "AccessPolicyExcludeOkta",
    "AccessPolicyExcludeOktaList",
    "AccessPolicyExcludeOktaOutputReference",
    "AccessPolicyExcludeOutputReference",
    "AccessPolicyExcludeSaml",
    "AccessPolicyExcludeSamlList",
    "AccessPolicyExcludeSamlOutputReference",
    "AccessPolicyInclude",
    "AccessPolicyIncludeAzure",
    "AccessPolicyIncludeAzureList",
    "AccessPolicyIncludeAzureOutputReference",
    "AccessPolicyIncludeExternalEvaluation",
    "AccessPolicyIncludeExternalEvaluationOutputReference",
    "AccessPolicyIncludeGithub",
    "AccessPolicyIncludeGithubList",
    "AccessPolicyIncludeGithubOutputReference",
    "AccessPolicyIncludeGsuite",
    "AccessPolicyIncludeGsuiteList",
    "AccessPolicyIncludeGsuiteOutputReference",
    "AccessPolicyIncludeList",
    "AccessPolicyIncludeOkta",
    "AccessPolicyIncludeOktaList",
    "AccessPolicyIncludeOktaOutputReference",
    "AccessPolicyIncludeOutputReference",
    "AccessPolicyIncludeSaml",
    "AccessPolicyIncludeSamlList",
    "AccessPolicyIncludeSamlOutputReference",
    "AccessPolicyRequire",
    "AccessPolicyRequireAzure",
    "AccessPolicyRequireAzureList",
    "AccessPolicyRequireAzureOutputReference",
    "AccessPolicyRequireExternalEvaluation",
    "AccessPolicyRequireExternalEvaluationOutputReference",
    "AccessPolicyRequireGithub",
    "AccessPolicyRequireGithubList",
    "AccessPolicyRequireGithubOutputReference",
    "AccessPolicyRequireGsuite",
    "AccessPolicyRequireGsuiteList",
    "AccessPolicyRequireGsuiteOutputReference",
    "AccessPolicyRequireList",
    "AccessPolicyRequireOkta",
    "AccessPolicyRequireOktaList",
    "AccessPolicyRequireOktaOutputReference",
    "AccessPolicyRequireOutputReference",
    "AccessPolicyRequireSaml",
    "AccessPolicyRequireSamlList",
    "AccessPolicyRequireSamlOutputReference",
]

publication.publish()

def _typecheckingstub__84803941c8b0f08e7908009abe099ae89c5da91512a76b9aabbb809ef3f0da7d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    application_id: builtins.str,
    decision: builtins.str,
    include: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyInclude, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    precedence: jsii.Number,
    account_id: typing.Optional[builtins.str] = None,
    approval_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyApprovalGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    purpose_justification_prompt: typing.Optional[builtins.str] = None,
    purpose_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequire, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zone_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__5aa8972525155999d841f3a4393f69b729b21a9736e053534d44d89f0f8bafcd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyApprovalGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32c29944eed015f4a1350b0ab83170336fb8f8318952fd64dabe02832182b54(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExclude, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385e62f86ec3e627635539700ed65f7fd1f20dccfd4cada85915c4fdfa90b420(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyInclude, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83433aad0de83bfa32006de2a7834ab5ec99bef96aeea7be43087442df6e08c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequire, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812687f01185441ed0ca5edcf80b05d1152b9618a859e6939dc7432a1186380b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78f82e7f0edde76df3916aa2de853ec94f806616d1d7825fcddc45300b8c4f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104e5c974bf6f1947b572ba76e322e0a986e67826a65aa9ff3cd48883250b4ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c042c21bc7ef2104917e21f2ca589e4f13a2c76206c2aa1a1b4b31fef79645(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee695d28b4960c15bd09dacb7c51c6684693333fe8a0e488d8ac139cb163dcf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ed9def2ee82e4e3267f7724b1f9c27228b54b1d8dd0bf4f0894d750f5152be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2355c681f01799e64e4a16b1e80139548a57f3e078fe1bc14c9708f1850134(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe7592280906da81037c8fec461aade9ce1d663f25601e4a0c7b33c649796f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b29d7a75d2b5be985401eec8131df6118b20b26a9ecb839a8c0745c1f12f8ad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a87d6fc4f2e1f19fface8408b9ae70b3b76ba1d966d011be8f31666c34c3ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af12df2711fe494f597739c90c8210d6e4dec8b622742112ea742514b2cc3061(
    *,
    approvals_needed: jsii.Number,
    email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_list_uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c01b59337d1d67a5c4a0ec0b823ebf43728835a045cecffa54b0df2227897cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069af8b87306c643e9d2060d82cd973a1e0c79817f5758eb21a35c84f755c6b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63635911ce44154eb320d00db2dc89fe65da7218ebd34bed65cd0f492791f8a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b003bd16123ef53c5173f00fd59090913eed2e7cccc5433543f47121f0a7999e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41e8096a0dacd1c279a02a96c4051086ffdad22820d2696339fa6865983d894(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c237e9adc126d2764ae36ced209698f9327c4d0bf5f656ed71f27e4cb8255493(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyApprovalGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401e950804cfb771af36b22864a3767285d7ccb8b9606e8a8bab7f49e7ae6abb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bfacab364a27b2d00942472d7e93325501e64e2802137bfd7f7cf2272f6f5fb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e86e938b41518c8666139198bf55e97925d68c1135fb1d0791fd8fefe9eda72(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddbc533fca520b702969ac17abc93af0e00b43fb56bc9559483ed65854409d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3051d8f46c0d8abe5093c13e1326c65e7673cda733bce29414e4807c51cfb8a6(
    value: typing.Optional[typing.Union[AccessPolicyApprovalGroup, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9c6708ac3ae02816b0ebbf61a38ba2e8505af5488f2844de55cafbc4d3fc3c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_id: builtins.str,
    decision: builtins.str,
    include: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyInclude, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    precedence: jsii.Number,
    account_id: typing.Optional[builtins.str] = None,
    approval_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyApprovalGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    approval_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExclude, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    purpose_justification_prompt: typing.Optional[builtins.str] = None,
    purpose_justification_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequire, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bd596c6f1f8c1e33c17f2a3fad0d68580170184200c2f6a94fd70f7be40cb6(
    *,
    any_valid_service_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auth_method: typing.Optional[builtins.str] = None,
    azure: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeAzure, typing.Dict[builtins.str, typing.Any]]]]] = None,
    certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    common_name: typing.Optional[builtins.str] = None,
    device_posture: typing.Optional[typing.Sequence[builtins.str]] = None,
    email: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_domain: typing.Optional[typing.Sequence[builtins.str]] = None,
    everyone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_evaluation: typing.Optional[typing.Union[AccessPolicyExcludeExternalEvaluation, typing.Dict[builtins.str, typing.Any]]] = None,
    geo: typing.Optional[typing.Sequence[builtins.str]] = None,
    github: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeGithub, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group: typing.Optional[typing.Sequence[builtins.str]] = None,
    gsuite: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeGsuite, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_method: typing.Optional[typing.Sequence[builtins.str]] = None,
    okta: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeOkta, typing.Dict[builtins.str, typing.Any]]]]] = None,
    saml: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeSaml, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_token: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe2352dbb106bb5d71983034609a84d021e9ebdff469dc72e5159cc2a5ec813(
    *,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_provider_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74583d6d8a2269a30f1851f87c4f626b088d42352e11895c4a5e72b2ca987d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22db79ab2f4ffb7503ce804377491a53c4826ec887b9dae4d09eb11c0bdd3962(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2a76703ee69726cbc543f5a6a65f1752f34d913b6623986f0a12c250eac876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19528b4dc4464229dac5b73e50f3e1f4f63b75188e1e2b64682fe3f076a1aa6d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a832d84de740e1367116ae2c7dbbde3bf9885a35336a2cbea51dcdc36830b2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec77b51c7e232fb71c13285c500ac8487232bfaf9978e72a51ee2230d0fe698c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeAzure]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4020e8b9b779a5ff9ca1f69480c317ea46af25b9e9fac5622aa193978633fd0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8bfa76994eb2d52d8f23ca4eeca81164fd517e686aae8cfd7d09c7ca71bfea(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699f783480367e127e3ac5eee51579d551082d36f9e376fcae9dabc2472daf99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c72a0cd934da86e1fc661ba5bb923c231bcf5f149b77ddc20e7b8900cd00555(
    value: typing.Optional[typing.Union[AccessPolicyExcludeAzure, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0708eefeb53f667c392a735574394dff4e9004f9d56c042b62018d5cf044c402(
    *,
    evaluate_url: typing.Optional[builtins.str] = None,
    keys_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c0d6ede8491c497eb534b2077288efb9b24fd5bba09234991ee972a77950da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ef8492f45d922d3a71213d7cc6da340889f1c0c6988c3070221a35137ea99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf3bee254cc20154fa5b91aef73d85e7ed1c2ca3048879710be3e866db6bb45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2dfc626f635ab8054a6d9e7108cbc3c5cbba735dada2c500ad937692632f19(
    value: typing.Optional[AccessPolicyExcludeExternalEvaluation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221e51c17a43211154739e44b1c48b957ad7bca748c5fc33fb2962d98c424b21(
    *,
    identity_provider_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    teams: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb42dda753b790ff7603efbe2e9d39c6801142f4514a11298ae343ef66a29e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab796aad987396af3d2143d29f27a9d4bff1d79f86a4d6dde1d62a7a5c87f936(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e466cb2b55215455d5135ed24120d48de380eacf8bdf2c3f4cf7c6b9e2e84a49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf58e8126566f565230c7a554ebeb1d070db85947f094701c224babbe3afc8d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec8dc46ce8a58ccc77079958af9603f548bff7b035180f7c1bea2513acf3b28(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33975837ebc1fc161780295e4031cc0745d6ca08ef890bbb0ef70d6061646cbe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGithub]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6448e05ff747b9cefbf154906574068ff220d194c4f8195e81caf8df8e835a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa04e3d10dae4da417b756f95b17a89c173d6107778a48d88964d09340c8b13f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4b74efaba86c82260fec61cf62d8e5dd71bee16c7c80564ad336f99ca940f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc4de1806c633c63db308c20b8f55371b1a77b12548394633e880c8a06da664(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53efc3cc4cbcbbf78652a6975bea620e02d5487f3de1dc9aecf4d73ef7d30122(
    value: typing.Optional[typing.Union[AccessPolicyExcludeGithub, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff3a53499e1a71c3d5b4f8433665416c1deee47649e4c1e12cf924a083b4acf(
    *,
    email: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_provider_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd629be31bbf1b7278065c67da9d6657abe6ecee322a41fc1aa269e8e3ad0ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ab9db55dfe2940159c7574801ef6f77092974f766c6d6e6cd122561434ae2e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ce475968d262f67a7b280a6e3b259b80808313671fa68fd23f7beee9d0d2d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb308e73c3e8e5ce5aacbfe07ff04648b68ef77009de1ab3c88b47dd6933e159(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b9f4a32730f819631265abd83fe9755e03bb2e751b8fe0cd99438d9f229931(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e39ceec195e67fc419a2c947d15dcc8047628b3b32875e194cf122bb505290(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeGsuite]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9697f0e25a18562bad456ea542529ddd5e9466f19f4b2da9ce8c5d6ba7b6de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c3fd03671e0fd947b6b50383e8a03a07820d4e056c026f667d8c8bf6610e8b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef9eb674412811e1a079e1e7b7e73d42fc405697185c30a4dee755c92b731ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26568adaf0fa9a476bdb968a19e0bce34644db9ac5f594f5b11185e01f2e3501(
    value: typing.Optional[typing.Union[AccessPolicyExcludeGsuite, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de05addc01948152a823f84f62efcb43f70e62117731e3a9c9eba6afa74ca25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8315c74e6eefea1427621fec8ab2bbbcc3639274ecc6f345ebedcfe553c642cb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ae839d5ceabfc049172f2e9e47e8d644405ec9c03a9cc6566d7b3f4b741590(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be32042fa401ccbc3fd5033e57f1c6d8d4b614a237afcb062c6b50ba0a0f2d8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70adb846604236b553ed608dc405462d6fd0acbbff310263de333618cc9e6662(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df467676956e07b69bafdd83a9e14ddd0d3abcd4d2830901769a49f82a94887(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExclude]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c54082121ca2289d82f2d843b24a05c387479b39e1cddd0e679af0e79eb801(
    *,
    identity_provider_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3e2bbee26487babf21c6c2491410967f3962bac7a0a9dd9e022c3e6cff4e30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2977bd3fd722d34bf685a9463783b0200fa04372e923e05c80a66ac35f23701d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcd9bf6decf0f6263aa6baad3082f18613b4c8b47ccf2f250b487241a22fd18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938752f671052e30cac449f7e2ad1ed0970b57c637e2f12a10e1e7b32bcdbede(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d584ea8ef9adc35162cecc7a8cd09b96ef63f491023a16f1117e8460b69645(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7646179bd32b841af52f1eada0beb9921243e74170a490173ab797a9327958cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeOkta]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812371f9629a8c5a28ad7d84a3ca29c9b596c58dcaa090f23c38777e07c5bf0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c704ea5a346c04e3065ed5f58da67a1b3a6693a19cc4302b2e591446d8c704b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce8b757a4b2b8f5f716bff169c2dc382210bb51a2cb5cf637a8fb28ca7d1ff6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54479f44d2c8a4c4d57775224dcb2214470465cf8dd7187bf3fb5cff6750c19(
    value: typing.Optional[typing.Union[AccessPolicyExcludeOkta, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf0e416bfe12d94850ab7b0c91a0c58c3b3289de81d11853bdb1509b4a2bd39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53dccb4f2837eecad7514db087ff0cb88d3c4dcd749eaf2c73a1dca8d71f64d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeAzure, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f007ad21c7899ad6ae212deaa65bce0a1b97557b5c1a92623c3e92dc002068d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeGithub, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83fda570c2acc71a553400e50a55cbc9b151f33df8c7b16957fc58f905b7b7cd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeGsuite, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af23a5888b64021868de935ad71d6555819b305648efae52323ab422dea8fb0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeOkta, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ee94a3cc9a781dfca740fcd489aa62c68cd546dafce25bcb36c397ae99d594(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyExcludeSaml, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0719a1e52e5e17e0882334df3df6e6e99ab05ed0011542c0fe451fb85f94c50b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf5aef3a6223af8de535a04fc764423942cfa94bde59ca86c1262577ecd7b173(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c72ca973764cd98fbc3b9cce847f2a98f3dde6882cf38b228b47125e243bc0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd6bb4ba387b9ee040536a3c21db56e736d19eb63a7ac8ce874dff3995f1179(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa67e4d5dd288c10bc2a7ef25075e6b3274b193070ac4d2aba4f20c4af695e3c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7279dee33d3c2625868506d07c40ba678c1740d2dfffad9c4e386783f8cc7e0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e724fc8eaf74d5dffb258775f0f17d6d9230f0f4bf12e27b4784483d86dbbd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aac89174bf5083e1c91b2e252fc52e34f50b12c3e27c5936e1aea98aad6fc30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90c69fcd1eab5430435a65174dcbeaecc447eb056b2abb54ce446694691fa8c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a40a143b2d67e812145475d298b8298c022b1dcb0e59f7df8ed5ec657a2db32(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb58b061d0aa36fb81f376843d93190bfdbec75d0edb0e3e2712c4da8374917f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d7932bb4ebd3c1f8540634c574ec2c47b8fc0a53687dc4f6acc9cf4c09598e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7631206af465b1df4fa7f5d7e45b22c997a7bf302f5280eda153dc5eaa29fb3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb60ac58e733ec888306e13f3e9db32928a7ce508629c75f5cf0fb20d8a554d5(
    value: typing.Optional[typing.Union[AccessPolicyExclude, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe60fa7c5755419369967cbde726378f27ac4606e64e8493efe8052fe568a35(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    attribute_value: typing.Optional[builtins.str] = None,
    identity_provider_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c50aec812e07b0256aba0d0a9f8f6453ab807cab01d3fa86bb60d59e8b55dfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e71f6d0afb17a628668472e9203a3d9a06c55c448a6a82b6b6005eee0f53e4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99df21b87ed808bc75a153b7ccb9d3cee8c52c0b41063652f3140c937a838cc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814ad343fe49b715bd4bdf5e4c480684fab82f7007f2a18f0f957a679880eb7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e33b836e456c82d407806573a77d9cf19268ce3525d009590e6dceb54d908c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d965977cc286886a7b7b23ff48dd646db8ef7215b28567f4c3eb5823f9abbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyExcludeSaml]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823630abb8eb63e0dfcd569630fc85016136c2b310a26ccb093e708bd242c46a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c44f05219745f4aad45ef6c3b553f8a66480cb69efa1c35f5e7567ec57a048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac057ef69a1b1c50e0a223d2957232e562e14141344090bf038223d85ae2f6c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e04055223f996aa08c222e182243f15ab9f3da03447eff98cb0687aceb42283(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c07d6ce963759de25a53e70107bfd1d3bca50de4b5b919eb52e4c074ee7226d(
    value: typing.Optional[typing.Union[AccessPolicyExcludeSaml, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca231b2d68c6ea34a6ec54ebedb99537b6329ce587ebca40a0163e3afed96d5f(
    *,
    any_valid_service_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auth_method: typing.Optional[builtins.str] = None,
    azure: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeAzure, typing.Dict[builtins.str, typing.Any]]]]] = None,
    certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    common_name: typing.Optional[builtins.str] = None,
    device_posture: typing.Optional[typing.Sequence[builtins.str]] = None,
    email: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_domain: typing.Optional[typing.Sequence[builtins.str]] = None,
    everyone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_evaluation: typing.Optional[typing.Union[AccessPolicyIncludeExternalEvaluation, typing.Dict[builtins.str, typing.Any]]] = None,
    geo: typing.Optional[typing.Sequence[builtins.str]] = None,
    github: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeGithub, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group: typing.Optional[typing.Sequence[builtins.str]] = None,
    gsuite: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeGsuite, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_method: typing.Optional[typing.Sequence[builtins.str]] = None,
    okta: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeOkta, typing.Dict[builtins.str, typing.Any]]]]] = None,
    saml: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeSaml, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_token: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3934ff8bb0aa7cf88980c1a57a8d82485763f3fd8cbb39ac068681847a2e5f10(
    *,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_provider_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0aa05167434a2598f4ea65c78a7c0dd801fb9ca0d6c898b15c1f9bba0bb3c1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87e1d4becf1b0dc47a918888de762ae1dbcdca78cd47d2f5696cdf2df66f91e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaeb284d3ead63c5efa163567d04768592ce137a87ab1825ccd62c5d49a49851(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6953032138552c67d6430718d5202fb464ae704c4045075be7cbaaa4d84986e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47629b63031e66530a89d72b6dde7fbdea4a17ac662db9d5c38726861bfd2d8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57eeee0c3bd05ea5e56753b4b6b7a2bd56ef05571f8aea5e58155179bb5f9d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeAzure]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4458ad2a53865fcbfe55b7fd8b21f87ebd5f0ed4ce0cdc49841fd348e567b705(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e5a0068581af2b0f90d73819a72e7cc7504d07954e5ea6d4bb291821053789(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230073dc79f2164d1fcec824288169d8045f524354ec02b061a1a8f99194235f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa46ff367be827f641a1df2cd50e559684f6029fd2a4f89d84a7476599314a2(
    value: typing.Optional[typing.Union[AccessPolicyIncludeAzure, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edde7be87a8ba678fdd789315a28a1b86c6d4e88749e79c466238bcbcbf504e3(
    *,
    evaluate_url: typing.Optional[builtins.str] = None,
    keys_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731143a89fda40e3233b10bbdb626924e921eb6f8fdaea663e77583ecfb22784(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19d25126f7b0c88e2d50e51d3c7818e69cf0ab66030f18b76aa7b93e79e8813(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8123a0071311fe1d701bf0d4e6d2867e0506926fc17328c100029eb02feee468(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18d29491c3aee07592c3a91a5c9384842034c734ad7c0dc0c28c24bc81df1dd(
    value: typing.Optional[AccessPolicyIncludeExternalEvaluation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22198ae31009317a723ca1bbe62f3a31a753413bbdc28aa21c5fdc7ce01052ec(
    *,
    identity_provider_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    teams: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae97386eb42a38fb47476cc2d19a67d6e2457b66ce360ec6a146efaa469b35c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d1ea0cb148000de2dd291bd26e0b8ae8b0781e429d6c836bf402d8921a94c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7768e95f125991501fae9b84ad0f0d4f41c05f05507d808e4cd5778bc5d50d9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257513b30c8c5a4765e63b4333845bd0a9fe6e1c1fd95f3f53e86b975e6aa741(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e88c6c3eee0cbf3e9fbc52b388ed7fc7d933c46b83abf5eb55cd297df64c80c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3790ca2ed238ef071c93aed26db49851979a2fe081b2284c5d82690a6517c71e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGithub]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2340254d2ab2bf6e14f0dbeb03719b37e056a5d58a732600c0d8e714849a54b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5782d4c75671b766db5b047d4983217f50d0c9bae90c9c080c8e851d6f49eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4155c7e51cef781842cadccf16b16ed1041794bf7bb6c50e46d1c0fdb77279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfcbf3a282531ff5d8d79d8117ccf2ed55a7cd2df730244a792e2685f8b2b31a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097d0f38b868e8552d9946231ec29d078cdee42cc88376d0bfe847efe9b13014(
    value: typing.Optional[typing.Union[AccessPolicyIncludeGithub, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dbdfc8a3d6e76921b2182aa3ab1088376de8f4cd24b441df1e6c4f4ee7debb1(
    *,
    email: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_provider_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae80c8abcf0b5f83bc90f38803f9e074f1ca2dab3f0921ae65993b259d779e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ac8fb2c7ebb481186f6da23f3cdb84754849d4358df54d12991a6a38aa51ff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142d479600e26cb5be7393040b1ea518b271a117edbb982a4149c5f4653c70f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca8713cfc321cb97bd47cf2f629b798f0ddc6c715c4359c5467631270365ee0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8e02bf3ed277c570c0e2e0ba92bdf13f9f685ec7d6d0d64eb2596ad455bd58(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2f4f26f425cea945d6b47475ba019adc83789d652806fdcfa498190f2ff561(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeGsuite]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7338f427af8584f2283425807f407a5b9b0e426e0173b66f112e88414c3886f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16a34212c127a45d08dd15dabd9ad78159d8858671ed6ae30dc60e195be20bb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4c30fff648171b7b40a5776725ae6b42277f40180146a5033de95a5826a731(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9998eb01089a94bdb625db2eb187f0a89dabb3d5f1551ed4d73ac243889604d1(
    value: typing.Optional[typing.Union[AccessPolicyIncludeGsuite, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3dd568166a353ef3ec6578d829e40e28ad44672799f6f1504276ac2f921bf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0ac8ca6f26bc2bfc9985db822b66814b41e74aafb4e93060f891e958c58601(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77829cb286e37da020695da89329b151a1d791ee73eddb81f924bcf82895fbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57bacea9b0fede6644e06080c0b9ff298fa2708a2c705d15cbf36685356806d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d06355ba457b6955712179a0759587a7f30027f2fa17da852f8aeea46acafb5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eeeadc0f5788c9a4a0b3eabc0508dd993bfc9f7cb57767b753ba0baa41ad1b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyInclude]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68e736525185a389784f257f6523ad7a1618bdd1c009deabb3c448ffbda116c(
    *,
    identity_provider_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307fe7b8a98e8231bd3b827a0d55a095a96786a0c882390312059528e12f95e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67694ae0ff0607e465ca91efd86c3f73b37e29d2847fccfe064b74384b8bcb9b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d6150e477f74f6e796d9944e46352de34a297a440944f70f4ebdc762080a5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6455150b51501aca494bfc3253f955a48cac67adcafe52ebc3f5552621ea8528(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fe456bfd84ab8480554ae729ac67d75eb0c2e38da968410f047a7f7b0434e0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae149d5791cef25d351587c1a679ed5e3a1ef26e6f0690807fda4a0b53e43f2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeOkta]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984269807a712f265fe7682cfdd7abfaf9596d7e94a9c1fd92827ffdc87aba9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa55bec9af1685b78de506123abb717afd9a196bacc4e34e4d86024e630764b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d1979574ace9ce4852e9e5df4a926924ec982a5789751f5bca6a605f872266(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4018a89c43a2d7dec4d671f861bb4f2e5d0cd25660df1eb32f2c386c226f6627(
    value: typing.Optional[typing.Union[AccessPolicyIncludeOkta, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f772a983e4e7937a9adc8bb112711de542bbab1d734b9e33c979b16f430b722a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6496b428d419ff77386f1e0175493e47fcfec80705366dcc482b1c5cdb3c334f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeAzure, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd050234f83da902debed59b13b15ac75a22a67970d0850c2f62b18c7168c6f9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeGithub, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0756502e2dfb2d6abdec4ef32710e7e3a03a7fa2bceb1d2324faa45ec8ab71b3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeGsuite, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb71f46fa1eb9421affb9a106d5cdbc59b37761760df32b2aa367eec617cbc9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeOkta, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a814ff4185e2e8e611d3e90b40c8391c611ee03db55a4b0caf3d2b3e23330e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyIncludeSaml, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2dba7569072c26c8ead4fc8135bc0b472e1dbf9eec8107fe9e04e5b391e99f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1440a9bb8aa242010dc7ea34223358e8e8fd42a60425fb9d3d2120449a58f792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470d2f6309bb91b1171bd2a86dc0c33c0fb8f255d2554bcbc7dfa465c41a54fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de34861ee30d0c8a269f43753ce5fd8b42d7c192aad5b5cbd1e6ba4a992c5f74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fa838f2a769705159ae5841ee789f1ef4e2bb23419c3827d05e51885c6cb94(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829583fb61afb5cd78b25183f44e4e481889b62cafd2e91653179f560dd9eab0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f316532ccaf3f368324b56ae019d5bbd3995687a22e28cdd398fdfc3aa742884(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443ba7868ff8a75bf9618187481914d9dd69e6e9fce32f6e5660d3d2b1100462(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8b13abbcee4b8c982db96a9d22cb87a48c32d567afeb6a00aba712fc89ff19(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9625eef34773e43a104000cb879237f5d520cc52d3c5bd4369419d81f4887f66(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4994773d565590a64c8cb3b4b840c975d0327d23d55c421a1abaafee43233daf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71aac2f955b301fcd7622c5eb0fc16b48a97c8d2809f25a55ac0c49e34dc2f42(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5666b1eb0c33252c5769221e832978e6183535000d4aa759795201d25fe40f4b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00274e393471eadab07e528bcf3332030c55d0d30890a532e70f4b15580eaa0b(
    value: typing.Optional[typing.Union[AccessPolicyInclude, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b50446c5aebaffb7b0813471069dd3e11fa4a2739f73ef076a44cd8b2491f5(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    attribute_value: typing.Optional[builtins.str] = None,
    identity_provider_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91899907563f0fb244b9323b68bcdbffe2a41626e07e5e9d5e951429318ed4a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77dcd3ddf58736eaf632178fa12a36e3d66325f13c349e2fa5735d63e8cf0e89(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51a0ed8b30eac5d2817647e8edac79f5705c372a09aa66f232618b6dfe9d000(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3c42ec8c5912108899ea01c1152ee1e2ea352d1eed0c9fa07b04cacb92d1b1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360d718fb5fe8ffdd870682fcba648e1939da510f2a9166589e3d1abfdd68be4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff8ea4f54e573dade9810aa8b68973829d6add29f8eb770c4f9fcc477b24773(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyIncludeSaml]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebab05767071a22c21f41eeca850b650e1f127f6c60f1fdf76a8de8370edd212(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c175f26e593dfd61f1a7cac525c91e23f17c4ae6ef1f78d71c7aefcfb9466e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9687376d518cb81c07c65645974dc58d892422a47b325a561c855dca05ea13f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48aa0d7bc13b947da5df8bfe79b6f0ed0d94da5d83a31bf892767fcb506b7cc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fadae813314d360f5c9f04d80e0da414906dccba5ed891b873cfeb9cf18b11e(
    value: typing.Optional[typing.Union[AccessPolicyIncludeSaml, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a1d8a8011ef7f6a05eeb4b54966d10e4df2db7c9dffd0d69a7ce9d424599d3(
    *,
    any_valid_service_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auth_method: typing.Optional[builtins.str] = None,
    azure: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireAzure, typing.Dict[builtins.str, typing.Any]]]]] = None,
    certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    common_name: typing.Optional[builtins.str] = None,
    device_posture: typing.Optional[typing.Sequence[builtins.str]] = None,
    email: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_domain: typing.Optional[typing.Sequence[builtins.str]] = None,
    everyone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_evaluation: typing.Optional[typing.Union[AccessPolicyRequireExternalEvaluation, typing.Dict[builtins.str, typing.Any]]] = None,
    geo: typing.Optional[typing.Sequence[builtins.str]] = None,
    github: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireGithub, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group: typing.Optional[typing.Sequence[builtins.str]] = None,
    gsuite: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireGsuite, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_method: typing.Optional[typing.Sequence[builtins.str]] = None,
    okta: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireOkta, typing.Dict[builtins.str, typing.Any]]]]] = None,
    saml: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireSaml, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_token: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af178787ae750d4083934fc2b6feca8ea8351e20b9f21fa9c1d48ee08516737a(
    *,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_provider_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70560147f51a74668b36e1644beec217be38e42cf70cdd6c1e96dfc6326a652(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f63ee78c1c1c4a4045903e2f29d44bf39af3bcc81065e3aa4c8c77997970df9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d98c1980cb5d78119990af2dcdead5a598a3a1b9f3583cdbb8f923dac05de4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee2749d85b07683a1605f1b4fec8d50a5d55b4a83889f82574e60474417264a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9906f6e6613e95b6e1205df02a4cd54103862c2c46274165234e6d34bbf97c87(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d7b84ffde2b1f18400fe67ea4328163dc98a557661dbf2adde1e7db365cc32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireAzure]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb8cd0309e3f0f3ef131080afc69b34bd62661de72effc00d333099ac700569(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd0af73be81674640f8cdbf46f0994cccc2edb63f8fca984c55f6c5ad225623(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417af373e0d1a759816f6d09cd4f4efe47cdaa45ddaaf5999afc91241ed2150d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f67c57c52f4b9ef20d4f3318ed26ca081bba3b534f6017100d59e80f69f2ff(
    value: typing.Optional[typing.Union[AccessPolicyRequireAzure, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5189490fe5cb30537b55b8815efaeb2b5ab3d87b14b64c525242f5f4cc56d30b(
    *,
    evaluate_url: typing.Optional[builtins.str] = None,
    keys_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf2f5a5aa1d7538d34565bdd313b3006879c3e0a9924459606e6c19fbd4391e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a304dbff6270b92ebf6564e030f55e621fc5a3de2e822670f0435ec5f52c5577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2168810e2ca23e1c6da552ff6cbadcab901aad5406e425fdb59b1c504ee1c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8223a1b297cc20b8ad5d102df3e7c22bf60841612c51d47ca4f7619bea3452(
    value: typing.Optional[AccessPolicyRequireExternalEvaluation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d1abeff207dfce282f94077f48ad839fc26b80bea39674a7efd6da13903f75(
    *,
    identity_provider_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    teams: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a98194246b7ee8add3040ff40204514fea2006a9e61a38409b7b020c18c5c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865230b1a057fef6cf330af36de81b319bc76b2dbc468549703166002fcdb2a4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6feea9da9f33889c5555adc47093e25bea5f3d0e530ccf6938ae47a751ed5dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab62fb21d8316ca57b79c5a0e8be5ce0dde1991d84f5feccf39b097e0fceeec0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6c34579ec3f9a650fe652c3ce17eb837bf51cb5b0c21691a885ce82a3c5ff0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906ee90812e9c2bd3184f015905efbabefbba6947080bd3740762e1646ba8206(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGithub]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15bb1f322ae8b6266794da352f0e0868065f267b39bc08c747dd3319a800c82c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1393d71aeac5dad6fdf9fde1313936107183aaf993c1e274a81fdc3ff609aa17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed4fcc1a2e47da7111606a7b2f951f5b81522dd1c9267a665f907bac3b6db17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c8996c6836466e55d5887a0229d102bfe03915d018b0a8087aa1aeaf7658c4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be7b7c0b21b8b6b0ccab72827fd6d3a41c77ef92a9c869285d10f8f4b077bdc(
    value: typing.Optional[typing.Union[AccessPolicyRequireGithub, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b88b05b5fc64d4904f6366af5cefa415986a2eed00b671871db6cdeeff591b(
    *,
    email: typing.Optional[typing.Sequence[builtins.str]] = None,
    identity_provider_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108f18ec63199cadcff87c25bf051be5ea6c0293b1a6832a49121eadaf857f85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eadf330ebd5af6c54cc5b4ad98a8f5a533be753187fb1195a87f372edebb0540(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54775d6bd3dfc9d0dc7e068146fd3eafe9a06dc988cb13fa2b22a5fad21614fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed48bc1bd44aab28f8cc0813c5330b5a6e6d40934176f13bf061aeb3116c9ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b781ad024b300dcff43df0b286f3d575751942023004cf475ed3abcc58b318(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dac2eeeb05f5aae30f45e9ed278dd084b949f9b5a19a5fb4423f1018c84ac9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireGsuite]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c3a53a410c1b1fefca5844d20f817178eaed4f8a640a03f43dc62a6355cca7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a5767aec6c9bc12edbafba9194feaa94484d8444d7a188ad53800a289a05f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163ca3cf47337fcf8a889cb8c6779869378c65adae7632a8cec4244704587d1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c58bad664d508dd9c0a65dcc8aa31625ccd9c2ff51845b3997186025c8abce(
    value: typing.Optional[typing.Union[AccessPolicyRequireGsuite, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0b2e8cbf51d1d3fdb2db0ac17f39b49505a3d01b99e585f533610dfa086e36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bda79d7b5243c45c00a143acd0ba9a7a4f6e785250844dd187e5643d85ef682(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f910cb8d7cb2daf1b9aa2aee0c0eb4b7255c69d9cd2ba1b983f7b226fe8213ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042c3e6eb5d4a3c85115066dee4a67adcb75a2f2ebdec4c3df473b8fd6820f41(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb5105feea0108b461396a8dc57b9f86f1ec4bbbdb7ee7c9a04640478486a2d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421136bc24cd864892aaf19226bfbee583d86327c846f384828a9e9d01bd4063(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequire]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf465a602e6c58158e9fe7c3b4bcaffd4b9d94f1477e4e4a078ba34abf3b804(
    *,
    identity_provider_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3ee18caed3713980c595f788afd78a3cadf5dcfe843bc2ad9096e66bc1b8c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4f807afadff897136c522d75640bab58c4df01bde9dd0dd1f9b5a1f9299208(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ea39277718b4dd2d401d97ce263721fce79252b6856bf39a625373ed031086(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4823230d4aa26a4ae917d1c79215451c8331653dcf5c0be80501d02827e54eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d4c8e9ff611f44db7243e89034aa7ab6b9be7d07d7aee0a485e2b6b649263c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d00d9b7f40a2df9b019e54445940ca6f44ea5792f46d8da6c019ba5af7dc31(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireOkta]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6f3aa9354625aa7a0d448b1b80c6dde175aacb4acf435f02138e6f518c1f6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d040244d2119974456529689ecbb19035601092b3c78a701b618efb7dc35e960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f78d1007ba4822835befa566dcb7d57654f772c1d0b37f788b1f988e2ae0799(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504e5db5de400b37e2218cfb2fe20778dea169a39e64ffd8a8cb9a09c4a83e65(
    value: typing.Optional[typing.Union[AccessPolicyRequireOkta, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a342121f2f9fed5f9b13c6903963a90ee4b7f7e9de6021db62e4a5f7e8d847(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8542a2a4e99f4ff12dd10abc36032366e06765373025a2cebb848841fea555d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireAzure, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bac3e7d051e0cde3805a0a4d83fd9694331fa26c840e633042a7edaaf6adb5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireGithub, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec75de26e60fddd8e0bd8ab25c7a1c1d263f80c58912640846fef2983b6e13a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireGsuite, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8f231bb1c77c70162315b4a2c6daa183cb0248794c090561513d75a3c02569(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireOkta, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b01ad3abe5cee7d1828b48922131dea7003cdc7adc3d906c4b3635f2dc89d9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessPolicyRequireSaml, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f134f242e91265ab53a0d9fa168305f5f65ad1b56bd2d0986c4247615cb090d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5e7aceae03a9abf9f0919c7cfae51a256058e1b5a51a949b25721f362d7482(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88bc0df710eb7d22233973da2cd941851ca68f50ace12a19e7c7ad2068e0093(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8da47610fc0c40817ce66448079e3f1da84357e71ff337d018870cf4e847d26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5878f820b9ab9f244dbc276cc192c3471bf6f5381fe109c3a739f665bf9c38(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282e805dbc198ed2343700ef5a746ee55677a62676c5c97caf724a9244ed5c91(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf53c62f9f09ec4a67a47d7444ff461e5675ff3f1b8fa6f660935979c1747e2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783d966d008fbc9122b9b37facf4522e20b1d7d85686c99a663bfbe4a0f8f046(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1766ef1c35afdd1db1ea3b7df612bbf17bfdcc0b99136617c34eb02225aa742a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befaa9a9dfb25953dee57b7a99c5fbf84102d901fa6389ca07669c0cd0852d96(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07666527c6d7d87439ae08602fa311310906ad050036d9e8ee028452711ca57(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532515cf2da1cf2437a48ef89f72bed399374f3b5e2ee406a88919636a1a9181(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76385b23d67f8a90197a11040605e80e47c9c90afb94d0e48cead1f3ee0ea49d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0564fdb2a990034ed0c8224f0edee9da190beeecf025963235a32f08f6f899(
    value: typing.Optional[typing.Union[AccessPolicyRequire, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cc628912e40622419e8d47faba59f6fa066c8481498ca22c467aeacfa0dd8f(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    attribute_value: typing.Optional[builtins.str] = None,
    identity_provider_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44afc539a0b32810cab8bba8b55334a290c6a72ecb344d31d0968809423eef3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82446f270d73539b7691bb2272597e8438e17b87c99339ea23b5d164de3ee6a2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2909bc32bf0ef46e1c0eb39f6ef69e025a52f472c4dd1380c35583aa3072196(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8a321ddbc6f614205c5862d9984d6881e27b6f8c0786a5f019be84fefb49b1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d160ab14d9d80761db9fb053a9f633904da0738981e189c95efc755e3eadc9a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f79598985429d880805af193c806eb4af55cb246da5e54f3e4370e843d014f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessPolicyRequireSaml]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d682643cb5ceca7009560ac9671178ec350297fe6ddd2342df6555456a2dde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968ac736e6cb9bd06a7200dcb1599adda51a9cc6a079f9fc0d1ce5afccbfcd2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a6d69b9f7179e0b0e20f8a276267b20b8c886def52ffdcc19abd5a3795be7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0005865c9580411a34c1f329d6f79ecdf1cd83226d20414078f3db5aef8f9bab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c9426558d01a1155edc24659a6e2661f6cf73f8654e85d1eca3722836c6d37(
    value: typing.Optional[typing.Union[AccessPolicyRequireSaml, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
