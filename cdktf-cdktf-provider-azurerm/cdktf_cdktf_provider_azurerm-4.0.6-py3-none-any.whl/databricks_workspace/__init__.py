'''
# `azurerm_databricks_workspace`

Refer to the Terraform Registory for docs: [`azurerm_databricks_workspace`](https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace).
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


class DatabricksWorkspace(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databricksWorkspace.DatabricksWorkspace",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace azurerm_databricks_workspace}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku: builtins.str,
        customer_managed_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_parameters: typing.Optional[typing.Union["DatabricksWorkspaceCustomParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        load_balancer_backend_address_pool_id: typing.Optional[builtins.str] = None,
        managed_resource_group_name: typing.Optional[builtins.str] = None,
        managed_services_cmk_key_vault_key_id: typing.Optional[builtins.str] = None,
        network_security_group_rules_required: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DatabricksWorkspaceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace azurerm_databricks_workspace} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#location DatabricksWorkspace#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#name DatabricksWorkspace#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#resource_group_name DatabricksWorkspace#resource_group_name}.
        :param sku: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#sku DatabricksWorkspace#sku}.
        :param customer_managed_key_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#customer_managed_key_enabled DatabricksWorkspace#customer_managed_key_enabled}.
        :param custom_parameters: custom_parameters block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#custom_parameters DatabricksWorkspace#custom_parameters}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#id DatabricksWorkspace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param infrastructure_encryption_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#infrastructure_encryption_enabled DatabricksWorkspace#infrastructure_encryption_enabled}.
        :param load_balancer_backend_address_pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#load_balancer_backend_address_pool_id DatabricksWorkspace#load_balancer_backend_address_pool_id}.
        :param managed_resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#managed_resource_group_name DatabricksWorkspace#managed_resource_group_name}.
        :param managed_services_cmk_key_vault_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#managed_services_cmk_key_vault_key_id DatabricksWorkspace#managed_services_cmk_key_vault_key_id}.
        :param network_security_group_rules_required: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#network_security_group_rules_required DatabricksWorkspace#network_security_group_rules_required}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_network_access_enabled DatabricksWorkspace#public_network_access_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#tags DatabricksWorkspace#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#timeouts DatabricksWorkspace#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1accdd55672c74ed4c70d65a9cd0ab85befb9969d93e94ec2d3ff885ba76e78)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DatabricksWorkspaceConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            sku=sku,
            customer_managed_key_enabled=customer_managed_key_enabled,
            custom_parameters=custom_parameters,
            id=id,
            infrastructure_encryption_enabled=infrastructure_encryption_enabled,
            load_balancer_backend_address_pool_id=load_balancer_backend_address_pool_id,
            managed_resource_group_name=managed_resource_group_name,
            managed_services_cmk_key_vault_key_id=managed_services_cmk_key_vault_key_id,
            network_security_group_rules_required=network_security_group_rules_required,
            public_network_access_enabled=public_network_access_enabled,
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

    @jsii.member(jsii_name="putCustomParameters")
    def put_custom_parameters(
        self,
        *,
        machine_learning_workspace_id: typing.Optional[builtins.str] = None,
        nat_gateway_name: typing.Optional[builtins.str] = None,
        no_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_subnet_name: typing.Optional[builtins.str] = None,
        private_subnet_network_security_group_association_id: typing.Optional[builtins.str] = None,
        public_ip_name: typing.Optional[builtins.str] = None,
        public_subnet_name: typing.Optional[builtins.str] = None,
        public_subnet_network_security_group_association_id: typing.Optional[builtins.str] = None,
        storage_account_name: typing.Optional[builtins.str] = None,
        storage_account_sku_name: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
        vnet_address_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param machine_learning_workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#machine_learning_workspace_id DatabricksWorkspace#machine_learning_workspace_id}.
        :param nat_gateway_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#nat_gateway_name DatabricksWorkspace#nat_gateway_name}.
        :param no_public_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#no_public_ip DatabricksWorkspace#no_public_ip}.
        :param private_subnet_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#private_subnet_name DatabricksWorkspace#private_subnet_name}.
        :param private_subnet_network_security_group_association_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#private_subnet_network_security_group_association_id DatabricksWorkspace#private_subnet_network_security_group_association_id}.
        :param public_ip_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_ip_name DatabricksWorkspace#public_ip_name}.
        :param public_subnet_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_subnet_name DatabricksWorkspace#public_subnet_name}.
        :param public_subnet_network_security_group_association_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_subnet_network_security_group_association_id DatabricksWorkspace#public_subnet_network_security_group_association_id}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#storage_account_name DatabricksWorkspace#storage_account_name}.
        :param storage_account_sku_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#storage_account_sku_name DatabricksWorkspace#storage_account_sku_name}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#virtual_network_id DatabricksWorkspace#virtual_network_id}.
        :param vnet_address_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#vnet_address_prefix DatabricksWorkspace#vnet_address_prefix}.
        '''
        value = DatabricksWorkspaceCustomParameters(
            machine_learning_workspace_id=machine_learning_workspace_id,
            nat_gateway_name=nat_gateway_name,
            no_public_ip=no_public_ip,
            private_subnet_name=private_subnet_name,
            private_subnet_network_security_group_association_id=private_subnet_network_security_group_association_id,
            public_ip_name=public_ip_name,
            public_subnet_name=public_subnet_name,
            public_subnet_network_security_group_association_id=public_subnet_network_security_group_association_id,
            storage_account_name=storage_account_name,
            storage_account_sku_name=storage_account_sku_name,
            virtual_network_id=virtual_network_id,
            vnet_address_prefix=vnet_address_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomParameters", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#create DatabricksWorkspace#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#delete DatabricksWorkspace#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#read DatabricksWorkspace#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#update DatabricksWorkspace#update}.
        '''
        value = DatabricksWorkspaceTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomerManagedKeyEnabled")
    def reset_customer_managed_key_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedKeyEnabled", []))

    @jsii.member(jsii_name="resetCustomParameters")
    def reset_custom_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomParameters", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInfrastructureEncryptionEnabled")
    def reset_infrastructure_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfrastructureEncryptionEnabled", []))

    @jsii.member(jsii_name="resetLoadBalancerBackendAddressPoolId")
    def reset_load_balancer_backend_address_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerBackendAddressPoolId", []))

    @jsii.member(jsii_name="resetManagedResourceGroupName")
    def reset_managed_resource_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedResourceGroupName", []))

    @jsii.member(jsii_name="resetManagedServicesCmkKeyVaultKeyId")
    def reset_managed_services_cmk_key_vault_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedServicesCmkKeyVaultKeyId", []))

    @jsii.member(jsii_name="resetNetworkSecurityGroupRulesRequired")
    def reset_network_security_group_rules_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkSecurityGroupRulesRequired", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

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
    @jsii.member(jsii_name="customParameters")
    def custom_parameters(self) -> "DatabricksWorkspaceCustomParametersOutputReference":
        return typing.cast("DatabricksWorkspaceCustomParametersOutputReference", jsii.get(self, "customParameters"))

    @builtins.property
    @jsii.member(jsii_name="managedResourceGroupId")
    def managed_resource_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedResourceGroupId"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdentity")
    def storage_account_identity(
        self,
    ) -> "DatabricksWorkspaceStorageAccountIdentityList":
        return typing.cast("DatabricksWorkspaceStorageAccountIdentityList", jsii.get(self, "storageAccountIdentity"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DatabricksWorkspaceTimeoutsOutputReference":
        return typing.cast("DatabricksWorkspaceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @builtins.property
    @jsii.member(jsii_name="workspaceUrl")
    def workspace_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceUrl"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKeyEnabledInput")
    def customer_managed_key_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customerManagedKeyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="customParametersInput")
    def custom_parameters_input(
        self,
    ) -> typing.Optional["DatabricksWorkspaceCustomParameters"]:
        return typing.cast(typing.Optional["DatabricksWorkspaceCustomParameters"], jsii.get(self, "customParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureEncryptionEnabledInput")
    def infrastructure_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "infrastructureEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerBackendAddressPoolIdInput")
    def load_balancer_backend_address_pool_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerBackendAddressPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedResourceGroupNameInput")
    def managed_resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="managedServicesCmkKeyVaultKeyIdInput")
    def managed_services_cmk_key_vault_key_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedServicesCmkKeyVaultKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkSecurityGroupRulesRequiredInput")
    def network_security_group_rules_required_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkSecurityGroupRulesRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["DatabricksWorkspaceTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["DatabricksWorkspaceTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKeyEnabled")
    def customer_managed_key_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customerManagedKeyEnabled"))

    @customer_managed_key_enabled.setter
    def customer_managed_key_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a200daa3aafb5b77f94e6293e70ab5c66415181b58e8a4b770f21bdb68c7db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerManagedKeyEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__200198470356fbd098dd7f3d327c79899625f4779212b73d1233d29bc5b935ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="infrastructureEncryptionEnabled")
    def infrastructure_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "infrastructureEncryptionEnabled"))

    @infrastructure_encryption_enabled.setter
    def infrastructure_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5000e65582b4036adce35b6c7f50ae801f43ccc64a6797b640e332215372079c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureEncryptionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerBackendAddressPoolId")
    def load_balancer_backend_address_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerBackendAddressPoolId"))

    @load_balancer_backend_address_pool_id.setter
    def load_balancer_backend_address_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8fb131fa353575ca9152a8dcaf53c547cb612f0b44ac01f43042ae15be85d7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerBackendAddressPoolId", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9dfb92437233a578675967c90ce3217a30dc7ba115cc11d61dade9bb7d076f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="managedResourceGroupName")
    def managed_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedResourceGroupName"))

    @managed_resource_group_name.setter
    def managed_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0c4534998b6fa56910e5bf58d5872a0d0366759492057db4c93a5e645eb94a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedResourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="managedServicesCmkKeyVaultKeyId")
    def managed_services_cmk_key_vault_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedServicesCmkKeyVaultKeyId"))

    @managed_services_cmk_key_vault_key_id.setter
    def managed_services_cmk_key_vault_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6412a79a8a29de21db9b2f88f52328ead5f2e4d146b7d08ba26c1e9d6bf0df24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedServicesCmkKeyVaultKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e09e9bdfb9330370247fc7a4b42e532d2599ded55a9be712a25dfbbd34f359c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkSecurityGroupRulesRequired")
    def network_security_group_rules_required(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkSecurityGroupRulesRequired"))

    @network_security_group_rules_required.setter
    def network_security_group_rules_required(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a94649129d64db57f647c431f1ff795a6a1cb511e59527ff0ac10118753b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkSecurityGroupRulesRequired", value)

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabled")
    def public_network_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicNetworkAccessEnabled"))

    @public_network_access_enabled.setter
    def public_network_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b614c454302794eb967c218ccd3dda411b211e5cf44161d2758aadbb6560adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c514befacf4f7b22ad9afb2b9f4b2791266dc039b035e01b61520873926218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2f707f8e9aa15da4b50a6cee946f0ea88283dd382954ae65b598f9ff3b2b85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc751b09cde6afa6a7056f936da9719d94c1bd39e005070a2772bedf7c819bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databricksWorkspace.DatabricksWorkspaceConfig",
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
        "sku": "sku",
        "customer_managed_key_enabled": "customerManagedKeyEnabled",
        "custom_parameters": "customParameters",
        "id": "id",
        "infrastructure_encryption_enabled": "infrastructureEncryptionEnabled",
        "load_balancer_backend_address_pool_id": "loadBalancerBackendAddressPoolId",
        "managed_resource_group_name": "managedResourceGroupName",
        "managed_services_cmk_key_vault_key_id": "managedServicesCmkKeyVaultKeyId",
        "network_security_group_rules_required": "networkSecurityGroupRulesRequired",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class DatabricksWorkspaceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        sku: builtins.str,
        customer_managed_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_parameters: typing.Optional[typing.Union["DatabricksWorkspaceCustomParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        load_balancer_backend_address_pool_id: typing.Optional[builtins.str] = None,
        managed_resource_group_name: typing.Optional[builtins.str] = None,
        managed_services_cmk_key_vault_key_id: typing.Optional[builtins.str] = None,
        network_security_group_rules_required: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DatabricksWorkspaceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#location DatabricksWorkspace#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#name DatabricksWorkspace#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#resource_group_name DatabricksWorkspace#resource_group_name}.
        :param sku: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#sku DatabricksWorkspace#sku}.
        :param customer_managed_key_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#customer_managed_key_enabled DatabricksWorkspace#customer_managed_key_enabled}.
        :param custom_parameters: custom_parameters block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#custom_parameters DatabricksWorkspace#custom_parameters}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#id DatabricksWorkspace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param infrastructure_encryption_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#infrastructure_encryption_enabled DatabricksWorkspace#infrastructure_encryption_enabled}.
        :param load_balancer_backend_address_pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#load_balancer_backend_address_pool_id DatabricksWorkspace#load_balancer_backend_address_pool_id}.
        :param managed_resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#managed_resource_group_name DatabricksWorkspace#managed_resource_group_name}.
        :param managed_services_cmk_key_vault_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#managed_services_cmk_key_vault_key_id DatabricksWorkspace#managed_services_cmk_key_vault_key_id}.
        :param network_security_group_rules_required: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#network_security_group_rules_required DatabricksWorkspace#network_security_group_rules_required}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_network_access_enabled DatabricksWorkspace#public_network_access_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#tags DatabricksWorkspace#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#timeouts DatabricksWorkspace#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_parameters, dict):
            custom_parameters = DatabricksWorkspaceCustomParameters(**custom_parameters)
        if isinstance(timeouts, dict):
            timeouts = DatabricksWorkspaceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6b8d0cd8473f8f24da00c4dd5a77bc2079ccedca5ed46f8799a75e5f40320b)
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
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument customer_managed_key_enabled", value=customer_managed_key_enabled, expected_type=type_hints["customer_managed_key_enabled"])
            check_type(argname="argument custom_parameters", value=custom_parameters, expected_type=type_hints["custom_parameters"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument infrastructure_encryption_enabled", value=infrastructure_encryption_enabled, expected_type=type_hints["infrastructure_encryption_enabled"])
            check_type(argname="argument load_balancer_backend_address_pool_id", value=load_balancer_backend_address_pool_id, expected_type=type_hints["load_balancer_backend_address_pool_id"])
            check_type(argname="argument managed_resource_group_name", value=managed_resource_group_name, expected_type=type_hints["managed_resource_group_name"])
            check_type(argname="argument managed_services_cmk_key_vault_key_id", value=managed_services_cmk_key_vault_key_id, expected_type=type_hints["managed_services_cmk_key_vault_key_id"])
            check_type(argname="argument network_security_group_rules_required", value=network_security_group_rules_required, expected_type=type_hints["network_security_group_rules_required"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "sku": sku,
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
        if customer_managed_key_enabled is not None:
            self._values["customer_managed_key_enabled"] = customer_managed_key_enabled
        if custom_parameters is not None:
            self._values["custom_parameters"] = custom_parameters
        if id is not None:
            self._values["id"] = id
        if infrastructure_encryption_enabled is not None:
            self._values["infrastructure_encryption_enabled"] = infrastructure_encryption_enabled
        if load_balancer_backend_address_pool_id is not None:
            self._values["load_balancer_backend_address_pool_id"] = load_balancer_backend_address_pool_id
        if managed_resource_group_name is not None:
            self._values["managed_resource_group_name"] = managed_resource_group_name
        if managed_services_cmk_key_vault_key_id is not None:
            self._values["managed_services_cmk_key_vault_key_id"] = managed_services_cmk_key_vault_key_id
        if network_security_group_rules_required is not None:
            self._values["network_security_group_rules_required"] = network_security_group_rules_required
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#location DatabricksWorkspace#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#name DatabricksWorkspace#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#resource_group_name DatabricksWorkspace#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#sku DatabricksWorkspace#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def customer_managed_key_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#customer_managed_key_enabled DatabricksWorkspace#customer_managed_key_enabled}.'''
        result = self._values.get("customer_managed_key_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom_parameters(
        self,
    ) -> typing.Optional["DatabricksWorkspaceCustomParameters"]:
        '''custom_parameters block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#custom_parameters DatabricksWorkspace#custom_parameters}
        '''
        result = self._values.get("custom_parameters")
        return typing.cast(typing.Optional["DatabricksWorkspaceCustomParameters"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#id DatabricksWorkspace#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def infrastructure_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#infrastructure_encryption_enabled DatabricksWorkspace#infrastructure_encryption_enabled}.'''
        result = self._values.get("infrastructure_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def load_balancer_backend_address_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#load_balancer_backend_address_pool_id DatabricksWorkspace#load_balancer_backend_address_pool_id}.'''
        result = self._values.get("load_balancer_backend_address_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_resource_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#managed_resource_group_name DatabricksWorkspace#managed_resource_group_name}.'''
        result = self._values.get("managed_resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_services_cmk_key_vault_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#managed_services_cmk_key_vault_key_id DatabricksWorkspace#managed_services_cmk_key_vault_key_id}.'''
        result = self._values.get("managed_services_cmk_key_vault_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_security_group_rules_required(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#network_security_group_rules_required DatabricksWorkspace#network_security_group_rules_required}.'''
        result = self._values.get("network_security_group_rules_required")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_network_access_enabled DatabricksWorkspace#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#tags DatabricksWorkspace#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DatabricksWorkspaceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#timeouts DatabricksWorkspace#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DatabricksWorkspaceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabricksWorkspaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databricksWorkspace.DatabricksWorkspaceCustomParameters",
    jsii_struct_bases=[],
    name_mapping={
        "machine_learning_workspace_id": "machineLearningWorkspaceId",
        "nat_gateway_name": "natGatewayName",
        "no_public_ip": "noPublicIp",
        "private_subnet_name": "privateSubnetName",
        "private_subnet_network_security_group_association_id": "privateSubnetNetworkSecurityGroupAssociationId",
        "public_ip_name": "publicIpName",
        "public_subnet_name": "publicSubnetName",
        "public_subnet_network_security_group_association_id": "publicSubnetNetworkSecurityGroupAssociationId",
        "storage_account_name": "storageAccountName",
        "storage_account_sku_name": "storageAccountSkuName",
        "virtual_network_id": "virtualNetworkId",
        "vnet_address_prefix": "vnetAddressPrefix",
    },
)
class DatabricksWorkspaceCustomParameters:
    def __init__(
        self,
        *,
        machine_learning_workspace_id: typing.Optional[builtins.str] = None,
        nat_gateway_name: typing.Optional[builtins.str] = None,
        no_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_subnet_name: typing.Optional[builtins.str] = None,
        private_subnet_network_security_group_association_id: typing.Optional[builtins.str] = None,
        public_ip_name: typing.Optional[builtins.str] = None,
        public_subnet_name: typing.Optional[builtins.str] = None,
        public_subnet_network_security_group_association_id: typing.Optional[builtins.str] = None,
        storage_account_name: typing.Optional[builtins.str] = None,
        storage_account_sku_name: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
        vnet_address_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param machine_learning_workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#machine_learning_workspace_id DatabricksWorkspace#machine_learning_workspace_id}.
        :param nat_gateway_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#nat_gateway_name DatabricksWorkspace#nat_gateway_name}.
        :param no_public_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#no_public_ip DatabricksWorkspace#no_public_ip}.
        :param private_subnet_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#private_subnet_name DatabricksWorkspace#private_subnet_name}.
        :param private_subnet_network_security_group_association_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#private_subnet_network_security_group_association_id DatabricksWorkspace#private_subnet_network_security_group_association_id}.
        :param public_ip_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_ip_name DatabricksWorkspace#public_ip_name}.
        :param public_subnet_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_subnet_name DatabricksWorkspace#public_subnet_name}.
        :param public_subnet_network_security_group_association_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_subnet_network_security_group_association_id DatabricksWorkspace#public_subnet_network_security_group_association_id}.
        :param storage_account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#storage_account_name DatabricksWorkspace#storage_account_name}.
        :param storage_account_sku_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#storage_account_sku_name DatabricksWorkspace#storage_account_sku_name}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#virtual_network_id DatabricksWorkspace#virtual_network_id}.
        :param vnet_address_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#vnet_address_prefix DatabricksWorkspace#vnet_address_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1780f82849a31d7e8dc5c3fbdfe772e90e96289147d09fbfb2ea7ffc0503a6f)
            check_type(argname="argument machine_learning_workspace_id", value=machine_learning_workspace_id, expected_type=type_hints["machine_learning_workspace_id"])
            check_type(argname="argument nat_gateway_name", value=nat_gateway_name, expected_type=type_hints["nat_gateway_name"])
            check_type(argname="argument no_public_ip", value=no_public_ip, expected_type=type_hints["no_public_ip"])
            check_type(argname="argument private_subnet_name", value=private_subnet_name, expected_type=type_hints["private_subnet_name"])
            check_type(argname="argument private_subnet_network_security_group_association_id", value=private_subnet_network_security_group_association_id, expected_type=type_hints["private_subnet_network_security_group_association_id"])
            check_type(argname="argument public_ip_name", value=public_ip_name, expected_type=type_hints["public_ip_name"])
            check_type(argname="argument public_subnet_name", value=public_subnet_name, expected_type=type_hints["public_subnet_name"])
            check_type(argname="argument public_subnet_network_security_group_association_id", value=public_subnet_network_security_group_association_id, expected_type=type_hints["public_subnet_network_security_group_association_id"])
            check_type(argname="argument storage_account_name", value=storage_account_name, expected_type=type_hints["storage_account_name"])
            check_type(argname="argument storage_account_sku_name", value=storage_account_sku_name, expected_type=type_hints["storage_account_sku_name"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
            check_type(argname="argument vnet_address_prefix", value=vnet_address_prefix, expected_type=type_hints["vnet_address_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if machine_learning_workspace_id is not None:
            self._values["machine_learning_workspace_id"] = machine_learning_workspace_id
        if nat_gateway_name is not None:
            self._values["nat_gateway_name"] = nat_gateway_name
        if no_public_ip is not None:
            self._values["no_public_ip"] = no_public_ip
        if private_subnet_name is not None:
            self._values["private_subnet_name"] = private_subnet_name
        if private_subnet_network_security_group_association_id is not None:
            self._values["private_subnet_network_security_group_association_id"] = private_subnet_network_security_group_association_id
        if public_ip_name is not None:
            self._values["public_ip_name"] = public_ip_name
        if public_subnet_name is not None:
            self._values["public_subnet_name"] = public_subnet_name
        if public_subnet_network_security_group_association_id is not None:
            self._values["public_subnet_network_security_group_association_id"] = public_subnet_network_security_group_association_id
        if storage_account_name is not None:
            self._values["storage_account_name"] = storage_account_name
        if storage_account_sku_name is not None:
            self._values["storage_account_sku_name"] = storage_account_sku_name
        if virtual_network_id is not None:
            self._values["virtual_network_id"] = virtual_network_id
        if vnet_address_prefix is not None:
            self._values["vnet_address_prefix"] = vnet_address_prefix

    @builtins.property
    def machine_learning_workspace_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#machine_learning_workspace_id DatabricksWorkspace#machine_learning_workspace_id}.'''
        result = self._values.get("machine_learning_workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nat_gateway_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#nat_gateway_name DatabricksWorkspace#nat_gateway_name}.'''
        result = self._values.get("nat_gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#no_public_ip DatabricksWorkspace#no_public_ip}.'''
        result = self._values.get("no_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_subnet_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#private_subnet_name DatabricksWorkspace#private_subnet_name}.'''
        result = self._values.get("private_subnet_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_subnet_network_security_group_association_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#private_subnet_network_security_group_association_id DatabricksWorkspace#private_subnet_network_security_group_association_id}.'''
        result = self._values.get("private_subnet_network_security_group_association_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ip_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_ip_name DatabricksWorkspace#public_ip_name}.'''
        result = self._values.get("public_ip_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_subnet_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_subnet_name DatabricksWorkspace#public_subnet_name}.'''
        result = self._values.get("public_subnet_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_subnet_network_security_group_association_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#public_subnet_network_security_group_association_id DatabricksWorkspace#public_subnet_network_security_group_association_id}.'''
        result = self._values.get("public_subnet_network_security_group_association_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#storage_account_name DatabricksWorkspace#storage_account_name}.'''
        result = self._values.get("storage_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_sku_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#storage_account_sku_name DatabricksWorkspace#storage_account_sku_name}.'''
        result = self._values.get("storage_account_sku_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#virtual_network_id DatabricksWorkspace#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vnet_address_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#vnet_address_prefix DatabricksWorkspace#vnet_address_prefix}.'''
        result = self._values.get("vnet_address_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabricksWorkspaceCustomParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabricksWorkspaceCustomParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databricksWorkspace.DatabricksWorkspaceCustomParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8d38516268804b807b3035a194d894a88c654adc0dd7d1195e8826170066b11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMachineLearningWorkspaceId")
    def reset_machine_learning_workspace_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineLearningWorkspaceId", []))

    @jsii.member(jsii_name="resetNatGatewayName")
    def reset_nat_gateway_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNatGatewayName", []))

    @jsii.member(jsii_name="resetNoPublicIp")
    def reset_no_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoPublicIp", []))

    @jsii.member(jsii_name="resetPrivateSubnetName")
    def reset_private_subnet_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateSubnetName", []))

    @jsii.member(jsii_name="resetPrivateSubnetNetworkSecurityGroupAssociationId")
    def reset_private_subnet_network_security_group_association_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateSubnetNetworkSecurityGroupAssociationId", []))

    @jsii.member(jsii_name="resetPublicIpName")
    def reset_public_ip_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpName", []))

    @jsii.member(jsii_name="resetPublicSubnetName")
    def reset_public_subnet_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicSubnetName", []))

    @jsii.member(jsii_name="resetPublicSubnetNetworkSecurityGroupAssociationId")
    def reset_public_subnet_network_security_group_association_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicSubnetNetworkSecurityGroupAssociationId", []))

    @jsii.member(jsii_name="resetStorageAccountName")
    def reset_storage_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountName", []))

    @jsii.member(jsii_name="resetStorageAccountSkuName")
    def reset_storage_account_sku_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountSkuName", []))

    @jsii.member(jsii_name="resetVirtualNetworkId")
    def reset_virtual_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkId", []))

    @jsii.member(jsii_name="resetVnetAddressPrefix")
    def reset_vnet_address_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVnetAddressPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="machineLearningWorkspaceIdInput")
    def machine_learning_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineLearningWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="natGatewayNameInput")
    def nat_gateway_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "natGatewayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="noPublicIpInput")
    def no_public_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noPublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="privateSubnetNameInput")
    def private_subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateSubnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="privateSubnetNetworkSecurityGroupAssociationIdInput")
    def private_subnet_network_security_group_association_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateSubnetNetworkSecurityGroupAssociationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpNameInput")
    def public_ip_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicIpNameInput"))

    @builtins.property
    @jsii.member(jsii_name="publicSubnetNameInput")
    def public_subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicSubnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="publicSubnetNetworkSecurityGroupAssociationIdInput")
    def public_subnet_network_security_group_association_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicSubnetNetworkSecurityGroupAssociationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountNameInput")
    def storage_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountSkuNameInput")
    def storage_account_sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountSkuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetAddressPrefixInput")
    def vnet_address_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vnetAddressPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="machineLearningWorkspaceId")
    def machine_learning_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineLearningWorkspaceId"))

    @machine_learning_workspace_id.setter
    def machine_learning_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ad15c24a4a06b58eb5e995ee164b9f4447c5eae6ab57a3a542e980f7cf3ec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineLearningWorkspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="natGatewayName")
    def nat_gateway_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "natGatewayName"))

    @nat_gateway_name.setter
    def nat_gateway_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f9de446ab8d3ab11685d181392044c840aa5a497f9a03f23014012a64d6c0d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natGatewayName", value)

    @builtins.property
    @jsii.member(jsii_name="noPublicIp")
    def no_public_ip(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noPublicIp"))

    @no_public_ip.setter
    def no_public_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214615e18029cbda32dd7162295775d1e731dcf151cd2ab56afe34c4ba2e2161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noPublicIp", value)

    @builtins.property
    @jsii.member(jsii_name="privateSubnetName")
    def private_subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateSubnetName"))

    @private_subnet_name.setter
    def private_subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4048e2c56a13ee8da36552c13a574d97ca0ca597d9d4bbc068818033c4997f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateSubnetName", value)

    @builtins.property
    @jsii.member(jsii_name="privateSubnetNetworkSecurityGroupAssociationId")
    def private_subnet_network_security_group_association_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateSubnetNetworkSecurityGroupAssociationId"))

    @private_subnet_network_security_group_association_id.setter
    def private_subnet_network_security_group_association_id(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14aa07e36b23e35384cddd9dc8c78c85d7784f000856b98f6c3c777745d2e84a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateSubnetNetworkSecurityGroupAssociationId", value)

    @builtins.property
    @jsii.member(jsii_name="publicIpName")
    def public_ip_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpName"))

    @public_ip_name.setter
    def public_ip_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c0a07e53b03430e75ed9d7503ce9fb1aa7330ae30ebf39646b673e98b551a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpName", value)

    @builtins.property
    @jsii.member(jsii_name="publicSubnetName")
    def public_subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicSubnetName"))

    @public_subnet_name.setter
    def public_subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb9069190039e6a1a0dad74e9568dcc044061203d44445f55b8a974a8eac56b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicSubnetName", value)

    @builtins.property
    @jsii.member(jsii_name="publicSubnetNetworkSecurityGroupAssociationId")
    def public_subnet_network_security_group_association_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicSubnetNetworkSecurityGroupAssociationId"))

    @public_subnet_network_security_group_association_id.setter
    def public_subnet_network_security_group_association_id(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369d84bb7614881320485b87ee3911b20cea03843171bcae2d1bbf3d9525b3a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicSubnetNetworkSecurityGroupAssociationId", value)

    @builtins.property
    @jsii.member(jsii_name="storageAccountName")
    def storage_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountName"))

    @storage_account_name.setter
    def storage_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9df4b4981692e15a98004c62358d6bd39d48e25cfaa2f25c34852e8ac14c05f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountName", value)

    @builtins.property
    @jsii.member(jsii_name="storageAccountSkuName")
    def storage_account_sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountSkuName"))

    @storage_account_sku_name.setter
    def storage_account_sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1244a199d622b14215336190e8a89fbf4ac7c7a96baebf1bc5e64dd23c7450d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountSkuName", value)

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274620af07be27f3efe6bcc42db6aa982c94fa09bbc3b3f1b23a450e73bca8b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="vnetAddressPrefix")
    def vnet_address_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vnetAddressPrefix"))

    @vnet_address_prefix.setter
    def vnet_address_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c161717d06611f461089d07595e311cb1207a19a42fa7845695dba0b8f5a3d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vnetAddressPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DatabricksWorkspaceCustomParameters]:
        return typing.cast(typing.Optional[DatabricksWorkspaceCustomParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabricksWorkspaceCustomParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb08ce85e7e5d9a613142a67e9613c5ba538dace58e0bd3c5e3ed2396ea6eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databricksWorkspace.DatabricksWorkspaceStorageAccountIdentity",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatabricksWorkspaceStorageAccountIdentity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabricksWorkspaceStorageAccountIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabricksWorkspaceStorageAccountIdentityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databricksWorkspace.DatabricksWorkspaceStorageAccountIdentityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79ea374a8e9bec90d2c3009d624d6366708ff3af749ec4518471177502b6deef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabricksWorkspaceStorageAccountIdentityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__559c081fb6606ec7ffa9313351220456c8599f3027036e32b9bcee325ceb73a4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabricksWorkspaceStorageAccountIdentityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a979b027b5ede91771e91c8d10ea0afc7efd0bc6c0c72b5d5d1f77d85b0bd69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__163a32b48d912734f3631972c6fdc2db7a9ed84499712a492162b0e061761ab5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d5ed588816ec1012ad8f902bfb23520bdb5e8de4f033418ec9128d7a725327e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DatabricksWorkspaceStorageAccountIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databricksWorkspace.DatabricksWorkspaceStorageAccountIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0619a8264132f5f954831b89288dbb32bff0963f3ecb4ee815b5e3273b956b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabricksWorkspaceStorageAccountIdentity]:
        return typing.cast(typing.Optional[DatabricksWorkspaceStorageAccountIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabricksWorkspaceStorageAccountIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e69de49e159743e11e8e6ff22aaf3adadc4f29e8e1c4a9f2ecbff4c4089829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.databricksWorkspace.DatabricksWorkspaceTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DatabricksWorkspaceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#create DatabricksWorkspace#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#delete DatabricksWorkspace#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#read DatabricksWorkspace#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#update DatabricksWorkspace#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e62346db128236348114cf5eca4670198bb72661a3e84b9300648364b315d1f5)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#create DatabricksWorkspace#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#delete DatabricksWorkspace#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#read DatabricksWorkspace#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/databricks_workspace#update DatabricksWorkspace#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabricksWorkspaceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabricksWorkspaceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.databricksWorkspace.DatabricksWorkspaceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d121b6717071bd8a064feaededc3893833832e7e98e347d9843f6ae6b777fceb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__637ae48478bc5abe82dbe6f27bfa025ce9f54aa50433c847ada57e9a043b6e97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad24a4734edd39df54a9bd47c45323cb0675865d6d31ff04afe68a32c3c1be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c7aeb260a699486eb92423cde3d8390aa107644e69fd11df84b83e2a00e6df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b77fdb320f75e6fe171c24afe92f2f078c63c339a75b9aad139db38ae9a671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DatabricksWorkspaceTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DatabricksWorkspaceTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DatabricksWorkspaceTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9f31ab3559d88090d6c8b03c1e1bc3ce769ee8f18e48e904c3b594e2cd16f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DatabricksWorkspace",
    "DatabricksWorkspaceConfig",
    "DatabricksWorkspaceCustomParameters",
    "DatabricksWorkspaceCustomParametersOutputReference",
    "DatabricksWorkspaceStorageAccountIdentity",
    "DatabricksWorkspaceStorageAccountIdentityList",
    "DatabricksWorkspaceStorageAccountIdentityOutputReference",
    "DatabricksWorkspaceTimeouts",
    "DatabricksWorkspaceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f1accdd55672c74ed4c70d65a9cd0ab85befb9969d93e94ec2d3ff885ba76e78(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku: builtins.str,
    customer_managed_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_parameters: typing.Optional[typing.Union[DatabricksWorkspaceCustomParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    load_balancer_backend_address_pool_id: typing.Optional[builtins.str] = None,
    managed_resource_group_name: typing.Optional[builtins.str] = None,
    managed_services_cmk_key_vault_key_id: typing.Optional[builtins.str] = None,
    network_security_group_rules_required: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DatabricksWorkspaceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6a200daa3aafb5b77f94e6293e70ab5c66415181b58e8a4b770f21bdb68c7db3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200198470356fbd098dd7f3d327c79899625f4779212b73d1233d29bc5b935ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5000e65582b4036adce35b6c7f50ae801f43ccc64a6797b640e332215372079c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8fb131fa353575ca9152a8dcaf53c547cb612f0b44ac01f43042ae15be85d7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9dfb92437233a578675967c90ce3217a30dc7ba115cc11d61dade9bb7d076f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0c4534998b6fa56910e5bf58d5872a0d0366759492057db4c93a5e645eb94a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6412a79a8a29de21db9b2f88f52328ead5f2e4d146b7d08ba26c1e9d6bf0df24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e09e9bdfb9330370247fc7a4b42e532d2599ded55a9be712a25dfbbd34f359c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a94649129d64db57f647c431f1ff795a6a1cb511e59527ff0ac10118753b6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b614c454302794eb967c218ccd3dda411b211e5cf44161d2758aadbb6560adf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c514befacf4f7b22ad9afb2b9f4b2791266dc039b035e01b61520873926218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2f707f8e9aa15da4b50a6cee946f0ea88283dd382954ae65b598f9ff3b2b85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc751b09cde6afa6a7056f936da9719d94c1bd39e005070a2772bedf7c819bae(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6b8d0cd8473f8f24da00c4dd5a77bc2079ccedca5ed46f8799a75e5f40320b(
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
    sku: builtins.str,
    customer_managed_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_parameters: typing.Optional[typing.Union[DatabricksWorkspaceCustomParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    load_balancer_backend_address_pool_id: typing.Optional[builtins.str] = None,
    managed_resource_group_name: typing.Optional[builtins.str] = None,
    managed_services_cmk_key_vault_key_id: typing.Optional[builtins.str] = None,
    network_security_group_rules_required: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DatabricksWorkspaceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1780f82849a31d7e8dc5c3fbdfe772e90e96289147d09fbfb2ea7ffc0503a6f(
    *,
    machine_learning_workspace_id: typing.Optional[builtins.str] = None,
    nat_gateway_name: typing.Optional[builtins.str] = None,
    no_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_subnet_name: typing.Optional[builtins.str] = None,
    private_subnet_network_security_group_association_id: typing.Optional[builtins.str] = None,
    public_ip_name: typing.Optional[builtins.str] = None,
    public_subnet_name: typing.Optional[builtins.str] = None,
    public_subnet_network_security_group_association_id: typing.Optional[builtins.str] = None,
    storage_account_name: typing.Optional[builtins.str] = None,
    storage_account_sku_name: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
    vnet_address_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d38516268804b807b3035a194d894a88c654adc0dd7d1195e8826170066b11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ad15c24a4a06b58eb5e995ee164b9f4447c5eae6ab57a3a542e980f7cf3ec3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9de446ab8d3ab11685d181392044c840aa5a497f9a03f23014012a64d6c0d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214615e18029cbda32dd7162295775d1e731dcf151cd2ab56afe34c4ba2e2161(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4048e2c56a13ee8da36552c13a574d97ca0ca597d9d4bbc068818033c4997f74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14aa07e36b23e35384cddd9dc8c78c85d7784f000856b98f6c3c777745d2e84a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c0a07e53b03430e75ed9d7503ce9fb1aa7330ae30ebf39646b673e98b551a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb9069190039e6a1a0dad74e9568dcc044061203d44445f55b8a974a8eac56b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369d84bb7614881320485b87ee3911b20cea03843171bcae2d1bbf3d9525b3a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9df4b4981692e15a98004c62358d6bd39d48e25cfaa2f25c34852e8ac14c05f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1244a199d622b14215336190e8a89fbf4ac7c7a96baebf1bc5e64dd23c7450d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274620af07be27f3efe6bcc42db6aa982c94fa09bbc3b3f1b23a450e73bca8b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c161717d06611f461089d07595e311cb1207a19a42fa7845695dba0b8f5a3d05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb08ce85e7e5d9a613142a67e9613c5ba538dace58e0bd3c5e3ed2396ea6eaf(
    value: typing.Optional[DatabricksWorkspaceCustomParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ea374a8e9bec90d2c3009d624d6366708ff3af749ec4518471177502b6deef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559c081fb6606ec7ffa9313351220456c8599f3027036e32b9bcee325ceb73a4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a979b027b5ede91771e91c8d10ea0afc7efd0bc6c0c72b5d5d1f77d85b0bd69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163a32b48d912734f3631972c6fdc2db7a9ed84499712a492162b0e061761ab5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5ed588816ec1012ad8f902bfb23520bdb5e8de4f033418ec9128d7a725327e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0619a8264132f5f954831b89288dbb32bff0963f3ecb4ee815b5e3273b956b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e69de49e159743e11e8e6ff22aaf3adadc4f29e8e1c4a9f2ecbff4c4089829(
    value: typing.Optional[DatabricksWorkspaceStorageAccountIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62346db128236348114cf5eca4670198bb72661a3e84b9300648364b315d1f5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d121b6717071bd8a064feaededc3893833832e7e98e347d9843f6ae6b777fceb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637ae48478bc5abe82dbe6f27bfa025ce9f54aa50433c847ada57e9a043b6e97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad24a4734edd39df54a9bd47c45323cb0675865d6d31ff04afe68a32c3c1be0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c7aeb260a699486eb92423cde3d8390aa107644e69fd11df84b83e2a00e6df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b77fdb320f75e6fe171c24afe92f2f078c63c339a75b9aad139db38ae9a671(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9f31ab3559d88090d6c8b03c1e1bc3ce769ee8f18e48e904c3b594e2cd16f0(
    value: typing.Optional[typing.Union[DatabricksWorkspaceTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
