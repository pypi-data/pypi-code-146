'''
# `aws_sagemaker_space`

Refer to the Terraform Registory for docs: [`aws_sagemaker_space`](https://www.terraform.io/docs/providers/aws/r/sagemaker_space).
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


class SagemakerSpace(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpace",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space aws_sagemaker_space}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        domain_id: builtins.str,
        space_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        space_settings: typing.Optional[typing.Union["SagemakerSpaceSpaceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space aws_sagemaker_space} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param domain_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#domain_id SagemakerSpace#domain_id}.
        :param space_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#space_name SagemakerSpace#space_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#id SagemakerSpace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param space_settings: space_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#space_settings SagemakerSpace#space_settings}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#tags SagemakerSpace#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#tags_all SagemakerSpace#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3387f8ee82cf0f5651f5129108d1c232b61dc93bd9bb364daeef9679c21e6b18)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerSpaceConfig(
            domain_id=domain_id,
            space_name=space_name,
            id=id,
            space_settings=space_settings,
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

    @jsii.member(jsii_name="putSpaceSettings")
    def put_space_settings(
        self,
        *,
        jupyter_server_app_settings: typing.Optional[typing.Union["SagemakerSpaceSpaceSettingsJupyterServerAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kernel_gateway_app_settings: typing.Optional[typing.Union["SagemakerSpaceSpaceSettingsKernelGatewayAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param jupyter_server_app_settings: jupyter_server_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#jupyter_server_app_settings SagemakerSpace#jupyter_server_app_settings}
        :param kernel_gateway_app_settings: kernel_gateway_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#kernel_gateway_app_settings SagemakerSpace#kernel_gateway_app_settings}
        '''
        value = SagemakerSpaceSpaceSettings(
            jupyter_server_app_settings=jupyter_server_app_settings,
            kernel_gateway_app_settings=kernel_gateway_app_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putSpaceSettings", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSpaceSettings")
    def reset_space_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpaceSettings", []))

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
    @jsii.member(jsii_name="homeEfsFileSystemUid")
    def home_efs_file_system_uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "homeEfsFileSystemUid"))

    @builtins.property
    @jsii.member(jsii_name="spaceSettings")
    def space_settings(self) -> "SagemakerSpaceSpaceSettingsOutputReference":
        return typing.cast("SagemakerSpaceSpaceSettingsOutputReference", jsii.get(self, "spaceSettings"))

    @builtins.property
    @jsii.member(jsii_name="domainIdInput")
    def domain_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="spaceNameInput")
    def space_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spaceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="spaceSettingsInput")
    def space_settings_input(self) -> typing.Optional["SagemakerSpaceSpaceSettings"]:
        return typing.cast(typing.Optional["SagemakerSpaceSpaceSettings"], jsii.get(self, "spaceSettingsInput"))

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
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @domain_id.setter
    def domain_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c8b560eb9785c44cabe47a80b83e39e49ba42051f5fc9f3de50656c86c9c67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6578ffbbc2330ac0c398923bedb4921c716f77faa791b5a7b3e693a34246e3c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="spaceName")
    def space_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spaceName"))

    @space_name.setter
    def space_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c11c6f024f5b5bd168bb7d3b3971df4255888439969b65e645380603c68fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spaceName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d91728e83c1f80c69ae5502b079852e1a630a86be4350bc6562da111714a366a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3d1c7af083e893c82434486939ea45eb7a9d4203dcd2ff40c621835291745f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "domain_id": "domainId",
        "space_name": "spaceName",
        "id": "id",
        "space_settings": "spaceSettings",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class SagemakerSpaceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        domain_id: builtins.str,
        space_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        space_settings: typing.Optional[typing.Union["SagemakerSpaceSpaceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param domain_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#domain_id SagemakerSpace#domain_id}.
        :param space_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#space_name SagemakerSpace#space_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#id SagemakerSpace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param space_settings: space_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#space_settings SagemakerSpace#space_settings}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#tags SagemakerSpace#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#tags_all SagemakerSpace#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(space_settings, dict):
            space_settings = SagemakerSpaceSpaceSettings(**space_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115ba9c4208d250962e44e6e773b8dbc42a66b057999e8953fb3bbb7f469eafd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
            check_type(argname="argument space_name", value=space_name, expected_type=type_hints["space_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument space_settings", value=space_settings, expected_type=type_hints["space_settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_id": domain_id,
            "space_name": space_name,
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
        if space_settings is not None:
            self._values["space_settings"] = space_settings
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
    def domain_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#domain_id SagemakerSpace#domain_id}.'''
        result = self._values.get("domain_id")
        assert result is not None, "Required property 'domain_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def space_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#space_name SagemakerSpace#space_name}.'''
        result = self._values.get("space_name")
        assert result is not None, "Required property 'space_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#id SagemakerSpace#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def space_settings(self) -> typing.Optional["SagemakerSpaceSpaceSettings"]:
        '''space_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#space_settings SagemakerSpace#space_settings}
        '''
        result = self._values.get("space_settings")
        return typing.cast(typing.Optional["SagemakerSpaceSpaceSettings"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#tags SagemakerSpace#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#tags_all SagemakerSpace#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerSpaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettings",
    jsii_struct_bases=[],
    name_mapping={
        "jupyter_server_app_settings": "jupyterServerAppSettings",
        "kernel_gateway_app_settings": "kernelGatewayAppSettings",
    },
)
class SagemakerSpaceSpaceSettings:
    def __init__(
        self,
        *,
        jupyter_server_app_settings: typing.Optional[typing.Union["SagemakerSpaceSpaceSettingsJupyterServerAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kernel_gateway_app_settings: typing.Optional[typing.Union["SagemakerSpaceSpaceSettingsKernelGatewayAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param jupyter_server_app_settings: jupyter_server_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#jupyter_server_app_settings SagemakerSpace#jupyter_server_app_settings}
        :param kernel_gateway_app_settings: kernel_gateway_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#kernel_gateway_app_settings SagemakerSpace#kernel_gateway_app_settings}
        '''
        if isinstance(jupyter_server_app_settings, dict):
            jupyter_server_app_settings = SagemakerSpaceSpaceSettingsJupyterServerAppSettings(**jupyter_server_app_settings)
        if isinstance(kernel_gateway_app_settings, dict):
            kernel_gateway_app_settings = SagemakerSpaceSpaceSettingsKernelGatewayAppSettings(**kernel_gateway_app_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e8cf736fe2bea251c6fc3f1d447b933be972f65a73ef66a1422714399b8a6a)
            check_type(argname="argument jupyter_server_app_settings", value=jupyter_server_app_settings, expected_type=type_hints["jupyter_server_app_settings"])
            check_type(argname="argument kernel_gateway_app_settings", value=kernel_gateway_app_settings, expected_type=type_hints["kernel_gateway_app_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if jupyter_server_app_settings is not None:
            self._values["jupyter_server_app_settings"] = jupyter_server_app_settings
        if kernel_gateway_app_settings is not None:
            self._values["kernel_gateway_app_settings"] = kernel_gateway_app_settings

    @builtins.property
    def jupyter_server_app_settings(
        self,
    ) -> typing.Optional["SagemakerSpaceSpaceSettingsJupyterServerAppSettings"]:
        '''jupyter_server_app_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#jupyter_server_app_settings SagemakerSpace#jupyter_server_app_settings}
        '''
        result = self._values.get("jupyter_server_app_settings")
        return typing.cast(typing.Optional["SagemakerSpaceSpaceSettingsJupyterServerAppSettings"], result)

    @builtins.property
    def kernel_gateway_app_settings(
        self,
    ) -> typing.Optional["SagemakerSpaceSpaceSettingsKernelGatewayAppSettings"]:
        '''kernel_gateway_app_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#kernel_gateway_app_settings SagemakerSpace#kernel_gateway_app_settings}
        '''
        result = self._values.get("kernel_gateway_app_settings")
        return typing.cast(typing.Optional["SagemakerSpaceSpaceSettingsKernelGatewayAppSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerSpaceSpaceSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsJupyterServerAppSettings",
    jsii_struct_bases=[],
    name_mapping={
        "default_resource_spec": "defaultResourceSpec",
        "code_repository": "codeRepository",
        "lifecycle_config_arns": "lifecycleConfigArns",
    },
)
class SagemakerSpaceSpaceSettingsJupyterServerAppSettings:
    def __init__(
        self,
        *,
        default_resource_spec: typing.Union["SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]],
        code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#default_resource_spec SagemakerSpace#default_resource_spec}
        :param code_repository: code_repository block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#code_repository SagemakerSpace#code_repository}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arns SagemakerSpace#lifecycle_config_arns}.
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db4d00de74dd6b44144ea20d5f07600f7bff0c49be30f931531d1293c093db9)
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
            check_type(argname="argument code_repository", value=code_repository, expected_type=type_hints["code_repository"])
            check_type(argname="argument lifecycle_config_arns", value=lifecycle_config_arns, expected_type=type_hints["lifecycle_config_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_resource_spec": default_resource_spec,
        }
        if code_repository is not None:
            self._values["code_repository"] = code_repository
        if lifecycle_config_arns is not None:
            self._values["lifecycle_config_arns"] = lifecycle_config_arns

    @builtins.property
    def default_resource_spec(
        self,
    ) -> "SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec":
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#default_resource_spec SagemakerSpace#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        assert result is not None, "Required property 'default_resource_spec' is missing"
        return typing.cast("SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec", result)

    @builtins.property
    def code_repository(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository"]]]:
        '''code_repository block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#code_repository SagemakerSpace#code_repository}
        '''
        result = self._values.get("code_repository")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository"]]], result)

    @builtins.property
    def lifecycle_config_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arns SagemakerSpace#lifecycle_config_arns}.'''
        result = self._values.get("lifecycle_config_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerSpaceSpaceSettingsJupyterServerAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository",
    jsii_struct_bases=[],
    name_mapping={"repository_url": "repositoryUrl"},
)
class SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository:
    def __init__(self, *, repository_url: builtins.str) -> None:
        '''
        :param repository_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#repository_url SagemakerSpace#repository_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b82c6130dc75373611c201962b28bce84954ffb1ee9932f9dd18b3ffd760c3a3)
            check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_url": repository_url,
        }

    @builtins.property
    def repository_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#repository_url SagemakerSpace#repository_url}.'''
        result = self._values.get("repository_url")
        assert result is not None, "Required property 'repository_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepositoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepositoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc0ea2bb824b535742e96e0b20d689bea2390d7b721f765ec724bc3443f89d1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepositoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac054c337ddd971db778eb86257f91983c77341516d60f873c465c03e5c0cec9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepositoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9520b400c2bcca0731df04a932a1452e1ef4a9085f4b0d923d9bf97f7d92c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80fe1da9fd51d0580f3d9728add69500292a18bc3bab07917e4c4be604ee67bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfb9ae71d2fd67b3e04bf9e31f70dd4615430715acad7766caac2723d624a02e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66536ba2909dfb96199ef0c8c342f0a9eebc91c236742313a637e2e5df06ee03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f41343d08860d7b29ea72a05b4942c3e32de569ca2a51bd132af01c6a33224a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="repositoryUrlInput")
    def repository_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryUrl")
    def repository_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryUrl"))

    @repository_url.setter
    def repository_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c60c454ddb00cf89f6c653d4077a0075f0f5c55b1681b0d39137e6017a9447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryUrl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c264b476d5da749923bc519300bd83730402805d97f3f1033a834916e72e7b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#instance_type SagemakerSpace#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arn SagemakerSpace#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_arn SagemakerSpace#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_version_arn SagemakerSpace#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa59c016048284310ebc1f1fd0f42017840d586385e759dd66a8c52e44257da7)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#instance_type SagemakerSpace#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arn SagemakerSpace#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_arn SagemakerSpace#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_version_arn SagemakerSpace#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e070a70d7566bc41eb14c3b56cc985f10eec1e964a246019f163974eff9731f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98cd6400e31f86c585216819a32beb9b3d6ca26299fbaa3708cb2dc8258e73f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d33d0d9d7cf07ad4468ccdd0635fae6399a15ce662a9471e62fbb9929b9d243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad35af61089808e6bad633c5adf51edad33629994cd7c366903f47ad74c987b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4860c5816f4a5eef3dd9850881630c16ae6b851c756f18b238798afcc0a46629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5ffb28dc529c51cb110ef96359e528ad8621a475e9fe85a05400ee2626ea19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerSpaceSpaceSettingsJupyterServerAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsJupyterServerAppSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15d44cb0878cbb0dfcfc303f9b5711193283362e026403047fbe64f5dfbbc527)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCodeRepository")
    def put_code_repository(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03b998750877c5251508f12b8b274bf918aeda25a10142b26b389c82169daf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCodeRepository", [value]))

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#instance_type SagemakerSpace#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arn SagemakerSpace#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_arn SagemakerSpace#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_version_arn SagemakerSpace#sagemaker_image_version_arn}.
        '''
        value = SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @jsii.member(jsii_name="resetCodeRepository")
    def reset_code_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeRepository", []))

    @jsii.member(jsii_name="resetLifecycleConfigArns")
    def reset_lifecycle_config_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArns", []))

    @builtins.property
    @jsii.member(jsii_name="codeRepository")
    def code_repository(
        self,
    ) -> SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepositoryList:
        return typing.cast(SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepositoryList, jsii.get(self, "codeRepository"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="codeRepositoryInput")
    def code_repository_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository]]], jsii.get(self, "codeRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnsInput")
    def lifecycle_config_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "lifecycleConfigArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArns")
    def lifecycle_config_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lifecycleConfigArns"))

    @lifecycle_config_arns.setter
    def lifecycle_config_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c903508ea20ae39081b9f97917ee017e10b3e16ff4ea38cc006448c67688942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArns", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettings]:
        return typing.cast(typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae77d657bc66e1797ab52d4ab1ef0585dd0bdb32bbf769285457911c1f08f36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsKernelGatewayAppSettings",
    jsii_struct_bases=[],
    name_mapping={
        "default_resource_spec": "defaultResourceSpec",
        "custom_image": "customImage",
        "lifecycle_config_arns": "lifecycleConfigArns",
    },
)
class SagemakerSpaceSpaceSettingsKernelGatewayAppSettings:
    def __init__(
        self,
        *,
        default_resource_spec: typing.Union["SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]],
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#default_resource_spec SagemakerSpace#default_resource_spec}
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#custom_image SagemakerSpace#custom_image}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arns SagemakerSpace#lifecycle_config_arns}.
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49fc14cd5d5f0e8fba517fcc16c16a223eb284992daafe6cb034187ce8768735)
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
            check_type(argname="argument custom_image", value=custom_image, expected_type=type_hints["custom_image"])
            check_type(argname="argument lifecycle_config_arns", value=lifecycle_config_arns, expected_type=type_hints["lifecycle_config_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_resource_spec": default_resource_spec,
        }
        if custom_image is not None:
            self._values["custom_image"] = custom_image
        if lifecycle_config_arns is not None:
            self._values["lifecycle_config_arns"] = lifecycle_config_arns

    @builtins.property
    def default_resource_spec(
        self,
    ) -> "SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec":
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#default_resource_spec SagemakerSpace#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        assert result is not None, "Required property 'default_resource_spec' is missing"
        return typing.cast("SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec", result)

    @builtins.property
    def custom_image(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage"]]]:
        '''custom_image block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#custom_image SagemakerSpace#custom_image}
        '''
        result = self._values.get("custom_image")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage"]]], result)

    @builtins.property
    def lifecycle_config_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arns SagemakerSpace#lifecycle_config_arns}.'''
        result = self._values.get("lifecycle_config_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerSpaceSpaceSettingsKernelGatewayAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage",
    jsii_struct_bases=[],
    name_mapping={
        "app_image_config_name": "appImageConfigName",
        "image_name": "imageName",
        "image_version_number": "imageVersionNumber",
    },
)
class SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage:
    def __init__(
        self,
        *,
        app_image_config_name: builtins.str,
        image_name: builtins.str,
        image_version_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param app_image_config_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#app_image_config_name SagemakerSpace#app_image_config_name}.
        :param image_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#image_name SagemakerSpace#image_name}.
        :param image_version_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#image_version_number SagemakerSpace#image_version_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f69f60c449429d2644f1a406f11b6b4bbae66f62f7fa01011c9583f2bb650f)
            check_type(argname="argument app_image_config_name", value=app_image_config_name, expected_type=type_hints["app_image_config_name"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_version_number", value=image_version_number, expected_type=type_hints["image_version_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_image_config_name": app_image_config_name,
            "image_name": image_name,
        }
        if image_version_number is not None:
            self._values["image_version_number"] = image_version_number

    @builtins.property
    def app_image_config_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#app_image_config_name SagemakerSpace#app_image_config_name}.'''
        result = self._values.get("app_image_config_name")
        assert result is not None, "Required property 'app_image_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#image_name SagemakerSpace#image_name}.'''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_version_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#image_version_number SagemakerSpace#image_version_number}.'''
        result = self._values.get("image_version_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19ff7bfb0ae091f930aec23ece4e479d7f5e14f5e8073d19d6eb19c4823b709c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a758ac3b106ef05cf6eb3f9fad4295feac696bfb39b63acc32a77b9f76ecfb32)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f33402da1fdac3c54934d0272df23ed6daa7fa36e40d7740d064927d45208ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cacb532181738f34f181f26587e19673f1c9d3d877277c710bf52d015ab890f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5bb93b0a3226e059d69186a6df5cb75e59e46de563727d18edbde51ceaada4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e44a944e6f34a64b44ffe4765ae1fe074ccd95dc3d4857d97756c296df6e336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e164bd9a3bba626c95bf32d8fe66bdc2bcec847912218bb073a3b52e9974f6e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetImageVersionNumber")
    def reset_image_version_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersionNumber", []))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigNameInput")
    def app_image_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appImageConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumberInput")
    def image_version_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageVersionNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigName")
    def app_image_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appImageConfigName"))

    @app_image_config_name.setter
    def app_image_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647202eb24d4a6481997b74140b6a83746631a0e85bdfbef6e5ebd260c4ea710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appImageConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc791f5c86efd08de3c3aedf58a4533202df97f0c734d80f7a711eea940231b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumber")
    def image_version_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageVersionNumber"))

    @image_version_number.setter
    def image_version_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bff7a89e741d45538926bf9639a026e486476aae9b56c2e5411b2338f6e1c6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersionNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c24e01c3367ccd7561a40a408735afaf18c0aa9809ad803ee4da80fd11dca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#instance_type SagemakerSpace#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arn SagemakerSpace#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_arn SagemakerSpace#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_version_arn SagemakerSpace#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f84be4b2358ff03b3268efd074933de4d45e4e7a4b981c924f0d5d7d8d8bf6d)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#instance_type SagemakerSpace#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arn SagemakerSpace#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_arn SagemakerSpace#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_version_arn SagemakerSpace#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1da943e222202390b4aed9af7a7136a964bd005e035a968a7a7886a2574c1229)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794bf8a5e3f791e5941c6f77a7e8d42b1f8ce8775dbb420d3a1ba4422b457a75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5df7a8318113d44b7f5f7daaef3d73c42dd3d0dbf5bdf184182b10d764d4fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e4ad2343c1a36853b5a1a2101e2253d61fa4d258901d624c46c95d8cbc0415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eff6cedd5cb008a90a3439fb73df16f5e4f2e32400f10bff65c24cb7e3b383b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c608698a47a70906a0ea68df141ff715f90478ba1fc0de39aa21c6012ea98b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc933e81453c9ce7a63de1461d2c4cc4689b44b2ffe883f66046fdbd847ed7f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomImage")
    def put_custom_image(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cacca4ed1f30f70b4c8879b9e1c308b49ba36b9d52519113cea84d0179e6b966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomImage", [value]))

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#instance_type SagemakerSpace#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arn SagemakerSpace#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_arn SagemakerSpace#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#sagemaker_image_version_arn SagemakerSpace#sagemaker_image_version_arn}.
        '''
        value = SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @jsii.member(jsii_name="resetCustomImage")
    def reset_custom_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomImage", []))

    @jsii.member(jsii_name="resetLifecycleConfigArns")
    def reset_lifecycle_config_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArns", []))

    @builtins.property
    @jsii.member(jsii_name="customImage")
    def custom_image(
        self,
    ) -> SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImageList:
        return typing.cast(SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImageList, jsii.get(self, "customImage"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="customImageInput")
    def custom_image_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage]]], jsii.get(self, "customImageInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnsInput")
    def lifecycle_config_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "lifecycleConfigArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArns")
    def lifecycle_config_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lifecycleConfigArns"))

    @lifecycle_config_arns.setter
    def lifecycle_config_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1600005712c9ea07b02be8cce35f82312cd3eadbd0535c1c0e6c59e831529e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArns", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettings]:
        return typing.cast(typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9d657f2e818c12515a45d485e9e05cb98ecc43265c54ca34220861f85098ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerSpaceSpaceSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerSpace.SagemakerSpaceSpaceSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ae26ef9a20851e1e0d170e1f6a64952e5fa2f3670f0f32dae49f31615036de8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putJupyterServerAppSettings")
    def put_jupyter_server_app_settings(
        self,
        *,
        default_resource_spec: typing.Union[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]],
        code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#default_resource_spec SagemakerSpace#default_resource_spec}
        :param code_repository: code_repository block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#code_repository SagemakerSpace#code_repository}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arns SagemakerSpace#lifecycle_config_arns}.
        '''
        value = SagemakerSpaceSpaceSettingsJupyterServerAppSettings(
            default_resource_spec=default_resource_spec,
            code_repository=code_repository,
            lifecycle_config_arns=lifecycle_config_arns,
        )

        return typing.cast(None, jsii.invoke(self, "putJupyterServerAppSettings", [value]))

    @jsii.member(jsii_name="putKernelGatewayAppSettings")
    def put_kernel_gateway_app_settings(
        self,
        *,
        default_resource_spec: typing.Union[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]],
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#default_resource_spec SagemakerSpace#default_resource_spec}
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#custom_image SagemakerSpace#custom_image}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_space#lifecycle_config_arns SagemakerSpace#lifecycle_config_arns}.
        '''
        value = SagemakerSpaceSpaceSettingsKernelGatewayAppSettings(
            default_resource_spec=default_resource_spec,
            custom_image=custom_image,
            lifecycle_config_arns=lifecycle_config_arns,
        )

        return typing.cast(None, jsii.invoke(self, "putKernelGatewayAppSettings", [value]))

    @jsii.member(jsii_name="resetJupyterServerAppSettings")
    def reset_jupyter_server_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJupyterServerAppSettings", []))

    @jsii.member(jsii_name="resetKernelGatewayAppSettings")
    def reset_kernel_gateway_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKernelGatewayAppSettings", []))

    @builtins.property
    @jsii.member(jsii_name="jupyterServerAppSettings")
    def jupyter_server_app_settings(
        self,
    ) -> SagemakerSpaceSpaceSettingsJupyterServerAppSettingsOutputReference:
        return typing.cast(SagemakerSpaceSpaceSettingsJupyterServerAppSettingsOutputReference, jsii.get(self, "jupyterServerAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="kernelGatewayAppSettings")
    def kernel_gateway_app_settings(
        self,
    ) -> SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsOutputReference:
        return typing.cast(SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsOutputReference, jsii.get(self, "kernelGatewayAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="jupyterServerAppSettingsInput")
    def jupyter_server_app_settings_input(
        self,
    ) -> typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettings]:
        return typing.cast(typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettings], jsii.get(self, "jupyterServerAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="kernelGatewayAppSettingsInput")
    def kernel_gateway_app_settings_input(
        self,
    ) -> typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettings]:
        return typing.cast(typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettings], jsii.get(self, "kernelGatewayAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerSpaceSpaceSettings]:
        return typing.cast(typing.Optional[SagemakerSpaceSpaceSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerSpaceSpaceSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc74da3e9d11926298068127eab18ee807647e423be5478e51278573d70eeced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SagemakerSpace",
    "SagemakerSpaceConfig",
    "SagemakerSpaceSpaceSettings",
    "SagemakerSpaceSpaceSettingsJupyterServerAppSettings",
    "SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository",
    "SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepositoryList",
    "SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepositoryOutputReference",
    "SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec",
    "SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerSpaceSpaceSettingsJupyterServerAppSettingsOutputReference",
    "SagemakerSpaceSpaceSettingsKernelGatewayAppSettings",
    "SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage",
    "SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImageList",
    "SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImageOutputReference",
    "SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec",
    "SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsOutputReference",
    "SagemakerSpaceSpaceSettingsOutputReference",
]

publication.publish()

def _typecheckingstub__3387f8ee82cf0f5651f5129108d1c232b61dc93bd9bb364daeef9679c21e6b18(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    domain_id: builtins.str,
    space_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    space_settings: typing.Optional[typing.Union[SagemakerSpaceSpaceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__40c8b560eb9785c44cabe47a80b83e39e49ba42051f5fc9f3de50656c86c9c67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6578ffbbc2330ac0c398923bedb4921c716f77faa791b5a7b3e693a34246e3c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c11c6f024f5b5bd168bb7d3b3971df4255888439969b65e645380603c68fcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91728e83c1f80c69ae5502b079852e1a630a86be4350bc6562da111714a366a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3d1c7af083e893c82434486939ea45eb7a9d4203dcd2ff40c621835291745f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115ba9c4208d250962e44e6e773b8dbc42a66b057999e8953fb3bbb7f469eafd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain_id: builtins.str,
    space_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    space_settings: typing.Optional[typing.Union[SagemakerSpaceSpaceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e8cf736fe2bea251c6fc3f1d447b933be972f65a73ef66a1422714399b8a6a(
    *,
    jupyter_server_app_settings: typing.Optional[typing.Union[SagemakerSpaceSpaceSettingsJupyterServerAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kernel_gateway_app_settings: typing.Optional[typing.Union[SagemakerSpaceSpaceSettingsKernelGatewayAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db4d00de74dd6b44144ea20d5f07600f7bff0c49be30f931531d1293c093db9(
    *,
    default_resource_spec: typing.Union[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]],
    code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82c6130dc75373611c201962b28bce84954ffb1ee9932f9dd18b3ffd760c3a3(
    *,
    repository_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0ea2bb824b535742e96e0b20d689bea2390d7b721f765ec724bc3443f89d1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac054c337ddd971db778eb86257f91983c77341516d60f873c465c03e5c0cec9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9520b400c2bcca0731df04a932a1452e1ef4a9085f4b0d923d9bf97f7d92c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fe1da9fd51d0580f3d9728add69500292a18bc3bab07917e4c4be604ee67bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb9ae71d2fd67b3e04bf9e31f70dd4615430715acad7766caac2723d624a02e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66536ba2909dfb96199ef0c8c342f0a9eebc91c236742313a637e2e5df06ee03(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41343d08860d7b29ea72a05b4942c3e32de569ca2a51bd132af01c6a33224a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c60c454ddb00cf89f6c653d4077a0075f0f5c55b1681b0d39137e6017a9447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c264b476d5da749923bc519300bd83730402805d97f3f1033a834916e72e7b0(
    value: typing.Optional[typing.Union[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa59c016048284310ebc1f1fd0f42017840d586385e759dd66a8c52e44257da7(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e070a70d7566bc41eb14c3b56cc985f10eec1e964a246019f163974eff9731f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98cd6400e31f86c585216819a32beb9b3d6ca26299fbaa3708cb2dc8258e73f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d33d0d9d7cf07ad4468ccdd0635fae6399a15ce662a9471e62fbb9929b9d243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad35af61089808e6bad633c5adf51edad33629994cd7c366903f47ad74c987b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4860c5816f4a5eef3dd9850881630c16ae6b851c756f18b238798afcc0a46629(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5ffb28dc529c51cb110ef96359e528ad8621a475e9fe85a05400ee2626ea19(
    value: typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d44cb0878cbb0dfcfc303f9b5711193283362e026403047fbe64f5dfbbc527(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03b998750877c5251508f12b8b274bf918aeda25a10142b26b389c82169daf5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerSpaceSpaceSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c903508ea20ae39081b9f97917ee017e10b3e16ff4ea38cc006448c67688942(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae77d657bc66e1797ab52d4ab1ef0585dd0bdb32bbf769285457911c1f08f36(
    value: typing.Optional[SagemakerSpaceSpaceSettingsJupyterServerAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fc14cd5d5f0e8fba517fcc16c16a223eb284992daafe6cb034187ce8768735(
    *,
    default_resource_spec: typing.Union[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]],
    custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f69f60c449429d2644f1a406f11b6b4bbae66f62f7fa01011c9583f2bb650f(
    *,
    app_image_config_name: builtins.str,
    image_name: builtins.str,
    image_version_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ff7bfb0ae091f930aec23ece4e479d7f5e14f5e8073d19d6eb19c4823b709c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a758ac3b106ef05cf6eb3f9fad4295feac696bfb39b63acc32a77b9f76ecfb32(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f33402da1fdac3c54934d0272df23ed6daa7fa36e40d7740d064927d45208ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cacb532181738f34f181f26587e19673f1c9d3d877277c710bf52d015ab890f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5bb93b0a3226e059d69186a6df5cb75e59e46de563727d18edbde51ceaada4b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e44a944e6f34a64b44ffe4765ae1fe074ccd95dc3d4857d97756c296df6e336(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e164bd9a3bba626c95bf32d8fe66bdc2bcec847912218bb073a3b52e9974f6e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647202eb24d4a6481997b74140b6a83746631a0e85bdfbef6e5ebd260c4ea710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc791f5c86efd08de3c3aedf58a4533202df97f0c734d80f7a711eea940231b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bff7a89e741d45538926bf9639a026e486476aae9b56c2e5411b2338f6e1c6f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c24e01c3367ccd7561a40a408735afaf18c0aa9809ad803ee4da80fd11dca4(
    value: typing.Optional[typing.Union[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f84be4b2358ff03b3268efd074933de4d45e4e7a4b981c924f0d5d7d8d8bf6d(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da943e222202390b4aed9af7a7136a964bd005e035a968a7a7886a2574c1229(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794bf8a5e3f791e5941c6f77a7e8d42b1f8ce8775dbb420d3a1ba4422b457a75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5df7a8318113d44b7f5f7daaef3d73c42dd3d0dbf5bdf184182b10d764d4fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e4ad2343c1a36853b5a1a2101e2253d61fa4d258901d624c46c95d8cbc0415(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eff6cedd5cb008a90a3439fb73df16f5e4f2e32400f10bff65c24cb7e3b383b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c608698a47a70906a0ea68df141ff715f90478ba1fc0de39aa21c6012ea98b6(
    value: typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc933e81453c9ce7a63de1461d2c4cc4689b44b2ffe883f66046fdbd847ed7f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacca4ed1f30f70b4c8879b9e1c308b49ba36b9d52519113cea84d0179e6b966(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerSpaceSpaceSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1600005712c9ea07b02be8cce35f82312cd3eadbd0535c1c0e6c59e831529e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9d657f2e818c12515a45d485e9e05cb98ecc43265c54ca34220861f85098ea(
    value: typing.Optional[SagemakerSpaceSpaceSettingsKernelGatewayAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae26ef9a20851e1e0d170e1f6a64952e5fa2f3670f0f32dae49f31615036de8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc74da3e9d11926298068127eab18ee807647e423be5478e51278573d70eeced(
    value: typing.Optional[SagemakerSpaceSpaceSettings],
) -> None:
    """Type checking stubs"""
    pass
