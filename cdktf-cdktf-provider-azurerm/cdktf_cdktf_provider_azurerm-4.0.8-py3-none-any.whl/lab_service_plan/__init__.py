'''
# `azurerm_lab_service_plan`

Refer to the Terraform Registory for docs: [`azurerm_lab_service_plan`](https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan).
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


class LabServicePlan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServicePlan.LabServicePlan",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan azurerm_lab_service_plan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        allowed_regions: typing.Sequence[builtins.str],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        default_auto_shutdown: typing.Optional[typing.Union["LabServicePlanDefaultAutoShutdown", typing.Dict[builtins.str, typing.Any]]] = None,
        default_connection: typing.Optional[typing.Union["LabServicePlanDefaultConnection", typing.Dict[builtins.str, typing.Any]]] = None,
        default_network_subnet_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        shared_gallery_id: typing.Optional[builtins.str] = None,
        support: typing.Optional[typing.Union["LabServicePlanSupport", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LabServicePlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan azurerm_lab_service_plan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param allowed_regions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#allowed_regions LabServicePlan#allowed_regions}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#location LabServicePlan#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#name LabServicePlan#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#resource_group_name LabServicePlan#resource_group_name}.
        :param default_auto_shutdown: default_auto_shutdown block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#default_auto_shutdown LabServicePlan#default_auto_shutdown}
        :param default_connection: default_connection block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#default_connection LabServicePlan#default_connection}
        :param default_network_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#default_network_subnet_id LabServicePlan#default_network_subnet_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#id LabServicePlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param shared_gallery_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#shared_gallery_id LabServicePlan#shared_gallery_id}.
        :param support: support block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#support LabServicePlan#support}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#tags LabServicePlan#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#timeouts LabServicePlan#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e27e3848c66f1c0707f30f4d704c3de5fdc67419a124853780b300522dda0cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LabServicePlanConfig(
            allowed_regions=allowed_regions,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            default_auto_shutdown=default_auto_shutdown,
            default_connection=default_connection,
            default_network_subnet_id=default_network_subnet_id,
            id=id,
            shared_gallery_id=shared_gallery_id,
            support=support,
            tags=tags,
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

    @jsii.member(jsii_name="putDefaultAutoShutdown")
    def put_default_auto_shutdown(
        self,
        *,
        disconnect_delay: typing.Optional[builtins.str] = None,
        idle_delay: typing.Optional[builtins.str] = None,
        no_connect_delay: typing.Optional[builtins.str] = None,
        shutdown_on_idle: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disconnect_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#disconnect_delay LabServicePlan#disconnect_delay}.
        :param idle_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#idle_delay LabServicePlan#idle_delay}.
        :param no_connect_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#no_connect_delay LabServicePlan#no_connect_delay}.
        :param shutdown_on_idle: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#shutdown_on_idle LabServicePlan#shutdown_on_idle}.
        '''
        value = LabServicePlanDefaultAutoShutdown(
            disconnect_delay=disconnect_delay,
            idle_delay=idle_delay,
            no_connect_delay=no_connect_delay,
            shutdown_on_idle=shutdown_on_idle,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultAutoShutdown", [value]))

    @jsii.member(jsii_name="putDefaultConnection")
    def put_default_connection(
        self,
        *,
        client_rdp_access: typing.Optional[builtins.str] = None,
        client_ssh_access: typing.Optional[builtins.str] = None,
        web_rdp_access: typing.Optional[builtins.str] = None,
        web_ssh_access: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_rdp_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#client_rdp_access LabServicePlan#client_rdp_access}.
        :param client_ssh_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#client_ssh_access LabServicePlan#client_ssh_access}.
        :param web_rdp_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#web_rdp_access LabServicePlan#web_rdp_access}.
        :param web_ssh_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#web_ssh_access LabServicePlan#web_ssh_access}.
        '''
        value = LabServicePlanDefaultConnection(
            client_rdp_access=client_rdp_access,
            client_ssh_access=client_ssh_access,
            web_rdp_access=web_rdp_access,
            web_ssh_access=web_ssh_access,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultConnection", [value]))

    @jsii.member(jsii_name="putSupport")
    def put_support(
        self,
        *,
        email: typing.Optional[builtins.str] = None,
        instructions: typing.Optional[builtins.str] = None,
        phone: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#email LabServicePlan#email}.
        :param instructions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#instructions LabServicePlan#instructions}.
        :param phone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#phone LabServicePlan#phone}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#url LabServicePlan#url}.
        '''
        value = LabServicePlanSupport(
            email=email, instructions=instructions, phone=phone, url=url
        )

        return typing.cast(None, jsii.invoke(self, "putSupport", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#create LabServicePlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#delete LabServicePlan#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#read LabServicePlan#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#update LabServicePlan#update}.
        '''
        value = LabServicePlanTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDefaultAutoShutdown")
    def reset_default_auto_shutdown(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultAutoShutdown", []))

    @jsii.member(jsii_name="resetDefaultConnection")
    def reset_default_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultConnection", []))

    @jsii.member(jsii_name="resetDefaultNetworkSubnetId")
    def reset_default_network_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultNetworkSubnetId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSharedGalleryId")
    def reset_shared_gallery_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedGalleryId", []))

    @jsii.member(jsii_name="resetSupport")
    def reset_support(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupport", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="defaultAutoShutdown")
    def default_auto_shutdown(
        self,
    ) -> "LabServicePlanDefaultAutoShutdownOutputReference":
        return typing.cast("LabServicePlanDefaultAutoShutdownOutputReference", jsii.get(self, "defaultAutoShutdown"))

    @builtins.property
    @jsii.member(jsii_name="defaultConnection")
    def default_connection(self) -> "LabServicePlanDefaultConnectionOutputReference":
        return typing.cast("LabServicePlanDefaultConnectionOutputReference", jsii.get(self, "defaultConnection"))

    @builtins.property
    @jsii.member(jsii_name="support")
    def support(self) -> "LabServicePlanSupportOutputReference":
        return typing.cast("LabServicePlanSupportOutputReference", jsii.get(self, "support"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LabServicePlanTimeoutsOutputReference":
        return typing.cast("LabServicePlanTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allowedRegionsInput")
    def allowed_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAutoShutdownInput")
    def default_auto_shutdown_input(
        self,
    ) -> typing.Optional["LabServicePlanDefaultAutoShutdown"]:
        return typing.cast(typing.Optional["LabServicePlanDefaultAutoShutdown"], jsii.get(self, "defaultAutoShutdownInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultConnectionInput")
    def default_connection_input(
        self,
    ) -> typing.Optional["LabServicePlanDefaultConnection"]:
        return typing.cast(typing.Optional["LabServicePlanDefaultConnection"], jsii.get(self, "defaultConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultNetworkSubnetIdInput")
    def default_network_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultNetworkSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedGalleryIdInput")
    def shared_gallery_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedGalleryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="supportInput")
    def support_input(self) -> typing.Optional["LabServicePlanSupport"]:
        return typing.cast(typing.Optional["LabServicePlanSupport"], jsii.get(self, "supportInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["LabServicePlanTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["LabServicePlanTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRegions")
    def allowed_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRegions"))

    @allowed_regions.setter
    def allowed_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f428bac05c2761df115a27d816ab3e7f045cf402b754ff75cbc02b6f5c3da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRegions", value)

    @builtins.property
    @jsii.member(jsii_name="defaultNetworkSubnetId")
    def default_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultNetworkSubnetId"))

    @default_network_subnet_id.setter
    def default_network_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b242a9b763d6ebf37ce935ddc1afa790514bae63a2f2dff83cb19d0d952d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultNetworkSubnetId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__193cef3db718175eee53fcd23d59d9cf28f4332e14c51771f43a2ec03e543aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eac5792988494b19a7d82ebb3d4f54cc787dd3d201a7454e4deab21eaa33371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a5a9c3b05c61b1592058b09a8b0ea2d19070b0e23156e156fba2eeb419f000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ce4532aa548c96a85ccc2b38236b7f6d628f78a27d3602bb48ae46903a2446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="sharedGalleryId")
    def shared_gallery_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedGalleryId"))

    @shared_gallery_id.setter
    def shared_gallery_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755cd94800cae9de5b1f14f80b61acf7354829a1080ac4e19d9f355f309f7f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedGalleryId", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36402b4d96a522e2f2b5fac5d74a3e71e87fff49a3b16b428cb5c9d2d100a784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServicePlan.LabServicePlanConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "allowed_regions": "allowedRegions",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "default_auto_shutdown": "defaultAutoShutdown",
        "default_connection": "defaultConnection",
        "default_network_subnet_id": "defaultNetworkSubnetId",
        "id": "id",
        "shared_gallery_id": "sharedGalleryId",
        "support": "support",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class LabServicePlanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allowed_regions: typing.Sequence[builtins.str],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        default_auto_shutdown: typing.Optional[typing.Union["LabServicePlanDefaultAutoShutdown", typing.Dict[builtins.str, typing.Any]]] = None,
        default_connection: typing.Optional[typing.Union["LabServicePlanDefaultConnection", typing.Dict[builtins.str, typing.Any]]] = None,
        default_network_subnet_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        shared_gallery_id: typing.Optional[builtins.str] = None,
        support: typing.Optional[typing.Union["LabServicePlanSupport", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LabServicePlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param allowed_regions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#allowed_regions LabServicePlan#allowed_regions}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#location LabServicePlan#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#name LabServicePlan#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#resource_group_name LabServicePlan#resource_group_name}.
        :param default_auto_shutdown: default_auto_shutdown block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#default_auto_shutdown LabServicePlan#default_auto_shutdown}
        :param default_connection: default_connection block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#default_connection LabServicePlan#default_connection}
        :param default_network_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#default_network_subnet_id LabServicePlan#default_network_subnet_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#id LabServicePlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param shared_gallery_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#shared_gallery_id LabServicePlan#shared_gallery_id}.
        :param support: support block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#support LabServicePlan#support}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#tags LabServicePlan#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#timeouts LabServicePlan#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_auto_shutdown, dict):
            default_auto_shutdown = LabServicePlanDefaultAutoShutdown(**default_auto_shutdown)
        if isinstance(default_connection, dict):
            default_connection = LabServicePlanDefaultConnection(**default_connection)
        if isinstance(support, dict):
            support = LabServicePlanSupport(**support)
        if isinstance(timeouts, dict):
            timeouts = LabServicePlanTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb3bd3b6d66934119825e8fe173777a1e362a08f47ac086334937a82110245b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument allowed_regions", value=allowed_regions, expected_type=type_hints["allowed_regions"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument default_auto_shutdown", value=default_auto_shutdown, expected_type=type_hints["default_auto_shutdown"])
            check_type(argname="argument default_connection", value=default_connection, expected_type=type_hints["default_connection"])
            check_type(argname="argument default_network_subnet_id", value=default_network_subnet_id, expected_type=type_hints["default_network_subnet_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument shared_gallery_id", value=shared_gallery_id, expected_type=type_hints["shared_gallery_id"])
            check_type(argname="argument support", value=support, expected_type=type_hints["support"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_regions": allowed_regions,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if default_auto_shutdown is not None:
            self._values["default_auto_shutdown"] = default_auto_shutdown
        if default_connection is not None:
            self._values["default_connection"] = default_connection
        if default_network_subnet_id is not None:
            self._values["default_network_subnet_id"] = default_network_subnet_id
        if id is not None:
            self._values["id"] = id
        if shared_gallery_id is not None:
            self._values["shared_gallery_id"] = shared_gallery_id
        if support is not None:
            self._values["support"] = support
        if tags is not None:
            self._values["tags"] = tags
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
    def allowed_regions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#allowed_regions LabServicePlan#allowed_regions}.'''
        result = self._values.get("allowed_regions")
        assert result is not None, "Required property 'allowed_regions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#location LabServicePlan#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#name LabServicePlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#resource_group_name LabServicePlan#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_auto_shutdown(
        self,
    ) -> typing.Optional["LabServicePlanDefaultAutoShutdown"]:
        '''default_auto_shutdown block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#default_auto_shutdown LabServicePlan#default_auto_shutdown}
        '''
        result = self._values.get("default_auto_shutdown")
        return typing.cast(typing.Optional["LabServicePlanDefaultAutoShutdown"], result)

    @builtins.property
    def default_connection(self) -> typing.Optional["LabServicePlanDefaultConnection"]:
        '''default_connection block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#default_connection LabServicePlan#default_connection}
        '''
        result = self._values.get("default_connection")
        return typing.cast(typing.Optional["LabServicePlanDefaultConnection"], result)

    @builtins.property
    def default_network_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#default_network_subnet_id LabServicePlan#default_network_subnet_id}.'''
        result = self._values.get("default_network_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#id LabServicePlan#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_gallery_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#shared_gallery_id LabServicePlan#shared_gallery_id}.'''
        result = self._values.get("shared_gallery_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support(self) -> typing.Optional["LabServicePlanSupport"]:
        '''support block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#support LabServicePlan#support}
        '''
        result = self._values.get("support")
        return typing.cast(typing.Optional["LabServicePlanSupport"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#tags LabServicePlan#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LabServicePlanTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#timeouts LabServicePlan#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LabServicePlanTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServicePlanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServicePlan.LabServicePlanDefaultAutoShutdown",
    jsii_struct_bases=[],
    name_mapping={
        "disconnect_delay": "disconnectDelay",
        "idle_delay": "idleDelay",
        "no_connect_delay": "noConnectDelay",
        "shutdown_on_idle": "shutdownOnIdle",
    },
)
class LabServicePlanDefaultAutoShutdown:
    def __init__(
        self,
        *,
        disconnect_delay: typing.Optional[builtins.str] = None,
        idle_delay: typing.Optional[builtins.str] = None,
        no_connect_delay: typing.Optional[builtins.str] = None,
        shutdown_on_idle: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disconnect_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#disconnect_delay LabServicePlan#disconnect_delay}.
        :param idle_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#idle_delay LabServicePlan#idle_delay}.
        :param no_connect_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#no_connect_delay LabServicePlan#no_connect_delay}.
        :param shutdown_on_idle: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#shutdown_on_idle LabServicePlan#shutdown_on_idle}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192745b01308d128abc34d4cf843943c12666117a9b454a4a067564f1cc58327)
            check_type(argname="argument disconnect_delay", value=disconnect_delay, expected_type=type_hints["disconnect_delay"])
            check_type(argname="argument idle_delay", value=idle_delay, expected_type=type_hints["idle_delay"])
            check_type(argname="argument no_connect_delay", value=no_connect_delay, expected_type=type_hints["no_connect_delay"])
            check_type(argname="argument shutdown_on_idle", value=shutdown_on_idle, expected_type=type_hints["shutdown_on_idle"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disconnect_delay is not None:
            self._values["disconnect_delay"] = disconnect_delay
        if idle_delay is not None:
            self._values["idle_delay"] = idle_delay
        if no_connect_delay is not None:
            self._values["no_connect_delay"] = no_connect_delay
        if shutdown_on_idle is not None:
            self._values["shutdown_on_idle"] = shutdown_on_idle

    @builtins.property
    def disconnect_delay(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#disconnect_delay LabServicePlan#disconnect_delay}.'''
        result = self._values.get("disconnect_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_delay(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#idle_delay LabServicePlan#idle_delay}.'''
        result = self._values.get("idle_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_connect_delay(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#no_connect_delay LabServicePlan#no_connect_delay}.'''
        result = self._values.get("no_connect_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shutdown_on_idle(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#shutdown_on_idle LabServicePlan#shutdown_on_idle}.'''
        result = self._values.get("shutdown_on_idle")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServicePlanDefaultAutoShutdown(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServicePlanDefaultAutoShutdownOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServicePlan.LabServicePlanDefaultAutoShutdownOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__636c724921a1a2f21d65d5b83ba49e98261419d016080dff8086145a9720b842)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisconnectDelay")
    def reset_disconnect_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisconnectDelay", []))

    @jsii.member(jsii_name="resetIdleDelay")
    def reset_idle_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleDelay", []))

    @jsii.member(jsii_name="resetNoConnectDelay")
    def reset_no_connect_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoConnectDelay", []))

    @jsii.member(jsii_name="resetShutdownOnIdle")
    def reset_shutdown_on_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShutdownOnIdle", []))

    @builtins.property
    @jsii.member(jsii_name="disconnectDelayInput")
    def disconnect_delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "disconnectDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="idleDelayInput")
    def idle_delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idleDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="noConnectDelayInput")
    def no_connect_delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noConnectDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="shutdownOnIdleInput")
    def shutdown_on_idle_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shutdownOnIdleInput"))

    @builtins.property
    @jsii.member(jsii_name="disconnectDelay")
    def disconnect_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disconnectDelay"))

    @disconnect_delay.setter
    def disconnect_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abfc4660c785aac5c870b95046f00de62b5f3a88bc4a2540ba470e9b9544be29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disconnectDelay", value)

    @builtins.property
    @jsii.member(jsii_name="idleDelay")
    def idle_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idleDelay"))

    @idle_delay.setter
    def idle_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6162cc7a64a04abb86988b70656bad12742b2674ec2a786f4cb62774ed049c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleDelay", value)

    @builtins.property
    @jsii.member(jsii_name="noConnectDelay")
    def no_connect_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noConnectDelay"))

    @no_connect_delay.setter
    def no_connect_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c48b550156e30f3be17cfb2cbed5e8c2edbd41b6d1b5c666356179752a7a712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noConnectDelay", value)

    @builtins.property
    @jsii.member(jsii_name="shutdownOnIdle")
    def shutdown_on_idle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shutdownOnIdle"))

    @shutdown_on_idle.setter
    def shutdown_on_idle(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c99b52a06edeb7629d3306a527b8515d7cc3e5145da1f182e0c88f9b407917b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shutdownOnIdle", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LabServicePlanDefaultAutoShutdown]:
        return typing.cast(typing.Optional[LabServicePlanDefaultAutoShutdown], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LabServicePlanDefaultAutoShutdown],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8387196997d20540d3b9a5aef40363b6a6739ebdde7812b0dfa042fbbb2134da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServicePlan.LabServicePlanDefaultConnection",
    jsii_struct_bases=[],
    name_mapping={
        "client_rdp_access": "clientRdpAccess",
        "client_ssh_access": "clientSshAccess",
        "web_rdp_access": "webRdpAccess",
        "web_ssh_access": "webSshAccess",
    },
)
class LabServicePlanDefaultConnection:
    def __init__(
        self,
        *,
        client_rdp_access: typing.Optional[builtins.str] = None,
        client_ssh_access: typing.Optional[builtins.str] = None,
        web_rdp_access: typing.Optional[builtins.str] = None,
        web_ssh_access: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_rdp_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#client_rdp_access LabServicePlan#client_rdp_access}.
        :param client_ssh_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#client_ssh_access LabServicePlan#client_ssh_access}.
        :param web_rdp_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#web_rdp_access LabServicePlan#web_rdp_access}.
        :param web_ssh_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#web_ssh_access LabServicePlan#web_ssh_access}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b099138c98234c5b763f17e904e12ea190a33cf0429229c70ce72ad7748264c)
            check_type(argname="argument client_rdp_access", value=client_rdp_access, expected_type=type_hints["client_rdp_access"])
            check_type(argname="argument client_ssh_access", value=client_ssh_access, expected_type=type_hints["client_ssh_access"])
            check_type(argname="argument web_rdp_access", value=web_rdp_access, expected_type=type_hints["web_rdp_access"])
            check_type(argname="argument web_ssh_access", value=web_ssh_access, expected_type=type_hints["web_ssh_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_rdp_access is not None:
            self._values["client_rdp_access"] = client_rdp_access
        if client_ssh_access is not None:
            self._values["client_ssh_access"] = client_ssh_access
        if web_rdp_access is not None:
            self._values["web_rdp_access"] = web_rdp_access
        if web_ssh_access is not None:
            self._values["web_ssh_access"] = web_ssh_access

    @builtins.property
    def client_rdp_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#client_rdp_access LabServicePlan#client_rdp_access}.'''
        result = self._values.get("client_rdp_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ssh_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#client_ssh_access LabServicePlan#client_ssh_access}.'''
        result = self._values.get("client_ssh_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_rdp_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#web_rdp_access LabServicePlan#web_rdp_access}.'''
        result = self._values.get("web_rdp_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_ssh_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#web_ssh_access LabServicePlan#web_ssh_access}.'''
        result = self._values.get("web_ssh_access")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServicePlanDefaultConnection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServicePlanDefaultConnectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServicePlan.LabServicePlanDefaultConnectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fc4986a35eff91d8dd6abc6675fd8b74afcc7f72dbaceef99d833e58ca142aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientRdpAccess")
    def reset_client_rdp_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientRdpAccess", []))

    @jsii.member(jsii_name="resetClientSshAccess")
    def reset_client_ssh_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSshAccess", []))

    @jsii.member(jsii_name="resetWebRdpAccess")
    def reset_web_rdp_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebRdpAccess", []))

    @jsii.member(jsii_name="resetWebSshAccess")
    def reset_web_ssh_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebSshAccess", []))

    @builtins.property
    @jsii.member(jsii_name="clientRdpAccessInput")
    def client_rdp_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientRdpAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSshAccessInput")
    def client_ssh_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSshAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="webRdpAccessInput")
    def web_rdp_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webRdpAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="webSshAccessInput")
    def web_ssh_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webSshAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="clientRdpAccess")
    def client_rdp_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientRdpAccess"))

    @client_rdp_access.setter
    def client_rdp_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579654ddd5711205e3d78a2f6eaf789edc1949b178d34536acad6a5d7608d1ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientRdpAccess", value)

    @builtins.property
    @jsii.member(jsii_name="clientSshAccess")
    def client_ssh_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSshAccess"))

    @client_ssh_access.setter
    def client_ssh_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc9f4a955025caad8b681b12f4ededc740457f7a6c20aedf191c4f44ac3f4652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSshAccess", value)

    @builtins.property
    @jsii.member(jsii_name="webRdpAccess")
    def web_rdp_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webRdpAccess"))

    @web_rdp_access.setter
    def web_rdp_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3fb41e6197b01c51210d6093f68fd6781c7657d150283091e8e7e21d5580cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webRdpAccess", value)

    @builtins.property
    @jsii.member(jsii_name="webSshAccess")
    def web_ssh_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webSshAccess"))

    @web_ssh_access.setter
    def web_ssh_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3026776b099ccd577c00ca5821ca79fc85b499f6e132f0d8a8f565fc96c8bbe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webSshAccess", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LabServicePlanDefaultConnection]:
        return typing.cast(typing.Optional[LabServicePlanDefaultConnection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LabServicePlanDefaultConnection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f69c44707daf8e15303de56bc4b5e190d0659e6414dce14961b197e310b088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServicePlan.LabServicePlanSupport",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "instructions": "instructions",
        "phone": "phone",
        "url": "url",
    },
)
class LabServicePlanSupport:
    def __init__(
        self,
        *,
        email: typing.Optional[builtins.str] = None,
        instructions: typing.Optional[builtins.str] = None,
        phone: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#email LabServicePlan#email}.
        :param instructions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#instructions LabServicePlan#instructions}.
        :param phone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#phone LabServicePlan#phone}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#url LabServicePlan#url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6ab65d1dd3af04fc263a72acbb7cffcbb962c8d90a090ee12ad2ef376fcad1)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument instructions", value=instructions, expected_type=type_hints["instructions"])
            check_type(argname="argument phone", value=phone, expected_type=type_hints["phone"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if instructions is not None:
            self._values["instructions"] = instructions
        if phone is not None:
            self._values["phone"] = phone
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#email LabServicePlan#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instructions(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#instructions LabServicePlan#instructions}.'''
        result = self._values.get("instructions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#phone LabServicePlan#phone}.'''
        result = self._values.get("phone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#url LabServicePlan#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServicePlanSupport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServicePlanSupportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServicePlan.LabServicePlanSupportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be57a0ab18cde3ef1eff382216f1828337f68621d7ef65d6581fdd057d2446aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetInstructions")
    def reset_instructions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstructions", []))

    @jsii.member(jsii_name="resetPhone")
    def reset_phone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhone", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="instructionsInput")
    def instructions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instructionsInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneInput")
    def phone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a1a4783278a1d3b384402667b6b32c72213cf940d3a70521467ec82926a7406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="instructions")
    def instructions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instructions"))

    @instructions.setter
    def instructions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4185c8355f3c3021379ac0f179a8be36aaf4febda7e6e67c24ab052a46f48b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instructions", value)

    @builtins.property
    @jsii.member(jsii_name="phone")
    def phone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phone"))

    @phone.setter
    def phone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d4e4733569ebb4dafd4627faef720506ea8db7c7fba2007c8dc1ad04d23247a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phone", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a3d3fef696897c6542dcd3f0cb3220cadaa0c9830b5cf842dff29c49d24814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LabServicePlanSupport]:
        return typing.cast(typing.Optional[LabServicePlanSupport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LabServicePlanSupport]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a6be2d2f025f8c80ad16d92ffcccf37c1b66eb28a353e37fb24f2ee228dbb3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServicePlan.LabServicePlanTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class LabServicePlanTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#create LabServicePlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#delete LabServicePlan#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#read LabServicePlan#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#update LabServicePlan#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993842c2ae8ec0f1ff5db9a2c5e28027d32cc88682c29a5cb1bcd297ff970760)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#create LabServicePlan#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#delete LabServicePlan#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#read LabServicePlan#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_plan#update LabServicePlan#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServicePlanTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServicePlanTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServicePlan.LabServicePlanTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45fc31d3dedacda584e35861712da73dad0b883fbe87d9a8d62db31882784bec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__15dcaa94560111fc1471e80a85274affc7e8a170644e9c2ec5e30095dd33b6ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36aac7dbb7f29bdac7fb749f3e25818d6e3871108ba764fca1bb91a083c383c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6dc64b0f3d639f80e75dc0d7130f7fb99dbf3274347e9bbd9a771ec54521db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f61f4799fb30879748f0170d0955f32ddaf1c71be251afa021064d07f5c99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LabServicePlanTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LabServicePlanTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LabServicePlanTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906a8db80f99f0703dbe695e9366a64190bed521a2cde665b8b87c649c373aa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "LabServicePlan",
    "LabServicePlanConfig",
    "LabServicePlanDefaultAutoShutdown",
    "LabServicePlanDefaultAutoShutdownOutputReference",
    "LabServicePlanDefaultConnection",
    "LabServicePlanDefaultConnectionOutputReference",
    "LabServicePlanSupport",
    "LabServicePlanSupportOutputReference",
    "LabServicePlanTimeouts",
    "LabServicePlanTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3e27e3848c66f1c0707f30f4d704c3de5fdc67419a124853780b300522dda0cc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    allowed_regions: typing.Sequence[builtins.str],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    default_auto_shutdown: typing.Optional[typing.Union[LabServicePlanDefaultAutoShutdown, typing.Dict[builtins.str, typing.Any]]] = None,
    default_connection: typing.Optional[typing.Union[LabServicePlanDefaultConnection, typing.Dict[builtins.str, typing.Any]]] = None,
    default_network_subnet_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    shared_gallery_id: typing.Optional[builtins.str] = None,
    support: typing.Optional[typing.Union[LabServicePlanSupport, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LabServicePlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c9f428bac05c2761df115a27d816ab3e7f045cf402b754ff75cbc02b6f5c3da7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b242a9b763d6ebf37ce935ddc1afa790514bae63a2f2dff83cb19d0d952d4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193cef3db718175eee53fcd23d59d9cf28f4332e14c51771f43a2ec03e543aac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eac5792988494b19a7d82ebb3d4f54cc787dd3d201a7454e4deab21eaa33371(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a5a9c3b05c61b1592058b09a8b0ea2d19070b0e23156e156fba2eeb419f000(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ce4532aa548c96a85ccc2b38236b7f6d628f78a27d3602bb48ae46903a2446(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755cd94800cae9de5b1f14f80b61acf7354829a1080ac4e19d9f355f309f7f20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36402b4d96a522e2f2b5fac5d74a3e71e87fff49a3b16b428cb5c9d2d100a784(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb3bd3b6d66934119825e8fe173777a1e362a08f47ac086334937a82110245b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allowed_regions: typing.Sequence[builtins.str],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    default_auto_shutdown: typing.Optional[typing.Union[LabServicePlanDefaultAutoShutdown, typing.Dict[builtins.str, typing.Any]]] = None,
    default_connection: typing.Optional[typing.Union[LabServicePlanDefaultConnection, typing.Dict[builtins.str, typing.Any]]] = None,
    default_network_subnet_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    shared_gallery_id: typing.Optional[builtins.str] = None,
    support: typing.Optional[typing.Union[LabServicePlanSupport, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LabServicePlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192745b01308d128abc34d4cf843943c12666117a9b454a4a067564f1cc58327(
    *,
    disconnect_delay: typing.Optional[builtins.str] = None,
    idle_delay: typing.Optional[builtins.str] = None,
    no_connect_delay: typing.Optional[builtins.str] = None,
    shutdown_on_idle: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636c724921a1a2f21d65d5b83ba49e98261419d016080dff8086145a9720b842(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfc4660c785aac5c870b95046f00de62b5f3a88bc4a2540ba470e9b9544be29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6162cc7a64a04abb86988b70656bad12742b2674ec2a786f4cb62774ed049c36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c48b550156e30f3be17cfb2cbed5e8c2edbd41b6d1b5c666356179752a7a712(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99b52a06edeb7629d3306a527b8515d7cc3e5145da1f182e0c88f9b407917b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8387196997d20540d3b9a5aef40363b6a6739ebdde7812b0dfa042fbbb2134da(
    value: typing.Optional[LabServicePlanDefaultAutoShutdown],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b099138c98234c5b763f17e904e12ea190a33cf0429229c70ce72ad7748264c(
    *,
    client_rdp_access: typing.Optional[builtins.str] = None,
    client_ssh_access: typing.Optional[builtins.str] = None,
    web_rdp_access: typing.Optional[builtins.str] = None,
    web_ssh_access: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc4986a35eff91d8dd6abc6675fd8b74afcc7f72dbaceef99d833e58ca142aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579654ddd5711205e3d78a2f6eaf789edc1949b178d34536acad6a5d7608d1ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9f4a955025caad8b681b12f4ededc740457f7a6c20aedf191c4f44ac3f4652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3fb41e6197b01c51210d6093f68fd6781c7657d150283091e8e7e21d5580cdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3026776b099ccd577c00ca5821ca79fc85b499f6e132f0d8a8f565fc96c8bbe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f69c44707daf8e15303de56bc4b5e190d0659e6414dce14961b197e310b088(
    value: typing.Optional[LabServicePlanDefaultConnection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6ab65d1dd3af04fc263a72acbb7cffcbb962c8d90a090ee12ad2ef376fcad1(
    *,
    email: typing.Optional[builtins.str] = None,
    instructions: typing.Optional[builtins.str] = None,
    phone: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be57a0ab18cde3ef1eff382216f1828337f68621d7ef65d6581fdd057d2446aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1a4783278a1d3b384402667b6b32c72213cf940d3a70521467ec82926a7406(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4185c8355f3c3021379ac0f179a8be36aaf4febda7e6e67c24ab052a46f48b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d4e4733569ebb4dafd4627faef720506ea8db7c7fba2007c8dc1ad04d23247a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a3d3fef696897c6542dcd3f0cb3220cadaa0c9830b5cf842dff29c49d24814(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6be2d2f025f8c80ad16d92ffcccf37c1b66eb28a353e37fb24f2ee228dbb3b(
    value: typing.Optional[LabServicePlanSupport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993842c2ae8ec0f1ff5db9a2c5e28027d32cc88682c29a5cb1bcd297ff970760(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fc31d3dedacda584e35861712da73dad0b883fbe87d9a8d62db31882784bec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15dcaa94560111fc1471e80a85274affc7e8a170644e9c2ec5e30095dd33b6ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36aac7dbb7f29bdac7fb749f3e25818d6e3871108ba764fca1bb91a083c383c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6dc64b0f3d639f80e75dc0d7130f7fb99dbf3274347e9bbd9a771ec54521db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f61f4799fb30879748f0170d0955f32ddaf1c71be251afa021064d07f5c99c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906a8db80f99f0703dbe695e9366a64190bed521a2cde665b8b87c649c373aa3(
    value: typing.Optional[typing.Union[LabServicePlanTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
