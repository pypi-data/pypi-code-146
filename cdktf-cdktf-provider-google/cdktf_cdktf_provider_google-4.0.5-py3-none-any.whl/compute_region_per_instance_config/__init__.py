'''
# `google_compute_region_per_instance_config`

Refer to the Terraform Registory for docs: [`google_compute_region_per_instance_config`](https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config).
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


class ComputeRegionPerInstanceConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfig",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config google_compute_region_per_instance_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        region_instance_group_manager: builtins.str,
        id: typing.Optional[builtins.str] = None,
        minimal_action: typing.Optional[builtins.str] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        preserved_state: typing.Optional[typing.Union["ComputeRegionPerInstanceConfigPreservedState", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionPerInstanceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config google_compute_region_per_instance_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name for this per-instance config and its corresponding instance. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#name ComputeRegionPerInstanceConfig#name}
        :param region_instance_group_manager: The region instance group manager this instance config is part of. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#region_instance_group_manager ComputeRegionPerInstanceConfig#region_instance_group_manager}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#id ComputeRegionPerInstanceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimal_action: The minimal action to perform on the instance during an update. Default is 'NONE'. Possible values are: REPLACE RESTART REFRESH NONE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#minimal_action ComputeRegionPerInstanceConfig#minimal_action}
        :param most_disruptive_allowed_action: The most disruptive action to perform on the instance during an update. Default is 'REPLACE'. Possible values are: REPLACE RESTART REFRESH NONE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#most_disruptive_allowed_action ComputeRegionPerInstanceConfig#most_disruptive_allowed_action}
        :param preserved_state: preserved_state block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#preserved_state ComputeRegionPerInstanceConfig#preserved_state}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#project ComputeRegionPerInstanceConfig#project}.
        :param region: Region where the containing instance group manager is located. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#region ComputeRegionPerInstanceConfig#region}
        :param remove_instance_state_on_destroy: When true, deleting this config will immediately remove any specified state from the underlying instance. When false, deleting this config will *not* immediately remove any state from the underlying instance. State will be removed on the next instance recreation or update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#remove_instance_state_on_destroy ComputeRegionPerInstanceConfig#remove_instance_state_on_destroy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#timeouts ComputeRegionPerInstanceConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3b4c07428889bc8bdc1f6d7e2a896449f9d80cc100b154cd57ab99f8546a67)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionPerInstanceConfigConfig(
            name=name,
            region_instance_group_manager=region_instance_group_manager,
            id=id,
            minimal_action=minimal_action,
            most_disruptive_allowed_action=most_disruptive_allowed_action,
            preserved_state=preserved_state,
            project=project,
            region=region,
            remove_instance_state_on_destroy=remove_instance_state_on_destroy,
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

    @jsii.member(jsii_name="putPreservedState")
    def put_preserved_state(
        self,
        *,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionPerInstanceConfigPreservedStateDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param disk: disk block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#disk ComputeRegionPerInstanceConfig#disk}
        :param metadata: Preserved metadata defined for this instance. This is a list of key->value pairs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#metadata ComputeRegionPerInstanceConfig#metadata}
        '''
        value = ComputeRegionPerInstanceConfigPreservedState(
            disk=disk, metadata=metadata
        )

        return typing.cast(None, jsii.invoke(self, "putPreservedState", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#create ComputeRegionPerInstanceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#delete ComputeRegionPerInstanceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#update ComputeRegionPerInstanceConfig#update}.
        '''
        value = ComputeRegionPerInstanceConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinimalAction")
    def reset_minimal_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimalAction", []))

    @jsii.member(jsii_name="resetMostDisruptiveAllowedAction")
    def reset_most_disruptive_allowed_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMostDisruptiveAllowedAction", []))

    @jsii.member(jsii_name="resetPreservedState")
    def reset_preserved_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreservedState", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRemoveInstanceStateOnDestroy")
    def reset_remove_instance_state_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoveInstanceStateOnDestroy", []))

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
    @jsii.member(jsii_name="preservedState")
    def preserved_state(
        self,
    ) -> "ComputeRegionPerInstanceConfigPreservedStateOutputReference":
        return typing.cast("ComputeRegionPerInstanceConfigPreservedStateOutputReference", jsii.get(self, "preservedState"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRegionPerInstanceConfigTimeoutsOutputReference":
        return typing.cast("ComputeRegionPerInstanceConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="minimalActionInput")
    def minimal_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimalActionInput"))

    @builtins.property
    @jsii.member(jsii_name="mostDisruptiveAllowedActionInput")
    def most_disruptive_allowed_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mostDisruptiveAllowedActionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="preservedStateInput")
    def preserved_state_input(
        self,
    ) -> typing.Optional["ComputeRegionPerInstanceConfigPreservedState"]:
        return typing.cast(typing.Optional["ComputeRegionPerInstanceConfigPreservedState"], jsii.get(self, "preservedStateInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInstanceGroupManagerInput")
    def region_instance_group_manager_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInstanceGroupManagerInput"))

    @builtins.property
    @jsii.member(jsii_name="removeInstanceStateOnDestroyInput")
    def remove_instance_state_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "removeInstanceStateOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["ComputeRegionPerInstanceConfigTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ComputeRegionPerInstanceConfigTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08cf10da58fd57ee45c96187f5058b73d34b1895a5077e70345ba5402aeb6ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="minimalAction")
    def minimal_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimalAction"))

    @minimal_action.setter
    def minimal_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efb5b1a0acdb9d81e39748900f0ecd7305d712de7024fd4a3d3076dbfdc52231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimalAction", value)

    @builtins.property
    @jsii.member(jsii_name="mostDisruptiveAllowedAction")
    def most_disruptive_allowed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mostDisruptiveAllowedAction"))

    @most_disruptive_allowed_action.setter
    def most_disruptive_allowed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed547a811601086f7bd8bb3e49e80e12df0977d23492347d3daba35f16f4c57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mostDisruptiveAllowedAction", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316037137149f156a1017027a83aae75d90c9d1499999025a55b848d8613dc9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3aeac401bd2343fed7777645fa045f446249ce71a8648c7e7aae4914c5333b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7871ecee2b3d696057d8891209e45e79f640adeeb0e7b26e3fd7193ebdc920cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="regionInstanceGroupManager")
    def region_instance_group_manager(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionInstanceGroupManager"))

    @region_instance_group_manager.setter
    def region_instance_group_manager(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af3dfbc2e843c5ea55fb0b5920b8a0b651bf4b933050cb1066a86cf1cef8c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionInstanceGroupManager", value)

    @builtins.property
    @jsii.member(jsii_name="removeInstanceStateOnDestroy")
    def remove_instance_state_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "removeInstanceStateOnDestroy"))

    @remove_instance_state_on_destroy.setter
    def remove_instance_state_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de203a0bdfd48efd6332900a2db243919e50922bcf70a29085ee08553499f8af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "removeInstanceStateOnDestroy", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigConfig",
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
        "region_instance_group_manager": "regionInstanceGroupManager",
        "id": "id",
        "minimal_action": "minimalAction",
        "most_disruptive_allowed_action": "mostDisruptiveAllowedAction",
        "preserved_state": "preservedState",
        "project": "project",
        "region": "region",
        "remove_instance_state_on_destroy": "removeInstanceStateOnDestroy",
        "timeouts": "timeouts",
    },
)
class ComputeRegionPerInstanceConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        region_instance_group_manager: builtins.str,
        id: typing.Optional[builtins.str] = None,
        minimal_action: typing.Optional[builtins.str] = None,
        most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
        preserved_state: typing.Optional[typing.Union["ComputeRegionPerInstanceConfigPreservedState", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionPerInstanceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name for this per-instance config and its corresponding instance. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#name ComputeRegionPerInstanceConfig#name}
        :param region_instance_group_manager: The region instance group manager this instance config is part of. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#region_instance_group_manager ComputeRegionPerInstanceConfig#region_instance_group_manager}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#id ComputeRegionPerInstanceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimal_action: The minimal action to perform on the instance during an update. Default is 'NONE'. Possible values are: REPLACE RESTART REFRESH NONE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#minimal_action ComputeRegionPerInstanceConfig#minimal_action}
        :param most_disruptive_allowed_action: The most disruptive action to perform on the instance during an update. Default is 'REPLACE'. Possible values are: REPLACE RESTART REFRESH NONE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#most_disruptive_allowed_action ComputeRegionPerInstanceConfig#most_disruptive_allowed_action}
        :param preserved_state: preserved_state block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#preserved_state ComputeRegionPerInstanceConfig#preserved_state}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#project ComputeRegionPerInstanceConfig#project}.
        :param region: Region where the containing instance group manager is located. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#region ComputeRegionPerInstanceConfig#region}
        :param remove_instance_state_on_destroy: When true, deleting this config will immediately remove any specified state from the underlying instance. When false, deleting this config will *not* immediately remove any state from the underlying instance. State will be removed on the next instance recreation or update. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#remove_instance_state_on_destroy ComputeRegionPerInstanceConfig#remove_instance_state_on_destroy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#timeouts ComputeRegionPerInstanceConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(preserved_state, dict):
            preserved_state = ComputeRegionPerInstanceConfigPreservedState(**preserved_state)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionPerInstanceConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b53754ff16f749d2f6de541ea9476c9ccfbcf2722d58ea149e0512ba6ad3719c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region_instance_group_manager", value=region_instance_group_manager, expected_type=type_hints["region_instance_group_manager"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument minimal_action", value=minimal_action, expected_type=type_hints["minimal_action"])
            check_type(argname="argument most_disruptive_allowed_action", value=most_disruptive_allowed_action, expected_type=type_hints["most_disruptive_allowed_action"])
            check_type(argname="argument preserved_state", value=preserved_state, expected_type=type_hints["preserved_state"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument remove_instance_state_on_destroy", value=remove_instance_state_on_destroy, expected_type=type_hints["remove_instance_state_on_destroy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "region_instance_group_manager": region_instance_group_manager,
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
        if minimal_action is not None:
            self._values["minimal_action"] = minimal_action
        if most_disruptive_allowed_action is not None:
            self._values["most_disruptive_allowed_action"] = most_disruptive_allowed_action
        if preserved_state is not None:
            self._values["preserved_state"] = preserved_state
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if remove_instance_state_on_destroy is not None:
            self._values["remove_instance_state_on_destroy"] = remove_instance_state_on_destroy
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
        '''The name for this per-instance config and its corresponding instance.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#name ComputeRegionPerInstanceConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region_instance_group_manager(self) -> builtins.str:
        '''The region instance group manager this instance config is part of.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#region_instance_group_manager ComputeRegionPerInstanceConfig#region_instance_group_manager}
        '''
        result = self._values.get("region_instance_group_manager")
        assert result is not None, "Required property 'region_instance_group_manager' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#id ComputeRegionPerInstanceConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimal_action(self) -> typing.Optional[builtins.str]:
        '''The minimal action to perform on the instance during an update. Default is 'NONE'. Possible values are: REPLACE RESTART REFRESH NONE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#minimal_action ComputeRegionPerInstanceConfig#minimal_action}
        '''
        result = self._values.get("minimal_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def most_disruptive_allowed_action(self) -> typing.Optional[builtins.str]:
        '''The most disruptive action to perform on the instance during an update. Default is 'REPLACE'. Possible values are: REPLACE RESTART REFRESH NONE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#most_disruptive_allowed_action ComputeRegionPerInstanceConfig#most_disruptive_allowed_action}
        '''
        result = self._values.get("most_disruptive_allowed_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserved_state(
        self,
    ) -> typing.Optional["ComputeRegionPerInstanceConfigPreservedState"]:
        '''preserved_state block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#preserved_state ComputeRegionPerInstanceConfig#preserved_state}
        '''
        result = self._values.get("preserved_state")
        return typing.cast(typing.Optional["ComputeRegionPerInstanceConfigPreservedState"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#project ComputeRegionPerInstanceConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where the containing instance group manager is located.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#region ComputeRegionPerInstanceConfig#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove_instance_state_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, deleting this config will immediately remove any specified state from the underlying instance.

        When false, deleting this config will *not* immediately remove any state from the underlying instance.
        State will be removed on the next instance recreation or update.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#remove_instance_state_on_destroy ComputeRegionPerInstanceConfig#remove_instance_state_on_destroy}
        '''
        result = self._values.get("remove_instance_state_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRegionPerInstanceConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#timeouts ComputeRegionPerInstanceConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionPerInstanceConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedState",
    jsii_struct_bases=[],
    name_mapping={"disk": "disk", "metadata": "metadata"},
)
class ComputeRegionPerInstanceConfigPreservedState:
    def __init__(
        self,
        *,
        disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionPerInstanceConfigPreservedStateDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param disk: disk block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#disk ComputeRegionPerInstanceConfig#disk}
        :param metadata: Preserved metadata defined for this instance. This is a list of key->value pairs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#metadata ComputeRegionPerInstanceConfig#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9bb7d8802853c6db61881d42f7db9768fe1b56c02ba10b6d558b956716cf1d6)
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk is not None:
            self._values["disk"] = disk
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionPerInstanceConfigPreservedStateDisk"]]]:
        '''disk block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#disk ComputeRegionPerInstanceConfig#disk}
        '''
        result = self._values.get("disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionPerInstanceConfigPreservedStateDisk"]]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Preserved metadata defined for this instance. This is a list of key->value pairs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#metadata ComputeRegionPerInstanceConfig#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigPreservedState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateDisk",
    jsii_struct_bases=[],
    name_mapping={
        "device_name": "deviceName",
        "source": "source",
        "delete_rule": "deleteRule",
        "mode": "mode",
    },
)
class ComputeRegionPerInstanceConfigPreservedStateDisk:
    def __init__(
        self,
        *,
        device_name: builtins.str,
        source: builtins.str,
        delete_rule: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param device_name: A unique device name that is reflected into the /dev/ tree of a Linux operating system running within the instance. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#device_name ComputeRegionPerInstanceConfig#device_name}
        :param source: The URI of an existing persistent disk to attach under the specified device-name in the format 'projects/project-id/zones/zone/disks/disk-name'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#source ComputeRegionPerInstanceConfig#source}
        :param delete_rule: A value that prescribes what should happen to the stateful disk when the VM instance is deleted. The available options are 'NEVER' and 'ON_PERMANENT_INSTANCE_DELETION'. 'NEVER' - detach the disk when the VM is deleted, but do not delete the disk. 'ON_PERMANENT_INSTANCE_DELETION' will delete the stateful disk when the VM is permanently deleted from the instance group. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#delete_rule ComputeRegionPerInstanceConfig#delete_rule}
        :param mode: The mode of the disk. Default value: "READ_WRITE" Possible values: ["READ_ONLY", "READ_WRITE"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#mode ComputeRegionPerInstanceConfig#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ad95f010b05961a7a4ac5434319ea7626e4b00e8be99b762bf41695dea5fd9)
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument delete_rule", value=delete_rule, expected_type=type_hints["delete_rule"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "device_name": device_name,
            "source": source,
        }
        if delete_rule is not None:
            self._values["delete_rule"] = delete_rule
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def device_name(self) -> builtins.str:
        '''A unique device name that is reflected into the /dev/ tree of a Linux operating system running within the instance.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#device_name ComputeRegionPerInstanceConfig#device_name}
        '''
        result = self._values.get("device_name")
        assert result is not None, "Required property 'device_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''The URI of an existing persistent disk to attach under the specified device-name in the format 'projects/project-id/zones/zone/disks/disk-name'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#source ComputeRegionPerInstanceConfig#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_rule(self) -> typing.Optional[builtins.str]:
        '''A value that prescribes what should happen to the stateful disk when the VM instance is deleted.

        The available options are 'NEVER' and 'ON_PERMANENT_INSTANCE_DELETION'.
        'NEVER' - detach the disk when the VM is deleted, but do not delete the disk.
        'ON_PERMANENT_INSTANCE_DELETION' will delete the stateful disk when the VM is permanently
        deleted from the instance group. Default value: "NEVER" Possible values: ["NEVER", "ON_PERMANENT_INSTANCE_DELETION"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#delete_rule ComputeRegionPerInstanceConfig#delete_rule}
        '''
        result = self._values.get("delete_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode of the disk. Default value: "READ_WRITE" Possible values: ["READ_ONLY", "READ_WRITE"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#mode ComputeRegionPerInstanceConfig#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigPreservedStateDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionPerInstanceConfigPreservedStateDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67130bdfe09826a986c27c9364bcca7d17823991e3c2ef60e6e44953cd4ff8fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionPerInstanceConfigPreservedStateDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fdb93cb9da5a4e0dd76d3251fe24b2ecf494552882751a324bb3129adb7918)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionPerInstanceConfigPreservedStateDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97ef6b44bd74550678bf8d22740fe8bcca48ff69558a8551f230eea89bf4169)
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
            type_hints = typing.get_type_hints(_typecheckingstub__def7b4427ec6e1ae8d2cbe7639ca6956ba2671839810bd2c0b3cf6e8a4bfb470)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7a37d440e74a78b0781b2ff7095bb3cd8aa0e129eac039265376a20a09b8776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4cc0d6652da29d3e382769068f2b56634f409ed80417369f27c6c985ad4a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ComputeRegionPerInstanceConfigPreservedStateDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c94597de2c936f6d10de02269a6f04f4dc9a7698fb70fc19eff6b65eb968f19c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDeleteRule")
    def reset_delete_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteRule", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="deleteRuleInput")
    def delete_rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteRule")
    def delete_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteRule"))

    @delete_rule.setter
    def delete_rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__febf33509f861a068d3219f56c9701aa6d869d413bed627e74e4c5a75895f772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteRule", value)

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916ee8557a44372fbcccf84a8b28ff31f80f813c9b903906c45d53b19a087d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642d0ca8effb9feb7bee78c484b4194577dd68be44cbc1900c044effba5a906f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6367248e161cb3684d3a48c243b75df8c79e5b03339957c04d8c5cd794355433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ComputeRegionPerInstanceConfigPreservedStateDisk, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ComputeRegionPerInstanceConfigPreservedStateDisk, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigPreservedStateDisk, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4561caa7f99cf896d8fbab2529be04ae3b5584ad3af06bd4b5bb9e0235aa04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ComputeRegionPerInstanceConfigPreservedStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigPreservedStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4bfdb9d761f510c9dc62185e9b0bdd0bb89f6a6abcfaadcceedf96f5ee5177e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDisk")
    def put_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateDisk, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc840fc1d58916d21722a290cafa470777ea76b3d7674b8a995b2d3f70e226e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDisk", [value]))

    @jsii.member(jsii_name="resetDisk")
    def reset_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisk", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> ComputeRegionPerInstanceConfigPreservedStateDiskList:
        return typing.cast(ComputeRegionPerInstanceConfigPreservedStateDiskList, jsii.get(self, "disk"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eeaa819a0f0ebe97236fe136ff5099756823e39632856a606eee8454c3366c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionPerInstanceConfigPreservedState]:
        return typing.cast(typing.Optional[ComputeRegionPerInstanceConfigPreservedState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionPerInstanceConfigPreservedState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de8fabc81cd776ea4b62373b6bb57df1afdc5d4bc3c21c004a5da36467ec67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRegionPerInstanceConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#create ComputeRegionPerInstanceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#delete ComputeRegionPerInstanceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#update ComputeRegionPerInstanceConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9b271f582cb8d88eefef254f79d10d0f640d0fc341658e619bab3fc772243a)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#create ComputeRegionPerInstanceConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#delete ComputeRegionPerInstanceConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_region_per_instance_config#update ComputeRegionPerInstanceConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionPerInstanceConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionPerInstanceConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionPerInstanceConfig.ComputeRegionPerInstanceConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d12dac853d1b12481326a9683c84ce28abe9db3fbf874d7ae590689ce14013c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7b2fada7bb64f1a753db4abcf02175ea2026382afde6b06da04afcbffd48ecd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7d79e264cd89005af6d1241c086792359647034186631569775a0988f23a1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1cc960b7166cef3a8801a4866b92ce359450e42d99434a99f156a16c3d3cb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ComputeRegionPerInstanceConfigTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ComputeRegionPerInstanceConfigTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5029b7bfcc76fe16d86990a4a4293064710b86a0e62b97777cececf03de9a7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ComputeRegionPerInstanceConfig",
    "ComputeRegionPerInstanceConfigConfig",
    "ComputeRegionPerInstanceConfigPreservedState",
    "ComputeRegionPerInstanceConfigPreservedStateDisk",
    "ComputeRegionPerInstanceConfigPreservedStateDiskList",
    "ComputeRegionPerInstanceConfigPreservedStateDiskOutputReference",
    "ComputeRegionPerInstanceConfigPreservedStateOutputReference",
    "ComputeRegionPerInstanceConfigTimeouts",
    "ComputeRegionPerInstanceConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4d3b4c07428889bc8bdc1f6d7e2a896449f9d80cc100b154cd57ab99f8546a67(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    region_instance_group_manager: builtins.str,
    id: typing.Optional[builtins.str] = None,
    minimal_action: typing.Optional[builtins.str] = None,
    most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
    preserved_state: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigPreservedState, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d08cf10da58fd57ee45c96187f5058b73d34b1895a5077e70345ba5402aeb6ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb5b1a0acdb9d81e39748900f0ecd7305d712de7024fd4a3d3076dbfdc52231(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed547a811601086f7bd8bb3e49e80e12df0977d23492347d3daba35f16f4c57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316037137149f156a1017027a83aae75d90c9d1499999025a55b848d8613dc9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3aeac401bd2343fed7777645fa045f446249ce71a8648c7e7aae4914c5333b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7871ecee2b3d696057d8891209e45e79f640adeeb0e7b26e3fd7193ebdc920cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af3dfbc2e843c5ea55fb0b5920b8a0b651bf4b933050cb1066a86cf1cef8c83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de203a0bdfd48efd6332900a2db243919e50922bcf70a29085ee08553499f8af(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53754ff16f749d2f6de541ea9476c9ccfbcf2722d58ea149e0512ba6ad3719c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    region_instance_group_manager: builtins.str,
    id: typing.Optional[builtins.str] = None,
    minimal_action: typing.Optional[builtins.str] = None,
    most_disruptive_allowed_action: typing.Optional[builtins.str] = None,
    preserved_state: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigPreservedState, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    remove_instance_state_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bb7d8802853c6db61881d42f7db9768fe1b56c02ba10b6d558b956716cf1d6(
    *,
    disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ad95f010b05961a7a4ac5434319ea7626e4b00e8be99b762bf41695dea5fd9(
    *,
    device_name: builtins.str,
    source: builtins.str,
    delete_rule: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67130bdfe09826a986c27c9364bcca7d17823991e3c2ef60e6e44953cd4ff8fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fdb93cb9da5a4e0dd76d3251fe24b2ecf494552882751a324bb3129adb7918(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97ef6b44bd74550678bf8d22740fe8bcca48ff69558a8551f230eea89bf4169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def7b4427ec6e1ae8d2cbe7639ca6956ba2671839810bd2c0b3cf6e8a4bfb470(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a37d440e74a78b0781b2ff7095bb3cd8aa0e129eac039265376a20a09b8776(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4cc0d6652da29d3e382769068f2b56634f409ed80417369f27c6c985ad4a91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionPerInstanceConfigPreservedStateDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94597de2c936f6d10de02269a6f04f4dc9a7698fb70fc19eff6b65eb968f19c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febf33509f861a068d3219f56c9701aa6d869d413bed627e74e4c5a75895f772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916ee8557a44372fbcccf84a8b28ff31f80f813c9b903906c45d53b19a087d7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642d0ca8effb9feb7bee78c484b4194577dd68be44cbc1900c044effba5a906f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6367248e161cb3684d3a48c243b75df8c79e5b03339957c04d8c5cd794355433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4561caa7f99cf896d8fbab2529be04ae3b5584ad3af06bd4b5bb9e0235aa04(
    value: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigPreservedStateDisk, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bfdb9d761f510c9dc62185e9b0bdd0bb89f6a6abcfaadcceedf96f5ee5177e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc840fc1d58916d21722a290cafa470777ea76b3d7674b8a995b2d3f70e226e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionPerInstanceConfigPreservedStateDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eeaa819a0f0ebe97236fe136ff5099756823e39632856a606eee8454c3366c5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de8fabc81cd776ea4b62373b6bb57df1afdc5d4bc3c21c004a5da36467ec67b(
    value: typing.Optional[ComputeRegionPerInstanceConfigPreservedState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9b271f582cb8d88eefef254f79d10d0f640d0fc341658e619bab3fc772243a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d12dac853d1b12481326a9683c84ce28abe9db3fbf874d7ae590689ce14013c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b2fada7bb64f1a753db4abcf02175ea2026382afde6b06da04afcbffd48ecd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7d79e264cd89005af6d1241c086792359647034186631569775a0988f23a1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1cc960b7166cef3a8801a4866b92ce359450e42d99434a99f156a16c3d3cb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5029b7bfcc76fe16d86990a4a4293064710b86a0e62b97777cececf03de9a7f7(
    value: typing.Optional[typing.Union[ComputeRegionPerInstanceConfigTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
