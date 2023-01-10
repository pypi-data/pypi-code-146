'''
# `azurerm_data_factory_integration_runtime_managed`

Refer to the Terraform Registory for docs: [`azurerm_data_factory_integration_runtime_managed`](https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed).
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


class DataFactoryIntegrationRuntimeManaged(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeManaged.DataFactoryIntegrationRuntimeManaged",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed azurerm_data_factory_integration_runtime_managed}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_factory_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        node_size: builtins.str,
        catalog_info: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeManagedCatalogInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_setup_script: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeManagedCustomSetupScript", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        license_type: typing.Optional[builtins.str] = None,
        max_parallel_executions_per_node: typing.Optional[jsii.Number] = None,
        number_of_nodes: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeManagedTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vnet_integration: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeManagedVnetIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed azurerm_data_factory_integration_runtime_managed} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_factory_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#data_factory_id DataFactoryIntegrationRuntimeManaged#data_factory_id}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#location DataFactoryIntegrationRuntimeManaged#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#name DataFactoryIntegrationRuntimeManaged#name}.
        :param node_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#node_size DataFactoryIntegrationRuntimeManaged#node_size}.
        :param catalog_info: catalog_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#catalog_info DataFactoryIntegrationRuntimeManaged#catalog_info}
        :param custom_setup_script: custom_setup_script block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#custom_setup_script DataFactoryIntegrationRuntimeManaged#custom_setup_script}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#description DataFactoryIntegrationRuntimeManaged#description}.
        :param edition: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#edition DataFactoryIntegrationRuntimeManaged#edition}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#id DataFactoryIntegrationRuntimeManaged#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param license_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#license_type DataFactoryIntegrationRuntimeManaged#license_type}.
        :param max_parallel_executions_per_node: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#max_parallel_executions_per_node DataFactoryIntegrationRuntimeManaged#max_parallel_executions_per_node}.
        :param number_of_nodes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#number_of_nodes DataFactoryIntegrationRuntimeManaged#number_of_nodes}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#timeouts DataFactoryIntegrationRuntimeManaged#timeouts}
        :param vnet_integration: vnet_integration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#vnet_integration DataFactoryIntegrationRuntimeManaged#vnet_integration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871af973bbfa308c9f2b07abc6ec81e443998ce17b406dc1e5584824eb9824b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataFactoryIntegrationRuntimeManagedConfig(
            data_factory_id=data_factory_id,
            location=location,
            name=name,
            node_size=node_size,
            catalog_info=catalog_info,
            custom_setup_script=custom_setup_script,
            description=description,
            edition=edition,
            id=id,
            license_type=license_type,
            max_parallel_executions_per_node=max_parallel_executions_per_node,
            number_of_nodes=number_of_nodes,
            timeouts=timeouts,
            vnet_integration=vnet_integration,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putCatalogInfo")
    def put_catalog_info(
        self,
        *,
        server_endpoint: builtins.str,
        administrator_login: typing.Optional[builtins.str] = None,
        administrator_password: typing.Optional[builtins.str] = None,
        pricing_tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param server_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#server_endpoint DataFactoryIntegrationRuntimeManaged#server_endpoint}.
        :param administrator_login: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#administrator_login DataFactoryIntegrationRuntimeManaged#administrator_login}.
        :param administrator_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#administrator_password DataFactoryIntegrationRuntimeManaged#administrator_password}.
        :param pricing_tier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#pricing_tier DataFactoryIntegrationRuntimeManaged#pricing_tier}.
        '''
        value = DataFactoryIntegrationRuntimeManagedCatalogInfo(
            server_endpoint=server_endpoint,
            administrator_login=administrator_login,
            administrator_password=administrator_password,
            pricing_tier=pricing_tier,
        )

        return typing.cast(None, jsii.invoke(self, "putCatalogInfo", [value]))

    @jsii.member(jsii_name="putCustomSetupScript")
    def put_custom_setup_script(
        self,
        *,
        blob_container_uri: builtins.str,
        sas_token: builtins.str,
    ) -> None:
        '''
        :param blob_container_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#blob_container_uri DataFactoryIntegrationRuntimeManaged#blob_container_uri}.
        :param sas_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#sas_token DataFactoryIntegrationRuntimeManaged#sas_token}.
        '''
        value = DataFactoryIntegrationRuntimeManagedCustomSetupScript(
            blob_container_uri=blob_container_uri, sas_token=sas_token
        )

        return typing.cast(None, jsii.invoke(self, "putCustomSetupScript", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#create DataFactoryIntegrationRuntimeManaged#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#delete DataFactoryIntegrationRuntimeManaged#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#read DataFactoryIntegrationRuntimeManaged#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#update DataFactoryIntegrationRuntimeManaged#update}.
        '''
        value = DataFactoryIntegrationRuntimeManagedTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVnetIntegration")
    def put_vnet_integration(
        self,
        *,
        subnet_name: builtins.str,
        vnet_id: builtins.str,
    ) -> None:
        '''
        :param subnet_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#subnet_name DataFactoryIntegrationRuntimeManaged#subnet_name}.
        :param vnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#vnet_id DataFactoryIntegrationRuntimeManaged#vnet_id}.
        '''
        value = DataFactoryIntegrationRuntimeManagedVnetIntegration(
            subnet_name=subnet_name, vnet_id=vnet_id
        )

        return typing.cast(None, jsii.invoke(self, "putVnetIntegration", [value]))

    @jsii.member(jsii_name="resetCatalogInfo")
    def reset_catalog_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalogInfo", []))

    @jsii.member(jsii_name="resetCustomSetupScript")
    def reset_custom_setup_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomSetupScript", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEdition")
    def reset_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdition", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLicenseType")
    def reset_license_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseType", []))

    @jsii.member(jsii_name="resetMaxParallelExecutionsPerNode")
    def reset_max_parallel_executions_per_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxParallelExecutionsPerNode", []))

    @jsii.member(jsii_name="resetNumberOfNodes")
    def reset_number_of_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberOfNodes", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVnetIntegration")
    def reset_vnet_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVnetIntegration", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="catalogInfo")
    def catalog_info(
        self,
    ) -> "DataFactoryIntegrationRuntimeManagedCatalogInfoOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeManagedCatalogInfoOutputReference", jsii.get(self, "catalogInfo"))

    @builtins.property
    @jsii.member(jsii_name="customSetupScript")
    def custom_setup_script(
        self,
    ) -> "DataFactoryIntegrationRuntimeManagedCustomSetupScriptOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeManagedCustomSetupScriptOutputReference", jsii.get(self, "customSetupScript"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataFactoryIntegrationRuntimeManagedTimeoutsOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeManagedTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vnetIntegration")
    def vnet_integration(
        self,
    ) -> "DataFactoryIntegrationRuntimeManagedVnetIntegrationOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeManagedVnetIntegrationOutputReference", jsii.get(self, "vnetIntegration"))

    @builtins.property
    @jsii.member(jsii_name="catalogInfoInput")
    def catalog_info_input(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeManagedCatalogInfo"]:
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeManagedCatalogInfo"], jsii.get(self, "catalogInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="customSetupScriptInput")
    def custom_setup_script_input(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeManagedCustomSetupScript"]:
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeManagedCustomSetupScript"], jsii.get(self, "customSetupScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFactoryIdInput")
    def data_factory_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFactoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="editionInput")
    def edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseTypeInput")
    def license_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxParallelExecutionsPerNodeInput")
    def max_parallel_executions_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxParallelExecutionsPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeSizeInput")
    def node_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfNodesInput")
    def number_of_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["DataFactoryIntegrationRuntimeManagedTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["DataFactoryIntegrationRuntimeManagedTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetIntegrationInput")
    def vnet_integration_input(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeManagedVnetIntegration"]:
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeManagedVnetIntegration"], jsii.get(self, "vnetIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFactoryId")
    def data_factory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataFactoryId"))

    @data_factory_id.setter
    def data_factory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772aa4055d4c627d81deaf1600078f3baa69c947fe1012be6ec7d8d7812e2d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFactoryId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939898fc6bcb76adc4bf1314268a18b30af6af780b775669c39e089e123b6fc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da178b1762a022a4b9a60714930299df13f20e60dd72f8adef8017fabd7bdb1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0475bfd49835fbf4186093fb7db8a046b02e4a66554b0d82f6cc4618c73f4690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @license_type.setter
    def license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cbbf94c9620ef0722e4a4c178ca15c222ba0e6cc7785ef2660713fb3c9d25f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseType", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81d65856f18e691cc39cac747f14f796a5f9b61f1697a8d0b25e8082d776389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="maxParallelExecutionsPerNode")
    def max_parallel_executions_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxParallelExecutionsPerNode"))

    @max_parallel_executions_per_node.setter
    def max_parallel_executions_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3862ee1632831686854d10a19c1e47b903bdc2c1679c6625522bbdb5e2ec0c55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxParallelExecutionsPerNode", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460c7301cbb533f4dbd3ffb4ec7e980549bd7fdecbab0e2949e4678ba99ce276)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nodeSize")
    def node_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeSize"))

    @node_size.setter
    def node_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585da250602ecb8bfcf1cfcdc1028bab2dc45afe18cb1f64675063487a05aecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeSize", value)

    @builtins.property
    @jsii.member(jsii_name="numberOfNodes")
    def number_of_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfNodes"))

    @number_of_nodes.setter
    def number_of_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77393de158111b406e901b24929e2227ab25ed2c84f3ebf30bc85628236ea1d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfNodes", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeManaged.DataFactoryIntegrationRuntimeManagedCatalogInfo",
    jsii_struct_bases=[],
    name_mapping={
        "server_endpoint": "serverEndpoint",
        "administrator_login": "administratorLogin",
        "administrator_password": "administratorPassword",
        "pricing_tier": "pricingTier",
    },
)
class DataFactoryIntegrationRuntimeManagedCatalogInfo:
    def __init__(
        self,
        *,
        server_endpoint: builtins.str,
        administrator_login: typing.Optional[builtins.str] = None,
        administrator_password: typing.Optional[builtins.str] = None,
        pricing_tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param server_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#server_endpoint DataFactoryIntegrationRuntimeManaged#server_endpoint}.
        :param administrator_login: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#administrator_login DataFactoryIntegrationRuntimeManaged#administrator_login}.
        :param administrator_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#administrator_password DataFactoryIntegrationRuntimeManaged#administrator_password}.
        :param pricing_tier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#pricing_tier DataFactoryIntegrationRuntimeManaged#pricing_tier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a199b00d07e280b5c6dac8ae84fb1ed4b8028870dd0c287acefdbd08cfb8859c)
            check_type(argname="argument server_endpoint", value=server_endpoint, expected_type=type_hints["server_endpoint"])
            check_type(argname="argument administrator_login", value=administrator_login, expected_type=type_hints["administrator_login"])
            check_type(argname="argument administrator_password", value=administrator_password, expected_type=type_hints["administrator_password"])
            check_type(argname="argument pricing_tier", value=pricing_tier, expected_type=type_hints["pricing_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server_endpoint": server_endpoint,
        }
        if administrator_login is not None:
            self._values["administrator_login"] = administrator_login
        if administrator_password is not None:
            self._values["administrator_password"] = administrator_password
        if pricing_tier is not None:
            self._values["pricing_tier"] = pricing_tier

    @builtins.property
    def server_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#server_endpoint DataFactoryIntegrationRuntimeManaged#server_endpoint}.'''
        result = self._values.get("server_endpoint")
        assert result is not None, "Required property 'server_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administrator_login(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#administrator_login DataFactoryIntegrationRuntimeManaged#administrator_login}.'''
        result = self._values.get("administrator_login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def administrator_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#administrator_password DataFactoryIntegrationRuntimeManaged#administrator_password}.'''
        result = self._values.get("administrator_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_tier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#pricing_tier DataFactoryIntegrationRuntimeManaged#pricing_tier}.'''
        result = self._values.get("pricing_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeManagedCatalogInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeManagedCatalogInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeManaged.DataFactoryIntegrationRuntimeManagedCatalogInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b10d717053915e518787e7b06bf532691d9e3f114fddf92cd156c0eccbac1f04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdministratorLogin")
    def reset_administrator_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorLogin", []))

    @jsii.member(jsii_name="resetAdministratorPassword")
    def reset_administrator_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorPassword", []))

    @jsii.member(jsii_name="resetPricingTier")
    def reset_pricing_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPricingTier", []))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginInput")
    def administrator_login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorPasswordInput")
    def administrator_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="pricingTierInput")
    def pricing_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingTierInput"))

    @builtins.property
    @jsii.member(jsii_name="serverEndpointInput")
    def server_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorLogin")
    def administrator_login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorLogin"))

    @administrator_login.setter
    def administrator_login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e189abca58d7fc8b1ecbac248cb8e9b90ec242f33ed1cdc2cea814b92d36eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorLogin", value)

    @builtins.property
    @jsii.member(jsii_name="administratorPassword")
    def administrator_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorPassword"))

    @administrator_password.setter
    def administrator_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc90a1985c4cddbad68ebb3e6adc01094244b30616e78f86d07d9466abea88f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorPassword", value)

    @builtins.property
    @jsii.member(jsii_name="pricingTier")
    def pricing_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pricingTier"))

    @pricing_tier.setter
    def pricing_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__322e86736857708102594f8541260e141c539f4481e3013e030405e6ea3f964b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingTier", value)

    @builtins.property
    @jsii.member(jsii_name="serverEndpoint")
    def server_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverEndpoint"))

    @server_endpoint.setter
    def server_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0985ff2706af50b7193115c8b35765d4ce8f9184d71a72e20b8c6c61f5cae49f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeManagedCatalogInfo]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeManagedCatalogInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeManagedCatalogInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325e4447793c20dbc59e89ad535a3ccacdf62fe897b3982f617947bc88dad6f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeManaged.DataFactoryIntegrationRuntimeManagedConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_factory_id": "dataFactoryId",
        "location": "location",
        "name": "name",
        "node_size": "nodeSize",
        "catalog_info": "catalogInfo",
        "custom_setup_script": "customSetupScript",
        "description": "description",
        "edition": "edition",
        "id": "id",
        "license_type": "licenseType",
        "max_parallel_executions_per_node": "maxParallelExecutionsPerNode",
        "number_of_nodes": "numberOfNodes",
        "timeouts": "timeouts",
        "vnet_integration": "vnetIntegration",
    },
)
class DataFactoryIntegrationRuntimeManagedConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        data_factory_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        node_size: builtins.str,
        catalog_info: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedCatalogInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_setup_script: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeManagedCustomSetupScript", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        license_type: typing.Optional[builtins.str] = None,
        max_parallel_executions_per_node: typing.Optional[jsii.Number] = None,
        number_of_nodes: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeManagedTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vnet_integration: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeManagedVnetIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_factory_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#data_factory_id DataFactoryIntegrationRuntimeManaged#data_factory_id}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#location DataFactoryIntegrationRuntimeManaged#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#name DataFactoryIntegrationRuntimeManaged#name}.
        :param node_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#node_size DataFactoryIntegrationRuntimeManaged#node_size}.
        :param catalog_info: catalog_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#catalog_info DataFactoryIntegrationRuntimeManaged#catalog_info}
        :param custom_setup_script: custom_setup_script block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#custom_setup_script DataFactoryIntegrationRuntimeManaged#custom_setup_script}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#description DataFactoryIntegrationRuntimeManaged#description}.
        :param edition: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#edition DataFactoryIntegrationRuntimeManaged#edition}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#id DataFactoryIntegrationRuntimeManaged#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param license_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#license_type DataFactoryIntegrationRuntimeManaged#license_type}.
        :param max_parallel_executions_per_node: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#max_parallel_executions_per_node DataFactoryIntegrationRuntimeManaged#max_parallel_executions_per_node}.
        :param number_of_nodes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#number_of_nodes DataFactoryIntegrationRuntimeManaged#number_of_nodes}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#timeouts DataFactoryIntegrationRuntimeManaged#timeouts}
        :param vnet_integration: vnet_integration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#vnet_integration DataFactoryIntegrationRuntimeManaged#vnet_integration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(catalog_info, dict):
            catalog_info = DataFactoryIntegrationRuntimeManagedCatalogInfo(**catalog_info)
        if isinstance(custom_setup_script, dict):
            custom_setup_script = DataFactoryIntegrationRuntimeManagedCustomSetupScript(**custom_setup_script)
        if isinstance(timeouts, dict):
            timeouts = DataFactoryIntegrationRuntimeManagedTimeouts(**timeouts)
        if isinstance(vnet_integration, dict):
            vnet_integration = DataFactoryIntegrationRuntimeManagedVnetIntegration(**vnet_integration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314c496afa36a1fa1abd44d8f619a19ea308f8200e7f082d44b56fd2fd4d4b1c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_factory_id", value=data_factory_id, expected_type=type_hints["data_factory_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_size", value=node_size, expected_type=type_hints["node_size"])
            check_type(argname="argument catalog_info", value=catalog_info, expected_type=type_hints["catalog_info"])
            check_type(argname="argument custom_setup_script", value=custom_setup_script, expected_type=type_hints["custom_setup_script"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument license_type", value=license_type, expected_type=type_hints["license_type"])
            check_type(argname="argument max_parallel_executions_per_node", value=max_parallel_executions_per_node, expected_type=type_hints["max_parallel_executions_per_node"])
            check_type(argname="argument number_of_nodes", value=number_of_nodes, expected_type=type_hints["number_of_nodes"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vnet_integration", value=vnet_integration, expected_type=type_hints["vnet_integration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_factory_id": data_factory_id,
            "location": location,
            "name": name,
            "node_size": node_size,
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
        if catalog_info is not None:
            self._values["catalog_info"] = catalog_info
        if custom_setup_script is not None:
            self._values["custom_setup_script"] = custom_setup_script
        if description is not None:
            self._values["description"] = description
        if edition is not None:
            self._values["edition"] = edition
        if id is not None:
            self._values["id"] = id
        if license_type is not None:
            self._values["license_type"] = license_type
        if max_parallel_executions_per_node is not None:
            self._values["max_parallel_executions_per_node"] = max_parallel_executions_per_node
        if number_of_nodes is not None:
            self._values["number_of_nodes"] = number_of_nodes
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vnet_integration is not None:
            self._values["vnet_integration"] = vnet_integration

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
    def data_factory_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#data_factory_id DataFactoryIntegrationRuntimeManaged#data_factory_id}.'''
        result = self._values.get("data_factory_id")
        assert result is not None, "Required property 'data_factory_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#location DataFactoryIntegrationRuntimeManaged#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#name DataFactoryIntegrationRuntimeManaged#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#node_size DataFactoryIntegrationRuntimeManaged#node_size}.'''
        result = self._values.get("node_size")
        assert result is not None, "Required property 'node_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def catalog_info(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeManagedCatalogInfo]:
        '''catalog_info block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#catalog_info DataFactoryIntegrationRuntimeManaged#catalog_info}
        '''
        result = self._values.get("catalog_info")
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeManagedCatalogInfo], result)

    @builtins.property
    def custom_setup_script(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeManagedCustomSetupScript"]:
        '''custom_setup_script block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#custom_setup_script DataFactoryIntegrationRuntimeManaged#custom_setup_script}
        '''
        result = self._values.get("custom_setup_script")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeManagedCustomSetupScript"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#description DataFactoryIntegrationRuntimeManaged#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#edition DataFactoryIntegrationRuntimeManaged#edition}.'''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#id DataFactoryIntegrationRuntimeManaged#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#license_type DataFactoryIntegrationRuntimeManaged#license_type}.'''
        result = self._values.get("license_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_parallel_executions_per_node(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#max_parallel_executions_per_node DataFactoryIntegrationRuntimeManaged#max_parallel_executions_per_node}.'''
        result = self._values.get("max_parallel_executions_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#number_of_nodes DataFactoryIntegrationRuntimeManaged#number_of_nodes}.'''
        result = self._values.get("number_of_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeManagedTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#timeouts DataFactoryIntegrationRuntimeManaged#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeManagedTimeouts"], result)

    @builtins.property
    def vnet_integration(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeManagedVnetIntegration"]:
        '''vnet_integration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#vnet_integration DataFactoryIntegrationRuntimeManaged#vnet_integration}
        '''
        result = self._values.get("vnet_integration")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeManagedVnetIntegration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeManagedConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeManaged.DataFactoryIntegrationRuntimeManagedCustomSetupScript",
    jsii_struct_bases=[],
    name_mapping={"blob_container_uri": "blobContainerUri", "sas_token": "sasToken"},
)
class DataFactoryIntegrationRuntimeManagedCustomSetupScript:
    def __init__(
        self,
        *,
        blob_container_uri: builtins.str,
        sas_token: builtins.str,
    ) -> None:
        '''
        :param blob_container_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#blob_container_uri DataFactoryIntegrationRuntimeManaged#blob_container_uri}.
        :param sas_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#sas_token DataFactoryIntegrationRuntimeManaged#sas_token}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22db752a67c8b6cc93e256d8a3592fa950d49140ed1ee79df4027730301440b9)
            check_type(argname="argument blob_container_uri", value=blob_container_uri, expected_type=type_hints["blob_container_uri"])
            check_type(argname="argument sas_token", value=sas_token, expected_type=type_hints["sas_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "blob_container_uri": blob_container_uri,
            "sas_token": sas_token,
        }

    @builtins.property
    def blob_container_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#blob_container_uri DataFactoryIntegrationRuntimeManaged#blob_container_uri}.'''
        result = self._values.get("blob_container_uri")
        assert result is not None, "Required property 'blob_container_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sas_token(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#sas_token DataFactoryIntegrationRuntimeManaged#sas_token}.'''
        result = self._values.get("sas_token")
        assert result is not None, "Required property 'sas_token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeManagedCustomSetupScript(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeManagedCustomSetupScriptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeManaged.DataFactoryIntegrationRuntimeManagedCustomSetupScriptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0bf6addfc7e9f70494c8b8e046ea941f7d496fa2ac74c76627b6d3d7290f19a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="blobContainerUriInput")
    def blob_container_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blobContainerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="sasTokenInput")
    def sas_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sasTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="blobContainerUri")
    def blob_container_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blobContainerUri"))

    @blob_container_uri.setter
    def blob_container_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f419b555c57cc02329e5fcaaac2eb8820d1cf54a57051dbbe152882433a2945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blobContainerUri", value)

    @builtins.property
    @jsii.member(jsii_name="sasToken")
    def sas_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sasToken"))

    @sas_token.setter
    def sas_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7226035a6a730118e0c0cb5c7b18ee152e89b262f0e2e36be6f7517514eaf36f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sasToken", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeManagedCustomSetupScript]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeManagedCustomSetupScript], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeManagedCustomSetupScript],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7853f03d316696017579106349fcc5c5f3764b1cd937246980875d73bf35f621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeManaged.DataFactoryIntegrationRuntimeManagedTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DataFactoryIntegrationRuntimeManagedTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#create DataFactoryIntegrationRuntimeManaged#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#delete DataFactoryIntegrationRuntimeManaged#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#read DataFactoryIntegrationRuntimeManaged#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#update DataFactoryIntegrationRuntimeManaged#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d8c2c9a39845d8f9fbab7716f2dd290eae7fad31c9c007e0ee8e5307fcccfb)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#create DataFactoryIntegrationRuntimeManaged#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#delete DataFactoryIntegrationRuntimeManaged#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#read DataFactoryIntegrationRuntimeManaged#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#update DataFactoryIntegrationRuntimeManaged#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeManagedTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeManagedTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeManaged.DataFactoryIntegrationRuntimeManagedTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__104e50a9830f3ddb784a9bde2167d005430a4380f77f452c019b87ecd48bce84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f4b70a7deb27158e800fb4376c3666b884d6d95f48fcc75896468dd72bf9bc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23c77a851ee9b26c65f1c64e21ef438dc5d9a82eb806a36e4524c2113529ca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e57c59ce52a073bd62e3978116c33f41b6d38d30d2552db1f208e5e71c3bce4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d7cf7778df15595ff4a239c3b105ee247ec2c39a102502508ba684727cddc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0baafb04665a410c0005281e4237c587ca2f21d754c60266a91b9e10f2aa428c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeManaged.DataFactoryIntegrationRuntimeManagedVnetIntegration",
    jsii_struct_bases=[],
    name_mapping={"subnet_name": "subnetName", "vnet_id": "vnetId"},
)
class DataFactoryIntegrationRuntimeManagedVnetIntegration:
    def __init__(self, *, subnet_name: builtins.str, vnet_id: builtins.str) -> None:
        '''
        :param subnet_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#subnet_name DataFactoryIntegrationRuntimeManaged#subnet_name}.
        :param vnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#vnet_id DataFactoryIntegrationRuntimeManaged#vnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25370a22ea19960fff5b28da1f44a42029c2d8799163b78dc4637c4885e97a5)
            check_type(argname="argument subnet_name", value=subnet_name, expected_type=type_hints["subnet_name"])
            check_type(argname="argument vnet_id", value=vnet_id, expected_type=type_hints["vnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_name": subnet_name,
            "vnet_id": vnet_id,
        }

    @builtins.property
    def subnet_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#subnet_name DataFactoryIntegrationRuntimeManaged#subnet_name}.'''
        result = self._values.get("subnet_name")
        assert result is not None, "Required property 'subnet_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_factory_integration_runtime_managed#vnet_id DataFactoryIntegrationRuntimeManaged#vnet_id}.'''
        result = self._values.get("vnet_id")
        assert result is not None, "Required property 'vnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeManagedVnetIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeManagedVnetIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeManaged.DataFactoryIntegrationRuntimeManagedVnetIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed7b78b49b1e60318ceb05a0b9f920cbe980338b5418c0feb4ce6c2907f4664e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="subnetNameInput")
    def subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetIdInput")
    def vnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetName")
    def subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetName"))

    @subnet_name.setter
    def subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf439f97d94c41995174f399074fc88c82aa4185c56fa637b61934c434eb9dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetName", value)

    @builtins.property
    @jsii.member(jsii_name="vnetId")
    def vnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vnetId"))

    @vnet_id.setter
    def vnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85db32d64224043de4bc44d4cb57a732f9a5654c77c5e175599d30bdcce7c750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vnetId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeManagedVnetIntegration]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeManagedVnetIntegration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeManagedVnetIntegration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db76c446dc4e3b84e24f9c1d62cc890b1ac2a6c68d7d5fe46971fcade692a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataFactoryIntegrationRuntimeManaged",
    "DataFactoryIntegrationRuntimeManagedCatalogInfo",
    "DataFactoryIntegrationRuntimeManagedCatalogInfoOutputReference",
    "DataFactoryIntegrationRuntimeManagedConfig",
    "DataFactoryIntegrationRuntimeManagedCustomSetupScript",
    "DataFactoryIntegrationRuntimeManagedCustomSetupScriptOutputReference",
    "DataFactoryIntegrationRuntimeManagedTimeouts",
    "DataFactoryIntegrationRuntimeManagedTimeoutsOutputReference",
    "DataFactoryIntegrationRuntimeManagedVnetIntegration",
    "DataFactoryIntegrationRuntimeManagedVnetIntegrationOutputReference",
]

