'''
# `aws_ce_cost_category`

Refer to the Terraform Registory for docs: [`aws_ce_cost_category`](https://www.terraform.io/docs/providers/aws/r/ce_cost_category).
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


class CeCostCategory(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategory",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category aws_ce_cost_category}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategoryRule", typing.Dict[builtins.str, typing.Any]]]],
        rule_version: builtins.str,
        default_value: typing.Optional[builtins.str] = None,
        effective_start: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        split_charge_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategorySplitChargeRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category aws_ce_cost_category} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#name CeCostCategory#name}.
        :param rule: rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#rule CeCostCategory#rule}
        :param rule_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#rule_version CeCostCategory#rule_version}.
        :param default_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#default_value CeCostCategory#default_value}.
        :param effective_start: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#effective_start CeCostCategory#effective_start}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#id CeCostCategory#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param split_charge_rule: split_charge_rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#split_charge_rule CeCostCategory#split_charge_rule}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags_all CeCostCategory#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca903bb7ad34af3622ebfd528487d1ff715c9fb1a1989688d33ceb2c9a6b8d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CeCostCategoryConfig(
            name=name,
            rule=rule,
            rule_version=rule_version,
            default_value=default_value,
            effective_start=effective_start,
            id=id,
            split_charge_rule=split_charge_rule,
            tags=tags,
            tags_all=tags_all,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategoryRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86920f21cd8ed679af2e450accb9943953924c6f6832ab66903f0b0b216abd91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="putSplitChargeRule")
    def put_split_charge_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategorySplitChargeRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e007d77781ef5b18e1ae58dfa9ad2db3dae3c9c99f09f63cdcdd2bd19b3244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSplitChargeRule", [value]))

    @jsii.member(jsii_name="resetDefaultValue")
    def reset_default_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultValue", []))

    @jsii.member(jsii_name="resetEffectiveStart")
    def reset_effective_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffectiveStart", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSplitChargeRule")
    def reset_split_charge_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSplitChargeRule", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="effectiveEnd")
    def effective_end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveEnd"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "CeCostCategoryRuleList":
        return typing.cast("CeCostCategoryRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="splitChargeRule")
    def split_charge_rule(self) -> "CeCostCategorySplitChargeRuleList":
        return typing.cast("CeCostCategorySplitChargeRuleList", jsii.get(self, "splitChargeRule"))

    @builtins.property
    @jsii.member(jsii_name="defaultValueInput")
    def default_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultValueInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveStartInput")
    def effective_start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectiveStartInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategoryRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategoryRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleVersionInput")
    def rule_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="splitChargeRuleInput")
    def split_charge_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategorySplitChargeRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategorySplitChargeRule"]]], jsii.get(self, "splitChargeRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultValue")
    def default_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultValue"))

    @default_value.setter
    def default_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e0595ae68d5b1dcd7eeda6df114ba9546944963aed455d5b30eed22f8675f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultValue", value)

    @builtins.property
    @jsii.member(jsii_name="effectiveStart")
    def effective_start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveStart"))

    @effective_start.setter
    def effective_start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d200d333f377435ae160cb1e5121694c4d5d69fa89cc1a15d5968a246ada63e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveStart", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d196460e2f03485f8051693aa44447697843d3f92900c3826061bd0aa7df43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2d624d22e20b89bca0b969e9c96b42346e8bddd7eadc5ef55dd0308a9d8fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="ruleVersion")
    def rule_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleVersion"))

    @rule_version.setter
    def rule_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c666dd29ce81ebfcfdd259274680d185d7e2bb936cccf33852675675af2e030e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleVersion", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__923f41ded42cd183e1ea776d7692e120dccccbc8d114c19eb42ee4e57de76c1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136a9af8d8ec1e3f3d35d5701635e68cb0a8283cca8664578d788de00ef5f2f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryConfig",
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
        "rule": "rule",
        "rule_version": "ruleVersion",
        "default_value": "defaultValue",
        "effective_start": "effectiveStart",
        "id": "id",
        "split_charge_rule": "splitChargeRule",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class CeCostCategoryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategoryRule", typing.Dict[builtins.str, typing.Any]]]],
        rule_version: builtins.str,
        default_value: typing.Optional[builtins.str] = None,
        effective_start: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        split_charge_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategorySplitChargeRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#name CeCostCategory#name}.
        :param rule: rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#rule CeCostCategory#rule}
        :param rule_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#rule_version CeCostCategory#rule_version}.
        :param default_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#default_value CeCostCategory#default_value}.
        :param effective_start: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#effective_start CeCostCategory#effective_start}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#id CeCostCategory#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param split_charge_rule: split_charge_rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#split_charge_rule CeCostCategory#split_charge_rule}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags_all CeCostCategory#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f4d662237fd4686b32bfb59c4d22ec4735c33d67ec7d0002cb5ad026c585c8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument rule_version", value=rule_version, expected_type=type_hints["rule_version"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            check_type(argname="argument effective_start", value=effective_start, expected_type=type_hints["effective_start"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument split_charge_rule", value=split_charge_rule, expected_type=type_hints["split_charge_rule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "rule": rule,
            "rule_version": rule_version,
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
        if default_value is not None:
            self._values["default_value"] = default_value
        if effective_start is not None:
            self._values["effective_start"] = effective_start
        if id is not None:
            self._values["id"] = id
        if split_charge_rule is not None:
            self._values["split_charge_rule"] = split_charge_rule
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#name CeCostCategory#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategoryRule"]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#rule CeCostCategory#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategoryRule"]], result)

    @builtins.property
    def rule_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#rule_version CeCostCategory#rule_version}.'''
        result = self._values.get("rule_version")
        assert result is not None, "Required property 'rule_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#default_value CeCostCategory#default_value}.'''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def effective_start(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#effective_start CeCostCategory#effective_start}.'''
        result = self._values.get("effective_start")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#id CeCostCategory#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def split_charge_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategorySplitChargeRule"]]]:
        '''split_charge_rule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#split_charge_rule CeCostCategory#split_charge_rule}
        '''
        result = self._values.get("split_charge_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategorySplitChargeRule"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags_all CeCostCategory#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRule",
    jsii_struct_bases=[],
    name_mapping={
        "inherited_value": "inheritedValue",
        "rule": "rule",
        "type": "type",
        "value": "value",
    },
)
class CeCostCategoryRule:
    def __init__(
        self,
        *,
        inherited_value: typing.Optional[typing.Union["CeCostCategoryRuleInheritedValue", typing.Dict[builtins.str, typing.Any]]] = None,
        rule: typing.Optional[typing.Union["CeCostCategoryRuleRule", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inherited_value: inherited_value block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#inherited_value CeCostCategory#inherited_value}
        :param rule: rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#rule CeCostCategory#rule}
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#type CeCostCategory#type}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#value CeCostCategory#value}.
        '''
        if isinstance(inherited_value, dict):
            inherited_value = CeCostCategoryRuleInheritedValue(**inherited_value)
        if isinstance(rule, dict):
            rule = CeCostCategoryRuleRule(**rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81464be801c1eed01907e941fed52ac7ca6158120baa3fddd298fe4a4966e149)
            check_type(argname="argument inherited_value", value=inherited_value, expected_type=type_hints["inherited_value"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inherited_value is not None:
            self._values["inherited_value"] = inherited_value
        if rule is not None:
            self._values["rule"] = rule
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def inherited_value(self) -> typing.Optional["CeCostCategoryRuleInheritedValue"]:
        '''inherited_value block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#inherited_value CeCostCategory#inherited_value}
        '''
        result = self._values.get("inherited_value")
        return typing.cast(typing.Optional["CeCostCategoryRuleInheritedValue"], result)

    @builtins.property
    def rule(self) -> typing.Optional["CeCostCategoryRuleRule"]:
        '''rule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#rule CeCostCategory#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional["CeCostCategoryRuleRule"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#type CeCostCategory#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#value CeCostCategory#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleInheritedValue",
    jsii_struct_bases=[],
    name_mapping={"dimension_key": "dimensionKey", "dimension_name": "dimensionName"},
)
class CeCostCategoryRuleInheritedValue:
    def __init__(
        self,
        *,
        dimension_key: typing.Optional[builtins.str] = None,
        dimension_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dimension_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension_key CeCostCategory#dimension_key}.
        :param dimension_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension_name CeCostCategory#dimension_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d879549216b38dee5b4d152e5537fbb5a899bc01b7ac22231f384ad40e0d1f1)
            check_type(argname="argument dimension_key", value=dimension_key, expected_type=type_hints["dimension_key"])
            check_type(argname="argument dimension_name", value=dimension_name, expected_type=type_hints["dimension_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dimension_key is not None:
            self._values["dimension_key"] = dimension_key
        if dimension_name is not None:
            self._values["dimension_name"] = dimension_name

    @builtins.property
    def dimension_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension_key CeCostCategory#dimension_key}.'''
        result = self._values.get("dimension_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dimension_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension_name CeCostCategory#dimension_name}.'''
        result = self._values.get("dimension_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleInheritedValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleInheritedValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleInheritedValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__345dd2ca950ae81c202fa3d5946820c934dbfa5d4221035fafb56fced4519f25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDimensionKey")
    def reset_dimension_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimensionKey", []))

    @jsii.member(jsii_name="resetDimensionName")
    def reset_dimension_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimensionName", []))

    @builtins.property
    @jsii.member(jsii_name="dimensionKeyInput")
    def dimension_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dimensionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionNameInput")
    def dimension_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dimensionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionKey")
    def dimension_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dimensionKey"))

    @dimension_key.setter
    def dimension_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a02e73938d00007ffc80bfe49a314f7430c6d84504ed900ae0aec35cef055d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensionKey", value)

    @builtins.property
    @jsii.member(jsii_name="dimensionName")
    def dimension_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dimensionName"))

    @dimension_name.setter
    def dimension_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bfbb1381db0612b8093d1546eca93d42cb1d45f90ecf5349d184140439db4df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensionName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleInheritedValue]:
        return typing.cast(typing.Optional[CeCostCategoryRuleInheritedValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleInheritedValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34600a1a01d7b532849053f8d92e998d42f5107eb02b8da702acf20f2f2a5b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CeCostCategoryRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ba55b96b46e3ad4c854a04f8b66b107ece6fb1317da701b5b39d1dca5d08e79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CeCostCategoryRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e143a66436d8304d5801e5adc035c0cbe024d5ac6b080eb4d4d23dcbcafc90d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CeCostCategoryRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead26ae2a3b6c047ed66435351ec4d7c13b6cb224616e0352cc743faa3e8ca96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__275881d410b02674471343636079d0ac1aee1e3018ada46091d46a08eafb4a1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a1e23d84eb8ea2f430e438831d1d12cbdc4fbb770164378453ed74a8e838dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe85d09cfd2e2a94983aface9fe6d830ce8af89f3906b0e6f64ab965264ed72b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CeCostCategoryRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d22c33e827b1c29ab07a889c945efb609b070e9906ba8a6799dd5c28e204613b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInheritedValue")
    def put_inherited_value(
        self,
        *,
        dimension_key: typing.Optional[builtins.str] = None,
        dimension_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dimension_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension_key CeCostCategory#dimension_key}.
        :param dimension_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension_name CeCostCategory#dimension_name}.
        '''
        value = CeCostCategoryRuleInheritedValue(
            dimension_key=dimension_key, dimension_name=dimension_name
        )

        return typing.cast(None, jsii.invoke(self, "putInheritedValue", [value]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategoryRuleRuleAnd", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cost_category: typing.Optional[typing.Union["CeCostCategoryRuleRuleCostCategory", typing.Dict[builtins.str, typing.Any]]] = None,
        dimension: typing.Optional[typing.Union["CeCostCategoryRuleRuleDimension", typing.Dict[builtins.str, typing.Any]]] = None,
        not_: typing.Optional[typing.Union["CeCostCategoryRuleRuleNot", typing.Dict[builtins.str, typing.Any]]] = None,
        or_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategoryRuleRuleOr", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Union["CeCostCategoryRuleRuleTags", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#and CeCostCategory#and}
        :param cost_category: cost_category block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#cost_category CeCostCategory#cost_category}
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension CeCostCategory#dimension}
        :param not_: not block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#not CeCostCategory#not}
        :param or_: or block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#or CeCostCategory#or}
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}
        '''
        value = CeCostCategoryRuleRule(
            and_=and_,
            cost_category=cost_category,
            dimension=dimension,
            not_=not_,
            or_=or_,
            tags=tags,
        )

        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetInheritedValue")
    def reset_inherited_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInheritedValue", []))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="inheritedValue")
    def inherited_value(self) -> CeCostCategoryRuleInheritedValueOutputReference:
        return typing.cast(CeCostCategoryRuleInheritedValueOutputReference, jsii.get(self, "inheritedValue"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "CeCostCategoryRuleRuleOutputReference":
        return typing.cast("CeCostCategoryRuleRuleOutputReference", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="inheritedValueInput")
    def inherited_value_input(
        self,
    ) -> typing.Optional[CeCostCategoryRuleInheritedValue]:
        return typing.cast(typing.Optional[CeCostCategoryRuleInheritedValue], jsii.get(self, "inheritedValueInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(self) -> typing.Optional["CeCostCategoryRuleRule"]:
        return typing.cast(typing.Optional["CeCostCategoryRuleRule"], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3c32b73baa1b2a624d00e2ff6fc1f7c4e78d0a0c11ca9188c2b0c29dd693ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e4a28e1c3aaa0551dfb6592c887d1a0bb5e4ae2d23ee468baff9839b8b45ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CeCostCategoryRule, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CeCostCategoryRule, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CeCostCategoryRule, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d8b5479cd2bc65b614de06939794b103e01c1e8251b0d0f3d14c18a5ffd415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRule",
    jsii_struct_bases=[],
    name_mapping={
        "and_": "and",
        "cost_category": "costCategory",
        "dimension": "dimension",
        "not_": "not",
        "or_": "or",
        "tags": "tags",
    },
)
class CeCostCategoryRuleRule:
    def __init__(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategoryRuleRuleAnd", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cost_category: typing.Optional[typing.Union["CeCostCategoryRuleRuleCostCategory", typing.Dict[builtins.str, typing.Any]]] = None,
        dimension: typing.Optional[typing.Union["CeCostCategoryRuleRuleDimension", typing.Dict[builtins.str, typing.Any]]] = None,
        not_: typing.Optional[typing.Union["CeCostCategoryRuleRuleNot", typing.Dict[builtins.str, typing.Any]]] = None,
        or_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategoryRuleRuleOr", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Union["CeCostCategoryRuleRuleTags", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#and CeCostCategory#and}
        :param cost_category: cost_category block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#cost_category CeCostCategory#cost_category}
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension CeCostCategory#dimension}
        :param not_: not block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#not CeCostCategory#not}
        :param or_: or block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#or CeCostCategory#or}
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}
        '''
        if isinstance(cost_category, dict):
            cost_category = CeCostCategoryRuleRuleCostCategory(**cost_category)
        if isinstance(dimension, dict):
            dimension = CeCostCategoryRuleRuleDimension(**dimension)
        if isinstance(not_, dict):
            not_ = CeCostCategoryRuleRuleNot(**not_)
        if isinstance(tags, dict):
            tags = CeCostCategoryRuleRuleTags(**tags)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1382d024a5cf3e63e423103a2c6b0aaf4fbd13ef5f6ddd454dcc5934dbe7dd0b)
            check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
            check_type(argname="argument cost_category", value=cost_category, expected_type=type_hints["cost_category"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument not_", value=not_, expected_type=type_hints["not_"])
            check_type(argname="argument or_", value=or_, expected_type=type_hints["or_"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if and_ is not None:
            self._values["and_"] = and_
        if cost_category is not None:
            self._values["cost_category"] = cost_category
        if dimension is not None:
            self._values["dimension"] = dimension
        if not_ is not None:
            self._values["not_"] = not_
        if or_ is not None:
            self._values["or_"] = or_
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def and_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategoryRuleRuleAnd"]]]:
        '''and block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#and CeCostCategory#and}
        '''
        result = self._values.get("and_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategoryRuleRuleAnd"]]], result)

    @builtins.property
    def cost_category(self) -> typing.Optional["CeCostCategoryRuleRuleCostCategory"]:
        '''cost_category block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#cost_category CeCostCategory#cost_category}
        '''
        result = self._values.get("cost_category")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleCostCategory"], result)

    @builtins.property
    def dimension(self) -> typing.Optional["CeCostCategoryRuleRuleDimension"]:
        '''dimension block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension CeCostCategory#dimension}
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleDimension"], result)

    @builtins.property
    def not_(self) -> typing.Optional["CeCostCategoryRuleRuleNot"]:
        '''not block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#not CeCostCategory#not}
        '''
        result = self._values.get("not_")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleNot"], result)

    @builtins.property
    def or_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategoryRuleRuleOr"]]]:
        '''or block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#or CeCostCategory#or}
        '''
        result = self._values.get("or_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategoryRuleRuleOr"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional["CeCostCategoryRuleRuleTags"]:
        '''tags block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleTags"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleAnd",
    jsii_struct_bases=[],
    name_mapping={
        "cost_category": "costCategory",
        "dimension": "dimension",
        "tags": "tags",
    },
)
class CeCostCategoryRuleRuleAnd:
    def __init__(
        self,
        *,
        cost_category: typing.Optional[typing.Union["CeCostCategoryRuleRuleAndCostCategory", typing.Dict[builtins.str, typing.Any]]] = None,
        dimension: typing.Optional[typing.Union["CeCostCategoryRuleRuleAndDimension", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Union["CeCostCategoryRuleRuleAndTags", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cost_category: cost_category block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#cost_category CeCostCategory#cost_category}
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension CeCostCategory#dimension}
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}
        '''
        if isinstance(cost_category, dict):
            cost_category = CeCostCategoryRuleRuleAndCostCategory(**cost_category)
        if isinstance(dimension, dict):
            dimension = CeCostCategoryRuleRuleAndDimension(**dimension)
        if isinstance(tags, dict):
            tags = CeCostCategoryRuleRuleAndTags(**tags)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a826bfc5e8068f94ceb06e69603b03d05aeb694b98e8aec4f13b9e96fe031173)
            check_type(argname="argument cost_category", value=cost_category, expected_type=type_hints["cost_category"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cost_category is not None:
            self._values["cost_category"] = cost_category
        if dimension is not None:
            self._values["dimension"] = dimension
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cost_category(self) -> typing.Optional["CeCostCategoryRuleRuleAndCostCategory"]:
        '''cost_category block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#cost_category CeCostCategory#cost_category}
        '''
        result = self._values.get("cost_category")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleAndCostCategory"], result)

    @builtins.property
    def dimension(self) -> typing.Optional["CeCostCategoryRuleRuleAndDimension"]:
        '''dimension block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension CeCostCategory#dimension}
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleAndDimension"], result)

    @builtins.property
    def tags(self) -> typing.Optional["CeCostCategoryRuleRuleAndTags"]:
        '''tags block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleAndTags"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleAnd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleAndCostCategory",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleAndCostCategory:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693ebd54dd0c6a188a93315e7fd2384dcaeb6d6b28c03e13a9f86a62a186d35f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleAndCostCategory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleAndCostCategoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleAndCostCategoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__610ddf7ec5eefefc5f63d1f8cd34943f3ae9275ac51d0d6517d27ca5ad3fa2c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f086dfa7f4f6ae39dd2d1062d6d658a5f9fd49388ad5fc7863aa27be4bc67114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf3e1d7f49a432d1d6284a494991b658c756b2b7ec5ffccabe3e722974e8c4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f9978e4e4d23f7db72a87b8ece9aa24e5daa7cb6e9bd08e7466c2192b6d5fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleAndCostCategory]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleAndCostCategory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleAndCostCategory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd7f4d4dcbfabb4c544281a63825467d1ea3500183762c0959b5840172c3d39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleAndDimension",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleAndDimension:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248eda79c8c00f0767325544ba1b3d141be206555d863a847fdd152a400bc3a0)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleAndDimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleAndDimensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleAndDimensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__198d3d5a3aa7d9ea8958a416826ebf9d7b3571d8cbcbd33bed9862fa21775025)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d77d7a78ca5a06e18fc0fbbe3a0c6de59f266be1ce586bcadfb4388ebd9765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8aaec3588282293c5888be6e70de5b53dc8a4f9da20e256981e06d427f3470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b704007be813ea10ae5b54bcdfc49c7b38249e50ab7ae899129dbfbbfa25b1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleAndDimension]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleAndDimension], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleAndDimension],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2219d4c0889afb41875fdcb2c70348409d081b2ea8b2ffb44f8a8ad6541e4109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CeCostCategoryRuleRuleAndList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleAndList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6b54d15dda0fdb97af8a906781a6776ac38238195611c95129fb40aca71cde2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CeCostCategoryRuleRuleAndOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada196453dd83f291de6d4420ca81fb1e36c0c28f37bee93545096624d74bd2c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CeCostCategoryRuleRuleAndOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bedf5e90f0c23151ebb84856cd9cd8320b71fe138ca45b345fbecd1f9b9dd9d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__531148d8de24351b54620f02f5b3fba327f81f5450338c87189ea58de7683580)
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
            type_hints = typing.get_type_hints(_typecheckingstub__893323bd3ebedeb76fbd68c5b33791ade46e1bae304450976f60284721d853c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleAnd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleAnd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78306587216b105de76bb202379cb7af6acc89159bde030beb3e11f8c846c8da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CeCostCategoryRuleRuleAndOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleAndOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cc877610e1ed320d59472b6eed08deea07db7725ec8bff54a2d5273ff80a12f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCostCategory")
    def put_cost_category(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleAndCostCategory(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putCostCategory", [value]))

    @jsii.member(jsii_name="putDimension")
    def put_dimension(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleAndDimension(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putDimension", [value]))

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleAndTags(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="resetCostCategory")
    def reset_cost_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostCategory", []))

    @jsii.member(jsii_name="resetDimension")
    def reset_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimension", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="costCategory")
    def cost_category(self) -> CeCostCategoryRuleRuleAndCostCategoryOutputReference:
        return typing.cast(CeCostCategoryRuleRuleAndCostCategoryOutputReference, jsii.get(self, "costCategory"))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> CeCostCategoryRuleRuleAndDimensionOutputReference:
        return typing.cast(CeCostCategoryRuleRuleAndDimensionOutputReference, jsii.get(self, "dimension"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "CeCostCategoryRuleRuleAndTagsOutputReference":
        return typing.cast("CeCostCategoryRuleRuleAndTagsOutputReference", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="costCategoryInput")
    def cost_category_input(
        self,
    ) -> typing.Optional[CeCostCategoryRuleRuleAndCostCategory]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleAndCostCategory], jsii.get(self, "costCategoryInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(self) -> typing.Optional[CeCostCategoryRuleRuleAndDimension]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleAndDimension], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional["CeCostCategoryRuleRuleAndTags"]:
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleAndTags"], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CeCostCategoryRuleRuleAnd, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CeCostCategoryRuleRuleAnd, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CeCostCategoryRuleRuleAnd, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d2a704409d05ca1870408da92ed3a21c6a603e42cf1cc747988ef905882dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleAndTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleAndTags:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4229c1a54d2b3ab6cdee7acf9ae6b012245de3cb2f8e2aa83b509c4390315950)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleAndTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleAndTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleAndTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ba917470a0fa6b045de5cd0e88e23625ad656585c1ec4a63efaac4c8b38f842)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d01418af70102df9faac638995f9f6c91db85537d2f4d4a35a66fd1802d42910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6392b760d5cd7d6953c988bf9d686111afbb3384024111fd839cda23ca4c5fb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167987fc643ca85ca2b7066af5310b585b513dd2acd56aed65831a3f2136d5b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleAndTags]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleAndTags], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleAndTags],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1483c10a70d79470bbe6747d3a441f71579bd51f0e0b5754a45a3659658e7677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleCostCategory",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleCostCategory:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ecb408659afebfedd52145599269b62985e173f0b7f906b3b5ee25f9453f7a)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleCostCategory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleCostCategoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleCostCategoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31ce47394aa4de2a70037069ce67f135106e5714747364dda6f44a3d9f3356bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225ee701497d1d8ad1ff5285f7088f3cce12a466fdc6cc2f2091db1197c07728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa64f4e0a2b40724b4d3ff1fb4c022fdbe9168a85f1ae63e0e29d2886a5a7dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541ebe1dcc136aafd3fea2128d81d2659b3538f341a01dcb69514aa8cf944824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleCostCategory]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleCostCategory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleCostCategory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af38f606444da62047e9eb9ac2fc10612c8b525e462f105af1f90250be4c2735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleDimension",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleDimension:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2edee190bc1788b7be1c1a2b966fec6a8a624a55bacdecf7a91685c31baada37)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleDimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleDimensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleDimensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4eca606391ab8a234de91919c669fa452f62aad0c2ca2f62b831908069f2c6d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48f7b9b0e90e80e37a4b0a2388cdcee1a5a7f22a89b4e04a294c4f2422e251c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2413a66a3f916812010cfa7df415e9c3e76a4a60ae408aa46348ab20acd3af1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebbafa594a632d8e2acccc8c0ee880f272f41fe46feade370614ba00d19e5a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleDimension]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleDimension], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleDimension],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511d4ebe6a2ee17066ab0bda4f29b85c6b2e85fbbe2699e5a904ef10edcb5ae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleNot",
    jsii_struct_bases=[],
    name_mapping={
        "cost_category": "costCategory",
        "dimension": "dimension",
        "tags": "tags",
    },
)
class CeCostCategoryRuleRuleNot:
    def __init__(
        self,
        *,
        cost_category: typing.Optional[typing.Union["CeCostCategoryRuleRuleNotCostCategory", typing.Dict[builtins.str, typing.Any]]] = None,
        dimension: typing.Optional[typing.Union["CeCostCategoryRuleRuleNotDimension", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Union["CeCostCategoryRuleRuleNotTags", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cost_category: cost_category block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#cost_category CeCostCategory#cost_category}
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension CeCostCategory#dimension}
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}
        '''
        if isinstance(cost_category, dict):
            cost_category = CeCostCategoryRuleRuleNotCostCategory(**cost_category)
        if isinstance(dimension, dict):
            dimension = CeCostCategoryRuleRuleNotDimension(**dimension)
        if isinstance(tags, dict):
            tags = CeCostCategoryRuleRuleNotTags(**tags)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8515ab75bf8d429b3b1d8bc0ca32957491ac8b6856d4659c4efd7bc3c751a75)
            check_type(argname="argument cost_category", value=cost_category, expected_type=type_hints["cost_category"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cost_category is not None:
            self._values["cost_category"] = cost_category
        if dimension is not None:
            self._values["dimension"] = dimension
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cost_category(self) -> typing.Optional["CeCostCategoryRuleRuleNotCostCategory"]:
        '''cost_category block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#cost_category CeCostCategory#cost_category}
        '''
        result = self._values.get("cost_category")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleNotCostCategory"], result)

    @builtins.property
    def dimension(self) -> typing.Optional["CeCostCategoryRuleRuleNotDimension"]:
        '''dimension block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension CeCostCategory#dimension}
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleNotDimension"], result)

    @builtins.property
    def tags(self) -> typing.Optional["CeCostCategoryRuleRuleNotTags"]:
        '''tags block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleNotTags"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleNot(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleNotCostCategory",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleNotCostCategory:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab28c78999f895e0c64fd1513e398c97d3c625221b519e1f78b84ebbf95989e9)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleNotCostCategory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleNotCostCategoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleNotCostCategoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e38d2cdc2f2b2b5d75ff6193a1f87a753e5984013f8f62fa66547f42be45d4cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d126c9075a0d41cd0b401872c64e1d80376fc6db077227bb719edb67b8b473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30289081daf9d14465342ee8862bf02579cdfac4e6e060c34d397ecd41a2ae06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e78db6a3eeaf20f9d3e89a1d28fd132ba67d6f504c451c9c237a1ac974c7bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleNotCostCategory]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleNotCostCategory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleNotCostCategory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a1728928ef44429bd9ca02cb3ce35f5baaed275308b61a9c0b40bbe5ebc012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleNotDimension",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleNotDimension:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66193d4c3177be998864e1bd8f593ace5d7182a1d4cdd796b208696d58b7ad85)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleNotDimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleNotDimensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleNotDimensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3539942eb1441fb2617fc6c3b499b1ee943d7433723ea2ecb9d4d3522759dc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30fb25cdda9af1193a6588892e5b41bc25021fedb9bcb4a5c75afae579da380f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af6baed3de59850ea650dee472d1faa8d5138ee1ffb3e3da4a31663e0e07f10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc91d261f4623940a39dbd5d3128d918fe6c09afc25b5f3a2d4b50538eafa2b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleNotDimension]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleNotDimension], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleNotDimension],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d26bc3ce4e8640270c61aa907197e4417bb38724ecc996090a7b0a0ab9d6525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CeCostCategoryRuleRuleNotOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleNotOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f6c53d0bcdc0247fc098e55c920d02213aca81e24addebb0476111472077996)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCostCategory")
    def put_cost_category(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleNotCostCategory(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putCostCategory", [value]))

    @jsii.member(jsii_name="putDimension")
    def put_dimension(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleNotDimension(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putDimension", [value]))

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleNotTags(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="resetCostCategory")
    def reset_cost_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostCategory", []))

    @jsii.member(jsii_name="resetDimension")
    def reset_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimension", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="costCategory")
    def cost_category(self) -> CeCostCategoryRuleRuleNotCostCategoryOutputReference:
        return typing.cast(CeCostCategoryRuleRuleNotCostCategoryOutputReference, jsii.get(self, "costCategory"))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> CeCostCategoryRuleRuleNotDimensionOutputReference:
        return typing.cast(CeCostCategoryRuleRuleNotDimensionOutputReference, jsii.get(self, "dimension"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "CeCostCategoryRuleRuleNotTagsOutputReference":
        return typing.cast("CeCostCategoryRuleRuleNotTagsOutputReference", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="costCategoryInput")
    def cost_category_input(
        self,
    ) -> typing.Optional[CeCostCategoryRuleRuleNotCostCategory]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleNotCostCategory], jsii.get(self, "costCategoryInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(self) -> typing.Optional[CeCostCategoryRuleRuleNotDimension]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleNotDimension], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional["CeCostCategoryRuleRuleNotTags"]:
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleNotTags"], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleNot]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleNot], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CeCostCategoryRuleRuleNot]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca18de625a87cca395a65a9b8593a01d8ddbb9cc5ba82d981ed3a2d41c09c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleNotTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleNotTags:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43895437dd520f74c895982a104462b5224ec2813b79d0947b4e01ef89c7beb4)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleNotTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleNotTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleNotTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cde3c1c66089cb77ecd2f2d158120907b488773b5b91fdc79c1164e78e252ab8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecdbff7c383bc3ea44c7643173dd74f812d30cd4693b4481d16e09b9a85812a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e64cc4c9b835e80599006431d3cc3d277389356fb91d93a1e581a0c8b94aab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0050b3ab50038efd164fb2ee20bb9b13017aabce9579e190d2d2a49e648db9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleNotTags]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleNotTags], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleNotTags],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de3b665ca5cfd9c9f2eed8298d056aa2430ab230ebbfad4489657977edeaaa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleOr",
    jsii_struct_bases=[],
    name_mapping={
        "cost_category": "costCategory",
        "dimension": "dimension",
        "tags": "tags",
    },
)
class CeCostCategoryRuleRuleOr:
    def __init__(
        self,
        *,
        cost_category: typing.Optional[typing.Union["CeCostCategoryRuleRuleOrCostCategory", typing.Dict[builtins.str, typing.Any]]] = None,
        dimension: typing.Optional[typing.Union["CeCostCategoryRuleRuleOrDimension", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Union["CeCostCategoryRuleRuleOrTags", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cost_category: cost_category block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#cost_category CeCostCategory#cost_category}
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension CeCostCategory#dimension}
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}
        '''
        if isinstance(cost_category, dict):
            cost_category = CeCostCategoryRuleRuleOrCostCategory(**cost_category)
        if isinstance(dimension, dict):
            dimension = CeCostCategoryRuleRuleOrDimension(**dimension)
        if isinstance(tags, dict):
            tags = CeCostCategoryRuleRuleOrTags(**tags)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10af28b0edda8039dfa47eaca979cb39be25c44340facbeedab0b4f50de0efa)
            check_type(argname="argument cost_category", value=cost_category, expected_type=type_hints["cost_category"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cost_category is not None:
            self._values["cost_category"] = cost_category
        if dimension is not None:
            self._values["dimension"] = dimension
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cost_category(self) -> typing.Optional["CeCostCategoryRuleRuleOrCostCategory"]:
        '''cost_category block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#cost_category CeCostCategory#cost_category}
        '''
        result = self._values.get("cost_category")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleOrCostCategory"], result)

    @builtins.property
    def dimension(self) -> typing.Optional["CeCostCategoryRuleRuleOrDimension"]:
        '''dimension block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension CeCostCategory#dimension}
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleOrDimension"], result)

    @builtins.property
    def tags(self) -> typing.Optional["CeCostCategoryRuleRuleOrTags"]:
        '''tags block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleOrTags"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleOr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleOrCostCategory",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleOrCostCategory:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8e12393dd787f22cabd9deeea1f6306cb6a4c41669c1a8eb80613e7c13c9c2)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleOrCostCategory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleOrCostCategoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleOrCostCategoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77fb70e87a3a5d4075a31e765a3316c105238bb32397cd6700c17a5548047a24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c51912368a8868489ce7add6aab75605a287279c4666bb19ada423b50d6f5e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36888bc6c6a8ebbac1a890b8d598401be945bf0e5d1654e1299a32b9ce6fe93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__addc6291eafebcb8541e0534fe473156499744612338256f9704a6e4cb1bc364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleOrCostCategory]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleOrCostCategory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleOrCostCategory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd05f272493a418abcd30b80e6fd987dbc92405b91c4a163946bd1ba01143a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleOrDimension",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleOrDimension:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20619a1018ab990799d867d95d58196d6cd908dd36f2c7a937acc7bcbc50a23)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleOrDimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleOrDimensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleOrDimensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6571ac3187f13ca62ef45e029e04e4a4d58cb57a1c6a8e88a1edc74b4bd0c0c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0fe04fa74c8d48e3f6c8559be84002911f998360d8fdb76ce6b7d40c9011b0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03fb930a56d4423b803f6ca7f78d2eba75559eb297b873b2cb67df67406cd325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9e19f7ae74d9214676922ce9863854b3a8e4860393681ecdb86a2cccd725d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleOrDimension]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleOrDimension], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleOrDimension],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af71369c6bcda0b54de1a7f53a50cb523ab403abb721f612858a2fe7079634b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CeCostCategoryRuleRuleOrList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleOrList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc32ee6b21a41a976172f477579c0e3d1f4bfdd0c09bf7358ead8ef3da7f9711)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CeCostCategoryRuleRuleOrOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa3c2817535f106227249305e757ef8818f998e0c0d11e38627d2bc85b7fb48)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CeCostCategoryRuleRuleOrOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9bc570949807c45dd10f5ef85a3765928a6ae3516c47161756db74db5a39fca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34dd661cace7f682f1b4e17f1af0dfefbbaae47fede0176adb585973d695b593)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7953f1144c96acc6bc0d841b182bdd1a092cba7477c06ffc9ba5d1c19eeab128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleOr]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleOr]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleOr]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836350224c4964104f7a59b5d2621f754f7ec0f7916f33e2476ca4ea671ad104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CeCostCategoryRuleRuleOrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleOrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54e54489281a9877000c7174af0d02e5d92057ad8e5099901ab70470fb71fdab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCostCategory")
    def put_cost_category(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleOrCostCategory(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putCostCategory", [value]))

    @jsii.member(jsii_name="putDimension")
    def put_dimension(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleOrDimension(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putDimension", [value]))

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleOrTags(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="resetCostCategory")
    def reset_cost_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostCategory", []))

    @jsii.member(jsii_name="resetDimension")
    def reset_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimension", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="costCategory")
    def cost_category(self) -> CeCostCategoryRuleRuleOrCostCategoryOutputReference:
        return typing.cast(CeCostCategoryRuleRuleOrCostCategoryOutputReference, jsii.get(self, "costCategory"))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> CeCostCategoryRuleRuleOrDimensionOutputReference:
        return typing.cast(CeCostCategoryRuleRuleOrDimensionOutputReference, jsii.get(self, "dimension"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "CeCostCategoryRuleRuleOrTagsOutputReference":
        return typing.cast("CeCostCategoryRuleRuleOrTagsOutputReference", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="costCategoryInput")
    def cost_category_input(
        self,
    ) -> typing.Optional[CeCostCategoryRuleRuleOrCostCategory]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleOrCostCategory], jsii.get(self, "costCategoryInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(self) -> typing.Optional[CeCostCategoryRuleRuleOrDimension]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleOrDimension], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional["CeCostCategoryRuleRuleOrTags"]:
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleOrTags"], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CeCostCategoryRuleRuleOr, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CeCostCategoryRuleRuleOr, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CeCostCategoryRuleRuleOr, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8906b05660a51f1d882b1d003b997754b833d5287e6c311cc000e9dc8dc581)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleOrTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleOrTags:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188783368c97562e89d106c61c05393b8f9b3ba8ff48f7a139d85d3a75bfce38)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleOrTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleOrTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleOrTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3f77e07096bf57793fac370a7b4ef7748a3ffd15c77f7a7dd26e1efe2700616)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4922e0f18b94719a8c954bf4fad76510e1d99110a63da3b2020432913381d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1920cd40fd20f91d3793e1560271974b5960f7d8168046849d4e9c514da0bcb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ad2e061d2223794cac04a5a97d55e31df2b4156ef6b80ee1767aa073a29319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleOrTags]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleOrTags], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleOrTags],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303fad7dc0e98ec9f806623b4f15055a8a1fda98f2ee9dcbaaff2289c3c9c322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CeCostCategoryRuleRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e64907bf4650a800e89ed0f3a01bfc7d87d7f2ba7e3c98010b5ec95c99f1a88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnd")
    def put_and(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategoryRuleRuleAnd, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10ec911de9d2c6c82907105bd9bf2afe76613904087224db8c7b96f9d25fc5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnd", [value]))

    @jsii.member(jsii_name="putCostCategory")
    def put_cost_category(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleCostCategory(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putCostCategory", [value]))

    @jsii.member(jsii_name="putDimension")
    def put_dimension(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleDimension(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putDimension", [value]))

    @jsii.member(jsii_name="putNot")
    def put_not(
        self,
        *,
        cost_category: typing.Optional[typing.Union[CeCostCategoryRuleRuleNotCostCategory, typing.Dict[builtins.str, typing.Any]]] = None,
        dimension: typing.Optional[typing.Union[CeCostCategoryRuleRuleNotDimension, typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Union[CeCostCategoryRuleRuleNotTags, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cost_category: cost_category block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#cost_category CeCostCategory#cost_category}
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#dimension CeCostCategory#dimension}
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#tags CeCostCategory#tags}
        '''
        value = CeCostCategoryRuleRuleNot(
            cost_category=cost_category, dimension=dimension, tags=tags
        )

        return typing.cast(None, jsii.invoke(self, "putNot", [value]))

    @jsii.member(jsii_name="putOr")
    def put_or(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategoryRuleRuleOr, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d88819b793baad54bd9ebcecdb3495ec971c821bb7f311e4ba0e377d5dec53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOr", [value]))

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        value = CeCostCategoryRuleRuleTags(
            key=key, match_options=match_options, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="resetAnd")
    def reset_and(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnd", []))

    @jsii.member(jsii_name="resetCostCategory")
    def reset_cost_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostCategory", []))

    @jsii.member(jsii_name="resetDimension")
    def reset_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimension", []))

    @jsii.member(jsii_name="resetNot")
    def reset_not(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNot", []))

    @jsii.member(jsii_name="resetOr")
    def reset_or(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOr", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="and")
    def and_(self) -> CeCostCategoryRuleRuleAndList:
        return typing.cast(CeCostCategoryRuleRuleAndList, jsii.get(self, "and"))

    @builtins.property
    @jsii.member(jsii_name="costCategory")
    def cost_category(self) -> CeCostCategoryRuleRuleCostCategoryOutputReference:
        return typing.cast(CeCostCategoryRuleRuleCostCategoryOutputReference, jsii.get(self, "costCategory"))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> CeCostCategoryRuleRuleDimensionOutputReference:
        return typing.cast(CeCostCategoryRuleRuleDimensionOutputReference, jsii.get(self, "dimension"))

    @builtins.property
    @jsii.member(jsii_name="not")
    def not_(self) -> CeCostCategoryRuleRuleNotOutputReference:
        return typing.cast(CeCostCategoryRuleRuleNotOutputReference, jsii.get(self, "not"))

    @builtins.property
    @jsii.member(jsii_name="or")
    def or_(self) -> CeCostCategoryRuleRuleOrList:
        return typing.cast(CeCostCategoryRuleRuleOrList, jsii.get(self, "or"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "CeCostCategoryRuleRuleTagsOutputReference":
        return typing.cast("CeCostCategoryRuleRuleTagsOutputReference", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="andInput")
    def and_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleAnd]]], jsii.get(self, "andInput"))

    @builtins.property
    @jsii.member(jsii_name="costCategoryInput")
    def cost_category_input(
        self,
    ) -> typing.Optional[CeCostCategoryRuleRuleCostCategory]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleCostCategory], jsii.get(self, "costCategoryInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(self) -> typing.Optional[CeCostCategoryRuleRuleDimension]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleDimension], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="notInput")
    def not_input(self) -> typing.Optional[CeCostCategoryRuleRuleNot]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleNot], jsii.get(self, "notInput"))

    @builtins.property
    @jsii.member(jsii_name="orInput")
    def or_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleOr]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleOr]]], jsii.get(self, "orInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional["CeCostCategoryRuleRuleTags"]:
        return typing.cast(typing.Optional["CeCostCategoryRuleRuleTags"], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRule]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CeCostCategoryRuleRule]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1365c4e9b5a5849a31434743e4c13f031c98a77b96c3acf5deab25b4ee960e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "match_options": "matchOptions", "values": "values"},
)
class CeCostCategoryRuleRuleTags:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.
        :param match_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21897034ad168c58444ef560a442af862fb67fdd82fecce28037d598ddd16e7e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if match_options is not None:
            self._values["match_options"] = match_options
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#key CeCostCategory#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#match_options CeCostCategory#match_options}.'''
        result = self._values.get("match_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategoryRuleRuleTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategoryRuleRuleTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategoryRuleRuleTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed214a00c1790a6bf2d5f28bef40dcd7e490856a0dd191b53b77766340844a14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetMatchOptions")
    def reset_match_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchOptions", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchOptionsInput")
    def match_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "matchOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c82b1970cff2416b99af98c1a7bdd1b982bf6a861d66c50d770466dcb05d816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="matchOptions")
    def match_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "matchOptions"))

    @match_options.setter
    def match_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55be325fcd5cfb8992ed9ed3b0015ab49963910fb458e81a6a245b39ecb7e3f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchOptions", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8081781fe722291cd61407ea23bbcdd9456a7fdf1d0c7fc3058ae95c9e385b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CeCostCategoryRuleRuleTags]:
        return typing.cast(typing.Optional[CeCostCategoryRuleRuleTags], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CeCostCategoryRuleRuleTags],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3429a51b0060f94cfaf6af0d37ba0369856908b0f0afb90638a09cffd66662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategorySplitChargeRule",
    jsii_struct_bases=[],
    name_mapping={
        "method": "method",
        "source": "source",
        "targets": "targets",
        "parameter": "parameter",
    },
)
class CeCostCategorySplitChargeRule:
    def __init__(
        self,
        *,
        method: builtins.str,
        source: builtins.str,
        targets: typing.Sequence[builtins.str],
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategorySplitChargeRuleParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param method: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#method CeCostCategory#method}.
        :param source: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#source CeCostCategory#source}.
        :param targets: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#targets CeCostCategory#targets}.
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#parameter CeCostCategory#parameter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2acf5780c91ff56b2039951fddbbcd18217b16c656de07a26a1410a75346083e)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "method": method,
            "source": source,
            "targets": targets,
        }
        if parameter is not None:
            self._values["parameter"] = parameter

    @builtins.property
    def method(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#method CeCostCategory#method}.'''
        result = self._values.get("method")
        assert result is not None, "Required property 'method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#source CeCostCategory#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def targets(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#targets CeCostCategory#targets}.'''
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategorySplitChargeRuleParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#parameter CeCostCategory#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategorySplitChargeRuleParameter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategorySplitChargeRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategorySplitChargeRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategorySplitChargeRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d2fbc76b1d0c0d6796c8efa1eb1d0237a56c65fec4142e90cfdf1ea5d69abdd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CeCostCategorySplitChargeRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ab8fbbff4412d926c40b76d7b0fd46365f0133bf90637ff6399f788ebfb8d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CeCostCategorySplitChargeRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c2e44dcb11a26a1f14d1d58c54bedfb65331cd5c11ec7bbca6d45a0e1554f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3daf5b22e394d435878b2ab625c265000c02b8e90c9de298864fdb77d05e6aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d96010148c023cf777b385836b2b406279895e4e675a633c255979522f113a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategorySplitChargeRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategorySplitChargeRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategorySplitChargeRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc2678eaaa76b32678351a56f8bdb401738457cf5d29df99fc84a342388f305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CeCostCategorySplitChargeRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategorySplitChargeRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fab63de02eda2638c92a4dd46465cb1457ad7ce0fad4b694f11f991b1b71282)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CeCostCategorySplitChargeRuleParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf86ebb4273660798862be6d646308b85e2e9366519c4a115acf8f56c345f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameter", [value]))

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(self) -> "CeCostCategorySplitChargeRuleParameterList":
        return typing.cast("CeCostCategorySplitChargeRuleParameterList", jsii.get(self, "parameter"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategorySplitChargeRuleParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CeCostCategorySplitChargeRuleParameter"]]], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetsInput")
    def targets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetsInput"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e431301d69d64f96a55c5bd24c074bd3caba0b1a365603c5a25a215510de50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3327315722502d433ddb990ec55dd8631e3b3d9ee8ff5a8f09cdcfb3810ef5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targets"))

    @targets.setter
    def targets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62438b683098183ba71f2ac4fdd050345548fbb4a3c6e7c9b63d2ac677523e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targets", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CeCostCategorySplitChargeRule, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CeCostCategorySplitChargeRule, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CeCostCategorySplitChargeRule, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b053a3a505632104173271c25206a5a53f7d8efd5713b7875ecddd4bacc285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategorySplitChargeRuleParameter",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "values": "values"},
)
class CeCostCategorySplitChargeRuleParameter:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#type CeCostCategory#type}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47f291c1eaa278817694b8bbeadb242e84d135121c232d85b2d24bf4d80909b)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#type CeCostCategory#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ce_cost_category#values CeCostCategory#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CeCostCategorySplitChargeRuleParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CeCostCategorySplitChargeRuleParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategorySplitChargeRuleParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__667dca30bf2524df354089781480be857d31f1e8feafa225103bfbd7682799f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CeCostCategorySplitChargeRuleParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6353e084030fb9c79b0fc76607ccddafb1bed928f322a70441e481e81c7d66c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CeCostCategorySplitChargeRuleParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb3b37b87f0dad40b4a2663f0c74a4ca020857ea0eadf81d31a3d7062fe6386)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b367e741aac29acdf376d3cb7e08a7c7c8e3e0e15736db19f49743cc6fc11d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8781fe4d23623c1619c290bf1c03ad382e8150165de9a9d5e85c352d5ccb21eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategorySplitChargeRuleParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategorySplitChargeRuleParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategorySplitChargeRuleParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e776ce2d6cb790545b46d6d0af57e58fbf93d320f6c10621b4782106773329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CeCostCategorySplitChargeRuleParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ceCostCategory.CeCostCategorySplitChargeRuleParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b95899f70a6939e512bec1188e7befa5ffdd0ad38645389e12d3f930bedfe7e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2708ea2b504470a9f7c36ab8106fc15c76f0a0f529ad4d3513747597c071db35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeda48ef7af4a487482089011ce573215ea8bb51cf1bc14155c0c794b4e1376a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CeCostCategorySplitChargeRuleParameter, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CeCostCategorySplitChargeRuleParameter, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CeCostCategorySplitChargeRuleParameter, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6751a913838ce569e54ee0bf6d52fe6450fbcc144152b898e44a677e23b984f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CeCostCategory",
    "CeCostCategoryConfig",
    "CeCostCategoryRule",
    "CeCostCategoryRuleInheritedValue",
    "CeCostCategoryRuleInheritedValueOutputReference",
    "CeCostCategoryRuleList",
    "CeCostCategoryRuleOutputReference",
    "CeCostCategoryRuleRule",
    "CeCostCategoryRuleRuleAnd",
    "CeCostCategoryRuleRuleAndCostCategory",
    "CeCostCategoryRuleRuleAndCostCategoryOutputReference",
    "CeCostCategoryRuleRuleAndDimension",
    "CeCostCategoryRuleRuleAndDimensionOutputReference",
    "CeCostCategoryRuleRuleAndList",
    "CeCostCategoryRuleRuleAndOutputReference",
    "CeCostCategoryRuleRuleAndTags",
    "CeCostCategoryRuleRuleAndTagsOutputReference",
    "CeCostCategoryRuleRuleCostCategory",
    "CeCostCategoryRuleRuleCostCategoryOutputReference",
    "CeCostCategoryRuleRuleDimension",
    "CeCostCategoryRuleRuleDimensionOutputReference",
    "CeCostCategoryRuleRuleNot",
    "CeCostCategoryRuleRuleNotCostCategory",
    "CeCostCategoryRuleRuleNotCostCategoryOutputReference",
    "CeCostCategoryRuleRuleNotDimension",
    "CeCostCategoryRuleRuleNotDimensionOutputReference",
    "CeCostCategoryRuleRuleNotOutputReference",
    "CeCostCategoryRuleRuleNotTags",
    "CeCostCategoryRuleRuleNotTagsOutputReference",
    "CeCostCategoryRuleRuleOr",
    "CeCostCategoryRuleRuleOrCostCategory",
    "CeCostCategoryRuleRuleOrCostCategoryOutputReference",
    "CeCostCategoryRuleRuleOrDimension",
    "CeCostCategoryRuleRuleOrDimensionOutputReference",
    "CeCostCategoryRuleRuleOrList",
    "CeCostCategoryRuleRuleOrOutputReference",
    "CeCostCategoryRuleRuleOrTags",
    "CeCostCategoryRuleRuleOrTagsOutputReference",
    "CeCostCategoryRuleRuleOutputReference",
    "CeCostCategoryRuleRuleTags",
    "CeCostCategoryRuleRuleTagsOutputReference",
    "CeCostCategorySplitChargeRule",
    "CeCostCategorySplitChargeRuleList",
    "CeCostCategorySplitChargeRuleOutputReference",
    "CeCostCategorySplitChargeRuleParameter",
    "CeCostCategorySplitChargeRuleParameterList",
    "CeCostCategorySplitChargeRuleParameterOutputReference",
]

publication.publish()

def _typecheckingstub__dca903bb7ad34af3622ebfd528487d1ff715c9fb1a1989688d33ceb2c9a6b8d9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategoryRule, typing.Dict[builtins.str, typing.Any]]]],
    rule_version: builtins.str,
    default_value: typing.Optional[builtins.str] = None,
    effective_start: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    split_charge_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategorySplitChargeRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__86920f21cd8ed679af2e450accb9943953924c6f6832ab66903f0b0b216abd91(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategoryRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e007d77781ef5b18e1ae58dfa9ad2db3dae3c9c99f09f63cdcdd2bd19b3244(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategorySplitChargeRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e0595ae68d5b1dcd7eeda6df114ba9546944963aed455d5b30eed22f8675f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d200d333f377435ae160cb1e5121694c4d5d69fa89cc1a15d5968a246ada63e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d196460e2f03485f8051693aa44447697843d3f92900c3826061bd0aa7df43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2d624d22e20b89bca0b969e9c96b42346e8bddd7eadc5ef55dd0308a9d8fa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c666dd29ce81ebfcfdd259274680d185d7e2bb936cccf33852675675af2e030e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923f41ded42cd183e1ea776d7692e120dccccbc8d114c19eb42ee4e57de76c1c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136a9af8d8ec1e3f3d35d5701635e68cb0a8283cca8664578d788de00ef5f2f0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f4d662237fd4686b32bfb59c4d22ec4735c33d67ec7d0002cb5ad026c585c8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategoryRule, typing.Dict[builtins.str, typing.Any]]]],
    rule_version: builtins.str,
    default_value: typing.Optional[builtins.str] = None,
    effective_start: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    split_charge_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategorySplitChargeRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81464be801c1eed01907e941fed52ac7ca6158120baa3fddd298fe4a4966e149(
    *,
    inherited_value: typing.Optional[typing.Union[CeCostCategoryRuleInheritedValue, typing.Dict[builtins.str, typing.Any]]] = None,
    rule: typing.Optional[typing.Union[CeCostCategoryRuleRule, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d879549216b38dee5b4d152e5537fbb5a899bc01b7ac22231f384ad40e0d1f1(
    *,
    dimension_key: typing.Optional[builtins.str] = None,
    dimension_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345dd2ca950ae81c202fa3d5946820c934dbfa5d4221035fafb56fced4519f25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a02e73938d00007ffc80bfe49a314f7430c6d84504ed900ae0aec35cef055d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfbb1381db0612b8093d1546eca93d42cb1d45f90ecf5349d184140439db4df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34600a1a01d7b532849053f8d92e998d42f5107eb02b8da702acf20f2f2a5b9(
    value: typing.Optional[CeCostCategoryRuleInheritedValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba55b96b46e3ad4c854a04f8b66b107ece6fb1317da701b5b39d1dca5d08e79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e143a66436d8304d5801e5adc035c0cbe024d5ac6b080eb4d4d23dcbcafc90d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead26ae2a3b6c047ed66435351ec4d7c13b6cb224616e0352cc743faa3e8ca96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275881d410b02674471343636079d0ac1aee1e3018ada46091d46a08eafb4a1a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1e23d84eb8ea2f430e438831d1d12cbdc4fbb770164378453ed74a8e838dea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe85d09cfd2e2a94983aface9fe6d830ce8af89f3906b0e6f64ab965264ed72b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22c33e827b1c29ab07a889c945efb609b070e9906ba8a6799dd5c28e204613b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c32b73baa1b2a624d00e2ff6fc1f7c4e78d0a0c11ca9188c2b0c29dd693ef7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e4a28e1c3aaa0551dfb6592c887d1a0bb5e4ae2d23ee468baff9839b8b45ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d8b5479cd2bc65b614de06939794b103e01c1e8251b0d0f3d14c18a5ffd415(
    value: typing.Optional[typing.Union[CeCostCategoryRule, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1382d024a5cf3e63e423103a2c6b0aaf4fbd13ef5f6ddd454dcc5934dbe7dd0b(
    *,
    and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategoryRuleRuleAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cost_category: typing.Optional[typing.Union[CeCostCategoryRuleRuleCostCategory, typing.Dict[builtins.str, typing.Any]]] = None,
    dimension: typing.Optional[typing.Union[CeCostCategoryRuleRuleDimension, typing.Dict[builtins.str, typing.Any]]] = None,
    not_: typing.Optional[typing.Union[CeCostCategoryRuleRuleNot, typing.Dict[builtins.str, typing.Any]]] = None,
    or_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategoryRuleRuleOr, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Union[CeCostCategoryRuleRuleTags, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a826bfc5e8068f94ceb06e69603b03d05aeb694b98e8aec4f13b9e96fe031173(
    *,
    cost_category: typing.Optional[typing.Union[CeCostCategoryRuleRuleAndCostCategory, typing.Dict[builtins.str, typing.Any]]] = None,
    dimension: typing.Optional[typing.Union[CeCostCategoryRuleRuleAndDimension, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Union[CeCostCategoryRuleRuleAndTags, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693ebd54dd0c6a188a93315e7fd2384dcaeb6d6b28c03e13a9f86a62a186d35f(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610ddf7ec5eefefc5f63d1f8cd34943f3ae9275ac51d0d6517d27ca5ad3fa2c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f086dfa7f4f6ae39dd2d1062d6d658a5f9fd49388ad5fc7863aa27be4bc67114(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf3e1d7f49a432d1d6284a494991b658c756b2b7ec5ffccabe3e722974e8c4e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f9978e4e4d23f7db72a87b8ece9aa24e5daa7cb6e9bd08e7466c2192b6d5fc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd7f4d4dcbfabb4c544281a63825467d1ea3500183762c0959b5840172c3d39(
    value: typing.Optional[CeCostCategoryRuleRuleAndCostCategory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248eda79c8c00f0767325544ba1b3d141be206555d863a847fdd152a400bc3a0(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198d3d5a3aa7d9ea8958a416826ebf9d7b3571d8cbcbd33bed9862fa21775025(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d77d7a78ca5a06e18fc0fbbe3a0c6de59f266be1ce586bcadfb4388ebd9765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8aaec3588282293c5888be6e70de5b53dc8a4f9da20e256981e06d427f3470(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b704007be813ea10ae5b54bcdfc49c7b38249e50ab7ae899129dbfbbfa25b1a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2219d4c0889afb41875fdcb2c70348409d081b2ea8b2ffb44f8a8ad6541e4109(
    value: typing.Optional[CeCostCategoryRuleRuleAndDimension],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b54d15dda0fdb97af8a906781a6776ac38238195611c95129fb40aca71cde2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada196453dd83f291de6d4420ca81fb1e36c0c28f37bee93545096624d74bd2c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bedf5e90f0c23151ebb84856cd9cd8320b71fe138ca45b345fbecd1f9b9dd9d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531148d8de24351b54620f02f5b3fba327f81f5450338c87189ea58de7683580(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893323bd3ebedeb76fbd68c5b33791ade46e1bae304450976f60284721d853c1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78306587216b105de76bb202379cb7af6acc89159bde030beb3e11f8c846c8da(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleAnd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc877610e1ed320d59472b6eed08deea07db7725ec8bff54a2d5273ff80a12f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d2a704409d05ca1870408da92ed3a21c6a603e42cf1cc747988ef905882dc4(
    value: typing.Optional[typing.Union[CeCostCategoryRuleRuleAnd, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4229c1a54d2b3ab6cdee7acf9ae6b012245de3cb2f8e2aa83b509c4390315950(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba917470a0fa6b045de5cd0e88e23625ad656585c1ec4a63efaac4c8b38f842(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01418af70102df9faac638995f9f6c91db85537d2f4d4a35a66fd1802d42910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6392b760d5cd7d6953c988bf9d686111afbb3384024111fd839cda23ca4c5fb3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167987fc643ca85ca2b7066af5310b585b513dd2acd56aed65831a3f2136d5b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1483c10a70d79470bbe6747d3a441f71579bd51f0e0b5754a45a3659658e7677(
    value: typing.Optional[CeCostCategoryRuleRuleAndTags],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ecb408659afebfedd52145599269b62985e173f0b7f906b3b5ee25f9453f7a(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ce47394aa4de2a70037069ce67f135106e5714747364dda6f44a3d9f3356bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225ee701497d1d8ad1ff5285f7088f3cce12a466fdc6cc2f2091db1197c07728(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa64f4e0a2b40724b4d3ff1fb4c022fdbe9168a85f1ae63e0e29d2886a5a7dd6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541ebe1dcc136aafd3fea2128d81d2659b3538f341a01dcb69514aa8cf944824(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af38f606444da62047e9eb9ac2fc10612c8b525e462f105af1f90250be4c2735(
    value: typing.Optional[CeCostCategoryRuleRuleCostCategory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2edee190bc1788b7be1c1a2b966fec6a8a624a55bacdecf7a91685c31baada37(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eca606391ab8a234de91919c669fa452f62aad0c2ca2f62b831908069f2c6d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48f7b9b0e90e80e37a4b0a2388cdcee1a5a7f22a89b4e04a294c4f2422e251c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2413a66a3f916812010cfa7df415e9c3e76a4a60ae408aa46348ab20acd3af1d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebbafa594a632d8e2acccc8c0ee880f272f41fe46feade370614ba00d19e5a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511d4ebe6a2ee17066ab0bda4f29b85c6b2e85fbbe2699e5a904ef10edcb5ae6(
    value: typing.Optional[CeCostCategoryRuleRuleDimension],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8515ab75bf8d429b3b1d8bc0ca32957491ac8b6856d4659c4efd7bc3c751a75(
    *,
    cost_category: typing.Optional[typing.Union[CeCostCategoryRuleRuleNotCostCategory, typing.Dict[builtins.str, typing.Any]]] = None,
    dimension: typing.Optional[typing.Union[CeCostCategoryRuleRuleNotDimension, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Union[CeCostCategoryRuleRuleNotTags, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab28c78999f895e0c64fd1513e398c97d3c625221b519e1f78b84ebbf95989e9(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e38d2cdc2f2b2b5d75ff6193a1f87a753e5984013f8f62fa66547f42be45d4cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d126c9075a0d41cd0b401872c64e1d80376fc6db077227bb719edb67b8b473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30289081daf9d14465342ee8862bf02579cdfac4e6e060c34d397ecd41a2ae06(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e78db6a3eeaf20f9d3e89a1d28fd132ba67d6f504c451c9c237a1ac974c7bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a1728928ef44429bd9ca02cb3ce35f5baaed275308b61a9c0b40bbe5ebc012(
    value: typing.Optional[CeCostCategoryRuleRuleNotCostCategory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66193d4c3177be998864e1bd8f593ace5d7182a1d4cdd796b208696d58b7ad85(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3539942eb1441fb2617fc6c3b499b1ee943d7433723ea2ecb9d4d3522759dc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fb25cdda9af1193a6588892e5b41bc25021fedb9bcb4a5c75afae579da380f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6baed3de59850ea650dee472d1faa8d5138ee1ffb3e3da4a31663e0e07f10e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc91d261f4623940a39dbd5d3128d918fe6c09afc25b5f3a2d4b50538eafa2b3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d26bc3ce4e8640270c61aa907197e4417bb38724ecc996090a7b0a0ab9d6525(
    value: typing.Optional[CeCostCategoryRuleRuleNotDimension],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6c53d0bcdc0247fc098e55c920d02213aca81e24addebb0476111472077996(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca18de625a87cca395a65a9b8593a01d8ddbb9cc5ba82d981ed3a2d41c09c88(
    value: typing.Optional[CeCostCategoryRuleRuleNot],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43895437dd520f74c895982a104462b5224ec2813b79d0947b4e01ef89c7beb4(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde3c1c66089cb77ecd2f2d158120907b488773b5b91fdc79c1164e78e252ab8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecdbff7c383bc3ea44c7643173dd74f812d30cd4693b4481d16e09b9a85812a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e64cc4c9b835e80599006431d3cc3d277389356fb91d93a1e581a0c8b94aab6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0050b3ab50038efd164fb2ee20bb9b13017aabce9579e190d2d2a49e648db9d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de3b665ca5cfd9c9f2eed8298d056aa2430ab230ebbfad4489657977edeaaa1(
    value: typing.Optional[CeCostCategoryRuleRuleNotTags],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10af28b0edda8039dfa47eaca979cb39be25c44340facbeedab0b4f50de0efa(
    *,
    cost_category: typing.Optional[typing.Union[CeCostCategoryRuleRuleOrCostCategory, typing.Dict[builtins.str, typing.Any]]] = None,
    dimension: typing.Optional[typing.Union[CeCostCategoryRuleRuleOrDimension, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Union[CeCostCategoryRuleRuleOrTags, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8e12393dd787f22cabd9deeea1f6306cb6a4c41669c1a8eb80613e7c13c9c2(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fb70e87a3a5d4075a31e765a3316c105238bb32397cd6700c17a5548047a24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c51912368a8868489ce7add6aab75605a287279c4666bb19ada423b50d6f5e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36888bc6c6a8ebbac1a890b8d598401be945bf0e5d1654e1299a32b9ce6fe93(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__addc6291eafebcb8541e0534fe473156499744612338256f9704a6e4cb1bc364(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd05f272493a418abcd30b80e6fd987dbc92405b91c4a163946bd1ba01143a9(
    value: typing.Optional[CeCostCategoryRuleRuleOrCostCategory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20619a1018ab990799d867d95d58196d6cd908dd36f2c7a937acc7bcbc50a23(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6571ac3187f13ca62ef45e029e04e4a4d58cb57a1c6a8e88a1edc74b4bd0c0c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0fe04fa74c8d48e3f6c8559be84002911f998360d8fdb76ce6b7d40c9011b0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03fb930a56d4423b803f6ca7f78d2eba75559eb297b873b2cb67df67406cd325(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9e19f7ae74d9214676922ce9863854b3a8e4860393681ecdb86a2cccd725d3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af71369c6bcda0b54de1a7f53a50cb523ab403abb721f612858a2fe7079634b(
    value: typing.Optional[CeCostCategoryRuleRuleOrDimension],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc32ee6b21a41a976172f477579c0e3d1f4bfdd0c09bf7358ead8ef3da7f9711(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa3c2817535f106227249305e757ef8818f998e0c0d11e38627d2bc85b7fb48(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bc570949807c45dd10f5ef85a3765928a6ae3516c47161756db74db5a39fca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34dd661cace7f682f1b4e17f1af0dfefbbaae47fede0176adb585973d695b593(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7953f1144c96acc6bc0d841b182bdd1a092cba7477c06ffc9ba5d1c19eeab128(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836350224c4964104f7a59b5d2621f754f7ec0f7916f33e2476ca4ea671ad104(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategoryRuleRuleOr]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e54489281a9877000c7174af0d02e5d92057ad8e5099901ab70470fb71fdab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8906b05660a51f1d882b1d003b997754b833d5287e6c311cc000e9dc8dc581(
    value: typing.Optional[typing.Union[CeCostCategoryRuleRuleOr, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188783368c97562e89d106c61c05393b8f9b3ba8ff48f7a139d85d3a75bfce38(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f77e07096bf57793fac370a7b4ef7748a3ffd15c77f7a7dd26e1efe2700616(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4922e0f18b94719a8c954bf4fad76510e1d99110a63da3b2020432913381d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1920cd40fd20f91d3793e1560271974b5960f7d8168046849d4e9c514da0bcb1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ad2e061d2223794cac04a5a97d55e31df2b4156ef6b80ee1767aa073a29319(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303fad7dc0e98ec9f806623b4f15055a8a1fda98f2ee9dcbaaff2289c3c9c322(
    value: typing.Optional[CeCostCategoryRuleRuleOrTags],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e64907bf4650a800e89ed0f3a01bfc7d87d7f2ba7e3c98010b5ec95c99f1a88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10ec911de9d2c6c82907105bd9bf2afe76613904087224db8c7b96f9d25fc5b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategoryRuleRuleAnd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d88819b793baad54bd9ebcecdb3495ec971c821bb7f311e4ba0e377d5dec53(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategoryRuleRuleOr, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1365c4e9b5a5849a31434743e4c13f031c98a77b96c3acf5deab25b4ee960e(
    value: typing.Optional[CeCostCategoryRuleRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21897034ad168c58444ef560a442af862fb67fdd82fecce28037d598ddd16e7e(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed214a00c1790a6bf2d5f28bef40dcd7e490856a0dd191b53b77766340844a14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c82b1970cff2416b99af98c1a7bdd1b982bf6a861d66c50d770466dcb05d816(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55be325fcd5cfb8992ed9ed3b0015ab49963910fb458e81a6a245b39ecb7e3f8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8081781fe722291cd61407ea23bbcdd9456a7fdf1d0c7fc3058ae95c9e385b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3429a51b0060f94cfaf6af0d37ba0369856908b0f0afb90638a09cffd66662(
    value: typing.Optional[CeCostCategoryRuleRuleTags],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2acf5780c91ff56b2039951fddbbcd18217b16c656de07a26a1410a75346083e(
    *,
    method: builtins.str,
    source: builtins.str,
    targets: typing.Sequence[builtins.str],
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategorySplitChargeRuleParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2fbc76b1d0c0d6796c8efa1eb1d0237a56c65fec4142e90cfdf1ea5d69abdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ab8fbbff4412d926c40b76d7b0fd46365f0133bf90637ff6399f788ebfb8d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c2e44dcb11a26a1f14d1d58c54bedfb65331cd5c11ec7bbca6d45a0e1554f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3daf5b22e394d435878b2ab625c265000c02b8e90c9de298864fdb77d05e6aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96010148c023cf777b385836b2b406279895e4e675a633c255979522f113a3c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc2678eaaa76b32678351a56f8bdb401738457cf5d29df99fc84a342388f305(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategorySplitChargeRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fab63de02eda2638c92a4dd46465cb1457ad7ce0fad4b694f11f991b1b71282(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf86ebb4273660798862be6d646308b85e2e9366519c4a115acf8f56c345f7b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CeCostCategorySplitChargeRuleParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e431301d69d64f96a55c5bd24c074bd3caba0b1a365603c5a25a215510de50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3327315722502d433ddb990ec55dd8631e3b3d9ee8ff5a8f09cdcfb3810ef5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62438b683098183ba71f2ac4fdd050345548fbb4a3c6e7c9b63d2ac677523e95(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b053a3a505632104173271c25206a5a53f7d8efd5713b7875ecddd4bacc285(
    value: typing.Optional[typing.Union[CeCostCategorySplitChargeRule, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47f291c1eaa278817694b8bbeadb242e84d135121c232d85b2d24bf4d80909b(
    *,
    type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667dca30bf2524df354089781480be857d31f1e8feafa225103bfbd7682799f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6353e084030fb9c79b0fc76607ccddafb1bed928f322a70441e481e81c7d66c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb3b37b87f0dad40b4a2663f0c74a4ca020857ea0eadf81d31a3d7062fe6386(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b367e741aac29acdf376d3cb7e08a7c7c8e3e0e15736db19f49743cc6fc11d4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8781fe4d23623c1619c290bf1c03ad382e8150165de9a9d5e85c352d5ccb21eb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e776ce2d6cb790545b46d6d0af57e58fbf93d320f6c10621b4782106773329(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CeCostCategorySplitChargeRuleParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95899f70a6939e512bec1188e7befa5ffdd0ad38645389e12d3f930bedfe7e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2708ea2b504470a9f7c36ab8106fc15c76f0a0f529ad4d3513747597c071db35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeda48ef7af4a487482089011ce573215ea8bb51cf1bc14155c0c794b4e1376a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6751a913838ce569e54ee0bf6d52fe6450fbcc144152b898e44a677e23b984f6(
    value: typing.Optional[typing.Union[CeCostCategorySplitChargeRuleParameter, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
