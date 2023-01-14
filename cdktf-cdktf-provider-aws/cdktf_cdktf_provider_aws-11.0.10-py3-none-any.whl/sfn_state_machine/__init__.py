'''
# `aws_sfn_state_machine`

Refer to the Terraform Registory for docs: [`aws_sfn_state_machine`](https://www.terraform.io/docs/providers/aws/r/sfn_state_machine).
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


class SfnStateMachine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sfnStateMachine.SfnStateMachine",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine aws_sfn_state_machine}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        definition: builtins.str,
        role_arn: builtins.str,
        id: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union["SfnStateMachineLoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing_configuration: typing.Optional[typing.Union["SfnStateMachineTracingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine aws_sfn_state_machine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param definition: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#definition SfnStateMachine#definition}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#role_arn SfnStateMachine#role_arn}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#id SfnStateMachine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_configuration: logging_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#logging_configuration SfnStateMachine#logging_configuration}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#name SfnStateMachine#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#name_prefix SfnStateMachine#name_prefix}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#tags SfnStateMachine#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#tags_all SfnStateMachine#tags_all}.
        :param tracing_configuration: tracing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#tracing_configuration SfnStateMachine#tracing_configuration}
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#type SfnStateMachine#type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__781d02a1556191b8481a489bf9a7accdcefcb2379fa489e8e9fd927fbde21bed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SfnStateMachineConfig(
            definition=definition,
            role_arn=role_arn,
            id=id,
            logging_configuration=logging_configuration,
            name=name,
            name_prefix=name_prefix,
            tags=tags,
            tags_all=tags_all,
            tracing_configuration=tracing_configuration,
            type=type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putLoggingConfiguration")
    def put_logging_configuration(
        self,
        *,
        include_execution_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        level: typing.Optional[builtins.str] = None,
        log_destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param include_execution_data: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#include_execution_data SfnStateMachine#include_execution_data}.
        :param level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#level SfnStateMachine#level}.
        :param log_destination: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#log_destination SfnStateMachine#log_destination}.
        '''
        value = SfnStateMachineLoggingConfiguration(
            include_execution_data=include_execution_data,
            level=level,
            log_destination=log_destination,
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfiguration", [value]))

    @jsii.member(jsii_name="putTracingConfiguration")
    def put_tracing_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#enabled SfnStateMachine#enabled}.
        '''
        value = SfnStateMachineTracingConfiguration(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putTracingConfiguration", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoggingConfiguration")
    def reset_logging_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfiguration", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTracingConfiguration")
    def reset_tracing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTracingConfiguration", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="creationDate")
    def creation_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationDate"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfiguration")
    def logging_configuration(
        self,
    ) -> "SfnStateMachineLoggingConfigurationOutputReference":
        return typing.cast("SfnStateMachineLoggingConfigurationOutputReference", jsii.get(self, "loggingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="tracingConfiguration")
    def tracing_configuration(
        self,
    ) -> "SfnStateMachineTracingConfigurationOutputReference":
        return typing.cast("SfnStateMachineTracingConfigurationOutputReference", jsii.get(self, "tracingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="definitionInput")
    def definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "definitionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigurationInput")
    def logging_configuration_input(
        self,
    ) -> typing.Optional["SfnStateMachineLoggingConfiguration"]:
        return typing.cast(typing.Optional["SfnStateMachineLoggingConfiguration"], jsii.get(self, "loggingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

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
    @jsii.member(jsii_name="tracingConfigurationInput")
    def tracing_configuration_input(
        self,
    ) -> typing.Optional["SfnStateMachineTracingConfiguration"]:
        return typing.cast(typing.Optional["SfnStateMachineTracingConfiguration"], jsii.get(self, "tracingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "definition"))

    @definition.setter
    def definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f2be8c05db67e4481285f7f32c781d424b994fb98256e641e82e6e701591df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4deb1dd20b0f1ad615e2db30f66f78e6bd2d227bb9540a873b4b30a92b2ffd6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d5826169daf4efd00e81ef4ef9716f215df54741a0eac9f43f021c5466a3d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4dfb74944908a5a9dedc5d68c370a58c64c443a3765bbc78b8edb8d1c3a4a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8394ce5726f793ff5e453a9f931bd5bdc51b9c25e247bbe5a72815343f1afb7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68eee6bbe3a0c8124d184ad855c2256f835ebd47db48399c2431961fc8bf9d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c0bc704dce22818ffa71fb8dd67b0be7ce27809a820876f1d7683cfbcedc05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2174206262c522dad3c97ca19ae7a78a008768f9132a8e5619bf5b13e2f44f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sfnStateMachine.SfnStateMachineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "definition": "definition",
        "role_arn": "roleArn",
        "id": "id",
        "logging_configuration": "loggingConfiguration",
        "name": "name",
        "name_prefix": "namePrefix",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tracing_configuration": "tracingConfiguration",
        "type": "type",
    },
)
class SfnStateMachineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        definition: builtins.str,
        role_arn: builtins.str,
        id: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union["SfnStateMachineLoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tracing_configuration: typing.Optional[typing.Union["SfnStateMachineTracingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param definition: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#definition SfnStateMachine#definition}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#role_arn SfnStateMachine#role_arn}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#id SfnStateMachine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_configuration: logging_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#logging_configuration SfnStateMachine#logging_configuration}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#name SfnStateMachine#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#name_prefix SfnStateMachine#name_prefix}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#tags SfnStateMachine#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#tags_all SfnStateMachine#tags_all}.
        :param tracing_configuration: tracing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#tracing_configuration SfnStateMachine#tracing_configuration}
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#type SfnStateMachine#type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(logging_configuration, dict):
            logging_configuration = SfnStateMachineLoggingConfiguration(**logging_configuration)
        if isinstance(tracing_configuration, dict):
            tracing_configuration = SfnStateMachineTracingConfiguration(**tracing_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9a8e877b616f15eec935564f14c83704eb031da1d970f46027eba67e096f2f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tracing_configuration", value=tracing_configuration, expected_type=type_hints["tracing_configuration"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
            "role_arn": role_arn,
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
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tracing_configuration is not None:
            self._values["tracing_configuration"] = tracing_configuration
        if type is not None:
            self._values["type"] = type

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
    def definition(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#definition SfnStateMachine#definition}.'''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#role_arn SfnStateMachine#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#id SfnStateMachine#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional["SfnStateMachineLoggingConfiguration"]:
        '''logging_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#logging_configuration SfnStateMachine#logging_configuration}
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional["SfnStateMachineLoggingConfiguration"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#name SfnStateMachine#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#name_prefix SfnStateMachine#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#tags SfnStateMachine#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#tags_all SfnStateMachine#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tracing_configuration(
        self,
    ) -> typing.Optional["SfnStateMachineTracingConfiguration"]:
        '''tracing_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#tracing_configuration SfnStateMachine#tracing_configuration}
        '''
        result = self._values.get("tracing_configuration")
        return typing.cast(typing.Optional["SfnStateMachineTracingConfiguration"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#type SfnStateMachine#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SfnStateMachineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sfnStateMachine.SfnStateMachineLoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "include_execution_data": "includeExecutionData",
        "level": "level",
        "log_destination": "logDestination",
    },
)
class SfnStateMachineLoggingConfiguration:
    def __init__(
        self,
        *,
        include_execution_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        level: typing.Optional[builtins.str] = None,
        log_destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param include_execution_data: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#include_execution_data SfnStateMachine#include_execution_data}.
        :param level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#level SfnStateMachine#level}.
        :param log_destination: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#log_destination SfnStateMachine#log_destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1a05bb56212ad581b7aa354aac4eb5aa3f21f19d8321cd062845ae7e123625)
            check_type(argname="argument include_execution_data", value=include_execution_data, expected_type=type_hints["include_execution_data"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument log_destination", value=log_destination, expected_type=type_hints["log_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_execution_data is not None:
            self._values["include_execution_data"] = include_execution_data
        if level is not None:
            self._values["level"] = level
        if log_destination is not None:
            self._values["log_destination"] = log_destination

    @builtins.property
    def include_execution_data(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#include_execution_data SfnStateMachine#include_execution_data}.'''
        result = self._values.get("include_execution_data")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#level SfnStateMachine#level}.'''
        result = self._values.get("level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_destination(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#log_destination SfnStateMachine#log_destination}.'''
        result = self._values.get("log_destination")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SfnStateMachineLoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SfnStateMachineLoggingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sfnStateMachine.SfnStateMachineLoggingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6d06d2f655aad8ea8b571a3a4ef7daa1caff44a16bbec5a88a122cae28a9a68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeExecutionData")
    def reset_include_execution_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeExecutionData", []))

    @jsii.member(jsii_name="resetLevel")
    def reset_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevel", []))

    @jsii.member(jsii_name="resetLogDestination")
    def reset_log_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDestination", []))

    @builtins.property
    @jsii.member(jsii_name="includeExecutionDataInput")
    def include_execution_data_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeExecutionDataInput"))

    @builtins.property
    @jsii.member(jsii_name="levelInput")
    def level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "levelInput"))

    @builtins.property
    @jsii.member(jsii_name="logDestinationInput")
    def log_destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="includeExecutionData")
    def include_execution_data(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeExecutionData"))

    @include_execution_data.setter
    def include_execution_data(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f15761ed96f11a5bac414ac43d1134c20eadc4c90d6651e552f8b207763b0dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeExecutionData", value)

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__092033129af27bd474fffbded8aa3feb86b607dbd27fb7b13cbe7f65e353bbb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value)

    @builtins.property
    @jsii.member(jsii_name="logDestination")
    def log_destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logDestination"))

    @log_destination.setter
    def log_destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967fdc84192a117679ca0c2961812a9796905520673a12af715ae47ef3a133c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDestination", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SfnStateMachineLoggingConfiguration]:
        return typing.cast(typing.Optional[SfnStateMachineLoggingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SfnStateMachineLoggingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a239335300dc852a546c10145f70be41e06e1f631e2432490280f4c7273f0d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sfnStateMachine.SfnStateMachineTracingConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class SfnStateMachineTracingConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#enabled SfnStateMachine#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e015adda61869a51421ed7d9aa0e5cd3e5664b6a20ef8a3373d2d2cc710de5)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sfn_state_machine#enabled SfnStateMachine#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SfnStateMachineTracingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SfnStateMachineTracingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sfnStateMachine.SfnStateMachineTracingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c8cae2a92fab5fb61b37adde857c01dcead1349503a5be34ad9566ee228efbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7e2bc3f03c2a461307c5a9c06c4dff0a97b6a15e927afc0d6fd5da30d4cc8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SfnStateMachineTracingConfiguration]:
        return typing.cast(typing.Optional[SfnStateMachineTracingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SfnStateMachineTracingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ab1757b0754939289a79c4f31575932a2ae193816e89a2cc5b6d963bf8875e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SfnStateMachine",
    "SfnStateMachineConfig",
    "SfnStateMachineLoggingConfiguration",
    "SfnStateMachineLoggingConfigurationOutputReference",
    "SfnStateMachineTracingConfiguration",
    "SfnStateMachineTracingConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__781d02a1556191b8481a489bf9a7accdcefcb2379fa489e8e9fd927fbde21bed(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    definition: builtins.str,
    role_arn: builtins.str,
    id: typing.Optional[builtins.str] = None,
    logging_configuration: typing.Optional[typing.Union[SfnStateMachineLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing_configuration: typing.Optional[typing.Union[SfnStateMachineTracingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__37f2be8c05db67e4481285f7f32c781d424b994fb98256e641e82e6e701591df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4deb1dd20b0f1ad615e2db30f66f78e6bd2d227bb9540a873b4b30a92b2ffd6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d5826169daf4efd00e81ef4ef9716f215df54741a0eac9f43f021c5466a3d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4dfb74944908a5a9dedc5d68c370a58c64c443a3765bbc78b8edb8d1c3a4a64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8394ce5726f793ff5e453a9f931bd5bdc51b9c25e247bbe5a72815343f1afb7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68eee6bbe3a0c8124d184ad855c2256f835ebd47db48399c2431961fc8bf9d52(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c0bc704dce22818ffa71fb8dd67b0be7ce27809a820876f1d7683cfbcedc05(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2174206262c522dad3c97ca19ae7a78a008768f9132a8e5619bf5b13e2f44f72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9a8e877b616f15eec935564f14c83704eb031da1d970f46027eba67e096f2f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    definition: builtins.str,
    role_arn: builtins.str,
    id: typing.Optional[builtins.str] = None,
    logging_configuration: typing.Optional[typing.Union[SfnStateMachineLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tracing_configuration: typing.Optional[typing.Union[SfnStateMachineTracingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1a05bb56212ad581b7aa354aac4eb5aa3f21f19d8321cd062845ae7e123625(
    *,
    include_execution_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    level: typing.Optional[builtins.str] = None,
    log_destination: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d06d2f655aad8ea8b571a3a4ef7daa1caff44a16bbec5a88a122cae28a9a68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f15761ed96f11a5bac414ac43d1134c20eadc4c90d6651e552f8b207763b0dc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__092033129af27bd474fffbded8aa3feb86b607dbd27fb7b13cbe7f65e353bbb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967fdc84192a117679ca0c2961812a9796905520673a12af715ae47ef3a133c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a239335300dc852a546c10145f70be41e06e1f631e2432490280f4c7273f0d45(
    value: typing.Optional[SfnStateMachineLoggingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e015adda61869a51421ed7d9aa0e5cd3e5664b6a20ef8a3373d2d2cc710de5(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8cae2a92fab5fb61b37adde857c01dcead1349503a5be34ad9566ee228efbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7e2bc3f03c2a461307c5a9c06c4dff0a97b6a15e927afc0d6fd5da30d4cc8c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ab1757b0754939289a79c4f31575932a2ae193816e89a2cc5b6d963bf8875e(
    value: typing.Optional[SfnStateMachineTracingConfiguration],
) -> None:
    """Type checking stubs"""
    pass
