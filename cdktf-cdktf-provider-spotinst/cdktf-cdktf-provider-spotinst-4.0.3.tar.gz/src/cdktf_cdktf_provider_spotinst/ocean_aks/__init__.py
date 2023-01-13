'''
# `spotinst_ocean_aks`

Refer to the Terraform Registory for docs: [`spotinst_ocean_aks`](https://www.terraform.io/docs/providers/spotinst/r/ocean_aks).
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


class OceanAks(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAks",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks spotinst_ocean_aks}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        acd_identifier: builtins.str,
        aks_name: builtins.str,
        aks_resource_group_name: builtins.str,
        name: builtins.str,
        ssh_public_key: builtins.str,
        autoscaler: typing.Optional[typing.Union["OceanAksAutoscaler", typing.Dict[builtins.str, typing.Any]]] = None,
        controller_cluster_id: typing.Optional[builtins.str] = None,
        custom_data: typing.Optional[builtins.str] = None,
        extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksExtension", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health: typing.Optional[typing.Union["OceanAksHealth", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksImage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        load_balancer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksLoadBalancer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        managed_service_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksManagedServiceIdentity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        network: typing.Optional[typing.Union["OceanAksNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        os_disk: typing.Optional[typing.Union["OceanAksOsDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
        strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        user_name: typing.Optional[builtins.str] = None,
        vm_sizes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVmSizes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks spotinst_ocean_aks} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param acd_identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#acd_identifier OceanAks#acd_identifier}.
        :param aks_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#aks_name OceanAks#aks_name}.
        :param aks_resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#aks_resource_group_name OceanAks#aks_resource_group_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#ssh_public_key OceanAks#ssh_public_key}.
        :param autoscaler: autoscaler block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscaler OceanAks#autoscaler}
        :param controller_cluster_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#controller_cluster_id OceanAks#controller_cluster_id}.
        :param custom_data: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#custom_data OceanAks#custom_data}.
        :param extension: extension block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#extension OceanAks#extension}
        :param health: health block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#health OceanAks#health}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#id OceanAks#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image: image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#image OceanAks#image}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#load_balancer OceanAks#load_balancer}
        :param managed_service_identity: managed_service_identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#managed_service_identity OceanAks#managed_service_identity}
        :param max_pods: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_pods OceanAks#max_pods}.
        :param network: network block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#network OceanAks#network}
        :param os_disk: os_disk block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#os_disk OceanAks#os_disk}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.
        :param strategy: strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#strategy OceanAks#strategy}
        :param tag: tag block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#tag OceanAks#tag}
        :param user_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#user_name OceanAks#user_name}.
        :param vm_sizes: vm_sizes block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#vm_sizes OceanAks#vm_sizes}
        :param zones: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#zones OceanAks#zones}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76dcc528340cfbc5cca9e89b16b8271c4996e77e60921ec340ac55db950aaf04)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OceanAksConfig(
            acd_identifier=acd_identifier,
            aks_name=aks_name,
            aks_resource_group_name=aks_resource_group_name,
            name=name,
            ssh_public_key=ssh_public_key,
            autoscaler=autoscaler,
            controller_cluster_id=controller_cluster_id,
            custom_data=custom_data,
            extension=extension,
            health=health,
            id=id,
            image=image,
            load_balancer=load_balancer,
            managed_service_identity=managed_service_identity,
            max_pods=max_pods,
            network=network,
            os_disk=os_disk,
            resource_group_name=resource_group_name,
            strategy=strategy,
            tag=tag,
            user_name=user_name,
            vm_sizes=vm_sizes,
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

    @jsii.member(jsii_name="putAutoscaler")
    def put_autoscaler(
        self,
        *,
        autoscale_down: typing.Optional[typing.Union["OceanAksAutoscalerAutoscaleDown", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscale_headroom: typing.Optional[typing.Union["OceanAksAutoscalerAutoscaleHeadroom", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscale_is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_limits: typing.Optional[typing.Union["OceanAksAutoscalerResourceLimits", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscale_down: autoscale_down block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscale_down OceanAks#autoscale_down}
        :param autoscale_headroom: autoscale_headroom block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscale_headroom OceanAks#autoscale_headroom}
        :param autoscale_is_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscale_is_enabled OceanAks#autoscale_is_enabled}.
        :param resource_limits: resource_limits block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_limits OceanAks#resource_limits}
        '''
        value = OceanAksAutoscaler(
            autoscale_down=autoscale_down,
            autoscale_headroom=autoscale_headroom,
            autoscale_is_enabled=autoscale_is_enabled,
            resource_limits=resource_limits,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaler", [value]))

    @jsii.member(jsii_name="putExtension")
    def put_extension(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksExtension", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a02531c6ad233b7264dfa86eb3cf920cb3dadb6aa98a733284c81c2445fbd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtension", [value]))

    @jsii.member(jsii_name="putHealth")
    def put_health(self, *, grace_period: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param grace_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#grace_period OceanAks#grace_period}.
        '''
        value = OceanAksHealth(grace_period=grace_period)

        return typing.cast(None, jsii.invoke(self, "putHealth", [value]))

    @jsii.member(jsii_name="putImage")
    def put_image(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksImage", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa34202c53b38a7ff90efb53633e90a444814300c6f96fec63c2c0b78e62625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putImage", [value]))

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksLoadBalancer", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a31d5081b16e33595ce816655e9d039c1aa807785bffb114059ca324c3e87b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLoadBalancer", [value]))

    @jsii.member(jsii_name="putManagedServiceIdentity")
    def put_managed_service_identity(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksManagedServiceIdentity", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe720d0dd31b8952f40e403c612e611d8d4c15bdb11aafa3b67e018abbab6315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagedServiceIdentity", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(
        self,
        *,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksNetworkNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
        virtual_network_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#network_interface OceanAks#network_interface}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.
        :param virtual_network_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#virtual_network_name OceanAks#virtual_network_name}.
        '''
        value = OceanAksNetwork(
            network_interface=network_interface,
            resource_group_name=resource_group_name,
            virtual_network_name=virtual_network_name,
        )

        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putOsDisk")
    def put_os_disk(
        self,
        *,
        size_gb: jsii.Number,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#size_gb OceanAks#size_gb}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#type OceanAks#type}.
        '''
        value = OceanAksOsDisk(size_gb=size_gb, type=type)

        return typing.cast(None, jsii.invoke(self, "putOsDisk", [value]))

    @jsii.member(jsii_name="putStrategy")
    def put_strategy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksStrategy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2574893f221ea86cdb716dee13b16460bc95a494d3c6df60d83c6fcbb5cf5cb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStrategy", [value]))

    @jsii.member(jsii_name="putTag")
    def put_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0723469680dffa85731de3b1f1b0f21c97d0c2eabe68a53aa42f9b020087f231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTag", [value]))

    @jsii.member(jsii_name="putVmSizes")
    def put_vm_sizes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVmSizes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c5b9244b429b69e88ecc45ced4dbbf92a4bbe747594875c2a6532e549b89d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVmSizes", [value]))

    @jsii.member(jsii_name="resetAutoscaler")
    def reset_autoscaler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaler", []))

    @jsii.member(jsii_name="resetControllerClusterId")
    def reset_controller_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControllerClusterId", []))

    @jsii.member(jsii_name="resetCustomData")
    def reset_custom_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomData", []))

    @jsii.member(jsii_name="resetExtension")
    def reset_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtension", []))

    @jsii.member(jsii_name="resetHealth")
    def reset_health(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealth", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetLoadBalancer")
    def reset_load_balancer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancer", []))

    @jsii.member(jsii_name="resetManagedServiceIdentity")
    def reset_managed_service_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedServiceIdentity", []))

    @jsii.member(jsii_name="resetMaxPods")
    def reset_max_pods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPods", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetOsDisk")
    def reset_os_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDisk", []))

    @jsii.member(jsii_name="resetResourceGroupName")
    def reset_resource_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroupName", []))

    @jsii.member(jsii_name="resetStrategy")
    def reset_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrategy", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetUserName")
    def reset_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserName", []))

    @jsii.member(jsii_name="resetVmSizes")
    def reset_vm_sizes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmSizes", []))

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
    @jsii.member(jsii_name="autoscaler")
    def autoscaler(self) -> "OceanAksAutoscalerOutputReference":
        return typing.cast("OceanAksAutoscalerOutputReference", jsii.get(self, "autoscaler"))

    @builtins.property
    @jsii.member(jsii_name="extension")
    def extension(self) -> "OceanAksExtensionList":
        return typing.cast("OceanAksExtensionList", jsii.get(self, "extension"))

    @builtins.property
    @jsii.member(jsii_name="health")
    def health(self) -> "OceanAksHealthOutputReference":
        return typing.cast("OceanAksHealthOutputReference", jsii.get(self, "health"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> "OceanAksImageList":
        return typing.cast("OceanAksImageList", jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> "OceanAksLoadBalancerList":
        return typing.cast("OceanAksLoadBalancerList", jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="managedServiceIdentity")
    def managed_service_identity(self) -> "OceanAksManagedServiceIdentityList":
        return typing.cast("OceanAksManagedServiceIdentityList", jsii.get(self, "managedServiceIdentity"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "OceanAksNetworkOutputReference":
        return typing.cast("OceanAksNetworkOutputReference", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="osDisk")
    def os_disk(self) -> "OceanAksOsDiskOutputReference":
        return typing.cast("OceanAksOsDiskOutputReference", jsii.get(self, "osDisk"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> "OceanAksStrategyList":
        return typing.cast("OceanAksStrategyList", jsii.get(self, "strategy"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> "OceanAksTagList":
        return typing.cast("OceanAksTagList", jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="vmSizes")
    def vm_sizes(self) -> "OceanAksVmSizesList":
        return typing.cast("OceanAksVmSizesList", jsii.get(self, "vmSizes"))

    @builtins.property
    @jsii.member(jsii_name="acdIdentifierInput")
    def acd_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acdIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="aksNameInput")
    def aks_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aksNameInput"))

    @builtins.property
    @jsii.member(jsii_name="aksResourceGroupNameInput")
    def aks_resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aksResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalerInput")
    def autoscaler_input(self) -> typing.Optional["OceanAksAutoscaler"]:
        return typing.cast(typing.Optional["OceanAksAutoscaler"], jsii.get(self, "autoscalerInput"))

    @builtins.property
    @jsii.member(jsii_name="controllerClusterIdInput")
    def controller_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controllerClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customDataInput")
    def custom_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDataInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionInput")
    def extension_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksExtension"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksExtension"]]], jsii.get(self, "extensionInput"))

    @builtins.property
    @jsii.member(jsii_name="healthInput")
    def health_input(self) -> typing.Optional["OceanAksHealth"]:
        return typing.cast(typing.Optional["OceanAksHealth"], jsii.get(self, "healthInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksImage"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksImage"]]], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInput")
    def load_balancer_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksLoadBalancer"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksLoadBalancer"]]], jsii.get(self, "loadBalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="managedServiceIdentityInput")
    def managed_service_identity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksManagedServiceIdentity"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksManagedServiceIdentity"]]], jsii.get(self, "managedServiceIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsInput")
    def max_pods_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional["OceanAksNetwork"]:
        return typing.cast(typing.Optional["OceanAksNetwork"], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskInput")
    def os_disk_input(self) -> typing.Optional["OceanAksOsDisk"]:
        return typing.cast(typing.Optional["OceanAksOsDisk"], jsii.get(self, "osDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeyInput")
    def ssh_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="strategyInput")
    def strategy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksStrategy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksStrategy"]]], jsii.get(self, "strategyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksTag"]]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizesInput")
    def vm_sizes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVmSizes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVmSizes"]]], jsii.get(self, "vmSizesInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="acdIdentifier")
    def acd_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acdIdentifier"))

    @acd_identifier.setter
    def acd_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0749d54685748f661a65031407c5f7cdbf348c4a63dd40970db7998427b716e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acdIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="aksName")
    def aks_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aksName"))

    @aks_name.setter
    def aks_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d66b1d2f8bbf95599c4267f09058671ad282196a1da37be24ed5ce752b4be49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aksName", value)

    @builtins.property
    @jsii.member(jsii_name="aksResourceGroupName")
    def aks_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aksResourceGroupName"))

    @aks_resource_group_name.setter
    def aks_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519dc9ea47002faee8b55a8aa52f55383f4335f0dc9ee236fe5bd6f6e7749403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aksResourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="controllerClusterId")
    def controller_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controllerClusterId"))

    @controller_cluster_id.setter
    def controller_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f62b8d54fd3df01a98a254487c8302fdb271a08c21aa3976044a4501baf314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controllerClusterId", value)

    @builtins.property
    @jsii.member(jsii_name="customData")
    def custom_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customData"))

    @custom_data.setter
    def custom_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d5c635eebdec057515284cff2aebd15c84cf08538ff5fcadbcb5de019942ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customData", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ac62b5e9b72f1c9980992c67eccebdf954e5efcab4e868d5486fd3b3d4b7fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="maxPods")
    def max_pods(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPods"))

    @max_pods.setter
    def max_pods(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d15d8def1b925a9ddb4e403c4653416ec63b2456b828016e3e8b69d037a5178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPods", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f196455de045afa3b3a9447c729ed6c3b569072985815ca41b339cb506ed812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe6f464a37b47b11504678caf48ef31d4de6fe292a4dafe35c245b876849bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="sshPublicKey")
    def ssh_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPublicKey"))

    @ssh_public_key.setter
    def ssh_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7085c72a347909b11b985573f3d11747fb915ed19811e6fb411df54b88aebc4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKey", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa36021afb1de2ff4ab8016f119621d166530615d7f9cf3fd5025d373b7ea3fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a6ac7c9193d3b24cfd89baffa315db5bdadfb358f550ff2689712f03343951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksAutoscaler",
    jsii_struct_bases=[],
    name_mapping={
        "autoscale_down": "autoscaleDown",
        "autoscale_headroom": "autoscaleHeadroom",
        "autoscale_is_enabled": "autoscaleIsEnabled",
        "resource_limits": "resourceLimits",
    },
)
class OceanAksAutoscaler:
    def __init__(
        self,
        *,
        autoscale_down: typing.Optional[typing.Union["OceanAksAutoscalerAutoscaleDown", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscale_headroom: typing.Optional[typing.Union["OceanAksAutoscalerAutoscaleHeadroom", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscale_is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_limits: typing.Optional[typing.Union["OceanAksAutoscalerResourceLimits", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscale_down: autoscale_down block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscale_down OceanAks#autoscale_down}
        :param autoscale_headroom: autoscale_headroom block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscale_headroom OceanAks#autoscale_headroom}
        :param autoscale_is_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscale_is_enabled OceanAks#autoscale_is_enabled}.
        :param resource_limits: resource_limits block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_limits OceanAks#resource_limits}
        '''
        if isinstance(autoscale_down, dict):
            autoscale_down = OceanAksAutoscalerAutoscaleDown(**autoscale_down)
        if isinstance(autoscale_headroom, dict):
            autoscale_headroom = OceanAksAutoscalerAutoscaleHeadroom(**autoscale_headroom)
        if isinstance(resource_limits, dict):
            resource_limits = OceanAksAutoscalerResourceLimits(**resource_limits)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae822831bee781a374a763b68a5a8439d3d48d7dfc1b85784531bed9f8c206b)
            check_type(argname="argument autoscale_down", value=autoscale_down, expected_type=type_hints["autoscale_down"])
            check_type(argname="argument autoscale_headroom", value=autoscale_headroom, expected_type=type_hints["autoscale_headroom"])
            check_type(argname="argument autoscale_is_enabled", value=autoscale_is_enabled, expected_type=type_hints["autoscale_is_enabled"])
            check_type(argname="argument resource_limits", value=resource_limits, expected_type=type_hints["resource_limits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autoscale_down is not None:
            self._values["autoscale_down"] = autoscale_down
        if autoscale_headroom is not None:
            self._values["autoscale_headroom"] = autoscale_headroom
        if autoscale_is_enabled is not None:
            self._values["autoscale_is_enabled"] = autoscale_is_enabled
        if resource_limits is not None:
            self._values["resource_limits"] = resource_limits

    @builtins.property
    def autoscale_down(self) -> typing.Optional["OceanAksAutoscalerAutoscaleDown"]:
        '''autoscale_down block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscale_down OceanAks#autoscale_down}
        '''
        result = self._values.get("autoscale_down")
        return typing.cast(typing.Optional["OceanAksAutoscalerAutoscaleDown"], result)

    @builtins.property
    def autoscale_headroom(
        self,
    ) -> typing.Optional["OceanAksAutoscalerAutoscaleHeadroom"]:
        '''autoscale_headroom block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscale_headroom OceanAks#autoscale_headroom}
        '''
        result = self._values.get("autoscale_headroom")
        return typing.cast(typing.Optional["OceanAksAutoscalerAutoscaleHeadroom"], result)

    @builtins.property
    def autoscale_is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscale_is_enabled OceanAks#autoscale_is_enabled}.'''
        result = self._values.get("autoscale_is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def resource_limits(self) -> typing.Optional["OceanAksAutoscalerResourceLimits"]:
        '''resource_limits block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_limits OceanAks#resource_limits}
        '''
        result = self._values.get("resource_limits")
        return typing.cast(typing.Optional["OceanAksAutoscalerResourceLimits"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksAutoscaler(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksAutoscalerAutoscaleDown",
    jsii_struct_bases=[],
    name_mapping={"max_scale_down_percentage": "maxScaleDownPercentage"},
)
class OceanAksAutoscalerAutoscaleDown:
    def __init__(
        self,
        *,
        max_scale_down_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scale_down_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_scale_down_percentage OceanAks#max_scale_down_percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95862ab1c6ba5f4dff0e85ce26dffc21976ecdd643d2db433f63d4fb25403fc)
            check_type(argname="argument max_scale_down_percentage", value=max_scale_down_percentage, expected_type=type_hints["max_scale_down_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_scale_down_percentage is not None:
            self._values["max_scale_down_percentage"] = max_scale_down_percentage

    @builtins.property
    def max_scale_down_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_scale_down_percentage OceanAks#max_scale_down_percentage}.'''
        result = self._values.get("max_scale_down_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksAutoscalerAutoscaleDown(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksAutoscalerAutoscaleDownOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksAutoscalerAutoscaleDownOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cf6ead3071f846336543f10a88132b736759f20fb62342a64c0281afff72f81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxScaleDownPercentage")
    def reset_max_scale_down_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxScaleDownPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="maxScaleDownPercentageInput")
    def max_scale_down_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxScaleDownPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="maxScaleDownPercentage")
    def max_scale_down_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxScaleDownPercentage"))

    @max_scale_down_percentage.setter
    def max_scale_down_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b89839b3eec125f1afde6b3facf896bd82bb2b39b489b370f9a49c87f01e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxScaleDownPercentage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksAutoscalerAutoscaleDown]:
        return typing.cast(typing.Optional[OceanAksAutoscalerAutoscaleDown], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OceanAksAutoscalerAutoscaleDown],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec44787765eb73e5c15daa1be97e6019eecbb068ee5c853a7034862393727dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksAutoscalerAutoscaleHeadroom",
    jsii_struct_bases=[],
    name_mapping={"automatic": "automatic"},
)
class OceanAksAutoscalerAutoscaleHeadroom:
    def __init__(
        self,
        *,
        automatic: typing.Optional[typing.Union["OceanAksAutoscalerAutoscaleHeadroomAutomatic", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param automatic: automatic block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#automatic OceanAks#automatic}
        '''
        if isinstance(automatic, dict):
            automatic = OceanAksAutoscalerAutoscaleHeadroomAutomatic(**automatic)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e826edea17a771b623e2fd2abe0cd591a4035539838944d0f5860322f14a47)
            check_type(argname="argument automatic", value=automatic, expected_type=type_hints["automatic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automatic is not None:
            self._values["automatic"] = automatic

    @builtins.property
    def automatic(
        self,
    ) -> typing.Optional["OceanAksAutoscalerAutoscaleHeadroomAutomatic"]:
        '''automatic block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#automatic OceanAks#automatic}
        '''
        result = self._values.get("automatic")
        return typing.cast(typing.Optional["OceanAksAutoscalerAutoscaleHeadroomAutomatic"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksAutoscalerAutoscaleHeadroom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksAutoscalerAutoscaleHeadroomAutomatic",
    jsii_struct_bases=[],
    name_mapping={"is_enabled": "isEnabled", "percentage": "percentage"},
)
class OceanAksAutoscalerAutoscaleHeadroomAutomatic:
    def __init__(
        self,
        *,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param is_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#is_enabled OceanAks#is_enabled}.
        :param percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#percentage OceanAks#percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178888b53fdc75c5e2efa6e51a6604f6a0ffcdec1c03c413b23d6793dd388142)
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if percentage is not None:
            self._values["percentage"] = percentage

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#is_enabled OceanAks#is_enabled}.'''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#percentage OceanAks#percentage}.'''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksAutoscalerAutoscaleHeadroomAutomatic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksAutoscalerAutoscaleHeadroomAutomaticOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksAutoscalerAutoscaleHeadroomAutomaticOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07948dc79ed296808a0fe05217142963b0745b248d04d00d633f6bcef6f94c95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetPercentage")
    def reset_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="percentageInput")
    def percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentageInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b399759c6fc1e474558ebb9be3748bf4f572790e2f8f3f36cca6e796abdeaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea3c8977174eb2982a86e09dc58b2b9385cfc34826e3c6e12edc540f12ea0b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OceanAksAutoscalerAutoscaleHeadroomAutomatic]:
        return typing.cast(typing.Optional[OceanAksAutoscalerAutoscaleHeadroomAutomatic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OceanAksAutoscalerAutoscaleHeadroomAutomatic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9958c8102a10db8affb251d25918ff3157ade54f522ce3c005ea5abafdec8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksAutoscalerAutoscaleHeadroomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksAutoscalerAutoscaleHeadroomOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8b94a4ccb3f31b11f453084335f36e14222f91161c528a493906b644c8debd9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutomatic")
    def put_automatic(
        self,
        *,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param is_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#is_enabled OceanAks#is_enabled}.
        :param percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#percentage OceanAks#percentage}.
        '''
        value = OceanAksAutoscalerAutoscaleHeadroomAutomatic(
            is_enabled=is_enabled, percentage=percentage
        )

        return typing.cast(None, jsii.invoke(self, "putAutomatic", [value]))

    @jsii.member(jsii_name="resetAutomatic")
    def reset_automatic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomatic", []))

    @builtins.property
    @jsii.member(jsii_name="automatic")
    def automatic(self) -> OceanAksAutoscalerAutoscaleHeadroomAutomaticOutputReference:
        return typing.cast(OceanAksAutoscalerAutoscaleHeadroomAutomaticOutputReference, jsii.get(self, "automatic"))

    @builtins.property
    @jsii.member(jsii_name="automaticInput")
    def automatic_input(
        self,
    ) -> typing.Optional[OceanAksAutoscalerAutoscaleHeadroomAutomatic]:
        return typing.cast(typing.Optional[OceanAksAutoscalerAutoscaleHeadroomAutomatic], jsii.get(self, "automaticInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksAutoscalerAutoscaleHeadroom]:
        return typing.cast(typing.Optional[OceanAksAutoscalerAutoscaleHeadroom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OceanAksAutoscalerAutoscaleHeadroom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d278692cb611daef7b76fa93355ab1868b4c9f36e875b32d7b7264a1e7aedd0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksAutoscalerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksAutoscalerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2aaae37025d03e48afe15f04b26270a86d1762a8325f627b19cd4f1c1342546)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscaleDown")
    def put_autoscale_down(
        self,
        *,
        max_scale_down_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scale_down_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_scale_down_percentage OceanAks#max_scale_down_percentage}.
        '''
        value = OceanAksAutoscalerAutoscaleDown(
            max_scale_down_percentage=max_scale_down_percentage
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaleDown", [value]))

    @jsii.member(jsii_name="putAutoscaleHeadroom")
    def put_autoscale_headroom(
        self,
        *,
        automatic: typing.Optional[typing.Union[OceanAksAutoscalerAutoscaleHeadroomAutomatic, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param automatic: automatic block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#automatic OceanAks#automatic}
        '''
        value = OceanAksAutoscalerAutoscaleHeadroom(automatic=automatic)

        return typing.cast(None, jsii.invoke(self, "putAutoscaleHeadroom", [value]))

    @jsii.member(jsii_name="putResourceLimits")
    def put_resource_limits(
        self,
        *,
        max_memory_gib: typing.Optional[jsii.Number] = None,
        max_vcpu: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_memory_gib: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_memory_gib OceanAks#max_memory_gib}.
        :param max_vcpu: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_vcpu OceanAks#max_vcpu}.
        '''
        value = OceanAksAutoscalerResourceLimits(
            max_memory_gib=max_memory_gib, max_vcpu=max_vcpu
        )

        return typing.cast(None, jsii.invoke(self, "putResourceLimits", [value]))

    @jsii.member(jsii_name="resetAutoscaleDown")
    def reset_autoscale_down(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaleDown", []))

    @jsii.member(jsii_name="resetAutoscaleHeadroom")
    def reset_autoscale_headroom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaleHeadroom", []))

    @jsii.member(jsii_name="resetAutoscaleIsEnabled")
    def reset_autoscale_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaleIsEnabled", []))

    @jsii.member(jsii_name="resetResourceLimits")
    def reset_resource_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceLimits", []))

    @builtins.property
    @jsii.member(jsii_name="autoscaleDown")
    def autoscale_down(self) -> OceanAksAutoscalerAutoscaleDownOutputReference:
        return typing.cast(OceanAksAutoscalerAutoscaleDownOutputReference, jsii.get(self, "autoscaleDown"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleHeadroom")
    def autoscale_headroom(self) -> OceanAksAutoscalerAutoscaleHeadroomOutputReference:
        return typing.cast(OceanAksAutoscalerAutoscaleHeadroomOutputReference, jsii.get(self, "autoscaleHeadroom"))

    @builtins.property
    @jsii.member(jsii_name="resourceLimits")
    def resource_limits(self) -> "OceanAksAutoscalerResourceLimitsOutputReference":
        return typing.cast("OceanAksAutoscalerResourceLimitsOutputReference", jsii.get(self, "resourceLimits"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleDownInput")
    def autoscale_down_input(self) -> typing.Optional[OceanAksAutoscalerAutoscaleDown]:
        return typing.cast(typing.Optional[OceanAksAutoscalerAutoscaleDown], jsii.get(self, "autoscaleDownInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleHeadroomInput")
    def autoscale_headroom_input(
        self,
    ) -> typing.Optional[OceanAksAutoscalerAutoscaleHeadroom]:
        return typing.cast(typing.Optional[OceanAksAutoscalerAutoscaleHeadroom], jsii.get(self, "autoscaleHeadroomInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleIsEnabledInput")
    def autoscale_is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoscaleIsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceLimitsInput")
    def resource_limits_input(
        self,
    ) -> typing.Optional["OceanAksAutoscalerResourceLimits"]:
        return typing.cast(typing.Optional["OceanAksAutoscalerResourceLimits"], jsii.get(self, "resourceLimitsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleIsEnabled")
    def autoscale_is_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoscaleIsEnabled"))

    @autoscale_is_enabled.setter
    def autoscale_is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaaeb22e91b0020d415fd482c54db243c55ea1e17ab5fe79cc8dd9828d41a78b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscaleIsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksAutoscaler]:
        return typing.cast(typing.Optional[OceanAksAutoscaler], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OceanAksAutoscaler]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793d85455930197670ce5cceb53594184e80a211c31ce1d2d805e561026548e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksAutoscalerResourceLimits",
    jsii_struct_bases=[],
    name_mapping={"max_memory_gib": "maxMemoryGib", "max_vcpu": "maxVcpu"},
)
class OceanAksAutoscalerResourceLimits:
    def __init__(
        self,
        *,
        max_memory_gib: typing.Optional[jsii.Number] = None,
        max_vcpu: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_memory_gib: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_memory_gib OceanAks#max_memory_gib}.
        :param max_vcpu: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_vcpu OceanAks#max_vcpu}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1dee30275acf5b87d2d4accf9272f6a27a0bfd73a3c989de54eb74412313b27)
            check_type(argname="argument max_memory_gib", value=max_memory_gib, expected_type=type_hints["max_memory_gib"])
            check_type(argname="argument max_vcpu", value=max_vcpu, expected_type=type_hints["max_vcpu"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_memory_gib is not None:
            self._values["max_memory_gib"] = max_memory_gib
        if max_vcpu is not None:
            self._values["max_vcpu"] = max_vcpu

    @builtins.property
    def max_memory_gib(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_memory_gib OceanAks#max_memory_gib}.'''
        result = self._values.get("max_memory_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_vcpu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_vcpu OceanAks#max_vcpu}.'''
        result = self._values.get("max_vcpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksAutoscalerResourceLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksAutoscalerResourceLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksAutoscalerResourceLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36601e4f410fc21caffc0bb17991a3a0056fb323a736749f44a713a478924e36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxMemoryGib")
    def reset_max_memory_gib(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxMemoryGib", []))

    @jsii.member(jsii_name="resetMaxVcpu")
    def reset_max_vcpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxVcpu", []))

    @builtins.property
    @jsii.member(jsii_name="maxMemoryGibInput")
    def max_memory_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxMemoryGibInput"))

    @builtins.property
    @jsii.member(jsii_name="maxVcpuInput")
    def max_vcpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxVcpuInput"))

    @builtins.property
    @jsii.member(jsii_name="maxMemoryGib")
    def max_memory_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxMemoryGib"))

    @max_memory_gib.setter
    def max_memory_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646cec1bdc6a0faa7f372d5b70dcbb709c0471937a9c7c7847dc104e2fe83536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxMemoryGib", value)

    @builtins.property
    @jsii.member(jsii_name="maxVcpu")
    def max_vcpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxVcpu"))

    @max_vcpu.setter
    def max_vcpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f0597fa39fdd7c92e20901881e41721bae62cc09d348f9b64a1f78e04719f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxVcpu", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksAutoscalerResourceLimits]:
        return typing.cast(typing.Optional[OceanAksAutoscalerResourceLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OceanAksAutoscalerResourceLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325fda81c706f6a202d6cce330ac6cd4d10fc4622b59892e4fa65492e064b329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "acd_identifier": "acdIdentifier",
        "aks_name": "aksName",
        "aks_resource_group_name": "aksResourceGroupName",
        "name": "name",
        "ssh_public_key": "sshPublicKey",
        "autoscaler": "autoscaler",
        "controller_cluster_id": "controllerClusterId",
        "custom_data": "customData",
        "extension": "extension",
        "health": "health",
        "id": "id",
        "image": "image",
        "load_balancer": "loadBalancer",
        "managed_service_identity": "managedServiceIdentity",
        "max_pods": "maxPods",
        "network": "network",
        "os_disk": "osDisk",
        "resource_group_name": "resourceGroupName",
        "strategy": "strategy",
        "tag": "tag",
        "user_name": "userName",
        "vm_sizes": "vmSizes",
        "zones": "zones",
    },
)
class OceanAksConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        acd_identifier: builtins.str,
        aks_name: builtins.str,
        aks_resource_group_name: builtins.str,
        name: builtins.str,
        ssh_public_key: builtins.str,
        autoscaler: typing.Optional[typing.Union[OceanAksAutoscaler, typing.Dict[builtins.str, typing.Any]]] = None,
        controller_cluster_id: typing.Optional[builtins.str] = None,
        custom_data: typing.Optional[builtins.str] = None,
        extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksExtension", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health: typing.Optional[typing.Union["OceanAksHealth", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksImage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        load_balancer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksLoadBalancer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        managed_service_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksManagedServiceIdentity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        network: typing.Optional[typing.Union["OceanAksNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        os_disk: typing.Optional[typing.Union["OceanAksOsDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
        strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        user_name: typing.Optional[builtins.str] = None,
        vm_sizes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksVmSizes", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param acd_identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#acd_identifier OceanAks#acd_identifier}.
        :param aks_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#aks_name OceanAks#aks_name}.
        :param aks_resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#aks_resource_group_name OceanAks#aks_resource_group_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.
        :param ssh_public_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#ssh_public_key OceanAks#ssh_public_key}.
        :param autoscaler: autoscaler block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscaler OceanAks#autoscaler}
        :param controller_cluster_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#controller_cluster_id OceanAks#controller_cluster_id}.
        :param custom_data: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#custom_data OceanAks#custom_data}.
        :param extension: extension block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#extension OceanAks#extension}
        :param health: health block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#health OceanAks#health}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#id OceanAks#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image: image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#image OceanAks#image}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#load_balancer OceanAks#load_balancer}
        :param managed_service_identity: managed_service_identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#managed_service_identity OceanAks#managed_service_identity}
        :param max_pods: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_pods OceanAks#max_pods}.
        :param network: network block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#network OceanAks#network}
        :param os_disk: os_disk block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#os_disk OceanAks#os_disk}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.
        :param strategy: strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#strategy OceanAks#strategy}
        :param tag: tag block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#tag OceanAks#tag}
        :param user_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#user_name OceanAks#user_name}.
        :param vm_sizes: vm_sizes block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#vm_sizes OceanAks#vm_sizes}
        :param zones: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#zones OceanAks#zones}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaler, dict):
            autoscaler = OceanAksAutoscaler(**autoscaler)
        if isinstance(health, dict):
            health = OceanAksHealth(**health)
        if isinstance(network, dict):
            network = OceanAksNetwork(**network)
        if isinstance(os_disk, dict):
            os_disk = OceanAksOsDisk(**os_disk)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6214905b248239e1ae616041c358f12c757235005dcbf7db8285871cbc0d918)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument acd_identifier", value=acd_identifier, expected_type=type_hints["acd_identifier"])
            check_type(argname="argument aks_name", value=aks_name, expected_type=type_hints["aks_name"])
            check_type(argname="argument aks_resource_group_name", value=aks_resource_group_name, expected_type=type_hints["aks_resource_group_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ssh_public_key", value=ssh_public_key, expected_type=type_hints["ssh_public_key"])
            check_type(argname="argument autoscaler", value=autoscaler, expected_type=type_hints["autoscaler"])
            check_type(argname="argument controller_cluster_id", value=controller_cluster_id, expected_type=type_hints["controller_cluster_id"])
            check_type(argname="argument custom_data", value=custom_data, expected_type=type_hints["custom_data"])
            check_type(argname="argument extension", value=extension, expected_type=type_hints["extension"])
            check_type(argname="argument health", value=health, expected_type=type_hints["health"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument managed_service_identity", value=managed_service_identity, expected_type=type_hints["managed_service_identity"])
            check_type(argname="argument max_pods", value=max_pods, expected_type=type_hints["max_pods"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument os_disk", value=os_disk, expected_type=type_hints["os_disk"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument vm_sizes", value=vm_sizes, expected_type=type_hints["vm_sizes"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "acd_identifier": acd_identifier,
            "aks_name": aks_name,
            "aks_resource_group_name": aks_resource_group_name,
            "name": name,
            "ssh_public_key": ssh_public_key,
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
        if autoscaler is not None:
            self._values["autoscaler"] = autoscaler
        if controller_cluster_id is not None:
            self._values["controller_cluster_id"] = controller_cluster_id
        if custom_data is not None:
            self._values["custom_data"] = custom_data
        if extension is not None:
            self._values["extension"] = extension
        if health is not None:
            self._values["health"] = health
        if id is not None:
            self._values["id"] = id
        if image is not None:
            self._values["image"] = image
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if managed_service_identity is not None:
            self._values["managed_service_identity"] = managed_service_identity
        if max_pods is not None:
            self._values["max_pods"] = max_pods
        if network is not None:
            self._values["network"] = network
        if os_disk is not None:
            self._values["os_disk"] = os_disk
        if resource_group_name is not None:
            self._values["resource_group_name"] = resource_group_name
        if strategy is not None:
            self._values["strategy"] = strategy
        if tag is not None:
            self._values["tag"] = tag
        if user_name is not None:
            self._values["user_name"] = user_name
        if vm_sizes is not None:
            self._values["vm_sizes"] = vm_sizes
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
    def acd_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#acd_identifier OceanAks#acd_identifier}.'''
        result = self._values.get("acd_identifier")
        assert result is not None, "Required property 'acd_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aks_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#aks_name OceanAks#aks_name}.'''
        result = self._values.get("aks_name")
        assert result is not None, "Required property 'aks_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aks_resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#aks_resource_group_name OceanAks#aks_resource_group_name}.'''
        result = self._values.get("aks_resource_group_name")
        assert result is not None, "Required property 'aks_resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_public_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#ssh_public_key OceanAks#ssh_public_key}.'''
        result = self._values.get("ssh_public_key")
        assert result is not None, "Required property 'ssh_public_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaler(self) -> typing.Optional[OceanAksAutoscaler]:
        '''autoscaler block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#autoscaler OceanAks#autoscaler}
        '''
        result = self._values.get("autoscaler")
        return typing.cast(typing.Optional[OceanAksAutoscaler], result)

    @builtins.property
    def controller_cluster_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#controller_cluster_id OceanAks#controller_cluster_id}.'''
        result = self._values.get("controller_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#custom_data OceanAks#custom_data}.'''
        result = self._values.get("custom_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extension(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksExtension"]]]:
        '''extension block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#extension OceanAks#extension}
        '''
        result = self._values.get("extension")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksExtension"]]], result)

    @builtins.property
    def health(self) -> typing.Optional["OceanAksHealth"]:
        '''health block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#health OceanAks#health}
        '''
        result = self._values.get("health")
        return typing.cast(typing.Optional["OceanAksHealth"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#id OceanAks#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksImage"]]]:
        '''image block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#image OceanAks#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksImage"]]], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksLoadBalancer"]]]:
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#load_balancer OceanAks#load_balancer}
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksLoadBalancer"]]], result)

    @builtins.property
    def managed_service_identity(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksManagedServiceIdentity"]]]:
        '''managed_service_identity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#managed_service_identity OceanAks#managed_service_identity}
        '''
        result = self._values.get("managed_service_identity")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksManagedServiceIdentity"]]], result)

    @builtins.property
    def max_pods(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#max_pods OceanAks#max_pods}.'''
        result = self._values.get("max_pods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network(self) -> typing.Optional["OceanAksNetwork"]:
        '''network block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#network OceanAks#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["OceanAksNetwork"], result)

    @builtins.property
    def os_disk(self) -> typing.Optional["OceanAksOsDisk"]:
        '''os_disk block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#os_disk OceanAks#os_disk}
        '''
        result = self._values.get("os_disk")
        return typing.cast(typing.Optional["OceanAksOsDisk"], result)

    @builtins.property
    def resource_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strategy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksStrategy"]]]:
        '''strategy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#strategy OceanAks#strategy}
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksStrategy"]]], result)

    @builtins.property
    def tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksTag"]]]:
        '''tag block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#tag OceanAks#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksTag"]]], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#user_name OceanAks#user_name}.'''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_sizes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVmSizes"]]]:
        '''vm_sizes block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#vm_sizes OceanAks#vm_sizes}
        '''
        result = self._values.get("vm_sizes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksVmSizes"]]], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#zones OceanAks#zones}.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksExtension",
    jsii_struct_bases=[],
    name_mapping={
        "api_version": "apiVersion",
        "minor_version_auto_upgrade": "minorVersionAutoUpgrade",
        "name": "name",
        "publisher": "publisher",
        "type": "type",
    },
)
class OceanAksExtension:
    def __init__(
        self,
        *,
        api_version: typing.Optional[builtins.str] = None,
        minor_version_auto_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#api_version OceanAks#api_version}.
        :param minor_version_auto_upgrade: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#minor_version_auto_upgrade OceanAks#minor_version_auto_upgrade}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.
        :param publisher: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#publisher OceanAks#publisher}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#type OceanAks#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b349a7066a07e042c329fd1e0d9b53393592752eeb0dd999ca798f1c4aeef2b)
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument minor_version_auto_upgrade", value=minor_version_auto_upgrade, expected_type=type_hints["minor_version_auto_upgrade"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_version is not None:
            self._values["api_version"] = api_version
        if minor_version_auto_upgrade is not None:
            self._values["minor_version_auto_upgrade"] = minor_version_auto_upgrade
        if name is not None:
            self._values["name"] = name
        if publisher is not None:
            self._values["publisher"] = publisher
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#api_version OceanAks#api_version}.'''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minor_version_auto_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#minor_version_auto_upgrade OceanAks#minor_version_auto_upgrade}.'''
        result = self._values.get("minor_version_auto_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#publisher OceanAks#publisher}.'''
        result = self._values.get("publisher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#type OceanAks#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksExtension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksExtensionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksExtensionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__658937e4dedc96fe11ad66d2cb815b98d1c8b5c43073be9650d387007b39094a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OceanAksExtensionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d18ad19ca49517e6b656f782348b28e1c711140772bb3e00124f73ceaa3416)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksExtensionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f4d27ca7f5a5c27665a1e7071b67169984dd12e58d438acf50ca15befab0be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7bc1affc82082990717a73413469189422941cdc0236f60babf3af871d0836e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd751c441c6e00a061e0aeda3033416e084ad93ac5296f0e5f64d6a1e19bad46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksExtension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksExtension]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksExtension]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b53a7a32536faa3cc3ed7fe66c91af8da7ec07ebf469717ed33edb082b49ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksExtensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksExtensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4c46dcdbbe1c8585260c293856614f4449bef076ef7dcf6d9c60790b8ec026b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetApiVersion")
    def reset_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiVersion", []))

    @jsii.member(jsii_name="resetMinorVersionAutoUpgrade")
    def reset_minor_version_auto_upgrade(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinorVersionAutoUpgrade", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPublisher")
    def reset_publisher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublisher", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="minorVersionAutoUpgradeInput")
    def minor_version_auto_upgrade_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "minorVersionAutoUpgradeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3c992720c3eccd3931ae9d9c6122b5f30df92d84becfd7edb69afa4f8fca6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value)

    @builtins.property
    @jsii.member(jsii_name="minorVersionAutoUpgrade")
    def minor_version_auto_upgrade(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "minorVersionAutoUpgrade"))

    @minor_version_auto_upgrade.setter
    def minor_version_auto_upgrade(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40f25cb96fd8737dfd963231df3f1aa47a704079d8edd0ff1a5e71ffdb9ee6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minorVersionAutoUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8116002b83000ce730b4e1c15258465a38e930addaa28d2fd5f2d1e74475e0d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e4014d1b52dd708a99a3f39bbd0327a2497aac535e6b2c33d451c1dbceab10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce1bc6a9876cca9e3cfd44d9c53ae9df5a22789c5e0308f8453a695f7b1a146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksExtension, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksExtension, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksExtension, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d99ec82cf6db78ba1befc6c920331eeb3215dd587a030999867a673558bfdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksHealth",
    jsii_struct_bases=[],
    name_mapping={"grace_period": "gracePeriod"},
)
class OceanAksHealth:
    def __init__(self, *, grace_period: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param grace_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#grace_period OceanAks#grace_period}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a30af99792eb483280c75356a57ce98953944ff2ccbe1317139b311b72e97127)
            check_type(argname="argument grace_period", value=grace_period, expected_type=type_hints["grace_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grace_period is not None:
            self._values["grace_period"] = grace_period

    @builtins.property
    def grace_period(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#grace_period OceanAks#grace_period}.'''
        result = self._values.get("grace_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksHealth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksHealthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksHealthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e99357f04f8929e2697d66499c2d7eec6436812df5e3baf118180288ce5228d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGracePeriod")
    def reset_grace_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGracePeriod", []))

    @builtins.property
    @jsii.member(jsii_name="gracePeriodInput")
    def grace_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gracePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="gracePeriod")
    def grace_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gracePeriod"))

    @grace_period.setter
    def grace_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c3c6d5e487e2c02933f83cf452a5fac3547c402dbe0eae1891f089f4e9a4da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gracePeriod", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksHealth]:
        return typing.cast(typing.Optional[OceanAksHealth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OceanAksHealth]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668c56b9843ede57c8f2f8952f2922ade1f2e45a1b676fd22b205c1d4198ae5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksImage",
    jsii_struct_bases=[],
    name_mapping={"marketplace": "marketplace"},
)
class OceanAksImage:
    def __init__(
        self,
        *,
        marketplace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksImageMarketplace", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param marketplace: marketplace block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#marketplace OceanAks#marketplace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544ed47651e52093b9015bcba3c724a9c4ce200fd01240a573faeae766d3181e)
            check_type(argname="argument marketplace", value=marketplace, expected_type=type_hints["marketplace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if marketplace is not None:
            self._values["marketplace"] = marketplace

    @builtins.property
    def marketplace(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksImageMarketplace"]]]:
        '''marketplace block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#marketplace OceanAks#marketplace}
        '''
        result = self._values.get("marketplace")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksImageMarketplace"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksImageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksImageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75a2295b1f979cd7fde50344a7cb5864ad2bd03e57633778a919eccc9307737a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OceanAksImageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867cbd55a1fc119cada1362ff313770973b78b810d9fc78b8330150cacf5958c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksImageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e625c026b85ba70da5b8bf3bce0f3ed388300170b01136bcec58d32d46b4d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec2780ec880ec3269153045228fb26056cde8d5862d1faf975a56fdbdda1c51f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c196527d4e4e032cc86bae963289220f001679c82a927c382918808ecbd6c23c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksImage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksImage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341ec0bcb66d1778ce2d8a347e13146839d81d0eead71798001d651f2ae2e60a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksImageMarketplace",
    jsii_struct_bases=[],
    name_mapping={
        "offer": "offer",
        "publisher": "publisher",
        "sku": "sku",
        "version": "version",
    },
)
class OceanAksImageMarketplace:
    def __init__(
        self,
        *,
        offer: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[builtins.str] = None,
        sku: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param offer: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#offer OceanAks#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#publisher OceanAks#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#sku OceanAks#sku}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#version OceanAks#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a28fd44ed7fa6886d568cda078b685f14bbf45087c286674115b842bd0948eb4)
            check_type(argname="argument offer", value=offer, expected_type=type_hints["offer"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if offer is not None:
            self._values["offer"] = offer
        if publisher is not None:
            self._values["publisher"] = publisher
        if sku is not None:
            self._values["sku"] = sku
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def offer(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#offer OceanAks#offer}.'''
        result = self._values.get("offer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#publisher OceanAks#publisher}.'''
        result = self._values.get("publisher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#sku OceanAks#sku}.'''
        result = self._values.get("sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#version OceanAks#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksImageMarketplace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksImageMarketplaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksImageMarketplaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5979b09ad1733674223768567cc1a3965b166762fa0ca0394eda5c3e41ea5120)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OceanAksImageMarketplaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf187fcacde8dc2b0f3568d4004c1c314bf776ba82a8ea96149f08a8e604dcb2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksImageMarketplaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd2f3cc1aca117615155b85d77abff5606403088735c5b1f8e05a5ca46b08cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__907314756833326167c32b10c45fe00a6f0631790e9a035d517866313b866f99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7972cf0ab807f54b2c5c87b83844082f6063496570ca85d779b194508629c30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksImageMarketplace]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksImageMarketplace]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksImageMarketplace]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2663a5dd251227a1bdc0de31d4f05f31522d8e63b7cd2a6cb8744f38b44e790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksImageMarketplaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksImageMarketplaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f3e696217f354b68d32397a3a8ab2378041e9d2133118d5560aeafb43b1b704)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOffer")
    def reset_offer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOffer", []))

    @jsii.member(jsii_name="resetPublisher")
    def reset_publisher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublisher", []))

    @jsii.member(jsii_name="resetSku")
    def reset_sku(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSku", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="offerInput")
    def offer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offerInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="offer")
    def offer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offer"))

    @offer.setter
    def offer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3fa6c608267eb63ec2ef136b42342bfaf9abb3ccc1fbcc57bddf600ec12f613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offer", value)

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcdaa9315d03914d2a46d1f24de4975555bc6f88e8819ec45a0a85d13930db33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value)

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__707e14d5049fb6d3c50873c5d8dac0c2100f7886909d41d583116aab94e9c545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efd6ddc6b02f93de1951051a2891f3795e2c370d896d719c18cc8c72e685b53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksImageMarketplace, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksImageMarketplace, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksImageMarketplace, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782d409f2bb122f45aab0cc297448d121395e701660aa65ff43a32790f0d6ef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16c74ebb924db40504ca97606fb7ac57d3a9781585b101b54f9d87b79a1aac53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMarketplace")
    def put_marketplace(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksImageMarketplace, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720bad18cac313d81fe2f0acf9706e24e2faeeb0c7ca2405d0dcfa3f2253c445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMarketplace", [value]))

    @jsii.member(jsii_name="resetMarketplace")
    def reset_marketplace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketplace", []))

    @builtins.property
    @jsii.member(jsii_name="marketplace")
    def marketplace(self) -> OceanAksImageMarketplaceList:
        return typing.cast(OceanAksImageMarketplaceList, jsii.get(self, "marketplace"))

    @builtins.property
    @jsii.member(jsii_name="marketplaceInput")
    def marketplace_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksImageMarketplace]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksImageMarketplace]]], jsii.get(self, "marketplaceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksImage, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksImage, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksImage, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb20d2642d66e8dd33abc5a706d9f20f78c3ad4609fbe5e2fc6e9b7b44269ea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "backend_pool_names": "backendPoolNames",
        "load_balancer_sku": "loadBalancerSku",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "type": "type",
    },
)
class OceanAksLoadBalancer:
    def __init__(
        self,
        *,
        backend_pool_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        load_balancer_sku: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backend_pool_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#backend_pool_names OceanAks#backend_pool_names}.
        :param load_balancer_sku: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#load_balancer_sku OceanAks#load_balancer_sku}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#type OceanAks#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30268f77d6ac6b45e799dcf6888208ad9bb291a71c16efd736441c4e0e67183a)
            check_type(argname="argument backend_pool_names", value=backend_pool_names, expected_type=type_hints["backend_pool_names"])
            check_type(argname="argument load_balancer_sku", value=load_balancer_sku, expected_type=type_hints["load_balancer_sku"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backend_pool_names is not None:
            self._values["backend_pool_names"] = backend_pool_names
        if load_balancer_sku is not None:
            self._values["load_balancer_sku"] = load_balancer_sku
        if name is not None:
            self._values["name"] = name
        if resource_group_name is not None:
            self._values["resource_group_name"] = resource_group_name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def backend_pool_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#backend_pool_names OceanAks#backend_pool_names}.'''
        result = self._values.get("backend_pool_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def load_balancer_sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#load_balancer_sku OceanAks#load_balancer_sku}.'''
        result = self._values.get("load_balancer_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#type OceanAks#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksLoadBalancerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksLoadBalancerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7582a00905b28c75fb1349ea2263904880547f04e855f6e896282ec3a90972b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OceanAksLoadBalancerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed2542d849bae884fb68a85996349b7f71250e40b336280ff19c4533ad38dad)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksLoadBalancerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5605ecf9953edf3d113e7a2c45414399114d440bf696621f8b170a0dcd6f7c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__980420fd5f154a627f680c55bd228d6fb4ca4764134042dee99c99f8cd7cc2fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2867ca95031c8a617cfc3e2ac1b93584ccdd27eb92d4141cc09520c09f520e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksLoadBalancer]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksLoadBalancer]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksLoadBalancer]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f4bc0a790cde6028e2da14c3bb321dfed9dd7cc2f2de3ce919f9ee3b623294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksLoadBalancerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb142fc846366619ad45a2a1c9ef8f37cfd4230dc6ba33da6b33c068ced2e371)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBackendPoolNames")
    def reset_backend_pool_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendPoolNames", []))

    @jsii.member(jsii_name="resetLoadBalancerSku")
    def reset_load_balancer_sku(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerSku", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetResourceGroupName")
    def reset_resource_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroupName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="backendPoolNamesInput")
    def backend_pool_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "backendPoolNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerSkuInput")
    def load_balancer_sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerSkuInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="backendPoolNames")
    def backend_pool_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backendPoolNames"))

    @backend_pool_names.setter
    def backend_pool_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8dcaf2ece1f23a3edd421d20612a5f8045e1ebeba9377476761afeff5ccc314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backendPoolNames", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerSku")
    def load_balancer_sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerSku"))

    @load_balancer_sku.setter
    def load_balancer_sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c6689cb2332c45a9690188b9b46f82bdd3aef8826cee52785fd770338dc81f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerSku", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62ee2d62bcbf785c4f78f856f99b250271aebe49fab46caffbbb39f1f6dbf4ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c8eceb4cdaefaafa4fe9a8f7b408b06162c4471b2493f859666c89001ca558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b4e769589632ad4c35b691b7bccd2bce53237384f06c7c17191b15915919e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksLoadBalancer, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksLoadBalancer, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksLoadBalancer, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d826fa36e5d99b7296f72c133e260877d9e6ace3b6d567b1be10b9937c19dce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksManagedServiceIdentity",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "resource_group_name": "resourceGroupName"},
)
class OceanAksManagedServiceIdentity:
    def __init__(
        self,
        *,
        name: builtins.str,
        resource_group_name: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cda664452e2f5cf168e1f2220f417f97f8e62a61f1996112acf516ddee0c754)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource_group_name": resource_group_name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksManagedServiceIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksManagedServiceIdentityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksManagedServiceIdentityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__798904b182dfa808282e77fda16af7d98af4298a2f0a9402b8a5e91c0f9c8cd3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OceanAksManagedServiceIdentityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6087feda6471ce81d00cc8a19ecac7e2e0c8554892edb8dbac998ae5398c3d47)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksManagedServiceIdentityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f81a0e9f0290394c7afdcf15426f28403224cb1b57c6fb10c2e9227ea7b2b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2aa83ee39ec89de65fc7c0713ad0590fd6f34614388bf566743dc747119afa4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9214911f47631ccb7fd4bde1f5cd43152549e0980ef36972ba1080a7a06e677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksManagedServiceIdentity]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksManagedServiceIdentity]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksManagedServiceIdentity]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0427a45077772cab741e74a516f4d1adc7c28942025290d8bc8db7e69a5239c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksManagedServiceIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksManagedServiceIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__befffe5eeacb2aa2d2797a9731844edea4a35537a5951abf0ca5fbb116bc29a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7384eb5d9cd14703b49fae863de4ce51f5e0284c2ab7d2878aac21a9fcffd39f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71cc8ec627d6acc4038305b4a5e00ca158cdd88a5f857cefa8334e2428acd9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksManagedServiceIdentity, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksManagedServiceIdentity, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksManagedServiceIdentity, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e81136fcc2393199cc7343a271f0a71983a17f66bc9c3c65c2161d730ad375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "network_interface": "networkInterface",
        "resource_group_name": "resourceGroupName",
        "virtual_network_name": "virtualNetworkName",
    },
)
class OceanAksNetwork:
    def __init__(
        self,
        *,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksNetworkNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
        virtual_network_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#network_interface OceanAks#network_interface}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.
        :param virtual_network_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#virtual_network_name OceanAks#virtual_network_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44055b0100d00c2e1efa96c49cfb80eaf68e1c7056a35bb6cb7474b37c11bae7)
            check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument virtual_network_name", value=virtual_network_name, expected_type=type_hints["virtual_network_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network_interface is not None:
            self._values["network_interface"] = network_interface
        if resource_group_name is not None:
            self._values["resource_group_name"] = resource_group_name
        if virtual_network_name is not None:
            self._values["virtual_network_name"] = virtual_network_name

    @builtins.property
    def network_interface(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNetworkNetworkInterface"]]]:
        '''network_interface block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#network_interface OceanAks#network_interface}
        '''
        result = self._values.get("network_interface")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNetworkNetworkInterface"]]], result)

    @builtins.property
    def resource_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#virtual_network_name OceanAks#virtual_network_name}.'''
        result = self._values.get("virtual_network_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksNetworkNetworkInterface",
    jsii_struct_bases=[],
    name_mapping={
        "additional_ip_config": "additionalIpConfig",
        "assign_public_ip": "assignPublicIp",
        "is_primary": "isPrimary",
        "security_group": "securityGroup",
        "subnet_name": "subnetName",
    },
)
class OceanAksNetworkNetworkInterface:
    def __init__(
        self,
        *,
        additional_ip_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksNetworkNetworkInterfaceAdditionalIpConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        assign_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_group: typing.Optional[typing.Union["OceanAksNetworkNetworkInterfaceSecurityGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        subnet_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_ip_config: additional_ip_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#additional_ip_config OceanAks#additional_ip_config}
        :param assign_public_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#assign_public_ip OceanAks#assign_public_ip}.
        :param is_primary: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#is_primary OceanAks#is_primary}.
        :param security_group: security_group block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#security_group OceanAks#security_group}
        :param subnet_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#subnet_name OceanAks#subnet_name}.
        '''
        if isinstance(security_group, dict):
            security_group = OceanAksNetworkNetworkInterfaceSecurityGroup(**security_group)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d469f156b97c924871c2ac85472a6b275e050832d997b9197b2a59c5e50dd50a)
            check_type(argname="argument additional_ip_config", value=additional_ip_config, expected_type=type_hints["additional_ip_config"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument is_primary", value=is_primary, expected_type=type_hints["is_primary"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument subnet_name", value=subnet_name, expected_type=type_hints["subnet_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_ip_config is not None:
            self._values["additional_ip_config"] = additional_ip_config
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if is_primary is not None:
            self._values["is_primary"] = is_primary
        if security_group is not None:
            self._values["security_group"] = security_group
        if subnet_name is not None:
            self._values["subnet_name"] = subnet_name

    @builtins.property
    def additional_ip_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNetworkNetworkInterfaceAdditionalIpConfig"]]]:
        '''additional_ip_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#additional_ip_config OceanAks#additional_ip_config}
        '''
        result = self._values.get("additional_ip_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNetworkNetworkInterfaceAdditionalIpConfig"]]], result)

    @builtins.property
    def assign_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#assign_public_ip OceanAks#assign_public_ip}.'''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_primary(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#is_primary OceanAks#is_primary}.'''
        result = self._values.get("is_primary")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional["OceanAksNetworkNetworkInterfaceSecurityGroup"]:
        '''security_group block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#security_group OceanAks#security_group}
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional["OceanAksNetworkNetworkInterfaceSecurityGroup"], result)

    @builtins.property
    def subnet_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#subnet_name OceanAks#subnet_name}.'''
        result = self._values.get("subnet_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNetworkNetworkInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksNetworkNetworkInterfaceAdditionalIpConfig",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "private_ip_version": "privateIpVersion"},
)
class OceanAksNetworkNetworkInterfaceAdditionalIpConfig:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        private_ip_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.
        :param private_ip_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#private_ip_version OceanAks#private_ip_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186fe969342aeee27c4b73796ade96c1f3e7e0bdcbbaa6c4afef5b8ca31cd8f6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument private_ip_version", value=private_ip_version, expected_type=type_hints["private_ip_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if private_ip_version is not None:
            self._values["private_ip_version"] = private_ip_version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#private_ip_version OceanAks#private_ip_version}.'''
        result = self._values.get("private_ip_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNetworkNetworkInterfaceAdditionalIpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksNetworkNetworkInterfaceAdditionalIpConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksNetworkNetworkInterfaceAdditionalIpConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__519f3a83146bf4eab02cff3116011d36e964343474a8f3c1b41dec4ce8b8bb2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OceanAksNetworkNetworkInterfaceAdditionalIpConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1215fd5996e7d6ca6c647be2a6204c7a1c69bd7f94779f51f000d18c28516918)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksNetworkNetworkInterfaceAdditionalIpConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31a428c235c229dfb26f3f742bd121cc90dcf08d8e96ef387c438e463fef7722)
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
            type_hints = typing.get_type_hints(_typecheckingstub__073a31928ec33b75fd4ec33e1cd2553d56dc87615af77777efd0a5603aec2122)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ac0d5a32075001b13bad4b53917efdb494a15e684afc8a05e8134de9ff8e8c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterfaceAdditionalIpConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterfaceAdditionalIpConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterfaceAdditionalIpConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96a20b90a02598bd8333c3c45a01c3c5a3c2d6ea06e2154a65dc9aa1d077faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksNetworkNetworkInterfaceAdditionalIpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksNetworkNetworkInterfaceAdditionalIpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7720557a5761941f25047f41906be5630a9d0ca6f31aac9827c9e413361099b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPrivateIpVersion")
    def reset_private_ip_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpVersion", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpVersionInput")
    def private_ip_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddff0ac789a8018b654bb1e0d3f72e8ccb04c36fc9eed326be067e96fad549f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="privateIpVersion")
    def private_ip_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpVersion"))

    @private_ip_version.setter
    def private_ip_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a12e5b7349f455db4d2ee727a7c3c97570d9a9ed2916d3204ceb13de2912ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpVersion", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksNetworkNetworkInterfaceAdditionalIpConfig, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksNetworkNetworkInterfaceAdditionalIpConfig, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksNetworkNetworkInterfaceAdditionalIpConfig, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd54f1a6564cecd58bb9a68b3667610f9f2d301a49388a93e14ead25946010e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksNetworkNetworkInterfaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksNetworkNetworkInterfaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__980abf17a662b0a879443d3712140fc47c427ab41db579fec04638fea1198e56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OceanAksNetworkNetworkInterfaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b334c4bb233ca606b7a19d9c89d3b76380768046f86f3aff26bdea3f8525b54f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksNetworkNetworkInterfaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a78c79d4a23c492f12204186aeba83c7cacf45e358ee8339e8cd32fb3b00873)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddcc2e69c7f0720f65c9e073f666f5180c90cdd6706ebe49e817a1da7deb939c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c82b24042e0a40224d3b2fc1518cd895acd30f6f56bea8aa9d7e5b65c69f999f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterface]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterface]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterface]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a90b0f995208c7b6300370c146de4e6fe95ff967462065a8c461149e79add1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksNetworkNetworkInterfaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksNetworkNetworkInterfaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e62bbd522a6c6524339da6df55bf1f84596f7e9785f0775516c276200859ed5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAdditionalIpConfig")
    def put_additional_ip_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNetworkNetworkInterfaceAdditionalIpConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d03abb7461ac22a6d9c496f3a211d131eb5f9aefefe1601675c0e935d821de51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalIpConfig", [value]))

    @jsii.member(jsii_name="putSecurityGroup")
    def put_security_group(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.
        '''
        value = OceanAksNetworkNetworkInterfaceSecurityGroup(
            name=name, resource_group_name=resource_group_name
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityGroup", [value]))

    @jsii.member(jsii_name="resetAdditionalIpConfig")
    def reset_additional_ip_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalIpConfig", []))

    @jsii.member(jsii_name="resetAssignPublicIp")
    def reset_assign_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssignPublicIp", []))

    @jsii.member(jsii_name="resetIsPrimary")
    def reset_is_primary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsPrimary", []))

    @jsii.member(jsii_name="resetSecurityGroup")
    def reset_security_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroup", []))

    @jsii.member(jsii_name="resetSubnetName")
    def reset_subnet_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetName", []))

    @builtins.property
    @jsii.member(jsii_name="additionalIpConfig")
    def additional_ip_config(
        self,
    ) -> OceanAksNetworkNetworkInterfaceAdditionalIpConfigList:
        return typing.cast(OceanAksNetworkNetworkInterfaceAdditionalIpConfigList, jsii.get(self, "additionalIpConfig"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(
        self,
    ) -> "OceanAksNetworkNetworkInterfaceSecurityGroupOutputReference":
        return typing.cast("OceanAksNetworkNetworkInterfaceSecurityGroupOutputReference", jsii.get(self, "securityGroup"))

    @builtins.property
    @jsii.member(jsii_name="additionalIpConfigInput")
    def additional_ip_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterfaceAdditionalIpConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterfaceAdditionalIpConfig]]], jsii.get(self, "additionalIpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="assignPublicIpInput")
    def assign_public_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "assignPublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="isPrimaryInput")
    def is_primary_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isPrimaryInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupInput")
    def security_group_input(
        self,
    ) -> typing.Optional["OceanAksNetworkNetworkInterfaceSecurityGroup"]:
        return typing.cast(typing.Optional["OceanAksNetworkNetworkInterfaceSecurityGroup"], jsii.get(self, "securityGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetNameInput")
    def subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "assignPublicIp"))

    @assign_public_ip.setter
    def assign_public_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9304585881ae6f3aaf632a15ac55f8e570d15cf8638e167b6b017d8ab8650f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assignPublicIp", value)

    @builtins.property
    @jsii.member(jsii_name="isPrimary")
    def is_primary(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isPrimary"))

    @is_primary.setter
    def is_primary(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe8c4c1c9627af9a60d5583bacbbda54f32c7b800e90439b6b20d0f19963251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPrimary", value)

    @builtins.property
    @jsii.member(jsii_name="subnetName")
    def subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetName"))

    @subnet_name.setter
    def subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95a5ca9e94e1917225ecdf0a2a0e06e6cf7f8806934e0b5abe0d2def7d3512b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksNetworkNetworkInterface, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksNetworkNetworkInterface, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksNetworkNetworkInterface, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f695b4a26160523e8de55743e2db29a5fada766b45450607bfa92c031595a72d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksNetworkNetworkInterfaceSecurityGroup",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "resource_group_name": "resourceGroupName"},
)
class OceanAksNetworkNetworkInterfaceSecurityGroup:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        resource_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf3410b5030b0dda2d8bdbf93051180bf267667db4e2f48b01e50abc50b0e5a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if resource_group_name is not None:
            self._values["resource_group_name"] = resource_group_name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#name OceanAks#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#resource_group_name OceanAks#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNetworkNetworkInterfaceSecurityGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksNetworkNetworkInterfaceSecurityGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksNetworkNetworkInterfaceSecurityGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec2f890013d9cf54d4948f37a1d16f109aec96056ddffbe501bc5c613c99ccf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetResourceGroupName")
    def reset_resource_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroupName", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a0b476bfdb7ea765c5119d3f690349c722752fa47ce39e65f174bbef93c4c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14eec666b2a11cc8d7dd56e00e3d6e365d8b9377f297eedcb7c88be28c85d038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OceanAksNetworkNetworkInterfaceSecurityGroup]:
        return typing.cast(typing.Optional[OceanAksNetworkNetworkInterfaceSecurityGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OceanAksNetworkNetworkInterfaceSecurityGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f55dcf49f35abf38636df8bd13556b6d5d693a3459d0b1e045f67148719bd611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b0959abbb880fee044efd1b5cf41a5aa5dddb1498364d61c01e911d9b7338a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworkInterface")
    def put_network_interface(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNetworkNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56bb1e056cc9319975c4935007d758e179e01910d4f6d77581431d3e008d1a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterface", [value]))

    @jsii.member(jsii_name="resetNetworkInterface")
    def reset_network_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterface", []))

    @jsii.member(jsii_name="resetResourceGroupName")
    def reset_resource_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroupName", []))

    @jsii.member(jsii_name="resetVirtualNetworkName")
    def reset_virtual_network_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkName", []))

    @builtins.property
    @jsii.member(jsii_name="networkInterface")
    def network_interface(self) -> OceanAksNetworkNetworkInterfaceList:
        return typing.cast(OceanAksNetworkNetworkInterfaceList, jsii.get(self, "networkInterface"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceInput")
    def network_interface_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterface]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterface]]], jsii.get(self, "networkInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkNameInput")
    def virtual_network_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1872ae898b799212065f80316b5fceca0e3eeee1eb42f01731a7896317ec3f39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkName")
    def virtual_network_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkName"))

    @virtual_network_name.setter
    def virtual_network_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317e3ef187b8fb3bf38d14cab305852e9e7f970d58fdcb737e6b816110c775cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksNetwork]:
        return typing.cast(typing.Optional[OceanAksNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OceanAksNetwork]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd4034a016efd05b5d7cd8e3c69972d72ac4fef291bdb32614d1e613943cee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksOsDisk",
    jsii_struct_bases=[],
    name_mapping={"size_gb": "sizeGb", "type": "type"},
)
class OceanAksOsDisk:
    def __init__(
        self,
        *,
        size_gb: jsii.Number,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#size_gb OceanAks#size_gb}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#type OceanAks#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a768facb3e7b071b3f5efcf7dbfda65e61426ffc96a4afccd8b9fb36f5992cc)
            check_type(argname="argument size_gb", value=size_gb, expected_type=type_hints["size_gb"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "size_gb": size_gb,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def size_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#size_gb OceanAks#size_gb}.'''
        result = self._values.get("size_gb")
        assert result is not None, "Required property 'size_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#type OceanAks#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksOsDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksOsDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksOsDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__816ffb48616c934e754fecf68270295616da3ae825ec35c312a715caf91b6b66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="sizeGbInput")
    def size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeGb")
    def size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGb"))

    @size_gb.setter
    def size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78aa7d7fe69aa8d3d5430b4a870b0288789a0a5d28c65f82082d86120972d441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGb", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6aed9a34c152701afae7c62aca6ddfcc4dfb3f65241349097a0169aed3ecaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksOsDisk]:
        return typing.cast(typing.Optional[OceanAksOsDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OceanAksOsDisk]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be843cf0458ee3f37ca48ef75480671209f1cd9c9246bb3a1bae681283f34e54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "fallback_to_ondemand": "fallbackToOndemand",
        "spot_percentage": "spotPercentage",
    },
)
class OceanAksStrategy:
    def __init__(
        self,
        *,
        fallback_to_ondemand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        spot_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fallback_to_ondemand: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#fallback_to_ondemand OceanAks#fallback_to_ondemand}.
        :param spot_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#spot_percentage OceanAks#spot_percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd6fc7fa77133e8667d3343f36c1234f34c2afbfc1d391c3aae25ed5f973489)
            check_type(argname="argument fallback_to_ondemand", value=fallback_to_ondemand, expected_type=type_hints["fallback_to_ondemand"])
            check_type(argname="argument spot_percentage", value=spot_percentage, expected_type=type_hints["spot_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fallback_to_ondemand is not None:
            self._values["fallback_to_ondemand"] = fallback_to_ondemand
        if spot_percentage is not None:
            self._values["spot_percentage"] = spot_percentage

    @builtins.property
    def fallback_to_ondemand(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#fallback_to_ondemand OceanAks#fallback_to_ondemand}.'''
        result = self._values.get("fallback_to_ondemand")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def spot_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#spot_percentage OceanAks#spot_percentage}.'''
        result = self._values.get("spot_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksStrategyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksStrategyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5455af57d553c11ebfc95141c1a2be4ab8ff17467ee2350efae6c46cafbb2c20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OceanAksStrategyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4adfd895844508ad6b2eaf1efb74bb6839f1a7526a6271e678922a4aa4b4dd6a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksStrategyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62cbbc645fc9d2dd511eaf3a737f9ad02133d1edff2413a5ac70497bc8dea2b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2282b319a3e73a54044ebd6c0be0334ac8a71dacbbf0fd6358a8a823018cfafc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fdf5dd61e9e52f465ec24ebb7227e8301145951a781cf0b325d52370da02df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksStrategy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksStrategy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306de7a07401b322c03c11370eb243e475c7fe0b619b0cb4a29676d32fcb6815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6660cd9cb2b6f6f1a1a12cf2583ca6993bd2648061005ec474eccb1676d63ba9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFallbackToOndemand")
    def reset_fallback_to_ondemand(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFallbackToOndemand", []))

    @jsii.member(jsii_name="resetSpotPercentage")
    def reset_spot_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpotPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="fallbackToOndemandInput")
    def fallback_to_ondemand_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fallbackToOndemandInput"))

    @builtins.property
    @jsii.member(jsii_name="spotPercentageInput")
    def spot_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="fallbackToOndemand")
    def fallback_to_ondemand(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fallbackToOndemand"))

    @fallback_to_ondemand.setter
    def fallback_to_ondemand(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a231cd04076914b3fe107fb0b8c1d0c2c09234d649ad87aeebf4f4fefbbf116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fallbackToOndemand", value)

    @builtins.property
    @jsii.member(jsii_name="spotPercentage")
    def spot_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "spotPercentage"))

    @spot_percentage.setter
    def spot_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae3a7e932669b0926992ee65177edbf46d3de20efae6d79ac0a0fb5179d12cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spotPercentage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksStrategy, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksStrategy, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksStrategy, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503e22157f80912e5603fc330f6dad8f0f346625defe5ce829c00b6d646e8c6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class OceanAksTag:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#key OceanAks#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#value OceanAks#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173a0a90bdbb68c71d90c1c950bbfac5e720c6fb5c4b16b85ca6f4721dbf7e0c)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#key OceanAks#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#value OceanAks#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0218ccf96fcb158e3ea05c177a346bf26c499764c5d296c86f4375ccfa272660)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OceanAksTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ce67cad8dc22b210868f802412b7ea22a7dbf2c8df17a56f4cf2dd046562a9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b689c58727329fabea1757de4d5fcd29a82f28732510524940d95404dbd67a81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fad1545da5ab38682b9eb895f43d3392681f067b371809284075d22b64d65aa0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11b14bcacbf70aa06c3f656c9ccf671d04a29e82c804a0a94f6ed8c34b8aaeff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b859558575e533cff68f2c68ea3d2fad39bd1a250c27189cf97e531fa11e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4f097d6118daab00509b58426062cb7d7855b704e1e23674668b390f05dac2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d71bbce48839b3ee9098e07df03c73b08f057699276ed42d3d040d7898086cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49a531290835b81fb0a47f3744ced9b1c56ac226156fb29217e1590a687b144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksTag, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksTag, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksTag, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c18d32595f8ceb8ed938c4c2cef191661af3a21c192e2f97b93985ed4717ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksVmSizes",
    jsii_struct_bases=[],
    name_mapping={"whitelist": "whitelist"},
)
class OceanAksVmSizes:
    def __init__(
        self,
        *,
        whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param whitelist: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#whitelist OceanAks#whitelist}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bafa40c378cb3e2a63ed918cda17229a737882fd57cde5ef080413d834c59892)
            check_type(argname="argument whitelist", value=whitelist, expected_type=type_hints["whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if whitelist is not None:
            self._values["whitelist"] = whitelist

    @builtins.property
    def whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/ocean_aks#whitelist OceanAks#whitelist}.'''
        result = self._values.get("whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksVmSizes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksVmSizesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksVmSizesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acd8cb897bf076ec10a21b1b27ad55c3baaeb72015852a247bd86e8dca36882a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OceanAksVmSizesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd1a86f770714da229cc6fceb7e1f1c8c46aac1c7b2236c58771dc1be40fdc7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksVmSizesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a85bacee1c1c90a6f11090aad5a8af767703c1b57151c18fbba0e8abe3d86776)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56b062da65d93f265281fe657cf551652b803b6599f74ec39e44b70b46d556fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ebf3102adcf1115d4ffe3635a91a29410be3345cb3dcc719b01bffb0aad2ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVmSizes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVmSizes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVmSizes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9b1b05f70f7e7fdf85d6ea178af0379456433799a51164073ab19d8f20ed6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksVmSizesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAks.OceanAksVmSizesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e412483ca4a8cc1258f0f9ccc764db4041918746a5db6715e5bebdbb9f4c889)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetWhitelist")
    def reset_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhitelist", []))

    @builtins.property
    @jsii.member(jsii_name="whitelistInput")
    def whitelist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "whitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="whitelist")
    def whitelist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "whitelist"))

    @whitelist.setter
    def whitelist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91cec6dacd94ebc69de81d853a4355b7d1cf787cea0cb8872ecad5ad9fe1c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "whitelist", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OceanAksVmSizes, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OceanAksVmSizes, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OceanAksVmSizes, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748bf37ea12647c497e4e496da60d51241cf52f96e961ea0ec73c868a4e059a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OceanAks",
    "OceanAksAutoscaler",
    "OceanAksAutoscalerAutoscaleDown",
    "OceanAksAutoscalerAutoscaleDownOutputReference",
    "OceanAksAutoscalerAutoscaleHeadroom",
    "OceanAksAutoscalerAutoscaleHeadroomAutomatic",
    "OceanAksAutoscalerAutoscaleHeadroomAutomaticOutputReference",
    "OceanAksAutoscalerAutoscaleHeadroomOutputReference",
    "OceanAksAutoscalerOutputReference",
    "OceanAksAutoscalerResourceLimits",
    "OceanAksAutoscalerResourceLimitsOutputReference",
    "OceanAksConfig",
    "OceanAksExtension",
    "OceanAksExtensionList",
    "OceanAksExtensionOutputReference",
    "OceanAksHealth",
    "OceanAksHealthOutputReference",
    "OceanAksImage",
    "OceanAksImageList",
    "OceanAksImageMarketplace",
    "OceanAksImageMarketplaceList",
    "OceanAksImageMarketplaceOutputReference",
    "OceanAksImageOutputReference",
    "OceanAksLoadBalancer",
    "OceanAksLoadBalancerList",
    "OceanAksLoadBalancerOutputReference",
    "OceanAksManagedServiceIdentity",
    "OceanAksManagedServiceIdentityList",
    "OceanAksManagedServiceIdentityOutputReference",
    "OceanAksNetwork",
    "OceanAksNetworkNetworkInterface",
    "OceanAksNetworkNetworkInterfaceAdditionalIpConfig",
    "OceanAksNetworkNetworkInterfaceAdditionalIpConfigList",
    "OceanAksNetworkNetworkInterfaceAdditionalIpConfigOutputReference",
    "OceanAksNetworkNetworkInterfaceList",
    "OceanAksNetworkNetworkInterfaceOutputReference",
    "OceanAksNetworkNetworkInterfaceSecurityGroup",
    "OceanAksNetworkNetworkInterfaceSecurityGroupOutputReference",
    "OceanAksNetworkOutputReference",
    "OceanAksOsDisk",
    "OceanAksOsDiskOutputReference",
    "OceanAksStrategy",
    "OceanAksStrategyList",
    "OceanAksStrategyOutputReference",
    "OceanAksTag",
    "OceanAksTagList",
    "OceanAksTagOutputReference",
    "OceanAksVmSizes",
    "OceanAksVmSizesList",
    "OceanAksVmSizesOutputReference",
]

publication.publish()

def _typecheckingstub__76dcc528340cfbc5cca9e89b16b8271c4996e77e60921ec340ac55db950aaf04(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    acd_identifier: builtins.str,
    aks_name: builtins.str,
    aks_resource_group_name: builtins.str,
    name: builtins.str,
    ssh_public_key: builtins.str,
    autoscaler: typing.Optional[typing.Union[OceanAksAutoscaler, typing.Dict[builtins.str, typing.Any]]] = None,
    controller_cluster_id: typing.Optional[builtins.str] = None,
    custom_data: typing.Optional[builtins.str] = None,
    extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksExtension, typing.Dict[builtins.str, typing.Any]]]]] = None,
    health: typing.Optional[typing.Union[OceanAksHealth, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    load_balancer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksLoadBalancer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    managed_service_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksManagedServiceIdentity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_pods: typing.Optional[jsii.Number] = None,
    network: typing.Optional[typing.Union[OceanAksNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    os_disk: typing.Optional[typing.Union[OceanAksOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_group_name: typing.Optional[builtins.str] = None,
    strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    user_name: typing.Optional[builtins.str] = None,
    vm_sizes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVmSizes, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__10a02531c6ad233b7264dfa86eb3cf920cb3dadb6aa98a733284c81c2445fbd6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksExtension, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa34202c53b38a7ff90efb53633e90a444814300c6f96fec63c2c0b78e62625(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksImage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a31d5081b16e33595ce816655e9d039c1aa807785bffb114059ca324c3e87b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksLoadBalancer, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe720d0dd31b8952f40e403c612e611d8d4c15bdb11aafa3b67e018abbab6315(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksManagedServiceIdentity, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2574893f221ea86cdb716dee13b16460bc95a494d3c6df60d83c6fcbb5cf5cb1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksStrategy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0723469680dffa85731de3b1f1b0f21c97d0c2eabe68a53aa42f9b020087f231(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c5b9244b429b69e88ecc45ced4dbbf92a4bbe747594875c2a6532e549b89d9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVmSizes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0749d54685748f661a65031407c5f7cdbf348c4a63dd40970db7998427b716e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d66b1d2f8bbf95599c4267f09058671ad282196a1da37be24ed5ce752b4be49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519dc9ea47002faee8b55a8aa52f55383f4335f0dc9ee236fe5bd6f6e7749403(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f62b8d54fd3df01a98a254487c8302fdb271a08c21aa3976044a4501baf314(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d5c635eebdec057515284cff2aebd15c84cf08538ff5fcadbcb5de019942ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ac62b5e9b72f1c9980992c67eccebdf954e5efcab4e868d5486fd3b3d4b7fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d15d8def1b925a9ddb4e403c4653416ec63b2456b828016e3e8b69d037a5178(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f196455de045afa3b3a9447c729ed6c3b569072985815ca41b339cb506ed812(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe6f464a37b47b11504678caf48ef31d4de6fe292a4dafe35c245b876849bff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7085c72a347909b11b985573f3d11747fb915ed19811e6fb411df54b88aebc4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa36021afb1de2ff4ab8016f119621d166530615d7f9cf3fd5025d373b7ea3fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a6ac7c9193d3b24cfd89baffa315db5bdadfb358f550ff2689712f03343951(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae822831bee781a374a763b68a5a8439d3d48d7dfc1b85784531bed9f8c206b(
    *,
    autoscale_down: typing.Optional[typing.Union[OceanAksAutoscalerAutoscaleDown, typing.Dict[builtins.str, typing.Any]]] = None,
    autoscale_headroom: typing.Optional[typing.Union[OceanAksAutoscalerAutoscaleHeadroom, typing.Dict[builtins.str, typing.Any]]] = None,
    autoscale_is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource_limits: typing.Optional[typing.Union[OceanAksAutoscalerResourceLimits, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95862ab1c6ba5f4dff0e85ce26dffc21976ecdd643d2db433f63d4fb25403fc(
    *,
    max_scale_down_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf6ead3071f846336543f10a88132b736759f20fb62342a64c0281afff72f81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b89839b3eec125f1afde6b3facf896bd82bb2b39b489b370f9a49c87f01e58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec44787765eb73e5c15daa1be97e6019eecbb068ee5c853a7034862393727dd(
    value: typing.Optional[OceanAksAutoscalerAutoscaleDown],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e826edea17a771b623e2fd2abe0cd591a4035539838944d0f5860322f14a47(
    *,
    automatic: typing.Optional[typing.Union[OceanAksAutoscalerAutoscaleHeadroomAutomatic, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178888b53fdc75c5e2efa6e51a6604f6a0ffcdec1c03c413b23d6793dd388142(
    *,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07948dc79ed296808a0fe05217142963b0745b248d04d00d633f6bcef6f94c95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b399759c6fc1e474558ebb9be3748bf4f572790e2f8f3f36cca6e796abdeaf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea3c8977174eb2982a86e09dc58b2b9385cfc34826e3c6e12edc540f12ea0b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9958c8102a10db8affb251d25918ff3157ade54f522ce3c005ea5abafdec8f4(
    value: typing.Optional[OceanAksAutoscalerAutoscaleHeadroomAutomatic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b94a4ccb3f31b11f453084335f36e14222f91161c528a493906b644c8debd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d278692cb611daef7b76fa93355ab1868b4c9f36e875b32d7b7264a1e7aedd0f(
    value: typing.Optional[OceanAksAutoscalerAutoscaleHeadroom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2aaae37025d03e48afe15f04b26270a86d1762a8325f627b19cd4f1c1342546(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaaeb22e91b0020d415fd482c54db243c55ea1e17ab5fe79cc8dd9828d41a78b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793d85455930197670ce5cceb53594184e80a211c31ce1d2d805e561026548e5(
    value: typing.Optional[OceanAksAutoscaler],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1dee30275acf5b87d2d4accf9272f6a27a0bfd73a3c989de54eb74412313b27(
    *,
    max_memory_gib: typing.Optional[jsii.Number] = None,
    max_vcpu: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36601e4f410fc21caffc0bb17991a3a0056fb323a736749f44a713a478924e36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646cec1bdc6a0faa7f372d5b70dcbb709c0471937a9c7c7847dc104e2fe83536(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f0597fa39fdd7c92e20901881e41721bae62cc09d348f9b64a1f78e04719f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325fda81c706f6a202d6cce330ac6cd4d10fc4622b59892e4fa65492e064b329(
    value: typing.Optional[OceanAksAutoscalerResourceLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6214905b248239e1ae616041c358f12c757235005dcbf7db8285871cbc0d918(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    acd_identifier: builtins.str,
    aks_name: builtins.str,
    aks_resource_group_name: builtins.str,
    name: builtins.str,
    ssh_public_key: builtins.str,
    autoscaler: typing.Optional[typing.Union[OceanAksAutoscaler, typing.Dict[builtins.str, typing.Any]]] = None,
    controller_cluster_id: typing.Optional[builtins.str] = None,
    custom_data: typing.Optional[builtins.str] = None,
    extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksExtension, typing.Dict[builtins.str, typing.Any]]]]] = None,
    health: typing.Optional[typing.Union[OceanAksHealth, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    load_balancer: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksLoadBalancer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    managed_service_identity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksManagedServiceIdentity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_pods: typing.Optional[jsii.Number] = None,
    network: typing.Optional[typing.Union[OceanAksNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    os_disk: typing.Optional[typing.Union[OceanAksOsDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_group_name: typing.Optional[builtins.str] = None,
    strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    user_name: typing.Optional[builtins.str] = None,
    vm_sizes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksVmSizes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b349a7066a07e042c329fd1e0d9b53393592752eeb0dd999ca798f1c4aeef2b(
    *,
    api_version: typing.Optional[builtins.str] = None,
    minor_version_auto_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    publisher: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__658937e4dedc96fe11ad66d2cb815b98d1c8b5c43073be9650d387007b39094a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d18ad19ca49517e6b656f782348b28e1c711140772bb3e00124f73ceaa3416(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f4d27ca7f5a5c27665a1e7071b67169984dd12e58d438acf50ca15befab0be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bc1affc82082990717a73413469189422941cdc0236f60babf3af871d0836e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd751c441c6e00a061e0aeda3033416e084ad93ac5296f0e5f64d6a1e19bad46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b53a7a32536faa3cc3ed7fe66c91af8da7ec07ebf469717ed33edb082b49ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksExtension]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c46dcdbbe1c8585260c293856614f4449bef076ef7dcf6d9c60790b8ec026b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3c992720c3eccd3931ae9d9c6122b5f30df92d84becfd7edb69afa4f8fca6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40f25cb96fd8737dfd963231df3f1aa47a704079d8edd0ff1a5e71ffdb9ee6c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8116002b83000ce730b4e1c15258465a38e930addaa28d2fd5f2d1e74475e0d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e4014d1b52dd708a99a3f39bbd0327a2497aac535e6b2c33d451c1dbceab10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce1bc6a9876cca9e3cfd44d9c53ae9df5a22789c5e0308f8453a695f7b1a146(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d99ec82cf6db78ba1befc6c920331eeb3215dd587a030999867a673558bfdd(
    value: typing.Optional[typing.Union[OceanAksExtension, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30af99792eb483280c75356a57ce98953944ff2ccbe1317139b311b72e97127(
    *,
    grace_period: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e99357f04f8929e2697d66499c2d7eec6436812df5e3baf118180288ce5228d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3c6d5e487e2c02933f83cf452a5fac3547c402dbe0eae1891f089f4e9a4da5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668c56b9843ede57c8f2f8952f2922ade1f2e45a1b676fd22b205c1d4198ae5e(
    value: typing.Optional[OceanAksHealth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544ed47651e52093b9015bcba3c724a9c4ce200fd01240a573faeae766d3181e(
    *,
    marketplace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksImageMarketplace, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a2295b1f979cd7fde50344a7cb5864ad2bd03e57633778a919eccc9307737a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867cbd55a1fc119cada1362ff313770973b78b810d9fc78b8330150cacf5958c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e625c026b85ba70da5b8bf3bce0f3ed388300170b01136bcec58d32d46b4d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2780ec880ec3269153045228fb26056cde8d5862d1faf975a56fdbdda1c51f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c196527d4e4e032cc86bae963289220f001679c82a927c382918808ecbd6c23c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341ec0bcb66d1778ce2d8a347e13146839d81d0eead71798001d651f2ae2e60a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksImage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28fd44ed7fa6886d568cda078b685f14bbf45087c286674115b842bd0948eb4(
    *,
    offer: typing.Optional[builtins.str] = None,
    publisher: typing.Optional[builtins.str] = None,
    sku: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5979b09ad1733674223768567cc1a3965b166762fa0ca0394eda5c3e41ea5120(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf187fcacde8dc2b0f3568d4004c1c314bf776ba82a8ea96149f08a8e604dcb2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd2f3cc1aca117615155b85d77abff5606403088735c5b1f8e05a5ca46b08cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907314756833326167c32b10c45fe00a6f0631790e9a035d517866313b866f99(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7972cf0ab807f54b2c5c87b83844082f6063496570ca85d779b194508629c30(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2663a5dd251227a1bdc0de31d4f05f31522d8e63b7cd2a6cb8744f38b44e790(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksImageMarketplace]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3e696217f354b68d32397a3a8ab2378041e9d2133118d5560aeafb43b1b704(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fa6c608267eb63ec2ef136b42342bfaf9abb3ccc1fbcc57bddf600ec12f613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdaa9315d03914d2a46d1f24de4975555bc6f88e8819ec45a0a85d13930db33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707e14d5049fb6d3c50873c5d8dac0c2100f7886909d41d583116aab94e9c545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efd6ddc6b02f93de1951051a2891f3795e2c370d896d719c18cc8c72e685b53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782d409f2bb122f45aab0cc297448d121395e701660aa65ff43a32790f0d6ef2(
    value: typing.Optional[typing.Union[OceanAksImageMarketplace, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c74ebb924db40504ca97606fb7ac57d3a9781585b101b54f9d87b79a1aac53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720bad18cac313d81fe2f0acf9706e24e2faeeb0c7ca2405d0dcfa3f2253c445(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksImageMarketplace, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb20d2642d66e8dd33abc5a706d9f20f78c3ad4609fbe5e2fc6e9b7b44269ea9(
    value: typing.Optional[typing.Union[OceanAksImage, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30268f77d6ac6b45e799dcf6888208ad9bb291a71c16efd736441c4e0e67183a(
    *,
    backend_pool_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    load_balancer_sku: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resource_group_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7582a00905b28c75fb1349ea2263904880547f04e855f6e896282ec3a90972b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed2542d849bae884fb68a85996349b7f71250e40b336280ff19c4533ad38dad(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5605ecf9953edf3d113e7a2c45414399114d440bf696621f8b170a0dcd6f7c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980420fd5f154a627f680c55bd228d6fb4ca4764134042dee99c99f8cd7cc2fb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2867ca95031c8a617cfc3e2ac1b93584ccdd27eb92d4141cc09520c09f520e6b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f4bc0a790cde6028e2da14c3bb321dfed9dd7cc2f2de3ce919f9ee3b623294(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksLoadBalancer]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb142fc846366619ad45a2a1c9ef8f37cfd4230dc6ba33da6b33c068ced2e371(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8dcaf2ece1f23a3edd421d20612a5f8045e1ebeba9377476761afeff5ccc314(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c6689cb2332c45a9690188b9b46f82bdd3aef8826cee52785fd770338dc81f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ee2d62bcbf785c4f78f856f99b250271aebe49fab46caffbbb39f1f6dbf4ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c8eceb4cdaefaafa4fe9a8f7b408b06162c4471b2493f859666c89001ca558(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b4e769589632ad4c35b691b7bccd2bce53237384f06c7c17191b15915919e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d826fa36e5d99b7296f72c133e260877d9e6ace3b6d567b1be10b9937c19dce(
    value: typing.Optional[typing.Union[OceanAksLoadBalancer, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cda664452e2f5cf168e1f2220f417f97f8e62a61f1996112acf516ddee0c754(
    *,
    name: builtins.str,
    resource_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798904b182dfa808282e77fda16af7d98af4298a2f0a9402b8a5e91c0f9c8cd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6087feda6471ce81d00cc8a19ecac7e2e0c8554892edb8dbac998ae5398c3d47(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f81a0e9f0290394c7afdcf15426f28403224cb1b57c6fb10c2e9227ea7b2b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa83ee39ec89de65fc7c0713ad0590fd6f34614388bf566743dc747119afa4b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9214911f47631ccb7fd4bde1f5cd43152549e0980ef36972ba1080a7a06e677(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0427a45077772cab741e74a516f4d1adc7c28942025290d8bc8db7e69a5239c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksManagedServiceIdentity]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befffe5eeacb2aa2d2797a9731844edea4a35537a5951abf0ca5fbb116bc29a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7384eb5d9cd14703b49fae863de4ce51f5e0284c2ab7d2878aac21a9fcffd39f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71cc8ec627d6acc4038305b4a5e00ca158cdd88a5f857cefa8334e2428acd9dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e81136fcc2393199cc7343a271f0a71983a17f66bc9c3c65c2161d730ad375(
    value: typing.Optional[typing.Union[OceanAksManagedServiceIdentity, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44055b0100d00c2e1efa96c49cfb80eaf68e1c7056a35bb6cb7474b37c11bae7(
    *,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNetworkNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_group_name: typing.Optional[builtins.str] = None,
    virtual_network_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d469f156b97c924871c2ac85472a6b275e050832d997b9197b2a59c5e50dd50a(
    *,
    additional_ip_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNetworkNetworkInterfaceAdditionalIpConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    assign_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_primary: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_group: typing.Optional[typing.Union[OceanAksNetworkNetworkInterfaceSecurityGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186fe969342aeee27c4b73796ade96c1f3e7e0bdcbbaa6c4afef5b8ca31cd8f6(
    *,
    name: typing.Optional[builtins.str] = None,
    private_ip_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519f3a83146bf4eab02cff3116011d36e964343474a8f3c1b41dec4ce8b8bb2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1215fd5996e7d6ca6c647be2a6204c7a1c69bd7f94779f51f000d18c28516918(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a428c235c229dfb26f3f742bd121cc90dcf08d8e96ef387c438e463fef7722(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073a31928ec33b75fd4ec33e1cd2553d56dc87615af77777efd0a5603aec2122(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac0d5a32075001b13bad4b53917efdb494a15e684afc8a05e8134de9ff8e8c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96a20b90a02598bd8333c3c45a01c3c5a3c2d6ea06e2154a65dc9aa1d077faf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterfaceAdditionalIpConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7720557a5761941f25047f41906be5630a9d0ca6f31aac9827c9e413361099b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddff0ac789a8018b654bb1e0d3f72e8ccb04c36fc9eed326be067e96fad549f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a12e5b7349f455db4d2ee727a7c3c97570d9a9ed2916d3204ceb13de2912ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd54f1a6564cecd58bb9a68b3667610f9f2d301a49388a93e14ead25946010e(
    value: typing.Optional[typing.Union[OceanAksNetworkNetworkInterfaceAdditionalIpConfig, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980abf17a662b0a879443d3712140fc47c427ab41db579fec04638fea1198e56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b334c4bb233ca606b7a19d9c89d3b76380768046f86f3aff26bdea3f8525b54f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a78c79d4a23c492f12204186aeba83c7cacf45e358ee8339e8cd32fb3b00873(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcc2e69c7f0720f65c9e073f666f5180c90cdd6706ebe49e817a1da7deb939c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82b24042e0a40224d3b2fc1518cd895acd30f6f56bea8aa9d7e5b65c69f999f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a90b0f995208c7b6300370c146de4e6fe95ff967462065a8c461149e79add1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNetworkNetworkInterface]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62bbd522a6c6524339da6df55bf1f84596f7e9785f0775516c276200859ed5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03abb7461ac22a6d9c496f3a211d131eb5f9aefefe1601675c0e935d821de51(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNetworkNetworkInterfaceAdditionalIpConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9304585881ae6f3aaf632a15ac55f8e570d15cf8638e167b6b017d8ab8650f73(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe8c4c1c9627af9a60d5583bacbbda54f32c7b800e90439b6b20d0f19963251(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a5ca9e94e1917225ecdf0a2a0e06e6cf7f8806934e0b5abe0d2def7d3512b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f695b4a26160523e8de55743e2db29a5fada766b45450607bfa92c031595a72d(
    value: typing.Optional[typing.Union[OceanAksNetworkNetworkInterface, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf3410b5030b0dda2d8bdbf93051180bf267667db4e2f48b01e50abc50b0e5a(
    *,
    name: typing.Optional[builtins.str] = None,
    resource_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2f890013d9cf54d4948f37a1d16f109aec96056ddffbe501bc5c613c99ccf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a0b476bfdb7ea765c5119d3f690349c722752fa47ce39e65f174bbef93c4c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14eec666b2a11cc8d7dd56e00e3d6e365d8b9377f297eedcb7c88be28c85d038(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f55dcf49f35abf38636df8bd13556b6d5d693a3459d0b1e045f67148719bd611(
    value: typing.Optional[OceanAksNetworkNetworkInterfaceSecurityGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0959abbb880fee044efd1b5cf41a5aa5dddb1498364d61c01e911d9b7338a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56bb1e056cc9319975c4935007d758e179e01910d4f6d77581431d3e008d1a9d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNetworkNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1872ae898b799212065f80316b5fceca0e3eeee1eb42f01731a7896317ec3f39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317e3ef187b8fb3bf38d14cab305852e9e7f970d58fdcb737e6b816110c775cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd4034a016efd05b5d7cd8e3c69972d72ac4fef291bdb32614d1e613943cee8(
    value: typing.Optional[OceanAksNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a768facb3e7b071b3f5efcf7dbfda65e61426ffc96a4afccd8b9fb36f5992cc(
    *,
    size_gb: jsii.Number,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816ffb48616c934e754fecf68270295616da3ae825ec35c312a715caf91b6b66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78aa7d7fe69aa8d3d5430b4a870b0288789a0a5d28c65f82082d86120972d441(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6aed9a34c152701afae7c62aca6ddfcc4dfb3f65241349097a0169aed3ecaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be843cf0458ee3f37ca48ef75480671209f1cd9c9246bb3a1bae681283f34e54(
    value: typing.Optional[OceanAksOsDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd6fc7fa77133e8667d3343f36c1234f34c2afbfc1d391c3aae25ed5f973489(
    *,
    fallback_to_ondemand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    spot_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5455af57d553c11ebfc95141c1a2be4ab8ff17467ee2350efae6c46cafbb2c20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4adfd895844508ad6b2eaf1efb74bb6839f1a7526a6271e678922a4aa4b4dd6a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cbbc645fc9d2dd511eaf3a737f9ad02133d1edff2413a5ac70497bc8dea2b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2282b319a3e73a54044ebd6c0be0334ac8a71dacbbf0fd6358a8a823018cfafc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdf5dd61e9e52f465ec24ebb7227e8301145951a781cf0b325d52370da02df2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306de7a07401b322c03c11370eb243e475c7fe0b619b0cb4a29676d32fcb6815(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksStrategy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6660cd9cb2b6f6f1a1a12cf2583ca6993bd2648061005ec474eccb1676d63ba9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a231cd04076914b3fe107fb0b8c1d0c2c09234d649ad87aeebf4f4fefbbf116(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae3a7e932669b0926992ee65177edbf46d3de20efae6d79ac0a0fb5179d12cd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503e22157f80912e5603fc330f6dad8f0f346625defe5ce829c00b6d646e8c6c(
    value: typing.Optional[typing.Union[OceanAksStrategy, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173a0a90bdbb68c71d90c1c950bbfac5e720c6fb5c4b16b85ca6f4721dbf7e0c(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0218ccf96fcb158e3ea05c177a346bf26c499764c5d296c86f4375ccfa272660(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ce67cad8dc22b210868f802412b7ea22a7dbf2c8df17a56f4cf2dd046562a9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b689c58727329fabea1757de4d5fcd29a82f28732510524940d95404dbd67a81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad1545da5ab38682b9eb895f43d3392681f067b371809284075d22b64d65aa0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b14bcacbf70aa06c3f656c9ccf671d04a29e82c804a0a94f6ed8c34b8aaeff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b859558575e533cff68f2c68ea3d2fad39bd1a250c27189cf97e531fa11e4e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f097d6118daab00509b58426062cb7d7855b704e1e23674668b390f05dac2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71bbce48839b3ee9098e07df03c73b08f057699276ed42d3d040d7898086cc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49a531290835b81fb0a47f3744ced9b1c56ac226156fb29217e1590a687b144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c18d32595f8ceb8ed938c4c2cef191661af3a21c192e2f97b93985ed4717ed(
    value: typing.Optional[typing.Union[OceanAksTag, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafa40c378cb3e2a63ed918cda17229a737882fd57cde5ef080413d834c59892(
    *,
    whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd8cb897bf076ec10a21b1b27ad55c3baaeb72015852a247bd86e8dca36882a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd1a86f770714da229cc6fceb7e1f1c8c46aac1c7b2236c58771dc1be40fdc7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85bacee1c1c90a6f11090aad5a8af767703c1b57151c18fbba0e8abe3d86776(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b062da65d93f265281fe657cf551652b803b6599f74ec39e44b70b46d556fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebf3102adcf1115d4ffe3635a91a29410be3345cb3dcc719b01bffb0aad2ca0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9b1b05f70f7e7fdf85d6ea178af0379456433799a51164073ab19d8f20ed6c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksVmSizes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e412483ca4a8cc1258f0f9ccc764db4041918746a5db6715e5bebdbb9f4c889(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91cec6dacd94ebc69de81d853a4355b7d1cf787cea0cb8872ecad5ad9fe1c3d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748bf37ea12647c497e4e496da60d51241cf52f96e961ea0ec73c868a4e059a2(
    value: typing.Optional[typing.Union[OceanAksVmSizes, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
