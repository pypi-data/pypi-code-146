'''
# `aws_fis_experiment_template`

Refer to the Terraform Registory for docs: [`aws_fis_experiment_template`](https://www.terraform.io/docs/providers/aws/r/fis_experiment_template).
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


class FisExperimentTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplate",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template aws_fis_experiment_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateAction", typing.Dict[builtins.str, typing.Any]]]],
        description: builtins.str,
        role_arn: builtins.str,
        stop_condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateStopCondition", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["FisExperimentTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template aws_fis_experiment_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#action FisExperimentTemplate#action}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#description FisExperimentTemplate#description}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#role_arn FisExperimentTemplate#role_arn}.
        :param stop_condition: stop_condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#stop_condition FisExperimentTemplate#stop_condition}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#id FisExperimentTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#tags FisExperimentTemplate#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#tags_all FisExperimentTemplate#tags_all}.
        :param target: target block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#target FisExperimentTemplate#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#timeouts FisExperimentTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5010f13d06ae9bb491da2c143204daf47aa02033197a1bb4fc9674468b6ae58b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FisExperimentTemplateConfig(
            action=action,
            description=description,
            role_arn=role_arn,
            stop_condition=stop_condition,
            id=id,
            tags=tags,
            tags_all=tags_all,
            target=target,
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

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70fd4cba3e5db93feb9a0ef4646513d6689eb3285b651b46e8941b1b99dd3b68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putStopCondition")
    def put_stop_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateStopCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__227ebed9cc6018ec355979671b892f8fc6a34a52924e22f757e522c9450e6d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStopCondition", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0bd28a788c2b43010a6c1cb86e346548e2b357da2ab04ae2ceb177dd7be61f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#create FisExperimentTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#delete FisExperimentTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#update FisExperimentTemplate#update}.
        '''
        value = FisExperimentTemplateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

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
    @jsii.member(jsii_name="action")
    def action(self) -> "FisExperimentTemplateActionList":
        return typing.cast("FisExperimentTemplateActionList", jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="stopCondition")
    def stop_condition(self) -> "FisExperimentTemplateStopConditionList":
        return typing.cast("FisExperimentTemplateStopConditionList", jsii.get(self, "stopCondition"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "FisExperimentTemplateTargetList":
        return typing.cast("FisExperimentTemplateTargetList", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FisExperimentTemplateTimeoutsOutputReference":
        return typing.cast("FisExperimentTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateAction"]]], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stopConditionInput")
    def stop_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateStopCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateStopCondition"]]], jsii.get(self, "stopConditionInput"))

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
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTarget"]]], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["FisExperimentTemplateTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["FisExperimentTemplateTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dae61cf50e8cde002808f657d26d1961e42d3b00970f7053b9c92e8aea162c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea9d0bd842035827c1c017dc61142d29f98b079cea584a547dfecd86cd15d971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479d7cd42f00b4b97b122c9a7af3189f4bcf8c12182b5af621b0290e4382ec9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0efed8774020cad3d6f181121fab716b03233e4263077bea9919f972920a7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcadacc373b140f545c94ddb22117a07536d0adb5f8a59c233f38a08c5a6eb00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateAction",
    jsii_struct_bases=[],
    name_mapping={
        "action_id": "actionId",
        "name": "name",
        "description": "description",
        "parameter": "parameter",
        "start_after": "startAfter",
        "target": "target",
    },
)
class FisExperimentTemplateAction:
    def __init__(
        self,
        *,
        action_id: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateActionParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        start_after: typing.Optional[typing.Sequence[builtins.str]] = None,
        target: typing.Optional[typing.Union["FisExperimentTemplateActionTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#action_id FisExperimentTemplate#action_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#name FisExperimentTemplate#name}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#description FisExperimentTemplate#description}.
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#parameter FisExperimentTemplate#parameter}
        :param start_after: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#start_after FisExperimentTemplate#start_after}.
        :param target: target block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#target FisExperimentTemplate#target}
        '''
        if isinstance(target, dict):
            target = FisExperimentTemplateActionTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__789b5fa40cc7bf9af4c0b002c084d0ac8f18619572d09b312d0d85e9a10bccc2)
            check_type(argname="argument action_id", value=action_id, expected_type=type_hints["action_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument start_after", value=start_after, expected_type=type_hints["start_after"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_id": action_id,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if parameter is not None:
            self._values["parameter"] = parameter
        if start_after is not None:
            self._values["start_after"] = start_after
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def action_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#action_id FisExperimentTemplate#action_id}.'''
        result = self._values.get("action_id")
        assert result is not None, "Required property 'action_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#name FisExperimentTemplate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#description FisExperimentTemplate#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateActionParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#parameter FisExperimentTemplate#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateActionParameter"]]], result)

    @builtins.property
    def start_after(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#start_after FisExperimentTemplate#start_after}.'''
        result = self._values.get("start_after")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target(self) -> typing.Optional["FisExperimentTemplateActionTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#target FisExperimentTemplate#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["FisExperimentTemplateActionTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a527ae094cf8b1842b323b364609789efcc4c946b0ffee7d115b5907ddc1364)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FisExperimentTemplateActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c440e9e2b41b783cc3fb73e6dbc9d965d758ebcf35712aa80c63ae81344e21)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a840aa67e6dd68005c2bf3996bc1591912da72ab4654a1efa070d68d460ebfc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76e84de6b2ae71126feb29db6568f217a5fd8cbff8f827b6ce642080baeae332)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a79e8c2146838583649cdde64c196828a45686c7784499bf893dc0ebd644520c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a916b4bf8ef2327ac3a05428daf52bfc33ba8e65c705230953c15e856ee4b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class FisExperimentTemplateActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68a77713fe7820625bb7451cb64abd645706ccc94fa021f83832dfb70d9921e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateActionParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3b376e0a6aa2ed57cab5b21b8254f40400e1d5e4eefec1e81a612df9492d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameter", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#key FisExperimentTemplate#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#value FisExperimentTemplate#value}.
        '''
        value_ = FisExperimentTemplateActionTarget(key=key, value=value)

        return typing.cast(None, jsii.invoke(self, "putTarget", [value_]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @jsii.member(jsii_name="resetStartAfter")
    def reset_start_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartAfter", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(self) -> "FisExperimentTemplateActionParameterList":
        return typing.cast("FisExperimentTemplateActionParameterList", jsii.get(self, "parameter"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "FisExperimentTemplateActionTargetOutputReference":
        return typing.cast("FisExperimentTemplateActionTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="actionIdInput")
    def action_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateActionParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateActionParameter"]]], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="startAfterInput")
    def start_after_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "startAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional["FisExperimentTemplateActionTarget"]:
        return typing.cast(typing.Optional["FisExperimentTemplateActionTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="actionId")
    def action_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionId"))

    @action_id.setter
    def action_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90427120196825064e01b1371cb1eba8f7b56e2bb82c16974eff014f889db4c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ae1d744fa43745600d6c861f4090451a198ab6de3c20f6164037102f8cec69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755e4cb38a0e152e4d047fd2c8d454698eb9c65f793eb749f205cfd3ed5f89b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="startAfter")
    def start_after(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "startAfter"))

    @start_after.setter
    def start_after(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247417d8473b5a5146d672b6463bcc5846cbbf530e6f16612ae17e0bfd96d3ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAfter", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[FisExperimentTemplateAction, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[FisExperimentTemplateAction, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[FisExperimentTemplateAction, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7859ab0147acaecffc9d8edf6025e37cb57967e12717f2d3d0b3865b85d8c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionParameter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class FisExperimentTemplateActionParameter:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#key FisExperimentTemplate#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#value FisExperimentTemplate#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03546c9c4fbbd910967efa8d80997493a9d9a77425e5744e4e34016abf0ce924)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#key FisExperimentTemplate#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#value FisExperimentTemplate#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateActionParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateActionParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3046af9cd1b28d8d76c4718d4b66e795b6c08c07a3a81731fd1bbc1453f901b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FisExperimentTemplateActionParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ccfe6cc2da88fc01b31920233fc2cc60307027f50895b10f6b9e0a64fd1fe1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateActionParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ad2a6bf3428099d36872107aebc8e90edf178ef965cf6b4e4a2848bb504187)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b2ceafdecb490176de0a1cc4d988a2d771b1cc026e876bee4b5c8604a8e3525)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9688e930b4d9e725ccb277eb5eb05fa05b8e0f022c1ca34497c36eca4974d74c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateActionParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateActionParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateActionParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a100fbd24c83fae6f1c343f72ec19ad4194281a91f374e51186b637ad7cd94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class FisExperimentTemplateActionParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__616db847f9bba13c3c2de1c96d5fcd65ad59e746de439d3a203bad6a909fadee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__01c9449560ca3c49d5a63681abe59be6ab46458b6beb8885cee863a319da8ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58899abc4cf68c062d852ff9dcb3bace3643dfa20b1c1f76a3c80c7a4f84bb50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[FisExperimentTemplateActionParameter, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[FisExperimentTemplateActionParameter, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[FisExperimentTemplateActionParameter, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a7ba4e28dd1064d9db7948d295d32d6d9e613428b9e3c8ba06a89dd35e143b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionTarget",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class FisExperimentTemplateActionTarget:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#key FisExperimentTemplate#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#value FisExperimentTemplate#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271bb7595b3cd263685ef0f05246da67b30ba9b7050b8c1a67a7f8d57d64085b)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#key FisExperimentTemplate#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#value FisExperimentTemplate#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateActionTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateActionTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__564a0c00b8f74631c761438537d3851b6db29281bb89e84892b75b6ab5f3b749)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a91a513dfd1bff54a1bae0f884e6a05d49acb7c14d0b5cbc6a9a5ae40850e4cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4716c966b019d6fc545f40c756f98d7919bb8a7f54cc59f0aa46c7f849ac4cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FisExperimentTemplateActionTarget]:
        return typing.cast(typing.Optional[FisExperimentTemplateActionTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FisExperimentTemplateActionTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea76e81fdab790e9deabcafa711270ce09f0a48ab9b7113af6d36727860104b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action": "action",
        "description": "description",
        "role_arn": "roleArn",
        "stop_condition": "stopCondition",
        "id": "id",
        "tags": "tags",
        "tags_all": "tagsAll",
        "target": "target",
        "timeouts": "timeouts",
    },
)
class FisExperimentTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateAction, typing.Dict[builtins.str, typing.Any]]]],
        description: builtins.str,
        role_arn: builtins.str,
        stop_condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateStopCondition", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["FisExperimentTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#action FisExperimentTemplate#action}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#description FisExperimentTemplate#description}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#role_arn FisExperimentTemplate#role_arn}.
        :param stop_condition: stop_condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#stop_condition FisExperimentTemplate#stop_condition}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#id FisExperimentTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#tags FisExperimentTemplate#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#tags_all FisExperimentTemplate#tags_all}.
        :param target: target block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#target FisExperimentTemplate#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#timeouts FisExperimentTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = FisExperimentTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb79c51340f69266ae32516c341e0f8f1f8df3fd0f178f1c032d60efc0d24db)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stop_condition", value=stop_condition, expected_type=type_hints["stop_condition"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "description": description,
            "role_arn": role_arn,
            "stop_condition": stop_condition,
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
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if target is not None:
            self._values["target"] = target
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
    def action(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]]:
        '''action block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#action FisExperimentTemplate#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]], result)

    @builtins.property
    def description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#description FisExperimentTemplate#description}.'''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#role_arn FisExperimentTemplate#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stop_condition(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateStopCondition"]]:
        '''stop_condition block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#stop_condition FisExperimentTemplate#stop_condition}
        '''
        result = self._values.get("stop_condition")
        assert result is not None, "Required property 'stop_condition' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateStopCondition"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#id FisExperimentTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#tags FisExperimentTemplate#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#tags_all FisExperimentTemplate#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTarget"]]]:
        '''target block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#target FisExperimentTemplate#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTarget"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FisExperimentTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#timeouts FisExperimentTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FisExperimentTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateStopCondition",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "value": "value"},
)
class FisExperimentTemplateStopCondition:
    def __init__(
        self,
        *,
        source: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#source FisExperimentTemplate#source}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#value FisExperimentTemplate#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9be20f2acace1b0837001604faf60b54cef0a5571b567c0392f2239cf3715b)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#source FisExperimentTemplate#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#value FisExperimentTemplate#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateStopCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateStopConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateStopConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2158e3be5811ce246ab7b40503852f07d9cff7dc42673d7d20a0e353c02997f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FisExperimentTemplateStopConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df53126c8d18fad1ec0c22df34246328a2f1ad5490999cc9c79335f693a65e05)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateStopConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e3329ade06e13e14fbb726da3170ac9779f64578a25978f62a01957a7f8bbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6285faf5a8af8445b96e4e018d625d44c3ca8b5d649e5b28b2c3d85a9f2f14c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0aa4311ffe01a5efdb6d7c28a483751ff02309a9133ac611469243a776d248d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateStopCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateStopCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateStopCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645dc66f4f9534c13b2ae2e2c145c21d1ddb445dd26d10e51d0fa90218170f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class FisExperimentTemplateStopConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateStopConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df7146693dc39b7b55361389eab14fdaae2c91c969a869403b06438ca40cc3df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__641f6d8f026c83121c8f6981a78e7c2ae6bad40e2460e77bc2584b57eed00347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abdc428a8f03e96ec365a84f9f158b9ace9ed6ce92d6f4fd09c9c36b1472d720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[FisExperimentTemplateStopCondition, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[FisExperimentTemplateStopCondition, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[FisExperimentTemplateStopCondition, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9916d1cb7201d29656b00847141f43a941f76cc01a9a9ddb795bff423d46f971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateTarget",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "resource_type": "resourceType",
        "selection_mode": "selectionMode",
        "filter": "filter",
        "resource_arns": "resourceArns",
        "resource_tag": "resourceTag",
    },
)
class FisExperimentTemplateTarget:
    def __init__(
        self,
        *,
        name: builtins.str,
        resource_type: builtins.str,
        selection_mode: builtins.str,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTargetFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTargetResourceTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#name FisExperimentTemplate#name}.
        :param resource_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#resource_type FisExperimentTemplate#resource_type}.
        :param selection_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#selection_mode FisExperimentTemplate#selection_mode}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#filter FisExperimentTemplate#filter}
        :param resource_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#resource_arns FisExperimentTemplate#resource_arns}.
        :param resource_tag: resource_tag block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#resource_tag FisExperimentTemplate#resource_tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97993927574dcf7637e00d2e87ef614b3bd14be16d5e691d48ee5caaed844c56)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument selection_mode", value=selection_mode, expected_type=type_hints["selection_mode"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument resource_tag", value=resource_tag, expected_type=type_hints["resource_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource_type": resource_type,
            "selection_mode": selection_mode,
        }
        if filter is not None:
            self._values["filter"] = filter
        if resource_arns is not None:
            self._values["resource_arns"] = resource_arns
        if resource_tag is not None:
            self._values["resource_tag"] = resource_tag

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#name FisExperimentTemplate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#resource_type FisExperimentTemplate#resource_type}.'''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selection_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#selection_mode FisExperimentTemplate#selection_mode}.'''
        result = self._values.get("selection_mode")
        assert result is not None, "Required property 'selection_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#filter FisExperimentTemplate#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetFilter"]]], result)

    @builtins.property
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#resource_arns FisExperimentTemplate#resource_arns}.'''
        result = self._values.get("resource_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetResourceTag"]]]:
        '''resource_tag block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#resource_tag FisExperimentTemplate#resource_tag}
        '''
        result = self._values.get("resource_tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetResourceTag"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetFilter",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "values": "values"},
)
class FisExperimentTemplateTargetFilter:
    def __init__(
        self,
        *,
        path: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#path FisExperimentTemplate#path}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#values FisExperimentTemplate#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2879ca49dda0aaaa1e5a7f68d1d75216f0cf54737dd80fbddf2950df7c41e2f8)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "values": values,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#path FisExperimentTemplate#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#values FisExperimentTemplate#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateTargetFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateTargetFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21e580dcfc9cc09ef6fac896ecd8aaa50f258c7a3a67bbd2a0b212177e8c49ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FisExperimentTemplateTargetFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4490c87255f2a5dcc392d9b2202339180c7d35d70d595e6667e85c0cf226cff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateTargetFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e139e46b2fe08aad69445cd2c21f3114fa778e674117630c219344481304c5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdd1546702c9746a133db8903535ad0c9bf97f5f75af00aedab0a1f7ae7293fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79b341947f953035d75611b192cd977f0aabea4fb43d9085d14b0a15c8c655ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f1ab5fd8bcf4c9437eb5c06b169235074c8872b327d431a63c57d166448ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class FisExperimentTemplateTargetFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e2746868dcf5b79b79500188c9cb2e79ba7cc880e07edf6837112ccabdbc804)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__087c0071b18825e32ff3a9cd841acbf7a47677b7380d16f2a66acd7337964c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1eb1325329473248df95861795229bec7bea98cf02edadf599bfd1d4ccfa63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[FisExperimentTemplateTargetFilter, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[FisExperimentTemplateTargetFilter, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[FisExperimentTemplateTargetFilter, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8a16f4c7c563a73659d65f853d271dbdc4ce4250d9a24d1d1b5ef5f16319c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class FisExperimentTemplateTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__575ae3857671da98fe1193770af4e48300f2e234dc81ad32165a19d5bc6ceac7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FisExperimentTemplateTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3537a2db7ced52f89aaf212fb3c2fb962cddcaa2027c2f3f88036caf39d5b2c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33804de8dff43297a9f7ca8f218132ad1af866daa6914cab8f17b3e2be92437)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25afc49b18f50ce90b9539a1414a70f15170a5f7bc378dced58db60d2fea0eb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc5af1085d82dcb80a27dde6bd8b0b605b8ef9e59e348989f0c3aa201bf60c2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1874901a030b99c13aa6118ca27437e5848a4f13e7266f21dd8be101c74050da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class FisExperimentTemplateTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96fa89a13c9dbced27a032420c28e58402be8e14a3ace9bd746ca9ff70b01195)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTargetFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ebfe6a45318d17f3627cd4a2ff363855a8bfc42a20932cef290768bd95116e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putResourceTag")
    def put_resource_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTargetResourceTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7fd896825708248f1f8a830b0c075ecdc3d15feb9cd92a186711a256fe43c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceTag", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetResourceArns")
    def reset_resource_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceArns", []))

    @jsii.member(jsii_name="resetResourceTag")
    def reset_resource_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTag", []))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> FisExperimentTemplateTargetFilterList:
        return typing.cast(FisExperimentTemplateTargetFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="resourceTag")
    def resource_tag(self) -> "FisExperimentTemplateTargetResourceTagList":
        return typing.cast("FisExperimentTemplateTargetResourceTagList", jsii.get(self, "resourceTag"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArnsInput")
    def resource_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagInput")
    def resource_tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetResourceTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetResourceTag"]]], jsii.get(self, "resourceTagInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="selectionModeInput")
    def selection_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030107ca4a3ff327c48fef325f18ecab9bf76f949722a31099dd6a3585c05a05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceArns")
    def resource_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceArns"))

    @resource_arns.setter
    def resource_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74431df6357a64f417c8211ae463664ca8f17ea279e13e737d0bc5b318c0b76e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArns", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e7ea882d4d3876674c89e5f8da57dd1b6c0936454e7a3bcb8fa43148854d34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)

    @builtins.property
    @jsii.member(jsii_name="selectionMode")
    def selection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selectionMode"))

    @selection_mode.setter
    def selection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2191dcf652fe995a21fba1caa5c945e2e2c1baac0a24fe860ac038138e1754d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectionMode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[FisExperimentTemplateTarget, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[FisExperimentTemplateTarget, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[FisExperimentTemplateTarget, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfb13bd71cba28746c0a02ef1f99e70d22e44b885aadb1fb599bc602f585435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetResourceTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class FisExperimentTemplateTargetResourceTag:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#key FisExperimentTemplate#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#value FisExperimentTemplate#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96cd0457a4eb10458b8a50abc119af79a1fbb88419c031ef3ab8290ee4ff549)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#key FisExperimentTemplate#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#value FisExperimentTemplate#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateTargetResourceTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateTargetResourceTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetResourceTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f287db3e2610c858a05c626da9fedba7c97aee4902a0d01d6bb2bf3265276265)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FisExperimentTemplateTargetResourceTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39323d35e8b994c4c7a9f24dbd940861f76a438cf95358b1bb42f4d5633d861)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateTargetResourceTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f2791f7155c84736464c9e442afa27d3328fede61469c7a0b2d5ab625f242a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2121a31a7488a824e8bca21e350c0bdbc50b5848f7d20ba19c37c58c6d162f05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b6e1f265b035e6c2a77929539465a4bff2904a99d164cc1b85285555a9c6571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetResourceTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetResourceTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetResourceTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329727619979022caa5f88617ab39f12ed0538311cdb76c19d6f984a1fe9a16c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class FisExperimentTemplateTargetResourceTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetResourceTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db3dff3e87657353cb6e54797600173936b9d65474d181f9417b8db21a76aef4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__efd09f6840a24839599e1b883e4c4c87d858696a7031c2d34d304c8386e813ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0731a531dcbb7427c29ee1a95b06cb0bbe76b5603a64b0a6890081db726460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[FisExperimentTemplateTargetResourceTag, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[FisExperimentTemplateTargetResourceTag, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[FisExperimentTemplateTargetResourceTag, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477140c69a0118d275aca43c7890a1ecb5d61e617096ea674207f3623a4ccbda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class FisExperimentTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#create FisExperimentTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#delete FisExperimentTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#update FisExperimentTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08bcd3d6b912c7b5f17a936e92823fce6113e12a18e5b1655b8f76842bfbfca8)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#create FisExperimentTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#delete FisExperimentTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fis_experiment_template#update FisExperimentTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fisExperimentTemplate.FisExperimentTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__646f8ffe97cd95013ca6ad12432cc8f75a0ee3bc2b29e59bf329cb24966b54dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3a0a07e6f47c09733ec7b5f3f40a413138e7c126a612b88260c5c42faa1b29cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46643f85c953cd3469feec5d52f6d846b9cddef3fe31a4808ddc6be6751db31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891f36a52abfc2f83e28b09f973f86c7ce153c3ebffd9561c0a1ae6d7de5a832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[FisExperimentTemplateTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[FisExperimentTemplateTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[FisExperimentTemplateTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f330f3a7e8e3994783f5e76697b9e52fc564ea52dd2e016aaccd59739d53993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "FisExperimentTemplate",
    "FisExperimentTemplateAction",
    "FisExperimentTemplateActionList",
    "FisExperimentTemplateActionOutputReference",
    "FisExperimentTemplateActionParameter",
    "FisExperimentTemplateActionParameterList",
    "FisExperimentTemplateActionParameterOutputReference",
    "FisExperimentTemplateActionTarget",
    "FisExperimentTemplateActionTargetOutputReference",
    "FisExperimentTemplateConfig",
    "FisExperimentTemplateStopCondition",
    "FisExperimentTemplateStopConditionList",
    "FisExperimentTemplateStopConditionOutputReference",
    "FisExperimentTemplateTarget",
    "FisExperimentTemplateTargetFilter",
    "FisExperimentTemplateTargetFilterList",
    "FisExperimentTemplateTargetFilterOutputReference",
    "FisExperimentTemplateTargetList",
    "FisExperimentTemplateTargetOutputReference",
    "FisExperimentTemplateTargetResourceTag",
    "FisExperimentTemplateTargetResourceTagList",
    "FisExperimentTemplateTargetResourceTagOutputReference",
    "FisExperimentTemplateTimeouts",
    "FisExperimentTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5010f13d06ae9bb491da2c143204daf47aa02033197a1bb4fc9674468b6ae58b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateAction, typing.Dict[builtins.str, typing.Any]]]],
    description: builtins.str,
    role_arn: builtins.str,
    stop_condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateStopCondition, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[FisExperimentTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__70fd4cba3e5db93feb9a0ef4646513d6689eb3285b651b46e8941b1b99dd3b68(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227ebed9cc6018ec355979671b892f8fc6a34a52924e22f757e522c9450e6d28(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateStopCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0bd28a788c2b43010a6c1cb86e346548e2b357da2ab04ae2ceb177dd7be61f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dae61cf50e8cde002808f657d26d1961e42d3b00970f7053b9c92e8aea162c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea9d0bd842035827c1c017dc61142d29f98b079cea584a547dfecd86cd15d971(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479d7cd42f00b4b97b122c9a7af3189f4bcf8c12182b5af621b0290e4382ec9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0efed8774020cad3d6f181121fab716b03233e4263077bea9919f972920a7d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcadacc373b140f545c94ddb22117a07536d0adb5f8a59c233f38a08c5a6eb00(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__789b5fa40cc7bf9af4c0b002c084d0ac8f18619572d09b312d0d85e9a10bccc2(
    *,
    action_id: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateActionParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    start_after: typing.Optional[typing.Sequence[builtins.str]] = None,
    target: typing.Optional[typing.Union[FisExperimentTemplateActionTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a527ae094cf8b1842b323b364609789efcc4c946b0ffee7d115b5907ddc1364(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c440e9e2b41b783cc3fb73e6dbc9d965d758ebcf35712aa80c63ae81344e21(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a840aa67e6dd68005c2bf3996bc1591912da72ab4654a1efa070d68d460ebfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e84de6b2ae71126feb29db6568f217a5fd8cbff8f827b6ce642080baeae332(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79e8c2146838583649cdde64c196828a45686c7784499bf893dc0ebd644520c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a916b4bf8ef2327ac3a05428daf52bfc33ba8e65c705230953c15e856ee4b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a77713fe7820625bb7451cb64abd645706ccc94fa021f83832dfb70d9921e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3b376e0a6aa2ed57cab5b21b8254f40400e1d5e4eefec1e81a612df9492d64(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateActionParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90427120196825064e01b1371cb1eba8f7b56e2bb82c16974eff014f889db4c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ae1d744fa43745600d6c861f4090451a198ab6de3c20f6164037102f8cec69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755e4cb38a0e152e4d047fd2c8d454698eb9c65f793eb749f205cfd3ed5f89b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247417d8473b5a5146d672b6463bcc5846cbbf530e6f16612ae17e0bfd96d3ae(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7859ab0147acaecffc9d8edf6025e37cb57967e12717f2d3d0b3865b85d8c4(
    value: typing.Optional[typing.Union[FisExperimentTemplateAction, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03546c9c4fbbd910967efa8d80997493a9d9a77425e5744e4e34016abf0ce924(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3046af9cd1b28d8d76c4718d4b66e795b6c08c07a3a81731fd1bbc1453f901b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ccfe6cc2da88fc01b31920233fc2cc60307027f50895b10f6b9e0a64fd1fe1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ad2a6bf3428099d36872107aebc8e90edf178ef965cf6b4e4a2848bb504187(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2ceafdecb490176de0a1cc4d988a2d771b1cc026e876bee4b5c8604a8e3525(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9688e930b4d9e725ccb277eb5eb05fa05b8e0f022c1ca34497c36eca4974d74c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a100fbd24c83fae6f1c343f72ec19ad4194281a91f374e51186b637ad7cd94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateActionParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616db847f9bba13c3c2de1c96d5fcd65ad59e746de439d3a203bad6a909fadee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c9449560ca3c49d5a63681abe59be6ab46458b6beb8885cee863a319da8ae5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58899abc4cf68c062d852ff9dcb3bace3643dfa20b1c1f76a3c80c7a4f84bb50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a7ba4e28dd1064d9db7948d295d32d6d9e613428b9e3c8ba06a89dd35e143b(
    value: typing.Optional[typing.Union[FisExperimentTemplateActionParameter, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271bb7595b3cd263685ef0f05246da67b30ba9b7050b8c1a67a7f8d57d64085b(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564a0c00b8f74631c761438537d3851b6db29281bb89e84892b75b6ab5f3b749(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91a513dfd1bff54a1bae0f884e6a05d49acb7c14d0b5cbc6a9a5ae40850e4cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4716c966b019d6fc545f40c756f98d7919bb8a7f54cc59f0aa46c7f849ac4cdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea76e81fdab790e9deabcafa711270ce09f0a48ab9b7113af6d36727860104b5(
    value: typing.Optional[FisExperimentTemplateActionTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb79c51340f69266ae32516c341e0f8f1f8df3fd0f178f1c032d60efc0d24db(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateAction, typing.Dict[builtins.str, typing.Any]]]],
    description: builtins.str,
    role_arn: builtins.str,
    stop_condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateStopCondition, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[FisExperimentTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9be20f2acace1b0837001604faf60b54cef0a5571b567c0392f2239cf3715b(
    *,
    source: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2158e3be5811ce246ab7b40503852f07d9cff7dc42673d7d20a0e353c02997f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df53126c8d18fad1ec0c22df34246328a2f1ad5490999cc9c79335f693a65e05(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e3329ade06e13e14fbb726da3170ac9779f64578a25978f62a01957a7f8bbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6285faf5a8af8445b96e4e018d625d44c3ca8b5d649e5b28b2c3d85a9f2f14c6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0aa4311ffe01a5efdb6d7c28a483751ff02309a9133ac611469243a776d248d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645dc66f4f9534c13b2ae2e2c145c21d1ddb445dd26d10e51d0fa90218170f16(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateStopCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7146693dc39b7b55361389eab14fdaae2c91c969a869403b06438ca40cc3df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641f6d8f026c83121c8f6981a78e7c2ae6bad40e2460e77bc2584b57eed00347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abdc428a8f03e96ec365a84f9f158b9ace9ed6ce92d6f4fd09c9c36b1472d720(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9916d1cb7201d29656b00847141f43a941f76cc01a9a9ddb795bff423d46f971(
    value: typing.Optional[typing.Union[FisExperimentTemplateStopCondition, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97993927574dcf7637e00d2e87ef614b3bd14be16d5e691d48ee5caaed844c56(
    *,
    name: builtins.str,
    resource_type: builtins.str,
    selection_mode: builtins.str,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTargetFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTargetResourceTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2879ca49dda0aaaa1e5a7f68d1d75216f0cf54737dd80fbddf2950df7c41e2f8(
    *,
    path: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e580dcfc9cc09ef6fac896ecd8aaa50f258c7a3a67bbd2a0b212177e8c49ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4490c87255f2a5dcc392d9b2202339180c7d35d70d595e6667e85c0cf226cff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e139e46b2fe08aad69445cd2c21f3114fa778e674117630c219344481304c5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd1546702c9746a133db8903535ad0c9bf97f5f75af00aedab0a1f7ae7293fb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b341947f953035d75611b192cd977f0aabea4fb43d9085d14b0a15c8c655ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f1ab5fd8bcf4c9437eb5c06b169235074c8872b327d431a63c57d166448ba7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2746868dcf5b79b79500188c9cb2e79ba7cc880e07edf6837112ccabdbc804(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087c0071b18825e32ff3a9cd841acbf7a47677b7380d16f2a66acd7337964c90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1eb1325329473248df95861795229bec7bea98cf02edadf599bfd1d4ccfa63(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8a16f4c7c563a73659d65f853d271dbdc4ce4250d9a24d1d1b5ef5f16319c1(
    value: typing.Optional[typing.Union[FisExperimentTemplateTargetFilter, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575ae3857671da98fe1193770af4e48300f2e234dc81ad32165a19d5bc6ceac7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3537a2db7ced52f89aaf212fb3c2fb962cddcaa2027c2f3f88036caf39d5b2c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33804de8dff43297a9f7ca8f218132ad1af866daa6914cab8f17b3e2be92437(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25afc49b18f50ce90b9539a1414a70f15170a5f7bc378dced58db60d2fea0eb7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5af1085d82dcb80a27dde6bd8b0b605b8ef9e59e348989f0c3aa201bf60c2d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1874901a030b99c13aa6118ca27437e5848a4f13e7266f21dd8be101c74050da(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96fa89a13c9dbced27a032420c28e58402be8e14a3ace9bd746ca9ff70b01195(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ebfe6a45318d17f3627cd4a2ff363855a8bfc42a20932cef290768bd95116e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTargetFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7fd896825708248f1f8a830b0c075ecdc3d15feb9cd92a186711a256fe43c3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTargetResourceTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030107ca4a3ff327c48fef325f18ecab9bf76f949722a31099dd6a3585c05a05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74431df6357a64f417c8211ae463664ca8f17ea279e13e737d0bc5b318c0b76e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e7ea882d4d3876674c89e5f8da57dd1b6c0936454e7a3bcb8fa43148854d34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2191dcf652fe995a21fba1caa5c945e2e2c1baac0a24fe860ac038138e1754d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfb13bd71cba28746c0a02ef1f99e70d22e44b885aadb1fb599bc602f585435(
    value: typing.Optional[typing.Union[FisExperimentTemplateTarget, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96cd0457a4eb10458b8a50abc119af79a1fbb88419c031ef3ab8290ee4ff549(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f287db3e2610c858a05c626da9fedba7c97aee4902a0d01d6bb2bf3265276265(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39323d35e8b994c4c7a9f24dbd940861f76a438cf95358b1bb42f4d5633d861(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f2791f7155c84736464c9e442afa27d3328fede61469c7a0b2d5ab625f242a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2121a31a7488a824e8bca21e350c0bdbc50b5848f7d20ba19c37c58c6d162f05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6e1f265b035e6c2a77929539465a4bff2904a99d164cc1b85285555a9c6571(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329727619979022caa5f88617ab39f12ed0538311cdb76c19d6f984a1fe9a16c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetResourceTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3dff3e87657353cb6e54797600173936b9d65474d181f9417b8db21a76aef4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd09f6840a24839599e1b883e4c4c87d858696a7031c2d34d304c8386e813ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0731a531dcbb7427c29ee1a95b06cb0bbe76b5603a64b0a6890081db726460(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477140c69a0118d275aca43c7890a1ecb5d61e617096ea674207f3623a4ccbda(
    value: typing.Optional[typing.Union[FisExperimentTemplateTargetResourceTag, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bcd3d6b912c7b5f17a936e92823fce6113e12a18e5b1655b8f76842bfbfca8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646f8ffe97cd95013ca6ad12432cc8f75a0ee3bc2b29e59bf329cb24966b54dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0a07e6f47c09733ec7b5f3f40a413138e7c126a612b88260c5c42faa1b29cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46643f85c953cd3469feec5d52f6d846b9cddef3fe31a4808ddc6be6751db31b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891f36a52abfc2f83e28b09f973f86c7ce153c3ebffd9561c0a1ae6d7de5a832(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f330f3a7e8e3994783f5e76697b9e52fc564ea52dd2e016aaccd59739d53993(
    value: typing.Optional[typing.Union[FisExperimentTemplateTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
