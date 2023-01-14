'''
# `aws_batch_job_definition`

Refer to the Terraform Registory for docs: [`aws_batch_job_definition`](https://www.terraform.io/docs/providers/aws/r/batch_job_definition).
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


class BatchJobDefinition(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.batchJobDefinition.BatchJobDefinition",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition aws_batch_job_definition}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        container_properties: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        platform_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        propagate_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_strategy: typing.Optional[typing.Union["BatchJobDefinitionRetryStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[typing.Union["BatchJobDefinitionTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition aws_batch_job_definition} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#name BatchJobDefinition#name}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#type BatchJobDefinition#type}.
        :param container_properties: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#container_properties BatchJobDefinition#container_properties}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#id BatchJobDefinition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parameters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#parameters BatchJobDefinition#parameters}.
        :param platform_capabilities: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#platform_capabilities BatchJobDefinition#platform_capabilities}.
        :param propagate_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#propagate_tags BatchJobDefinition#propagate_tags}.
        :param retry_strategy: retry_strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#retry_strategy BatchJobDefinition#retry_strategy}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#tags BatchJobDefinition#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#tags_all BatchJobDefinition#tags_all}.
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#timeout BatchJobDefinition#timeout}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309cabf3e9ee844cfd674ae546007b49fa8b2cc318470a02de1f28a9a9407ffc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BatchJobDefinitionConfig(
            name=name,
            type=type,
            container_properties=container_properties,
            id=id,
            parameters=parameters,
            platform_capabilities=platform_capabilities,
            propagate_tags=propagate_tags,
            retry_strategy=retry_strategy,
            tags=tags,
            tags_all=tags_all,
            timeout=timeout,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putRetryStrategy")
    def put_retry_strategy(
        self,
        *,
        attempts: typing.Optional[jsii.Number] = None,
        evaluate_on_exit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchJobDefinitionRetryStrategyEvaluateOnExit", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param attempts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#attempts BatchJobDefinition#attempts}.
        :param evaluate_on_exit: evaluate_on_exit block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#evaluate_on_exit BatchJobDefinition#evaluate_on_exit}
        '''
        value = BatchJobDefinitionRetryStrategy(
            attempts=attempts, evaluate_on_exit=evaluate_on_exit
        )

        return typing.cast(None, jsii.invoke(self, "putRetryStrategy", [value]))

    @jsii.member(jsii_name="putTimeout")
    def put_timeout(
        self,
        *,
        attempt_duration_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param attempt_duration_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#attempt_duration_seconds BatchJobDefinition#attempt_duration_seconds}.
        '''
        value = BatchJobDefinitionTimeout(
            attempt_duration_seconds=attempt_duration_seconds
        )

        return typing.cast(None, jsii.invoke(self, "putTimeout", [value]))

    @jsii.member(jsii_name="resetContainerProperties")
    def reset_container_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerProperties", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetPlatformCapabilities")
    def reset_platform_capabilities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformCapabilities", []))

    @jsii.member(jsii_name="resetPropagateTags")
    def reset_propagate_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropagateTags", []))

    @jsii.member(jsii_name="resetRetryStrategy")
    def reset_retry_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryStrategy", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

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
    @jsii.member(jsii_name="retryStrategy")
    def retry_strategy(self) -> "BatchJobDefinitionRetryStrategyOutputReference":
        return typing.cast("BatchJobDefinitionRetryStrategyOutputReference", jsii.get(self, "retryStrategy"))

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "revision"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> "BatchJobDefinitionTimeoutOutputReference":
        return typing.cast("BatchJobDefinitionTimeoutOutputReference", jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="containerPropertiesInput")
    def container_properties_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="platformCapabilitiesInput")
    def platform_capabilities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "platformCapabilitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="propagateTagsInput")
    def propagate_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "propagateTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="retryStrategyInput")
    def retry_strategy_input(
        self,
    ) -> typing.Optional["BatchJobDefinitionRetryStrategy"]:
        return typing.cast(typing.Optional["BatchJobDefinitionRetryStrategy"], jsii.get(self, "retryStrategyInput"))

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
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional["BatchJobDefinitionTimeout"]:
        return typing.cast(typing.Optional["BatchJobDefinitionTimeout"], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="containerProperties")
    def container_properties(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerProperties"))

    @container_properties.setter
    def container_properties(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ba6db631c7736448eb517f14f12e50b65a7a6a13e164a5ee3b79c6ff5e9f5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerProperties", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b0d5ab0f2af9a0cdee72e56439cf7faabb7870e45e3d4a4987d4aa48b24935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55538cf5d80e83851e90931af174cf2e1bd82f3248f43b223b092cff802a3939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98582ddda188d8b868759e614df65b6ffbaa77358ac2b4eed54243ae71e9ca4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="platformCapabilities")
    def platform_capabilities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "platformCapabilities"))

    @platform_capabilities.setter
    def platform_capabilities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519f13404c965347952a7414caf20903788dfa4d1b0d0a18621efaac2bc1c853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformCapabilities", value)

    @builtins.property
    @jsii.member(jsii_name="propagateTags")
    def propagate_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "propagateTags"))

    @propagate_tags.setter
    def propagate_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9aa5d4c006ddcd65684d1ced1fed76f80c1660f8e1035233e36b0d610900902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propagateTags", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb94fcc15cd43aa4c58274b424f372c945eb89aaff01dbdf6433344e4bd7ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c064c908b635c7315acf59ae89ccf8e01c2ccb7bea07e4eca73fb57dd69c39fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7bfb607530ea180a1a2786189bda94e4f666cc86a5e9ff8d8bdcc04256c585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.batchJobDefinition.BatchJobDefinitionConfig",
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
        "type": "type",
        "container_properties": "containerProperties",
        "id": "id",
        "parameters": "parameters",
        "platform_capabilities": "platformCapabilities",
        "propagate_tags": "propagateTags",
        "retry_strategy": "retryStrategy",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeout": "timeout",
    },
)
class BatchJobDefinitionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        type: builtins.str,
        container_properties: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        platform_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        propagate_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_strategy: typing.Optional[typing.Union["BatchJobDefinitionRetryStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[typing.Union["BatchJobDefinitionTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#name BatchJobDefinition#name}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#type BatchJobDefinition#type}.
        :param container_properties: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#container_properties BatchJobDefinition#container_properties}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#id BatchJobDefinition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parameters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#parameters BatchJobDefinition#parameters}.
        :param platform_capabilities: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#platform_capabilities BatchJobDefinition#platform_capabilities}.
        :param propagate_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#propagate_tags BatchJobDefinition#propagate_tags}.
        :param retry_strategy: retry_strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#retry_strategy BatchJobDefinition#retry_strategy}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#tags BatchJobDefinition#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#tags_all BatchJobDefinition#tags_all}.
        :param timeout: timeout block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#timeout BatchJobDefinition#timeout}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(retry_strategy, dict):
            retry_strategy = BatchJobDefinitionRetryStrategy(**retry_strategy)
        if isinstance(timeout, dict):
            timeout = BatchJobDefinitionTimeout(**timeout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f827f6a9b3e925d2fab5aaa85cd112c1fa6821d3bd1c9a9ca4f5a35ea458e95)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument container_properties", value=container_properties, expected_type=type_hints["container_properties"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument platform_capabilities", value=platform_capabilities, expected_type=type_hints["platform_capabilities"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument retry_strategy", value=retry_strategy, expected_type=type_hints["retry_strategy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
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
        if container_properties is not None:
            self._values["container_properties"] = container_properties
        if id is not None:
            self._values["id"] = id
        if parameters is not None:
            self._values["parameters"] = parameters
        if platform_capabilities is not None:
            self._values["platform_capabilities"] = platform_capabilities
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if retry_strategy is not None:
            self._values["retry_strategy"] = retry_strategy
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeout is not None:
            self._values["timeout"] = timeout

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#name BatchJobDefinition#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#type BatchJobDefinition#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_properties(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#container_properties BatchJobDefinition#container_properties}.'''
        result = self._values.get("container_properties")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#id BatchJobDefinition#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#parameters BatchJobDefinition#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def platform_capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#platform_capabilities BatchJobDefinition#platform_capabilities}.'''
        result = self._values.get("platform_capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#propagate_tags BatchJobDefinition#propagate_tags}.'''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retry_strategy(self) -> typing.Optional["BatchJobDefinitionRetryStrategy"]:
        '''retry_strategy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#retry_strategy BatchJobDefinition#retry_strategy}
        '''
        result = self._values.get("retry_strategy")
        return typing.cast(typing.Optional["BatchJobDefinitionRetryStrategy"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#tags BatchJobDefinition#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#tags_all BatchJobDefinition#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional["BatchJobDefinitionTimeout"]:
        '''timeout block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#timeout BatchJobDefinition#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["BatchJobDefinitionTimeout"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchJobDefinitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.batchJobDefinition.BatchJobDefinitionRetryStrategy",
    jsii_struct_bases=[],
    name_mapping={"attempts": "attempts", "evaluate_on_exit": "evaluateOnExit"},
)
class BatchJobDefinitionRetryStrategy:
    def __init__(
        self,
        *,
        attempts: typing.Optional[jsii.Number] = None,
        evaluate_on_exit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BatchJobDefinitionRetryStrategyEvaluateOnExit", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param attempts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#attempts BatchJobDefinition#attempts}.
        :param evaluate_on_exit: evaluate_on_exit block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#evaluate_on_exit BatchJobDefinition#evaluate_on_exit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882a19ae7d68f6746f2171ae969ab7c258c2e77162e6b232b3503536715c15ae)
            check_type(argname="argument attempts", value=attempts, expected_type=type_hints["attempts"])
            check_type(argname="argument evaluate_on_exit", value=evaluate_on_exit, expected_type=type_hints["evaluate_on_exit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attempts is not None:
            self._values["attempts"] = attempts
        if evaluate_on_exit is not None:
            self._values["evaluate_on_exit"] = evaluate_on_exit

    @builtins.property
    def attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#attempts BatchJobDefinition#attempts}.'''
        result = self._values.get("attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluate_on_exit(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchJobDefinitionRetryStrategyEvaluateOnExit"]]]:
        '''evaluate_on_exit block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#evaluate_on_exit BatchJobDefinition#evaluate_on_exit}
        '''
        result = self._values.get("evaluate_on_exit")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BatchJobDefinitionRetryStrategyEvaluateOnExit"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchJobDefinitionRetryStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.batchJobDefinition.BatchJobDefinitionRetryStrategyEvaluateOnExit",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "on_exit_code": "onExitCode",
        "on_reason": "onReason",
        "on_status_reason": "onStatusReason",
    },
)
class BatchJobDefinitionRetryStrategyEvaluateOnExit:
    def __init__(
        self,
        *,
        action: builtins.str,
        on_exit_code: typing.Optional[builtins.str] = None,
        on_reason: typing.Optional[builtins.str] = None,
        on_status_reason: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#action BatchJobDefinition#action}.
        :param on_exit_code: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#on_exit_code BatchJobDefinition#on_exit_code}.
        :param on_reason: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#on_reason BatchJobDefinition#on_reason}.
        :param on_status_reason: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#on_status_reason BatchJobDefinition#on_status_reason}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a19769c75f18255518ef4be17db6306d9d56e51b45a70907e45ab082618fe0)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument on_exit_code", value=on_exit_code, expected_type=type_hints["on_exit_code"])
            check_type(argname="argument on_reason", value=on_reason, expected_type=type_hints["on_reason"])
            check_type(argname="argument on_status_reason", value=on_status_reason, expected_type=type_hints["on_status_reason"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
        }
        if on_exit_code is not None:
            self._values["on_exit_code"] = on_exit_code
        if on_reason is not None:
            self._values["on_reason"] = on_reason
        if on_status_reason is not None:
            self._values["on_status_reason"] = on_status_reason

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#action BatchJobDefinition#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def on_exit_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#on_exit_code BatchJobDefinition#on_exit_code}.'''
        result = self._values.get("on_exit_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_reason(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#on_reason BatchJobDefinition#on_reason}.'''
        result = self._values.get("on_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_status_reason(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#on_status_reason BatchJobDefinition#on_status_reason}.'''
        result = self._values.get("on_status_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchJobDefinitionRetryStrategyEvaluateOnExit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchJobDefinitionRetryStrategyEvaluateOnExitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.batchJobDefinition.BatchJobDefinitionRetryStrategyEvaluateOnExitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__682003c97e057f76c33c9bcfaf3cb9da3d0f22af79286dce2dc2519288f2436a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BatchJobDefinitionRetryStrategyEvaluateOnExitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd2f7c330a3ebf59ab9b516206d0a1a916dc0416ff49f817ea1664188b2a633)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BatchJobDefinitionRetryStrategyEvaluateOnExitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5738c9755f66790b0408df06796043d5ef6471c33b854817a0ce8b0e120825d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01db207383caa4c1b71ea8f0c8727cd2cb924d6f60515829f9f5e3a61feae5a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bfe6c4b87014403482f89acdab3b1ada9cdbc0b173c15dcd19d3184efe35ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchJobDefinitionRetryStrategyEvaluateOnExit]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchJobDefinitionRetryStrategyEvaluateOnExit]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchJobDefinitionRetryStrategyEvaluateOnExit]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ec6ef47a0ed76c14c4f6ffcdfea3f979047fc90178b122df9b395b8fb99dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BatchJobDefinitionRetryStrategyEvaluateOnExitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.batchJobDefinition.BatchJobDefinitionRetryStrategyEvaluateOnExitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__691bb0845d3622e20449c1b2d79d1aec745f137565121f85bc5785c9ab16bb43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOnExitCode")
    def reset_on_exit_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnExitCode", []))

    @jsii.member(jsii_name="resetOnReason")
    def reset_on_reason(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnReason", []))

    @jsii.member(jsii_name="resetOnStatusReason")
    def reset_on_status_reason(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnStatusReason", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="onExitCodeInput")
    def on_exit_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onExitCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="onReasonInput")
    def on_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="onStatusReasonInput")
    def on_status_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onStatusReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d110dab592168ec440b1da39150a170e7b3909bf9bbe16bff671da8ef3a1ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="onExitCode")
    def on_exit_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onExitCode"))

    @on_exit_code.setter
    def on_exit_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd4299d582a358092d6b2d8e7a06f280c5d9a523696c4b7ca5336d477342031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onExitCode", value)

    @builtins.property
    @jsii.member(jsii_name="onReason")
    def on_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onReason"))

    @on_reason.setter
    def on_reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5190a31957fdb3bb87b176e6a5d0aa6739860cfd0a59c3554936a375e1c893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onReason", value)

    @builtins.property
    @jsii.member(jsii_name="onStatusReason")
    def on_status_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onStatusReason"))

    @on_status_reason.setter
    def on_status_reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ccdbc6fb2304a38f985b24ff79413a9e03b77e43898b31db4e03bf9a1d3f7fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onStatusReason", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[BatchJobDefinitionRetryStrategyEvaluateOnExit, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BatchJobDefinitionRetryStrategyEvaluateOnExit, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BatchJobDefinitionRetryStrategyEvaluateOnExit, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a5930b3613d0b13a8dd59f849f9c20ec7b161e09bf29beb7d3f5d149b5e808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BatchJobDefinitionRetryStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.batchJobDefinition.BatchJobDefinitionRetryStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6d946a66082a6a77bb9beeb9a41542b22ae5c9897f015789d2d83dc30f463fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEvaluateOnExit")
    def put_evaluate_on_exit(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchJobDefinitionRetryStrategyEvaluateOnExit, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2bb16c86b9740bf862e32d6f0f3b0ba6ad82020cb2a388efebfb3130a380294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEvaluateOnExit", [value]))

    @jsii.member(jsii_name="resetAttempts")
    def reset_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttempts", []))

    @jsii.member(jsii_name="resetEvaluateOnExit")
    def reset_evaluate_on_exit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluateOnExit", []))

    @builtins.property
    @jsii.member(jsii_name="evaluateOnExit")
    def evaluate_on_exit(self) -> BatchJobDefinitionRetryStrategyEvaluateOnExitList:
        return typing.cast(BatchJobDefinitionRetryStrategyEvaluateOnExitList, jsii.get(self, "evaluateOnExit"))

    @builtins.property
    @jsii.member(jsii_name="attemptsInput")
    def attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "attemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluateOnExitInput")
    def evaluate_on_exit_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchJobDefinitionRetryStrategyEvaluateOnExit]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchJobDefinitionRetryStrategyEvaluateOnExit]]], jsii.get(self, "evaluateOnExitInput"))

    @builtins.property
    @jsii.member(jsii_name="attempts")
    def attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "attempts"))

    @attempts.setter
    def attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06a0ae4ea422aeb7ff3648828f83a2e539ae4b79e18b197f69a842c63883009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attempts", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchJobDefinitionRetryStrategy]:
        return typing.cast(typing.Optional[BatchJobDefinitionRetryStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BatchJobDefinitionRetryStrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd629ef55dfacb172db0d621c13eec7e2aeab22222603a0e752e1023df1d93b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.batchJobDefinition.BatchJobDefinitionTimeout",
    jsii_struct_bases=[],
    name_mapping={"attempt_duration_seconds": "attemptDurationSeconds"},
)
class BatchJobDefinitionTimeout:
    def __init__(
        self,
        *,
        attempt_duration_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param attempt_duration_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#attempt_duration_seconds BatchJobDefinition#attempt_duration_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a201c164549a6819088b01f4c4ffade6627d3e9d06046831908faccf7e67674)
            check_type(argname="argument attempt_duration_seconds", value=attempt_duration_seconds, expected_type=type_hints["attempt_duration_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attempt_duration_seconds is not None:
            self._values["attempt_duration_seconds"] = attempt_duration_seconds

    @builtins.property
    def attempt_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/batch_job_definition#attempt_duration_seconds BatchJobDefinition#attempt_duration_seconds}.'''
        result = self._values.get("attempt_duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchJobDefinitionTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BatchJobDefinitionTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.batchJobDefinition.BatchJobDefinitionTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__313ecd197fa562f9966cf7cadf7fcb1b7407c388808026660be0b86fb77ac270)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAttemptDurationSeconds")
    def reset_attempt_duration_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttemptDurationSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="attemptDurationSecondsInput")
    def attempt_duration_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "attemptDurationSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="attemptDurationSeconds")
    def attempt_duration_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "attemptDurationSeconds"))

    @attempt_duration_seconds.setter
    def attempt_duration_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dea36cdd8d4a19d4a3af19a6ffa3193fb9256680c31b614e704c6e054446e7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attemptDurationSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BatchJobDefinitionTimeout]:
        return typing.cast(typing.Optional[BatchJobDefinitionTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BatchJobDefinitionTimeout]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a21974aab07796e5e58c14ef2481b4b4c86a82ec7a9a972295046b9608dfb1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "BatchJobDefinition",
    "BatchJobDefinitionConfig",
    "BatchJobDefinitionRetryStrategy",
    "BatchJobDefinitionRetryStrategyEvaluateOnExit",
    "BatchJobDefinitionRetryStrategyEvaluateOnExitList",
    "BatchJobDefinitionRetryStrategyEvaluateOnExitOutputReference",
    "BatchJobDefinitionRetryStrategyOutputReference",
    "BatchJobDefinitionTimeout",
    "BatchJobDefinitionTimeoutOutputReference",
]

