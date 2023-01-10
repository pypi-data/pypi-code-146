'''
# `data_aws_networkmanager_core_network_policy_document`

Refer to the Terraform Registory for docs: [`data_aws_networkmanager_core_network_policy_document`](https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document).
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


class DataAwsNetworkmanagerCoreNetworkPolicyDocument(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocument",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document aws_networkmanager_core_network_policy_document}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        core_network_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        segments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments", typing.Dict[builtins.str, typing.Any]]]],
        attachment_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        segment_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document aws_networkmanager_core_network_policy_document} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param core_network_configuration: core_network_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#core_network_configuration DataAwsNetworkmanagerCoreNetworkPolicyDocument#core_network_configuration}
        :param segments: segments block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#segments DataAwsNetworkmanagerCoreNetworkPolicyDocument#segments}
        :param attachment_policies: attachment_policies block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#attachment_policies DataAwsNetworkmanagerCoreNetworkPolicyDocument#attachment_policies}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#id DataAwsNetworkmanagerCoreNetworkPolicyDocument#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param segment_actions: segment_actions block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#segment_actions DataAwsNetworkmanagerCoreNetworkPolicyDocument#segment_actions}
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#version DataAwsNetworkmanagerCoreNetworkPolicyDocument#version}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df29d47d6dde10f511d59a019b9ac71d75d61b482857becefd3c241072f214e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataAwsNetworkmanagerCoreNetworkPolicyDocumentConfig(
            core_network_configuration=core_network_configuration,
            segments=segments,
            attachment_policies=attachment_policies,
            id=id,
            segment_actions=segment_actions,
            version=version,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAttachmentPolicies")
    def put_attachment_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcad7ccfe4b6a6b0f1c62dc050a14d799f74aead5d48ae046c0892a1d814ed88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAttachmentPolicies", [value]))

    @jsii.member(jsii_name="putCoreNetworkConfiguration")
    def put_core_network_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176fd6b2e8c19ce618cb1f5d88081b062146b5342b66afd2879a9a0cb1ca5edd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCoreNetworkConfiguration", [value]))

    @jsii.member(jsii_name="putSegmentActions")
    def put_segment_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b99a41ae4c887c16a2e46d0581908a9091350d9a0d76a484bead50dff2e32c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSegmentActions", [value]))

    @jsii.member(jsii_name="putSegments")
    def put_segments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a9de918a77f9a83aef8c1f9ac0a5a247bf3254332bfcbafce14aa67f18e091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSegments", [value]))

    @jsii.member(jsii_name="resetAttachmentPolicies")
    def reset_attachment_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttachmentPolicies", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSegmentActions")
    def reset_segment_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSegmentActions", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="attachmentPolicies")
    def attachment_policies(
        self,
    ) -> "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesList":
        return typing.cast("DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesList", jsii.get(self, "attachmentPolicies"))

    @builtins.property
    @jsii.member(jsii_name="coreNetworkConfiguration")
    def core_network_configuration(
        self,
    ) -> "DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationList":
        return typing.cast("DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationList", jsii.get(self, "coreNetworkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="segmentActions")
    def segment_actions(
        self,
    ) -> "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActionsList":
        return typing.cast("DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActionsList", jsii.get(self, "segmentActions"))

    @builtins.property
    @jsii.member(jsii_name="segments")
    def segments(self) -> "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentsList":
        return typing.cast("DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentsList", jsii.get(self, "segments"))

    @builtins.property
    @jsii.member(jsii_name="attachmentPoliciesInput")
    def attachment_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies"]]], jsii.get(self, "attachmentPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="coreNetworkConfigurationInput")
    def core_network_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration"]]], jsii.get(self, "coreNetworkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentActionsInput")
    def segment_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions"]]], jsii.get(self, "segmentActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentsInput")
    def segments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments"]]], jsii.get(self, "segmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__559d5461b5e9cd5f706368a8470a805d8c8e71fa573aad3f352cf5da0788fbc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2a3ada3e77b621b0861c0c51cd9fdab2d07590fa39563dab9493b99648d1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "conditions": "conditions",
        "rule_number": "ruleNumber",
        "condition_logic": "conditionLogic",
        "description": "description",
    },
)
class DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies:
    def __init__(
        self,
        *,
        action: typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction", typing.Dict[builtins.str, typing.Any]],
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions", typing.Dict[builtins.str, typing.Any]]]],
        rule_number: jsii.Number,
        condition_logic: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#action DataAwsNetworkmanagerCoreNetworkPolicyDocument#action}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#conditions DataAwsNetworkmanagerCoreNetworkPolicyDocument#conditions}
        :param rule_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#rule_number DataAwsNetworkmanagerCoreNetworkPolicyDocument#rule_number}.
        :param condition_logic: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#condition_logic DataAwsNetworkmanagerCoreNetworkPolicyDocument#condition_logic}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#description DataAwsNetworkmanagerCoreNetworkPolicyDocument#description}.
        '''
        if isinstance(action, dict):
            action = DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d8487c97f2291d92c4db140480d9f283460d2fa330fcb327fdaba89189a4735)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument rule_number", value=rule_number, expected_type=type_hints["rule_number"])
            check_type(argname="argument condition_logic", value=condition_logic, expected_type=type_hints["condition_logic"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "conditions": conditions,
            "rule_number": rule_number,
        }
        if condition_logic is not None:
            self._values["condition_logic"] = condition_logic
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def action(
        self,
    ) -> "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction":
        '''action block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#action DataAwsNetworkmanagerCoreNetworkPolicyDocument#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction", result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions"]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#conditions DataAwsNetworkmanagerCoreNetworkPolicyDocument#conditions}
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions"]], result)

    @builtins.property
    def rule_number(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#rule_number DataAwsNetworkmanagerCoreNetworkPolicyDocument#rule_number}.'''
        result = self._values.get("rule_number")
        assert result is not None, "Required property 'rule_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def condition_logic(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#condition_logic DataAwsNetworkmanagerCoreNetworkPolicyDocument#condition_logic}.'''
        result = self._values.get("condition_logic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#description DataAwsNetworkmanagerCoreNetworkPolicyDocument#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction",
    jsii_struct_bases=[],
    name_mapping={
        "association_method": "associationMethod",
        "require_acceptance": "requireAcceptance",
        "segment": "segment",
        "tag_value_of_key": "tagValueOfKey",
    },
)
class DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction:
    def __init__(
        self,
        *,
        association_method: builtins.str,
        require_acceptance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        segment: typing.Optional[builtins.str] = None,
        tag_value_of_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param association_method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#association_method DataAwsNetworkmanagerCoreNetworkPolicyDocument#association_method}.
        :param require_acceptance: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#require_acceptance DataAwsNetworkmanagerCoreNetworkPolicyDocument#require_acceptance}.
        :param segment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#segment DataAwsNetworkmanagerCoreNetworkPolicyDocument#segment}.
        :param tag_value_of_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#tag_value_of_key DataAwsNetworkmanagerCoreNetworkPolicyDocument#tag_value_of_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66976f360d8653a45f387ba72ba98261aa337c24d399df9173f120ded9a96978)
            check_type(argname="argument association_method", value=association_method, expected_type=type_hints["association_method"])
            check_type(argname="argument require_acceptance", value=require_acceptance, expected_type=type_hints["require_acceptance"])
            check_type(argname="argument segment", value=segment, expected_type=type_hints["segment"])
            check_type(argname="argument tag_value_of_key", value=tag_value_of_key, expected_type=type_hints["tag_value_of_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "association_method": association_method,
        }
        if require_acceptance is not None:
            self._values["require_acceptance"] = require_acceptance
        if segment is not None:
            self._values["segment"] = segment
        if tag_value_of_key is not None:
            self._values["tag_value_of_key"] = tag_value_of_key

    @builtins.property
    def association_method(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#association_method DataAwsNetworkmanagerCoreNetworkPolicyDocument#association_method}.'''
        result = self._values.get("association_method")
        assert result is not None, "Required property 'association_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def require_acceptance(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#require_acceptance DataAwsNetworkmanagerCoreNetworkPolicyDocument#require_acceptance}.'''
        result = self._values.get("require_acceptance")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def segment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#segment DataAwsNetworkmanagerCoreNetworkPolicyDocument#segment}.'''
        result = self._values.get("segment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value_of_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#tag_value_of_key DataAwsNetworkmanagerCoreNetworkPolicyDocument#tag_value_of_key}.'''
        result = self._values.get("tag_value_of_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcf168c7bb1dac741a58ea2d09e8f0556b52b198417963f667d302b570fcc018)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRequireAcceptance")
    def reset_require_acceptance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireAcceptance", []))

    @jsii.member(jsii_name="resetSegment")
    def reset_segment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSegment", []))

    @jsii.member(jsii_name="resetTagValueOfKey")
    def reset_tag_value_of_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValueOfKey", []))

    @builtins.property
    @jsii.member(jsii_name="associationMethodInput")
    def association_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "associationMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="requireAcceptanceInput")
    def require_acceptance_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireAcceptanceInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentInput")
    def segment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "segmentInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueOfKeyInput")
    def tag_value_of_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueOfKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="associationMethod")
    def association_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "associationMethod"))

    @association_method.setter
    def association_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212248ae63061aeb13bd5e099c5468f4bce3f37ea1f0df3ced35e767855abc3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="requireAcceptance")
    def require_acceptance(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireAcceptance"))

    @require_acceptance.setter
    def require_acceptance(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4790172adac050ab740c30afe320597a13ac3b4dba8ad1c200d4eceace397184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAcceptance", value)

    @builtins.property
    @jsii.member(jsii_name="segment")
    def segment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "segment"))

    @segment.setter
    def segment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc5ce4a4636d7f06e4044b01745a9cd2bae03bedfb12abf76ac35554aa6847d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segment", value)

    @builtins.property
    @jsii.member(jsii_name="tagValueOfKey")
    def tag_value_of_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValueOfKey"))

    @tag_value_of_key.setter
    def tag_value_of_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c902523045e667f8c2f630c509269a30c72209cb3218c06e4f92245a49ca36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValueOfKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction]:
        return typing.cast(typing.Optional[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae69df513a46ef2fc311939a486f6b8f53fe945d50a6d0ad3dc703b6a393d24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "key": "key",
        "operator": "operator",
        "value": "value",
    },
)
class DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions:
    def __init__(
        self,
        *,
        type: builtins.str,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#type DataAwsNetworkmanagerCoreNetworkPolicyDocument#type}.
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#key DataAwsNetworkmanagerCoreNetworkPolicyDocument#key}.
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#operator DataAwsNetworkmanagerCoreNetworkPolicyDocument#operator}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#value DataAwsNetworkmanagerCoreNetworkPolicyDocument#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032e5e275a9f12436e1f82267cd378b351ff8532a633a94b9777bc9b5a37d347)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if key is not None:
            self._values["key"] = key
        if operator is not None:
            self._values["operator"] = operator
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#type DataAwsNetworkmanagerCoreNetworkPolicyDocument#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#key DataAwsNetworkmanagerCoreNetworkPolicyDocument#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#operator DataAwsNetworkmanagerCoreNetworkPolicyDocument#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#value DataAwsNetworkmanagerCoreNetworkPolicyDocument#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72d62e5159cac005d393fbb61bbba16cb225c28012c73446e2e6330c12c9e97a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d8b8a98d3b0b94509dc227df13bc562eab4f3be0ef8e7e7fde006f8de84dad0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c863f95b354d2554f47be68c34502242f9816af8ceb0b5886c3b02956a55b89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5502976785b90d6f0e6945cec18fd958e5d72329da03f6acd2ec4ac1d33718c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ac55bebd7a43d6d49e44ce6a17326de88915dbf771058d1fe5d11ffbbd5afd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3db355c2b6c00e4963b480e01c81bde80bf5fe30a8a5a56f17459e1e61894a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17ef1e2f62cd8365066389e1c6aa317d76fabaf0df0e7b383f8a40970cae954d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afae96d7599c8cc8e9fdad6ce38a070ff9faf613505d67965fab5cd126ecf095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f73f7bd2a2f1db0f12c272409452784cf9f04a0a98b6d0d0125deeda1952618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e025bef767e4da3715c48436625780e67466ae90865accbc9c7fcbabca70b99b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbaab719bdcc1da7c222e28cc4a1b0c13de32ee1fbc84b5d19e0462d827fb42f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c29ccf23816eb5d245832626c5e2d310c2678b0677e909fb66f42768fa3fa2d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c06d7bd585b86a6d33afe161799680d4449654279ad366b97dcdf723e817c8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48854a22c4b7942fc66acf60cec2968b2881544a6d0cb6e82dd303086f48ab00)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05eeca4477dd57ffb7a5e15a85018baa6cb89cb37e757ba6d2a766d14a72b8ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b51bb7308fa90ec7babc4e2c3ef6b0e178337d524451b4e318ccdb2b417ba770)
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
            type_hints = typing.get_type_hints(_typecheckingstub__870345679397ae6b54eefdbb28503772ad57551bd4fb080c3d6ab0b0b3bb8f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496b74d2981e4788ebc02dd4c30b68fcf150d275bff6026612c796c3c025c835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39582798f3eca97c17c5413a602951d4a29bbf35928b1d640e7dbc8f02af25ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        association_method: builtins.str,
        require_acceptance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        segment: typing.Optional[builtins.str] = None,
        tag_value_of_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param association_method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#association_method DataAwsNetworkmanagerCoreNetworkPolicyDocument#association_method}.
        :param require_acceptance: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#require_acceptance DataAwsNetworkmanagerCoreNetworkPolicyDocument#require_acceptance}.
        :param segment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#segment DataAwsNetworkmanagerCoreNetworkPolicyDocument#segment}.
        :param tag_value_of_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#tag_value_of_key DataAwsNetworkmanagerCoreNetworkPolicyDocument#tag_value_of_key}.
        '''
        value = DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction(
            association_method=association_method,
            require_acceptance=require_acceptance,
            segment=segment,
            tag_value_of_key=tag_value_of_key,
        )

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152b226a06ab166aa9100a33b05ba7ac892d50a0bcc153a60e0d2a3ae6893bc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="resetConditionLogic")
    def reset_condition_logic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionLogic", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(
        self,
    ) -> DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesActionOutputReference:
        return typing.cast(DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditionsList:
        return typing.cast(DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction]:
        return typing.cast(typing.Optional[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionLogicInput")
    def condition_logic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionLogicInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleNumberInput")
    def rule_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ruleNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionLogic")
    def condition_logic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionLogic"))

    @condition_logic.setter
    def condition_logic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f67c12f2ba74e89b8f7a7bf9fec87e2bc06b503d974c9f8cbd8e6384942252e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionLogic", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3967f00f0e49e6f217bda5c98e81bdd727e4edaf392c5b6269d7546b31bbc62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="ruleNumber")
    def rule_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleNumber"))

    @rule_number.setter
    def rule_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51b54345a3466abfcdf18407f50858e97d2b86b3e682e5679369dfa85c98d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f77ecd6981c6680bcd4a2774efa10ef06df7f4568eb3568adec4c68f87c716d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "core_network_configuration": "coreNetworkConfiguration",
        "segments": "segments",
        "attachment_policies": "attachmentPolicies",
        "id": "id",
        "segment_actions": "segmentActions",
        "version": "version",
    },
)
class DataAwsNetworkmanagerCoreNetworkPolicyDocumentConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        core_network_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        segments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments", typing.Dict[builtins.str, typing.Any]]]],
        attachment_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        segment_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param core_network_configuration: core_network_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#core_network_configuration DataAwsNetworkmanagerCoreNetworkPolicyDocument#core_network_configuration}
        :param segments: segments block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#segments DataAwsNetworkmanagerCoreNetworkPolicyDocument#segments}
        :param attachment_policies: attachment_policies block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#attachment_policies DataAwsNetworkmanagerCoreNetworkPolicyDocument#attachment_policies}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#id DataAwsNetworkmanagerCoreNetworkPolicyDocument#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param segment_actions: segment_actions block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#segment_actions DataAwsNetworkmanagerCoreNetworkPolicyDocument#segment_actions}
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#version DataAwsNetworkmanagerCoreNetworkPolicyDocument#version}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3afe0fa94b8cacce91eea79141c6419063cf2c0e11e13115005d089e15659eb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument core_network_configuration", value=core_network_configuration, expected_type=type_hints["core_network_configuration"])
            check_type(argname="argument segments", value=segments, expected_type=type_hints["segments"])
            check_type(argname="argument attachment_policies", value=attachment_policies, expected_type=type_hints["attachment_policies"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument segment_actions", value=segment_actions, expected_type=type_hints["segment_actions"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "core_network_configuration": core_network_configuration,
            "segments": segments,
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
        if attachment_policies is not None:
            self._values["attachment_policies"] = attachment_policies
        if id is not None:
            self._values["id"] = id
        if segment_actions is not None:
            self._values["segment_actions"] = segment_actions
        if version is not None:
            self._values["version"] = version

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
    def core_network_configuration(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration"]]:
        '''core_network_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#core_network_configuration DataAwsNetworkmanagerCoreNetworkPolicyDocument#core_network_configuration}
        '''
        result = self._values.get("core_network_configuration")
        assert result is not None, "Required property 'core_network_configuration' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration"]], result)

    @builtins.property
    def segments(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments"]]:
        '''segments block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#segments DataAwsNetworkmanagerCoreNetworkPolicyDocument#segments}
        '''
        result = self._values.get("segments")
        assert result is not None, "Required property 'segments' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments"]], result)

    @builtins.property
    def attachment_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies]]]:
        '''attachment_policies block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#attachment_policies DataAwsNetworkmanagerCoreNetworkPolicyDocument#attachment_policies}
        '''
        result = self._values.get("attachment_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#id DataAwsNetworkmanagerCoreNetworkPolicyDocument#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def segment_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions"]]]:
        '''segment_actions block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#segment_actions DataAwsNetworkmanagerCoreNetworkPolicyDocument#segment_actions}
        '''
        result = self._values.get("segment_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions"]]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#version DataAwsNetworkmanagerCoreNetworkPolicyDocument#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsNetworkmanagerCoreNetworkPolicyDocumentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "asn_ranges": "asnRanges",
        "edge_locations": "edgeLocations",
        "inside_cidr_blocks": "insideCidrBlocks",
        "vpn_ecmp_support": "vpnEcmpSupport",
    },
)
class DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration:
    def __init__(
        self,
        *,
        asn_ranges: typing.Sequence[builtins.str],
        edge_locations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations", typing.Dict[builtins.str, typing.Any]]]],
        inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpn_ecmp_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param asn_ranges: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#asn_ranges DataAwsNetworkmanagerCoreNetworkPolicyDocument#asn_ranges}.
        :param edge_locations: edge_locations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#edge_locations DataAwsNetworkmanagerCoreNetworkPolicyDocument#edge_locations}
        :param inside_cidr_blocks: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#inside_cidr_blocks DataAwsNetworkmanagerCoreNetworkPolicyDocument#inside_cidr_blocks}.
        :param vpn_ecmp_support: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#vpn_ecmp_support DataAwsNetworkmanagerCoreNetworkPolicyDocument#vpn_ecmp_support}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b063a8be9c7d404a88e077544162dba961be4dcb4afdcf24d82c8dc15541101)
            check_type(argname="argument asn_ranges", value=asn_ranges, expected_type=type_hints["asn_ranges"])
            check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
            check_type(argname="argument inside_cidr_blocks", value=inside_cidr_blocks, expected_type=type_hints["inside_cidr_blocks"])
            check_type(argname="argument vpn_ecmp_support", value=vpn_ecmp_support, expected_type=type_hints["vpn_ecmp_support"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asn_ranges": asn_ranges,
            "edge_locations": edge_locations,
        }
        if inside_cidr_blocks is not None:
            self._values["inside_cidr_blocks"] = inside_cidr_blocks
        if vpn_ecmp_support is not None:
            self._values["vpn_ecmp_support"] = vpn_ecmp_support

    @builtins.property
    def asn_ranges(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#asn_ranges DataAwsNetworkmanagerCoreNetworkPolicyDocument#asn_ranges}.'''
        result = self._values.get("asn_ranges")
        assert result is not None, "Required property 'asn_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def edge_locations(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations"]]:
        '''edge_locations block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#edge_locations DataAwsNetworkmanagerCoreNetworkPolicyDocument#edge_locations}
        '''
        result = self._values.get("edge_locations")
        assert result is not None, "Required property 'edge_locations' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations"]], result)

    @builtins.property
    def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#inside_cidr_blocks DataAwsNetworkmanagerCoreNetworkPolicyDocument#inside_cidr_blocks}.'''
        result = self._values.get("inside_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpn_ecmp_support(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#vpn_ecmp_support DataAwsNetworkmanagerCoreNetworkPolicyDocument#vpn_ecmp_support}.'''
        result = self._values.get("vpn_ecmp_support")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "asn": "asn",
        "inside_cidr_blocks": "insideCidrBlocks",
    },
)
class DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations:
    def __init__(
        self,
        *,
        location: builtins.str,
        asn: typing.Optional[builtins.str] = None,
        inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#location DataAwsNetworkmanagerCoreNetworkPolicyDocument#location}.
        :param asn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#asn DataAwsNetworkmanagerCoreNetworkPolicyDocument#asn}.
        :param inside_cidr_blocks: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#inside_cidr_blocks DataAwsNetworkmanagerCoreNetworkPolicyDocument#inside_cidr_blocks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c7ddbdb277b192ea6dc2bceeed641e4ecc2f2b911f6722bc391388dac77dd1)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
            check_type(argname="argument inside_cidr_blocks", value=inside_cidr_blocks, expected_type=type_hints["inside_cidr_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }
        if asn is not None:
            self._values["asn"] = asn
        if inside_cidr_blocks is not None:
            self._values["inside_cidr_blocks"] = inside_cidr_blocks

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#location DataAwsNetworkmanagerCoreNetworkPolicyDocument#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#asn DataAwsNetworkmanagerCoreNetworkPolicyDocument#asn}.'''
        result = self._values.get("asn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#inside_cidr_blocks DataAwsNetworkmanagerCoreNetworkPolicyDocument#inside_cidr_blocks}.'''
        result = self._values.get("inside_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a3d2fb8d73afe9dc44727ef81c3009e80ad3969d47b862fc9a89c97a1e0e55e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731be63368d296875a282677a1e811c940eba713fb2c78777c569ec06781771e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb977efd132341a0cf2f2500b871b2d9a1f9adc605478f0c16832e22a29e749b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e4868e114031cbd1814b62c986b5ebe5d2fa1dc6e663b0428961cee19ce6b9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f55aa05654247208d0fb7cd52337889c34d17e918947d5de24149bee7a99d487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b1be021a554d1178fece063ea660d4785ae15ca3912c7bff4969af74ca40bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56a0251c60a1b05cff913fab34e01b1d97c040640838b88f3d167f4e1860836b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAsn")
    def reset_asn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsn", []))

    @jsii.member(jsii_name="resetInsideCidrBlocks")
    def reset_inside_cidr_blocks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsideCidrBlocks", []))

    @builtins.property
    @jsii.member(jsii_name="asnInput")
    def asn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "asnInput"))

    @builtins.property
    @jsii.member(jsii_name="insideCidrBlocksInput")
    def inside_cidr_blocks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "insideCidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="asn")
    def asn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "asn"))

    @asn.setter
    def asn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5f97877f9ebe79aa6d1dce70197faca1923d0edd1dc70041dc8d8520c70a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value)

    @builtins.property
    @jsii.member(jsii_name="insideCidrBlocks")
    def inside_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "insideCidrBlocks"))

    @inside_cidr_blocks.setter
    def inside_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c28fab0860f4a020fbc369fa2f65a755475dec079fc129ec0fa51e4d533971c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insideCidrBlocks", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079a5b19e53bfe8c9a51eab3731e4edab2ae1a6bbdc07922afe6dfb290a77716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc45cf873570233044b02fdf999d25c16af5d40037ea978f3f16586dc0abbd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9f2f17b4326a0c9f7677a4e5de8ffa2487e5b6838f30cb571d74104c92b7754)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70a37440d63a474a7d94a5c1550a1edaca0aa3dd61242496bed7331827ce85b4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f514512d0fc71c6e3cdb9c37b7cd70746c89d3b1ed5350b52115efdf1a177f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b2846d16a2481c9172257862c629a4a7b37deaa761d6dec6be994bd577d7002)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6573f1a7828e796c3702bff50fe7acebdded72d56d629985c1f261098a35b0b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97e3717ae2192e848ae6134a45414a762e0842280fd46af5a153b11ef93413b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e29c6a6819145f546fa61accf506d81acff87220a0a00ea153e45272b83dde9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEdgeLocations")
    def put_edge_locations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1e0ea4755c6caff9f89f23f92e76583af7b23f6143e82764a8d6d259b880eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEdgeLocations", [value]))

    @jsii.member(jsii_name="resetInsideCidrBlocks")
    def reset_inside_cidr_blocks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsideCidrBlocks", []))

    @jsii.member(jsii_name="resetVpnEcmpSupport")
    def reset_vpn_ecmp_support(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpnEcmpSupport", []))

    @builtins.property
    @jsii.member(jsii_name="edgeLocations")
    def edge_locations(
        self,
    ) -> DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocationsList:
        return typing.cast(DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocationsList, jsii.get(self, "edgeLocations"))

    @builtins.property
    @jsii.member(jsii_name="asnRangesInput")
    def asn_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "asnRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeLocationsInput")
    def edge_locations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations]]], jsii.get(self, "edgeLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="insideCidrBlocksInput")
    def inside_cidr_blocks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "insideCidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnEcmpSupportInput")
    def vpn_ecmp_support_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vpnEcmpSupportInput"))

    @builtins.property
    @jsii.member(jsii_name="asnRanges")
    def asn_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "asnRanges"))

    @asn_ranges.setter
    def asn_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e0530a64009ad17c1891deb0b7a91fc70e46302789213daf2e4a39abd49c01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asnRanges", value)

    @builtins.property
    @jsii.member(jsii_name="insideCidrBlocks")
    def inside_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "insideCidrBlocks"))

    @inside_cidr_blocks.setter
    def inside_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8e1b93c1a74d33830ee245a516c4c089da682524ea04cf4857f785a4d1bad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insideCidrBlocks", value)

    @builtins.property
    @jsii.member(jsii_name="vpnEcmpSupport")
    def vpn_ecmp_support(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vpnEcmpSupport"))

    @vpn_ecmp_support.setter
    def vpn_ecmp_support(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d6bf0ad6774f26d36120b7e14138ce437fdc324f0199bd6ecd6daa387993ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnEcmpSupport", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1545bc0de9ab3b5efbd265f8b634a5f10a1cd6aebb31ec60fe2fcc18e3482a39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "segment": "segment",
        "description": "description",
        "destination_cidr_blocks": "destinationCidrBlocks",
        "destinations": "destinations",
        "mode": "mode",
        "share_with": "shareWith",
        "share_with_except": "shareWithExcept",
    },
)
class DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions:
    def __init__(
        self,
        *,
        action: builtins.str,
        segment: builtins.str,
        description: typing.Optional[builtins.str] = None,
        destination_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        mode: typing.Optional[builtins.str] = None,
        share_with: typing.Optional[typing.Sequence[builtins.str]] = None,
        share_with_except: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#action DataAwsNetworkmanagerCoreNetworkPolicyDocument#action}.
        :param segment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#segment DataAwsNetworkmanagerCoreNetworkPolicyDocument#segment}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#description DataAwsNetworkmanagerCoreNetworkPolicyDocument#description}.
        :param destination_cidr_blocks: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#destination_cidr_blocks DataAwsNetworkmanagerCoreNetworkPolicyDocument#destination_cidr_blocks}.
        :param destinations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#destinations DataAwsNetworkmanagerCoreNetworkPolicyDocument#destinations}.
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#mode DataAwsNetworkmanagerCoreNetworkPolicyDocument#mode}.
        :param share_with: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#share_with DataAwsNetworkmanagerCoreNetworkPolicyDocument#share_with}.
        :param share_with_except: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#share_with_except DataAwsNetworkmanagerCoreNetworkPolicyDocument#share_with_except}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020e2c35382d3e96119250c60f4be302c6149634f90d9341666e7a6d4f87c284)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument segment", value=segment, expected_type=type_hints["segment"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_cidr_blocks", value=destination_cidr_blocks, expected_type=type_hints["destination_cidr_blocks"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument share_with", value=share_with, expected_type=type_hints["share_with"])
            check_type(argname="argument share_with_except", value=share_with_except, expected_type=type_hints["share_with_except"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "segment": segment,
        }
        if description is not None:
            self._values["description"] = description
        if destination_cidr_blocks is not None:
            self._values["destination_cidr_blocks"] = destination_cidr_blocks
        if destinations is not None:
            self._values["destinations"] = destinations
        if mode is not None:
            self._values["mode"] = mode
        if share_with is not None:
            self._values["share_with"] = share_with
        if share_with_except is not None:
            self._values["share_with_except"] = share_with_except

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#action DataAwsNetworkmanagerCoreNetworkPolicyDocument#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def segment(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#segment DataAwsNetworkmanagerCoreNetworkPolicyDocument#segment}.'''
        result = self._values.get("segment")
        assert result is not None, "Required property 'segment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#description DataAwsNetworkmanagerCoreNetworkPolicyDocument#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#destination_cidr_blocks DataAwsNetworkmanagerCoreNetworkPolicyDocument#destination_cidr_blocks}.'''
        result = self._values.get("destination_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def destinations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#destinations DataAwsNetworkmanagerCoreNetworkPolicyDocument#destinations}.'''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#mode DataAwsNetworkmanagerCoreNetworkPolicyDocument#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_with(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#share_with DataAwsNetworkmanagerCoreNetworkPolicyDocument#share_with}.'''
        result = self._values.get("share_with")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def share_with_except(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#share_with_except DataAwsNetworkmanagerCoreNetworkPolicyDocument#share_with_except}.'''
        result = self._values.get("share_with_except")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d87a0bb2887501ad424a1919cb071ba499a6d40a7f2a1110254438bffc382ebf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48db07f958faf5737c778a7559403e98304b33715e1a6244c0368612c83a223)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf704b5704950dd129fea617b91081d11db697a845b94c8f594cfbb1322dd90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e00971b0bd762cefeb8a002d1a9e3e488a8dfdb021a5fdef63af4cbdc5fb6be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5beb74b9b5d19367475c397aeb621dc6df27aedd409695cf8fcea13c8292dd7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdddf8d2f9258974b1fbc2a0e6bb1b64a365b9697443a51d1d2f014ee678b0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6df622c173b92196d9a97ca71d682496be072d3ed33a6bc1d1db4407fc93467)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDestinationCidrBlocks")
    def reset_destination_cidr_blocks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationCidrBlocks", []))

    @jsii.member(jsii_name="resetDestinations")
    def reset_destinations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinations", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetShareWith")
    def reset_share_with(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareWith", []))

    @jsii.member(jsii_name="resetShareWithExcept")
    def reset_share_with_except(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareWithExcept", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationCidrBlocksInput")
    def destination_cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationCidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationsInput")
    def destinations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="segmentInput")
    def segment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "segmentInput"))

    @builtins.property
    @jsii.member(jsii_name="shareWithExceptInput")
    def share_with_except_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "shareWithExceptInput"))

    @builtins.property
    @jsii.member(jsii_name="shareWithInput")
    def share_with_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "shareWithInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3695f86ebe8fca92d373a027f242130665a1687c1806eef2f09d4a08fb716b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4cb09ea1522c78f131db443d747404d0d735b3cf87278d66e0475f95a7c573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="destinationCidrBlocks")
    def destination_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinationCidrBlocks"))

    @destination_cidr_blocks.setter
    def destination_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91ab0d4deb7954b149d4ff6c3a6876042eb071c67f50df8d81376176df9b0a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationCidrBlocks", value)

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinations"))

    @destinations.setter
    def destinations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c606db2757362d544f823382cec0a66bab2e91a6b04eba8af3488a43e98b0a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinations", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60aff452089d7a23e8474473db0eb060ca095dbc73745fd48c24f1860c6133a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="segment")
    def segment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "segment"))

    @segment.setter
    def segment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b6cf4c2cc75d3ba37e36294692eecc4c894829e88ba67e7e47eed7fce10cce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "segment", value)

    @builtins.property
    @jsii.member(jsii_name="shareWith")
    def share_with(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "shareWith"))

    @share_with.setter
    def share_with(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120fd092cf48ccaac62718b82237efc39bb91017f483b0bfffd998181b181c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareWith", value)

    @builtins.property
    @jsii.member(jsii_name="shareWithExcept")
    def share_with_except(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "shareWithExcept"))

    @share_with_except.setter
    def share_with_except(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48a4a7eda183c5130e81b9432a1796ebae4210835e1ce614c4da7f7055490afb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareWithExcept", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c9b4498087af3b141807ca9044818209c22fbb64382533cbece38f08a491e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_filter": "allowFilter",
        "deny_filter": "denyFilter",
        "description": "description",
        "edge_locations": "edgeLocations",
        "isolate_attachments": "isolateAttachments",
        "require_attachment_acceptance": "requireAttachmentAcceptance",
    },
)
class DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        deny_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        edge_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        isolate_attachments: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_attachment_acceptance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#name DataAwsNetworkmanagerCoreNetworkPolicyDocument#name}.
        :param allow_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#allow_filter DataAwsNetworkmanagerCoreNetworkPolicyDocument#allow_filter}.
        :param deny_filter: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#deny_filter DataAwsNetworkmanagerCoreNetworkPolicyDocument#deny_filter}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#description DataAwsNetworkmanagerCoreNetworkPolicyDocument#description}.
        :param edge_locations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#edge_locations DataAwsNetworkmanagerCoreNetworkPolicyDocument#edge_locations}.
        :param isolate_attachments: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#isolate_attachments DataAwsNetworkmanagerCoreNetworkPolicyDocument#isolate_attachments}.
        :param require_attachment_acceptance: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#require_attachment_acceptance DataAwsNetworkmanagerCoreNetworkPolicyDocument#require_attachment_acceptance}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4302c7fcf2c21c6155b0f005f75674deec6c6ef6bd363fbd45c8498c7907b1d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_filter", value=allow_filter, expected_type=type_hints["allow_filter"])
            check_type(argname="argument deny_filter", value=deny_filter, expected_type=type_hints["deny_filter"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
            check_type(argname="argument isolate_attachments", value=isolate_attachments, expected_type=type_hints["isolate_attachments"])
            check_type(argname="argument require_attachment_acceptance", value=require_attachment_acceptance, expected_type=type_hints["require_attachment_acceptance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allow_filter is not None:
            self._values["allow_filter"] = allow_filter
        if deny_filter is not None:
            self._values["deny_filter"] = deny_filter
        if description is not None:
            self._values["description"] = description
        if edge_locations is not None:
            self._values["edge_locations"] = edge_locations
        if isolate_attachments is not None:
            self._values["isolate_attachments"] = isolate_attachments
        if require_attachment_acceptance is not None:
            self._values["require_attachment_acceptance"] = require_attachment_acceptance

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#name DataAwsNetworkmanagerCoreNetworkPolicyDocument#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#allow_filter DataAwsNetworkmanagerCoreNetworkPolicyDocument#allow_filter}.'''
        result = self._values.get("allow_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deny_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#deny_filter DataAwsNetworkmanagerCoreNetworkPolicyDocument#deny_filter}.'''
        result = self._values.get("deny_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#description DataAwsNetworkmanagerCoreNetworkPolicyDocument#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#edge_locations DataAwsNetworkmanagerCoreNetworkPolicyDocument#edge_locations}.'''
        result = self._values.get("edge_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def isolate_attachments(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#isolate_attachments DataAwsNetworkmanagerCoreNetworkPolicyDocument#isolate_attachments}.'''
        result = self._values.get("isolate_attachments")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_attachment_acceptance(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/networkmanager_core_network_policy_document#require_attachment_acceptance DataAwsNetworkmanagerCoreNetworkPolicyDocument#require_attachment_acceptance}.'''
        result = self._values.get("require_attachment_acceptance")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c21658477b720e3917ad992814d0d4420bec74754d3ea715a80e721ea9ce4226)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a5facf9453ab0d6d1555f0edc491710c36a70f2150a2fc3c7f644aed79df52a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b234fa66f81b89ca64551411237c41981a2f50c5b12f7cc4a84462816f76d20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__514a60d74bfeb05793dc470e48391b50626354e93233838b87365930d9924426)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeb8aa645f38ed022a43f5dbdba35b03488b8025af708e1693d26948dbdbb012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb661a39b2081b5884aa362296d23aef6355b7fb9f308cf5cf211914ecce5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsNetworkmanagerCoreNetworkPolicyDocument.DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31bf8ae8abf2d318d26c7e49cf344d22b7c04ae9f7a30b97e9142e1ff093e692)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowFilter")
    def reset_allow_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowFilter", []))

    @jsii.member(jsii_name="resetDenyFilter")
    def reset_deny_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyFilter", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEdgeLocations")
    def reset_edge_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeLocations", []))

    @jsii.member(jsii_name="resetIsolateAttachments")
    def reset_isolate_attachments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsolateAttachments", []))

    @jsii.member(jsii_name="resetRequireAttachmentAcceptance")
    def reset_require_attachment_acceptance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireAttachmentAcceptance", []))

    @builtins.property
    @jsii.member(jsii_name="allowFilterInput")
    def allow_filter_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="denyFilterInput")
    def deny_filter_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "denyFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeLocationsInput")
    def edge_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "edgeLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="isolateAttachmentsInput")
    def isolate_attachments_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isolateAttachmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requireAttachmentAcceptanceInput")
    def require_attachment_acceptance_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireAttachmentAcceptanceInput"))

    @builtins.property
    @jsii.member(jsii_name="allowFilter")
    def allow_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowFilter"))

    @allow_filter.setter
    def allow_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7edf54165a440248f13578f449bf81ba80ce51266f3107a7cf495513a6c2716f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowFilter", value)

    @builtins.property
    @jsii.member(jsii_name="denyFilter")
    def deny_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "denyFilter"))

    @deny_filter.setter
    def deny_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e3b263d43877c5ae982c1addc61eef1ce603f526079d43b5ff2f466bffc0da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyFilter", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44cbea8d517c3951006a8508541f68a83c70c5188254a8f10a555155c2750cf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="edgeLocations")
    def edge_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "edgeLocations"))

    @edge_locations.setter
    def edge_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8772060258723dce386e363de744b09a93597a7c6675e00b2637ec89a87a2a88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeLocations", value)

    @builtins.property
    @jsii.member(jsii_name="isolateAttachments")
    def isolate_attachments(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isolateAttachments"))

    @isolate_attachments.setter
    def isolate_attachments(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a57c6b0ddbe281408efaa289d52de9a96a6e7d70d7f3d677ea1dd867342bebd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isolateAttachments", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8c5298c836d065b55293b3d14111f7f443ccbb080a36d125ce112a2f05e53c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="requireAttachmentAcceptance")
    def require_attachment_acceptance(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireAttachmentAcceptance"))

    @require_attachment_acceptance.setter
    def require_attachment_acceptance(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64ad1e8b3c3b56d42a53a8bfd8dbeaa2a18cb5f4fec6296c0c5b30a84f0b1ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAttachmentAcceptance", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479d69e7b6c83a6c4589b5f52a354428f92c4f9cddaa6f5b02b9a6083166a8ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataAwsNetworkmanagerCoreNetworkPolicyDocument",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesActionOutputReference",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditionsList",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditionsOutputReference",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesList",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesOutputReference",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentConfig",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocationsList",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocationsOutputReference",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationList",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationOutputReference",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActionsList",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActionsOutputReference",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentsList",
    "DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentsOutputReference",
]

publication.publish()

def _typecheckingstub__9df29d47d6dde10f511d59a019b9ac71d75d61b482857becefd3c241072f214e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    core_network_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    segments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments, typing.Dict[builtins.str, typing.Any]]]],
    attachment_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    segment_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    version: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__fcad7ccfe4b6a6b0f1c62dc050a14d799f74aead5d48ae046c0892a1d814ed88(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176fd6b2e8c19ce618cb1f5d88081b062146b5342b66afd2879a9a0cb1ca5edd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b99a41ae4c887c16a2e46d0581908a9091350d9a0d76a484bead50dff2e32c4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a9de918a77f9a83aef8c1f9ac0a5a247bf3254332bfcbafce14aa67f18e091(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559d5461b5e9cd5f706368a8470a805d8c8e71fa573aad3f352cf5da0788fbc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2a3ada3e77b621b0861c0c51cd9fdab2d07590fa39563dab9493b99648d1f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d8487c97f2291d92c4db140480d9f283460d2fa330fcb327fdaba89189a4735(
    *,
    action: typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction, typing.Dict[builtins.str, typing.Any]],
    conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions, typing.Dict[builtins.str, typing.Any]]]],
    rule_number: jsii.Number,
    condition_logic: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66976f360d8653a45f387ba72ba98261aa337c24d399df9173f120ded9a96978(
    *,
    association_method: builtins.str,
    require_acceptance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    segment: typing.Optional[builtins.str] = None,
    tag_value_of_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf168c7bb1dac741a58ea2d09e8f0556b52b198417963f667d302b570fcc018(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212248ae63061aeb13bd5e099c5468f4bce3f37ea1f0df3ced35e767855abc3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4790172adac050ab740c30afe320597a13ac3b4dba8ad1c200d4eceace397184(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc5ce4a4636d7f06e4044b01745a9cd2bae03bedfb12abf76ac35554aa6847d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c902523045e667f8c2f630c509269a30c72209cb3218c06e4f92245a49ca36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae69df513a46ef2fc311939a486f6b8f53fe945d50a6d0ad3dc703b6a393d24(
    value: typing.Optional[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032e5e275a9f12436e1f82267cd378b351ff8532a633a94b9777bc9b5a37d347(
    *,
    type: builtins.str,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d62e5159cac005d393fbb61bbba16cb225c28012c73446e2e6330c12c9e97a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d8b8a98d3b0b94509dc227df13bc562eab4f3be0ef8e7e7fde006f8de84dad0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c863f95b354d2554f47be68c34502242f9816af8ceb0b5886c3b02956a55b89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5502976785b90d6f0e6945cec18fd958e5d72329da03f6acd2ec4ac1d33718c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac55bebd7a43d6d49e44ce6a17326de88915dbf771058d1fe5d11ffbbd5afd6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3db355c2b6c00e4963b480e01c81bde80bf5fe30a8a5a56f17459e1e61894a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ef1e2f62cd8365066389e1c6aa317d76fabaf0df0e7b383f8a40970cae954d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afae96d7599c8cc8e9fdad6ce38a070ff9faf613505d67965fab5cd126ecf095(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f73f7bd2a2f1db0f12c272409452784cf9f04a0a98b6d0d0125deeda1952618(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e025bef767e4da3715c48436625780e67466ae90865accbc9c7fcbabca70b99b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbaab719bdcc1da7c222e28cc4a1b0c13de32ee1fbc84b5d19e0462d827fb42f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29ccf23816eb5d245832626c5e2d310c2678b0677e909fb66f42768fa3fa2d9(
    value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c06d7bd585b86a6d33afe161799680d4449654279ad366b97dcdf723e817c8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48854a22c4b7942fc66acf60cec2968b2881544a6d0cb6e82dd303086f48ab00(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05eeca4477dd57ffb7a5e15a85018baa6cb89cb37e757ba6d2a766d14a72b8ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51bb7308fa90ec7babc4e2c3ef6b0e178337d524451b4e318ccdb2b417ba770(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__870345679397ae6b54eefdbb28503772ad57551bd4fb080c3d6ab0b0b3bb8f73(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496b74d2981e4788ebc02dd4c30b68fcf150d275bff6026612c796c3c025c835(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39582798f3eca97c17c5413a602951d4a29bbf35928b1d640e7dbc8f02af25ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152b226a06ab166aa9100a33b05ba7ac892d50a0bcc153a60e0d2a3ae6893bc2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPoliciesConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f67c12f2ba74e89b8f7a7bf9fec87e2bc06b503d974c9f8cbd8e6384942252e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3967f00f0e49e6f217bda5c98e81bdd727e4edaf392c5b6269d7546b31bbc62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51b54345a3466abfcdf18407f50858e97d2b86b3e682e5679369dfa85c98d03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f77ecd6981c6680bcd4a2774efa10ef06df7f4568eb3568adec4c68f87c716d(
    value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3afe0fa94b8cacce91eea79141c6419063cf2c0e11e13115005d089e15659eb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    core_network_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    segments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments, typing.Dict[builtins.str, typing.Any]]]],
    attachment_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentAttachmentPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    segment_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b063a8be9c7d404a88e077544162dba961be4dcb4afdcf24d82c8dc15541101(
    *,
    asn_ranges: typing.Sequence[builtins.str],
    edge_locations: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations, typing.Dict[builtins.str, typing.Any]]]],
    inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpn_ecmp_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c7ddbdb277b192ea6dc2bceeed641e4ecc2f2b911f6722bc391388dac77dd1(
    *,
    location: builtins.str,
    asn: typing.Optional[builtins.str] = None,
    inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3d2fb8d73afe9dc44727ef81c3009e80ad3969d47b862fc9a89c97a1e0e55e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731be63368d296875a282677a1e811c940eba713fb2c78777c569ec06781771e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb977efd132341a0cf2f2500b871b2d9a1f9adc605478f0c16832e22a29e749b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4868e114031cbd1814b62c986b5ebe5d2fa1dc6e663b0428961cee19ce6b9a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f55aa05654247208d0fb7cd52337889c34d17e918947d5de24149bee7a99d487(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b1be021a554d1178fece063ea660d4785ae15ca3912c7bff4969af74ca40bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a0251c60a1b05cff913fab34e01b1d97c040640838b88f3d167f4e1860836b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5f97877f9ebe79aa6d1dce70197faca1923d0edd1dc70041dc8d8520c70a53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c28fab0860f4a020fbc369fa2f65a755475dec079fc129ec0fa51e4d533971c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079a5b19e53bfe8c9a51eab3731e4edab2ae1a6bbdc07922afe6dfb290a77716(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc45cf873570233044b02fdf999d25c16af5d40037ea978f3f16586dc0abbd3(
    value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f2f17b4326a0c9f7677a4e5de8ffa2487e5b6838f30cb571d74104c92b7754(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a37440d63a474a7d94a5c1550a1edaca0aa3dd61242496bed7331827ce85b4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f514512d0fc71c6e3cdb9c37b7cd70746c89d3b1ed5350b52115efdf1a177f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2846d16a2481c9172257862c629a4a7b37deaa761d6dec6be994bd577d7002(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6573f1a7828e796c3702bff50fe7acebdded72d56d629985c1f261098a35b0b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e3717ae2192e848ae6134a45414a762e0842280fd46af5a153b11ef93413b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e29c6a6819145f546fa61accf506d81acff87220a0a00ea153e45272b83dde9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e0ea4755c6caff9f89f23f92e76583af7b23f6143e82764a8d6d259b880eca(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfigurationEdgeLocations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0530a64009ad17c1891deb0b7a91fc70e46302789213daf2e4a39abd49c01a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8e1b93c1a74d33830ee245a516c4c089da682524ea04cf4857f785a4d1bad9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d6bf0ad6774f26d36120b7e14138ce437fdc324f0199bd6ecd6daa387993ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1545bc0de9ab3b5efbd265f8b634a5f10a1cd6aebb31ec60fe2fcc18e3482a39(
    value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentCoreNetworkConfiguration, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020e2c35382d3e96119250c60f4be302c6149634f90d9341666e7a6d4f87c284(
    *,
    action: builtins.str,
    segment: builtins.str,
    description: typing.Optional[builtins.str] = None,
    destination_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
    mode: typing.Optional[builtins.str] = None,
    share_with: typing.Optional[typing.Sequence[builtins.str]] = None,
    share_with_except: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87a0bb2887501ad424a1919cb071ba499a6d40a7f2a1110254438bffc382ebf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48db07f958faf5737c778a7559403e98304b33715e1a6244c0368612c83a223(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf704b5704950dd129fea617b91081d11db697a845b94c8f594cfbb1322dd90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e00971b0bd762cefeb8a002d1a9e3e488a8dfdb021a5fdef63af4cbdc5fb6be(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5beb74b9b5d19367475c397aeb621dc6df27aedd409695cf8fcea13c8292dd7e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdddf8d2f9258974b1fbc2a0e6bb1b64a365b9697443a51d1d2f014ee678b0d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6df622c173b92196d9a97ca71d682496be072d3ed33a6bc1d1db4407fc93467(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3695f86ebe8fca92d373a027f242130665a1687c1806eef2f09d4a08fb716b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4cb09ea1522c78f131db443d747404d0d735b3cf87278d66e0475f95a7c573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91ab0d4deb7954b149d4ff6c3a6876042eb071c67f50df8d81376176df9b0a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c606db2757362d544f823382cec0a66bab2e91a6b04eba8af3488a43e98b0a87(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60aff452089d7a23e8474473db0eb060ca095dbc73745fd48c24f1860c6133a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b6cf4c2cc75d3ba37e36294692eecc4c894829e88ba67e7e47eed7fce10cce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120fd092cf48ccaac62718b82237efc39bb91017f483b0bfffd998181b181c7f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a4a7eda183c5130e81b9432a1796ebae4210835e1ce614c4da7f7055490afb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c9b4498087af3b141807ca9044818209c22fbb64382533cbece38f08a491e7(
    value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegmentActions, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4302c7fcf2c21c6155b0f005f75674deec6c6ef6bd363fbd45c8498c7907b1d(
    *,
    name: builtins.str,
    allow_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    deny_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    edge_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    isolate_attachments: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_attachment_acceptance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21658477b720e3917ad992814d0d4420bec74754d3ea715a80e721ea9ce4226(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5facf9453ab0d6d1555f0edc491710c36a70f2150a2fc3c7f644aed79df52a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b234fa66f81b89ca64551411237c41981a2f50c5b12f7cc4a84462816f76d20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514a60d74bfeb05793dc470e48391b50626354e93233838b87365930d9924426(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb8aa645f38ed022a43f5dbdba35b03488b8025af708e1693d26948dbdbb012(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb661a39b2081b5884aa362296d23aef6355b7fb9f308cf5cf211914ecce5a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bf8ae8abf2d318d26c7e49cf344d22b7c04ae9f7a30b97e9142e1ff093e692(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7edf54165a440248f13578f449bf81ba80ce51266f3107a7cf495513a6c2716f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e3b263d43877c5ae982c1addc61eef1ce603f526079d43b5ff2f466bffc0da(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cbea8d517c3951006a8508541f68a83c70c5188254a8f10a555155c2750cf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8772060258723dce386e363de744b09a93597a7c6675e00b2637ec89a87a2a88(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57c6b0ddbe281408efaa289d52de9a96a6e7d70d7f3d677ea1dd867342bebd2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8c5298c836d065b55293b3d14111f7f443ccbb080a36d125ce112a2f05e53c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64ad1e8b3c3b56d42a53a8bfd8dbeaa2a18cb5f4fec6296c0c5b30a84f0b1ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479d69e7b6c83a6c4589b5f52a354428f92c4f9cddaa6f5b02b9a6083166a8ab(
    value: typing.Optional[typing.Union[DataAwsNetworkmanagerCoreNetworkPolicyDocumentSegments, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
