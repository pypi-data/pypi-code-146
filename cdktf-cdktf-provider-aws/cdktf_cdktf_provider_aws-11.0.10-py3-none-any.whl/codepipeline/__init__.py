'''
# `aws_codepipeline`

Refer to the Terraform Registory for docs: [`aws_codepipeline`](https://www.terraform.io/docs/providers/aws/r/codepipeline).
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


class Codepipeline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.Codepipeline",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/codepipeline aws_codepipeline}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        artifact_store: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineArtifactStore", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        role_arn: builtins.str,
        stage: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineStage", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/codepipeline aws_codepipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param artifact_store: artifact_store block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#artifact_store Codepipeline#artifact_store}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#name Codepipeline#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#role_arn Codepipeline#role_arn}.
        :param stage: stage block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#stage Codepipeline#stage}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#id Codepipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#tags Codepipeline#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#tags_all Codepipeline#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b05bf9d470a6d541c6793d8c11b37ee4652aafe5fdf5945767bdae8987af99b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CodepipelineConfig(
            artifact_store=artifact_store,
            name=name,
            role_arn=role_arn,
            stage=stage,
            id=id,
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

    @jsii.member(jsii_name="putArtifactStore")
    def put_artifact_store(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineArtifactStore", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10383963c155174b899e60ffc8f2f98399552b79c35a4de6c1594d741e354f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArtifactStore", [value]))

    @jsii.member(jsii_name="putStage")
    def put_stage(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineStage", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df349ff7dee10b41aa6aba23f53a3bbf1505b0a1e6327689dc5c6b4f314ad09f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStage", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="artifactStore")
    def artifact_store(self) -> "CodepipelineArtifactStoreList":
        return typing.cast("CodepipelineArtifactStoreList", jsii.get(self, "artifactStore"))

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> "CodepipelineStageList":
        return typing.cast("CodepipelineStageList", jsii.get(self, "stage"))

    @builtins.property
    @jsii.member(jsii_name="artifactStoreInput")
    def artifact_store_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineArtifactStore"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineArtifactStore"]]], jsii.get(self, "artifactStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stageInput")
    def stage_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStage"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStage"]]], jsii.get(self, "stageInput"))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f2b93040cead7a9937f01217f6352ea2233d2f400256af3f7e4a7b14cdb3bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad2c1e89e83d86c1039aaf9c1d57abcc0a27d9005cac5eb9a3baf63292f59bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d5a262fb418a52d9c077ee2a5b67d24123f15ddcf4a7cb9682b8266004f6d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b6ed8943de3fd52a65f1a6203dee739473e5c0cc0256f454d374149682de34b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e16b43e185b495bb94719ac17a947d8bc348193f0e70826ee610bdcd94037d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineArtifactStore",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "type": "type",
        "encryption_key": "encryptionKey",
        "region": "region",
    },
)
class CodepipelineArtifactStore:
    def __init__(
        self,
        *,
        location: builtins.str,
        type: builtins.str,
        encryption_key: typing.Optional[typing.Union["CodepipelineArtifactStoreEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#location Codepipeline#location}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#type Codepipeline#type}.
        :param encryption_key: encryption_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#encryption_key Codepipeline#encryption_key}
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#region Codepipeline#region}.
        '''
        if isinstance(encryption_key, dict):
            encryption_key = CodepipelineArtifactStoreEncryptionKey(**encryption_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922068355d678dd6effd40fe938c7b4bef095e80aafdc157f6347e9a154a7455)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "type": type,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#location Codepipeline#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#type Codepipeline#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(
        self,
    ) -> typing.Optional["CodepipelineArtifactStoreEncryptionKey"]:
        '''encryption_key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#encryption_key Codepipeline#encryption_key}
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional["CodepipelineArtifactStoreEncryptionKey"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#region Codepipeline#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineArtifactStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineArtifactStoreEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "type": "type"},
)
class CodepipelineArtifactStoreEncryptionKey:
    def __init__(self, *, id: builtins.str, type: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#id Codepipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#type Codepipeline#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d46126b88ec0637b8870b9918772f62c576de320afd50301c51ff6f2cb4a730)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "type": type,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#id Codepipeline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#type Codepipeline#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineArtifactStoreEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodepipelineArtifactStoreEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineArtifactStoreEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46c941e35195f370c8e8fed484db32b46c4930061ab32816151a6c9a77ed98a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e4af46ebfe947a3e6650b847155aeebc7fd20abb38822fc8a7fa9b66abe127f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6397c6cc84d9b854c5d220f016d81c03041b1cc9f7a19e2737721e673175d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodepipelineArtifactStoreEncryptionKey]:
        return typing.cast(typing.Optional[CodepipelineArtifactStoreEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodepipelineArtifactStoreEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f5a35c64dd518ba782d6fe1f72bc901c94647985fcb0f0410d8a36f9758c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CodepipelineArtifactStoreList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineArtifactStoreList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98845279dd07aa22f658694ce2d785b2f63880044cbc224cd270f73c530ed666)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CodepipelineArtifactStoreOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__110e0ac1b03bc412da726cf99c749a3213d21c96fa6fd765c2801666adaf8ad2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodepipelineArtifactStoreOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd95915f530001cb29302739bba967dc100350855e39797e71f05c760586e1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__388da3f1639c681b74313cc4f5d5034f54a9d30b265701a8ab65b3bf5fdf4b41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1d3d3d63a3a0886461f20af849e3daeac985588a43d5adb1259efd4988d0a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6b396dc65bdc3cb55da1e64f1ae1eccffb88c9a19379fe9adc874336629afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CodepipelineArtifactStoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineArtifactStoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32a9282c02570c1515b4ff146f29d98b0405b3f91c8562927c494269fbdf24ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEncryptionKey")
    def put_encryption_key(self, *, id: builtins.str, type: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#id Codepipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#type Codepipeline#type}.
        '''
        value = CodepipelineArtifactStoreEncryptionKey(id=id, type=type)

        return typing.cast(None, jsii.invoke(self, "putEncryptionKey", [value]))

    @jsii.member(jsii_name="resetEncryptionKey")
    def reset_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKey", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> CodepipelineArtifactStoreEncryptionKeyOutputReference:
        return typing.cast(CodepipelineArtifactStoreEncryptionKeyOutputReference, jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyInput")
    def encryption_key_input(
        self,
    ) -> typing.Optional[CodepipelineArtifactStoreEncryptionKey]:
        return typing.cast(typing.Optional[CodepipelineArtifactStoreEncryptionKey], jsii.get(self, "encryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7073ace0c2ac96908ecd48678800c927f8ee9ea800a55ea3dff5d90d9bd7491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644a35e7f02a989e4b3fdc9403a5a8d0921a77fdd69b886960fd8556e66a71f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3433081d5bd0381c76a04f4ce558aaf0808eac349c000c7a1f846a58c357cbbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CodepipelineArtifactStore, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CodepipelineArtifactStore, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CodepipelineArtifactStore, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a1b57429ee5766a4a1051555294a5e0a3065da41c51ae3aa106edc5bdc97d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "artifact_store": "artifactStore",
        "name": "name",
        "role_arn": "roleArn",
        "stage": "stage",
        "id": "id",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class CodepipelineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        artifact_store: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineArtifactStore, typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        role_arn: builtins.str,
        stage: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineStage", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
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
        :param artifact_store: artifact_store block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#artifact_store Codepipeline#artifact_store}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#name Codepipeline#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#role_arn Codepipeline#role_arn}.
        :param stage: stage block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#stage Codepipeline#stage}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#id Codepipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#tags Codepipeline#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#tags_all Codepipeline#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009e693604d53e9e0598d73e0bbcfe99d252352f522377b683d9881d7516179f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument artifact_store", value=artifact_store, expected_type=type_hints["artifact_store"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_store": artifact_store,
            "name": name,
            "role_arn": role_arn,
            "stage": stage,
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
    def artifact_store(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]]:
        '''artifact_store block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#artifact_store Codepipeline#artifact_store}
        '''
        result = self._values.get("artifact_store")
        assert result is not None, "Required property 'artifact_store' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#name Codepipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#role_arn Codepipeline#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStage"]]:
        '''stage block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#stage Codepipeline#stage}
        '''
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStage"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#id Codepipeline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#tags Codepipeline#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#tags_all Codepipeline#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStage",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "name": "name"},
)
class CodepipelineStage:
    def __init__(
        self,
        *,
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineStageAction", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#action Codepipeline#action}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#name Codepipeline#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f317cae47d1d43bfefb03a17abc49f8c36567a6558090d426f042e0b34d27a61)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
        }

    @builtins.property
    def action(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStageAction"]]:
        '''action block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#action Codepipeline#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStageAction"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#name Codepipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineStage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStageAction",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "name": "name",
        "owner": "owner",
        "provider": "provider",
        "version": "version",
        "configuration": "configuration",
        "input_artifacts": "inputArtifacts",
        "namespace": "namespace",
        "output_artifacts": "outputArtifacts",
        "region": "region",
        "role_arn": "roleArn",
        "run_order": "runOrder",
    },
)
class CodepipelineStageAction:
    def __init__(
        self,
        *,
        category: builtins.str,
        name: builtins.str,
        owner: builtins.str,
        provider: builtins.str,
        version: builtins.str,
        configuration: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        input_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        output_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#category Codepipeline#category}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#name Codepipeline#name}.
        :param owner: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#owner Codepipeline#owner}.
        :param provider: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#provider Codepipeline#provider}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#version Codepipeline#version}.
        :param configuration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#configuration Codepipeline#configuration}.
        :param input_artifacts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#input_artifacts Codepipeline#input_artifacts}.
        :param namespace: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#namespace Codepipeline#namespace}.
        :param output_artifacts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#output_artifacts Codepipeline#output_artifacts}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#region Codepipeline#region}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#role_arn Codepipeline#role_arn}.
        :param run_order: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#run_order Codepipeline#run_order}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f69913c0b6ea6e3efee6c519ce7ef6134ab72baa5cf682a9f77dffa02c3355)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument input_artifacts", value=input_artifacts, expected_type=type_hints["input_artifacts"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument output_artifacts", value=output_artifacts, expected_type=type_hints["output_artifacts"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument run_order", value=run_order, expected_type=type_hints["run_order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
            "name": name,
            "owner": owner,
            "provider": provider,
            "version": version,
        }
        if configuration is not None:
            self._values["configuration"] = configuration
        if input_artifacts is not None:
            self._values["input_artifacts"] = input_artifacts
        if namespace is not None:
            self._values["namespace"] = namespace
        if output_artifacts is not None:
            self._values["output_artifacts"] = output_artifacts
        if region is not None:
            self._values["region"] = region
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if run_order is not None:
            self._values["run_order"] = run_order

    @builtins.property
    def category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#category Codepipeline#category}.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#name Codepipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#owner Codepipeline#owner}.'''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#provider Codepipeline#provider}.'''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#version Codepipeline#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#configuration Codepipeline#configuration}.'''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def input_artifacts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#input_artifacts Codepipeline#input_artifacts}.'''
        result = self._values.get("input_artifacts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#namespace Codepipeline#namespace}.'''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_artifacts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#output_artifacts Codepipeline#output_artifacts}.'''
        result = self._values.get("output_artifacts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#region Codepipeline#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#role_arn Codepipeline#role_arn}.'''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/codepipeline#run_order Codepipeline#run_order}.'''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineStageAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodepipelineStageActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStageActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8810ed8d5fca6b86d5f3e61897150fee4d40ab3a38d59ec10d24620fc503d180)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CodepipelineStageActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb97058b9652c3aba975e5e01d27cea8ca71439863935e57c5f61422b70142d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodepipelineStageActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60afb90175647309fe7c3c8019e11a343b68fc29a57a14e64b75661caac136e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea7e5de378084dca737e0bb27f3222530fde85d7da5493879516d21f2ec020bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aa31127a50574768b62f5354e439ec55f690e4c318fecf9cff4a30e68fc853a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0365e5a923614b47962dd6a8869d692e0a3de517b8acf8be1912fbacbd24e855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CodepipelineStageActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStageActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a400239c0382a436b3c6e6aec4423109cf8bfabfbbc604da1dfed460acbef5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetInputArtifacts")
    def reset_input_artifacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputArtifacts", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetOutputArtifacts")
    def reset_output_artifacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputArtifacts", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @jsii.member(jsii_name="resetRunOrder")
    def reset_run_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunOrder", []))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="inputArtifactsInput")
    def input_artifacts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputArtifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="outputArtifactsInput")
    def output_artifacts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outputArtifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="providerInput")
    def provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="runOrderInput")
    def run_order_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "runOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b8bfb8f6f311dfd2c8864480e0a69f0fc9fa4058ed7aff6fcf7ddd64b11936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value)

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9e8d758e3e917ac8e3c987ad54d8dfcc34dd4ef0cfc04cd3c02c80ccb142bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="inputArtifacts")
    def input_artifacts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputArtifacts"))

    @input_artifacts.setter
    def input_artifacts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79aed965d763a80850ec35df4f28aa7aa6b309e39142c6ed4eed5b942d15215c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputArtifacts", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fde050ff30bbba6a868783c14f24a03e2dff66fca2181ed6b68e1d41ed74c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf79c669a7f32149d9c0c895f79a360c147f558bdc732d9b1dc3d8f67b64a33a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="outputArtifacts")
    def output_artifacts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outputArtifacts"))

    @output_artifacts.setter
    def output_artifacts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b49df4f4a3a1a2307b65a67a3c2e392622acc223c6c585a54400751316635f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputArtifacts", value)

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2179eeb40922294027e6735014b9b45b3f866bbbc64be9c59668bf3f8261ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provider"))

    @provider.setter
    def provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5947bc93c77598764051ecf2a150a2ad8c3ddae39bd4e28c7164c6845173acc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provider", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b0235e7359ea42567e71d8c02c370a2d9e26c0f6cc9738b86b3d77ef88c387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7231e16431dea3ee3f6f8266be621ac36bc00840ccad75d0fe089335de042be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="runOrder")
    def run_order(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "runOrder"))

    @run_order.setter
    def run_order(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f779cddb97adc4192c224fd087dc5d1be6cff4a621ad19117e345c2a0990231d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runOrder", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db00699348ce1ed0c58ca53ca27d0459f964fda3b96fb586694139bb5e6ee1d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CodepipelineStageAction, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CodepipelineStageAction, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CodepipelineStageAction, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b73a727fd3392933753d978f5d774e9d980acf7117ddfb7e0cd783218d9e08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CodepipelineStageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2ed8257e31f6f1a4ed7c507154b4c4ea2445204db927df623b260cadd6a12e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CodepipelineStageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a576933848558e35a815c240de4083c95316eb11f80b2c56f86db91ef86ee5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodepipelineStageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e3361d1ae5071052934a34214614d23a156bccfe214018cedb8118c4ba9384)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c11680928851de7087d9cc1ba3919b684f4432ab17df32af118603705aee3286)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe4c2c59cb15d226951da63a32901733443c2aed7731d8422e41d774ce638e7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c820b92db9eaa2fd2b2b3d43f7d2862c8df043311e9c2e4b0b2db58e6c874591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CodepipelineStageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85fbd29b809531d664bc8031778d57c94b24a586ecb8abcb50824d79aa7348d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStageAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0b1faebfad19d4d53302e79f3e9810ce0f0caede05594062dc56c9c883e052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> CodepipelineStageActionList:
        return typing.cast(CodepipelineStageActionList, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9583d78f934b5520a6a97e580d120baabd615bce279ff0119efa843b1d69ca97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CodepipelineStage, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CodepipelineStage, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CodepipelineStage, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4843df9e290cc66526e96ccf25839b8fdd7126d05b00512e788bf75996a53a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Codepipeline",
    "CodepipelineArtifactStore",
    "CodepipelineArtifactStoreEncryptionKey",
    "CodepipelineArtifactStoreEncryptionKeyOutputReference",
    "CodepipelineArtifactStoreList",
    "CodepipelineArtifactStoreOutputReference",
    "CodepipelineConfig",
    "CodepipelineStage",
    "CodepipelineStageAction",
    "CodepipelineStageActionList",
    "CodepipelineStageActionOutputReference",
    "CodepipelineStageList",
    "CodepipelineStageOutputReference",
]

publication.publish()

def _typecheckingstub__8b05bf9d470a6d541c6793d8c11b37ee4652aafe5fdf5945767bdae8987af99b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    artifact_store: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineArtifactStore, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    role_arn: builtins.str,
    stage: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStage, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__f10383963c155174b899e60ffc8f2f98399552b79c35a4de6c1594d741e354f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineArtifactStore, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df349ff7dee10b41aa6aba23f53a3bbf1505b0a1e6327689dc5c6b4f314ad09f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f2b93040cead7a9937f01217f6352ea2233d2f400256af3f7e4a7b14cdb3bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad2c1e89e83d86c1039aaf9c1d57abcc0a27d9005cac5eb9a3baf63292f59bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d5a262fb418a52d9c077ee2a5b67d24123f15ddcf4a7cb9682b8266004f6d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6ed8943de3fd52a65f1a6203dee739473e5c0cc0256f454d374149682de34b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e16b43e185b495bb94719ac17a947d8bc348193f0e70826ee610bdcd94037d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922068355d678dd6effd40fe938c7b4bef095e80aafdc157f6347e9a154a7455(
    *,
    location: builtins.str,
    type: builtins.str,
    encryption_key: typing.Optional[typing.Union[CodepipelineArtifactStoreEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d46126b88ec0637b8870b9918772f62c576de320afd50301c51ff6f2cb4a730(
    *,
    id: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c941e35195f370c8e8fed484db32b46c4930061ab32816151a6c9a77ed98a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4af46ebfe947a3e6650b847155aeebc7fd20abb38822fc8a7fa9b66abe127f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6397c6cc84d9b854c5d220f016d81c03041b1cc9f7a19e2737721e673175d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f5a35c64dd518ba782d6fe1f72bc901c94647985fcb0f0410d8a36f9758c73(
    value: typing.Optional[CodepipelineArtifactStoreEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98845279dd07aa22f658694ce2d785b2f63880044cbc224cd270f73c530ed666(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110e0ac1b03bc412da726cf99c749a3213d21c96fa6fd765c2801666adaf8ad2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd95915f530001cb29302739bba967dc100350855e39797e71f05c760586e1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388da3f1639c681b74313cc4f5d5034f54a9d30b265701a8ab65b3bf5fdf4b41(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d3d3d63a3a0886461f20af849e3daeac985588a43d5adb1259efd4988d0a3f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6b396dc65bdc3cb55da1e64f1ae1eccffb88c9a19379fe9adc874336629afa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a9282c02570c1515b4ff146f29d98b0405b3f91c8562927c494269fbdf24ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7073ace0c2ac96908ecd48678800c927f8ee9ea800a55ea3dff5d90d9bd7491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644a35e7f02a989e4b3fdc9403a5a8d0921a77fdd69b886960fd8556e66a71f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3433081d5bd0381c76a04f4ce558aaf0808eac349c000c7a1f846a58c357cbbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a1b57429ee5766a4a1051555294a5e0a3065da41c51ae3aa106edc5bdc97d2(
    value: typing.Optional[typing.Union[CodepipelineArtifactStore, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009e693604d53e9e0598d73e0bbcfe99d252352f522377b683d9881d7516179f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    artifact_store: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineArtifactStore, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    role_arn: builtins.str,
    stage: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStage, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f317cae47d1d43bfefb03a17abc49f8c36567a6558090d426f042e0b34d27a61(
    *,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStageAction, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f69913c0b6ea6e3efee6c519ce7ef6134ab72baa5cf682a9f77dffa02c3355(
    *,
    category: builtins.str,
    name: builtins.str,
    owner: builtins.str,
    provider: builtins.str,
    version: builtins.str,
    configuration: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    input_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    output_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    run_order: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8810ed8d5fca6b86d5f3e61897150fee4d40ab3a38d59ec10d24620fc503d180(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb97058b9652c3aba975e5e01d27cea8ca71439863935e57c5f61422b70142d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60afb90175647309fe7c3c8019e11a343b68fc29a57a14e64b75661caac136e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7e5de378084dca737e0bb27f3222530fde85d7da5493879516d21f2ec020bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa31127a50574768b62f5354e439ec55f690e4c318fecf9cff4a30e68fc853a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0365e5a923614b47962dd6a8869d692e0a3de517b8acf8be1912fbacbd24e855(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a400239c0382a436b3c6e6aec4423109cf8bfabfbbc604da1dfed460acbef5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b8bfb8f6f311dfd2c8864480e0a69f0fc9fa4058ed7aff6fcf7ddd64b11936(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9e8d758e3e917ac8e3c987ad54d8dfcc34dd4ef0cfc04cd3c02c80ccb142bd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79aed965d763a80850ec35df4f28aa7aa6b309e39142c6ed4eed5b942d15215c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fde050ff30bbba6a868783c14f24a03e2dff66fca2181ed6b68e1d41ed74c36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf79c669a7f32149d9c0c895f79a360c147f558bdc732d9b1dc3d8f67b64a33a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b49df4f4a3a1a2307b65a67a3c2e392622acc223c6c585a54400751316635f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2179eeb40922294027e6735014b9b45b3f866bbbc64be9c59668bf3f8261ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5947bc93c77598764051ecf2a150a2ad8c3ddae39bd4e28c7164c6845173acc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b0235e7359ea42567e71d8c02c370a2d9e26c0f6cc9738b86b3d77ef88c387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7231e16431dea3ee3f6f8266be621ac36bc00840ccad75d0fe089335de042be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f779cddb97adc4192c224fd087dc5d1be6cff4a621ad19117e345c2a0990231d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db00699348ce1ed0c58ca53ca27d0459f964fda3b96fb586694139bb5e6ee1d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b73a727fd3392933753d978f5d774e9d980acf7117ddfb7e0cd783218d9e08b(
    value: typing.Optional[typing.Union[CodepipelineStageAction, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ed8257e31f6f1a4ed7c507154b4c4ea2445204db927df623b260cadd6a12e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a576933848558e35a815c240de4083c95316eb11f80b2c56f86db91ef86ee5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e3361d1ae5071052934a34214614d23a156bccfe214018cedb8118c4ba9384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11680928851de7087d9cc1ba3919b684f4432ab17df32af118603705aee3286(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4c2c59cb15d226951da63a32901733443c2aed7731d8422e41d774ce638e7b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c820b92db9eaa2fd2b2b3d43f7d2862c8df043311e9c2e4b0b2db58e6c874591(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fbd29b809531d664bc8031778d57c94b24a586ecb8abcb50824d79aa7348d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0b1faebfad19d4d53302e79f3e9810ce0f0caede05594062dc56c9c883e052(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStageAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9583d78f934b5520a6a97e580d120baabd615bce279ff0119efa843b1d69ca97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4843df9e290cc66526e96ccf25839b8fdd7126d05b00512e788bf75996a53a5c(
    value: typing.Optional[typing.Union[CodepipelineStage, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
