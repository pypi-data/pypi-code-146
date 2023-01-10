'''
# `aws_fsx_ontap_volume`

Refer to the Terraform Registory for docs: [`aws_fsx_ontap_volume`](https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume).
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


class FsxOntapVolume(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fsxOntapVolume.FsxOntapVolume",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume aws_fsx_ontap_volume}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        junction_path: builtins.str,
        name: builtins.str,
        size_in_megabytes: jsii.Number,
        storage_efficiency_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        storage_virtual_machine_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        security_style: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tiering_policy: typing.Optional[typing.Union["FsxOntapVolumeTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["FsxOntapVolumeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume aws_fsx_ontap_volume} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param junction_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#junction_path FsxOntapVolume#junction_path}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#name FsxOntapVolume#name}.
        :param size_in_megabytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#size_in_megabytes FsxOntapVolume#size_in_megabytes}.
        :param storage_efficiency_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#storage_efficiency_enabled FsxOntapVolume#storage_efficiency_enabled}.
        :param storage_virtual_machine_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#storage_virtual_machine_id FsxOntapVolume#storage_virtual_machine_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#id FsxOntapVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param security_style: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#security_style FsxOntapVolume#security_style}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#tags FsxOntapVolume#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#tags_all FsxOntapVolume#tags_all}.
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#tiering_policy FsxOntapVolume#tiering_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#timeouts FsxOntapVolume#timeouts}
        :param volume_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#volume_type FsxOntapVolume#volume_type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33bd30fe951448e6a94703bc9d114d96b256ce72087df1117866bc3400045f5e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FsxOntapVolumeConfig(
            junction_path=junction_path,
            name=name,
            size_in_megabytes=size_in_megabytes,
            storage_efficiency_enabled=storage_efficiency_enabled,
            storage_virtual_machine_id=storage_virtual_machine_id,
            id=id,
            security_style=security_style,
            tags=tags,
            tags_all=tags_all,
            tiering_policy=tiering_policy,
            timeouts=timeouts,
            volume_type=volume_type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putTieringPolicy")
    def put_tiering_policy(
        self,
        *,
        cooling_period: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cooling_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#cooling_period FsxOntapVolume#cooling_period}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#name FsxOntapVolume#name}.
        '''
        value = FsxOntapVolumeTieringPolicy(cooling_period=cooling_period, name=name)

        return typing.cast(None, jsii.invoke(self, "putTieringPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#create FsxOntapVolume#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#delete FsxOntapVolume#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#update FsxOntapVolume#update}.
        '''
        value = FsxOntapVolumeTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSecurityStyle")
    def reset_security_style(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityStyle", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTieringPolicy")
    def reset_tiering_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTieringPolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVolumeType")
    def reset_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeType", []))

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
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @builtins.property
    @jsii.member(jsii_name="flexcacheEndpointType")
    def flexcache_endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flexcacheEndpointType"))

    @builtins.property
    @jsii.member(jsii_name="ontapVolumeType")
    def ontap_volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ontapVolumeType"))

    @builtins.property
    @jsii.member(jsii_name="tieringPolicy")
    def tiering_policy(self) -> "FsxOntapVolumeTieringPolicyOutputReference":
        return typing.cast("FsxOntapVolumeTieringPolicyOutputReference", jsii.get(self, "tieringPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FsxOntapVolumeTimeoutsOutputReference":
        return typing.cast("FsxOntapVolumeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="junctionPathInput")
    def junction_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "junctionPathInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityStyleInput")
    def security_style_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityStyleInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInMegabytesInput")
    def size_in_megabytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInMegabytesInput"))

    @builtins.property
    @jsii.member(jsii_name="storageEfficiencyEnabledInput")
    def storage_efficiency_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "storageEfficiencyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="storageVirtualMachineIdInput")
    def storage_virtual_machine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageVirtualMachineIdInput"))

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
    @jsii.member(jsii_name="tieringPolicyInput")
    def tiering_policy_input(self) -> typing.Optional["FsxOntapVolumeTieringPolicy"]:
        return typing.cast(typing.Optional["FsxOntapVolumeTieringPolicy"], jsii.get(self, "tieringPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["FsxOntapVolumeTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["FsxOntapVolumeTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260bc07892b494ef5eea79eb03c0eb8efb0c05086eff0516e1291bde14445a2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="junctionPath")
    def junction_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "junctionPath"))

    @junction_path.setter
    def junction_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75516a75dcf0c6cebd1298ce1106be1b183d36e3ff380660ea308a8d5b297cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "junctionPath", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331d45ccbf8932d259ead1071a237118c3e6746216036b5653d151e2f43287f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="securityStyle")
    def security_style(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityStyle"))

    @security_style.setter
    def security_style(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cb8e4219cd411785c10190fdb07e0cd5a8e78d13a495eece5a601def5dd17fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityStyle", value)

    @builtins.property
    @jsii.member(jsii_name="sizeInMegabytes")
    def size_in_megabytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeInMegabytes"))

    @size_in_megabytes.setter
    def size_in_megabytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c568529c75335689fd7eeca287638ed80dc5c564c20a519b81dfd9a209b44406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInMegabytes", value)

    @builtins.property
    @jsii.member(jsii_name="storageEfficiencyEnabled")
    def storage_efficiency_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "storageEfficiencyEnabled"))

    @storage_efficiency_enabled.setter
    def storage_efficiency_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a84c7704272e344015859d28b5279a78553129087fb16a572c8d196006c06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageEfficiencyEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="storageVirtualMachineId")
    def storage_virtual_machine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageVirtualMachineId"))

    @storage_virtual_machine_id.setter
    def storage_virtual_machine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eba4a7f54c826112aa35fe5444b3e4f093c1bbe0c7c7e1f6d0edfb385e6ba302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageVirtualMachineId", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f168f8d4c9da26138e7c25d20bf85bf53dc62fb3dda5c169d6b80f4766511942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448ca398bc6285827b2656db0851d1d942fde95ce577eacc02e3944fc3a5d2ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4bd46d38fc8b15b8f9316c535dd0e9d303acc2f712c671b7de27c6eb775cb4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fsxOntapVolume.FsxOntapVolumeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "junction_path": "junctionPath",
        "name": "name",
        "size_in_megabytes": "sizeInMegabytes",
        "storage_efficiency_enabled": "storageEfficiencyEnabled",
        "storage_virtual_machine_id": "storageVirtualMachineId",
        "id": "id",
        "security_style": "securityStyle",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tiering_policy": "tieringPolicy",
        "timeouts": "timeouts",
        "volume_type": "volumeType",
    },
)
class FsxOntapVolumeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        junction_path: builtins.str,
        name: builtins.str,
        size_in_megabytes: jsii.Number,
        storage_efficiency_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        storage_virtual_machine_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        security_style: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tiering_policy: typing.Optional[typing.Union["FsxOntapVolumeTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["FsxOntapVolumeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param junction_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#junction_path FsxOntapVolume#junction_path}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#name FsxOntapVolume#name}.
        :param size_in_megabytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#size_in_megabytes FsxOntapVolume#size_in_megabytes}.
        :param storage_efficiency_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#storage_efficiency_enabled FsxOntapVolume#storage_efficiency_enabled}.
        :param storage_virtual_machine_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#storage_virtual_machine_id FsxOntapVolume#storage_virtual_machine_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#id FsxOntapVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param security_style: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#security_style FsxOntapVolume#security_style}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#tags FsxOntapVolume#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#tags_all FsxOntapVolume#tags_all}.
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#tiering_policy FsxOntapVolume#tiering_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#timeouts FsxOntapVolume#timeouts}
        :param volume_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#volume_type FsxOntapVolume#volume_type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(tiering_policy, dict):
            tiering_policy = FsxOntapVolumeTieringPolicy(**tiering_policy)
        if isinstance(timeouts, dict):
            timeouts = FsxOntapVolumeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c0bd0efd37f12e31a09c15e5c2fa3886f6385b85ab1897fe0e64980e74fa91)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument junction_path", value=junction_path, expected_type=type_hints["junction_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument size_in_megabytes", value=size_in_megabytes, expected_type=type_hints["size_in_megabytes"])
            check_type(argname="argument storage_efficiency_enabled", value=storage_efficiency_enabled, expected_type=type_hints["storage_efficiency_enabled"])
            check_type(argname="argument storage_virtual_machine_id", value=storage_virtual_machine_id, expected_type=type_hints["storage_virtual_machine_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument security_style", value=security_style, expected_type=type_hints["security_style"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tiering_policy", value=tiering_policy, expected_type=type_hints["tiering_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "junction_path": junction_path,
            "name": name,
            "size_in_megabytes": size_in_megabytes,
            "storage_efficiency_enabled": storage_efficiency_enabled,
            "storage_virtual_machine_id": storage_virtual_machine_id,
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
        if security_style is not None:
            self._values["security_style"] = security_style
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tiering_policy is not None:
            self._values["tiering_policy"] = tiering_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if volume_type is not None:
            self._values["volume_type"] = volume_type

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
    def junction_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#junction_path FsxOntapVolume#junction_path}.'''
        result = self._values.get("junction_path")
        assert result is not None, "Required property 'junction_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#name FsxOntapVolume#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size_in_megabytes(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#size_in_megabytes FsxOntapVolume#size_in_megabytes}.'''
        result = self._values.get("size_in_megabytes")
        assert result is not None, "Required property 'size_in_megabytes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def storage_efficiency_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#storage_efficiency_enabled FsxOntapVolume#storage_efficiency_enabled}.'''
        result = self._values.get("storage_efficiency_enabled")
        assert result is not None, "Required property 'storage_efficiency_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def storage_virtual_machine_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#storage_virtual_machine_id FsxOntapVolume#storage_virtual_machine_id}.'''
        result = self._values.get("storage_virtual_machine_id")
        assert result is not None, "Required property 'storage_virtual_machine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#id FsxOntapVolume#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_style(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#security_style FsxOntapVolume#security_style}.'''
        result = self._values.get("security_style")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#tags FsxOntapVolume#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#tags_all FsxOntapVolume#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tiering_policy(self) -> typing.Optional["FsxOntapVolumeTieringPolicy"]:
        '''tiering_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#tiering_policy FsxOntapVolume#tiering_policy}
        '''
        result = self._values.get("tiering_policy")
        return typing.cast(typing.Optional["FsxOntapVolumeTieringPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FsxOntapVolumeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#timeouts FsxOntapVolume#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FsxOntapVolumeTimeouts"], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#volume_type FsxOntapVolume#volume_type}.'''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fsxOntapVolume.FsxOntapVolumeTieringPolicy",
    jsii_struct_bases=[],
    name_mapping={"cooling_period": "coolingPeriod", "name": "name"},
)
class FsxOntapVolumeTieringPolicy:
    def __init__(
        self,
        *,
        cooling_period: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cooling_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#cooling_period FsxOntapVolume#cooling_period}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#name FsxOntapVolume#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4869453cdd9a892a2c8a627237463100a511053741142bbbaf0b8bab38a1238)
            check_type(argname="argument cooling_period", value=cooling_period, expected_type=type_hints["cooling_period"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cooling_period is not None:
            self._values["cooling_period"] = cooling_period
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def cooling_period(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#cooling_period FsxOntapVolume#cooling_period}.'''
        result = self._values.get("cooling_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#name FsxOntapVolume#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeTieringPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FsxOntapVolumeTieringPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fsxOntapVolume.FsxOntapVolumeTieringPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fb2a143b408d4300f58dd4308661c2c1853500ab1154b5b44e49afe3df7b98b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCoolingPeriod")
    def reset_cooling_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoolingPeriod", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="coolingPeriodInput")
    def cooling_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coolingPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="coolingPeriod")
    def cooling_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coolingPeriod"))

    @cooling_period.setter
    def cooling_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3930d04e72e10f0ca43228378e53c62fdeb45b366dac38363c8219f755110e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolingPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac206c72f1ccdd72ef964b6a099bdcd9b93852db8a60da14d1741c588d9b22e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FsxOntapVolumeTieringPolicy]:
        return typing.cast(typing.Optional[FsxOntapVolumeTieringPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FsxOntapVolumeTieringPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ea2ce9d446845584acb7f8f7f0759e3e1dd6f781109c1e459e3716639a13ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fsxOntapVolume.FsxOntapVolumeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class FsxOntapVolumeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#create FsxOntapVolume#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#delete FsxOntapVolume#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#update FsxOntapVolume#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6845c8ab911ff226e38fb7f85fb24396547a2d88ddf0dca1caefb6403405120)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#create FsxOntapVolume#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#delete FsxOntapVolume#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fsx_ontap_volume#update FsxOntapVolume#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FsxOntapVolumeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fsxOntapVolume.FsxOntapVolumeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97cd974272041719d3d472710040c1d9394294823ea1710987808d69e5fc8d9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__696cb236f37562354da0f8d7865462604b057cf8d2e93f348be1665f32c3a389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c22431dbc789fd5969a4dfbe025c6d4febb3259aac2e25572148781506a07e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8292076365b3c5c169e85b986d970c1bbf63f66998c7bdc292dc36ccb500277f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[FsxOntapVolumeTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[FsxOntapVolumeTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[FsxOntapVolumeTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac03c2e9469dd97962a34a318bb5c8395aa6916ec05299bc89e5e53d90cf81d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "FsxOntapVolume",
    "FsxOntapVolumeConfig",
    "FsxOntapVolumeTieringPolicy",
    "FsxOntapVolumeTieringPolicyOutputReference",
    "FsxOntapVolumeTimeouts",
    "FsxOntapVolumeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__33bd30fe951448e6a94703bc9d114d96b256ce72087df1117866bc3400045f5e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    junction_path: builtins.str,
    name: builtins.str,
    size_in_megabytes: jsii.Number,
    storage_efficiency_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    storage_virtual_machine_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    security_style: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tiering_policy: typing.Optional[typing.Union[FsxOntapVolumeTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[FsxOntapVolumeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__260bc07892b494ef5eea79eb03c0eb8efb0c05086eff0516e1291bde14445a2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75516a75dcf0c6cebd1298ce1106be1b183d36e3ff380660ea308a8d5b297cdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331d45ccbf8932d259ead1071a237118c3e6746216036b5653d151e2f43287f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb8e4219cd411785c10190fdb07e0cd5a8e78d13a495eece5a601def5dd17fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c568529c75335689fd7eeca287638ed80dc5c564c20a519b81dfd9a209b44406(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a84c7704272e344015859d28b5279a78553129087fb16a572c8d196006c06a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba4a7f54c826112aa35fe5444b3e4f093c1bbe0c7c7e1f6d0edfb385e6ba302(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f168f8d4c9da26138e7c25d20bf85bf53dc62fb3dda5c169d6b80f4766511942(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448ca398bc6285827b2656db0851d1d942fde95ce577eacc02e3944fc3a5d2ac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4bd46d38fc8b15b8f9316c535dd0e9d303acc2f712c671b7de27c6eb775cb4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c0bd0efd37f12e31a09c15e5c2fa3886f6385b85ab1897fe0e64980e74fa91(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    junction_path: builtins.str,
    name: builtins.str,
    size_in_megabytes: jsii.Number,
    storage_efficiency_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    storage_virtual_machine_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    security_style: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tiering_policy: typing.Optional[typing.Union[FsxOntapVolumeTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[FsxOntapVolumeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4869453cdd9a892a2c8a627237463100a511053741142bbbaf0b8bab38a1238(
    *,
    cooling_period: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb2a143b408d4300f58dd4308661c2c1853500ab1154b5b44e49afe3df7b98b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3930d04e72e10f0ca43228378e53c62fdeb45b366dac38363c8219f755110e79(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac206c72f1ccdd72ef964b6a099bdcd9b93852db8a60da14d1741c588d9b22e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ea2ce9d446845584acb7f8f7f0759e3e1dd6f781109c1e459e3716639a13ef(
    value: typing.Optional[FsxOntapVolumeTieringPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6845c8ab911ff226e38fb7f85fb24396547a2d88ddf0dca1caefb6403405120(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97cd974272041719d3d472710040c1d9394294823ea1710987808d69e5fc8d9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696cb236f37562354da0f8d7865462604b057cf8d2e93f348be1665f32c3a389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c22431dbc789fd5969a4dfbe025c6d4febb3259aac2e25572148781506a07e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8292076365b3c5c169e85b986d970c1bbf63f66998c7bdc292dc36ccb500277f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac03c2e9469dd97962a34a318bb5c8395aa6916ec05299bc89e5e53d90cf81d2(
    value: typing.Optional[typing.Union[FsxOntapVolumeTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
