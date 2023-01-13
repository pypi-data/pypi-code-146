'''
# `spotinst_ocean_aks_virtual_node_group`

Refer to the Terraform Registory for docs: [`spotinst_ocean_aks_virtual_node_group`](https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group).
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


class OceanAksVirtualNodeGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroup",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group spotinst_ocean_aks_virtual_node_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        ocean_id: builtins.str,
        autoscale: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupAutoscale", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        label: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupLabel", typing.Dict[builtins.str, typing.Any]]]]] = None,
        launch_specification: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupLaunchSpecification", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_limits: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupResourceLimits", typing.Dict[builtins.str, typing.Any]]]]] = None,
        taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupTaint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group spotinst_ocean_aks_virtual_node_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#name OceanAksVirtualNodeGroup#name}.
        :param ocean_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#ocean_id OceanAksVirtualNodeGroup#ocean_id}.
        :param autoscale: autoscale block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#autoscale OceanAksVirtualNodeGroup#autoscale}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#id OceanAksVirtualNodeGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param label: label block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#label OceanAksVirtualNodeGroup#label}
        :param launch_specification: launch_specification block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#launch_specification OceanAksVirtualNodeGroup#launch_specification}
        :param resource_limits: resource_limits block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#resource_limits OceanAksVirtualNodeGroup#resource_limits}
        :param taint: taint block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#taint OceanAksVirtualNodeGroup#taint}
        :param zones: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#zones OceanAksVirtualNodeGroup#zones}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__678dcb933d2f9320b35530486a942b429232d45972984bb342bf1dbbaf281add)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OceanAksVirtualNodeGroupConfig(
            name=name,
            ocean_id=ocean_id,
            autoscale=autoscale,
            id=id,
            label=label,
            launch_specification=launch_specification,
            resource_limits=resource_limits,
            taint=taint,
            zones=zones,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAutoscale")
    def put_autoscale(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupAutoscale", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab3e62ce91acb0181c8598c82ab26202938448a191a3d0e1373e1acf063956f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAutoscale", [value]))

    @jsii.member(jsii_name="putLabel")
    def put_label(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupLabel", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dbffda12ff03921a2a1edb65e7c8ca51122f7269f99577bd673ba813b110b86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLabel", [value]))

    @jsii.member(jsii_name="putLaunchSpecification")
    def put_launch_specification(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupLaunchSpecification", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816b31ce5291772b1cb1acf754e50aa93265abf17cad1f2934524d5937732426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLaunchSpecification", [value]))

    @jsii.member(jsii_name="putResourceLimits")
    def put_resource_limits(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupResourceLimits", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a030c04f4b80cc7eb34b1bac8830824eccf036ce42161daeb8c2f3923295f9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceLimits", [value]))

    @jsii.member(jsii_name="putTaint")
    def put_taint(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupTaint", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__927a28e9a289f970287f5dba7c4c9fa91682579e7a9f8b4bb81827c01049131d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaint", [value]))

    @jsii.member(jsii_name="resetAutoscale")
    def reset_autoscale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscale", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @jsii.member(jsii_name="resetLaunchSpecification")
    def reset_launch_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchSpecification", []))

    @jsii.member(jsii_name="resetResourceLimits")
    def reset_resource_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceLimits", []))

    @jsii.member(jsii_name="resetTaint")
    def reset_taint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaint", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="autoscale")
    def autoscale(self) -> "OceanAksVirtualNodeGroupAutoscaleList":
        return typing.cast("OceanAksVirtualNodeGroupAutoscaleList", jsii.get(self, "autoscale"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> "OceanAksVirtualNodeGroupLabelList":
        return typing.cast("OceanAksVirtualNodeGroupLabelList", jsii.get(self, "label"))

    @builtins.property
    @jsii.member(jsii_name="launchSpecification")
    def launch_specification(self) -> "OceanAksVirtualNodeGroupLaunchSpecificationList":
        return typing.cast("OceanAksVirtualNodeGroupLaunchSpecificationList", jsii.get(self, "launchSpecification"))

    @builtins.property
    @jsii.member(jsii_name="resourceLimits")
    def resource_limits(self) -> "OceanAksVirtualNodeGroupResourceLimitsList":
        return typing.cast("OceanAksVirtualNodeGroupResourceLimitsList", jsii.get(self, "resourceLimits"))

    @builtins.property
    @jsii.member(jsii_name="taint")
    def taint(self) -> "OceanAksVirtualNodeGroupTaintList":
        return typing.cast("OceanAksVirtualNodeGroupTaintList", jsii.get(self, "taint"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleInput")
    def autoscale_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupAutoscale"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupAutoscale"]]], jsii.get(self, "autoscaleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLabel"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLabel"]]], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="launchSpecificationInput")
    def launch_specification_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLaunchSpecification"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLaunchSpecification"]]], jsii.get(self, "launchSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="oceanIdInput")
    def ocean_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oceanIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceLimitsInput")
    def resource_limits_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupResourceLimits"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupResourceLimits"]]], jsii.get(self, "resourceLimitsInput"))

    @builtins.property
    @jsii.member(jsii_name="taintInput")
    def taint_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupTaint"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupTaint"]]], jsii.get(self, "taintInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b9335b736ce17373e5b034e52168074241d4771a887f4f6ea7731a67c1d44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1cbc0fbd2b79c2c3880d074455899473bfb80e7d252f86aaf4fd4e4f5151b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="oceanId")
    def ocean_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oceanId"))

    @ocean_id.setter
    def ocean_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c3b936c86559cd4176acb7153c678a5eda4f709f107ad944aba0551cb6b210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oceanId", value)

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8e31ca0b429a458e9c9ae5a3e54b8503ed9bdd74bd5513c159dd50d69fdc63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupAutoscale",
    jsii_struct_bases=[],
    name_mapping={
        "auto_headroom_percentage": "autoHeadroomPercentage",
        "autoscale_headroom": "autoscaleHeadroom",
    },
)
class OceanAksVirtualNodeGroupAutoscale:
    def __init__(
        self,
        *,
        auto_headroom_percentage: typing.Optional[jsii.Number] = None,
        autoscale_headroom: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param auto_headroom_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#auto_headroom_percentage OceanAksVirtualNodeGroup#auto_headroom_percentage}.
        :param autoscale_headroom: autoscale_headroom block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#autoscale_headroom OceanAksVirtualNodeGroup#autoscale_headroom}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82bcbd44ed69e4bb71e87541f056000212152765a869cf0b34a43e1c84cb3413)
            check_type(argname="argument auto_headroom_percentage", value=auto_headroom_percentage, expected_type=type_hints["auto_headroom_percentage"])
            check_type(argname="argument autoscale_headroom", value=autoscale_headroom, expected_type=type_hints["autoscale_headroom"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_headroom_percentage is not None:
            self._values["auto_headroom_percentage"] = auto_headroom_percentage
        if autoscale_headroom is not None:
            self._values["autoscale_headroom"] = autoscale_headroom

    @builtins.property
    def auto_headroom_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#auto_headroom_percentage OceanAksVirtualNodeGroup#auto_headroom_percentage}.'''
        result = self._values.get("auto_headroom_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def autoscale_headroom(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom"]]]:
        '''autoscale_headroom block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#autoscale_headroom OceanAksVirtualNodeGroup#autoscale_headroom}
        '''
        result = self._values.get("autoscale_headroom")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksVirtualNodeGroupAutoscale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom",
    jsii_struct_bases=[],
    name_mapping={
        "num_of_units": "numOfUnits",
        "cpu_per_unit": "cpuPerUnit",
        "gpu_per_unit": "gpuPerUnit",
        "memory_per_unit": "memoryPerUnit",
    },
)
class OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom:
    def __init__(
        self,
        *,
        num_of_units: jsii.Number,
        cpu_per_unit: typing.Optional[jsii.Number] = None,
        gpu_per_unit: typing.Optional[jsii.Number] = None,
        memory_per_unit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param num_of_units: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#num_of_units OceanAksVirtualNodeGroup#num_of_units}.
        :param cpu_per_unit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#cpu_per_unit OceanAksVirtualNodeGroup#cpu_per_unit}.
        :param gpu_per_unit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#gpu_per_unit OceanAksVirtualNodeGroup#gpu_per_unit}.
        :param memory_per_unit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#memory_per_unit OceanAksVirtualNodeGroup#memory_per_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4276c79fcaad5c4a61bf3eb86e86f13ac213fe946ab2e7a30228b43fc1b79262)
            check_type(argname="argument num_of_units", value=num_of_units, expected_type=type_hints["num_of_units"])
            check_type(argname="argument cpu_per_unit", value=cpu_per_unit, expected_type=type_hints["cpu_per_unit"])
            check_type(argname="argument gpu_per_unit", value=gpu_per_unit, expected_type=type_hints["gpu_per_unit"])
            check_type(argname="argument memory_per_unit", value=memory_per_unit, expected_type=type_hints["memory_per_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "num_of_units": num_of_units,
        }
        if cpu_per_unit is not None:
            self._values["cpu_per_unit"] = cpu_per_unit
        if gpu_per_unit is not None:
            self._values["gpu_per_unit"] = gpu_per_unit
        if memory_per_unit is not None:
            self._values["memory_per_unit"] = memory_per_unit

    @builtins.property
    def num_of_units(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#num_of_units OceanAksVirtualNodeGroup#num_of_units}.'''
        result = self._values.get("num_of_units")
        assert result is not None, "Required property 'num_of_units' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cpu_per_unit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#cpu_per_unit OceanAksVirtualNodeGroup#cpu_per_unit}.'''
        result = self._values.get("cpu_per_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gpu_per_unit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#gpu_per_unit OceanAksVirtualNodeGroup#gpu_per_unit}.'''
        result = self._values.get("gpu_per_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_per_unit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#memory_per_unit OceanAksVirtualNodeGroup#memory_per_unit}.'''
        result = self._values.get("memory_per_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroomList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroomList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__239d226d2c55913edb8ec3a7cade81abbcfbe535884dc5638a87bcd28df9357c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroomOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2733a57f2069ea00f99e8b08cdc247bfaf91f5683e3047aadecfc690f910c187)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroomOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6899f3304a68f79781b575fa2980b0b38226d026767eaf35412dc83cbc26ebdb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc31eaf59edd16f2f58cb363aaa48baa1ee472a890d37bc35a9895bbcbdfa94d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e731c36047e5003004ffa85700fa77ec7ecc305f2aaa3b5065e26e857d49e683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdfc48eb6ef2dd006a2cae53eda857d94c5624f7129b184a5360f9a135008258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroomOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f99db8aa0940007e3ef605ea31ef8821ac4b4b7a17678dd224908ce44f0d35e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCpuPerUnit")
    def reset_cpu_per_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuPerUnit", []))

    @jsii.member(jsii_name="resetGpuPerUnit")
    def reset_gpu_per_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpuPerUnit", []))

    @jsii.member(jsii_name="resetMemoryPerUnit")
    def reset_memory_per_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryPerUnit", []))

    @builtins.property
    @jsii.member(jsii_name="cpuPerUnitInput")
    def cpu_per_unit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuPerUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuPerUnitInput")
    def gpu_per_unit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gpuPerUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryPerUnitInput")
    def memory_per_unit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryPerUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="numOfUnitsInput")
    def num_of_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numOfUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuPerUnit")
    def cpu_per_unit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuPerUnit"))

    @cpu_per_unit.setter
    def cpu_per_unit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7e955255e239a3a3f6e8e7cc7dfea5fa5ef3cad865a036d18054dee703519a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuPerUnit", value)

    @builtins.property
    @jsii.member(jsii_name="gpuPerUnit")
    def gpu_per_unit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gpuPerUnit"))

    @gpu_per_unit.setter
    def gpu_per_unit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288ede7280d999e53dabbee751d14d4a052e02929f214eb3c637ac15cb43d742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuPerUnit", value)

    @builtins.property
    @jsii.member(jsii_name="memoryPerUnit")
    def memory_per_unit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryPerUnit"))

    @memory_per_unit.setter
    def memory_per_unit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bc19ef8d247c0b9a0b7c528557a5041578696b49ee5382f4112625436c2db34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryPerUnit", value)

    @builtins.property
    @jsii.member(jsii_name="numOfUnits")
    def num_of_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numOfUnits"))

    @num_of_units.setter
    def num_of_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8733639d838fccdd6f10e15455f49345d8f296aa015ec8ed4ac9aef78c2fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numOfUnits", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450a43f68d7f0cf743eed605bc53625f307678130a1f773a51e33a55cc2cb14b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksVirtualNodeGroupAutoscaleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupAutoscaleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aac60ba12eb0d381610f63554cb3ccc45d37987e0373f543e7fa55b5adb1927)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OceanAksVirtualNodeGroupAutoscaleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c258580e7e176b66228d78e5113aa3f7f50e6ba5d09b955d6078fbffc3d8ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksVirtualNodeGroupAutoscaleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754b4a2c1b9500c7f4ab430750ce4e7a096b8c72743af906675769f0a4a2c14f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f72a2b4ec93f9785b92c3639140b2509892f248cb95d4c98ba03f025446ed66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__862ebee95a69cf344d0d11ea9e91ae931a535011ad02c4c80ebea5a9e2635bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscale]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscale]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscale]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d3dd749bab571524673f176bf93db88e1867293b7db9b05801ded055df07c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksVirtualNodeGroupAutoscaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupAutoscaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da57c8f30c21d0e35b3d88ff312ea828b42ff5d6560886e81cdfa91f092951fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAutoscaleHeadroom")
    def put_autoscale_headroom(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab376916d595041b38e410de0a56cd686e698101fc09c1629af123f009ba31d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAutoscaleHeadroom", [value]))

    @jsii.member(jsii_name="resetAutoHeadroomPercentage")
    def reset_auto_headroom_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoHeadroomPercentage", []))

    @jsii.member(jsii_name="resetAutoscaleHeadroom")
    def reset_autoscale_headroom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaleHeadroom", []))

    @builtins.property
    @jsii.member(jsii_name="autoscaleHeadroom")
    def autoscale_headroom(
        self,
    ) -> OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroomList:
        return typing.cast(OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroomList, jsii.get(self, "autoscaleHeadroom"))

    @builtins.property
    @jsii.member(jsii_name="autoHeadroomPercentageInput")
    def auto_headroom_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoHeadroomPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleHeadroomInput")
    def autoscale_headroom_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom]]], jsii.get(self, "autoscaleHeadroomInput"))

    @builtins.property
    @jsii.member(jsii_name="autoHeadroomPercentage")
    def auto_headroom_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoHeadroomPercentage"))

    @auto_headroom_percentage.setter
    def auto_headroom_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb6dd47e7abd3fd054a6f2e54229284422c25f121afed210c15b2e6cbd6e3c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoHeadroomPercentage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksVirtualNodeGroupAutoscale, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksVirtualNodeGroupAutoscale, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupAutoscale, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae621e5913786098c31f360e75de73d932312d5e3fe6a6983a3f6d99b228d04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupConfig",
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
        "ocean_id": "oceanId",
        "autoscale": "autoscale",
        "id": "id",
        "label": "label",
        "launch_specification": "launchSpecification",
        "resource_limits": "resourceLimits",
        "taint": "taint",
        "zones": "zones",
    },
)
class OceanAksVirtualNodeGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        ocean_id: builtins.str,
        autoscale: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupAutoscale, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        label: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupLabel", typing.Dict[builtins.str, typing.Any]]]]] = None,
        launch_specification: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupLaunchSpecification", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_limits: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupResourceLimits", typing.Dict[builtins.str, typing.Any]]]]] = None,
        taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupTaint", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#name OceanAksVirtualNodeGroup#name}.
        :param ocean_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#ocean_id OceanAksVirtualNodeGroup#ocean_id}.
        :param autoscale: autoscale block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#autoscale OceanAksVirtualNodeGroup#autoscale}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#id OceanAksVirtualNodeGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param label: label block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#label OceanAksVirtualNodeGroup#label}
        :param launch_specification: launch_specification block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#launch_specification OceanAksVirtualNodeGroup#launch_specification}
        :param resource_limits: resource_limits block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#resource_limits OceanAksVirtualNodeGroup#resource_limits}
        :param taint: taint block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#taint OceanAksVirtualNodeGroup#taint}
        :param zones: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#zones OceanAksVirtualNodeGroup#zones}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb30657daae1809c581ba647acc74c874d226e6578afba3dd72044758a201d3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ocean_id", value=ocean_id, expected_type=type_hints["ocean_id"])
            check_type(argname="argument autoscale", value=autoscale, expected_type=type_hints["autoscale"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument launch_specification", value=launch_specification, expected_type=type_hints["launch_specification"])
            check_type(argname="argument resource_limits", value=resource_limits, expected_type=type_hints["resource_limits"])
            check_type(argname="argument taint", value=taint, expected_type=type_hints["taint"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "ocean_id": ocean_id,
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
        if autoscale is not None:
            self._values["autoscale"] = autoscale
        if id is not None:
            self._values["id"] = id
        if label is not None:
            self._values["label"] = label
        if launch_specification is not None:
            self._values["launch_specification"] = launch_specification
        if resource_limits is not None:
            self._values["resource_limits"] = resource_limits
        if taint is not None:
            self._values["taint"] = taint
        if zones is not None:
            self._values["zones"] = zones

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#name OceanAksVirtualNodeGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ocean_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#ocean_id OceanAksVirtualNodeGroup#ocean_id}.'''
        result = self._values.get("ocean_id")
        assert result is not None, "Required property 'ocean_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscale(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscale]]]:
        '''autoscale block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#autoscale OceanAksVirtualNodeGroup#autoscale}
        '''
        result = self._values.get("autoscale")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscale]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#id OceanAksVirtualNodeGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLabel"]]]:
        '''label block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#label OceanAksVirtualNodeGroup#label}
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLabel"]]], result)

    @builtins.property
    def launch_specification(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLaunchSpecification"]]]:
        '''launch_specification block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#launch_specification OceanAksVirtualNodeGroup#launch_specification}
        '''
        result = self._values.get("launch_specification")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLaunchSpecification"]]], result)

    @builtins.property
    def resource_limits(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupResourceLimits"]]]:
        '''resource_limits block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#resource_limits OceanAksVirtualNodeGroup#resource_limits}
        '''
        result = self._values.get("resource_limits")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupResourceLimits"]]], result)

    @builtins.property
    def taint(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupTaint"]]]:
        '''taint block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#taint OceanAksVirtualNodeGroup#taint}
        '''
        result = self._values.get("taint")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupTaint"]]], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#zones OceanAksVirtualNodeGroup#zones}.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksVirtualNodeGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupLabel",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class OceanAksVirtualNodeGroupLabel:
    def __init__(
        self,
        *,
        key: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#key OceanAksVirtualNodeGroup#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#value OceanAksVirtualNodeGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7221e1e657456ffa7d68502f02f195b3657d1bd641bcb61b5c8fad91ff68816e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#key OceanAksVirtualNodeGroup#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#value OceanAksVirtualNodeGroup#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksVirtualNodeGroupLabel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksVirtualNodeGroupLabelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupLabelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77f677f49e5db73b84a58af654e018dca4ccca33035683f1113d7dd8c7d9acbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OceanAksVirtualNodeGroupLabelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2a91d72f4c6235183a8ff8b4e22318e4cc8502602e99cc015c633cdfaa848a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksVirtualNodeGroupLabelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7910cc69252c546409b0e9e9c4009adde06008dedd0316d95e222e749e3eea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5d22b453ec21312960aa6cd04c2a6f0a9b00d00312934dc4e2bf36ab5fdd3ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c802792965df267351bb07a9e9eec4f82a765c0afad8738d53c33e26ce6a035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLabel]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLabel]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLabel]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061f2d1684cfdcd4d96a7d8e50c4788659f2d24e363c063361224d321b51d432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksVirtualNodeGroupLabelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupLabelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e678a0b88bccde0cdf747dc3656925c6fae4ac1d67dd90fd42d853cdc0b7615c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2ed3d35737b3915e9c0d5a5e4d635c5cb8bcb627c6d67dc632f0297ece9d8057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92ec4d0d975aa3917b05b32355cc13d0e5caec2ff321f41be2158ea110c78ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksVirtualNodeGroupLabel, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksVirtualNodeGroupLabel, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupLabel, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbb542782f37f9c45d025bf266e37c48e39d9478215c592c00a3a1ba09ab4a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupLaunchSpecification",
    jsii_struct_bases=[],
    name_mapping={"max_pods": "maxPods", "os_disk": "osDisk", "tag": "tag"},
)
class OceanAksVirtualNodeGroupLaunchSpecification:
    def __init__(
        self,
        *,
        max_pods: typing.Optional[jsii.Number] = None,
        os_disk: typing.Optional[typing.Union["OceanAksVirtualNodeGroupLaunchSpecificationOsDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupLaunchSpecificationTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param max_pods: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#max_pods OceanAksVirtualNodeGroup#max_pods}.
        :param os_disk: os_disk block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#os_disk OceanAksVirtualNodeGroup#os_disk}
        :param tag: tag block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#tag OceanAksVirtualNodeGroup#tag}
        '''
        if isinstance(os_disk, dict):
            os_disk = OceanAksVirtualNodeGroupLaunchSpecificationOsDisk(**os_disk)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126d63f238f15fb2a97cd2ec18dfb53be91e3f4d97d2ead67262cfb4e92ffb1f)
            check_type(argname="argument max_pods", value=max_pods, expected_type=type_hints["max_pods"])
            check_type(argname="argument os_disk", value=os_disk, expected_type=type_hints["os_disk"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_pods is not None:
            self._values["max_pods"] = max_pods
        if os_disk is not None:
            self._values["os_disk"] = os_disk
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def max_pods(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#max_pods OceanAksVirtualNodeGroup#max_pods}.'''
        result = self._values.get("max_pods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def os_disk(
        self,
    ) -> typing.Optional["OceanAksVirtualNodeGroupLaunchSpecificationOsDisk"]:
        '''os_disk block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#os_disk OceanAksVirtualNodeGroup#os_disk}
        '''
        result = self._values.get("os_disk")
        return typing.cast(typing.Optional["OceanAksVirtualNodeGroupLaunchSpecificationOsDisk"], result)

    @builtins.property
    def tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLaunchSpecificationTag"]]]:
        '''tag block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#tag OceanAksVirtualNodeGroup#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLaunchSpecificationTag"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksVirtualNodeGroupLaunchSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksVirtualNodeGroupLaunchSpecificationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupLaunchSpecificationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c75331e483436a5ee122020230b09f1097bc89030bd6e3f7340680a73a4d695b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OceanAksVirtualNodeGroupLaunchSpecificationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bc381f004726bdd7a080b0a8614ec1f6cbc48ffad7abfeb75f84c12656db340)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksVirtualNodeGroupLaunchSpecificationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7288165a8922f5e47c861095cebf8a409ca56befbd514b07f87921f0dfc85e1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eaab0b5bd8b81a4504e1679316d22d1a2e28a4a222c4c84ef7734c8e0d1c4a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbc3e35085bc2f35b5fc137db5e731bf610b69532743f1985906855677734019)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLaunchSpecification]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLaunchSpecification]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLaunchSpecification]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa92cf4a72ee7dfd2ec3f9622a8265ca549d80f8e63ff28f333dbddf6d42f5ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupLaunchSpecificationOsDisk",
    jsii_struct_bases=[],
    name_mapping={
        "size_gb": "sizeGb",
        "type": "type",
        "utilize_ephemeral_storage": "utilizeEphemeralStorage",
    },
)
class OceanAksVirtualNodeGroupLaunchSpecificationOsDisk:
    def __init__(
        self,
        *,
        size_gb: jsii.Number,
        type: typing.Optional[builtins.str] = None,
        utilize_ephemeral_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param size_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#size_gb OceanAksVirtualNodeGroup#size_gb}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#type OceanAksVirtualNodeGroup#type}.
        :param utilize_ephemeral_storage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#utilize_ephemeral_storage OceanAksVirtualNodeGroup#utilize_ephemeral_storage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc938a3276702a3aed560b993b7f1f01fdb0faf2ae627343083346a8263fedf)
            check_type(argname="argument size_gb", value=size_gb, expected_type=type_hints["size_gb"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument utilize_ephemeral_storage", value=utilize_ephemeral_storage, expected_type=type_hints["utilize_ephemeral_storage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "size_gb": size_gb,
        }
        if type is not None:
            self._values["type"] = type
        if utilize_ephemeral_storage is not None:
            self._values["utilize_ephemeral_storage"] = utilize_ephemeral_storage

    @builtins.property
    def size_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#size_gb OceanAksVirtualNodeGroup#size_gb}.'''
        result = self._values.get("size_gb")
        assert result is not None, "Required property 'size_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#type OceanAksVirtualNodeGroup#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def utilize_ephemeral_storage(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#utilize_ephemeral_storage OceanAksVirtualNodeGroup#utilize_ephemeral_storage}.'''
        result = self._values.get("utilize_ephemeral_storage")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksVirtualNodeGroupLaunchSpecificationOsDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksVirtualNodeGroupLaunchSpecificationOsDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupLaunchSpecificationOsDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb4569f5442897e6d94f13856ba8d9ebc6f746ecbd9960a6c17ab3387e6ac1ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUtilizeEphemeralStorage")
    def reset_utilize_ephemeral_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUtilizeEphemeralStorage", []))

    @builtins.property
    @jsii.member(jsii_name="sizeGbInput")
    def size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="utilizeEphemeralStorageInput")
    def utilize_ephemeral_storage_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "utilizeEphemeralStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeGb")
    def size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGb"))

    @size_gb.setter
    def size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f15cc7768d4765f33aa0aad78e613b8a27961e32a5a7a4fb13f430ef8f735705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGb", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c217c33aaf8641e99c51a28b22c2f0b98b8148c07023aeb40822dc8a04eb6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="utilizeEphemeralStorage")
    def utilize_ephemeral_storage(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "utilizeEphemeralStorage"))

    @utilize_ephemeral_storage.setter
    def utilize_ephemeral_storage(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ad4e218ad047f4f18b62d541fbe21bd583bc57bb9f6031f8d9da096b671f21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "utilizeEphemeralStorage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OceanAksVirtualNodeGroupLaunchSpecificationOsDisk]:
        return typing.cast(typing.Optional[OceanAksVirtualNodeGroupLaunchSpecificationOsDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OceanAksVirtualNodeGroupLaunchSpecificationOsDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ff7590550113d353c32490a933caf44ba93e6d93c3264b21c9de8db56923ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksVirtualNodeGroupLaunchSpecificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupLaunchSpecificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9ae52d917bfb51ca648c0f36571d6c787fcbbdc06b5435cc6d397030511279d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putOsDisk")
    def put_os_disk(
        self,
        *,
        size_gb: jsii.Number,
        type: typing.Optional[builtins.str] = None,
        utilize_ephemeral_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param size_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#size_gb OceanAksVirtualNodeGroup#size_gb}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#type OceanAksVirtualNodeGroup#type}.
        :param utilize_ephemeral_storage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#utilize_ephemeral_storage OceanAksVirtualNodeGroup#utilize_ephemeral_storage}.
        '''
        value = OceanAksVirtualNodeGroupLaunchSpecificationOsDisk(
            size_gb=size_gb,
            type=type,
            utilize_ephemeral_storage=utilize_ephemeral_storage,
        )

        return typing.cast(None, jsii.invoke(self, "putOsDisk", [value]))

    @jsii.member(jsii_name="putTag")
    def put_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVirtualNodeGroupLaunchSpecificationTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ccd0456c40a64b008c9fbb441632f1fbcf7c7d048e9867a3213493e0101cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTag", [value]))

    @jsii.member(jsii_name="resetMaxPods")
    def reset_max_pods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPods", []))

    @jsii.member(jsii_name="resetOsDisk")
    def reset_os_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDisk", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @builtins.property
    @jsii.member(jsii_name="osDisk")
    def os_disk(
        self,
    ) -> OceanAksVirtualNodeGroupLaunchSpecificationOsDiskOutputReference:
        return typing.cast(OceanAksVirtualNodeGroupLaunchSpecificationOsDiskOutputReference, jsii.get(self, "osDisk"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> "OceanAksVirtualNodeGroupLaunchSpecificationTagList":
        return typing.cast("OceanAksVirtualNodeGroupLaunchSpecificationTagList", jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsInput")
    def max_pods_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskInput")
    def os_disk_input(
        self,
    ) -> typing.Optional[OceanAksVirtualNodeGroupLaunchSpecificationOsDisk]:
        return typing.cast(typing.Optional[OceanAksVirtualNodeGroupLaunchSpecificationOsDisk], jsii.get(self, "osDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLaunchSpecificationTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVirtualNodeGroupLaunchSpecificationTag"]]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPods")
    def max_pods(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPods"))

    @max_pods.setter
    def max_pods(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699d15ac03847d140a29fd20e6cc27bb1f60aeaaa0066f9a9570b0833866fbaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPods", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksVirtualNodeGroupLaunchSpecification, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksVirtualNodeGroupLaunchSpecification, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupLaunchSpecification, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f165b9e6dd9539e7207db49e7cb48680b17db1577ca9f4d7033e8b4c6190b0d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupLaunchSpecificationTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class OceanAksVirtualNodeGroupLaunchSpecificationTag:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#key OceanAksVirtualNodeGroup#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#value OceanAksVirtualNodeGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbfc81642e90b1dba2bfb8a21aa621ac9685a0cebf04a4930135be25b3a8b534)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#key OceanAksVirtualNodeGroup#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#value OceanAksVirtualNodeGroup#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksVirtualNodeGroupLaunchSpecificationTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksVirtualNodeGroupLaunchSpecificationTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupLaunchSpecificationTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf4cdd1d54540321d13bf3d02673f69e09a52e1d8a67940132939150e828a697)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OceanAksVirtualNodeGroupLaunchSpecificationTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164e941e6bdc5d42ab10cf291656f9171eeb264fdbc8a8ca9b420ed9bafb0c3e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksVirtualNodeGroupLaunchSpecificationTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e82a2ce7faa97b15b2e710f7c5f2948bbe1b2c27417d4e9f41a42aaaffce96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2334419ac47f05111c234a47af628c838b01d50a120ce1db23ec182da8d24d5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebb7842043915a4f51ecbbf447d7d1b36091625f6f9e2bf702ffb2ecc0700d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLaunchSpecificationTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLaunchSpecificationTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLaunchSpecificationTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ccd70aedbe69e798ee8052fa029681220e24fb32ef2888ec5d6a261532df8dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksVirtualNodeGroupLaunchSpecificationTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupLaunchSpecificationTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f05294bcb34e36644ff827514dfd60a7739660db8c79919a47464e2df64eeb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d37b94510b751463b183e97b3826f8303a703bc7dac30950d64a9bce6741bd92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a63105aff5bad2c9ec8d85ce3cb99144f556142a25272d06bde23d5bb45425f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksVirtualNodeGroupLaunchSpecificationTag, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksVirtualNodeGroupLaunchSpecificationTag, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupLaunchSpecificationTag, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfd56a8cc3306a88c3fcacb02d2dd858f8ae4e8139de5b5c736a67d0c7a10a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupResourceLimits",
    jsii_struct_bases=[],
    name_mapping={"max_instance_count": "maxInstanceCount"},
)
class OceanAksVirtualNodeGroupResourceLimits:
    def __init__(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instance_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#max_instance_count OceanAksVirtualNodeGroup#max_instance_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ef2b720100616ab7c46e61e8b9d56346e27650e2c88c13b6461e362b75c7c0)
            check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_instance_count is not None:
            self._values["max_instance_count"] = max_instance_count

    @builtins.property
    def max_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#max_instance_count OceanAksVirtualNodeGroup#max_instance_count}.'''
        result = self._values.get("max_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksVirtualNodeGroupResourceLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksVirtualNodeGroupResourceLimitsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupResourceLimitsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__962b3e0e7b3b7416c5def3d79db9e7ced8848597df09feb756605288ab55a512)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OceanAksVirtualNodeGroupResourceLimitsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad4229d20d631d5cb5b42123e52634248a75d4e4d150d57c5ef50c7afb720a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksVirtualNodeGroupResourceLimitsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f07977243667c90d4b9ff5dd04233109a5c594bef1c07d3fb2ba6f50ba4819)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f86642379ecdee526980870d8a703426fd136146f052975a6ec448e83641609d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19c350242ebca65c9481c91b92fe46d7f2e7bce22175a2fc571981ff31f28d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupResourceLimits]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupResourceLimits]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupResourceLimits]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b2f8e79c68482be22a5705a6a89cef0de590a74182b389c9cafed6be884707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksVirtualNodeGroupResourceLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupResourceLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c5469406142f7b669403e503e11e59c96cc758afcb3a1e45fed54d655bce8f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMaxInstanceCount")
    def reset_max_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceCount", []))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCountInput")
    def max_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCount")
    def max_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceCount"))

    @max_instance_count.setter
    def max_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa966f361689598fe89330d661448cd3b188f0bdd180a954fcabce4ad3d568d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksVirtualNodeGroupResourceLimits, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksVirtualNodeGroupResourceLimits, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupResourceLimits, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f70e3d3f6f169a978ee240fa7c32761f93b49dd39558f51b48dfe5208114a8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupTaint",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class OceanAksVirtualNodeGroupTaint:
    def __init__(
        self,
        *,
        effect: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param effect: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#effect OceanAksVirtualNodeGroup#effect}.
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#key OceanAksVirtualNodeGroup#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#value OceanAksVirtualNodeGroup#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c95e3707de8e0d546b3123420d26f5fca2fb2aeb504ffa19e3bd98ac73d083c)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "effect": effect,
            "key": key,
            "value": value,
        }

    @builtins.property
    def effect(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#effect OceanAksVirtualNodeGroup#effect}.'''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#key OceanAksVirtualNodeGroup#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks_virtual_node_group#value OceanAksVirtualNodeGroup#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksVirtualNodeGroupTaint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksVirtualNodeGroupTaintList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupTaintList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e53bb5f76498a81e4d7ec10cf5c67ee5bf0c23e1777701e2a5ff000d348a768)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OceanAksVirtualNodeGroupTaintOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014ed4ee7c557dc963d63401f5cb6d0ed6cdf340d359d530c33f3607865574a5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksVirtualNodeGroupTaintOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4c16826e3f4107439fed10b35e98a941076d683dc0808d8d2f9c7a9c2827fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ba2f43452233ec34a2b4aa2055a374defbf65d567bf56dea1aafe2e1f9245d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36187c3f6490198d0b1acbafe6ecc17606bd6741e96038ca9a76bf94f310f802)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupTaint]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupTaint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupTaint]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc952b9f7cf6864933bdf9f6f2f7781b6ab32ac2c39a86300d76bde55ff8c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksVirtualNodeGroupTaintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksVirtualNodeGroup.OceanAksVirtualNodeGroupTaintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__241ee8ea31adfab7647c52cf5256fe2a0d20f7b3ae439193a8cd26b1454372fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca4b376a16bcfa67dca16b030e597dc2c6e552b8aa4d3be3760a0cdf12a1477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99095d28b381572ad613537cc8790ed3a7f9895ccaabe70d53f39b59601309ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a408da67a81683a870608f786ecd12168d2d39b72abd005e158d8cee1ba5ddf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksVirtualNodeGroupTaint, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksVirtualNodeGroupTaint, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupTaint, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ae5c365d4ee413dc299cf9abd8499da25930836aface3efd4842fb36fb1d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OceanAksVirtualNodeGroup",
    "OceanAksVirtualNodeGroupAutoscale",
    "OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom",
    "OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroomList",
    "OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroomOutputReference",
    "OceanAksVirtualNodeGroupAutoscaleList",
    "OceanAksVirtualNodeGroupAutoscaleOutputReference",
    "OceanAksVirtualNodeGroupConfig",
    "OceanAksVirtualNodeGroupLabel",
    "OceanAksVirtualNodeGroupLabelList",
    "OceanAksVirtualNodeGroupLabelOutputReference",
    "OceanAksVirtualNodeGroupLaunchSpecification",
    "OceanAksVirtualNodeGroupLaunchSpecificationList",
    "OceanAksVirtualNodeGroupLaunchSpecificationOsDisk",
    "OceanAksVirtualNodeGroupLaunchSpecificationOsDiskOutputReference",
    "OceanAksVirtualNodeGroupLaunchSpecificationOutputReference",
    "OceanAksVirtualNodeGroupLaunchSpecificationTag",
    "OceanAksVirtualNodeGroupLaunchSpecificationTagList",
    "OceanAksVirtualNodeGroupLaunchSpecificationTagOutputReference",
    "OceanAksVirtualNodeGroupResourceLimits",
    "OceanAksVirtualNodeGroupResourceLimitsList",
    "OceanAksVirtualNodeGroupResourceLimitsOutputReference",
    "OceanAksVirtualNodeGroupTaint",
    "OceanAksVirtualNodeGroupTaintList",
    "OceanAksVirtualNodeGroupTaintOutputReference",
]

publication.publish()

def _typecheckingstub__678dcb933d2f9320b35530486a942b429232d45972984bb342bf1dbbaf281add(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    ocean_id: builtins.str,
    autoscale: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupAutoscale, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    label: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupLabel, typing.Dict[builtins.str, typing.Any]]]]] = None,
    launch_specification: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupLaunchSpecification, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_limits: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupResourceLimits, typing.Dict[builtins.str, typing.Any]]]]] = None,
    taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupTaint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__eab3e62ce91acb0181c8598c82ab26202938448a191a3d0e1373e1acf063956f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupAutoscale, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dbffda12ff03921a2a1edb65e7c8ca51122f7269f99577bd673ba813b110b86(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupLabel, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816b31ce5291772b1cb1acf754e50aa93265abf17cad1f2934524d5937732426(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupLaunchSpecification, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a030c04f4b80cc7eb34b1bac8830824eccf036ce42161daeb8c2f3923295f9a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupResourceLimits, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927a28e9a289f970287f5dba7c4c9fa91682579e7a9f8b4bb81827c01049131d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupTaint, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b9335b736ce17373e5b034e52168074241d4771a887f4f6ea7731a67c1d44d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1cbc0fbd2b79c2c3880d074455899473bfb80e7d252f86aaf4fd4e4f5151b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c3b936c86559cd4176acb7153c678a5eda4f709f107ad944aba0551cb6b210(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8e31ca0b429a458e9c9ae5a3e54b8503ed9bdd74bd5513c159dd50d69fdc63(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82bcbd44ed69e4bb71e87541f056000212152765a869cf0b34a43e1c84cb3413(
    *,
    auto_headroom_percentage: typing.Optional[jsii.Number] = None,
    autoscale_headroom: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4276c79fcaad5c4a61bf3eb86e86f13ac213fe946ab2e7a30228b43fc1b79262(
    *,
    num_of_units: jsii.Number,
    cpu_per_unit: typing.Optional[jsii.Number] = None,
    gpu_per_unit: typing.Optional[jsii.Number] = None,
    memory_per_unit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239d226d2c55913edb8ec3a7cade81abbcfbe535884dc5638a87bcd28df9357c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2733a57f2069ea00f99e8b08cdc247bfaf91f5683e3047aadecfc690f910c187(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6899f3304a68f79781b575fa2980b0b38226d026767eaf35412dc83cbc26ebdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc31eaf59edd16f2f58cb363aaa48baa1ee472a890d37bc35a9895bbcbdfa94d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e731c36047e5003004ffa85700fa77ec7ecc305f2aaa3b5065e26e857d49e683(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfc48eb6ef2dd006a2cae53eda857d94c5624f7129b184a5360f9a135008258(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99db8aa0940007e3ef605ea31ef8821ac4b4b7a17678dd224908ce44f0d35e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7e955255e239a3a3f6e8e7cc7dfea5fa5ef3cad865a036d18054dee703519a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288ede7280d999e53dabbee751d14d4a052e02929f214eb3c637ac15cb43d742(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc19ef8d247c0b9a0b7c528557a5041578696b49ee5382f4112625436c2db34(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8733639d838fccdd6f10e15455f49345d8f296aa015ec8ed4ac9aef78c2fe7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450a43f68d7f0cf743eed605bc53625f307678130a1f773a51e33a55cc2cb14b(
    value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aac60ba12eb0d381610f63554cb3ccc45d37987e0373f543e7fa55b5adb1927(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c258580e7e176b66228d78e5113aa3f7f50e6ba5d09b955d6078fbffc3d8ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754b4a2c1b9500c7f4ab430750ce4e7a096b8c72743af906675769f0a4a2c14f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f72a2b4ec93f9785b92c3639140b2509892f248cb95d4c98ba03f025446ed66(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862ebee95a69cf344d0d11ea9e91ae931a535011ad02c4c80ebea5a9e2635bb4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3dd749bab571524673f176bf93db88e1867293b7db9b05801ded055df07c1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupAutoscale]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da57c8f30c21d0e35b3d88ff312ea828b42ff5d6560886e81cdfa91f092951fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab376916d595041b38e410de0a56cd686e698101fc09c1629af123f009ba31d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupAutoscaleAutoscaleHeadroom, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb6dd47e7abd3fd054a6f2e54229284422c25f121afed210c15b2e6cbd6e3c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae621e5913786098c31f360e75de73d932312d5e3fe6a6983a3f6d99b228d04(
    value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupAutoscale, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb30657daae1809c581ba647acc74c874d226e6578afba3dd72044758a201d3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    ocean_id: builtins.str,
    autoscale: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupAutoscale, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    label: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupLabel, typing.Dict[builtins.str, typing.Any]]]]] = None,
    launch_specification: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupLaunchSpecification, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_limits: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupResourceLimits, typing.Dict[builtins.str, typing.Any]]]]] = None,
    taint: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupTaint, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7221e1e657456ffa7d68502f02f195b3657d1bd641bcb61b5c8fad91ff68816e(
    *,
    key: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f677f49e5db73b84a58af654e018dca4ccca33035683f1113d7dd8c7d9acbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2a91d72f4c6235183a8ff8b4e22318e4cc8502602e99cc015c633cdfaa848a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7910cc69252c546409b0e9e9c4009adde06008dedd0316d95e222e749e3eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d22b453ec21312960aa6cd04c2a6f0a9b00d00312934dc4e2bf36ab5fdd3ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c802792965df267351bb07a9e9eec4f82a765c0afad8738d53c33e26ce6a035(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061f2d1684cfdcd4d96a7d8e50c4788659f2d24e363c063361224d321b51d432(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLabel]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e678a0b88bccde0cdf747dc3656925c6fae4ac1d67dd90fd42d853cdc0b7615c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed3d35737b3915e9c0d5a5e4d635c5cb8bcb627c6d67dc632f0297ece9d8057(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92ec4d0d975aa3917b05b32355cc13d0e5caec2ff321f41be2158ea110c78ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbb542782f37f9c45d025bf266e37c48e39d9478215c592c00a3a1ba09ab4a1(
    value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupLabel, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126d63f238f15fb2a97cd2ec18dfb53be91e3f4d97d2ead67262cfb4e92ffb1f(
    *,
    max_pods: typing.Optional[jsii.Number] = None,
    os_disk: typing.Optional[typing.Union[OceanAksVirtualNodeGroupLaunchSpecificationOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupLaunchSpecificationTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75331e483436a5ee122020230b09f1097bc89030bd6e3f7340680a73a4d695b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc381f004726bdd7a080b0a8614ec1f6cbc48ffad7abfeb75f84c12656db340(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7288165a8922f5e47c861095cebf8a409ca56befbd514b07f87921f0dfc85e1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eaab0b5bd8b81a4504e1679316d22d1a2e28a4a222c4c84ef7734c8e0d1c4a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc3e35085bc2f35b5fc137db5e731bf610b69532743f1985906855677734019(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa92cf4a72ee7dfd2ec3f9622a8265ca549d80f8e63ff28f333dbddf6d42f5ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLaunchSpecification]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc938a3276702a3aed560b993b7f1f01fdb0faf2ae627343083346a8263fedf(
    *,
    size_gb: jsii.Number,
    type: typing.Optional[builtins.str] = None,
    utilize_ephemeral_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4569f5442897e6d94f13856ba8d9ebc6f746ecbd9960a6c17ab3387e6ac1ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f15cc7768d4765f33aa0aad78e613b8a27961e32a5a7a4fb13f430ef8f735705(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c217c33aaf8641e99c51a28b22c2f0b98b8148c07023aeb40822dc8a04eb6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ad4e218ad047f4f18b62d541fbe21bd583bc57bb9f6031f8d9da096b671f21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ff7590550113d353c32490a933caf44ba93e6d93c3264b21c9de8db56923ec(
    value: typing.Optional[OceanAksVirtualNodeGroupLaunchSpecificationOsDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ae52d917bfb51ca648c0f36571d6c787fcbbdc06b5435cc6d397030511279d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ccd0456c40a64b008c9fbb441632f1fbcf7c7d048e9867a3213493e0101cfa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVirtualNodeGroupLaunchSpecificationTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699d15ac03847d140a29fd20e6cc27bb1f60aeaaa0066f9a9570b0833866fbaa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f165b9e6dd9539e7207db49e7cb48680b17db1577ca9f4d7033e8b4c6190b0d4(
    value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupLaunchSpecification, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbfc81642e90b1dba2bfb8a21aa621ac9685a0cebf04a4930135be25b3a8b534(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf4cdd1d54540321d13bf3d02673f69e09a52e1d8a67940132939150e828a697(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164e941e6bdc5d42ab10cf291656f9171eeb264fdbc8a8ca9b420ed9bafb0c3e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e82a2ce7faa97b15b2e710f7c5f2948bbe1b2c27417d4e9f41a42aaaffce96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2334419ac47f05111c234a47af628c838b01d50a120ce1db23ec182da8d24d5c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb7842043915a4f51ecbbf447d7d1b36091625f6f9e2bf702ffb2ecc0700d26(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccd70aedbe69e798ee8052fa029681220e24fb32ef2888ec5d6a261532df8dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupLaunchSpecificationTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f05294bcb34e36644ff827514dfd60a7739660db8c79919a47464e2df64eeb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37b94510b751463b183e97b3826f8303a703bc7dac30950d64a9bce6741bd92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a63105aff5bad2c9ec8d85ce3cb99144f556142a25272d06bde23d5bb45425f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfd56a8cc3306a88c3fcacb02d2dd858f8ae4e8139de5b5c736a67d0c7a10a5(
    value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupLaunchSpecificationTag, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ef2b720100616ab7c46e61e8b9d56346e27650e2c88c13b6461e362b75c7c0(
    *,
    max_instance_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962b3e0e7b3b7416c5def3d79db9e7ced8848597df09feb756605288ab55a512(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad4229d20d631d5cb5b42123e52634248a75d4e4d150d57c5ef50c7afb720a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f07977243667c90d4b9ff5dd04233109a5c594bef1c07d3fb2ba6f50ba4819(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86642379ecdee526980870d8a703426fd136146f052975a6ec448e83641609d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c350242ebca65c9481c91b92fe46d7f2e7bce22175a2fc571981ff31f28d15(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b2f8e79c68482be22a5705a6a89cef0de590a74182b389c9cafed6be884707(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupResourceLimits]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5469406142f7b669403e503e11e59c96cc758afcb3a1e45fed54d655bce8f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa966f361689598fe89330d661448cd3b188f0bdd180a954fcabce4ad3d568d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f70e3d3f6f169a978ee240fa7c32761f93b49dd39558f51b48dfe5208114a8f(
    value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupResourceLimits, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c95e3707de8e0d546b3123420d26f5fca2fb2aeb504ffa19e3bd98ac73d083c(
    *,
    effect: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e53bb5f76498a81e4d7ec10cf5c67ee5bf0c23e1777701e2a5ff000d348a768(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014ed4ee7c557dc963d63401f5cb6d0ed6cdf340d359d530c33f3607865574a5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4c16826e3f4107439fed10b35e98a941076d683dc0808d8d2f9c7a9c2827fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba2f43452233ec34a2b4aa2055a374defbf65d567bf56dea1aafe2e1f9245d8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36187c3f6490198d0b1acbafe6ecc17606bd6741e96038ca9a76bf94f310f802(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc952b9f7cf6864933bdf9f6f2f7781b6ab32ac2c39a86300d76bde55ff8c8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVirtualNodeGroupTaint]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241ee8ea31adfab7647c52cf5256fe2a0d20f7b3ae439193a8cd26b1454372fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca4b376a16bcfa67dca16b030e597dc2c6e552b8aa4d3be3760a0cdf12a1477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99095d28b381572ad613537cc8790ed3a7f9895ccaabe70d53f39b59601309ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a408da67a81683a870608f786ecd12168d2d39b72abd005e158d8cee1ba5ddf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ae5c365d4ee413dc299cf9abd8499da25930836aface3efd4842fb36fb1d59(
    value: typing.Optional[typing.Union[OceanAksVirtualNodeGroupTaint, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
