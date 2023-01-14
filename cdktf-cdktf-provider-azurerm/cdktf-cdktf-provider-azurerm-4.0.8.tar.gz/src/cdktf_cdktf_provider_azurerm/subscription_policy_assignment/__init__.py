'''
# `azurerm_subscription_policy_assignment`

Refer to the Terraform Registory for docs: [`azurerm_subscription_policy_assignment`](https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment).
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


class SubscriptionPolicyAssignment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.subscriptionPolicyAssignment.SubscriptionPolicyAssignment",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment azurerm_subscription_policy_assignment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        policy_definition_id: builtins.str,
        subscription_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["SubscriptionPolicyAssignmentIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[builtins.str] = None,
        non_compliance_message: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SubscriptionPolicyAssignmentNonComplianceMessage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        not_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SubscriptionPolicyAssignmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment azurerm_subscription_policy_assignment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#name SubscriptionPolicyAssignment#name}.
        :param policy_definition_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#policy_definition_id SubscriptionPolicyAssignment#policy_definition_id}.
        :param subscription_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#subscription_id SubscriptionPolicyAssignment#subscription_id}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#description SubscriptionPolicyAssignment#description}.
        :param display_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#display_name SubscriptionPolicyAssignment#display_name}.
        :param enforce: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#enforce SubscriptionPolicyAssignment#enforce}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#id SubscriptionPolicyAssignment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#identity SubscriptionPolicyAssignment#identity}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#location SubscriptionPolicyAssignment#location}.
        :param metadata: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#metadata SubscriptionPolicyAssignment#metadata}.
        :param non_compliance_message: non_compliance_message block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#non_compliance_message SubscriptionPolicyAssignment#non_compliance_message}
        :param not_scopes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#not_scopes SubscriptionPolicyAssignment#not_scopes}.
        :param parameters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#parameters SubscriptionPolicyAssignment#parameters}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#timeouts SubscriptionPolicyAssignment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1a0d65a445d1ceabc4ff85bdbd2da5b71d8d8716f71fc8d0da279b902de078)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SubscriptionPolicyAssignmentConfig(
            name=name,
            policy_definition_id=policy_definition_id,
            subscription_id=subscription_id,
            description=description,
            display_name=display_name,
            enforce=enforce,
            id=id,
            identity=identity,
            location=location,
            metadata=metadata,
            non_compliance_message=non_compliance_message,
            not_scopes=not_scopes,
            parameters=parameters,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#type SubscriptionPolicyAssignment#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#identity_ids SubscriptionPolicyAssignment#identity_ids}.
        '''
        value = SubscriptionPolicyAssignmentIdentity(
            type=type, identity_ids=identity_ids
        )

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putNonComplianceMessage")
    def put_non_compliance_message(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SubscriptionPolicyAssignmentNonComplianceMessage", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d9a01810ee51364e2a8602142113567e857884e20968504ef5521282a94e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNonComplianceMessage", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#create SubscriptionPolicyAssignment#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#delete SubscriptionPolicyAssignment#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#read SubscriptionPolicyAssignment#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#update SubscriptionPolicyAssignment#update}.
        '''
        value = SubscriptionPolicyAssignmentTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetEnforce")
    def reset_enforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforce", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetNonComplianceMessage")
    def reset_non_compliance_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonComplianceMessage", []))

    @jsii.member(jsii_name="resetNotScopes")
    def reset_not_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotScopes", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "SubscriptionPolicyAssignmentIdentityOutputReference":
        return typing.cast("SubscriptionPolicyAssignmentIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="nonComplianceMessage")
    def non_compliance_message(
        self,
    ) -> "SubscriptionPolicyAssignmentNonComplianceMessageList":
        return typing.cast("SubscriptionPolicyAssignmentNonComplianceMessageList", jsii.get(self, "nonComplianceMessage"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SubscriptionPolicyAssignmentTimeoutsOutputReference":
        return typing.cast("SubscriptionPolicyAssignmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["SubscriptionPolicyAssignmentIdentity"]:
        return typing.cast(typing.Optional["SubscriptionPolicyAssignmentIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nonComplianceMessageInput")
    def non_compliance_message_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SubscriptionPolicyAssignmentNonComplianceMessage"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SubscriptionPolicyAssignmentNonComplianceMessage"]]], jsii.get(self, "nonComplianceMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="notScopesInput")
    def not_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDefinitionIdInput")
    def policy_definition_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDefinitionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionIdInput")
    def subscription_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscriptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["SubscriptionPolicyAssignmentTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["SubscriptionPolicyAssignmentTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d88800150abf43635fa17a4e8904ec3a52ec7bbfa9f5de7926e9af765057bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000cbdf4b17deceddd4e5b8f632104236ae2c196a790912aa5f9b97e53c0e73e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b1c1682bdf131c9c34e10417f11944c621b2eb860fca1a9308d55e0116f5091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3029c49e9d7b52085e9480c9b33ff3d22fea64bc3103439e7901689bc9c5878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055bc9c3e00925dce835feee985e27dbe1f3eb523477bb0871bf3e0967837dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085067b790a0aab04d5bb95b6a4653b395a1d1d070900783f8a2439f74072bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0435633c86dbd0a298e233bf9fe6c95ce1399c2b6e67862a31ce17618d98405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="notScopes")
    def not_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notScopes"))

    @not_scopes.setter
    def not_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b70a6f2a17efaa8ed76fc20640a4e492fecccc08231c68055e43455e0fda62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notScopes", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46c2ded16857a6a729a0500aa113b4f4f3f09219f25b5420d0dc780ae37cb68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="policyDefinitionId")
    def policy_definition_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDefinitionId"))

    @policy_definition_id.setter
    def policy_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9576e331944d274ea524054ddf580957e5a148ad9a8c6f7b182ef7dc61f9a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDefinitionId", value)

    @builtins.property
    @jsii.member(jsii_name="subscriptionId")
    def subscription_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionId"))

    @subscription_id.setter
    def subscription_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9aa2638944c38e796b8c6528e8dcc6f1f42835dfbb92d9b13fd939caff2513f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.subscriptionPolicyAssignment.SubscriptionPolicyAssignmentConfig",
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
        "policy_definition_id": "policyDefinitionId",
        "subscription_id": "subscriptionId",
        "description": "description",
        "display_name": "displayName",
        "enforce": "enforce",
        "id": "id",
        "identity": "identity",
        "location": "location",
        "metadata": "metadata",
        "non_compliance_message": "nonComplianceMessage",
        "not_scopes": "notScopes",
        "parameters": "parameters",
        "timeouts": "timeouts",
    },
)
class SubscriptionPolicyAssignmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        policy_definition_id: builtins.str,
        subscription_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["SubscriptionPolicyAssignmentIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        location: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[builtins.str] = None,
        non_compliance_message: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SubscriptionPolicyAssignmentNonComplianceMessage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        not_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SubscriptionPolicyAssignmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#name SubscriptionPolicyAssignment#name}.
        :param policy_definition_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#policy_definition_id SubscriptionPolicyAssignment#policy_definition_id}.
        :param subscription_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#subscription_id SubscriptionPolicyAssignment#subscription_id}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#description SubscriptionPolicyAssignment#description}.
        :param display_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#display_name SubscriptionPolicyAssignment#display_name}.
        :param enforce: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#enforce SubscriptionPolicyAssignment#enforce}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#id SubscriptionPolicyAssignment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#identity SubscriptionPolicyAssignment#identity}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#location SubscriptionPolicyAssignment#location}.
        :param metadata: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#metadata SubscriptionPolicyAssignment#metadata}.
        :param non_compliance_message: non_compliance_message block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#non_compliance_message SubscriptionPolicyAssignment#non_compliance_message}
        :param not_scopes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#not_scopes SubscriptionPolicyAssignment#not_scopes}.
        :param parameters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#parameters SubscriptionPolicyAssignment#parameters}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#timeouts SubscriptionPolicyAssignment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity, dict):
            identity = SubscriptionPolicyAssignmentIdentity(**identity)
        if isinstance(timeouts, dict):
            timeouts = SubscriptionPolicyAssignmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed20bda19e94b95b7a80c5447ffad7457a09711c63db9bfdc6d391a45ccdd3c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_definition_id", value=policy_definition_id, expected_type=type_hints["policy_definition_id"])
            check_type(argname="argument subscription_id", value=subscription_id, expected_type=type_hints["subscription_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument non_compliance_message", value=non_compliance_message, expected_type=type_hints["non_compliance_message"])
            check_type(argname="argument not_scopes", value=not_scopes, expected_type=type_hints["not_scopes"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "policy_definition_id": policy_definition_id,
            "subscription_id": subscription_id,
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
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if enforce is not None:
            self._values["enforce"] = enforce
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if location is not None:
            self._values["location"] = location
        if metadata is not None:
            self._values["metadata"] = metadata
        if non_compliance_message is not None:
            self._values["non_compliance_message"] = non_compliance_message
        if not_scopes is not None:
            self._values["not_scopes"] = not_scopes
        if parameters is not None:
            self._values["parameters"] = parameters
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#name SubscriptionPolicyAssignment#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_definition_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#policy_definition_id SubscriptionPolicyAssignment#policy_definition_id}.'''
        result = self._values.get("policy_definition_id")
        assert result is not None, "Required property 'policy_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscription_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#subscription_id SubscriptionPolicyAssignment#subscription_id}.'''
        result = self._values.get("subscription_id")
        assert result is not None, "Required property 'subscription_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#description SubscriptionPolicyAssignment#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#display_name SubscriptionPolicyAssignment#display_name}.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#enforce SubscriptionPolicyAssignment#enforce}.'''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#id SubscriptionPolicyAssignment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["SubscriptionPolicyAssignmentIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#identity SubscriptionPolicyAssignment#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["SubscriptionPolicyAssignmentIdentity"], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#location SubscriptionPolicyAssignment#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#metadata SubscriptionPolicyAssignment#metadata}.'''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def non_compliance_message(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SubscriptionPolicyAssignmentNonComplianceMessage"]]]:
        '''non_compliance_message block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#non_compliance_message SubscriptionPolicyAssignment#non_compliance_message}
        '''
        result = self._values.get("non_compliance_message")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SubscriptionPolicyAssignmentNonComplianceMessage"]]], result)

    @builtins.property
    def not_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#not_scopes SubscriptionPolicyAssignment#not_scopes}.'''
        result = self._values.get("not_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#parameters SubscriptionPolicyAssignment#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SubscriptionPolicyAssignmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#timeouts SubscriptionPolicyAssignment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SubscriptionPolicyAssignmentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionPolicyAssignmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.subscriptionPolicyAssignment.SubscriptionPolicyAssignmentIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class SubscriptionPolicyAssignmentIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#type SubscriptionPolicyAssignment#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#identity_ids SubscriptionPolicyAssignment#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710373d281b09142272001294c5a5445bd0607dd341b55070f1e1175afcac36a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#type SubscriptionPolicyAssignment#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#identity_ids SubscriptionPolicyAssignment#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionPolicyAssignmentIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SubscriptionPolicyAssignmentIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.subscriptionPolicyAssignment.SubscriptionPolicyAssignmentIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f5338f6eeb01c615bdeafb8f3f3e7e3ed4dd456335e72d6864b93f5c125fca4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c197bc8b61d418d9da37dcb5c200aaec18714cc8796ad3081369f9a1578ad4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7f8bb5378713e9da1f9593da8a28c0002f4fd4b4ce1e94bc35ea2a66f9191e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SubscriptionPolicyAssignmentIdentity]:
        return typing.cast(typing.Optional[SubscriptionPolicyAssignmentIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SubscriptionPolicyAssignmentIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a062a7fa835f9ff8a08e27faebbbf900a8dc3ed214072cde1d858e4f87f0130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.subscriptionPolicyAssignment.SubscriptionPolicyAssignmentNonComplianceMessage",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "policy_definition_reference_id": "policyDefinitionReferenceId",
    },
)
class SubscriptionPolicyAssignmentNonComplianceMessage:
    def __init__(
        self,
        *,
        content: builtins.str,
        policy_definition_reference_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#content SubscriptionPolicyAssignment#content}.
        :param policy_definition_reference_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#policy_definition_reference_id SubscriptionPolicyAssignment#policy_definition_reference_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b837f3388b42d1b365dd2943509a01fe4475a428f5983ba300a3d55d3b8641d8)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument policy_definition_reference_id", value=policy_definition_reference_id, expected_type=type_hints["policy_definition_reference_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }
        if policy_definition_reference_id is not None:
            self._values["policy_definition_reference_id"] = policy_definition_reference_id

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#content SubscriptionPolicyAssignment#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_definition_reference_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#policy_definition_reference_id SubscriptionPolicyAssignment#policy_definition_reference_id}.'''
        result = self._values.get("policy_definition_reference_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionPolicyAssignmentNonComplianceMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SubscriptionPolicyAssignmentNonComplianceMessageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.subscriptionPolicyAssignment.SubscriptionPolicyAssignmentNonComplianceMessageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78fc56ed2b2b64e1030794368a8cf74703af0a03fe0b03b4b09af30151931955)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SubscriptionPolicyAssignmentNonComplianceMessageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a09b87d04442fc053e5d8b2711df7704998bef5e4228d3dfb26ad83efc5370c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SubscriptionPolicyAssignmentNonComplianceMessageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22da8181c74e015da791fb1f3cbd76cd98bddb66f0a0a5ab88a731b1c368ae08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d77997b4c81b735b23e7601c6b8b4397440f7fb170976ba455c30c90c51659f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66eadee8d51f140d61994bca24574f6206f5f6b06148bf935dea799a6d5c9f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SubscriptionPolicyAssignmentNonComplianceMessage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SubscriptionPolicyAssignmentNonComplianceMessage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SubscriptionPolicyAssignmentNonComplianceMessage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f1dd525c1cd2fbe5313339ff1e356c684727af3cd14218605c5cefaf5bf610a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SubscriptionPolicyAssignmentNonComplianceMessageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.subscriptionPolicyAssignment.SubscriptionPolicyAssignmentNonComplianceMessageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce327faacfb85aca4ec99f339a71850bc8e10a518ab5f8b2a210c94c3d9bf326)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPolicyDefinitionReferenceId")
    def reset_policy_definition_reference_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyDefinitionReferenceId", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDefinitionReferenceIdInput")
    def policy_definition_reference_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDefinitionReferenceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42a2a1c18525ca4dab84b460634dc0610c74e3557092ae23816c21c80638394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="policyDefinitionReferenceId")
    def policy_definition_reference_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDefinitionReferenceId"))

    @policy_definition_reference_id.setter
    def policy_definition_reference_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f266e0d48f978c0eb4ba95f70020356ee45069db3ae2e6aeb82756c652384e45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDefinitionReferenceId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SubscriptionPolicyAssignmentNonComplianceMessage, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SubscriptionPolicyAssignmentNonComplianceMessage, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SubscriptionPolicyAssignmentNonComplianceMessage, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9a29e763a246575e3914e90df1684aee60202516b7b79a6d7fd035307da528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.subscriptionPolicyAssignment.SubscriptionPolicyAssignmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SubscriptionPolicyAssignmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#create SubscriptionPolicyAssignment#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#delete SubscriptionPolicyAssignment#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#read SubscriptionPolicyAssignment#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#update SubscriptionPolicyAssignment#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df23ee0f4cc21176ad10a521829ddf5770a671e4f8f811898b973a069d5abd1)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#create SubscriptionPolicyAssignment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#delete SubscriptionPolicyAssignment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#read SubscriptionPolicyAssignment#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/subscription_policy_assignment#update SubscriptionPolicyAssignment#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionPolicyAssignmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SubscriptionPolicyAssignmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.subscriptionPolicyAssignment.SubscriptionPolicyAssignmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a637d8bd32747191de116e1e6e53dbc96a5f1ee5be23acbc530b3f480b8d9bd3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__89b07a74ff4d20aad310ea97b24d79b37236204f990ea73381f9fb67e909218b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07b7b20585a535b2aa38b2273795dea68bb5c5c0333c206b209f3ee7a426f5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3c5d8d360286781585add8231ab081cda9c57850854bd870ab7350c2886f2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b9f91b814ef40df83592987ac0523a5781341d70ccd96d716f4e3f570a8064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SubscriptionPolicyAssignmentTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SubscriptionPolicyAssignmentTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SubscriptionPolicyAssignmentTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d8b99c44a7b0eb9da39b5d5c452680781389640099ff5f33cde91632e77bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SubscriptionPolicyAssignment",
    "SubscriptionPolicyAssignmentConfig",
    "SubscriptionPolicyAssignmentIdentity",
    "SubscriptionPolicyAssignmentIdentityOutputReference",
    "SubscriptionPolicyAssignmentNonComplianceMessage",
    "SubscriptionPolicyAssignmentNonComplianceMessageList",
    "SubscriptionPolicyAssignmentNonComplianceMessageOutputReference",
    "SubscriptionPolicyAssignmentTimeouts",
    "SubscriptionPolicyAssignmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5a1a0d65a445d1ceabc4ff85bdbd2da5b71d8d8716f71fc8d0da279b902de078(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    policy_definition_id: builtins.str,
    subscription_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[SubscriptionPolicyAssignmentIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
    non_compliance_message: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SubscriptionPolicyAssignmentNonComplianceMessage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    not_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SubscriptionPolicyAssignmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__85d9a01810ee51364e2a8602142113567e857884e20968504ef5521282a94e12(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SubscriptionPolicyAssignmentNonComplianceMessage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d88800150abf43635fa17a4e8904ec3a52ec7bbfa9f5de7926e9af765057bf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000cbdf4b17deceddd4e5b8f632104236ae2c196a790912aa5f9b97e53c0e73e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b1c1682bdf131c9c34e10417f11944c621b2eb860fca1a9308d55e0116f5091(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3029c49e9d7b52085e9480c9b33ff3d22fea64bc3103439e7901689bc9c5878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055bc9c3e00925dce835feee985e27dbe1f3eb523477bb0871bf3e0967837dbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085067b790a0aab04d5bb95b6a4653b395a1d1d070900783f8a2439f74072bb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0435633c86dbd0a298e233bf9fe6c95ce1399c2b6e67862a31ce17618d98405(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b70a6f2a17efaa8ed76fc20640a4e492fecccc08231c68055e43455e0fda62(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46c2ded16857a6a729a0500aa113b4f4f3f09219f25b5420d0dc780ae37cb68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9576e331944d274ea524054ddf580957e5a148ad9a8c6f7b182ef7dc61f9a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9aa2638944c38e796b8c6528e8dcc6f1f42835dfbb92d9b13fd939caff2513f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed20bda19e94b95b7a80c5447ffad7457a09711c63db9bfdc6d391a45ccdd3c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    policy_definition_id: builtins.str,
    subscription_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[SubscriptionPolicyAssignmentIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    location: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[builtins.str] = None,
    non_compliance_message: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SubscriptionPolicyAssignmentNonComplianceMessage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    not_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SubscriptionPolicyAssignmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710373d281b09142272001294c5a5445bd0607dd341b55070f1e1175afcac36a(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5338f6eeb01c615bdeafb8f3f3e7e3ed4dd456335e72d6864b93f5c125fca4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c197bc8b61d418d9da37dcb5c200aaec18714cc8796ad3081369f9a1578ad4b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7f8bb5378713e9da1f9593da8a28c0002f4fd4b4ce1e94bc35ea2a66f9191e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a062a7fa835f9ff8a08e27faebbbf900a8dc3ed214072cde1d858e4f87f0130(
    value: typing.Optional[SubscriptionPolicyAssignmentIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b837f3388b42d1b365dd2943509a01fe4475a428f5983ba300a3d55d3b8641d8(
    *,
    content: builtins.str,
    policy_definition_reference_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78fc56ed2b2b64e1030794368a8cf74703af0a03fe0b03b4b09af30151931955(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a09b87d04442fc053e5d8b2711df7704998bef5e4228d3dfb26ad83efc5370c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22da8181c74e015da791fb1f3cbd76cd98bddb66f0a0a5ab88a731b1c368ae08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d77997b4c81b735b23e7601c6b8b4397440f7fb170976ba455c30c90c51659f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66eadee8d51f140d61994bca24574f6206f5f6b06148bf935dea799a6d5c9f14(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f1dd525c1cd2fbe5313339ff1e356c684727af3cd14218605c5cefaf5bf610a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SubscriptionPolicyAssignmentNonComplianceMessage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce327faacfb85aca4ec99f339a71850bc8e10a518ab5f8b2a210c94c3d9bf326(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42a2a1c18525ca4dab84b460634dc0610c74e3557092ae23816c21c80638394(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f266e0d48f978c0eb4ba95f70020356ee45069db3ae2e6aeb82756c652384e45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9a29e763a246575e3914e90df1684aee60202516b7b79a6d7fd035307da528(
    value: typing.Optional[typing.Union[SubscriptionPolicyAssignmentNonComplianceMessage, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df23ee0f4cc21176ad10a521829ddf5770a671e4f8f811898b973a069d5abd1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a637d8bd32747191de116e1e6e53dbc96a5f1ee5be23acbc530b3f480b8d9bd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b07a74ff4d20aad310ea97b24d79b37236204f990ea73381f9fb67e909218b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07b7b20585a535b2aa38b2273795dea68bb5c5c0333c206b209f3ee7a426f5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3c5d8d360286781585add8231ab081cda9c57850854bd870ab7350c2886f2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b9f91b814ef40df83592987ac0523a5781341d70ccd96d716f4e3f570a8064(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d8b99c44a7b0eb9da39b5d5c452680781389640099ff5f33cde91632e77bee(
    value: typing.Optional[typing.Union[SubscriptionPolicyAssignmentTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
