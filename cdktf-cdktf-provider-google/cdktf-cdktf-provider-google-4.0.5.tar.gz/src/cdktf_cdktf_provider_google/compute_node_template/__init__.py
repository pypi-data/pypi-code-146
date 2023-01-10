'''
# `google_compute_node_template`

Refer to the Terraform Registory for docs: [`google_compute_node_template`](https://www.terraform.io/docs/providers/google/r/compute_node_template).
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


class ComputeNodeTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplate",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/compute_node_template google_compute_node_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cpu_overcommit_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        node_affinity_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_type: typing.Optional[builtins.str] = None,
        node_type_flexibility: typing.Optional[typing.Union["ComputeNodeTemplateNodeTypeFlexibility", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        server_binding: typing.Optional[typing.Union["ComputeNodeTemplateServerBinding", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeNodeTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/compute_node_template google_compute_node_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cpu_overcommit_type: CPU overcommit. Default value: "NONE" Possible values: ["ENABLED", "NONE"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#cpu_overcommit_type ComputeNodeTemplate#cpu_overcommit_type}
        :param description: An optional textual description of the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#description ComputeNodeTemplate#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#id ComputeNodeTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Name of the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#name ComputeNodeTemplate#name}
        :param node_affinity_labels: Labels to use for node affinity, which will be used in instance scheduling. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#node_affinity_labels ComputeNodeTemplate#node_affinity_labels}
        :param node_type: Node type to use for nodes group that are created from this template. Only one of nodeTypeFlexibility and nodeType can be specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#node_type ComputeNodeTemplate#node_type}
        :param node_type_flexibility: node_type_flexibility block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#node_type_flexibility ComputeNodeTemplate#node_type_flexibility}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#project ComputeNodeTemplate#project}.
        :param region: Region where nodes using the node template will be created. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#region ComputeNodeTemplate#region}
        :param server_binding: server_binding block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#server_binding ComputeNodeTemplate#server_binding}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#timeouts ComputeNodeTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a7fd3496aa64577524335df376838dc98d6ec71472a09fc5b8f9afe09fa14d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeNodeTemplateConfig(
            cpu_overcommit_type=cpu_overcommit_type,
            description=description,
            id=id,
            name=name,
            node_affinity_labels=node_affinity_labels,
            node_type=node_type,
            node_type_flexibility=node_type_flexibility,
            project=project,
            region=region,
            server_binding=server_binding,
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

    @jsii.member(jsii_name="putNodeTypeFlexibility")
    def put_node_type_flexibility(
        self,
        *,
        cpus: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpus: Number of virtual CPUs to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#cpus ComputeNodeTemplate#cpus}
        :param memory: Physical memory available to the node, defined in MB. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#memory ComputeNodeTemplate#memory}
        '''
        value = ComputeNodeTemplateNodeTypeFlexibility(cpus=cpus, memory=memory)

        return typing.cast(None, jsii.invoke(self, "putNodeTypeFlexibility", [value]))

    @jsii.member(jsii_name="putServerBinding")
    def put_server_binding(self, *, type: builtins.str) -> None:
        '''
        :param type: Type of server binding policy. If 'RESTART_NODE_ON_ANY_SERVER', nodes using this template will restart on any physical server following a maintenance event. If 'RESTART_NODE_ON_MINIMAL_SERVER', nodes using this template will restart on the same physical server following a maintenance event, instead of being live migrated to or restarted on a new physical server. This option may be useful if you are using software licenses tied to the underlying server characteristics such as physical sockets or cores, to avoid the need for additional licenses when maintenance occurs. However, VMs on such nodes will experience outages while maintenance is applied. Possible values: ["RESTART_NODE_ON_ANY_SERVER", "RESTART_NODE_ON_MINIMAL_SERVERS"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#type ComputeNodeTemplate#type}
        '''
        value = ComputeNodeTemplateServerBinding(type=type)

        return typing.cast(None, jsii.invoke(self, "putServerBinding", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#create ComputeNodeTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#delete ComputeNodeTemplate#delete}.
        '''
        value = ComputeNodeTemplateTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCpuOvercommitType")
    def reset_cpu_overcommit_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuOvercommitType", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNodeAffinityLabels")
    def reset_node_affinity_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeAffinityLabels", []))

    @jsii.member(jsii_name="resetNodeType")
    def reset_node_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeType", []))

    @jsii.member(jsii_name="resetNodeTypeFlexibility")
    def reset_node_type_flexibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeTypeFlexibility", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetServerBinding")
    def reset_server_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerBinding", []))

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
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeFlexibility")
    def node_type_flexibility(
        self,
    ) -> "ComputeNodeTemplateNodeTypeFlexibilityOutputReference":
        return typing.cast("ComputeNodeTemplateNodeTypeFlexibilityOutputReference", jsii.get(self, "nodeTypeFlexibility"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="serverBinding")
    def server_binding(self) -> "ComputeNodeTemplateServerBindingOutputReference":
        return typing.cast("ComputeNodeTemplateServerBindingOutputReference", jsii.get(self, "serverBinding"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeNodeTemplateTimeoutsOutputReference":
        return typing.cast("ComputeNodeTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cpuOvercommitTypeInput")
    def cpu_overcommit_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuOvercommitTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinityLabelsInput")
    def node_affinity_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "nodeAffinityLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeFlexibilityInput")
    def node_type_flexibility_input(
        self,
    ) -> typing.Optional["ComputeNodeTemplateNodeTypeFlexibility"]:
        return typing.cast(typing.Optional["ComputeNodeTemplateNodeTypeFlexibility"], jsii.get(self, "nodeTypeFlexibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeInput")
    def node_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="serverBindingInput")
    def server_binding_input(
        self,
    ) -> typing.Optional["ComputeNodeTemplateServerBinding"]:
        return typing.cast(typing.Optional["ComputeNodeTemplateServerBinding"], jsii.get(self, "serverBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["ComputeNodeTemplateTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ComputeNodeTemplateTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuOvercommitType")
    def cpu_overcommit_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuOvercommitType"))

    @cpu_overcommit_type.setter
    def cpu_overcommit_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d712415022023d522e69564f9019cdf851b9002c33313e386bfc723e0f02e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuOvercommitType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ac3c3079370c43fdbf841b600c0bfe3e2c9d870462424e8654ce67a2645b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a0f5120ed469cdbebfc8950b0579d11e194d769bed485d6c1a56c13ac9e842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6201fd4ba29837e86bf3e0ed9588c0a3fbc74732c167f9d99296aa13041a9780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nodeAffinityLabels")
    def node_affinity_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nodeAffinityLabels"))

    @node_affinity_labels.setter
    def node_affinity_labels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1409542951ff74adc9a708ac250baf154c0386d25582cd8ca0ce30279ffb77a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeAffinityLabels", value)

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539dd9ec3771332e287766c1f462eb6b4f65516b8cdfeaef7a9e4f100504b2f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4db10982f760bc8958bea98db2287b4ed0df0f8dea4191cf78cab9cc4e410f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2516b6a95f51cce0c6dc0a3f1ad71e6f3fa7d440abb1a64938207cb760c0e412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cpu_overcommit_type": "cpuOvercommitType",
        "description": "description",
        "id": "id",
        "name": "name",
        "node_affinity_labels": "nodeAffinityLabels",
        "node_type": "nodeType",
        "node_type_flexibility": "nodeTypeFlexibility",
        "project": "project",
        "region": "region",
        "server_binding": "serverBinding",
        "timeouts": "timeouts",
    },
)
class ComputeNodeTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cpu_overcommit_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        node_affinity_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_type: typing.Optional[builtins.str] = None,
        node_type_flexibility: typing.Optional[typing.Union["ComputeNodeTemplateNodeTypeFlexibility", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        server_binding: typing.Optional[typing.Union["ComputeNodeTemplateServerBinding", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeNodeTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cpu_overcommit_type: CPU overcommit. Default value: "NONE" Possible values: ["ENABLED", "NONE"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#cpu_overcommit_type ComputeNodeTemplate#cpu_overcommit_type}
        :param description: An optional textual description of the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#description ComputeNodeTemplate#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#id ComputeNodeTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Name of the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#name ComputeNodeTemplate#name}
        :param node_affinity_labels: Labels to use for node affinity, which will be used in instance scheduling. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#node_affinity_labels ComputeNodeTemplate#node_affinity_labels}
        :param node_type: Node type to use for nodes group that are created from this template. Only one of nodeTypeFlexibility and nodeType can be specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#node_type ComputeNodeTemplate#node_type}
        :param node_type_flexibility: node_type_flexibility block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#node_type_flexibility ComputeNodeTemplate#node_type_flexibility}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#project ComputeNodeTemplate#project}.
        :param region: Region where nodes using the node template will be created. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#region ComputeNodeTemplate#region}
        :param server_binding: server_binding block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#server_binding ComputeNodeTemplate#server_binding}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#timeouts ComputeNodeTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(node_type_flexibility, dict):
            node_type_flexibility = ComputeNodeTemplateNodeTypeFlexibility(**node_type_flexibility)
        if isinstance(server_binding, dict):
            server_binding = ComputeNodeTemplateServerBinding(**server_binding)
        if isinstance(timeouts, dict):
            timeouts = ComputeNodeTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37221f6afb49466914e56fec11d93e17202b06e7750389bfbba0452250477ac)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cpu_overcommit_type", value=cpu_overcommit_type, expected_type=type_hints["cpu_overcommit_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_affinity_labels", value=node_affinity_labels, expected_type=type_hints["node_affinity_labels"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument node_type_flexibility", value=node_type_flexibility, expected_type=type_hints["node_type_flexibility"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument server_binding", value=server_binding, expected_type=type_hints["server_binding"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if cpu_overcommit_type is not None:
            self._values["cpu_overcommit_type"] = cpu_overcommit_type
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if node_affinity_labels is not None:
            self._values["node_affinity_labels"] = node_affinity_labels
        if node_type is not None:
            self._values["node_type"] = node_type
        if node_type_flexibility is not None:
            self._values["node_type_flexibility"] = node_type_flexibility
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if server_binding is not None:
            self._values["server_binding"] = server_binding
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
    def cpu_overcommit_type(self) -> typing.Optional[builtins.str]:
        '''CPU overcommit. Default value: "NONE" Possible values: ["ENABLED", "NONE"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#cpu_overcommit_type ComputeNodeTemplate#cpu_overcommit_type}
        '''
        result = self._values.get("cpu_overcommit_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional textual description of the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#description ComputeNodeTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#id ComputeNodeTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#name ComputeNodeTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_affinity_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to use for node affinity, which will be used in instance scheduling.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#node_affinity_labels ComputeNodeTemplate#node_affinity_labels}
        '''
        result = self._values.get("node_affinity_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''Node type to use for nodes group that are created from this template.

        Only one of nodeTypeFlexibility and nodeType can be specified.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#node_type ComputeNodeTemplate#node_type}
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type_flexibility(
        self,
    ) -> typing.Optional["ComputeNodeTemplateNodeTypeFlexibility"]:
        '''node_type_flexibility block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#node_type_flexibility ComputeNodeTemplate#node_type_flexibility}
        '''
        result = self._values.get("node_type_flexibility")
        return typing.cast(typing.Optional["ComputeNodeTemplateNodeTypeFlexibility"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#project ComputeNodeTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where nodes using the node template will be created. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#region ComputeNodeTemplate#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_binding(self) -> typing.Optional["ComputeNodeTemplateServerBinding"]:
        '''server_binding block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#server_binding ComputeNodeTemplate#server_binding}
        '''
        result = self._values.get("server_binding")
        return typing.cast(typing.Optional["ComputeNodeTemplateServerBinding"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeNodeTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#timeouts ComputeNodeTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeNodeTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateNodeTypeFlexibility",
    jsii_struct_bases=[],
    name_mapping={"cpus": "cpus", "memory": "memory"},
)
class ComputeNodeTemplateNodeTypeFlexibility:
    def __init__(
        self,
        *,
        cpus: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpus: Number of virtual CPUs to use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#cpus ComputeNodeTemplate#cpus}
        :param memory: Physical memory available to the node, defined in MB. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#memory ComputeNodeTemplate#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faba0bc9816df5e52650b1154dbfd16276733b397b0828ad5c46465d1de25158)
            check_type(argname="argument cpus", value=cpus, expected_type=type_hints["cpus"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpus is not None:
            self._values["cpus"] = cpus
        if memory is not None:
            self._values["memory"] = memory

    @builtins.property
    def cpus(self) -> typing.Optional[builtins.str]:
        '''Number of virtual CPUs to use.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#cpus ComputeNodeTemplate#cpus}
        '''
        result = self._values.get("cpus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Physical memory available to the node, defined in MB.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#memory ComputeNodeTemplate#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeTemplateNodeTypeFlexibility(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeTemplateNodeTypeFlexibilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateNodeTypeFlexibilityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42b95c78f767b8e39cf540eb679b39aa2380e6a429f202e6d33fb354e41da32c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpus")
    def reset_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpus", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @builtins.property
    @jsii.member(jsii_name="localSsd")
    def local_ssd(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localSsd"))

    @builtins.property
    @jsii.member(jsii_name="cpusInput")
    def cpus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpusInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="cpus")
    def cpus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpus"))

    @cpus.setter
    def cpus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a9ef706830a01f82adf530c43ff886c38667c8da412b1eba759d35a7c072ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpus", value)

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b715353d07087de787c127c078f5fb49582635107278fdfa832ae81db01c72f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeNodeTemplateNodeTypeFlexibility]:
        return typing.cast(typing.Optional[ComputeNodeTemplateNodeTypeFlexibility], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeNodeTemplateNodeTypeFlexibility],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__936e7b3ac930806529a157b4509c666e015ba25566abb85ec3483838fa3e7198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateServerBinding",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class ComputeNodeTemplateServerBinding:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Type of server binding policy. If 'RESTART_NODE_ON_ANY_SERVER', nodes using this template will restart on any physical server following a maintenance event. If 'RESTART_NODE_ON_MINIMAL_SERVER', nodes using this template will restart on the same physical server following a maintenance event, instead of being live migrated to or restarted on a new physical server. This option may be useful if you are using software licenses tied to the underlying server characteristics such as physical sockets or cores, to avoid the need for additional licenses when maintenance occurs. However, VMs on such nodes will experience outages while maintenance is applied. Possible values: ["RESTART_NODE_ON_ANY_SERVER", "RESTART_NODE_ON_MINIMAL_SERVERS"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#type ComputeNodeTemplate#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf6d368448bd004749888bf72fe5e2b4b0020499f9718365312a56cd641ea0a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of server binding policy. If 'RESTART_NODE_ON_ANY_SERVER', nodes using this template will restart on any physical server following a maintenance event.

        If 'RESTART_NODE_ON_MINIMAL_SERVER', nodes using this template
        will restart on the same physical server following a maintenance
        event, instead of being live migrated to or restarted on a new
        physical server. This option may be useful if you are using
        software licenses tied to the underlying server characteristics
        such as physical sockets or cores, to avoid the need for
        additional licenses when maintenance occurs. However, VMs on such
        nodes will experience outages while maintenance is applied. Possible values: ["RESTART_NODE_ON_ANY_SERVER", "RESTART_NODE_ON_MINIMAL_SERVERS"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#type ComputeNodeTemplate#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeTemplateServerBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeTemplateServerBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateServerBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca9eb1e90d9f8f70caaad2e6f959aa22e7c03c902d38f025b11e66cb0aae1611)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c8cb26733673e8cf69c7e02d18b8700551dd65caf68925d531efce4bd19db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeNodeTemplateServerBinding]:
        return typing.cast(typing.Optional[ComputeNodeTemplateServerBinding], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeNodeTemplateServerBinding],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aac106b0f9990fa231d75b6cd4a81728b26afc4572bb158212031789689bda5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ComputeNodeTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#create ComputeNodeTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#delete ComputeNodeTemplate#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f18e1d98be0a5526aff9af50a949e77e691f212c6ddb61348817a89d538c3c)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#create ComputeNodeTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/compute_node_template#delete ComputeNodeTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNodeTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNodeTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNodeTemplate.ComputeNodeTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e49fb7f82707f3d436f2680c60d1e4e059fde83258dbb996493170ce62dd053)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95dc06b6a4ef25dd00985adc0e669a4c2a12a1f47e827eb585f675146a2c5764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a77fad9a003a81abe7cefbfd567f45c88ada0a42fb0662e825d87d4205b99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ComputeNodeTemplateTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ComputeNodeTemplateTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ComputeNodeTemplateTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a83ffb28093d770220f699ef8d62549dc8887a44335ffb30737a86b50a0f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ComputeNodeTemplate",
    "ComputeNodeTemplateConfig",
    "ComputeNodeTemplateNodeTypeFlexibility",
    "ComputeNodeTemplateNodeTypeFlexibilityOutputReference",
    "ComputeNodeTemplateServerBinding",
    "ComputeNodeTemplateServerBindingOutputReference",
    "ComputeNodeTemplateTimeouts",
    "ComputeNodeTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d5a7fd3496aa64577524335df376838dc98d6ec71472a09fc5b8f9afe09fa14d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cpu_overcommit_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    node_affinity_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_type: typing.Optional[builtins.str] = None,
    node_type_flexibility: typing.Optional[typing.Union[ComputeNodeTemplateNodeTypeFlexibility, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    server_binding: typing.Optional[typing.Union[ComputeNodeTemplateServerBinding, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeNodeTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b5d712415022023d522e69564f9019cdf851b9002c33313e386bfc723e0f02e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ac3c3079370c43fdbf841b600c0bfe3e2c9d870462424e8654ce67a2645b41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a0f5120ed469cdbebfc8950b0579d11e194d769bed485d6c1a56c13ac9e842(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6201fd4ba29837e86bf3e0ed9588c0a3fbc74732c167f9d99296aa13041a9780(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1409542951ff74adc9a708ac250baf154c0386d25582cd8ca0ce30279ffb77a4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539dd9ec3771332e287766c1f462eb6b4f65516b8cdfeaef7a9e4f100504b2f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4db10982f760bc8958bea98db2287b4ed0df0f8dea4191cf78cab9cc4e410f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2516b6a95f51cce0c6dc0a3f1ad71e6f3fa7d440abb1a64938207cb760c0e412(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37221f6afb49466914e56fec11d93e17202b06e7750389bfbba0452250477ac(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cpu_overcommit_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    node_affinity_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_type: typing.Optional[builtins.str] = None,
    node_type_flexibility: typing.Optional[typing.Union[ComputeNodeTemplateNodeTypeFlexibility, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    server_binding: typing.Optional[typing.Union[ComputeNodeTemplateServerBinding, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeNodeTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faba0bc9816df5e52650b1154dbfd16276733b397b0828ad5c46465d1de25158(
    *,
    cpus: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b95c78f767b8e39cf540eb679b39aa2380e6a429f202e6d33fb354e41da32c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a9ef706830a01f82adf530c43ff886c38667c8da412b1eba759d35a7c072ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b715353d07087de787c127c078f5fb49582635107278fdfa832ae81db01c72f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936e7b3ac930806529a157b4509c666e015ba25566abb85ec3483838fa3e7198(
    value: typing.Optional[ComputeNodeTemplateNodeTypeFlexibility],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf6d368448bd004749888bf72fe5e2b4b0020499f9718365312a56cd641ea0a(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9eb1e90d9f8f70caaad2e6f959aa22e7c03c902d38f025b11e66cb0aae1611(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c8cb26733673e8cf69c7e02d18b8700551dd65caf68925d531efce4bd19db3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aac106b0f9990fa231d75b6cd4a81728b26afc4572bb158212031789689bda5(
    value: typing.Optional[ComputeNodeTemplateServerBinding],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f18e1d98be0a5526aff9af50a949e77e691f212c6ddb61348817a89d538c3c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e49fb7f82707f3d436f2680c60d1e4e059fde83258dbb996493170ce62dd053(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95dc06b6a4ef25dd00985adc0e669a4c2a12a1f47e827eb585f675146a2c5764(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a77fad9a003a81abe7cefbfd567f45c88ada0a42fb0662e825d87d4205b99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a83ffb28093d770220f699ef8d62549dc8887a44335ffb30737a86b50a0f1a(
    value: typing.Optional[typing.Union[ComputeNodeTemplateTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
