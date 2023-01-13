'''
# `azurerm_lab_service_lab`

Refer to the Terraform Registory for docs: [`azurerm_lab_service_lab`](https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab).
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


class LabServiceLab(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLab",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab azurerm_lab_service_lab}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        security: typing.Union["LabServiceLabSecurity", typing.Dict[builtins.str, typing.Any]],
        title: builtins.str,
        virtual_machine: typing.Union["LabServiceLabVirtualMachine", typing.Dict[builtins.str, typing.Any]],
        auto_shutdown: typing.Optional[typing.Union["LabServiceLabAutoShutdown", typing.Dict[builtins.str, typing.Any]]] = None,
        connection_setting: typing.Optional[typing.Union["LabServiceLabConnectionSetting", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lab_plan_id: typing.Optional[builtins.str] = None,
        network: typing.Optional[typing.Union["LabServiceLabNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        roster: typing.Optional[typing.Union["LabServiceLabRoster", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LabServiceLabTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab azurerm_lab_service_lab} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#location LabServiceLab#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#name LabServiceLab#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#resource_group_name LabServiceLab#resource_group_name}.
        :param security: security block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#security LabServiceLab#security}
        :param title: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#title LabServiceLab#title}.
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#virtual_machine LabServiceLab#virtual_machine}
        :param auto_shutdown: auto_shutdown block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#auto_shutdown LabServiceLab#auto_shutdown}
        :param connection_setting: connection_setting block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#connection_setting LabServiceLab#connection_setting}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#description LabServiceLab#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#id LabServiceLab#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lab_plan_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lab_plan_id LabServiceLab#lab_plan_id}.
        :param network: network block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#network LabServiceLab#network}
        :param roster: roster block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#roster LabServiceLab#roster}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#tags LabServiceLab#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#timeouts LabServiceLab#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a623ff5f33e8c555bc1add389562da07826047fc7d1ca85826db176bbc893ee5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LabServiceLabConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            security=security,
            title=title,
            virtual_machine=virtual_machine,
            auto_shutdown=auto_shutdown,
            connection_setting=connection_setting,
            description=description,
            id=id,
            lab_plan_id=lab_plan_id,
            network=network,
            roster=roster,
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

    @jsii.member(jsii_name="putAutoShutdown")
    def put_auto_shutdown(
        self,
        *,
        disconnect_delay: typing.Optional[builtins.str] = None,
        idle_delay: typing.Optional[builtins.str] = None,
        no_connect_delay: typing.Optional[builtins.str] = None,
        shutdown_on_idle: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disconnect_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#disconnect_delay LabServiceLab#disconnect_delay}.
        :param idle_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#idle_delay LabServiceLab#idle_delay}.
        :param no_connect_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#no_connect_delay LabServiceLab#no_connect_delay}.
        :param shutdown_on_idle: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#shutdown_on_idle LabServiceLab#shutdown_on_idle}.
        '''
        value = LabServiceLabAutoShutdown(
            disconnect_delay=disconnect_delay,
            idle_delay=idle_delay,
            no_connect_delay=no_connect_delay,
            shutdown_on_idle=shutdown_on_idle,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoShutdown", [value]))

    @jsii.member(jsii_name="putConnectionSetting")
    def put_connection_setting(
        self,
        *,
        client_rdp_access: typing.Optional[builtins.str] = None,
        client_ssh_access: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_rdp_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#client_rdp_access LabServiceLab#client_rdp_access}.
        :param client_ssh_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#client_ssh_access LabServiceLab#client_ssh_access}.
        '''
        value = LabServiceLabConnectionSetting(
            client_rdp_access=client_rdp_access, client_ssh_access=client_ssh_access
        )

        return typing.cast(None, jsii.invoke(self, "putConnectionSetting", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(self, *, subnet_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#subnet_id LabServiceLab#subnet_id}.
        '''
        value = LabServiceLabNetwork(subnet_id=subnet_id)

        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putRoster")
    def put_roster(
        self,
        *,
        active_directory_group_id: typing.Optional[builtins.str] = None,
        lms_instance: typing.Optional[builtins.str] = None,
        lti_client_id: typing.Optional[builtins.str] = None,
        lti_context_id: typing.Optional[builtins.str] = None,
        lti_roster_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param active_directory_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#active_directory_group_id LabServiceLab#active_directory_group_id}.
        :param lms_instance: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lms_instance LabServiceLab#lms_instance}.
        :param lti_client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lti_client_id LabServiceLab#lti_client_id}.
        :param lti_context_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lti_context_id LabServiceLab#lti_context_id}.
        :param lti_roster_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lti_roster_endpoint LabServiceLab#lti_roster_endpoint}.
        '''
        value = LabServiceLabRoster(
            active_directory_group_id=active_directory_group_id,
            lms_instance=lms_instance,
            lti_client_id=lti_client_id,
            lti_context_id=lti_context_id,
            lti_roster_endpoint=lti_roster_endpoint,
        )

        return typing.cast(None, jsii.invoke(self, "putRoster", [value]))

    @jsii.member(jsii_name="putSecurity")
    def put_security(
        self,
        *,
        open_access_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param open_access_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#open_access_enabled LabServiceLab#open_access_enabled}.
        '''
        value = LabServiceLabSecurity(open_access_enabled=open_access_enabled)

        return typing.cast(None, jsii.invoke(self, "putSecurity", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#create LabServiceLab#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#delete LabServiceLab#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#read LabServiceLab#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#update LabServiceLab#update}.
        '''
        value = LabServiceLabTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualMachine")
    def put_virtual_machine(
        self,
        *,
        admin_user: typing.Union["LabServiceLabVirtualMachineAdminUser", typing.Dict[builtins.str, typing.Any]],
        image_reference: typing.Union["LabServiceLabVirtualMachineImageReference", typing.Dict[builtins.str, typing.Any]],
        sku: typing.Union["LabServiceLabVirtualMachineSku", typing.Dict[builtins.str, typing.Any]],
        additional_capability_gpu_drivers_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_option: typing.Optional[builtins.str] = None,
        non_admin_user: typing.Optional[typing.Union["LabServiceLabVirtualMachineNonAdminUser", typing.Dict[builtins.str, typing.Any]]] = None,
        shared_password_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        usage_quota: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_user: admin_user block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#admin_user LabServiceLab#admin_user}
        :param image_reference: image_reference block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#image_reference LabServiceLab#image_reference}
        :param sku: sku block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#sku LabServiceLab#sku}
        :param additional_capability_gpu_drivers_installed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#additional_capability_gpu_drivers_installed LabServiceLab#additional_capability_gpu_drivers_installed}.
        :param create_option: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#create_option LabServiceLab#create_option}.
        :param non_admin_user: non_admin_user block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#non_admin_user LabServiceLab#non_admin_user}
        :param shared_password_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#shared_password_enabled LabServiceLab#shared_password_enabled}.
        :param usage_quota: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#usage_quota LabServiceLab#usage_quota}.
        '''
        value = LabServiceLabVirtualMachine(
            admin_user=admin_user,
            image_reference=image_reference,
            sku=sku,
            additional_capability_gpu_drivers_installed=additional_capability_gpu_drivers_installed,
            create_option=create_option,
            non_admin_user=non_admin_user,
            shared_password_enabled=shared_password_enabled,
            usage_quota=usage_quota,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualMachine", [value]))

    @jsii.member(jsii_name="resetAutoShutdown")
    def reset_auto_shutdown(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoShutdown", []))

    @jsii.member(jsii_name="resetConnectionSetting")
    def reset_connection_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionSetting", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabPlanId")
    def reset_lab_plan_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabPlanId", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetRoster")
    def reset_roster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoster", []))

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
    @jsii.member(jsii_name="autoShutdown")
    def auto_shutdown(self) -> "LabServiceLabAutoShutdownOutputReference":
        return typing.cast("LabServiceLabAutoShutdownOutputReference", jsii.get(self, "autoShutdown"))

    @builtins.property
    @jsii.member(jsii_name="connectionSetting")
    def connection_setting(self) -> "LabServiceLabConnectionSettingOutputReference":
        return typing.cast("LabServiceLabConnectionSettingOutputReference", jsii.get(self, "connectionSetting"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "LabServiceLabNetworkOutputReference":
        return typing.cast("LabServiceLabNetworkOutputReference", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="roster")
    def roster(self) -> "LabServiceLabRosterOutputReference":
        return typing.cast("LabServiceLabRosterOutputReference", jsii.get(self, "roster"))

    @builtins.property
    @jsii.member(jsii_name="security")
    def security(self) -> "LabServiceLabSecurityOutputReference":
        return typing.cast("LabServiceLabSecurityOutputReference", jsii.get(self, "security"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LabServiceLabTimeoutsOutputReference":
        return typing.cast("LabServiceLabTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachine")
    def virtual_machine(self) -> "LabServiceLabVirtualMachineOutputReference":
        return typing.cast("LabServiceLabVirtualMachineOutputReference", jsii.get(self, "virtualMachine"))

    @builtins.property
    @jsii.member(jsii_name="autoShutdownInput")
    def auto_shutdown_input(self) -> typing.Optional["LabServiceLabAutoShutdown"]:
        return typing.cast(typing.Optional["LabServiceLabAutoShutdown"], jsii.get(self, "autoShutdownInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionSettingInput")
    def connection_setting_input(
        self,
    ) -> typing.Optional["LabServiceLabConnectionSetting"]:
        return typing.cast(typing.Optional["LabServiceLabConnectionSetting"], jsii.get(self, "connectionSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labPlanIdInput")
    def lab_plan_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labPlanIdInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional["LabServiceLabNetwork"]:
        return typing.cast(typing.Optional["LabServiceLabNetwork"], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rosterInput")
    def roster_input(self) -> typing.Optional["LabServiceLabRoster"]:
        return typing.cast(typing.Optional["LabServiceLabRoster"], jsii.get(self, "rosterInput"))

    @builtins.property
    @jsii.member(jsii_name="securityInput")
    def security_input(self) -> typing.Optional["LabServiceLabSecurity"]:
        return typing.cast(typing.Optional["LabServiceLabSecurity"], jsii.get(self, "securityInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["LabServiceLabTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["LabServiceLabTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineInput")
    def virtual_machine_input(self) -> typing.Optional["LabServiceLabVirtualMachine"]:
        return typing.cast(typing.Optional["LabServiceLabVirtualMachine"], jsii.get(self, "virtualMachineInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae8973e57a51ec9aaa47dfc184f70c945d3a9e52d0df3e27b0013b57e4ea447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b34c75eb72c48ba5520fa4ecedeb8ded6b6a588655909b026500e81ee7e447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labPlanId")
    def lab_plan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labPlanId"))

    @lab_plan_id.setter
    def lab_plan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a8d92e1dcbff39c21d2dbc53fab6b1fad0e08fefb8d17da5d834ed2e981736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labPlanId", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf6291d35416ebe367089694c2d8eaa1d0fb97d6bfcc2000e9084270367dd62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623aef57620fb8e3be2dbcef97c1ba498d496bcdf14e8cf5ee55e79db3e53165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676773229fb4029a8706849dac106cd933f3a45240dad654242a9282239e4c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ce0e857b0577d008d9f3664cfeb6966c893e5367bbfa393285d9b51af350ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a41a6790af7b289e724c3477f9258442b210c27c0b3781031104d3706316eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabAutoShutdown",
    jsii_struct_bases=[],
    name_mapping={
        "disconnect_delay": "disconnectDelay",
        "idle_delay": "idleDelay",
        "no_connect_delay": "noConnectDelay",
        "shutdown_on_idle": "shutdownOnIdle",
    },
)
class LabServiceLabAutoShutdown:
    def __init__(
        self,
        *,
        disconnect_delay: typing.Optional[builtins.str] = None,
        idle_delay: typing.Optional[builtins.str] = None,
        no_connect_delay: typing.Optional[builtins.str] = None,
        shutdown_on_idle: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disconnect_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#disconnect_delay LabServiceLab#disconnect_delay}.
        :param idle_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#idle_delay LabServiceLab#idle_delay}.
        :param no_connect_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#no_connect_delay LabServiceLab#no_connect_delay}.
        :param shutdown_on_idle: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#shutdown_on_idle LabServiceLab#shutdown_on_idle}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ce5b8dbbe503bf1cab48f46148fb72c61515d12a13fde2db9fa323fc308c03)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#disconnect_delay LabServiceLab#disconnect_delay}.'''
        result = self._values.get("disconnect_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_delay(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#idle_delay LabServiceLab#idle_delay}.'''
        result = self._values.get("idle_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_connect_delay(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#no_connect_delay LabServiceLab#no_connect_delay}.'''
        result = self._values.get("no_connect_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shutdown_on_idle(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#shutdown_on_idle LabServiceLab#shutdown_on_idle}.'''
        result = self._values.get("shutdown_on_idle")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabAutoShutdown(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServiceLabAutoShutdownOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabAutoShutdownOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89d89cf21d40b2733e171c857cbe5922d8d9489afdb5a72c0fdb84f2566abebc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9745ef2b3743b67555c53204f90dada046512965b71e4f3e9feed6971f599f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disconnectDelay", value)

    @builtins.property
    @jsii.member(jsii_name="idleDelay")
    def idle_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idleDelay"))

    @idle_delay.setter
    def idle_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31100998431cb989ba5af696b37f0017ebbef7feef448f025e91a89b72a94c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleDelay", value)

    @builtins.property
    @jsii.member(jsii_name="noConnectDelay")
    def no_connect_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noConnectDelay"))

    @no_connect_delay.setter
    def no_connect_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc7cae09c3aa2cd5260305b3dcab1383edc636bcd3e2fae48545dfd07c0e38b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noConnectDelay", value)

    @builtins.property
    @jsii.member(jsii_name="shutdownOnIdle")
    def shutdown_on_idle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shutdownOnIdle"))

    @shutdown_on_idle.setter
    def shutdown_on_idle(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d895e4cd1856e2e751a5aade4ad066fc2472b83f3a688a3cef7984927e1a5a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shutdownOnIdle", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LabServiceLabAutoShutdown]:
        return typing.cast(typing.Optional[LabServiceLabAutoShutdown], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LabServiceLabAutoShutdown]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a3eb3ccff5c25b0394475312c3e3ae4a26602186f378fd2d0472caad9f80b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "security": "security",
        "title": "title",
        "virtual_machine": "virtualMachine",
        "auto_shutdown": "autoShutdown",
        "connection_setting": "connectionSetting",
        "description": "description",
        "id": "id",
        "lab_plan_id": "labPlanId",
        "network": "network",
        "roster": "roster",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class LabServiceLabConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        security: typing.Union["LabServiceLabSecurity", typing.Dict[builtins.str, typing.Any]],
        title: builtins.str,
        virtual_machine: typing.Union["LabServiceLabVirtualMachine", typing.Dict[builtins.str, typing.Any]],
        auto_shutdown: typing.Optional[typing.Union[LabServiceLabAutoShutdown, typing.Dict[builtins.str, typing.Any]]] = None,
        connection_setting: typing.Optional[typing.Union["LabServiceLabConnectionSetting", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lab_plan_id: typing.Optional[builtins.str] = None,
        network: typing.Optional[typing.Union["LabServiceLabNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        roster: typing.Optional[typing.Union["LabServiceLabRoster", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LabServiceLabTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#location LabServiceLab#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#name LabServiceLab#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#resource_group_name LabServiceLab#resource_group_name}.
        :param security: security block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#security LabServiceLab#security}
        :param title: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#title LabServiceLab#title}.
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#virtual_machine LabServiceLab#virtual_machine}
        :param auto_shutdown: auto_shutdown block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#auto_shutdown LabServiceLab#auto_shutdown}
        :param connection_setting: connection_setting block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#connection_setting LabServiceLab#connection_setting}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#description LabServiceLab#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#id LabServiceLab#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lab_plan_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lab_plan_id LabServiceLab#lab_plan_id}.
        :param network: network block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#network LabServiceLab#network}
        :param roster: roster block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#roster LabServiceLab#roster}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#tags LabServiceLab#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#timeouts LabServiceLab#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(security, dict):
            security = LabServiceLabSecurity(**security)
        if isinstance(virtual_machine, dict):
            virtual_machine = LabServiceLabVirtualMachine(**virtual_machine)
        if isinstance(auto_shutdown, dict):
            auto_shutdown = LabServiceLabAutoShutdown(**auto_shutdown)
        if isinstance(connection_setting, dict):
            connection_setting = LabServiceLabConnectionSetting(**connection_setting)
        if isinstance(network, dict):
            network = LabServiceLabNetwork(**network)
        if isinstance(roster, dict):
            roster = LabServiceLabRoster(**roster)
        if isinstance(timeouts, dict):
            timeouts = LabServiceLabTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c78b9bc7a7c2f8396d31417d6933f36126cf7723b3070301cc233c233931d71)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument security", value=security, expected_type=type_hints["security"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument virtual_machine", value=virtual_machine, expected_type=type_hints["virtual_machine"])
            check_type(argname="argument auto_shutdown", value=auto_shutdown, expected_type=type_hints["auto_shutdown"])
            check_type(argname="argument connection_setting", value=connection_setting, expected_type=type_hints["connection_setting"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lab_plan_id", value=lab_plan_id, expected_type=type_hints["lab_plan_id"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument roster", value=roster, expected_type=type_hints["roster"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "security": security,
            "title": title,
            "virtual_machine": virtual_machine,
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
        if auto_shutdown is not None:
            self._values["auto_shutdown"] = auto_shutdown
        if connection_setting is not None:
            self._values["connection_setting"] = connection_setting
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if lab_plan_id is not None:
            self._values["lab_plan_id"] = lab_plan_id
        if network is not None:
            self._values["network"] = network
        if roster is not None:
            self._values["roster"] = roster
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#location LabServiceLab#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#name LabServiceLab#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#resource_group_name LabServiceLab#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security(self) -> "LabServiceLabSecurity":
        '''security block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#security LabServiceLab#security}
        '''
        result = self._values.get("security")
        assert result is not None, "Required property 'security' is missing"
        return typing.cast("LabServiceLabSecurity", result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#title LabServiceLab#title}.'''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_machine(self) -> "LabServiceLabVirtualMachine":
        '''virtual_machine block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#virtual_machine LabServiceLab#virtual_machine}
        '''
        result = self._values.get("virtual_machine")
        assert result is not None, "Required property 'virtual_machine' is missing"
        return typing.cast("LabServiceLabVirtualMachine", result)

    @builtins.property
    def auto_shutdown(self) -> typing.Optional[LabServiceLabAutoShutdown]:
        '''auto_shutdown block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#auto_shutdown LabServiceLab#auto_shutdown}
        '''
        result = self._values.get("auto_shutdown")
        return typing.cast(typing.Optional[LabServiceLabAutoShutdown], result)

    @builtins.property
    def connection_setting(self) -> typing.Optional["LabServiceLabConnectionSetting"]:
        '''connection_setting block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#connection_setting LabServiceLab#connection_setting}
        '''
        result = self._values.get("connection_setting")
        return typing.cast(typing.Optional["LabServiceLabConnectionSetting"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#description LabServiceLab#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#id LabServiceLab#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lab_plan_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lab_plan_id LabServiceLab#lab_plan_id}.'''
        result = self._values.get("lab_plan_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional["LabServiceLabNetwork"]:
        '''network block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#network LabServiceLab#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["LabServiceLabNetwork"], result)

    @builtins.property
    def roster(self) -> typing.Optional["LabServiceLabRoster"]:
        '''roster block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#roster LabServiceLab#roster}
        '''
        result = self._values.get("roster")
        return typing.cast(typing.Optional["LabServiceLabRoster"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#tags LabServiceLab#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LabServiceLabTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#timeouts LabServiceLab#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LabServiceLabTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabConnectionSetting",
    jsii_struct_bases=[],
    name_mapping={
        "client_rdp_access": "clientRdpAccess",
        "client_ssh_access": "clientSshAccess",
    },
)
class LabServiceLabConnectionSetting:
    def __init__(
        self,
        *,
        client_rdp_access: typing.Optional[builtins.str] = None,
        client_ssh_access: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_rdp_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#client_rdp_access LabServiceLab#client_rdp_access}.
        :param client_ssh_access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#client_ssh_access LabServiceLab#client_ssh_access}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6212b97fd9174930e0c28466508f10c22236d1921339d929296f6b07da22700)
            check_type(argname="argument client_rdp_access", value=client_rdp_access, expected_type=type_hints["client_rdp_access"])
            check_type(argname="argument client_ssh_access", value=client_ssh_access, expected_type=type_hints["client_ssh_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_rdp_access is not None:
            self._values["client_rdp_access"] = client_rdp_access
        if client_ssh_access is not None:
            self._values["client_ssh_access"] = client_ssh_access

    @builtins.property
    def client_rdp_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#client_rdp_access LabServiceLab#client_rdp_access}.'''
        result = self._values.get("client_rdp_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ssh_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#client_ssh_access LabServiceLab#client_ssh_access}.'''
        result = self._values.get("client_ssh_access")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabConnectionSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServiceLabConnectionSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabConnectionSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f8ed8956079c814a6d2804f621c706ca96100eb8ad32105268ac26df4bb9be8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientRdpAccess")
    def reset_client_rdp_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientRdpAccess", []))

    @jsii.member(jsii_name="resetClientSshAccess")
    def reset_client_ssh_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSshAccess", []))

    @builtins.property
    @jsii.member(jsii_name="clientRdpAccessInput")
    def client_rdp_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientRdpAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSshAccessInput")
    def client_ssh_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSshAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="clientRdpAccess")
    def client_rdp_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientRdpAccess"))

    @client_rdp_access.setter
    def client_rdp_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ba4076b79228e080e27781bdfb0fe472b3ee320c0672edc9c4649cfbb19a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientRdpAccess", value)

    @builtins.property
    @jsii.member(jsii_name="clientSshAccess")
    def client_ssh_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSshAccess"))

    @client_ssh_access.setter
    def client_ssh_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80d33e4644213af17d50278b7182127b716d90aedfba5d1b3b8b4724371240e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSshAccess", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LabServiceLabConnectionSetting]:
        return typing.cast(typing.Optional[LabServiceLabConnectionSetting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LabServiceLabConnectionSetting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3298fbe3a134eb982fc0fba253ca121ce8c239650d3f070f19732956022c276c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabNetwork",
    jsii_struct_bases=[],
    name_mapping={"subnet_id": "subnetId"},
)
class LabServiceLabNetwork:
    def __init__(self, *, subnet_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#subnet_id LabServiceLab#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5e9d194fcea4f4f79d29b03eea645f03c9dd480de9271437fce2c0e7315d7c)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#subnet_id LabServiceLab#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServiceLabNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a940f43eecad7cbde809dd8a4e3b012d228c046d5dcb67173f4ac0e699ec3a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerId")
    def load_balancer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerId"))

    @builtins.property
    @jsii.member(jsii_name="publicIpId")
    def public_ip_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpId"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9afad06f10d57301d1f7c174e3759c3b333b5033c825f2fefb79ace430bb2eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LabServiceLabNetwork]:
        return typing.cast(typing.Optional[LabServiceLabNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LabServiceLabNetwork]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744b9f284f83c6fb40c26328ce23bb37fa9b4c0057cce5c28109548c7600a584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabRoster",
    jsii_struct_bases=[],
    name_mapping={
        "active_directory_group_id": "activeDirectoryGroupId",
        "lms_instance": "lmsInstance",
        "lti_client_id": "ltiClientId",
        "lti_context_id": "ltiContextId",
        "lti_roster_endpoint": "ltiRosterEndpoint",
    },
)
class LabServiceLabRoster:
    def __init__(
        self,
        *,
        active_directory_group_id: typing.Optional[builtins.str] = None,
        lms_instance: typing.Optional[builtins.str] = None,
        lti_client_id: typing.Optional[builtins.str] = None,
        lti_context_id: typing.Optional[builtins.str] = None,
        lti_roster_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param active_directory_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#active_directory_group_id LabServiceLab#active_directory_group_id}.
        :param lms_instance: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lms_instance LabServiceLab#lms_instance}.
        :param lti_client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lti_client_id LabServiceLab#lti_client_id}.
        :param lti_context_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lti_context_id LabServiceLab#lti_context_id}.
        :param lti_roster_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lti_roster_endpoint LabServiceLab#lti_roster_endpoint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d973528dc1ac319bfae10af7664b108643430e0598ac47765196c30c96a122af)
            check_type(argname="argument active_directory_group_id", value=active_directory_group_id, expected_type=type_hints["active_directory_group_id"])
            check_type(argname="argument lms_instance", value=lms_instance, expected_type=type_hints["lms_instance"])
            check_type(argname="argument lti_client_id", value=lti_client_id, expected_type=type_hints["lti_client_id"])
            check_type(argname="argument lti_context_id", value=lti_context_id, expected_type=type_hints["lti_context_id"])
            check_type(argname="argument lti_roster_endpoint", value=lti_roster_endpoint, expected_type=type_hints["lti_roster_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_directory_group_id is not None:
            self._values["active_directory_group_id"] = active_directory_group_id
        if lms_instance is not None:
            self._values["lms_instance"] = lms_instance
        if lti_client_id is not None:
            self._values["lti_client_id"] = lti_client_id
        if lti_context_id is not None:
            self._values["lti_context_id"] = lti_context_id
        if lti_roster_endpoint is not None:
            self._values["lti_roster_endpoint"] = lti_roster_endpoint

    @builtins.property
    def active_directory_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#active_directory_group_id LabServiceLab#active_directory_group_id}.'''
        result = self._values.get("active_directory_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lms_instance(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lms_instance LabServiceLab#lms_instance}.'''
        result = self._values.get("lms_instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lti_client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lti_client_id LabServiceLab#lti_client_id}.'''
        result = self._values.get("lti_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lti_context_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lti_context_id LabServiceLab#lti_context_id}.'''
        result = self._values.get("lti_context_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lti_roster_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#lti_roster_endpoint LabServiceLab#lti_roster_endpoint}.'''
        result = self._values.get("lti_roster_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabRoster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServiceLabRosterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabRosterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff2160b468b8933a84c89ca40ae9eead4cf1bba910c8a8ef5d56ff7694385f2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActiveDirectoryGroupId")
    def reset_active_directory_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectoryGroupId", []))

    @jsii.member(jsii_name="resetLmsInstance")
    def reset_lms_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLmsInstance", []))

    @jsii.member(jsii_name="resetLtiClientId")
    def reset_lti_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLtiClientId", []))

    @jsii.member(jsii_name="resetLtiContextId")
    def reset_lti_context_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLtiContextId", []))

    @jsii.member(jsii_name="resetLtiRosterEndpoint")
    def reset_lti_roster_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLtiRosterEndpoint", []))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryGroupIdInput")
    def active_directory_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activeDirectoryGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="lmsInstanceInput")
    def lms_instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lmsInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="ltiClientIdInput")
    def lti_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ltiClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ltiContextIdInput")
    def lti_context_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ltiContextIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ltiRosterEndpointInput")
    def lti_roster_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ltiRosterEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryGroupId")
    def active_directory_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activeDirectoryGroupId"))

    @active_directory_group_id.setter
    def active_directory_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6070a8ecff6fe7186814f3f7b3ce44df0fbd573d6b5ad3a7d267b145a6dc3c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectoryGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="lmsInstance")
    def lms_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lmsInstance"))

    @lms_instance.setter
    def lms_instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e60cdb6d98a31044e20369e16754175e93efbd6ab647f7fde8d62075a9ee8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lmsInstance", value)

    @builtins.property
    @jsii.member(jsii_name="ltiClientId")
    def lti_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ltiClientId"))

    @lti_client_id.setter
    def lti_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20dec7c7dc1f0db38b7663c84603f19b2ef667165f629ad1361fb03bdbff0954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ltiClientId", value)

    @builtins.property
    @jsii.member(jsii_name="ltiContextId")
    def lti_context_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ltiContextId"))

    @lti_context_id.setter
    def lti_context_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d409b77c14ee5115e46e3ec8fb0709463386eb6eeacf39bf44b9fc13e6192ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ltiContextId", value)

    @builtins.property
    @jsii.member(jsii_name="ltiRosterEndpoint")
    def lti_roster_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ltiRosterEndpoint"))

    @lti_roster_endpoint.setter
    def lti_roster_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a313ff8ceda92d080aa83554d99159c4e457fdf1ea0733c46b7cf2b8d92910c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ltiRosterEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LabServiceLabRoster]:
        return typing.cast(typing.Optional[LabServiceLabRoster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LabServiceLabRoster]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d97f193950a005b8e0f2f965f397ae7a95779b9da42718143e57ce8e2cfb0dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabSecurity",
    jsii_struct_bases=[],
    name_mapping={"open_access_enabled": "openAccessEnabled"},
)
class LabServiceLabSecurity:
    def __init__(
        self,
        *,
        open_access_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param open_access_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#open_access_enabled LabServiceLab#open_access_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2afb5f0f912128444c9d45666dbaecd3cbae7f4723b9ad0bc4fce31eeab2362)
            check_type(argname="argument open_access_enabled", value=open_access_enabled, expected_type=type_hints["open_access_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "open_access_enabled": open_access_enabled,
        }

    @builtins.property
    def open_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#open_access_enabled LabServiceLab#open_access_enabled}.'''
        result = self._values.get("open_access_enabled")
        assert result is not None, "Required property 'open_access_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabSecurity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServiceLabSecurityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabSecurityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b7f58c4b89b314a50b2c7ec56963a9f7f386b21796772d98a5281abe27207bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="registrationCode")
    def registration_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registrationCode"))

    @builtins.property
    @jsii.member(jsii_name="openAccessEnabledInput")
    def open_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "openAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="openAccessEnabled")
    def open_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "openAccessEnabled"))

    @open_access_enabled.setter
    def open_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf28e4ee26848141d7ba5949adf307b83597853d3465e1d401ccdc69c210b1e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "openAccessEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LabServiceLabSecurity]:
        return typing.cast(typing.Optional[LabServiceLabSecurity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LabServiceLabSecurity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fcdf2ba799d3f7a799006a02563841a39d4277622b54c3bab65e66ce5abdb6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class LabServiceLabTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#create LabServiceLab#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#delete LabServiceLab#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#read LabServiceLab#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#update LabServiceLab#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3815f2b4d1bcdc06f62b884727eb3f48b88ad5a2d70ef544b9e2087a95ba5dbd)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#create LabServiceLab#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#delete LabServiceLab#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#read LabServiceLab#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#update LabServiceLab#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServiceLabTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcfd630280557ab84d1a5fe812c42c18bb0f36a1609b196a8b66ef2412414044)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cdd9fe31d0eba87c48057feda83b1b07b85486026baf4bbfc3263263a7b173f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd2ace516cd8281b6c2bdfa85452fef446f53ca8b660499d6e825c840233b2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b38ffaf5079fcdb9f9ae11b1459300484d8a3d3a9ec7f9f30d94be5c0a1ea24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149747e2b969799b1ee5b867e049843dc76108117c922f929070faa5c7b1b2c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LabServiceLabTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LabServiceLabTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LabServiceLabTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e9bb1ceff8356069dd95bcafd9b233303a2f79bbd1ca406ebd29daac79bba4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabVirtualMachine",
    jsii_struct_bases=[],
    name_mapping={
        "admin_user": "adminUser",
        "image_reference": "imageReference",
        "sku": "sku",
        "additional_capability_gpu_drivers_installed": "additionalCapabilityGpuDriversInstalled",
        "create_option": "createOption",
        "non_admin_user": "nonAdminUser",
        "shared_password_enabled": "sharedPasswordEnabled",
        "usage_quota": "usageQuota",
    },
)
class LabServiceLabVirtualMachine:
    def __init__(
        self,
        *,
        admin_user: typing.Union["LabServiceLabVirtualMachineAdminUser", typing.Dict[builtins.str, typing.Any]],
        image_reference: typing.Union["LabServiceLabVirtualMachineImageReference", typing.Dict[builtins.str, typing.Any]],
        sku: typing.Union["LabServiceLabVirtualMachineSku", typing.Dict[builtins.str, typing.Any]],
        additional_capability_gpu_drivers_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_option: typing.Optional[builtins.str] = None,
        non_admin_user: typing.Optional[typing.Union["LabServiceLabVirtualMachineNonAdminUser", typing.Dict[builtins.str, typing.Any]]] = None,
        shared_password_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        usage_quota: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_user: admin_user block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#admin_user LabServiceLab#admin_user}
        :param image_reference: image_reference block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#image_reference LabServiceLab#image_reference}
        :param sku: sku block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#sku LabServiceLab#sku}
        :param additional_capability_gpu_drivers_installed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#additional_capability_gpu_drivers_installed LabServiceLab#additional_capability_gpu_drivers_installed}.
        :param create_option: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#create_option LabServiceLab#create_option}.
        :param non_admin_user: non_admin_user block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#non_admin_user LabServiceLab#non_admin_user}
        :param shared_password_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#shared_password_enabled LabServiceLab#shared_password_enabled}.
        :param usage_quota: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#usage_quota LabServiceLab#usage_quota}.
        '''
        if isinstance(admin_user, dict):
            admin_user = LabServiceLabVirtualMachineAdminUser(**admin_user)
        if isinstance(image_reference, dict):
            image_reference = LabServiceLabVirtualMachineImageReference(**image_reference)
        if isinstance(sku, dict):
            sku = LabServiceLabVirtualMachineSku(**sku)
        if isinstance(non_admin_user, dict):
            non_admin_user = LabServiceLabVirtualMachineNonAdminUser(**non_admin_user)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e1800bcb2834e8e7ea97e28f66acc8daa9119e997cf05aa03dad715fd9a120)
            check_type(argname="argument admin_user", value=admin_user, expected_type=type_hints["admin_user"])
            check_type(argname="argument image_reference", value=image_reference, expected_type=type_hints["image_reference"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument additional_capability_gpu_drivers_installed", value=additional_capability_gpu_drivers_installed, expected_type=type_hints["additional_capability_gpu_drivers_installed"])
            check_type(argname="argument create_option", value=create_option, expected_type=type_hints["create_option"])
            check_type(argname="argument non_admin_user", value=non_admin_user, expected_type=type_hints["non_admin_user"])
            check_type(argname="argument shared_password_enabled", value=shared_password_enabled, expected_type=type_hints["shared_password_enabled"])
            check_type(argname="argument usage_quota", value=usage_quota, expected_type=type_hints["usage_quota"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_user": admin_user,
            "image_reference": image_reference,
            "sku": sku,
        }
        if additional_capability_gpu_drivers_installed is not None:
            self._values["additional_capability_gpu_drivers_installed"] = additional_capability_gpu_drivers_installed
        if create_option is not None:
            self._values["create_option"] = create_option
        if non_admin_user is not None:
            self._values["non_admin_user"] = non_admin_user
        if shared_password_enabled is not None:
            self._values["shared_password_enabled"] = shared_password_enabled
        if usage_quota is not None:
            self._values["usage_quota"] = usage_quota

    @builtins.property
    def admin_user(self) -> "LabServiceLabVirtualMachineAdminUser":
        '''admin_user block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#admin_user LabServiceLab#admin_user}
        '''
        result = self._values.get("admin_user")
        assert result is not None, "Required property 'admin_user' is missing"
        return typing.cast("LabServiceLabVirtualMachineAdminUser", result)

    @builtins.property
    def image_reference(self) -> "LabServiceLabVirtualMachineImageReference":
        '''image_reference block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#image_reference LabServiceLab#image_reference}
        '''
        result = self._values.get("image_reference")
        assert result is not None, "Required property 'image_reference' is missing"
        return typing.cast("LabServiceLabVirtualMachineImageReference", result)

    @builtins.property
    def sku(self) -> "LabServiceLabVirtualMachineSku":
        '''sku block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#sku LabServiceLab#sku}
        '''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast("LabServiceLabVirtualMachineSku", result)

    @builtins.property
    def additional_capability_gpu_drivers_installed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#additional_capability_gpu_drivers_installed LabServiceLab#additional_capability_gpu_drivers_installed}.'''
        result = self._values.get("additional_capability_gpu_drivers_installed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def create_option(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#create_option LabServiceLab#create_option}.'''
        result = self._values.get("create_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def non_admin_user(
        self,
    ) -> typing.Optional["LabServiceLabVirtualMachineNonAdminUser"]:
        '''non_admin_user block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#non_admin_user LabServiceLab#non_admin_user}
        '''
        result = self._values.get("non_admin_user")
        return typing.cast(typing.Optional["LabServiceLabVirtualMachineNonAdminUser"], result)

    @builtins.property
    def shared_password_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#shared_password_enabled LabServiceLab#shared_password_enabled}.'''
        result = self._values.get("shared_password_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def usage_quota(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#usage_quota LabServiceLab#usage_quota}.'''
        result = self._values.get("usage_quota")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabVirtualMachine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabVirtualMachineAdminUser",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class LabServiceLabVirtualMachineAdminUser:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#password LabServiceLab#password}.
        :param username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#username LabServiceLab#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__322130ee7031face858aad31ae589bff7caacdec54a468f17b12108976014c15)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#password LabServiceLab#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#username LabServiceLab#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabVirtualMachineAdminUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServiceLabVirtualMachineAdminUserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabVirtualMachineAdminUserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55464b1b9e8c46bb595d26e20bc564ca5aaf9f0ee2318471d3ea7516bcd8ecb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6e1702b16ab0b5042fffc470f58ad3b62d52243545ffc81e635976db7d33f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6178df96a21cfd4f2806b3420bab5c47cf5fb9c37cfb952ef8d3a92b2d9b209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LabServiceLabVirtualMachineAdminUser]:
        return typing.cast(typing.Optional[LabServiceLabVirtualMachineAdminUser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LabServiceLabVirtualMachineAdminUser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f259f570b80270b7ddeb9da9dd790de5bf8f99706156b1d7a471e921d91d612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabVirtualMachineImageReference",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "offer": "offer",
        "publisher": "publisher",
        "sku": "sku",
        "version": "version",
    },
)
class LabServiceLabVirtualMachineImageReference:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        offer: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[builtins.str] = None,
        sku: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#id LabServiceLab#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param offer: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#offer LabServiceLab#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#publisher LabServiceLab#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#sku LabServiceLab#sku}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#version LabServiceLab#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611e2219efba2edd956e69e76b807594f71b3e6589242f30cdae0220d7fc6976)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument offer", value=offer, expected_type=type_hints["offer"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if offer is not None:
            self._values["offer"] = offer
        if publisher is not None:
            self._values["publisher"] = publisher
        if sku is not None:
            self._values["sku"] = sku
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#id LabServiceLab#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def offer(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#offer LabServiceLab#offer}.'''
        result = self._values.get("offer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#publisher LabServiceLab#publisher}.'''
        result = self._values.get("publisher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#sku LabServiceLab#sku}.'''
        result = self._values.get("sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#version LabServiceLab#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabVirtualMachineImageReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServiceLabVirtualMachineImageReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabVirtualMachineImageReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb5dd4702de689492b83e833254b6796491cbc25f60b354a9a215347280fbb1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed5c073f71696c9c9c8b474dd75292ecec88452304d28b7e777dfaad35399f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="offer")
    def offer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offer"))

    @offer.setter
    def offer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd4d0a12c32bbfdd641bb9baa76466d3c6891b4ed9862853b5d36dc9cc33b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offer", value)

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f087b546c262de3fdc08bb4fdca26cd9a774158a62bd1b2de1a86460c656bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value)

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb472791b6c36b9b1dcb108fb57dcd0fab4b4d1b864b40a8667d9a88706f6d6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a57ce2cd4ce30b4e3ac1ed14b3191ea7a8128baa5039536d5c89c538a8d67fec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LabServiceLabVirtualMachineImageReference]:
        return typing.cast(typing.Optional[LabServiceLabVirtualMachineImageReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LabServiceLabVirtualMachineImageReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05806116e631dcffb36df94ab65a3d8faf013a90275df187809307238908c666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabVirtualMachineNonAdminUser",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class LabServiceLabVirtualMachineNonAdminUser:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#password LabServiceLab#password}.
        :param username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#username LabServiceLab#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78dfbff18e3421de540f9cd412a3d7922eb00ff8fba4389a28ae4de2b98c61fb)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#password LabServiceLab#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#username LabServiceLab#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabVirtualMachineNonAdminUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServiceLabVirtualMachineNonAdminUserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabVirtualMachineNonAdminUserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c976c99a19175c2dfa97864db354e824eafa836642f0fa44bf747cd0e0422d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18965102dc6370cdaf3077403b4c7d404ae587b2f3aa1be7e1678112128c6a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d2cf3ae2f2a55066e526192d6b463ecedc88bd5fa5117f9a600e7af0df0377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LabServiceLabVirtualMachineNonAdminUser]:
        return typing.cast(typing.Optional[LabServiceLabVirtualMachineNonAdminUser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LabServiceLabVirtualMachineNonAdminUser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742115496ed9dc6437418a8e73d8ce35cc1273e3a07d7b7bedbe7e2dc8b19eee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LabServiceLabVirtualMachineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabVirtualMachineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7c95eecf2761367d1e985b6256364e723d1575dde26d6e181f03e8643807d29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminUser")
    def put_admin_user(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#password LabServiceLab#password}.
        :param username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#username LabServiceLab#username}.
        '''
        value = LabServiceLabVirtualMachineAdminUser(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putAdminUser", [value]))

    @jsii.member(jsii_name="putImageReference")
    def put_image_reference(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        offer: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[builtins.str] = None,
        sku: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#id LabServiceLab#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param offer: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#offer LabServiceLab#offer}.
        :param publisher: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#publisher LabServiceLab#publisher}.
        :param sku: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#sku LabServiceLab#sku}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#version LabServiceLab#version}.
        '''
        value = LabServiceLabVirtualMachineImageReference(
            id=id, offer=offer, publisher=publisher, sku=sku, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putImageReference", [value]))

    @jsii.member(jsii_name="putNonAdminUser")
    def put_non_admin_user(
        self,
        *,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#password LabServiceLab#password}.
        :param username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#username LabServiceLab#username}.
        '''
        value = LabServiceLabVirtualMachineNonAdminUser(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putNonAdminUser", [value]))

    @jsii.member(jsii_name="putSku")
    def put_sku(self, *, capacity: jsii.Number, name: builtins.str) -> None:
        '''
        :param capacity: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#capacity LabServiceLab#capacity}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#name LabServiceLab#name}.
        '''
        value = LabServiceLabVirtualMachineSku(capacity=capacity, name=name)

        return typing.cast(None, jsii.invoke(self, "putSku", [value]))

    @jsii.member(jsii_name="resetAdditionalCapabilityGpuDriversInstalled")
    def reset_additional_capability_gpu_drivers_installed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalCapabilityGpuDriversInstalled", []))

    @jsii.member(jsii_name="resetCreateOption")
    def reset_create_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateOption", []))

    @jsii.member(jsii_name="resetNonAdminUser")
    def reset_non_admin_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonAdminUser", []))

    @jsii.member(jsii_name="resetSharedPasswordEnabled")
    def reset_shared_password_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedPasswordEnabled", []))

    @jsii.member(jsii_name="resetUsageQuota")
    def reset_usage_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsageQuota", []))

    @builtins.property
    @jsii.member(jsii_name="adminUser")
    def admin_user(self) -> LabServiceLabVirtualMachineAdminUserOutputReference:
        return typing.cast(LabServiceLabVirtualMachineAdminUserOutputReference, jsii.get(self, "adminUser"))

    @builtins.property
    @jsii.member(jsii_name="imageReference")
    def image_reference(
        self,
    ) -> LabServiceLabVirtualMachineImageReferenceOutputReference:
        return typing.cast(LabServiceLabVirtualMachineImageReferenceOutputReference, jsii.get(self, "imageReference"))

    @builtins.property
    @jsii.member(jsii_name="nonAdminUser")
    def non_admin_user(self) -> LabServiceLabVirtualMachineNonAdminUserOutputReference:
        return typing.cast(LabServiceLabVirtualMachineNonAdminUserOutputReference, jsii.get(self, "nonAdminUser"))

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> "LabServiceLabVirtualMachineSkuOutputReference":
        return typing.cast("LabServiceLabVirtualMachineSkuOutputReference", jsii.get(self, "sku"))

    @builtins.property
    @jsii.member(jsii_name="additionalCapabilityGpuDriversInstalledInput")
    def additional_capability_gpu_drivers_installed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "additionalCapabilityGpuDriversInstalledInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUserInput")
    def admin_user_input(self) -> typing.Optional[LabServiceLabVirtualMachineAdminUser]:
        return typing.cast(typing.Optional[LabServiceLabVirtualMachineAdminUser], jsii.get(self, "adminUserInput"))

    @builtins.property
    @jsii.member(jsii_name="createOptionInput")
    def create_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="imageReferenceInput")
    def image_reference_input(
        self,
    ) -> typing.Optional[LabServiceLabVirtualMachineImageReference]:
        return typing.cast(typing.Optional[LabServiceLabVirtualMachineImageReference], jsii.get(self, "imageReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="nonAdminUserInput")
    def non_admin_user_input(
        self,
    ) -> typing.Optional[LabServiceLabVirtualMachineNonAdminUser]:
        return typing.cast(typing.Optional[LabServiceLabVirtualMachineNonAdminUser], jsii.get(self, "nonAdminUserInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedPasswordEnabledInput")
    def shared_password_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sharedPasswordEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional["LabServiceLabVirtualMachineSku"]:
        return typing.cast(typing.Optional["LabServiceLabVirtualMachineSku"], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="usageQuotaInput")
    def usage_quota_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usageQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalCapabilityGpuDriversInstalled")
    def additional_capability_gpu_drivers_installed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "additionalCapabilityGpuDriversInstalled"))

    @additional_capability_gpu_drivers_installed.setter
    def additional_capability_gpu_drivers_installed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c1a81e345faaf8e0943cda9e78ea5a7d91fa9e97e84d47002e6a796d1d7b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalCapabilityGpuDriversInstalled", value)

    @builtins.property
    @jsii.member(jsii_name="createOption")
    def create_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createOption"))

    @create_option.setter
    def create_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7883f8bd28a12c29e9e45fa869feb9f83affebde8ac68181fec452230b6bef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createOption", value)

    @builtins.property
    @jsii.member(jsii_name="sharedPasswordEnabled")
    def shared_password_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sharedPasswordEnabled"))

    @shared_password_enabled.setter
    def shared_password_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c11381b742f1358b4be50245782d8ff6f33ea438c05adb48225827b70f8bc70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedPasswordEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="usageQuota")
    def usage_quota(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usageQuota"))

    @usage_quota.setter
    def usage_quota(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8cc276c688b388db088e7fc7bcef88ec9380ff880eca213077d22c7588a93b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usageQuota", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LabServiceLabVirtualMachine]:
        return typing.cast(typing.Optional[LabServiceLabVirtualMachine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LabServiceLabVirtualMachine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cf65131b3794b1fdd9151a001af2003cb9b06705cc8e95cf3c08900878ee4c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabVirtualMachineSku",
    jsii_struct_bases=[],
    name_mapping={"capacity": "capacity", "name": "name"},
)
class LabServiceLabVirtualMachineSku:
    def __init__(self, *, capacity: jsii.Number, name: builtins.str) -> None:
        '''
        :param capacity: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#capacity LabServiceLab#capacity}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#name LabServiceLab#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45352de1d692c4065c10124bb62a6b91bf5fb3f2e2bfb966711ddd126e50d1ea)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity": capacity,
            "name": name,
        }

    @builtins.property
    def capacity(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#capacity LabServiceLab#capacity}.'''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/lab_service_lab#name LabServiceLab#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabServiceLabVirtualMachineSku(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LabServiceLabVirtualMachineSkuOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.labServiceLab.LabServiceLabVirtualMachineSkuOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d02dfe48726c95ddaa71129d8a99cda78ab98861ed63dadc19fec8f4e4582d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a99e1d6f99d5776871c39d24a28e39dd6c86dcf5fa34a36129425f2dc323b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacity", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b2717302cba9e627a2fec1e61560a86f7d47cf3a86172e6554f054bf54fa2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LabServiceLabVirtualMachineSku]:
        return typing.cast(typing.Optional[LabServiceLabVirtualMachineSku], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LabServiceLabVirtualMachineSku],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04062e98318dbb52a8b5723f898c4fbba366a6a5db1e8ebf14b8b66cff3b1252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "LabServiceLab",
    "LabServiceLabAutoShutdown",
    "LabServiceLabAutoShutdownOutputReference",
    "LabServiceLabConfig",
    "LabServiceLabConnectionSetting",
    "LabServiceLabConnectionSettingOutputReference",
    "LabServiceLabNetwork",
    "LabServiceLabNetworkOutputReference",
    "LabServiceLabRoster",
    "LabServiceLabRosterOutputReference",
    "LabServiceLabSecurity",
    "LabServiceLabSecurityOutputReference",
    "LabServiceLabTimeouts",
    "LabServiceLabTimeoutsOutputReference",
    "LabServiceLabVirtualMachine",
    "LabServiceLabVirtualMachineAdminUser",
    "LabServiceLabVirtualMachineAdminUserOutputReference",
    "LabServiceLabVirtualMachineImageReference",
    "LabServiceLabVirtualMachineImageReferenceOutputReference",
    "LabServiceLabVirtualMachineNonAdminUser",
    "LabServiceLabVirtualMachineNonAdminUserOutputReference",
    "LabServiceLabVirtualMachineOutputReference",
    "LabServiceLabVirtualMachineSku",
    "LabServiceLabVirtualMachineSkuOutputReference",
]

publication.publish()

def _typecheckingstub__a623ff5f33e8c555bc1add389562da07826047fc7d1ca85826db176bbc893ee5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    security: typing.Union[LabServiceLabSecurity, typing.Dict[builtins.str, typing.Any]],
    title: builtins.str,
    virtual_machine: typing.Union[LabServiceLabVirtualMachine, typing.Dict[builtins.str, typing.Any]],
    auto_shutdown: typing.Optional[typing.Union[LabServiceLabAutoShutdown, typing.Dict[builtins.str, typing.Any]]] = None,
    connection_setting: typing.Optional[typing.Union[LabServiceLabConnectionSetting, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lab_plan_id: typing.Optional[builtins.str] = None,
    network: typing.Optional[typing.Union[LabServiceLabNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    roster: typing.Optional[typing.Union[LabServiceLabRoster, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LabServiceLabTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fae8973e57a51ec9aaa47dfc184f70c945d3a9e52d0df3e27b0013b57e4ea447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b34c75eb72c48ba5520fa4ecedeb8ded6b6a588655909b026500e81ee7e447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a8d92e1dcbff39c21d2dbc53fab6b1fad0e08fefb8d17da5d834ed2e981736(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf6291d35416ebe367089694c2d8eaa1d0fb97d6bfcc2000e9084270367dd62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623aef57620fb8e3be2dbcef97c1ba498d496bcdf14e8cf5ee55e79db3e53165(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676773229fb4029a8706849dac106cd933f3a45240dad654242a9282239e4c22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ce0e857b0577d008d9f3664cfeb6966c893e5367bbfa393285d9b51af350ae(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a41a6790af7b289e724c3477f9258442b210c27c0b3781031104d3706316eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ce5b8dbbe503bf1cab48f46148fb72c61515d12a13fde2db9fa323fc308c03(
    *,
    disconnect_delay: typing.Optional[builtins.str] = None,
    idle_delay: typing.Optional[builtins.str] = None,
    no_connect_delay: typing.Optional[builtins.str] = None,
    shutdown_on_idle: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d89cf21d40b2733e171c857cbe5922d8d9489afdb5a72c0fdb84f2566abebc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9745ef2b3743b67555c53204f90dada046512965b71e4f3e9feed6971f599f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31100998431cb989ba5af696b37f0017ebbef7feef448f025e91a89b72a94c99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc7cae09c3aa2cd5260305b3dcab1383edc636bcd3e2fae48545dfd07c0e38b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d895e4cd1856e2e751a5aade4ad066fc2472b83f3a688a3cef7984927e1a5a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3eb3ccff5c25b0394475312c3e3ae4a26602186f378fd2d0472caad9f80b90(
    value: typing.Optional[LabServiceLabAutoShutdown],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c78b9bc7a7c2f8396d31417d6933f36126cf7723b3070301cc233c233931d71(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    security: typing.Union[LabServiceLabSecurity, typing.Dict[builtins.str, typing.Any]],
    title: builtins.str,
    virtual_machine: typing.Union[LabServiceLabVirtualMachine, typing.Dict[builtins.str, typing.Any]],
    auto_shutdown: typing.Optional[typing.Union[LabServiceLabAutoShutdown, typing.Dict[builtins.str, typing.Any]]] = None,
    connection_setting: typing.Optional[typing.Union[LabServiceLabConnectionSetting, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lab_plan_id: typing.Optional[builtins.str] = None,
    network: typing.Optional[typing.Union[LabServiceLabNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    roster: typing.Optional[typing.Union[LabServiceLabRoster, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LabServiceLabTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6212b97fd9174930e0c28466508f10c22236d1921339d929296f6b07da22700(
    *,
    client_rdp_access: typing.Optional[builtins.str] = None,
    client_ssh_access: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8ed8956079c814a6d2804f621c706ca96100eb8ad32105268ac26df4bb9be8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ba4076b79228e080e27781bdfb0fe472b3ee320c0672edc9c4649cfbb19a33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80d33e4644213af17d50278b7182127b716d90aedfba5d1b3b8b4724371240e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3298fbe3a134eb982fc0fba253ca121ce8c239650d3f070f19732956022c276c(
    value: typing.Optional[LabServiceLabConnectionSetting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5e9d194fcea4f4f79d29b03eea645f03c9dd480de9271437fce2c0e7315d7c(
    *,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a940f43eecad7cbde809dd8a4e3b012d228c046d5dcb67173f4ac0e699ec3a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9afad06f10d57301d1f7c174e3759c3b333b5033c825f2fefb79ace430bb2eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744b9f284f83c6fb40c26328ce23bb37fa9b4c0057cce5c28109548c7600a584(
    value: typing.Optional[LabServiceLabNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d973528dc1ac319bfae10af7664b108643430e0598ac47765196c30c96a122af(
    *,
    active_directory_group_id: typing.Optional[builtins.str] = None,
    lms_instance: typing.Optional[builtins.str] = None,
    lti_client_id: typing.Optional[builtins.str] = None,
    lti_context_id: typing.Optional[builtins.str] = None,
    lti_roster_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2160b468b8933a84c89ca40ae9eead4cf1bba910c8a8ef5d56ff7694385f2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6070a8ecff6fe7186814f3f7b3ce44df0fbd573d6b5ad3a7d267b145a6dc3c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e60cdb6d98a31044e20369e16754175e93efbd6ab647f7fde8d62075a9ee8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20dec7c7dc1f0db38b7663c84603f19b2ef667165f629ad1361fb03bdbff0954(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d409b77c14ee5115e46e3ec8fb0709463386eb6eeacf39bf44b9fc13e6192ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a313ff8ceda92d080aa83554d99159c4e457fdf1ea0733c46b7cf2b8d92910c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d97f193950a005b8e0f2f965f397ae7a95779b9da42718143e57ce8e2cfb0dc(
    value: typing.Optional[LabServiceLabRoster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2afb5f0f912128444c9d45666dbaecd3cbae7f4723b9ad0bc4fce31eeab2362(
    *,
    open_access_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7f58c4b89b314a50b2c7ec56963a9f7f386b21796772d98a5281abe27207bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf28e4ee26848141d7ba5949adf307b83597853d3465e1d401ccdc69c210b1e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fcdf2ba799d3f7a799006a02563841a39d4277622b54c3bab65e66ce5abdb6e(
    value: typing.Optional[LabServiceLabSecurity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3815f2b4d1bcdc06f62b884727eb3f48b88ad5a2d70ef544b9e2087a95ba5dbd(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfd630280557ab84d1a5fe812c42c18bb0f36a1609b196a8b66ef2412414044(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdd9fe31d0eba87c48057feda83b1b07b85486026baf4bbfc3263263a7b173f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd2ace516cd8281b6c2bdfa85452fef446f53ca8b660499d6e825c840233b2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b38ffaf5079fcdb9f9ae11b1459300484d8a3d3a9ec7f9f30d94be5c0a1ea24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149747e2b969799b1ee5b867e049843dc76108117c922f929070faa5c7b1b2c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e9bb1ceff8356069dd95bcafd9b233303a2f79bbd1ca406ebd29daac79bba4a(
    value: typing.Optional[typing.Union[LabServiceLabTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e1800bcb2834e8e7ea97e28f66acc8daa9119e997cf05aa03dad715fd9a120(
    *,
    admin_user: typing.Union[LabServiceLabVirtualMachineAdminUser, typing.Dict[builtins.str, typing.Any]],
    image_reference: typing.Union[LabServiceLabVirtualMachineImageReference, typing.Dict[builtins.str, typing.Any]],
    sku: typing.Union[LabServiceLabVirtualMachineSku, typing.Dict[builtins.str, typing.Any]],
    additional_capability_gpu_drivers_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_option: typing.Optional[builtins.str] = None,
    non_admin_user: typing.Optional[typing.Union[LabServiceLabVirtualMachineNonAdminUser, typing.Dict[builtins.str, typing.Any]]] = None,
    shared_password_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    usage_quota: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322130ee7031face858aad31ae589bff7caacdec54a468f17b12108976014c15(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55464b1b9e8c46bb595d26e20bc564ca5aaf9f0ee2318471d3ea7516bcd8ecb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6e1702b16ab0b5042fffc470f58ad3b62d52243545ffc81e635976db7d33f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6178df96a21cfd4f2806b3420bab5c47cf5fb9c37cfb952ef8d3a92b2d9b209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f259f570b80270b7ddeb9da9dd790de5bf8f99706156b1d7a471e921d91d612(
    value: typing.Optional[LabServiceLabVirtualMachineAdminUser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611e2219efba2edd956e69e76b807594f71b3e6589242f30cdae0220d7fc6976(
    *,
    id: typing.Optional[builtins.str] = None,
    offer: typing.Optional[builtins.str] = None,
    publisher: typing.Optional[builtins.str] = None,
    sku: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5dd4702de689492b83e833254b6796491cbc25f60b354a9a215347280fbb1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed5c073f71696c9c9c8b474dd75292ecec88452304d28b7e777dfaad35399f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd4d0a12c32bbfdd641bb9baa76466d3c6891b4ed9862853b5d36dc9cc33b40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f087b546c262de3fdc08bb4fdca26cd9a774158a62bd1b2de1a86460c656bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb472791b6c36b9b1dcb108fb57dcd0fab4b4d1b864b40a8667d9a88706f6d6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57ce2cd4ce30b4e3ac1ed14b3191ea7a8128baa5039536d5c89c538a8d67fec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05806116e631dcffb36df94ab65a3d8faf013a90275df187809307238908c666(
    value: typing.Optional[LabServiceLabVirtualMachineImageReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78dfbff18e3421de540f9cd412a3d7922eb00ff8fba4389a28ae4de2b98c61fb(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c976c99a19175c2dfa97864db354e824eafa836642f0fa44bf747cd0e0422d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18965102dc6370cdaf3077403b4c7d404ae587b2f3aa1be7e1678112128c6a71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d2cf3ae2f2a55066e526192d6b463ecedc88bd5fa5117f9a600e7af0df0377(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742115496ed9dc6437418a8e73d8ce35cc1273e3a07d7b7bedbe7e2dc8b19eee(
    value: typing.Optional[LabServiceLabVirtualMachineNonAdminUser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c95eecf2761367d1e985b6256364e723d1575dde26d6e181f03e8643807d29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c1a81e345faaf8e0943cda9e78ea5a7d91fa9e97e84d47002e6a796d1d7b9b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7883f8bd28a12c29e9e45fa869feb9f83affebde8ac68181fec452230b6bef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c11381b742f1358b4be50245782d8ff6f33ea438c05adb48225827b70f8bc70(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8cc276c688b388db088e7fc7bcef88ec9380ff880eca213077d22c7588a93b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf65131b3794b1fdd9151a001af2003cb9b06705cc8e95cf3c08900878ee4c5(
    value: typing.Optional[LabServiceLabVirtualMachine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45352de1d692c4065c10124bb62a6b91bf5fb3f2e2bfb966711ddd126e50d1ea(
    *,
    capacity: jsii.Number,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d02dfe48726c95ddaa71129d8a99cda78ab98861ed63dadc19fec8f4e4582d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a99e1d6f99d5776871c39d24a28e39dd6c86dcf5fa34a36129425f2dc323b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b2717302cba9e627a2fec1e61560a86f7d47cf3a86172e6554f054bf54fa2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04062e98318dbb52a8b5723f898c4fbba366a6a5db1e8ebf14b8b66cff3b1252(
    value: typing.Optional[LabServiceLabVirtualMachineSku],
) -> None:
    """Type checking stubs"""
    pass
