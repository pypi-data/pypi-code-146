'''
# `aws_sagemaker_model`

Refer to the Terraform Registory for docs: [`aws_sagemaker_model`](https://www.terraform.io/docs/providers/aws/r/sagemaker_model).
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


class SagemakerModel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModel",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model aws_sagemaker_model}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        execution_role_arn: builtins.str,
        container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelContainer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        inference_execution_config: typing.Optional[typing.Union["SagemakerModelInferenceExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        primary_container: typing.Optional[typing.Union["SagemakerModelPrimaryContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_config: typing.Optional[typing.Union["SagemakerModelVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model aws_sagemaker_model} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param execution_role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#execution_role_arn SagemakerModel#execution_role_arn}.
        :param container: container block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#container SagemakerModel#container}
        :param enable_network_isolation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#enable_network_isolation SagemakerModel#enable_network_isolation}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#id SagemakerModel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inference_execution_config: inference_execution_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#inference_execution_config SagemakerModel#inference_execution_config}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#name SagemakerModel#name}.
        :param primary_container: primary_container block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#primary_container SagemakerModel#primary_container}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#tags SagemakerModel#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#tags_all SagemakerModel#tags_all}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#vpc_config SagemakerModel#vpc_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abe947e09f96e3915c2337aa9a84e5c3329a3e572460546560e618ed7afedf6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerModelConfig(
            execution_role_arn=execution_role_arn,
            container=container,
            enable_network_isolation=enable_network_isolation,
            id=id,
            inference_execution_config=inference_execution_config,
            name=name,
            primary_container=primary_container,
            tags=tags,
            tags_all=tags_all,
            vpc_config=vpc_config,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putContainer")
    def put_container(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelContainer", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3251d86e9d80695ac44d4b7884fa796a6607dbcec3b144894a0cd2c18829f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainer", [value]))

    @jsii.member(jsii_name="putInferenceExecutionConfig")
    def put_inference_execution_config(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#mode SagemakerModel#mode}.
        '''
        value = SagemakerModelInferenceExecutionConfig(mode=mode)

        return typing.cast(None, jsii.invoke(self, "putInferenceExecutionConfig", [value]))

    @jsii.member(jsii_name="putPrimaryContainer")
    def put_primary_container(
        self,
        *,
        image: builtins.str,
        container_hostname: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image_config: typing.Optional[typing.Union["SagemakerModelPrimaryContainerImageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        model_data_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#image SagemakerModel#image}.
        :param container_hostname: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#container_hostname SagemakerModel#container_hostname}.
        :param environment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#environment SagemakerModel#environment}.
        :param image_config: image_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#image_config SagemakerModel#image_config}
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#mode SagemakerModel#mode}.
        :param model_data_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#model_data_url SagemakerModel#model_data_url}.
        '''
        value = SagemakerModelPrimaryContainer(
            image=image,
            container_hostname=container_hostname,
            environment=environment,
            image_config=image_config,
            mode=mode,
            model_data_url=model_data_url,
        )

        return typing.cast(None, jsii.invoke(self, "putPrimaryContainer", [value]))

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#security_group_ids SagemakerModel#security_group_ids}.
        :param subnets: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#subnets SagemakerModel#subnets}.
        '''
        value = SagemakerModelVpcConfig(
            security_group_ids=security_group_ids, subnets=subnets
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @jsii.member(jsii_name="resetContainer")
    def reset_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainer", []))

    @jsii.member(jsii_name="resetEnableNetworkIsolation")
    def reset_enable_network_isolation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNetworkIsolation", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInferenceExecutionConfig")
    def reset_inference_execution_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceExecutionConfig", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPrimaryContainer")
    def reset_primary_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContainer", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetVpcConfig")
    def reset_vpc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConfig", []))

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
    @jsii.member(jsii_name="container")
    def container(self) -> "SagemakerModelContainerList":
        return typing.cast("SagemakerModelContainerList", jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="inferenceExecutionConfig")
    def inference_execution_config(
        self,
    ) -> "SagemakerModelInferenceExecutionConfigOutputReference":
        return typing.cast("SagemakerModelInferenceExecutionConfigOutputReference", jsii.get(self, "inferenceExecutionConfig"))

    @builtins.property
    @jsii.member(jsii_name="primaryContainer")
    def primary_container(self) -> "SagemakerModelPrimaryContainerOutputReference":
        return typing.cast("SagemakerModelPrimaryContainerOutputReference", jsii.get(self, "primaryContainer"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> "SagemakerModelVpcConfigOutputReference":
        return typing.cast("SagemakerModelVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainer"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainer"]]], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNetworkIsolationInput")
    def enable_network_isolation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNetworkIsolationInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArnInput")
    def execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceExecutionConfigInput")
    def inference_execution_config_input(
        self,
    ) -> typing.Optional["SagemakerModelInferenceExecutionConfig"]:
        return typing.cast(typing.Optional["SagemakerModelInferenceExecutionConfig"], jsii.get(self, "inferenceExecutionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContainerInput")
    def primary_container_input(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainer"]:
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainer"], jsii.get(self, "primaryContainerInput"))

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
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(self) -> typing.Optional["SagemakerModelVpcConfig"]:
        return typing.cast(typing.Optional["SagemakerModelVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNetworkIsolation")
    def enable_network_isolation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableNetworkIsolation"))

    @enable_network_isolation.setter
    def enable_network_isolation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a989662d8fbed9cc2adb46c558fb1fccd76e988a6f508b5cca4fca03dde8f07c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNetworkIsolation", value)

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5288f586e6db82049bb4321b9eefe66786411a66ab5660fd782e12ac986ad9d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69c13c6e28fe26e1643f2826b18b013245268996d8c4f3d6a92404c5331f207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df942a246b5c0915857323bb835df65e05f9d97bf2c6d9b04b4afa277666976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b20586f9f627a39d0d17355041bbdedac8e951d6b4e3dbd16e7f34254b803f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1400ea28b1d7c6619183865d8419be6d856bb2cfdd7b3ee3451a9f9cf117ee17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "execution_role_arn": "executionRoleArn",
        "container": "container",
        "enable_network_isolation": "enableNetworkIsolation",
        "id": "id",
        "inference_execution_config": "inferenceExecutionConfig",
        "name": "name",
        "primary_container": "primaryContainer",
        "tags": "tags",
        "tags_all": "tagsAll",
        "vpc_config": "vpcConfig",
    },
)
class SagemakerModelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        execution_role_arn: builtins.str,
        container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerModelContainer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        inference_execution_config: typing.Optional[typing.Union["SagemakerModelInferenceExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        primary_container: typing.Optional[typing.Union["SagemakerModelPrimaryContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_config: typing.Optional[typing.Union["SagemakerModelVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param execution_role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#execution_role_arn SagemakerModel#execution_role_arn}.
        :param container: container block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#container SagemakerModel#container}
        :param enable_network_isolation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#enable_network_isolation SagemakerModel#enable_network_isolation}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#id SagemakerModel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inference_execution_config: inference_execution_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#inference_execution_config SagemakerModel#inference_execution_config}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#name SagemakerModel#name}.
        :param primary_container: primary_container block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#primary_container SagemakerModel#primary_container}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#tags SagemakerModel#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#tags_all SagemakerModel#tags_all}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#vpc_config SagemakerModel#vpc_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(inference_execution_config, dict):
            inference_execution_config = SagemakerModelInferenceExecutionConfig(**inference_execution_config)
        if isinstance(primary_container, dict):
            primary_container = SagemakerModelPrimaryContainer(**primary_container)
        if isinstance(vpc_config, dict):
            vpc_config = SagemakerModelVpcConfig(**vpc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09783e2ec505e4c79f2c0e3caaa408e9e840d5b1bf1df364cd019a9227fb304)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument enable_network_isolation", value=enable_network_isolation, expected_type=type_hints["enable_network_isolation"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inference_execution_config", value=inference_execution_config, expected_type=type_hints["inference_execution_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary_container", value=primary_container, expected_type=type_hints["primary_container"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role_arn": execution_role_arn,
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
        if container is not None:
            self._values["container"] = container
        if enable_network_isolation is not None:
            self._values["enable_network_isolation"] = enable_network_isolation
        if id is not None:
            self._values["id"] = id
        if inference_execution_config is not None:
            self._values["inference_execution_config"] = inference_execution_config
        if name is not None:
            self._values["name"] = name
        if primary_container is not None:
            self._values["primary_container"] = primary_container
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

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
    def execution_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#execution_role_arn SagemakerModel#execution_role_arn}.'''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainer"]]]:
        '''container block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#container SagemakerModel#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerModelContainer"]]], result)

    @builtins.property
    def enable_network_isolation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#enable_network_isolation SagemakerModel#enable_network_isolation}.'''
        result = self._values.get("enable_network_isolation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#id SagemakerModel#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inference_execution_config(
        self,
    ) -> typing.Optional["SagemakerModelInferenceExecutionConfig"]:
        '''inference_execution_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#inference_execution_config SagemakerModel#inference_execution_config}
        '''
        result = self._values.get("inference_execution_config")
        return typing.cast(typing.Optional["SagemakerModelInferenceExecutionConfig"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#name SagemakerModel#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_container(self) -> typing.Optional["SagemakerModelPrimaryContainer"]:
        '''primary_container block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#primary_container SagemakerModel#primary_container}
        '''
        result = self._values.get("primary_container")
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainer"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#tags SagemakerModel#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#tags_all SagemakerModel#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vpc_config(self) -> typing.Optional["SagemakerModelVpcConfig"]:
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#vpc_config SagemakerModel#vpc_config}
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional["SagemakerModelVpcConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelContainer",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "container_hostname": "containerHostname",
        "environment": "environment",
        "image_config": "imageConfig",
        "mode": "mode",
        "model_data_url": "modelDataUrl",
    },
)
class SagemakerModelContainer:
    def __init__(
        self,
        *,
        image: builtins.str,
        container_hostname: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image_config: typing.Optional[typing.Union["SagemakerModelContainerImageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        model_data_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#image SagemakerModel#image}.
        :param container_hostname: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#container_hostname SagemakerModel#container_hostname}.
        :param environment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#environment SagemakerModel#environment}.
        :param image_config: image_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#image_config SagemakerModel#image_config}
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#mode SagemakerModel#mode}.
        :param model_data_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#model_data_url SagemakerModel#model_data_url}.
        '''
        if isinstance(image_config, dict):
            image_config = SagemakerModelContainerImageConfig(**image_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68307bd8f100616bb4e87ddd3f2c7ead9daa917afb5190dee0730b2be85c7d46)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument container_hostname", value=container_hostname, expected_type=type_hints["container_hostname"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument image_config", value=image_config, expected_type=type_hints["image_config"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument model_data_url", value=model_data_url, expected_type=type_hints["model_data_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if container_hostname is not None:
            self._values["container_hostname"] = container_hostname
        if environment is not None:
            self._values["environment"] = environment
        if image_config is not None:
            self._values["image_config"] = image_config
        if mode is not None:
            self._values["mode"] = mode
        if model_data_url is not None:
            self._values["model_data_url"] = model_data_url

    @builtins.property
    def image(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#image SagemakerModel#image}.'''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_hostname(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#container_hostname SagemakerModel#container_hostname}.'''
        result = self._values.get("container_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#environment SagemakerModel#environment}.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image_config(self) -> typing.Optional["SagemakerModelContainerImageConfig"]:
        '''image_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#image_config SagemakerModel#image_config}
        '''
        result = self._values.get("image_config")
        return typing.cast(typing.Optional["SagemakerModelContainerImageConfig"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#mode SagemakerModel#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_data_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#model_data_url SagemakerModel#model_data_url}.'''
        result = self._values.get("model_data_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelContainerImageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "repository_access_mode": "repositoryAccessMode",
        "repository_auth_config": "repositoryAuthConfig",
    },
)
class SagemakerModelContainerImageConfig:
    def __init__(
        self,
        *,
        repository_access_mode: builtins.str,
        repository_auth_config: typing.Optional[typing.Union["SagemakerModelContainerImageConfigRepositoryAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repository_access_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.
        :param repository_auth_config: repository_auth_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        if isinstance(repository_auth_config, dict):
            repository_auth_config = SagemakerModelContainerImageConfigRepositoryAuthConfig(**repository_auth_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286ae90372b278fcd68df6c08e949e4612ac85c8d68ac95282d2af4f04cf006e)
            check_type(argname="argument repository_access_mode", value=repository_access_mode, expected_type=type_hints["repository_access_mode"])
            check_type(argname="argument repository_auth_config", value=repository_auth_config, expected_type=type_hints["repository_auth_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_access_mode": repository_access_mode,
        }
        if repository_auth_config is not None:
            self._values["repository_auth_config"] = repository_auth_config

    @builtins.property
    def repository_access_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.'''
        result = self._values.get("repository_access_mode")
        assert result is not None, "Required property 'repository_access_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_auth_config(
        self,
    ) -> typing.Optional["SagemakerModelContainerImageConfigRepositoryAuthConfig"]:
        '''repository_auth_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        result = self._values.get("repository_auth_config")
        return typing.cast(typing.Optional["SagemakerModelContainerImageConfigRepositoryAuthConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainerImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelContainerImageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelContainerImageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e41a72672d038127090c9aff7cd148edc63aac927ebbaad43ce6378e5e76ef1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRepositoryAuthConfig")
    def put_repository_auth_config(
        self,
        *,
        repository_credentials_provider_arn: builtins.str,
    ) -> None:
        '''
        :param repository_credentials_provider_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.
        '''
        value = SagemakerModelContainerImageConfigRepositoryAuthConfig(
            repository_credentials_provider_arn=repository_credentials_provider_arn
        )

        return typing.cast(None, jsii.invoke(self, "putRepositoryAuthConfig", [value]))

    @jsii.member(jsii_name="resetRepositoryAuthConfig")
    def reset_repository_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryAuthConfig", []))

    @builtins.property
    @jsii.member(jsii_name="repositoryAuthConfig")
    def repository_auth_config(
        self,
    ) -> "SagemakerModelContainerImageConfigRepositoryAuthConfigOutputReference":
        return typing.cast("SagemakerModelContainerImageConfigRepositoryAuthConfigOutputReference", jsii.get(self, "repositoryAuthConfig"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessModeInput")
    def repository_access_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryAccessModeInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAuthConfigInput")
    def repository_auth_config_input(
        self,
    ) -> typing.Optional["SagemakerModelContainerImageConfigRepositoryAuthConfig"]:
        return typing.cast(typing.Optional["SagemakerModelContainerImageConfigRepositoryAuthConfig"], jsii.get(self, "repositoryAuthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessMode")
    def repository_access_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryAccessMode"))

    @repository_access_mode.setter
    def repository_access_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316ff075ba9ab0541b7c0bc2be93ffe03c94f1624b1e08c0ff52d7f917811630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryAccessMode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerModelContainerImageConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerImageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelContainerImageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3801fe50f6b8ad64c28ae58a94cc22c93bdbac7a2c7b37b82522fa2b726139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelContainerImageConfigRepositoryAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "repository_credentials_provider_arn": "repositoryCredentialsProviderArn",
    },
)
class SagemakerModelContainerImageConfigRepositoryAuthConfig:
    def __init__(self, *, repository_credentials_provider_arn: builtins.str) -> None:
        '''
        :param repository_credentials_provider_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b66dd144f0f919ec042f1d37e8648c6161929b36162948d15799f0b7ebf90f)
            check_type(argname="argument repository_credentials_provider_arn", value=repository_credentials_provider_arn, expected_type=type_hints["repository_credentials_provider_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_credentials_provider_arn": repository_credentials_provider_arn,
        }

    @builtins.property
    def repository_credentials_provider_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.'''
        result = self._values.get("repository_credentials_provider_arn")
        assert result is not None, "Required property 'repository_credentials_provider_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelContainerImageConfigRepositoryAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelContainerImageConfigRepositoryAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelContainerImageConfigRepositoryAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25948aeebaac551b5987a61cc209254e7a0241926dfcad1306c03aac4d5b70fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="repositoryCredentialsProviderArnInput")
    def repository_credentials_provider_arn_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryCredentialsProviderArnInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCredentialsProviderArn")
    def repository_credentials_provider_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryCredentialsProviderArn"))

    @repository_credentials_provider_arn.setter
    def repository_credentials_provider_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c5c5794b7f1c7976fb1fb8f12f559e9fcf48847a2fec9c6d706376516e9625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryCredentialsProviderArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelContainerImageConfigRepositoryAuthConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerImageConfigRepositoryAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelContainerImageConfigRepositoryAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe14d5870bb7176702463c38631551465dac123c30d9d05a7c20e2ddafc63ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerModelContainerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelContainerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6adafc3b74fc7cb590377f1d0ef831da5a69a6587b4d2e56c8096127e7e994b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SagemakerModelContainerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f419bf6f24452e9ec342fe8cc9fad6518f066e16722c21c27afc8c699f70bbc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerModelContainerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce71d5f78e49138f41d9afddbfbda07ab9ac5f83109f1d797cd8b49c32e1c2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5809531fb6831c8a89d010111c98ef6de9e7e54e6d4428ec5274c01724ab1325)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f475b919d9d1c4db1e8bf3c139963d4dd395cd7da9bf8d34f7cc3b0fd7db1d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d7bcedd7d6ed6cb0ef667170a8fcc570f79daedf3713d642cf7976d48b911e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerModelContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__884bf514ae76f9792966316eee8a3fe78ac03d971369beac2bf52eceab1e6f78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putImageConfig")
    def put_image_config(
        self,
        *,
        repository_access_mode: builtins.str,
        repository_auth_config: typing.Optional[typing.Union[SagemakerModelContainerImageConfigRepositoryAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repository_access_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.
        :param repository_auth_config: repository_auth_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        value = SagemakerModelContainerImageConfig(
            repository_access_mode=repository_access_mode,
            repository_auth_config=repository_auth_config,
        )

        return typing.cast(None, jsii.invoke(self, "putImageConfig", [value]))

    @jsii.member(jsii_name="resetContainerHostname")
    def reset_container_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerHostname", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetImageConfig")
    def reset_image_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageConfig", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetModelDataUrl")
    def reset_model_data_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelDataUrl", []))

    @builtins.property
    @jsii.member(jsii_name="imageConfig")
    def image_config(self) -> SagemakerModelContainerImageConfigOutputReference:
        return typing.cast(SagemakerModelContainerImageConfigOutputReference, jsii.get(self, "imageConfig"))

    @builtins.property
    @jsii.member(jsii_name="containerHostnameInput")
    def container_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="imageConfigInput")
    def image_config_input(self) -> typing.Optional[SagemakerModelContainerImageConfig]:
        return typing.cast(typing.Optional[SagemakerModelContainerImageConfig], jsii.get(self, "imageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="modelDataUrlInput")
    def model_data_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelDataUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="containerHostname")
    def container_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerHostname"))

    @container_hostname.setter
    def container_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640dba2934a3039bdf778811287f020d40cfae7673c14df30a79bbccc44b0c17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerHostname", value)

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58249705ffba1ce895f6ce261d01142dca0ce0e184202ba6534998ed023e36fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value)

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5534f155e3543bc6326b97e3ae334ae29a5a80f4d28f015b0c5bb48caea458f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76345e5622c1e0e3ec9f0753d65d6ff8298fcd1b75386e7b17a5e78f241d85bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="modelDataUrl")
    def model_data_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelDataUrl"))

    @model_data_url.setter
    def model_data_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a1b1ab19f9edfe4c67652029f2d56a762a327ea095f66ff76beb1e43386b910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelDataUrl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SagemakerModelContainer, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SagemakerModelContainer, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SagemakerModelContainer, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ce725afba5857cdb2f1034b336236364b84f984af4fc12f1a9be229d7183e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelInferenceExecutionConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class SagemakerModelInferenceExecutionConfig:
    def __init__(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#mode SagemakerModel#mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efde63e0ff2c1f21efd5a693b45d0fcbc164abb96d8215f6c5b4d5d0aa2936c4)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#mode SagemakerModel#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelInferenceExecutionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelInferenceExecutionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelInferenceExecutionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3081997da2d686c35b585ac98fe908c8e0242951e93fbe3b3e2536fc40425694)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a26bf1047d36c673b8d4ca74dcc1d8078629ca43bda36de430a83975691e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerModelInferenceExecutionConfig]:
        return typing.cast(typing.Optional[SagemakerModelInferenceExecutionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelInferenceExecutionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3aba6c88214fbbf862cdb06a83931693dd089ef824d2eb427237a07f84322d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelPrimaryContainer",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "container_hostname": "containerHostname",
        "environment": "environment",
        "image_config": "imageConfig",
        "mode": "mode",
        "model_data_url": "modelDataUrl",
    },
)
class SagemakerModelPrimaryContainer:
    def __init__(
        self,
        *,
        image: builtins.str,
        container_hostname: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image_config: typing.Optional[typing.Union["SagemakerModelPrimaryContainerImageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        model_data_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#image SagemakerModel#image}.
        :param container_hostname: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#container_hostname SagemakerModel#container_hostname}.
        :param environment: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#environment SagemakerModel#environment}.
        :param image_config: image_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#image_config SagemakerModel#image_config}
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#mode SagemakerModel#mode}.
        :param model_data_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#model_data_url SagemakerModel#model_data_url}.
        '''
        if isinstance(image_config, dict):
            image_config = SagemakerModelPrimaryContainerImageConfig(**image_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8dcc3ebd8ddee0ce41ec70f5c0e04be47d24b6d66c286611986157d7184bcf7)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument container_hostname", value=container_hostname, expected_type=type_hints["container_hostname"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument image_config", value=image_config, expected_type=type_hints["image_config"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument model_data_url", value=model_data_url, expected_type=type_hints["model_data_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if container_hostname is not None:
            self._values["container_hostname"] = container_hostname
        if environment is not None:
            self._values["environment"] = environment
        if image_config is not None:
            self._values["image_config"] = image_config
        if mode is not None:
            self._values["mode"] = mode
        if model_data_url is not None:
            self._values["model_data_url"] = model_data_url

    @builtins.property
    def image(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#image SagemakerModel#image}.'''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_hostname(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#container_hostname SagemakerModel#container_hostname}.'''
        result = self._values.get("container_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#environment SagemakerModel#environment}.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image_config(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainerImageConfig"]:
        '''image_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#image_config SagemakerModel#image_config}
        '''
        result = self._values.get("image_config")
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainerImageConfig"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#mode SagemakerModel#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_data_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#model_data_url SagemakerModel#model_data_url}.'''
        result = self._values.get("model_data_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerImageConfig",
    jsii_struct_bases=[],
    name_mapping={
        "repository_access_mode": "repositoryAccessMode",
        "repository_auth_config": "repositoryAuthConfig",
    },
)
class SagemakerModelPrimaryContainerImageConfig:
    def __init__(
        self,
        *,
        repository_access_mode: builtins.str,
        repository_auth_config: typing.Optional[typing.Union["SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repository_access_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.
        :param repository_auth_config: repository_auth_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        if isinstance(repository_auth_config, dict):
            repository_auth_config = SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig(**repository_auth_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61d743e5f93c35c29e8cab9be7470284ded899efb3517a8d6e8776ca1cb75d7)
            check_type(argname="argument repository_access_mode", value=repository_access_mode, expected_type=type_hints["repository_access_mode"])
            check_type(argname="argument repository_auth_config", value=repository_auth_config, expected_type=type_hints["repository_auth_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_access_mode": repository_access_mode,
        }
        if repository_auth_config is not None:
            self._values["repository_auth_config"] = repository_auth_config

    @builtins.property
    def repository_access_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.'''
        result = self._values.get("repository_access_mode")
        assert result is not None, "Required property 'repository_access_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_auth_config(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig"]:
        '''repository_auth_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        result = self._values.get("repository_auth_config")
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainerImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelPrimaryContainerImageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerImageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__799e46ec3dae35c3855c515cf334ebcf49a192053e17753123c9a4ea8f4c971e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRepositoryAuthConfig")
    def put_repository_auth_config(
        self,
        *,
        repository_credentials_provider_arn: builtins.str,
    ) -> None:
        '''
        :param repository_credentials_provider_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.
        '''
        value = SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig(
            repository_credentials_provider_arn=repository_credentials_provider_arn
        )

        return typing.cast(None, jsii.invoke(self, "putRepositoryAuthConfig", [value]))

    @jsii.member(jsii_name="resetRepositoryAuthConfig")
    def reset_repository_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryAuthConfig", []))

    @builtins.property
    @jsii.member(jsii_name="repositoryAuthConfig")
    def repository_auth_config(
        self,
    ) -> "SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfigOutputReference":
        return typing.cast("SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfigOutputReference", jsii.get(self, "repositoryAuthConfig"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessModeInput")
    def repository_access_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryAccessModeInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAuthConfigInput")
    def repository_auth_config_input(
        self,
    ) -> typing.Optional["SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig"]:
        return typing.cast(typing.Optional["SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig"], jsii.get(self, "repositoryAuthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessMode")
    def repository_access_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryAccessMode"))

    @repository_access_mode.setter
    def repository_access_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d065ebe4dc3c7d1269d04c908b5f7371029e45871a5162152adabd96ecaa350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryAccessMode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerImageConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerImageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelPrimaryContainerImageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701d56d2e033a8ebe099c64dd80af07c55a47ecc61f071de92352960f2d5e7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "repository_credentials_provider_arn": "repositoryCredentialsProviderArn",
    },
)
class SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig:
    def __init__(self, *, repository_credentials_provider_arn: builtins.str) -> None:
        '''
        :param repository_credentials_provider_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee80d760ac1dd95bb4e011da1f54686a423919b1eac14c3ea4ac2fde26b11f2b)
            check_type(argname="argument repository_credentials_provider_arn", value=repository_credentials_provider_arn, expected_type=type_hints["repository_credentials_provider_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_credentials_provider_arn": repository_credentials_provider_arn,
        }

    @builtins.property
    def repository_credentials_provider_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_credentials_provider_arn SagemakerModel#repository_credentials_provider_arn}.'''
        result = self._values.get("repository_credentials_provider_arn")
        assert result is not None, "Required property 'repository_credentials_provider_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82fbfba04c9d3ee57e6de57fecbf98f56ca512aa5e8e2276d980ebfc3f3d90f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="repositoryCredentialsProviderArnInput")
    def repository_credentials_provider_arn_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryCredentialsProviderArnInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCredentialsProviderArn")
    def repository_credentials_provider_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryCredentialsProviderArn"))

    @repository_credentials_provider_arn.setter
    def repository_credentials_provider_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9419a4d527dc9e7695121335ad8070bb9b4a807b5e163dd6c6c4ccded85534b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryCredentialsProviderArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524b7c2f7402b26bcd3967c5bd01064d816965156f89379a7951863299e4079e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerModelPrimaryContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelPrimaryContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dca8246beee1437ddb9d242422a52f80be45ffb35a47b986fc35a6f4c5a9da92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putImageConfig")
    def put_image_config(
        self,
        *,
        repository_access_mode: builtins.str,
        repository_auth_config: typing.Optional[typing.Union[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param repository_access_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_access_mode SagemakerModel#repository_access_mode}.
        :param repository_auth_config: repository_auth_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#repository_auth_config SagemakerModel#repository_auth_config}
        '''
        value = SagemakerModelPrimaryContainerImageConfig(
            repository_access_mode=repository_access_mode,
            repository_auth_config=repository_auth_config,
        )

        return typing.cast(None, jsii.invoke(self, "putImageConfig", [value]))

    @jsii.member(jsii_name="resetContainerHostname")
    def reset_container_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerHostname", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetImageConfig")
    def reset_image_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageConfig", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetModelDataUrl")
    def reset_model_data_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelDataUrl", []))

    @builtins.property
    @jsii.member(jsii_name="imageConfig")
    def image_config(self) -> SagemakerModelPrimaryContainerImageConfigOutputReference:
        return typing.cast(SagemakerModelPrimaryContainerImageConfigOutputReference, jsii.get(self, "imageConfig"))

    @builtins.property
    @jsii.member(jsii_name="containerHostnameInput")
    def container_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="imageConfigInput")
    def image_config_input(
        self,
    ) -> typing.Optional[SagemakerModelPrimaryContainerImageConfig]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainerImageConfig], jsii.get(self, "imageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="modelDataUrlInput")
    def model_data_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelDataUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="containerHostname")
    def container_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerHostname"))

    @container_hostname.setter
    def container_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818b3defdb3d3a718e6fd81d4ef4133d811e4019009c764cc0c84451e36631cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerHostname", value)

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67772da9dff609d5ef68b24ff287ccd21febc00d83e9451e52ff15c4374e9e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value)

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c98e6d8ef63a4bc244e26b924caa67cb2792898e3cbd6f7ad71764917021a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73ac917606a3797444179b11af0e592c6fc806d8c583cf6b8f617240398435e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="modelDataUrl")
    def model_data_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelDataUrl"))

    @model_data_url.setter
    def model_data_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd6bed5fa7e1a12a1a3f1782cbff2bb253fbf4d5db13f6cdf5a73daa0441fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelDataUrl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerModelPrimaryContainer]:
        return typing.cast(typing.Optional[SagemakerModelPrimaryContainer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerModelPrimaryContainer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646e3ab37db76cdb5d80ba0cfcb3519f600efd51d869caeba3027a6e9d9b37f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelVpcConfig",
    jsii_struct_bases=[],
    name_mapping={"security_group_ids": "securityGroupIds", "subnets": "subnets"},
)
class SagemakerModelVpcConfig:
    def __init__(
        self,
        *,
        security_group_ids: typing.Sequence[builtins.str],
        subnets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#security_group_ids SagemakerModel#security_group_ids}.
        :param subnets: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#subnets SagemakerModel#subnets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8bf98db05fca6815f9eb4a9a60639fc420ccb28c861433ff3f376553f249240)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_ids": security_group_ids,
            "subnets": subnets,
        }

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#security_group_ids SagemakerModel#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnets(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_model#subnets SagemakerModel#subnets}.'''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerModelVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerModelVpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerModel.SagemakerModelVpcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c644edfb290d59606a95a09be840c8aafb181648b2229807b9b51e700ba93f37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetsInput")
    def subnets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07eadee2189697a0635ad2e4b6642d98cadd65be569736f7ff3deff74ea9f435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5adb2c5b10d10e491ad784f8bebee77db646bf9cdf1fd6460bb561c66c4dbe03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerModelVpcConfig]:
        return typing.cast(typing.Optional[SagemakerModelVpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SagemakerModelVpcConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bedcab2d86c5bcf84a6797b26a311dc2ffc96dceb8e6dc3d473261e935182bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SagemakerModel",
    "SagemakerModelConfig",
    "SagemakerModelContainer",
    "SagemakerModelContainerImageConfig",
    "SagemakerModelContainerImageConfigOutputReference",
    "SagemakerModelContainerImageConfigRepositoryAuthConfig",
    "SagemakerModelContainerImageConfigRepositoryAuthConfigOutputReference",
    "SagemakerModelContainerList",
    "SagemakerModelContainerOutputReference",
    "SagemakerModelInferenceExecutionConfig",
    "SagemakerModelInferenceExecutionConfigOutputReference",
    "SagemakerModelPrimaryContainer",
    "SagemakerModelPrimaryContainerImageConfig",
    "SagemakerModelPrimaryContainerImageConfigOutputReference",
    "SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig",
    "SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfigOutputReference",
    "SagemakerModelPrimaryContainerOutputReference",
    "SagemakerModelVpcConfig",
    "SagemakerModelVpcConfigOutputReference",
]

publication.publish()

def _typecheckingstub__6abe947e09f96e3915c2337aa9a84e5c3329a3e572460546560e618ed7afedf6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    execution_role_arn: builtins.str,
    container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    inference_execution_config: typing.Optional[typing.Union[SagemakerModelInferenceExecutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    primary_container: typing.Optional[typing.Union[SagemakerModelPrimaryContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_config: typing.Optional[typing.Union[SagemakerModelVpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__dc3251d86e9d80695ac44d4b7884fa796a6607dbcec3b144894a0cd2c18829f9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a989662d8fbed9cc2adb46c558fb1fccd76e988a6f508b5cca4fca03dde8f07c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5288f586e6db82049bb4321b9eefe66786411a66ab5660fd782e12ac986ad9d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69c13c6e28fe26e1643f2826b18b013245268996d8c4f3d6a92404c5331f207(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df942a246b5c0915857323bb835df65e05f9d97bf2c6d9b04b4afa277666976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b20586f9f627a39d0d17355041bbdedac8e951d6b4e3dbd16e7f34254b803f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1400ea28b1d7c6619183865d8419be6d856bb2cfdd7b3ee3451a9f9cf117ee17(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09783e2ec505e4c79f2c0e3caaa408e9e840d5b1bf1df364cd019a9227fb304(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    execution_role_arn: builtins.str,
    container: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerModelContainer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_network_isolation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    inference_execution_config: typing.Optional[typing.Union[SagemakerModelInferenceExecutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    primary_container: typing.Optional[typing.Union[SagemakerModelPrimaryContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_config: typing.Optional[typing.Union[SagemakerModelVpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68307bd8f100616bb4e87ddd3f2c7ead9daa917afb5190dee0730b2be85c7d46(
    *,
    image: builtins.str,
    container_hostname: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image_config: typing.Optional[typing.Union[SagemakerModelContainerImageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    model_data_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286ae90372b278fcd68df6c08e949e4612ac85c8d68ac95282d2af4f04cf006e(
    *,
    repository_access_mode: builtins.str,
    repository_auth_config: typing.Optional[typing.Union[SagemakerModelContainerImageConfigRepositoryAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e41a72672d038127090c9aff7cd148edc63aac927ebbaad43ce6378e5e76ef1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316ff075ba9ab0541b7c0bc2be93ffe03c94f1624b1e08c0ff52d7f917811630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3801fe50f6b8ad64c28ae58a94cc22c93bdbac7a2c7b37b82522fa2b726139(
    value: typing.Optional[SagemakerModelContainerImageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b66dd144f0f919ec042f1d37e8648c6161929b36162948d15799f0b7ebf90f(
    *,
    repository_credentials_provider_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25948aeebaac551b5987a61cc209254e7a0241926dfcad1306c03aac4d5b70fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c5c5794b7f1c7976fb1fb8f12f559e9fcf48847a2fec9c6d706376516e9625(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe14d5870bb7176702463c38631551465dac123c30d9d05a7c20e2ddafc63ee7(
    value: typing.Optional[SagemakerModelContainerImageConfigRepositoryAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adafc3b74fc7cb590377f1d0ef831da5a69a6587b4d2e56c8096127e7e994b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f419bf6f24452e9ec342fe8cc9fad6518f066e16722c21c27afc8c699f70bbc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce71d5f78e49138f41d9afddbfbda07ab9ac5f83109f1d797cd8b49c32e1c2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5809531fb6831c8a89d010111c98ef6de9e7e54e6d4428ec5274c01724ab1325(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f475b919d9d1c4db1e8bf3c139963d4dd395cd7da9bf8d34f7cc3b0fd7db1d36(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d7bcedd7d6ed6cb0ef667170a8fcc570f79daedf3713d642cf7976d48b911e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerModelContainer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__884bf514ae76f9792966316eee8a3fe78ac03d971369beac2bf52eceab1e6f78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640dba2934a3039bdf778811287f020d40cfae7673c14df30a79bbccc44b0c17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58249705ffba1ce895f6ce261d01142dca0ce0e184202ba6534998ed023e36fc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5534f155e3543bc6326b97e3ae334ae29a5a80f4d28f015b0c5bb48caea458f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76345e5622c1e0e3ec9f0753d65d6ff8298fcd1b75386e7b17a5e78f241d85bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1b1ab19f9edfe4c67652029f2d56a762a327ea095f66ff76beb1e43386b910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ce725afba5857cdb2f1034b336236364b84f984af4fc12f1a9be229d7183e9(
    value: typing.Optional[typing.Union[SagemakerModelContainer, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efde63e0ff2c1f21efd5a693b45d0fcbc164abb96d8215f6c5b4d5d0aa2936c4(
    *,
    mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3081997da2d686c35b585ac98fe908c8e0242951e93fbe3b3e2536fc40425694(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a26bf1047d36c673b8d4ca74dcc1d8078629ca43bda36de430a83975691e32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3aba6c88214fbbf862cdb06a83931693dd089ef824d2eb427237a07f84322d4(
    value: typing.Optional[SagemakerModelInferenceExecutionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8dcc3ebd8ddee0ce41ec70f5c0e04be47d24b6d66c286611986157d7184bcf7(
    *,
    image: builtins.str,
    container_hostname: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image_config: typing.Optional[typing.Union[SagemakerModelPrimaryContainerImageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    model_data_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61d743e5f93c35c29e8cab9be7470284ded899efb3517a8d6e8776ca1cb75d7(
    *,
    repository_access_mode: builtins.str,
    repository_auth_config: typing.Optional[typing.Union[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799e46ec3dae35c3855c515cf334ebcf49a192053e17753123c9a4ea8f4c971e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d065ebe4dc3c7d1269d04c908b5f7371029e45871a5162152adabd96ecaa350(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701d56d2e033a8ebe099c64dd80af07c55a47ecc61f071de92352960f2d5e7a2(
    value: typing.Optional[SagemakerModelPrimaryContainerImageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee80d760ac1dd95bb4e011da1f54686a423919b1eac14c3ea4ac2fde26b11f2b(
    *,
    repository_credentials_provider_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fbfba04c9d3ee57e6de57fecbf98f56ca512aa5e8e2276d980ebfc3f3d90f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9419a4d527dc9e7695121335ad8070bb9b4a807b5e163dd6c6c4ccded85534b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524b7c2f7402b26bcd3967c5bd01064d816965156f89379a7951863299e4079e(
    value: typing.Optional[SagemakerModelPrimaryContainerImageConfigRepositoryAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca8246beee1437ddb9d242422a52f80be45ffb35a47b986fc35a6f4c5a9da92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818b3defdb3d3a718e6fd81d4ef4133d811e4019009c764cc0c84451e36631cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67772da9dff609d5ef68b24ff287ccd21febc00d83e9451e52ff15c4374e9e37(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c98e6d8ef63a4bc244e26b924caa67cb2792898e3cbd6f7ad71764917021a37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73ac917606a3797444179b11af0e592c6fc806d8c583cf6b8f617240398435e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd6bed5fa7e1a12a1a3f1782cbff2bb253fbf4d5db13f6cdf5a73daa0441fc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646e3ab37db76cdb5d80ba0cfcb3519f600efd51d869caeba3027a6e9d9b37f8(
    value: typing.Optional[SagemakerModelPrimaryContainer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bf98db05fca6815f9eb4a9a60639fc420ccb28c861433ff3f376553f249240(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnets: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c644edfb290d59606a95a09be840c8aafb181648b2229807b9b51e700ba93f37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07eadee2189697a0635ad2e4b6642d98cadd65be569736f7ff3deff74ea9f435(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adb2c5b10d10e491ad784f8bebee77db646bf9cdf1fd6460bb561c66c4dbe03(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bedcab2d86c5bcf84a6797b26a311dc2ffc96dceb8e6dc3d473261e935182bb(
    value: typing.Optional[SagemakerModelVpcConfig],
) -> None:
    """Type checking stubs"""
    pass