publication.publish()

def _typecheckingstub__871af973bbfa308c9f2b07abc6ec81e443998ce17b406dc1e5584824eb9824b8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_factory_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    node_size: builtins.str,
    catalog_info: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedCatalogInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_setup_script: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedCustomSetupScript, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    edition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    license_type: typing.Optional[builtins.str] = None,
    max_parallel_executions_per_node: typing.Optional[jsii.Number] = None,
    number_of_nodes: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vnet_integration: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedVnetIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__772aa4055d4c627d81deaf1600078f3baa69c947fe1012be6ec7d8d7812e2d93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939898fc6bcb76adc4bf1314268a18b30af6af780b775669c39e089e123b6fc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da178b1762a022a4b9a60714930299df13f20e60dd72f8adef8017fabd7bdb1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0475bfd49835fbf4186093fb7db8a046b02e4a66554b0d82f6cc4618c73f4690(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cbbf94c9620ef0722e4a4c178ca15c222ba0e6cc7785ef2660713fb3c9d25f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81d65856f18e691cc39cac747f14f796a5f9b61f1697a8d0b25e8082d776389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3862ee1632831686854d10a19c1e47b903bdc2c1679c6625522bbdb5e2ec0c55(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460c7301cbb533f4dbd3ffb4ec7e980549bd7fdecbab0e2949e4678ba99ce276(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585da250602ecb8bfcf1cfcdc1028bab2dc45afe18cb1f64675063487a05aecb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77393de158111b406e901b24929e2227ab25ed2c84f3ebf30bc85628236ea1d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a199b00d07e280b5c6dac8ae84fb1ed4b8028870dd0c287acefdbd08cfb8859c(
    *,
    server_endpoint: builtins.str,
    administrator_login: typing.Optional[builtins.str] = None,
    administrator_password: typing.Optional[builtins.str] = None,
    pricing_tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10d717053915e518787e7b06bf532691d9e3f114fddf92cd156c0eccbac1f04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e189abca58d7fc8b1ecbac248cb8e9b90ec242f33ed1cdc2cea814b92d36eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc90a1985c4cddbad68ebb3e6adc01094244b30616e78f86d07d9466abea88f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322e86736857708102594f8541260e141c539f4481e3013e030405e6ea3f964b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0985ff2706af50b7193115c8b35765d4ce8f9184d71a72e20b8c6c61f5cae49f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325e4447793c20dbc59e89ad535a3ccacdf62fe897b3982f617947bc88dad6f6(
    value: typing.Optional[DataFactoryIntegrationRuntimeManagedCatalogInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314c496afa36a1fa1abd44d8f619a19ea308f8200e7f082d44b56fd2fd4d4b1c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_factory_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    node_size: builtins.str,
    catalog_info: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedCatalogInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_setup_script: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedCustomSetupScript, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    edition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    license_type: typing.Optional[builtins.str] = None,
    max_parallel_executions_per_node: typing.Optional[jsii.Number] = None,
    number_of_nodes: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vnet_integration: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedVnetIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22db752a67c8b6cc93e256d8a3592fa950d49140ed1ee79df4027730301440b9(
    *,
    blob_container_uri: builtins.str,
    sas_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0bf6addfc7e9f70494c8b8e046ea941f7d496fa2ac74c76627b6d3d7290f19a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f419b555c57cc02329e5fcaaac2eb8820d1cf54a57051dbbe152882433a2945(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7226035a6a730118e0c0cb5c7b18ee152e89b262f0e2e36be6f7517514eaf36f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7853f03d316696017579106349fcc5c5f3764b1cd937246980875d73bf35f621(
    value: typing.Optional[DataFactoryIntegrationRuntimeManagedCustomSetupScript],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d8c2c9a39845d8f9fbab7716f2dd290eae7fad31c9c007e0ee8e5307fcccfb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104e50a9830f3ddb784a9bde2167d005430a4380f77f452c019b87ecd48bce84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4b70a7deb27158e800fb4376c3666b884d6d95f48fcc75896468dd72bf9bc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23c77a851ee9b26c65f1c64e21ef438dc5d9a82eb806a36e4524c2113529ca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57c59ce52a073bd62e3978116c33f41b6d38d30d2552db1f208e5e71c3bce4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d7cf7778df15595ff4a239c3b105ee247ec2c39a102502508ba684727cddc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0baafb04665a410c0005281e4237c587ca2f21d754c60266a91b9e10f2aa428c(
    value: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeManagedTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25370a22ea19960fff5b28da1f44a42029c2d8799163b78dc4637c4885e97a5(
    *,
    subnet_name: builtins.str,
    vnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7b78b49b1e60318ceb05a0b9f920cbe980338b5418c0feb4ce6c2907f4664e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf439f97d94c41995174f399074fc88c82aa4185c56fa637b61934c434eb9dd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85db32d64224043de4bc44d4cb57a732f9a5654c77c5e175599d30bdcce7c750(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db76c446dc4e3b84e24f9c1d62cc890b1ac2a6c68d7d5fe46971fcade692a58(
    value: typing.Optional[DataFactoryIntegrationRuntimeManagedVnetIntegration],
) -> None:
    """Type checking stubs"""
    pass