publication.publish()

def _typecheckingstub__309cabf3e9ee844cfd674ae546007b49fa8b2cc318470a02de1f28a9a9407ffc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    container_properties: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    platform_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    propagate_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retry_strategy: typing.Optional[typing.Union[BatchJobDefinitionRetryStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[typing.Union[BatchJobDefinitionTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__77ba6db631c7736448eb517f14f12e50b65a7a6a13e164a5ee3b79c6ff5e9f5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b0d5ab0f2af9a0cdee72e56439cf7faabb7870e45e3d4a4987d4aa48b24935(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55538cf5d80e83851e90931af174cf2e1bd82f3248f43b223b092cff802a3939(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98582ddda188d8b868759e614df65b6ffbaa77358ac2b4eed54243ae71e9ca4d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519f13404c965347952a7414caf20903788dfa4d1b0d0a18621efaac2bc1c853(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9aa5d4c006ddcd65684d1ced1fed76f80c1660f8e1035233e36b0d610900902(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb94fcc15cd43aa4c58274b424f372c945eb89aaff01dbdf6433344e4bd7ef8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c064c908b635c7315acf59ae89ccf8e01c2ccb7bea07e4eca73fb57dd69c39fc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7bfb607530ea180a1a2786189bda94e4f666cc86a5e9ff8d8bdcc04256c585(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f827f6a9b3e925d2fab5aaa85cd112c1fa6821d3bd1c9a9ca4f5a35ea458e95(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    type: builtins.str,
    container_properties: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    platform_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    propagate_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retry_strategy: typing.Optional[typing.Union[BatchJobDefinitionRetryStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[typing.Union[BatchJobDefinitionTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882a19ae7d68f6746f2171ae969ab7c258c2e77162e6b232b3503536715c15ae(
    *,
    attempts: typing.Optional[jsii.Number] = None,
    evaluate_on_exit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchJobDefinitionRetryStrategyEvaluateOnExit, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a19769c75f18255518ef4be17db6306d9d56e51b45a70907e45ab082618fe0(
    *,
    action: builtins.str,
    on_exit_code: typing.Optional[builtins.str] = None,
    on_reason: typing.Optional[builtins.str] = None,
    on_status_reason: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682003c97e057f76c33c9bcfaf3cb9da3d0f22af79286dce2dc2519288f2436a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd2f7c330a3ebf59ab9b516206d0a1a916dc0416ff49f817ea1664188b2a633(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5738c9755f66790b0408df06796043d5ef6471c33b854817a0ce8b0e120825d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01db207383caa4c1b71ea8f0c8727cd2cb924d6f60515829f9f5e3a61feae5a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfe6c4b87014403482f89acdab3b1ada9cdbc0b173c15dcd19d3184efe35ce3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ec6ef47a0ed76c14c4f6ffcdfea3f979047fc90178b122df9b395b8fb99dd6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BatchJobDefinitionRetryStrategyEvaluateOnExit]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691bb0845d3622e20449c1b2d79d1aec745f137565121f85bc5785c9ab16bb43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d110dab592168ec440b1da39150a170e7b3909bf9bbe16bff671da8ef3a1ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd4299d582a358092d6b2d8e7a06f280c5d9a523696c4b7ca5336d477342031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5190a31957fdb3bb87b176e6a5d0aa6739860cfd0a59c3554936a375e1c893(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccdbc6fb2304a38f985b24ff79413a9e03b77e43898b31db4e03bf9a1d3f7fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a5930b3613d0b13a8dd59f849f9c20ec7b161e09bf29beb7d3f5d149b5e808(
    value: typing.Optional[typing.Union[BatchJobDefinitionRetryStrategyEvaluateOnExit, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d946a66082a6a77bb9beeb9a41542b22ae5c9897f015789d2d83dc30f463fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bb16c86b9740bf862e32d6f0f3b0ba6ad82020cb2a388efebfb3130a380294(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BatchJobDefinitionRetryStrategyEvaluateOnExit, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06a0ae4ea422aeb7ff3648828f83a2e539ae4b79e18b197f69a842c63883009(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd629ef55dfacb172db0d621c13eec7e2aeab22222603a0e752e1023df1d93b7(
    value: typing.Optional[BatchJobDefinitionRetryStrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a201c164549a6819088b01f4c4ffade6627d3e9d06046831908faccf7e67674(
    *,
    attempt_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313ecd197fa562f9966cf7cadf7fcb1b7407c388808026660be0b86fb77ac270(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dea36cdd8d4a19d4a3af19a6ffa3193fb9256680c31b614e704c6e054446e7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a21974aab07796e5e58c14ef2481b4b4c86a82ec7a9a972295046b9608dfb1c(
    value: typing.Optional[BatchJobDefinitionTimeout],
) -> None:
    """Type checking stubs"""
    pass
