'''
# `azurerm_kubernetes_cluster`

Refer to the Terraform Registory for docs: [`azurerm_kubernetes_cluster`](https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster).
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


class KubernetesCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesCluster",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster azurerm_kubernetes_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_node_pool: typing.Union["KubernetesClusterDefaultNodePool", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        aci_connector_linux: typing.Optional[typing.Union["KubernetesClusterAciConnectorLinux", typing.Dict[builtins.str, typing.Any]]] = None,
        api_server_authorized_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        automatic_channel_upgrade: typing.Optional[builtins.str] = None,
        auto_scaler_profile: typing.Optional[typing.Union["KubernetesClusterAutoScalerProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_active_directory_role_based_access_control: typing.Optional[typing.Union["KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_policy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_encryption_set_id: typing.Optional[builtins.str] = None,
        dns_prefix: typing.Optional[builtins.str] = None,
        dns_prefix_private_cluster: typing.Optional[builtins.str] = None,
        edge_zone: typing.Optional[builtins.str] = None,
        enable_pod_security_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_application_routing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_proxy_config: typing.Optional[typing.Union["KubernetesClusterHttpProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["KubernetesClusterIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        image_cleaner_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image_cleaner_interval_hours: typing.Optional[jsii.Number] = None,
        ingress_application_gateway: typing.Optional[typing.Union["KubernetesClusterIngressApplicationGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_secrets_provider: typing.Optional[typing.Union["KubernetesClusterKeyVaultSecretsProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        kubelet_identity: typing.Optional[typing.Union["KubernetesClusterKubeletIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes_version: typing.Optional[builtins.str] = None,
        linux_profile: typing.Optional[typing.Union["KubernetesClusterLinuxProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        local_account_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maintenance_window: typing.Optional[typing.Union["KubernetesClusterMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        microsoft_defender: typing.Optional[typing.Union["KubernetesClusterMicrosoftDefender", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_metrics: typing.Optional[typing.Union["KubernetesClusterMonitorMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        network_profile: typing.Optional[typing.Union["KubernetesClusterNetworkProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        node_resource_group: typing.Optional[builtins.str] = None,
        oidc_issuer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        oms_agent: typing.Optional[typing.Union["KubernetesClusterOmsAgent", typing.Dict[builtins.str, typing.Any]]] = None,
        open_service_mesh_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_cluster_public_fqdn_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_dns_zone_id: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        role_based_access_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_command_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_principal: typing.Optional[typing.Union["KubernetesClusterServicePrincipal", typing.Dict[builtins.str, typing.Any]]] = None,
        sku_tier: typing.Optional[builtins.str] = None,
        storage_profile: typing.Optional[typing.Union["KubernetesClusterStorageProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KubernetesClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        web_app_routing: typing.Optional[typing.Union["KubernetesClusterWebAppRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_profile: typing.Optional[typing.Union["KubernetesClusterWindowsProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_autoscaler_profile: typing.Optional[typing.Union["KubernetesClusterWorkloadAutoscalerProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_identity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster azurerm_kubernetes_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_node_pool: default_node_pool block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#default_node_pool KubernetesCluster#default_node_pool}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#location KubernetesCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#name KubernetesCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#resource_group_name KubernetesCluster#resource_group_name}.
        :param aci_connector_linux: aci_connector_linux block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#aci_connector_linux KubernetesCluster#aci_connector_linux}
        :param api_server_authorized_ip_ranges: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#api_server_authorized_ip_ranges KubernetesCluster#api_server_authorized_ip_ranges}.
        :param automatic_channel_upgrade: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#automatic_channel_upgrade KubernetesCluster#automatic_channel_upgrade}.
        :param auto_scaler_profile: auto_scaler_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#auto_scaler_profile KubernetesCluster#auto_scaler_profile}
        :param azure_active_directory_role_based_access_control: azure_active_directory_role_based_access_control block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#azure_active_directory_role_based_access_control KubernetesCluster#azure_active_directory_role_based_access_control}
        :param azure_policy_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#azure_policy_enabled KubernetesCluster#azure_policy_enabled}.
        :param disk_encryption_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#disk_encryption_set_id KubernetesCluster#disk_encryption_set_id}.
        :param dns_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_prefix KubernetesCluster#dns_prefix}.
        :param dns_prefix_private_cluster: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_prefix_private_cluster KubernetesCluster#dns_prefix_private_cluster}.
        :param edge_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#edge_zone KubernetesCluster#edge_zone}.
        :param enable_pod_security_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_pod_security_policy KubernetesCluster#enable_pod_security_policy}.
        :param http_application_routing_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#http_application_routing_enabled KubernetesCluster#http_application_routing_enabled}.
        :param http_proxy_config: http_proxy_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#http_proxy_config KubernetesCluster#http_proxy_config}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#id KubernetesCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#identity KubernetesCluster#identity}
        :param image_cleaner_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_cleaner_enabled KubernetesCluster#image_cleaner_enabled}.
        :param image_cleaner_interval_hours: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_cleaner_interval_hours KubernetesCluster#image_cleaner_interval_hours}.
        :param ingress_application_gateway: ingress_application_gateway block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ingress_application_gateway KubernetesCluster#ingress_application_gateway}
        :param key_vault_secrets_provider: key_vault_secrets_provider block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#key_vault_secrets_provider KubernetesCluster#key_vault_secrets_provider}
        :param kubelet_identity: kubelet_identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubelet_identity KubernetesCluster#kubelet_identity}
        :param kubernetes_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubernetes_version KubernetesCluster#kubernetes_version}.
        :param linux_profile: linux_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#linux_profile KubernetesCluster#linux_profile}
        :param local_account_disabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#local_account_disabled KubernetesCluster#local_account_disabled}.
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#maintenance_window KubernetesCluster#maintenance_window}
        :param microsoft_defender: microsoft_defender block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#microsoft_defender KubernetesCluster#microsoft_defender}
        :param monitor_metrics: monitor_metrics block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#monitor_metrics KubernetesCluster#monitor_metrics}
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_profile KubernetesCluster#network_profile}
        :param node_resource_group: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_resource_group KubernetesCluster#node_resource_group}.
        :param oidc_issuer_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#oidc_issuer_enabled KubernetesCluster#oidc_issuer_enabled}.
        :param oms_agent: oms_agent block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#oms_agent KubernetesCluster#oms_agent}
        :param open_service_mesh_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#open_service_mesh_enabled KubernetesCluster#open_service_mesh_enabled}.
        :param private_cluster_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#private_cluster_enabled KubernetesCluster#private_cluster_enabled}.
        :param private_cluster_public_fqdn_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#private_cluster_public_fqdn_enabled KubernetesCluster#private_cluster_public_fqdn_enabled}.
        :param private_dns_zone_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#private_dns_zone_id KubernetesCluster#private_dns_zone_id}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#public_network_access_enabled KubernetesCluster#public_network_access_enabled}.
        :param role_based_access_control_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#role_based_access_control_enabled KubernetesCluster#role_based_access_control_enabled}.
        :param run_command_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#run_command_enabled KubernetesCluster#run_command_enabled}.
        :param service_principal: service_principal block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#service_principal KubernetesCluster#service_principal}
        :param sku_tier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#sku_tier KubernetesCluster#sku_tier}.
        :param storage_profile: storage_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#storage_profile KubernetesCluster#storage_profile}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#tags KubernetesCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#timeouts KubernetesCluster#timeouts}
        :param web_app_routing: web_app_routing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#web_app_routing KubernetesCluster#web_app_routing}
        :param windows_profile: windows_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#windows_profile KubernetesCluster#windows_profile}
        :param workload_autoscaler_profile: workload_autoscaler_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#workload_autoscaler_profile KubernetesCluster#workload_autoscaler_profile}
        :param workload_identity_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#workload_identity_enabled KubernetesCluster#workload_identity_enabled}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ce399717b7c228e398ae9350214c956093962687d3c01a8de989177b29e827)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KubernetesClusterConfig(
            default_node_pool=default_node_pool,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            aci_connector_linux=aci_connector_linux,
            api_server_authorized_ip_ranges=api_server_authorized_ip_ranges,
            automatic_channel_upgrade=automatic_channel_upgrade,
            auto_scaler_profile=auto_scaler_profile,
            azure_active_directory_role_based_access_control=azure_active_directory_role_based_access_control,
            azure_policy_enabled=azure_policy_enabled,
            disk_encryption_set_id=disk_encryption_set_id,
            dns_prefix=dns_prefix,
            dns_prefix_private_cluster=dns_prefix_private_cluster,
            edge_zone=edge_zone,
            enable_pod_security_policy=enable_pod_security_policy,
            http_application_routing_enabled=http_application_routing_enabled,
            http_proxy_config=http_proxy_config,
            id=id,
            identity=identity,
            image_cleaner_enabled=image_cleaner_enabled,
            image_cleaner_interval_hours=image_cleaner_interval_hours,
            ingress_application_gateway=ingress_application_gateway,
            key_vault_secrets_provider=key_vault_secrets_provider,
            kubelet_identity=kubelet_identity,
            kubernetes_version=kubernetes_version,
            linux_profile=linux_profile,
            local_account_disabled=local_account_disabled,
            maintenance_window=maintenance_window,
            microsoft_defender=microsoft_defender,
            monitor_metrics=monitor_metrics,
            network_profile=network_profile,
            node_resource_group=node_resource_group,
            oidc_issuer_enabled=oidc_issuer_enabled,
            oms_agent=oms_agent,
            open_service_mesh_enabled=open_service_mesh_enabled,
            private_cluster_enabled=private_cluster_enabled,
            private_cluster_public_fqdn_enabled=private_cluster_public_fqdn_enabled,
            private_dns_zone_id=private_dns_zone_id,
            public_network_access_enabled=public_network_access_enabled,
            role_based_access_control_enabled=role_based_access_control_enabled,
            run_command_enabled=run_command_enabled,
            service_principal=service_principal,
            sku_tier=sku_tier,
            storage_profile=storage_profile,
            tags=tags,
            timeouts=timeouts,
            web_app_routing=web_app_routing,
            windows_profile=windows_profile,
            workload_autoscaler_profile=workload_autoscaler_profile,
            workload_identity_enabled=workload_identity_enabled,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAciConnectorLinux")
    def put_aci_connector_linux(self, *, subnet_name: builtins.str) -> None:
        '''
        :param subnet_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#subnet_name KubernetesCluster#subnet_name}.
        '''
        value = KubernetesClusterAciConnectorLinux(subnet_name=subnet_name)

        return typing.cast(None, jsii.invoke(self, "putAciConnectorLinux", [value]))

    @jsii.member(jsii_name="putAutoScalerProfile")
    def put_auto_scaler_profile(
        self,
        *,
        balance_similar_node_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        empty_bulk_delete_max: typing.Optional[builtins.str] = None,
        expander: typing.Optional[builtins.str] = None,
        max_graceful_termination_sec: typing.Optional[builtins.str] = None,
        max_node_provisioning_time: typing.Optional[builtins.str] = None,
        max_unready_nodes: typing.Optional[jsii.Number] = None,
        max_unready_percentage: typing.Optional[jsii.Number] = None,
        new_pod_scale_up_delay: typing.Optional[builtins.str] = None,
        scale_down_delay_after_add: typing.Optional[builtins.str] = None,
        scale_down_delay_after_delete: typing.Optional[builtins.str] = None,
        scale_down_delay_after_failure: typing.Optional[builtins.str] = None,
        scale_down_unneeded: typing.Optional[builtins.str] = None,
        scale_down_unready: typing.Optional[builtins.str] = None,
        scale_down_utilization_threshold: typing.Optional[builtins.str] = None,
        scan_interval: typing.Optional[builtins.str] = None,
        skip_nodes_with_local_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_nodes_with_system_pods: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param balance_similar_node_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#balance_similar_node_groups KubernetesCluster#balance_similar_node_groups}.
        :param empty_bulk_delete_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#empty_bulk_delete_max KubernetesCluster#empty_bulk_delete_max}.
        :param expander: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#expander KubernetesCluster#expander}.
        :param max_graceful_termination_sec: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_graceful_termination_sec KubernetesCluster#max_graceful_termination_sec}.
        :param max_node_provisioning_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_node_provisioning_time KubernetesCluster#max_node_provisioning_time}.
        :param max_unready_nodes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_unready_nodes KubernetesCluster#max_unready_nodes}.
        :param max_unready_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_unready_percentage KubernetesCluster#max_unready_percentage}.
        :param new_pod_scale_up_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#new_pod_scale_up_delay KubernetesCluster#new_pod_scale_up_delay}.
        :param scale_down_delay_after_add: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_delay_after_add KubernetesCluster#scale_down_delay_after_add}.
        :param scale_down_delay_after_delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_delay_after_delete KubernetesCluster#scale_down_delay_after_delete}.
        :param scale_down_delay_after_failure: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_delay_after_failure KubernetesCluster#scale_down_delay_after_failure}.
        :param scale_down_unneeded: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_unneeded KubernetesCluster#scale_down_unneeded}.
        :param scale_down_unready: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_unready KubernetesCluster#scale_down_unready}.
        :param scale_down_utilization_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_utilization_threshold KubernetesCluster#scale_down_utilization_threshold}.
        :param scan_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scan_interval KubernetesCluster#scan_interval}.
        :param skip_nodes_with_local_storage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#skip_nodes_with_local_storage KubernetesCluster#skip_nodes_with_local_storage}.
        :param skip_nodes_with_system_pods: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#skip_nodes_with_system_pods KubernetesCluster#skip_nodes_with_system_pods}.
        '''
        value = KubernetesClusterAutoScalerProfile(
            balance_similar_node_groups=balance_similar_node_groups,
            empty_bulk_delete_max=empty_bulk_delete_max,
            expander=expander,
            max_graceful_termination_sec=max_graceful_termination_sec,
            max_node_provisioning_time=max_node_provisioning_time,
            max_unready_nodes=max_unready_nodes,
            max_unready_percentage=max_unready_percentage,
            new_pod_scale_up_delay=new_pod_scale_up_delay,
            scale_down_delay_after_add=scale_down_delay_after_add,
            scale_down_delay_after_delete=scale_down_delay_after_delete,
            scale_down_delay_after_failure=scale_down_delay_after_failure,
            scale_down_unneeded=scale_down_unneeded,
            scale_down_unready=scale_down_unready,
            scale_down_utilization_threshold=scale_down_utilization_threshold,
            scan_interval=scan_interval,
            skip_nodes_with_local_storage=skip_nodes_with_local_storage,
            skip_nodes_with_system_pods=skip_nodes_with_system_pods,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoScalerProfile", [value]))

    @jsii.member(jsii_name="putAzureActiveDirectoryRoleBasedAccessControl")
    def put_azure_active_directory_role_based_access_control(
        self,
        *,
        admin_group_object_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        azure_rbac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_app_id: typing.Optional[builtins.str] = None,
        managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_app_id: typing.Optional[builtins.str] = None,
        server_app_secret: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_group_object_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_group_object_ids KubernetesCluster#admin_group_object_ids}.
        :param azure_rbac_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#azure_rbac_enabled KubernetesCluster#azure_rbac_enabled}.
        :param client_app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_app_id KubernetesCluster#client_app_id}.
        :param managed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed KubernetesCluster#managed}.
        :param server_app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#server_app_id KubernetesCluster#server_app_id}.
        :param server_app_secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#server_app_secret KubernetesCluster#server_app_secret}.
        :param tenant_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#tenant_id KubernetesCluster#tenant_id}.
        '''
        value = KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl(
            admin_group_object_ids=admin_group_object_ids,
            azure_rbac_enabled=azure_rbac_enabled,
            client_app_id=client_app_id,
            managed=managed,
            server_app_id=server_app_id,
            server_app_secret=server_app_secret,
            tenant_id=tenant_id,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureActiveDirectoryRoleBasedAccessControl", [value]))

    @jsii.member(jsii_name="putDefaultNodePool")
    def put_default_node_pool(
        self,
        *,
        name: builtins.str,
        vm_size: builtins.str,
        capacity_reservation_group_id: typing.Optional[builtins.str] = None,
        custom_ca_trust_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_auto_scaling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_host_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_node_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_group_id: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["KubernetesClusterDefaultNodePoolKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        kubelet_disk_type: typing.Optional[builtins.str] = None,
        linux_os_config: typing.Optional[typing.Union["KubernetesClusterDefaultNodePoolLinuxOsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_count: typing.Optional[jsii.Number] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        message_of_the_day: typing.Optional[builtins.str] = None,
        min_count: typing.Optional[jsii.Number] = None,
        node_count: typing.Optional[jsii.Number] = None,
        node_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_public_ip_prefix_id: typing.Optional[builtins.str] = None,
        node_taints: typing.Optional[typing.Sequence[builtins.str]] = None,
        only_critical_addons_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        orchestrator_version: typing.Optional[builtins.str] = None,
        os_disk_size_gb: typing.Optional[jsii.Number] = None,
        os_disk_type: typing.Optional[builtins.str] = None,
        os_sku: typing.Optional[builtins.str] = None,
        pod_subnet_id: typing.Optional[builtins.str] = None,
        proximity_placement_group_id: typing.Optional[builtins.str] = None,
        scale_down_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
        ultra_ssd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        upgrade_settings: typing.Optional[typing.Union["KubernetesClusterDefaultNodePoolUpgradeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        vnet_subnet_id: typing.Optional[builtins.str] = None,
        workload_runtime: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#name KubernetesCluster#name}.
        :param vm_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_size KubernetesCluster#vm_size}.
        :param capacity_reservation_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#capacity_reservation_group_id KubernetesCluster#capacity_reservation_group_id}.
        :param custom_ca_trust_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#custom_ca_trust_enabled KubernetesCluster#custom_ca_trust_enabled}.
        :param enable_auto_scaling: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_auto_scaling KubernetesCluster#enable_auto_scaling}.
        :param enable_host_encryption: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_host_encryption KubernetesCluster#enable_host_encryption}.
        :param enable_node_public_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_node_public_ip KubernetesCluster#enable_node_public_ip}.
        :param fips_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fips_enabled KubernetesCluster#fips_enabled}.
        :param host_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#host_group_id KubernetesCluster#host_group_id}.
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubelet_config KubernetesCluster#kubelet_config}
        :param kubelet_disk_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubelet_disk_type KubernetesCluster#kubelet_disk_type}.
        :param linux_os_config: linux_os_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#linux_os_config KubernetesCluster#linux_os_config}
        :param max_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_count KubernetesCluster#max_count}.
        :param max_pods: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_pods KubernetesCluster#max_pods}.
        :param message_of_the_day: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#message_of_the_day KubernetesCluster#message_of_the_day}.
        :param min_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#min_count KubernetesCluster#min_count}.
        :param node_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_count KubernetesCluster#node_count}.
        :param node_labels: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_labels KubernetesCluster#node_labels}.
        :param node_public_ip_prefix_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_public_ip_prefix_id KubernetesCluster#node_public_ip_prefix_id}.
        :param node_taints: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_taints KubernetesCluster#node_taints}.
        :param only_critical_addons_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#only_critical_addons_enabled KubernetesCluster#only_critical_addons_enabled}.
        :param orchestrator_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#orchestrator_version KubernetesCluster#orchestrator_version}.
        :param os_disk_size_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#os_disk_size_gb KubernetesCluster#os_disk_size_gb}.
        :param os_disk_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#os_disk_type KubernetesCluster#os_disk_type}.
        :param os_sku: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#os_sku KubernetesCluster#os_sku}.
        :param pod_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_subnet_id KubernetesCluster#pod_subnet_id}.
        :param proximity_placement_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#proximity_placement_group_id KubernetesCluster#proximity_placement_group_id}.
        :param scale_down_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_mode KubernetesCluster#scale_down_mode}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#tags KubernetesCluster#tags}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#type KubernetesCluster#type}.
        :param ultra_ssd_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ultra_ssd_enabled KubernetesCluster#ultra_ssd_enabled}.
        :param upgrade_settings: upgrade_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#upgrade_settings KubernetesCluster#upgrade_settings}
        :param vnet_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vnet_subnet_id KubernetesCluster#vnet_subnet_id}.
        :param workload_runtime: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#workload_runtime KubernetesCluster#workload_runtime}.
        :param zones: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#zones KubernetesCluster#zones}.
        '''
        value = KubernetesClusterDefaultNodePool(
            name=name,
            vm_size=vm_size,
            capacity_reservation_group_id=capacity_reservation_group_id,
            custom_ca_trust_enabled=custom_ca_trust_enabled,
            enable_auto_scaling=enable_auto_scaling,
            enable_host_encryption=enable_host_encryption,
            enable_node_public_ip=enable_node_public_ip,
            fips_enabled=fips_enabled,
            host_group_id=host_group_id,
            kubelet_config=kubelet_config,
            kubelet_disk_type=kubelet_disk_type,
            linux_os_config=linux_os_config,
            max_count=max_count,
            max_pods=max_pods,
            message_of_the_day=message_of_the_day,
            min_count=min_count,
            node_count=node_count,
            node_labels=node_labels,
            node_public_ip_prefix_id=node_public_ip_prefix_id,
            node_taints=node_taints,
            only_critical_addons_enabled=only_critical_addons_enabled,
            orchestrator_version=orchestrator_version,
            os_disk_size_gb=os_disk_size_gb,
            os_disk_type=os_disk_type,
            os_sku=os_sku,
            pod_subnet_id=pod_subnet_id,
            proximity_placement_group_id=proximity_placement_group_id,
            scale_down_mode=scale_down_mode,
            tags=tags,
            type=type,
            ultra_ssd_enabled=ultra_ssd_enabled,
            upgrade_settings=upgrade_settings,
            vnet_subnet_id=vnet_subnet_id,
            workload_runtime=workload_runtime,
            zones=zones,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultNodePool", [value]))

    @jsii.member(jsii_name="putHttpProxyConfig")
    def put_http_proxy_config(
        self,
        *,
        http_proxy: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_ca: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param http_proxy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#http_proxy KubernetesCluster#http_proxy}.
        :param https_proxy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#https_proxy KubernetesCluster#https_proxy}.
        :param no_proxy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#no_proxy KubernetesCluster#no_proxy}.
        :param trusted_ca: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#trusted_ca KubernetesCluster#trusted_ca}.
        '''
        value = KubernetesClusterHttpProxyConfig(
            http_proxy=http_proxy,
            https_proxy=https_proxy,
            no_proxy=no_proxy,
            trusted_ca=trusted_ca,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpProxyConfig", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#type KubernetesCluster#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#identity_ids KubernetesCluster#identity_ids}.
        '''
        value = KubernetesClusterIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putIngressApplicationGateway")
    def put_ingress_application_gateway(
        self,
        *,
        gateway_id: typing.Optional[builtins.str] = None,
        gateway_name: typing.Optional[builtins.str] = None,
        subnet_cidr: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gateway_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#gateway_id KubernetesCluster#gateway_id}.
        :param gateway_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#gateway_name KubernetesCluster#gateway_name}.
        :param subnet_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#subnet_cidr KubernetesCluster#subnet_cidr}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#subnet_id KubernetesCluster#subnet_id}.
        '''
        value = KubernetesClusterIngressApplicationGateway(
            gateway_id=gateway_id,
            gateway_name=gateway_name,
            subnet_cidr=subnet_cidr,
            subnet_id=subnet_id,
        )

        return typing.cast(None, jsii.invoke(self, "putIngressApplicationGateway", [value]))

    @jsii.member(jsii_name="putKeyVaultSecretsProvider")
    def put_key_vault_secrets_provider(
        self,
        *,
        secret_rotation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_rotation_interval: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_rotation_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#secret_rotation_enabled KubernetesCluster#secret_rotation_enabled}.
        :param secret_rotation_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#secret_rotation_interval KubernetesCluster#secret_rotation_interval}.
        '''
        value = KubernetesClusterKeyVaultSecretsProvider(
            secret_rotation_enabled=secret_rotation_enabled,
            secret_rotation_interval=secret_rotation_interval,
        )

        return typing.cast(None, jsii.invoke(self, "putKeyVaultSecretsProvider", [value]))

    @jsii.member(jsii_name="putKubeletIdentity")
    def put_kubelet_identity(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        object_id: typing.Optional[builtins.str] = None,
        user_assigned_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_id KubernetesCluster#client_id}.
        :param object_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#object_id KubernetesCluster#object_id}.
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#user_assigned_identity_id KubernetesCluster#user_assigned_identity_id}.
        '''
        value = KubernetesClusterKubeletIdentity(
            client_id=client_id,
            object_id=object_id,
            user_assigned_identity_id=user_assigned_identity_id,
        )

        return typing.cast(None, jsii.invoke(self, "putKubeletIdentity", [value]))

    @jsii.member(jsii_name="putLinuxProfile")
    def put_linux_profile(
        self,
        *,
        admin_username: builtins.str,
        ssh_key: typing.Union["KubernetesClusterLinuxProfileSshKey", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_username KubernetesCluster#admin_username}.
        :param ssh_key: ssh_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ssh_key KubernetesCluster#ssh_key}
        '''
        value = KubernetesClusterLinuxProfile(
            admin_username=admin_username, ssh_key=ssh_key
        )

        return typing.cast(None, jsii.invoke(self, "putLinuxProfile", [value]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(
        self,
        *,
        allowed: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesClusterMaintenanceWindowAllowed", typing.Dict[builtins.str, typing.Any]]]]] = None,
        not_allowed: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesClusterMaintenanceWindowNotAllowed", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed: allowed block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#allowed KubernetesCluster#allowed}
        :param not_allowed: not_allowed block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#not_allowed KubernetesCluster#not_allowed}
        '''
        value = KubernetesClusterMaintenanceWindow(
            allowed=allowed, not_allowed=not_allowed
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="putMicrosoftDefender")
    def put_microsoft_defender(
        self,
        *,
        log_analytics_workspace_id: builtins.str,
    ) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#log_analytics_workspace_id KubernetesCluster#log_analytics_workspace_id}.
        '''
        value = KubernetesClusterMicrosoftDefender(
            log_analytics_workspace_id=log_analytics_workspace_id
        )

        return typing.cast(None, jsii.invoke(self, "putMicrosoftDefender", [value]))

    @jsii.member(jsii_name="putMonitorMetrics")
    def put_monitor_metrics(
        self,
        *,
        annotations_allowed: typing.Optional[builtins.str] = None,
        labels_allowed: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations_allowed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#annotations_allowed KubernetesCluster#annotations_allowed}.
        :param labels_allowed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#labels_allowed KubernetesCluster#labels_allowed}.
        '''
        value = KubernetesClusterMonitorMetrics(
            annotations_allowed=annotations_allowed, labels_allowed=labels_allowed
        )

        return typing.cast(None, jsii.invoke(self, "putMonitorMetrics", [value]))

    @jsii.member(jsii_name="putNetworkProfile")
    def put_network_profile(
        self,
        *,
        network_plugin: builtins.str,
        dns_service_ip: typing.Optional[builtins.str] = None,
        docker_bridge_cidr: typing.Optional[builtins.str] = None,
        ebpf_data_plane: typing.Optional[builtins.str] = None,
        ip_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        load_balancer_profile: typing.Optional[typing.Union["KubernetesClusterNetworkProfileLoadBalancerProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancer_sku: typing.Optional[builtins.str] = None,
        nat_gateway_profile: typing.Optional[typing.Union["KubernetesClusterNetworkProfileNatGatewayProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        network_mode: typing.Optional[builtins.str] = None,
        network_plugin_mode: typing.Optional[builtins.str] = None,
        network_policy: typing.Optional[builtins.str] = None,
        outbound_type: typing.Optional[builtins.str] = None,
        pod_cidr: typing.Optional[builtins.str] = None,
        pod_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_cidr: typing.Optional[builtins.str] = None,
        service_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network_plugin: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_plugin KubernetesCluster#network_plugin}.
        :param dns_service_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_service_ip KubernetesCluster#dns_service_ip}.
        :param docker_bridge_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#docker_bridge_cidr KubernetesCluster#docker_bridge_cidr}.
        :param ebpf_data_plane: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ebpf_data_plane KubernetesCluster#ebpf_data_plane}.
        :param ip_versions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ip_versions KubernetesCluster#ip_versions}.
        :param load_balancer_profile: load_balancer_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#load_balancer_profile KubernetesCluster#load_balancer_profile}
        :param load_balancer_sku: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#load_balancer_sku KubernetesCluster#load_balancer_sku}.
        :param nat_gateway_profile: nat_gateway_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#nat_gateway_profile KubernetesCluster#nat_gateway_profile}
        :param network_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_mode KubernetesCluster#network_mode}.
        :param network_plugin_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_plugin_mode KubernetesCluster#network_plugin_mode}.
        :param network_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_policy KubernetesCluster#network_policy}.
        :param outbound_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_type KubernetesCluster#outbound_type}.
        :param pod_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_cidr KubernetesCluster#pod_cidr}.
        :param pod_cidrs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_cidrs KubernetesCluster#pod_cidrs}.
        :param service_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#service_cidr KubernetesCluster#service_cidr}.
        :param service_cidrs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#service_cidrs KubernetesCluster#service_cidrs}.
        '''
        value = KubernetesClusterNetworkProfile(
            network_plugin=network_plugin,
            dns_service_ip=dns_service_ip,
            docker_bridge_cidr=docker_bridge_cidr,
            ebpf_data_plane=ebpf_data_plane,
            ip_versions=ip_versions,
            load_balancer_profile=load_balancer_profile,
            load_balancer_sku=load_balancer_sku,
            nat_gateway_profile=nat_gateway_profile,
            network_mode=network_mode,
            network_plugin_mode=network_plugin_mode,
            network_policy=network_policy,
            outbound_type=outbound_type,
            pod_cidr=pod_cidr,
            pod_cidrs=pod_cidrs,
            service_cidr=service_cidr,
            service_cidrs=service_cidrs,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkProfile", [value]))

    @jsii.member(jsii_name="putOmsAgent")
    def put_oms_agent(self, *, log_analytics_workspace_id: builtins.str) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#log_analytics_workspace_id KubernetesCluster#log_analytics_workspace_id}.
        '''
        value = KubernetesClusterOmsAgent(
            log_analytics_workspace_id=log_analytics_workspace_id
        )

        return typing.cast(None, jsii.invoke(self, "putOmsAgent", [value]))

    @jsii.member(jsii_name="putServicePrincipal")
    def put_service_principal(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_id KubernetesCluster#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_secret KubernetesCluster#client_secret}.
        '''
        value = KubernetesClusterServicePrincipal(
            client_id=client_id, client_secret=client_secret
        )

        return typing.cast(None, jsii.invoke(self, "putServicePrincipal", [value]))

    @jsii.member(jsii_name="putStorageProfile")
    def put_storage_profile(
        self,
        *,
        blob_driver_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_driver_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_driver_version: typing.Optional[builtins.str] = None,
        file_driver_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snapshot_controller_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param blob_driver_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#blob_driver_enabled KubernetesCluster#blob_driver_enabled}.
        :param disk_driver_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#disk_driver_enabled KubernetesCluster#disk_driver_enabled}.
        :param disk_driver_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#disk_driver_version KubernetesCluster#disk_driver_version}.
        :param file_driver_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#file_driver_enabled KubernetesCluster#file_driver_enabled}.
        :param snapshot_controller_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#snapshot_controller_enabled KubernetesCluster#snapshot_controller_enabled}.
        '''
        value = KubernetesClusterStorageProfile(
            blob_driver_enabled=blob_driver_enabled,
            disk_driver_enabled=disk_driver_enabled,
            disk_driver_version=disk_driver_version,
            file_driver_enabled=file_driver_enabled,
            snapshot_controller_enabled=snapshot_controller_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putStorageProfile", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#create KubernetesCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#delete KubernetesCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#read KubernetesCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#update KubernetesCluster#update}.
        '''
        value = KubernetesClusterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWebAppRouting")
    def put_web_app_routing(self, *, dns_zone_id: builtins.str) -> None:
        '''
        :param dns_zone_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_zone_id KubernetesCluster#dns_zone_id}.
        '''
        value = KubernetesClusterWebAppRouting(dns_zone_id=dns_zone_id)

        return typing.cast(None, jsii.invoke(self, "putWebAppRouting", [value]))

    @jsii.member(jsii_name="putWindowsProfile")
    def put_windows_profile(
        self,
        *,
        admin_username: builtins.str,
        admin_password: typing.Optional[builtins.str] = None,
        gmsa: typing.Optional[typing.Union["KubernetesClusterWindowsProfileGmsa", typing.Dict[builtins.str, typing.Any]]] = None,
        license: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_username KubernetesCluster#admin_username}.
        :param admin_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_password KubernetesCluster#admin_password}.
        :param gmsa: gmsa block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#gmsa KubernetesCluster#gmsa}
        :param license: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#license KubernetesCluster#license}.
        '''
        value = KubernetesClusterWindowsProfile(
            admin_username=admin_username,
            admin_password=admin_password,
            gmsa=gmsa,
            license=license,
        )

        return typing.cast(None, jsii.invoke(self, "putWindowsProfile", [value]))

    @jsii.member(jsii_name="putWorkloadAutoscalerProfile")
    def put_workload_autoscaler_profile(
        self,
        *,
        keda_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param keda_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#keda_enabled KubernetesCluster#keda_enabled}.
        '''
        value = KubernetesClusterWorkloadAutoscalerProfile(keda_enabled=keda_enabled)

        return typing.cast(None, jsii.invoke(self, "putWorkloadAutoscalerProfile", [value]))

    @jsii.member(jsii_name="resetAciConnectorLinux")
    def reset_aci_connector_linux(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAciConnectorLinux", []))

    @jsii.member(jsii_name="resetApiServerAuthorizedIpRanges")
    def reset_api_server_authorized_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiServerAuthorizedIpRanges", []))

    @jsii.member(jsii_name="resetAutomaticChannelUpgrade")
    def reset_automatic_channel_upgrade(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticChannelUpgrade", []))

    @jsii.member(jsii_name="resetAutoScalerProfile")
    def reset_auto_scaler_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoScalerProfile", []))

    @jsii.member(jsii_name="resetAzureActiveDirectoryRoleBasedAccessControl")
    def reset_azure_active_directory_role_based_access_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureActiveDirectoryRoleBasedAccessControl", []))

    @jsii.member(jsii_name="resetAzurePolicyEnabled")
    def reset_azure_policy_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzurePolicyEnabled", []))

    @jsii.member(jsii_name="resetDiskEncryptionSetId")
    def reset_disk_encryption_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionSetId", []))

    @jsii.member(jsii_name="resetDnsPrefix")
    def reset_dns_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsPrefix", []))

    @jsii.member(jsii_name="resetDnsPrefixPrivateCluster")
    def reset_dns_prefix_private_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsPrefixPrivateCluster", []))

    @jsii.member(jsii_name="resetEdgeZone")
    def reset_edge_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeZone", []))

    @jsii.member(jsii_name="resetEnablePodSecurityPolicy")
    def reset_enable_pod_security_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePodSecurityPolicy", []))

    @jsii.member(jsii_name="resetHttpApplicationRoutingEnabled")
    def reset_http_application_routing_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpApplicationRoutingEnabled", []))

    @jsii.member(jsii_name="resetHttpProxyConfig")
    def reset_http_proxy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpProxyConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetImageCleanerEnabled")
    def reset_image_cleaner_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageCleanerEnabled", []))

    @jsii.member(jsii_name="resetImageCleanerIntervalHours")
    def reset_image_cleaner_interval_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageCleanerIntervalHours", []))

    @jsii.member(jsii_name="resetIngressApplicationGateway")
    def reset_ingress_application_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressApplicationGateway", []))

    @jsii.member(jsii_name="resetKeyVaultSecretsProvider")
    def reset_key_vault_secrets_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultSecretsProvider", []))

    @jsii.member(jsii_name="resetKubeletIdentity")
    def reset_kubelet_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubeletIdentity", []))

    @jsii.member(jsii_name="resetKubernetesVersion")
    def reset_kubernetes_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesVersion", []))

    @jsii.member(jsii_name="resetLinuxProfile")
    def reset_linux_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinuxProfile", []))

    @jsii.member(jsii_name="resetLocalAccountDisabled")
    def reset_local_account_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalAccountDisabled", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetMicrosoftDefender")
    def reset_microsoft_defender(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicrosoftDefender", []))

    @jsii.member(jsii_name="resetMonitorMetrics")
    def reset_monitor_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorMetrics", []))

    @jsii.member(jsii_name="resetNetworkProfile")
    def reset_network_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkProfile", []))

    @jsii.member(jsii_name="resetNodeResourceGroup")
    def reset_node_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeResourceGroup", []))

    @jsii.member(jsii_name="resetOidcIssuerEnabled")
    def reset_oidc_issuer_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidcIssuerEnabled", []))

    @jsii.member(jsii_name="resetOmsAgent")
    def reset_oms_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOmsAgent", []))

    @jsii.member(jsii_name="resetOpenServiceMeshEnabled")
    def reset_open_service_mesh_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpenServiceMeshEnabled", []))

    @jsii.member(jsii_name="resetPrivateClusterEnabled")
    def reset_private_cluster_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateClusterEnabled", []))

    @jsii.member(jsii_name="resetPrivateClusterPublicFqdnEnabled")
    def reset_private_cluster_public_fqdn_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateClusterPublicFqdnEnabled", []))

    @jsii.member(jsii_name="resetPrivateDnsZoneId")
    def reset_private_dns_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateDnsZoneId", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetRoleBasedAccessControlEnabled")
    def reset_role_based_access_control_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleBasedAccessControlEnabled", []))

    @jsii.member(jsii_name="resetRunCommandEnabled")
    def reset_run_command_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunCommandEnabled", []))

    @jsii.member(jsii_name="resetServicePrincipal")
    def reset_service_principal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePrincipal", []))

    @jsii.member(jsii_name="resetSkuTier")
    def reset_sku_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkuTier", []))

    @jsii.member(jsii_name="resetStorageProfile")
    def reset_storage_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageProfile", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWebAppRouting")
    def reset_web_app_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebAppRouting", []))

    @jsii.member(jsii_name="resetWindowsProfile")
    def reset_windows_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsProfile", []))

    @jsii.member(jsii_name="resetWorkloadAutoscalerProfile")
    def reset_workload_autoscaler_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadAutoscalerProfile", []))

    @jsii.member(jsii_name="resetWorkloadIdentityEnabled")
    def reset_workload_identity_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadIdentityEnabled", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="aciConnectorLinux")
    def aci_connector_linux(
        self,
    ) -> "KubernetesClusterAciConnectorLinuxOutputReference":
        return typing.cast("KubernetesClusterAciConnectorLinuxOutputReference", jsii.get(self, "aciConnectorLinux"))

    @builtins.property
    @jsii.member(jsii_name="autoScalerProfile")
    def auto_scaler_profile(
        self,
    ) -> "KubernetesClusterAutoScalerProfileOutputReference":
        return typing.cast("KubernetesClusterAutoScalerProfileOutputReference", jsii.get(self, "autoScalerProfile"))

    @builtins.property
    @jsii.member(jsii_name="azureActiveDirectoryRoleBasedAccessControl")
    def azure_active_directory_role_based_access_control(
        self,
    ) -> "KubernetesClusterAzureActiveDirectoryRoleBasedAccessControlOutputReference":
        return typing.cast("KubernetesClusterAzureActiveDirectoryRoleBasedAccessControlOutputReference", jsii.get(self, "azureActiveDirectoryRoleBasedAccessControl"))

    @builtins.property
    @jsii.member(jsii_name="defaultNodePool")
    def default_node_pool(self) -> "KubernetesClusterDefaultNodePoolOutputReference":
        return typing.cast("KubernetesClusterDefaultNodePoolOutputReference", jsii.get(self, "defaultNodePool"))

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="httpApplicationRoutingZoneName")
    def http_application_routing_zone_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpApplicationRoutingZoneName"))

    @builtins.property
    @jsii.member(jsii_name="httpProxyConfig")
    def http_proxy_config(self) -> "KubernetesClusterHttpProxyConfigOutputReference":
        return typing.cast("KubernetesClusterHttpProxyConfigOutputReference", jsii.get(self, "httpProxyConfig"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "KubernetesClusterIdentityOutputReference":
        return typing.cast("KubernetesClusterIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="ingressApplicationGateway")
    def ingress_application_gateway(
        self,
    ) -> "KubernetesClusterIngressApplicationGatewayOutputReference":
        return typing.cast("KubernetesClusterIngressApplicationGatewayOutputReference", jsii.get(self, "ingressApplicationGateway"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretsProvider")
    def key_vault_secrets_provider(
        self,
    ) -> "KubernetesClusterKeyVaultSecretsProviderOutputReference":
        return typing.cast("KubernetesClusterKeyVaultSecretsProviderOutputReference", jsii.get(self, "keyVaultSecretsProvider"))

    @builtins.property
    @jsii.member(jsii_name="kubeAdminConfig")
    def kube_admin_config(self) -> "KubernetesClusterKubeAdminConfigList":
        return typing.cast("KubernetesClusterKubeAdminConfigList", jsii.get(self, "kubeAdminConfig"))

    @builtins.property
    @jsii.member(jsii_name="kubeAdminConfigRaw")
    def kube_admin_config_raw(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubeAdminConfigRaw"))

    @builtins.property
    @jsii.member(jsii_name="kubeConfig")
    def kube_config(self) -> "KubernetesClusterKubeConfigList":
        return typing.cast("KubernetesClusterKubeConfigList", jsii.get(self, "kubeConfig"))

    @builtins.property
    @jsii.member(jsii_name="kubeConfigRaw")
    def kube_config_raw(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubeConfigRaw"))

    @builtins.property
    @jsii.member(jsii_name="kubeletIdentity")
    def kubelet_identity(self) -> "KubernetesClusterKubeletIdentityOutputReference":
        return typing.cast("KubernetesClusterKubeletIdentityOutputReference", jsii.get(self, "kubeletIdentity"))

    @builtins.property
    @jsii.member(jsii_name="linuxProfile")
    def linux_profile(self) -> "KubernetesClusterLinuxProfileOutputReference":
        return typing.cast("KubernetesClusterLinuxProfileOutputReference", jsii.get(self, "linuxProfile"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(self) -> "KubernetesClusterMaintenanceWindowOutputReference":
        return typing.cast("KubernetesClusterMaintenanceWindowOutputReference", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="microsoftDefender")
    def microsoft_defender(self) -> "KubernetesClusterMicrosoftDefenderOutputReference":
        return typing.cast("KubernetesClusterMicrosoftDefenderOutputReference", jsii.get(self, "microsoftDefender"))

    @builtins.property
    @jsii.member(jsii_name="monitorMetrics")
    def monitor_metrics(self) -> "KubernetesClusterMonitorMetricsOutputReference":
        return typing.cast("KubernetesClusterMonitorMetricsOutputReference", jsii.get(self, "monitorMetrics"))

    @builtins.property
    @jsii.member(jsii_name="networkProfile")
    def network_profile(self) -> "KubernetesClusterNetworkProfileOutputReference":
        return typing.cast("KubernetesClusterNetworkProfileOutputReference", jsii.get(self, "networkProfile"))

    @builtins.property
    @jsii.member(jsii_name="oidcIssuerUrl")
    def oidc_issuer_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oidcIssuerUrl"))

    @builtins.property
    @jsii.member(jsii_name="omsAgent")
    def oms_agent(self) -> "KubernetesClusterOmsAgentOutputReference":
        return typing.cast("KubernetesClusterOmsAgentOutputReference", jsii.get(self, "omsAgent"))

    @builtins.property
    @jsii.member(jsii_name="portalFqdn")
    def portal_fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portalFqdn"))

    @builtins.property
    @jsii.member(jsii_name="privateFqdn")
    def private_fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateFqdn"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipal")
    def service_principal(self) -> "KubernetesClusterServicePrincipalOutputReference":
        return typing.cast("KubernetesClusterServicePrincipalOutputReference", jsii.get(self, "servicePrincipal"))

    @builtins.property
    @jsii.member(jsii_name="storageProfile")
    def storage_profile(self) -> "KubernetesClusterStorageProfileOutputReference":
        return typing.cast("KubernetesClusterStorageProfileOutputReference", jsii.get(self, "storageProfile"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KubernetesClusterTimeoutsOutputReference":
        return typing.cast("KubernetesClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="webAppRouting")
    def web_app_routing(self) -> "KubernetesClusterWebAppRoutingOutputReference":
        return typing.cast("KubernetesClusterWebAppRoutingOutputReference", jsii.get(self, "webAppRouting"))

    @builtins.property
    @jsii.member(jsii_name="windowsProfile")
    def windows_profile(self) -> "KubernetesClusterWindowsProfileOutputReference":
        return typing.cast("KubernetesClusterWindowsProfileOutputReference", jsii.get(self, "windowsProfile"))

    @builtins.property
    @jsii.member(jsii_name="workloadAutoscalerProfile")
    def workload_autoscaler_profile(
        self,
    ) -> "KubernetesClusterWorkloadAutoscalerProfileOutputReference":
        return typing.cast("KubernetesClusterWorkloadAutoscalerProfileOutputReference", jsii.get(self, "workloadAutoscalerProfile"))

    @builtins.property
    @jsii.member(jsii_name="aciConnectorLinuxInput")
    def aci_connector_linux_input(
        self,
    ) -> typing.Optional["KubernetesClusterAciConnectorLinux"]:
        return typing.cast(typing.Optional["KubernetesClusterAciConnectorLinux"], jsii.get(self, "aciConnectorLinuxInput"))

    @builtins.property
    @jsii.member(jsii_name="apiServerAuthorizedIpRangesInput")
    def api_server_authorized_ip_ranges_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apiServerAuthorizedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticChannelUpgradeInput")
    def automatic_channel_upgrade_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "automaticChannelUpgradeInput"))

    @builtins.property
    @jsii.member(jsii_name="autoScalerProfileInput")
    def auto_scaler_profile_input(
        self,
    ) -> typing.Optional["KubernetesClusterAutoScalerProfile"]:
        return typing.cast(typing.Optional["KubernetesClusterAutoScalerProfile"], jsii.get(self, "autoScalerProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="azureActiveDirectoryRoleBasedAccessControlInput")
    def azure_active_directory_role_based_access_control_input(
        self,
    ) -> typing.Optional["KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl"]:
        return typing.cast(typing.Optional["KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl"], jsii.get(self, "azureActiveDirectoryRoleBasedAccessControlInput"))

    @builtins.property
    @jsii.member(jsii_name="azurePolicyEnabledInput")
    def azure_policy_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "azurePolicyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultNodePoolInput")
    def default_node_pool_input(
        self,
    ) -> typing.Optional["KubernetesClusterDefaultNodePool"]:
        return typing.cast(typing.Optional["KubernetesClusterDefaultNodePool"], jsii.get(self, "defaultNodePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetIdInput")
    def disk_encryption_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsPrefixInput")
    def dns_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsPrefixPrivateClusterInput")
    def dns_prefix_private_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsPrefixPrivateClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeZoneInput")
    def edge_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePodSecurityPolicyInput")
    def enable_pod_security_policy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePodSecurityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="httpApplicationRoutingEnabledInput")
    def http_application_routing_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpApplicationRoutingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="httpProxyConfigInput")
    def http_proxy_config_input(
        self,
    ) -> typing.Optional["KubernetesClusterHttpProxyConfig"]:
        return typing.cast(typing.Optional["KubernetesClusterHttpProxyConfig"], jsii.get(self, "httpProxyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["KubernetesClusterIdentity"]:
        return typing.cast(typing.Optional["KubernetesClusterIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageCleanerEnabledInput")
    def image_cleaner_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "imageCleanerEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="imageCleanerIntervalHoursInput")
    def image_cleaner_interval_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageCleanerIntervalHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressApplicationGatewayInput")
    def ingress_application_gateway_input(
        self,
    ) -> typing.Optional["KubernetesClusterIngressApplicationGateway"]:
        return typing.cast(typing.Optional["KubernetesClusterIngressApplicationGateway"], jsii.get(self, "ingressApplicationGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultSecretsProviderInput")
    def key_vault_secrets_provider_input(
        self,
    ) -> typing.Optional["KubernetesClusterKeyVaultSecretsProvider"]:
        return typing.cast(typing.Optional["KubernetesClusterKeyVaultSecretsProvider"], jsii.get(self, "keyVaultSecretsProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="kubeletIdentityInput")
    def kubelet_identity_input(
        self,
    ) -> typing.Optional["KubernetesClusterKubeletIdentity"]:
        return typing.cast(typing.Optional["KubernetesClusterKubeletIdentity"], jsii.get(self, "kubeletIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesVersionInput")
    def kubernetes_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="linuxProfileInput")
    def linux_profile_input(self) -> typing.Optional["KubernetesClusterLinuxProfile"]:
        return typing.cast(typing.Optional["KubernetesClusterLinuxProfile"], jsii.get(self, "linuxProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="localAccountDisabledInput")
    def local_account_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localAccountDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional["KubernetesClusterMaintenanceWindow"]:
        return typing.cast(typing.Optional["KubernetesClusterMaintenanceWindow"], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftDefenderInput")
    def microsoft_defender_input(
        self,
    ) -> typing.Optional["KubernetesClusterMicrosoftDefender"]:
        return typing.cast(typing.Optional["KubernetesClusterMicrosoftDefender"], jsii.get(self, "microsoftDefenderInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorMetricsInput")
    def monitor_metrics_input(
        self,
    ) -> typing.Optional["KubernetesClusterMonitorMetrics"]:
        return typing.cast(typing.Optional["KubernetesClusterMonitorMetrics"], jsii.get(self, "monitorMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkProfileInput")
    def network_profile_input(
        self,
    ) -> typing.Optional["KubernetesClusterNetworkProfile"]:
        return typing.cast(typing.Optional["KubernetesClusterNetworkProfile"], jsii.get(self, "networkProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeResourceGroupInput")
    def node_resource_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeResourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcIssuerEnabledInput")
    def oidc_issuer_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "oidcIssuerEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="omsAgentInput")
    def oms_agent_input(self) -> typing.Optional["KubernetesClusterOmsAgent"]:
        return typing.cast(typing.Optional["KubernetesClusterOmsAgent"], jsii.get(self, "omsAgentInput"))

    @builtins.property
    @jsii.member(jsii_name="openServiceMeshEnabledInput")
    def open_service_mesh_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "openServiceMeshEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="privateClusterEnabledInput")
    def private_cluster_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privateClusterEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="privateClusterPublicFqdnEnabledInput")
    def private_cluster_public_fqdn_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privateClusterPublicFqdnEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="privateDnsZoneIdInput")
    def private_dns_zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateDnsZoneIdInput"))

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
    @jsii.member(jsii_name="roleBasedAccessControlEnabledInput")
    def role_based_access_control_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "roleBasedAccessControlEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="runCommandEnabledInput")
    def run_command_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runCommandEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalInput")
    def service_principal_input(
        self,
    ) -> typing.Optional["KubernetesClusterServicePrincipal"]:
        return typing.cast(typing.Optional["KubernetesClusterServicePrincipal"], jsii.get(self, "servicePrincipalInput"))

    @builtins.property
    @jsii.member(jsii_name="skuTierInput")
    def sku_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuTierInput"))

    @builtins.property
    @jsii.member(jsii_name="storageProfileInput")
    def storage_profile_input(
        self,
    ) -> typing.Optional["KubernetesClusterStorageProfile"]:
        return typing.cast(typing.Optional["KubernetesClusterStorageProfile"], jsii.get(self, "storageProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["KubernetesClusterTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["KubernetesClusterTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="webAppRoutingInput")
    def web_app_routing_input(
        self,
    ) -> typing.Optional["KubernetesClusterWebAppRouting"]:
        return typing.cast(typing.Optional["KubernetesClusterWebAppRouting"], jsii.get(self, "webAppRoutingInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsProfileInput")
    def windows_profile_input(
        self,
    ) -> typing.Optional["KubernetesClusterWindowsProfile"]:
        return typing.cast(typing.Optional["KubernetesClusterWindowsProfile"], jsii.get(self, "windowsProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadAutoscalerProfileInput")
    def workload_autoscaler_profile_input(
        self,
    ) -> typing.Optional["KubernetesClusterWorkloadAutoscalerProfile"]:
        return typing.cast(typing.Optional["KubernetesClusterWorkloadAutoscalerProfile"], jsii.get(self, "workloadAutoscalerProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityEnabledInput")
    def workload_identity_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "workloadIdentityEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="apiServerAuthorizedIpRanges")
    def api_server_authorized_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiServerAuthorizedIpRanges"))

    @api_server_authorized_ip_ranges.setter
    def api_server_authorized_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__582dde823364d3d292d3e328092b995493d5e15052d2787b0fbcc897c5f8d8ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiServerAuthorizedIpRanges", value)

    @builtins.property
    @jsii.member(jsii_name="automaticChannelUpgrade")
    def automatic_channel_upgrade(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "automaticChannelUpgrade"))

    @automatic_channel_upgrade.setter
    def automatic_channel_upgrade(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c06e8a93744e65ea41f990989bea8872a7a93ae3f8ac1308e59268051ddeabd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticChannelUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="azurePolicyEnabled")
    def azure_policy_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "azurePolicyEnabled"))

    @azure_policy_enabled.setter
    def azure_policy_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715b4afd55737e18bb367c2ee549d29a43249d4daee1aa36dfe4c71922f4a1c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azurePolicyEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionSetId")
    def disk_encryption_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionSetId"))

    @disk_encryption_set_id.setter
    def disk_encryption_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6554414a66e267cf74667cf0e7526a4a5695e3fdd16889992185ee5d1c3b7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionSetId", value)

    @builtins.property
    @jsii.member(jsii_name="dnsPrefix")
    def dns_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsPrefix"))

    @dns_prefix.setter
    def dns_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47109014c1c82426bd297eeea58079adff001cd23810b7d89347066f2af615b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="dnsPrefixPrivateCluster")
    def dns_prefix_private_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsPrefixPrivateCluster"))

    @dns_prefix_private_cluster.setter
    def dns_prefix_private_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b952f0e07d1d7acb7a380e65b766993dc015c34784786a674c7a4b2051d78a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsPrefixPrivateCluster", value)

    @builtins.property
    @jsii.member(jsii_name="edgeZone")
    def edge_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeZone"))

    @edge_zone.setter
    def edge_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0133a8bf763049472f7020c0d0d6c212661ce152e4ece61711458e9ef318827d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeZone", value)

    @builtins.property
    @jsii.member(jsii_name="enablePodSecurityPolicy")
    def enable_pod_security_policy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePodSecurityPolicy"))

    @enable_pod_security_policy.setter
    def enable_pod_security_policy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855cc036ef4c003c092ddb519d49836d1759f8c87e01c9e690bf2b3fe624a180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePodSecurityPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="httpApplicationRoutingEnabled")
    def http_application_routing_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpApplicationRoutingEnabled"))

    @http_application_routing_enabled.setter
    def http_application_routing_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b94249a6afe6d2c098d7b88a99d27dbb0d0457309a399872b2f27a779e56f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpApplicationRoutingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74e4aaa00d6360d9fc498b62c1ee6692ff384184b2802dd2db73e141ba4c079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="imageCleanerEnabled")
    def image_cleaner_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "imageCleanerEnabled"))

    @image_cleaner_enabled.setter
    def image_cleaner_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c80eaf170dd5942b27aa73b5dbec4fbc6c5c1f0709a4df4ac72602a27d43812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageCleanerEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="imageCleanerIntervalHours")
    def image_cleaner_interval_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageCleanerIntervalHours"))

    @image_cleaner_interval_hours.setter
    def image_cleaner_interval_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d2712cef0529aacde86896e5b205f72805ba3ae79d88079e6af4e6c78a25fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageCleanerIntervalHours", value)

    @builtins.property
    @jsii.member(jsii_name="kubernetesVersion")
    def kubernetes_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesVersion"))

    @kubernetes_version.setter
    def kubernetes_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4eb80977968be56080b990640a47520eedc5d2ccc1fa18564d74d438eae4809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesVersion", value)

    @builtins.property
    @jsii.member(jsii_name="localAccountDisabled")
    def local_account_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "localAccountDisabled"))

    @local_account_disabled.setter
    def local_account_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0a09d5a9b07d01d348e9118ecd6f62ca52bf274b9e6182ad8d6ff2250407dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAccountDisabled", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b22b38d2c019ce47a445aa4880fb44d853b5b27f2ad2077af7042bb11162154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3abdf0464f7b181b2de336e9358946ef52b1ba90a67d51d48c44fd03bb65ac51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nodeResourceGroup")
    def node_resource_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeResourceGroup"))

    @node_resource_group.setter
    def node_resource_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc5b0b484304154020fc2f13e3b347a8111dc0766ea3056be30fe707f52f3b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeResourceGroup", value)

    @builtins.property
    @jsii.member(jsii_name="oidcIssuerEnabled")
    def oidc_issuer_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "oidcIssuerEnabled"))

    @oidc_issuer_enabled.setter
    def oidc_issuer_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e538f940093aa6b614a5f229c1d340a39ef9c8a38393e084d05cc2fc530b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oidcIssuerEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="openServiceMeshEnabled")
    def open_service_mesh_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "openServiceMeshEnabled"))

    @open_service_mesh_enabled.setter
    def open_service_mesh_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9989347c527d6e283c9182909b0f34eea00dd6fc3c503a4e7b2d5ec8f1c06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "openServiceMeshEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="privateClusterEnabled")
    def private_cluster_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privateClusterEnabled"))

    @private_cluster_enabled.setter
    def private_cluster_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3598725d46f205d0eccfe4d0ec77c57ff8f7fc831c94e5c8871957a68ae0857c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateClusterEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="privateClusterPublicFqdnEnabled")
    def private_cluster_public_fqdn_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privateClusterPublicFqdnEnabled"))

    @private_cluster_public_fqdn_enabled.setter
    def private_cluster_public_fqdn_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e27c52f23f5c9e3a832499e49a8ec5d54880eb52dd4dc94e647ff05dc98f15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateClusterPublicFqdnEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="privateDnsZoneId")
    def private_dns_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateDnsZoneId"))

    @private_dns_zone_id.setter
    def private_dns_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16f0a2df36b8f40eea1f0bd9224083135d6856d766b8e6411e102378a49d372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateDnsZoneId", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__28531ca8e8bfa87f36ed0279b0cc0c2cce76630fb78b6372df1ca852df42be13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a781d10eb864942071a817e882239f815ed3fc79081cd31404e880b2a3117a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="roleBasedAccessControlEnabled")
    def role_based_access_control_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "roleBasedAccessControlEnabled"))

    @role_based_access_control_enabled.setter
    def role_based_access_control_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db7d6d55f0b710ef87479b188052fc6a28f7e40153c9c972d6a0077d8b7d8bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleBasedAccessControlEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="runCommandEnabled")
    def run_command_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runCommandEnabled"))

    @run_command_enabled.setter
    def run_command_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bbb7e1aa822a26f760595ba13573c76f606f9b7a28ea8ccc1f85cdadfe09a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runCommandEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="skuTier")
    def sku_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuTier"))

    @sku_tier.setter
    def sku_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a3f370bf96f12687f74553af6aece77b582d7ef104f8bf13a1d17f9821aa9fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuTier", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb01a15967585abb6329ad24958c3917c0f89bf7001bef35f86a9a29cb8758c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityEnabled")
    def workload_identity_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "workloadIdentityEnabled"))

    @workload_identity_enabled.setter
    def workload_identity_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69316152f2e32fc84978aae494d5ec2c5fe5bd1d3d92c239eaaa79ce1025ff95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadIdentityEnabled", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterAciConnectorLinux",
    jsii_struct_bases=[],
    name_mapping={"subnet_name": "subnetName"},
)
class KubernetesClusterAciConnectorLinux:
    def __init__(self, *, subnet_name: builtins.str) -> None:
        '''
        :param subnet_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#subnet_name KubernetesCluster#subnet_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607074898a400d1dbfc83ab061e17f21f4556d702ad0ce681441ad7002a1c528)
            check_type(argname="argument subnet_name", value=subnet_name, expected_type=type_hints["subnet_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_name": subnet_name,
        }

    @builtins.property
    def subnet_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#subnet_name KubernetesCluster#subnet_name}.'''
        result = self._values.get("subnet_name")
        assert result is not None, "Required property 'subnet_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterAciConnectorLinux(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterAciConnectorLinuxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterAciConnectorLinuxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac60ae4df6361a52a41737fcc8ab5e9587a062e0291780393dbd018f1e2f5227)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="subnetNameInput")
    def subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetName")
    def subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetName"))

    @subnet_name.setter
    def subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5c8db946b148801ec10790ba71cd7bb298fd30a87b1113cb94414e69f19165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterAciConnectorLinux]:
        return typing.cast(typing.Optional[KubernetesClusterAciConnectorLinux], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterAciConnectorLinux],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e6dffa8a73b32ffa6bcf9ea4219c506b363ef7842278facb867e0908b3ffb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterAutoScalerProfile",
    jsii_struct_bases=[],
    name_mapping={
        "balance_similar_node_groups": "balanceSimilarNodeGroups",
        "empty_bulk_delete_max": "emptyBulkDeleteMax",
        "expander": "expander",
        "max_graceful_termination_sec": "maxGracefulTerminationSec",
        "max_node_provisioning_time": "maxNodeProvisioningTime",
        "max_unready_nodes": "maxUnreadyNodes",
        "max_unready_percentage": "maxUnreadyPercentage",
        "new_pod_scale_up_delay": "newPodScaleUpDelay",
        "scale_down_delay_after_add": "scaleDownDelayAfterAdd",
        "scale_down_delay_after_delete": "scaleDownDelayAfterDelete",
        "scale_down_delay_after_failure": "scaleDownDelayAfterFailure",
        "scale_down_unneeded": "scaleDownUnneeded",
        "scale_down_unready": "scaleDownUnready",
        "scale_down_utilization_threshold": "scaleDownUtilizationThreshold",
        "scan_interval": "scanInterval",
        "skip_nodes_with_local_storage": "skipNodesWithLocalStorage",
        "skip_nodes_with_system_pods": "skipNodesWithSystemPods",
    },
)
class KubernetesClusterAutoScalerProfile:
    def __init__(
        self,
        *,
        balance_similar_node_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        empty_bulk_delete_max: typing.Optional[builtins.str] = None,
        expander: typing.Optional[builtins.str] = None,
        max_graceful_termination_sec: typing.Optional[builtins.str] = None,
        max_node_provisioning_time: typing.Optional[builtins.str] = None,
        max_unready_nodes: typing.Optional[jsii.Number] = None,
        max_unready_percentage: typing.Optional[jsii.Number] = None,
        new_pod_scale_up_delay: typing.Optional[builtins.str] = None,
        scale_down_delay_after_add: typing.Optional[builtins.str] = None,
        scale_down_delay_after_delete: typing.Optional[builtins.str] = None,
        scale_down_delay_after_failure: typing.Optional[builtins.str] = None,
        scale_down_unneeded: typing.Optional[builtins.str] = None,
        scale_down_unready: typing.Optional[builtins.str] = None,
        scale_down_utilization_threshold: typing.Optional[builtins.str] = None,
        scan_interval: typing.Optional[builtins.str] = None,
        skip_nodes_with_local_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_nodes_with_system_pods: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param balance_similar_node_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#balance_similar_node_groups KubernetesCluster#balance_similar_node_groups}.
        :param empty_bulk_delete_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#empty_bulk_delete_max KubernetesCluster#empty_bulk_delete_max}.
        :param expander: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#expander KubernetesCluster#expander}.
        :param max_graceful_termination_sec: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_graceful_termination_sec KubernetesCluster#max_graceful_termination_sec}.
        :param max_node_provisioning_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_node_provisioning_time KubernetesCluster#max_node_provisioning_time}.
        :param max_unready_nodes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_unready_nodes KubernetesCluster#max_unready_nodes}.
        :param max_unready_percentage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_unready_percentage KubernetesCluster#max_unready_percentage}.
        :param new_pod_scale_up_delay: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#new_pod_scale_up_delay KubernetesCluster#new_pod_scale_up_delay}.
        :param scale_down_delay_after_add: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_delay_after_add KubernetesCluster#scale_down_delay_after_add}.
        :param scale_down_delay_after_delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_delay_after_delete KubernetesCluster#scale_down_delay_after_delete}.
        :param scale_down_delay_after_failure: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_delay_after_failure KubernetesCluster#scale_down_delay_after_failure}.
        :param scale_down_unneeded: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_unneeded KubernetesCluster#scale_down_unneeded}.
        :param scale_down_unready: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_unready KubernetesCluster#scale_down_unready}.
        :param scale_down_utilization_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_utilization_threshold KubernetesCluster#scale_down_utilization_threshold}.
        :param scan_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scan_interval KubernetesCluster#scan_interval}.
        :param skip_nodes_with_local_storage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#skip_nodes_with_local_storage KubernetesCluster#skip_nodes_with_local_storage}.
        :param skip_nodes_with_system_pods: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#skip_nodes_with_system_pods KubernetesCluster#skip_nodes_with_system_pods}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831617a446d26cf4b19da83eeef042df1a97ed16a3bb453321366b344e56437e)
            check_type(argname="argument balance_similar_node_groups", value=balance_similar_node_groups, expected_type=type_hints["balance_similar_node_groups"])
            check_type(argname="argument empty_bulk_delete_max", value=empty_bulk_delete_max, expected_type=type_hints["empty_bulk_delete_max"])
            check_type(argname="argument expander", value=expander, expected_type=type_hints["expander"])
            check_type(argname="argument max_graceful_termination_sec", value=max_graceful_termination_sec, expected_type=type_hints["max_graceful_termination_sec"])
            check_type(argname="argument max_node_provisioning_time", value=max_node_provisioning_time, expected_type=type_hints["max_node_provisioning_time"])
            check_type(argname="argument max_unready_nodes", value=max_unready_nodes, expected_type=type_hints["max_unready_nodes"])
            check_type(argname="argument max_unready_percentage", value=max_unready_percentage, expected_type=type_hints["max_unready_percentage"])
            check_type(argname="argument new_pod_scale_up_delay", value=new_pod_scale_up_delay, expected_type=type_hints["new_pod_scale_up_delay"])
            check_type(argname="argument scale_down_delay_after_add", value=scale_down_delay_after_add, expected_type=type_hints["scale_down_delay_after_add"])
            check_type(argname="argument scale_down_delay_after_delete", value=scale_down_delay_after_delete, expected_type=type_hints["scale_down_delay_after_delete"])
            check_type(argname="argument scale_down_delay_after_failure", value=scale_down_delay_after_failure, expected_type=type_hints["scale_down_delay_after_failure"])
            check_type(argname="argument scale_down_unneeded", value=scale_down_unneeded, expected_type=type_hints["scale_down_unneeded"])
            check_type(argname="argument scale_down_unready", value=scale_down_unready, expected_type=type_hints["scale_down_unready"])
            check_type(argname="argument scale_down_utilization_threshold", value=scale_down_utilization_threshold, expected_type=type_hints["scale_down_utilization_threshold"])
            check_type(argname="argument scan_interval", value=scan_interval, expected_type=type_hints["scan_interval"])
            check_type(argname="argument skip_nodes_with_local_storage", value=skip_nodes_with_local_storage, expected_type=type_hints["skip_nodes_with_local_storage"])
            check_type(argname="argument skip_nodes_with_system_pods", value=skip_nodes_with_system_pods, expected_type=type_hints["skip_nodes_with_system_pods"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if balance_similar_node_groups is not None:
            self._values["balance_similar_node_groups"] = balance_similar_node_groups
        if empty_bulk_delete_max is not None:
            self._values["empty_bulk_delete_max"] = empty_bulk_delete_max
        if expander is not None:
            self._values["expander"] = expander
        if max_graceful_termination_sec is not None:
            self._values["max_graceful_termination_sec"] = max_graceful_termination_sec
        if max_node_provisioning_time is not None:
            self._values["max_node_provisioning_time"] = max_node_provisioning_time
        if max_unready_nodes is not None:
            self._values["max_unready_nodes"] = max_unready_nodes
        if max_unready_percentage is not None:
            self._values["max_unready_percentage"] = max_unready_percentage
        if new_pod_scale_up_delay is not None:
            self._values["new_pod_scale_up_delay"] = new_pod_scale_up_delay
        if scale_down_delay_after_add is not None:
            self._values["scale_down_delay_after_add"] = scale_down_delay_after_add
        if scale_down_delay_after_delete is not None:
            self._values["scale_down_delay_after_delete"] = scale_down_delay_after_delete
        if scale_down_delay_after_failure is not None:
            self._values["scale_down_delay_after_failure"] = scale_down_delay_after_failure
        if scale_down_unneeded is not None:
            self._values["scale_down_unneeded"] = scale_down_unneeded
        if scale_down_unready is not None:
            self._values["scale_down_unready"] = scale_down_unready
        if scale_down_utilization_threshold is not None:
            self._values["scale_down_utilization_threshold"] = scale_down_utilization_threshold
        if scan_interval is not None:
            self._values["scan_interval"] = scan_interval
        if skip_nodes_with_local_storage is not None:
            self._values["skip_nodes_with_local_storage"] = skip_nodes_with_local_storage
        if skip_nodes_with_system_pods is not None:
            self._values["skip_nodes_with_system_pods"] = skip_nodes_with_system_pods

    @builtins.property
    def balance_similar_node_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#balance_similar_node_groups KubernetesCluster#balance_similar_node_groups}.'''
        result = self._values.get("balance_similar_node_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def empty_bulk_delete_max(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#empty_bulk_delete_max KubernetesCluster#empty_bulk_delete_max}.'''
        result = self._values.get("empty_bulk_delete_max")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expander(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#expander KubernetesCluster#expander}.'''
        result = self._values.get("expander")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_graceful_termination_sec(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_graceful_termination_sec KubernetesCluster#max_graceful_termination_sec}.'''
        result = self._values.get("max_graceful_termination_sec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_node_provisioning_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_node_provisioning_time KubernetesCluster#max_node_provisioning_time}.'''
        result = self._values.get("max_node_provisioning_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_unready_nodes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_unready_nodes KubernetesCluster#max_unready_nodes}.'''
        result = self._values.get("max_unready_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_unready_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_unready_percentage KubernetesCluster#max_unready_percentage}.'''
        result = self._values.get("max_unready_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def new_pod_scale_up_delay(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#new_pod_scale_up_delay KubernetesCluster#new_pod_scale_up_delay}.'''
        result = self._values.get("new_pod_scale_up_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_delay_after_add(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_delay_after_add KubernetesCluster#scale_down_delay_after_add}.'''
        result = self._values.get("scale_down_delay_after_add")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_delay_after_delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_delay_after_delete KubernetesCluster#scale_down_delay_after_delete}.'''
        result = self._values.get("scale_down_delay_after_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_delay_after_failure(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_delay_after_failure KubernetesCluster#scale_down_delay_after_failure}.'''
        result = self._values.get("scale_down_delay_after_failure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_unneeded(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_unneeded KubernetesCluster#scale_down_unneeded}.'''
        result = self._values.get("scale_down_unneeded")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_unready(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_unready KubernetesCluster#scale_down_unready}.'''
        result = self._values.get("scale_down_unready")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_utilization_threshold(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_utilization_threshold KubernetesCluster#scale_down_utilization_threshold}.'''
        result = self._values.get("scale_down_utilization_threshold")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scan_interval(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scan_interval KubernetesCluster#scan_interval}.'''
        result = self._values.get("scan_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_nodes_with_local_storage(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#skip_nodes_with_local_storage KubernetesCluster#skip_nodes_with_local_storage}.'''
        result = self._values.get("skip_nodes_with_local_storage")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_nodes_with_system_pods(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#skip_nodes_with_system_pods KubernetesCluster#skip_nodes_with_system_pods}.'''
        result = self._values.get("skip_nodes_with_system_pods")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterAutoScalerProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterAutoScalerProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterAutoScalerProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__971c330a9a1f7db6f79d2c520a5b2ebb7d74da2f5affef53d178c57fee78b585)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBalanceSimilarNodeGroups")
    def reset_balance_similar_node_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBalanceSimilarNodeGroups", []))

    @jsii.member(jsii_name="resetEmptyBulkDeleteMax")
    def reset_empty_bulk_delete_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmptyBulkDeleteMax", []))

    @jsii.member(jsii_name="resetExpander")
    def reset_expander(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpander", []))

    @jsii.member(jsii_name="resetMaxGracefulTerminationSec")
    def reset_max_graceful_termination_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxGracefulTerminationSec", []))

    @jsii.member(jsii_name="resetMaxNodeProvisioningTime")
    def reset_max_node_provisioning_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNodeProvisioningTime", []))

    @jsii.member(jsii_name="resetMaxUnreadyNodes")
    def reset_max_unready_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnreadyNodes", []))

    @jsii.member(jsii_name="resetMaxUnreadyPercentage")
    def reset_max_unready_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUnreadyPercentage", []))

    @jsii.member(jsii_name="resetNewPodScaleUpDelay")
    def reset_new_pod_scale_up_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewPodScaleUpDelay", []))

    @jsii.member(jsii_name="resetScaleDownDelayAfterAdd")
    def reset_scale_down_delay_after_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDownDelayAfterAdd", []))

    @jsii.member(jsii_name="resetScaleDownDelayAfterDelete")
    def reset_scale_down_delay_after_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDownDelayAfterDelete", []))

    @jsii.member(jsii_name="resetScaleDownDelayAfterFailure")
    def reset_scale_down_delay_after_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDownDelayAfterFailure", []))

    @jsii.member(jsii_name="resetScaleDownUnneeded")
    def reset_scale_down_unneeded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDownUnneeded", []))

    @jsii.member(jsii_name="resetScaleDownUnready")
    def reset_scale_down_unready(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDownUnready", []))

    @jsii.member(jsii_name="resetScaleDownUtilizationThreshold")
    def reset_scale_down_utilization_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDownUtilizationThreshold", []))

    @jsii.member(jsii_name="resetScanInterval")
    def reset_scan_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanInterval", []))

    @jsii.member(jsii_name="resetSkipNodesWithLocalStorage")
    def reset_skip_nodes_with_local_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipNodesWithLocalStorage", []))

    @jsii.member(jsii_name="resetSkipNodesWithSystemPods")
    def reset_skip_nodes_with_system_pods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipNodesWithSystemPods", []))

    @builtins.property
    @jsii.member(jsii_name="balanceSimilarNodeGroupsInput")
    def balance_similar_node_groups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "balanceSimilarNodeGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="emptyBulkDeleteMaxInput")
    def empty_bulk_delete_max_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emptyBulkDeleteMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="expanderInput")
    def expander_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expanderInput"))

    @builtins.property
    @jsii.member(jsii_name="maxGracefulTerminationSecInput")
    def max_graceful_termination_sec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxGracefulTerminationSecInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeProvisioningTimeInput")
    def max_node_provisioning_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxNodeProvisioningTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnreadyNodesInput")
    def max_unready_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnreadyNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUnreadyPercentageInput")
    def max_unready_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUnreadyPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="newPodScaleUpDelayInput")
    def new_pod_scale_up_delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newPodScaleUpDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownDelayAfterAddInput")
    def scale_down_delay_after_add_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scaleDownDelayAfterAddInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownDelayAfterDeleteInput")
    def scale_down_delay_after_delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scaleDownDelayAfterDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownDelayAfterFailureInput")
    def scale_down_delay_after_failure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scaleDownDelayAfterFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownUnneededInput")
    def scale_down_unneeded_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scaleDownUnneededInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownUnreadyInput")
    def scale_down_unready_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scaleDownUnreadyInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownUtilizationThresholdInput")
    def scale_down_utilization_threshold_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scaleDownUtilizationThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="scanIntervalInput")
    def scan_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scanIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="skipNodesWithLocalStorageInput")
    def skip_nodes_with_local_storage_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipNodesWithLocalStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="skipNodesWithSystemPodsInput")
    def skip_nodes_with_system_pods_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipNodesWithSystemPodsInput"))

    @builtins.property
    @jsii.member(jsii_name="balanceSimilarNodeGroups")
    def balance_similar_node_groups(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "balanceSimilarNodeGroups"))

    @balance_similar_node_groups.setter
    def balance_similar_node_groups(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07b403ece3b8d03e56ecdf59d7b1b49364882852ee37c2168a9f0c943e7b4eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "balanceSimilarNodeGroups", value)

    @builtins.property
    @jsii.member(jsii_name="emptyBulkDeleteMax")
    def empty_bulk_delete_max(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emptyBulkDeleteMax"))

    @empty_bulk_delete_max.setter
    def empty_bulk_delete_max(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5323f23d5746df83afd352319328535f447fbd57425a2982b84a67620bffd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emptyBulkDeleteMax", value)

    @builtins.property
    @jsii.member(jsii_name="expander")
    def expander(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expander"))

    @expander.setter
    def expander(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01996b7de5515c40ffd236ad36c3111b0e0facaaa7ef5da6741a28ac8daa23c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expander", value)

    @builtins.property
    @jsii.member(jsii_name="maxGracefulTerminationSec")
    def max_graceful_termination_sec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxGracefulTerminationSec"))

    @max_graceful_termination_sec.setter
    def max_graceful_termination_sec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78f4d5b97cd70f8cd3f132f6cbdbb9e69869566575183c43d17c868f06ff454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxGracefulTerminationSec", value)

    @builtins.property
    @jsii.member(jsii_name="maxNodeProvisioningTime")
    def max_node_provisioning_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxNodeProvisioningTime"))

    @max_node_provisioning_time.setter
    def max_node_provisioning_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556ef2ecb57013c5ade1fc1e8d3619252233b2dfcdad5505707aa48a82d25dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeProvisioningTime", value)

    @builtins.property
    @jsii.member(jsii_name="maxUnreadyNodes")
    def max_unready_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnreadyNodes"))

    @max_unready_nodes.setter
    def max_unready_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f641f09ec31d69f4c5777fdc275830b3b8db14099fb59b551d7ce69827d19f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnreadyNodes", value)

    @builtins.property
    @jsii.member(jsii_name="maxUnreadyPercentage")
    def max_unready_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUnreadyPercentage"))

    @max_unready_percentage.setter
    def max_unready_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faeb880ccd1cf296f9b86c751688b712625b66737c122eb6a203b0b6f878834d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUnreadyPercentage", value)

    @builtins.property
    @jsii.member(jsii_name="newPodScaleUpDelay")
    def new_pod_scale_up_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newPodScaleUpDelay"))

    @new_pod_scale_up_delay.setter
    def new_pod_scale_up_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d00ddb62653bb7b367e88320c93a234ed48cfb2033eaf66adee1f6282711487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newPodScaleUpDelay", value)

    @builtins.property
    @jsii.member(jsii_name="scaleDownDelayAfterAdd")
    def scale_down_delay_after_add(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scaleDownDelayAfterAdd"))

    @scale_down_delay_after_add.setter
    def scale_down_delay_after_add(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08997754a87e618e00409636e13a438bd2defb0347bef3fc9ef743f2415ec05f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownDelayAfterAdd", value)

    @builtins.property
    @jsii.member(jsii_name="scaleDownDelayAfterDelete")
    def scale_down_delay_after_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scaleDownDelayAfterDelete"))

    @scale_down_delay_after_delete.setter
    def scale_down_delay_after_delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f83619f675cb901fb9e4fdfdb93c97831969df75581adb26856bbca28fe5e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownDelayAfterDelete", value)

    @builtins.property
    @jsii.member(jsii_name="scaleDownDelayAfterFailure")
    def scale_down_delay_after_failure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scaleDownDelayAfterFailure"))

    @scale_down_delay_after_failure.setter
    def scale_down_delay_after_failure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ceb97098b7f8e5c6ce6a16d6b356f595bedd029b4ece908880b1a4d666f65e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownDelayAfterFailure", value)

    @builtins.property
    @jsii.member(jsii_name="scaleDownUnneeded")
    def scale_down_unneeded(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scaleDownUnneeded"))

    @scale_down_unneeded.setter
    def scale_down_unneeded(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599239132e0e5d583629441c4aa4e134ef93022b6cb666cd24867ccc1ed860e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownUnneeded", value)

    @builtins.property
    @jsii.member(jsii_name="scaleDownUnready")
    def scale_down_unready(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scaleDownUnready"))

    @scale_down_unready.setter
    def scale_down_unready(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ab15a3ba35e0d059d9efdaba8d048aedc43f2139e62379d00889ed2a6cf8b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownUnready", value)

    @builtins.property
    @jsii.member(jsii_name="scaleDownUtilizationThreshold")
    def scale_down_utilization_threshold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scaleDownUtilizationThreshold"))

    @scale_down_utilization_threshold.setter
    def scale_down_utilization_threshold(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d07229cd3e2168445fae7b9fbf5bec73770d3b5bdc80e7abaacb5fd4dde357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownUtilizationThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="scanInterval")
    def scan_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scanInterval"))

    @scan_interval.setter
    def scan_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e0673d144092e3d7e8869eda8f4ef23c9fea1d41633f8be6b938216c6196e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanInterval", value)

    @builtins.property
    @jsii.member(jsii_name="skipNodesWithLocalStorage")
    def skip_nodes_with_local_storage(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipNodesWithLocalStorage"))

    @skip_nodes_with_local_storage.setter
    def skip_nodes_with_local_storage(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7282f2ab8547698958ee19519035103b92439a8dbf6147633ab71b737ae6bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipNodesWithLocalStorage", value)

    @builtins.property
    @jsii.member(jsii_name="skipNodesWithSystemPods")
    def skip_nodes_with_system_pods(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipNodesWithSystemPods"))

    @skip_nodes_with_system_pods.setter
    def skip_nodes_with_system_pods(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3af00c5c4b86c0681252d0c31fe094bad76535a48baeaa630dbf1211b45b68c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipNodesWithSystemPods", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterAutoScalerProfile]:
        return typing.cast(typing.Optional[KubernetesClusterAutoScalerProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterAutoScalerProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f30ca8ba54343404e43f706c87e1876e787a8680071dc8517cfb83e3e4f2814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl",
    jsii_struct_bases=[],
    name_mapping={
        "admin_group_object_ids": "adminGroupObjectIds",
        "azure_rbac_enabled": "azureRbacEnabled",
        "client_app_id": "clientAppId",
        "managed": "managed",
        "server_app_id": "serverAppId",
        "server_app_secret": "serverAppSecret",
        "tenant_id": "tenantId",
    },
)
class KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl:
    def __init__(
        self,
        *,
        admin_group_object_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        azure_rbac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_app_id: typing.Optional[builtins.str] = None,
        managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_app_id: typing.Optional[builtins.str] = None,
        server_app_secret: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_group_object_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_group_object_ids KubernetesCluster#admin_group_object_ids}.
        :param azure_rbac_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#azure_rbac_enabled KubernetesCluster#azure_rbac_enabled}.
        :param client_app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_app_id KubernetesCluster#client_app_id}.
        :param managed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed KubernetesCluster#managed}.
        :param server_app_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#server_app_id KubernetesCluster#server_app_id}.
        :param server_app_secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#server_app_secret KubernetesCluster#server_app_secret}.
        :param tenant_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#tenant_id KubernetesCluster#tenant_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d8040b4e7c0b0f85eff013a32ec1b824579b9f264b11867ce58475fc2248a5)
            check_type(argname="argument admin_group_object_ids", value=admin_group_object_ids, expected_type=type_hints["admin_group_object_ids"])
            check_type(argname="argument azure_rbac_enabled", value=azure_rbac_enabled, expected_type=type_hints["azure_rbac_enabled"])
            check_type(argname="argument client_app_id", value=client_app_id, expected_type=type_hints["client_app_id"])
            check_type(argname="argument managed", value=managed, expected_type=type_hints["managed"])
            check_type(argname="argument server_app_id", value=server_app_id, expected_type=type_hints["server_app_id"])
            check_type(argname="argument server_app_secret", value=server_app_secret, expected_type=type_hints["server_app_secret"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_group_object_ids is not None:
            self._values["admin_group_object_ids"] = admin_group_object_ids
        if azure_rbac_enabled is not None:
            self._values["azure_rbac_enabled"] = azure_rbac_enabled
        if client_app_id is not None:
            self._values["client_app_id"] = client_app_id
        if managed is not None:
            self._values["managed"] = managed
        if server_app_id is not None:
            self._values["server_app_id"] = server_app_id
        if server_app_secret is not None:
            self._values["server_app_secret"] = server_app_secret
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id

    @builtins.property
    def admin_group_object_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_group_object_ids KubernetesCluster#admin_group_object_ids}.'''
        result = self._values.get("admin_group_object_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def azure_rbac_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#azure_rbac_enabled KubernetesCluster#azure_rbac_enabled}.'''
        result = self._values.get("azure_rbac_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_app_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_app_id KubernetesCluster#client_app_id}.'''
        result = self._values.get("client_app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed KubernetesCluster#managed}.'''
        result = self._values.get("managed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def server_app_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#server_app_id KubernetesCluster#server_app_id}.'''
        result = self._values.get("server_app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_app_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#server_app_secret KubernetesCluster#server_app_secret}.'''
        result = self._values.get("server_app_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#tenant_id KubernetesCluster#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterAzureActiveDirectoryRoleBasedAccessControlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterAzureActiveDirectoryRoleBasedAccessControlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb10bf7d3f0c6163bfe80e4bf6d152b4aed923ac32b74890e06529727a2a7c09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdminGroupObjectIds")
    def reset_admin_group_object_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminGroupObjectIds", []))

    @jsii.member(jsii_name="resetAzureRbacEnabled")
    def reset_azure_rbac_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureRbacEnabled", []))

    @jsii.member(jsii_name="resetClientAppId")
    def reset_client_app_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientAppId", []))

    @jsii.member(jsii_name="resetManaged")
    def reset_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManaged", []))

    @jsii.member(jsii_name="resetServerAppId")
    def reset_server_app_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerAppId", []))

    @jsii.member(jsii_name="resetServerAppSecret")
    def reset_server_app_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerAppSecret", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @builtins.property
    @jsii.member(jsii_name="adminGroupObjectIdsInput")
    def admin_group_object_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "adminGroupObjectIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="azureRbacEnabledInput")
    def azure_rbac_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "azureRbacEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="clientAppIdInput")
    def client_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="managedInput")
    def managed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "managedInput"))

    @builtins.property
    @jsii.member(jsii_name="serverAppIdInput")
    def server_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serverAppSecretInput")
    def server_app_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverAppSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="adminGroupObjectIds")
    def admin_group_object_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "adminGroupObjectIds"))

    @admin_group_object_ids.setter
    def admin_group_object_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6330883a838c3f3331f4e2b7d7864c5e81d55d0589a866aa2c5a8873a98e6c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminGroupObjectIds", value)

    @builtins.property
    @jsii.member(jsii_name="azureRbacEnabled")
    def azure_rbac_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "azureRbacEnabled"))

    @azure_rbac_enabled.setter
    def azure_rbac_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e69f0fb600eb03e1aa210e2db0c013ef22519879b67327891744c13cdf3052d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureRbacEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="clientAppId")
    def client_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientAppId"))

    @client_app_id.setter
    def client_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36bfabfc303b7a0aca4d72f794b0c44395939ece0737a3f40044cc73c9ec35e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientAppId", value)

    @builtins.property
    @jsii.member(jsii_name="managed")
    def managed(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "managed"))

    @managed.setter
    def managed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394f764bf5be8cbddb7e22eb0ba8a77bc33982899e67653a52322fd98a455154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managed", value)

    @builtins.property
    @jsii.member(jsii_name="serverAppId")
    def server_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverAppId"))

    @server_app_id.setter
    def server_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0e0e447ec8891729725a2f0a66bc75fedfea2e14152c3ab8005ec3a2e8924d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverAppId", value)

    @builtins.property
    @jsii.member(jsii_name="serverAppSecret")
    def server_app_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverAppSecret"))

    @server_app_secret.setter
    def server_app_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec24a3c0b2afa1edb8e4212b8edd80faa462747c6de959b65fd0b0169520b6e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverAppSecret", value)

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0b71ce1a9fda8d8918500b3cacab804bfcbca2a3984dd45a92aff6e5268a127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl]:
        return typing.cast(typing.Optional[KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c788f2f29c0cba845a8a40bbfa9ee2785f1aa2cb3ec47272891aafb3120da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_node_pool": "defaultNodePool",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "aci_connector_linux": "aciConnectorLinux",
        "api_server_authorized_ip_ranges": "apiServerAuthorizedIpRanges",
        "automatic_channel_upgrade": "automaticChannelUpgrade",
        "auto_scaler_profile": "autoScalerProfile",
        "azure_active_directory_role_based_access_control": "azureActiveDirectoryRoleBasedAccessControl",
        "azure_policy_enabled": "azurePolicyEnabled",
        "disk_encryption_set_id": "diskEncryptionSetId",
        "dns_prefix": "dnsPrefix",
        "dns_prefix_private_cluster": "dnsPrefixPrivateCluster",
        "edge_zone": "edgeZone",
        "enable_pod_security_policy": "enablePodSecurityPolicy",
        "http_application_routing_enabled": "httpApplicationRoutingEnabled",
        "http_proxy_config": "httpProxyConfig",
        "id": "id",
        "identity": "identity",
        "image_cleaner_enabled": "imageCleanerEnabled",
        "image_cleaner_interval_hours": "imageCleanerIntervalHours",
        "ingress_application_gateway": "ingressApplicationGateway",
        "key_vault_secrets_provider": "keyVaultSecretsProvider",
        "kubelet_identity": "kubeletIdentity",
        "kubernetes_version": "kubernetesVersion",
        "linux_profile": "linuxProfile",
        "local_account_disabled": "localAccountDisabled",
        "maintenance_window": "maintenanceWindow",
        "microsoft_defender": "microsoftDefender",
        "monitor_metrics": "monitorMetrics",
        "network_profile": "networkProfile",
        "node_resource_group": "nodeResourceGroup",
        "oidc_issuer_enabled": "oidcIssuerEnabled",
        "oms_agent": "omsAgent",
        "open_service_mesh_enabled": "openServiceMeshEnabled",
        "private_cluster_enabled": "privateClusterEnabled",
        "private_cluster_public_fqdn_enabled": "privateClusterPublicFqdnEnabled",
        "private_dns_zone_id": "privateDnsZoneId",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "role_based_access_control_enabled": "roleBasedAccessControlEnabled",
        "run_command_enabled": "runCommandEnabled",
        "service_principal": "servicePrincipal",
        "sku_tier": "skuTier",
        "storage_profile": "storageProfile",
        "tags": "tags",
        "timeouts": "timeouts",
        "web_app_routing": "webAppRouting",
        "windows_profile": "windowsProfile",
        "workload_autoscaler_profile": "workloadAutoscalerProfile",
        "workload_identity_enabled": "workloadIdentityEnabled",
    },
)
class KubernetesClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_node_pool: typing.Union["KubernetesClusterDefaultNodePool", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        aci_connector_linux: typing.Optional[typing.Union[KubernetesClusterAciConnectorLinux, typing.Dict[builtins.str, typing.Any]]] = None,
        api_server_authorized_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        automatic_channel_upgrade: typing.Optional[builtins.str] = None,
        auto_scaler_profile: typing.Optional[typing.Union[KubernetesClusterAutoScalerProfile, typing.Dict[builtins.str, typing.Any]]] = None,
        azure_active_directory_role_based_access_control: typing.Optional[typing.Union[KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
        azure_policy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_encryption_set_id: typing.Optional[builtins.str] = None,
        dns_prefix: typing.Optional[builtins.str] = None,
        dns_prefix_private_cluster: typing.Optional[builtins.str] = None,
        edge_zone: typing.Optional[builtins.str] = None,
        enable_pod_security_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_application_routing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_proxy_config: typing.Optional[typing.Union["KubernetesClusterHttpProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["KubernetesClusterIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        image_cleaner_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image_cleaner_interval_hours: typing.Optional[jsii.Number] = None,
        ingress_application_gateway: typing.Optional[typing.Union["KubernetesClusterIngressApplicationGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_secrets_provider: typing.Optional[typing.Union["KubernetesClusterKeyVaultSecretsProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        kubelet_identity: typing.Optional[typing.Union["KubernetesClusterKubeletIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes_version: typing.Optional[builtins.str] = None,
        linux_profile: typing.Optional[typing.Union["KubernetesClusterLinuxProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        local_account_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maintenance_window: typing.Optional[typing.Union["KubernetesClusterMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        microsoft_defender: typing.Optional[typing.Union["KubernetesClusterMicrosoftDefender", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_metrics: typing.Optional[typing.Union["KubernetesClusterMonitorMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        network_profile: typing.Optional[typing.Union["KubernetesClusterNetworkProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        node_resource_group: typing.Optional[builtins.str] = None,
        oidc_issuer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        oms_agent: typing.Optional[typing.Union["KubernetesClusterOmsAgent", typing.Dict[builtins.str, typing.Any]]] = None,
        open_service_mesh_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_cluster_public_fqdn_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_dns_zone_id: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        role_based_access_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_command_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_principal: typing.Optional[typing.Union["KubernetesClusterServicePrincipal", typing.Dict[builtins.str, typing.Any]]] = None,
        sku_tier: typing.Optional[builtins.str] = None,
        storage_profile: typing.Optional[typing.Union["KubernetesClusterStorageProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KubernetesClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        web_app_routing: typing.Optional[typing.Union["KubernetesClusterWebAppRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        windows_profile: typing.Optional[typing.Union["KubernetesClusterWindowsProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_autoscaler_profile: typing.Optional[typing.Union["KubernetesClusterWorkloadAutoscalerProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_identity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_node_pool: default_node_pool block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#default_node_pool KubernetesCluster#default_node_pool}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#location KubernetesCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#name KubernetesCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#resource_group_name KubernetesCluster#resource_group_name}.
        :param aci_connector_linux: aci_connector_linux block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#aci_connector_linux KubernetesCluster#aci_connector_linux}
        :param api_server_authorized_ip_ranges: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#api_server_authorized_ip_ranges KubernetesCluster#api_server_authorized_ip_ranges}.
        :param automatic_channel_upgrade: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#automatic_channel_upgrade KubernetesCluster#automatic_channel_upgrade}.
        :param auto_scaler_profile: auto_scaler_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#auto_scaler_profile KubernetesCluster#auto_scaler_profile}
        :param azure_active_directory_role_based_access_control: azure_active_directory_role_based_access_control block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#azure_active_directory_role_based_access_control KubernetesCluster#azure_active_directory_role_based_access_control}
        :param azure_policy_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#azure_policy_enabled KubernetesCluster#azure_policy_enabled}.
        :param disk_encryption_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#disk_encryption_set_id KubernetesCluster#disk_encryption_set_id}.
        :param dns_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_prefix KubernetesCluster#dns_prefix}.
        :param dns_prefix_private_cluster: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_prefix_private_cluster KubernetesCluster#dns_prefix_private_cluster}.
        :param edge_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#edge_zone KubernetesCluster#edge_zone}.
        :param enable_pod_security_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_pod_security_policy KubernetesCluster#enable_pod_security_policy}.
        :param http_application_routing_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#http_application_routing_enabled KubernetesCluster#http_application_routing_enabled}.
        :param http_proxy_config: http_proxy_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#http_proxy_config KubernetesCluster#http_proxy_config}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#id KubernetesCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#identity KubernetesCluster#identity}
        :param image_cleaner_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_cleaner_enabled KubernetesCluster#image_cleaner_enabled}.
        :param image_cleaner_interval_hours: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_cleaner_interval_hours KubernetesCluster#image_cleaner_interval_hours}.
        :param ingress_application_gateway: ingress_application_gateway block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ingress_application_gateway KubernetesCluster#ingress_application_gateway}
        :param key_vault_secrets_provider: key_vault_secrets_provider block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#key_vault_secrets_provider KubernetesCluster#key_vault_secrets_provider}
        :param kubelet_identity: kubelet_identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubelet_identity KubernetesCluster#kubelet_identity}
        :param kubernetes_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubernetes_version KubernetesCluster#kubernetes_version}.
        :param linux_profile: linux_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#linux_profile KubernetesCluster#linux_profile}
        :param local_account_disabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#local_account_disabled KubernetesCluster#local_account_disabled}.
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#maintenance_window KubernetesCluster#maintenance_window}
        :param microsoft_defender: microsoft_defender block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#microsoft_defender KubernetesCluster#microsoft_defender}
        :param monitor_metrics: monitor_metrics block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#monitor_metrics KubernetesCluster#monitor_metrics}
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_profile KubernetesCluster#network_profile}
        :param node_resource_group: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_resource_group KubernetesCluster#node_resource_group}.
        :param oidc_issuer_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#oidc_issuer_enabled KubernetesCluster#oidc_issuer_enabled}.
        :param oms_agent: oms_agent block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#oms_agent KubernetesCluster#oms_agent}
        :param open_service_mesh_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#open_service_mesh_enabled KubernetesCluster#open_service_mesh_enabled}.
        :param private_cluster_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#private_cluster_enabled KubernetesCluster#private_cluster_enabled}.
        :param private_cluster_public_fqdn_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#private_cluster_public_fqdn_enabled KubernetesCluster#private_cluster_public_fqdn_enabled}.
        :param private_dns_zone_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#private_dns_zone_id KubernetesCluster#private_dns_zone_id}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#public_network_access_enabled KubernetesCluster#public_network_access_enabled}.
        :param role_based_access_control_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#role_based_access_control_enabled KubernetesCluster#role_based_access_control_enabled}.
        :param run_command_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#run_command_enabled KubernetesCluster#run_command_enabled}.
        :param service_principal: service_principal block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#service_principal KubernetesCluster#service_principal}
        :param sku_tier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#sku_tier KubernetesCluster#sku_tier}.
        :param storage_profile: storage_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#storage_profile KubernetesCluster#storage_profile}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#tags KubernetesCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#timeouts KubernetesCluster#timeouts}
        :param web_app_routing: web_app_routing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#web_app_routing KubernetesCluster#web_app_routing}
        :param windows_profile: windows_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#windows_profile KubernetesCluster#windows_profile}
        :param workload_autoscaler_profile: workload_autoscaler_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#workload_autoscaler_profile KubernetesCluster#workload_autoscaler_profile}
        :param workload_identity_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#workload_identity_enabled KubernetesCluster#workload_identity_enabled}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_node_pool, dict):
            default_node_pool = KubernetesClusterDefaultNodePool(**default_node_pool)
        if isinstance(aci_connector_linux, dict):
            aci_connector_linux = KubernetesClusterAciConnectorLinux(**aci_connector_linux)
        if isinstance(auto_scaler_profile, dict):
            auto_scaler_profile = KubernetesClusterAutoScalerProfile(**auto_scaler_profile)
        if isinstance(azure_active_directory_role_based_access_control, dict):
            azure_active_directory_role_based_access_control = KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl(**azure_active_directory_role_based_access_control)
        if isinstance(http_proxy_config, dict):
            http_proxy_config = KubernetesClusterHttpProxyConfig(**http_proxy_config)
        if isinstance(identity, dict):
            identity = KubernetesClusterIdentity(**identity)
        if isinstance(ingress_application_gateway, dict):
            ingress_application_gateway = KubernetesClusterIngressApplicationGateway(**ingress_application_gateway)
        if isinstance(key_vault_secrets_provider, dict):
            key_vault_secrets_provider = KubernetesClusterKeyVaultSecretsProvider(**key_vault_secrets_provider)
        if isinstance(kubelet_identity, dict):
            kubelet_identity = KubernetesClusterKubeletIdentity(**kubelet_identity)
        if isinstance(linux_profile, dict):
            linux_profile = KubernetesClusterLinuxProfile(**linux_profile)
        if isinstance(maintenance_window, dict):
            maintenance_window = KubernetesClusterMaintenanceWindow(**maintenance_window)
        if isinstance(microsoft_defender, dict):
            microsoft_defender = KubernetesClusterMicrosoftDefender(**microsoft_defender)
        if isinstance(monitor_metrics, dict):
            monitor_metrics = KubernetesClusterMonitorMetrics(**monitor_metrics)
        if isinstance(network_profile, dict):
            network_profile = KubernetesClusterNetworkProfile(**network_profile)
        if isinstance(oms_agent, dict):
            oms_agent = KubernetesClusterOmsAgent(**oms_agent)
        if isinstance(service_principal, dict):
            service_principal = KubernetesClusterServicePrincipal(**service_principal)
        if isinstance(storage_profile, dict):
            storage_profile = KubernetesClusterStorageProfile(**storage_profile)
        if isinstance(timeouts, dict):
            timeouts = KubernetesClusterTimeouts(**timeouts)
        if isinstance(web_app_routing, dict):
            web_app_routing = KubernetesClusterWebAppRouting(**web_app_routing)
        if isinstance(windows_profile, dict):
            windows_profile = KubernetesClusterWindowsProfile(**windows_profile)
        if isinstance(workload_autoscaler_profile, dict):
            workload_autoscaler_profile = KubernetesClusterWorkloadAutoscalerProfile(**workload_autoscaler_profile)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c27101fa956b9dcd1f20b6d95db8d4240a517affd5768be3aaf7f703c03223)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_node_pool", value=default_node_pool, expected_type=type_hints["default_node_pool"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument aci_connector_linux", value=aci_connector_linux, expected_type=type_hints["aci_connector_linux"])
            check_type(argname="argument api_server_authorized_ip_ranges", value=api_server_authorized_ip_ranges, expected_type=type_hints["api_server_authorized_ip_ranges"])
            check_type(argname="argument automatic_channel_upgrade", value=automatic_channel_upgrade, expected_type=type_hints["automatic_channel_upgrade"])
            check_type(argname="argument auto_scaler_profile", value=auto_scaler_profile, expected_type=type_hints["auto_scaler_profile"])
            check_type(argname="argument azure_active_directory_role_based_access_control", value=azure_active_directory_role_based_access_control, expected_type=type_hints["azure_active_directory_role_based_access_control"])
            check_type(argname="argument azure_policy_enabled", value=azure_policy_enabled, expected_type=type_hints["azure_policy_enabled"])
            check_type(argname="argument disk_encryption_set_id", value=disk_encryption_set_id, expected_type=type_hints["disk_encryption_set_id"])
            check_type(argname="argument dns_prefix", value=dns_prefix, expected_type=type_hints["dns_prefix"])
            check_type(argname="argument dns_prefix_private_cluster", value=dns_prefix_private_cluster, expected_type=type_hints["dns_prefix_private_cluster"])
            check_type(argname="argument edge_zone", value=edge_zone, expected_type=type_hints["edge_zone"])
            check_type(argname="argument enable_pod_security_policy", value=enable_pod_security_policy, expected_type=type_hints["enable_pod_security_policy"])
            check_type(argname="argument http_application_routing_enabled", value=http_application_routing_enabled, expected_type=type_hints["http_application_routing_enabled"])
            check_type(argname="argument http_proxy_config", value=http_proxy_config, expected_type=type_hints["http_proxy_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument image_cleaner_enabled", value=image_cleaner_enabled, expected_type=type_hints["image_cleaner_enabled"])
            check_type(argname="argument image_cleaner_interval_hours", value=image_cleaner_interval_hours, expected_type=type_hints["image_cleaner_interval_hours"])
            check_type(argname="argument ingress_application_gateway", value=ingress_application_gateway, expected_type=type_hints["ingress_application_gateway"])
            check_type(argname="argument key_vault_secrets_provider", value=key_vault_secrets_provider, expected_type=type_hints["key_vault_secrets_provider"])
            check_type(argname="argument kubelet_identity", value=kubelet_identity, expected_type=type_hints["kubelet_identity"])
            check_type(argname="argument kubernetes_version", value=kubernetes_version, expected_type=type_hints["kubernetes_version"])
            check_type(argname="argument linux_profile", value=linux_profile, expected_type=type_hints["linux_profile"])
            check_type(argname="argument local_account_disabled", value=local_account_disabled, expected_type=type_hints["local_account_disabled"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument microsoft_defender", value=microsoft_defender, expected_type=type_hints["microsoft_defender"])
            check_type(argname="argument monitor_metrics", value=monitor_metrics, expected_type=type_hints["monitor_metrics"])
            check_type(argname="argument network_profile", value=network_profile, expected_type=type_hints["network_profile"])
            check_type(argname="argument node_resource_group", value=node_resource_group, expected_type=type_hints["node_resource_group"])
            check_type(argname="argument oidc_issuer_enabled", value=oidc_issuer_enabled, expected_type=type_hints["oidc_issuer_enabled"])
            check_type(argname="argument oms_agent", value=oms_agent, expected_type=type_hints["oms_agent"])
            check_type(argname="argument open_service_mesh_enabled", value=open_service_mesh_enabled, expected_type=type_hints["open_service_mesh_enabled"])
            check_type(argname="argument private_cluster_enabled", value=private_cluster_enabled, expected_type=type_hints["private_cluster_enabled"])
            check_type(argname="argument private_cluster_public_fqdn_enabled", value=private_cluster_public_fqdn_enabled, expected_type=type_hints["private_cluster_public_fqdn_enabled"])
            check_type(argname="argument private_dns_zone_id", value=private_dns_zone_id, expected_type=type_hints["private_dns_zone_id"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument role_based_access_control_enabled", value=role_based_access_control_enabled, expected_type=type_hints["role_based_access_control_enabled"])
            check_type(argname="argument run_command_enabled", value=run_command_enabled, expected_type=type_hints["run_command_enabled"])
            check_type(argname="argument service_principal", value=service_principal, expected_type=type_hints["service_principal"])
            check_type(argname="argument sku_tier", value=sku_tier, expected_type=type_hints["sku_tier"])
            check_type(argname="argument storage_profile", value=storage_profile, expected_type=type_hints["storage_profile"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument web_app_routing", value=web_app_routing, expected_type=type_hints["web_app_routing"])
            check_type(argname="argument windows_profile", value=windows_profile, expected_type=type_hints["windows_profile"])
            check_type(argname="argument workload_autoscaler_profile", value=workload_autoscaler_profile, expected_type=type_hints["workload_autoscaler_profile"])
            check_type(argname="argument workload_identity_enabled", value=workload_identity_enabled, expected_type=type_hints["workload_identity_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_node_pool": default_node_pool,
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
        if aci_connector_linux is not None:
            self._values["aci_connector_linux"] = aci_connector_linux
        if api_server_authorized_ip_ranges is not None:
            self._values["api_server_authorized_ip_ranges"] = api_server_authorized_ip_ranges
        if automatic_channel_upgrade is not None:
            self._values["automatic_channel_upgrade"] = automatic_channel_upgrade
        if auto_scaler_profile is not None:
            self._values["auto_scaler_profile"] = auto_scaler_profile
        if azure_active_directory_role_based_access_control is not None:
            self._values["azure_active_directory_role_based_access_control"] = azure_active_directory_role_based_access_control
        if azure_policy_enabled is not None:
            self._values["azure_policy_enabled"] = azure_policy_enabled
        if disk_encryption_set_id is not None:
            self._values["disk_encryption_set_id"] = disk_encryption_set_id
        if dns_prefix is not None:
            self._values["dns_prefix"] = dns_prefix
        if dns_prefix_private_cluster is not None:
            self._values["dns_prefix_private_cluster"] = dns_prefix_private_cluster
        if edge_zone is not None:
            self._values["edge_zone"] = edge_zone
        if enable_pod_security_policy is not None:
            self._values["enable_pod_security_policy"] = enable_pod_security_policy
        if http_application_routing_enabled is not None:
            self._values["http_application_routing_enabled"] = http_application_routing_enabled
        if http_proxy_config is not None:
            self._values["http_proxy_config"] = http_proxy_config
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if image_cleaner_enabled is not None:
            self._values["image_cleaner_enabled"] = image_cleaner_enabled
        if image_cleaner_interval_hours is not None:
            self._values["image_cleaner_interval_hours"] = image_cleaner_interval_hours
        if ingress_application_gateway is not None:
            self._values["ingress_application_gateway"] = ingress_application_gateway
        if key_vault_secrets_provider is not None:
            self._values["key_vault_secrets_provider"] = key_vault_secrets_provider
        if kubelet_identity is not None:
            self._values["kubelet_identity"] = kubelet_identity
        if kubernetes_version is not None:
            self._values["kubernetes_version"] = kubernetes_version
        if linux_profile is not None:
            self._values["linux_profile"] = linux_profile
        if local_account_disabled is not None:
            self._values["local_account_disabled"] = local_account_disabled
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if microsoft_defender is not None:
            self._values["microsoft_defender"] = microsoft_defender
        if monitor_metrics is not None:
            self._values["monitor_metrics"] = monitor_metrics
        if network_profile is not None:
            self._values["network_profile"] = network_profile
        if node_resource_group is not None:
            self._values["node_resource_group"] = node_resource_group
        if oidc_issuer_enabled is not None:
            self._values["oidc_issuer_enabled"] = oidc_issuer_enabled
        if oms_agent is not None:
            self._values["oms_agent"] = oms_agent
        if open_service_mesh_enabled is not None:
            self._values["open_service_mesh_enabled"] = open_service_mesh_enabled
        if private_cluster_enabled is not None:
            self._values["private_cluster_enabled"] = private_cluster_enabled
        if private_cluster_public_fqdn_enabled is not None:
            self._values["private_cluster_public_fqdn_enabled"] = private_cluster_public_fqdn_enabled
        if private_dns_zone_id is not None:
            self._values["private_dns_zone_id"] = private_dns_zone_id
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if role_based_access_control_enabled is not None:
            self._values["role_based_access_control_enabled"] = role_based_access_control_enabled
        if run_command_enabled is not None:
            self._values["run_command_enabled"] = run_command_enabled
        if service_principal is not None:
            self._values["service_principal"] = service_principal
        if sku_tier is not None:
            self._values["sku_tier"] = sku_tier
        if storage_profile is not None:
            self._values["storage_profile"] = storage_profile
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if web_app_routing is not None:
            self._values["web_app_routing"] = web_app_routing
        if windows_profile is not None:
            self._values["windows_profile"] = windows_profile
        if workload_autoscaler_profile is not None:
            self._values["workload_autoscaler_profile"] = workload_autoscaler_profile
        if workload_identity_enabled is not None:
            self._values["workload_identity_enabled"] = workload_identity_enabled

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
    def default_node_pool(self) -> "KubernetesClusterDefaultNodePool":
        '''default_node_pool block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#default_node_pool KubernetesCluster#default_node_pool}
        '''
        result = self._values.get("default_node_pool")
        assert result is not None, "Required property 'default_node_pool' is missing"
        return typing.cast("KubernetesClusterDefaultNodePool", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#location KubernetesCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#name KubernetesCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#resource_group_name KubernetesCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aci_connector_linux(
        self,
    ) -> typing.Optional[KubernetesClusterAciConnectorLinux]:
        '''aci_connector_linux block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#aci_connector_linux KubernetesCluster#aci_connector_linux}
        '''
        result = self._values.get("aci_connector_linux")
        return typing.cast(typing.Optional[KubernetesClusterAciConnectorLinux], result)

    @builtins.property
    def api_server_authorized_ip_ranges(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#api_server_authorized_ip_ranges KubernetesCluster#api_server_authorized_ip_ranges}.'''
        result = self._values.get("api_server_authorized_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def automatic_channel_upgrade(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#automatic_channel_upgrade KubernetesCluster#automatic_channel_upgrade}.'''
        result = self._values.get("automatic_channel_upgrade")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_scaler_profile(
        self,
    ) -> typing.Optional[KubernetesClusterAutoScalerProfile]:
        '''auto_scaler_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#auto_scaler_profile KubernetesCluster#auto_scaler_profile}
        '''
        result = self._values.get("auto_scaler_profile")
        return typing.cast(typing.Optional[KubernetesClusterAutoScalerProfile], result)

    @builtins.property
    def azure_active_directory_role_based_access_control(
        self,
    ) -> typing.Optional[KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl]:
        '''azure_active_directory_role_based_access_control block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#azure_active_directory_role_based_access_control KubernetesCluster#azure_active_directory_role_based_access_control}
        '''
        result = self._values.get("azure_active_directory_role_based_access_control")
        return typing.cast(typing.Optional[KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl], result)

    @builtins.property
    def azure_policy_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#azure_policy_enabled KubernetesCluster#azure_policy_enabled}.'''
        result = self._values.get("azure_policy_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disk_encryption_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#disk_encryption_set_id KubernetesCluster#disk_encryption_set_id}.'''
        result = self._values.get("disk_encryption_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_prefix KubernetesCluster#dns_prefix}.'''
        result = self._values.get("dns_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_prefix_private_cluster(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_prefix_private_cluster KubernetesCluster#dns_prefix_private_cluster}.'''
        result = self._values.get("dns_prefix_private_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#edge_zone KubernetesCluster#edge_zone}.'''
        result = self._values.get("edge_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_pod_security_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_pod_security_policy KubernetesCluster#enable_pod_security_policy}.'''
        result = self._values.get("enable_pod_security_policy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_application_routing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#http_application_routing_enabled KubernetesCluster#http_application_routing_enabled}.'''
        result = self._values.get("http_application_routing_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_proxy_config(self) -> typing.Optional["KubernetesClusterHttpProxyConfig"]:
        '''http_proxy_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#http_proxy_config KubernetesCluster#http_proxy_config}
        '''
        result = self._values.get("http_proxy_config")
        return typing.cast(typing.Optional["KubernetesClusterHttpProxyConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#id KubernetesCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["KubernetesClusterIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#identity KubernetesCluster#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["KubernetesClusterIdentity"], result)

    @builtins.property
    def image_cleaner_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_cleaner_enabled KubernetesCluster#image_cleaner_enabled}.'''
        result = self._values.get("image_cleaner_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def image_cleaner_interval_hours(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_cleaner_interval_hours KubernetesCluster#image_cleaner_interval_hours}.'''
        result = self._values.get("image_cleaner_interval_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ingress_application_gateway(
        self,
    ) -> typing.Optional["KubernetesClusterIngressApplicationGateway"]:
        '''ingress_application_gateway block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ingress_application_gateway KubernetesCluster#ingress_application_gateway}
        '''
        result = self._values.get("ingress_application_gateway")
        return typing.cast(typing.Optional["KubernetesClusterIngressApplicationGateway"], result)

    @builtins.property
    def key_vault_secrets_provider(
        self,
    ) -> typing.Optional["KubernetesClusterKeyVaultSecretsProvider"]:
        '''key_vault_secrets_provider block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#key_vault_secrets_provider KubernetesCluster#key_vault_secrets_provider}
        '''
        result = self._values.get("key_vault_secrets_provider")
        return typing.cast(typing.Optional["KubernetesClusterKeyVaultSecretsProvider"], result)

    @builtins.property
    def kubelet_identity(self) -> typing.Optional["KubernetesClusterKubeletIdentity"]:
        '''kubelet_identity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubelet_identity KubernetesCluster#kubelet_identity}
        '''
        result = self._values.get("kubelet_identity")
        return typing.cast(typing.Optional["KubernetesClusterKubeletIdentity"], result)

    @builtins.property
    def kubernetes_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubernetes_version KubernetesCluster#kubernetes_version}.'''
        result = self._values.get("kubernetes_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def linux_profile(self) -> typing.Optional["KubernetesClusterLinuxProfile"]:
        '''linux_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#linux_profile KubernetesCluster#linux_profile}
        '''
        result = self._values.get("linux_profile")
        return typing.cast(typing.Optional["KubernetesClusterLinuxProfile"], result)

    @builtins.property
    def local_account_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#local_account_disabled KubernetesCluster#local_account_disabled}.'''
        result = self._values.get("local_account_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["KubernetesClusterMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#maintenance_window KubernetesCluster#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["KubernetesClusterMaintenanceWindow"], result)

    @builtins.property
    def microsoft_defender(
        self,
    ) -> typing.Optional["KubernetesClusterMicrosoftDefender"]:
        '''microsoft_defender block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#microsoft_defender KubernetesCluster#microsoft_defender}
        '''
        result = self._values.get("microsoft_defender")
        return typing.cast(typing.Optional["KubernetesClusterMicrosoftDefender"], result)

    @builtins.property
    def monitor_metrics(self) -> typing.Optional["KubernetesClusterMonitorMetrics"]:
        '''monitor_metrics block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#monitor_metrics KubernetesCluster#monitor_metrics}
        '''
        result = self._values.get("monitor_metrics")
        return typing.cast(typing.Optional["KubernetesClusterMonitorMetrics"], result)

    @builtins.property
    def network_profile(self) -> typing.Optional["KubernetesClusterNetworkProfile"]:
        '''network_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_profile KubernetesCluster#network_profile}
        '''
        result = self._values.get("network_profile")
        return typing.cast(typing.Optional["KubernetesClusterNetworkProfile"], result)

    @builtins.property
    def node_resource_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_resource_group KubernetesCluster#node_resource_group}.'''
        result = self._values.get("node_resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc_issuer_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#oidc_issuer_enabled KubernetesCluster#oidc_issuer_enabled}.'''
        result = self._values.get("oidc_issuer_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def oms_agent(self) -> typing.Optional["KubernetesClusterOmsAgent"]:
        '''oms_agent block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#oms_agent KubernetesCluster#oms_agent}
        '''
        result = self._values.get("oms_agent")
        return typing.cast(typing.Optional["KubernetesClusterOmsAgent"], result)

    @builtins.property
    def open_service_mesh_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#open_service_mesh_enabled KubernetesCluster#open_service_mesh_enabled}.'''
        result = self._values.get("open_service_mesh_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_cluster_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#private_cluster_enabled KubernetesCluster#private_cluster_enabled}.'''
        result = self._values.get("private_cluster_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_cluster_public_fqdn_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#private_cluster_public_fqdn_enabled KubernetesCluster#private_cluster_public_fqdn_enabled}.'''
        result = self._values.get("private_cluster_public_fqdn_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_dns_zone_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#private_dns_zone_id KubernetesCluster#private_dns_zone_id}.'''
        result = self._values.get("private_dns_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#public_network_access_enabled KubernetesCluster#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def role_based_access_control_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#role_based_access_control_enabled KubernetesCluster#role_based_access_control_enabled}.'''
        result = self._values.get("role_based_access_control_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_command_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#run_command_enabled KubernetesCluster#run_command_enabled}.'''
        result = self._values.get("run_command_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def service_principal(self) -> typing.Optional["KubernetesClusterServicePrincipal"]:
        '''service_principal block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#service_principal KubernetesCluster#service_principal}
        '''
        result = self._values.get("service_principal")
        return typing.cast(typing.Optional["KubernetesClusterServicePrincipal"], result)

    @builtins.property
    def sku_tier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#sku_tier KubernetesCluster#sku_tier}.'''
        result = self._values.get("sku_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_profile(self) -> typing.Optional["KubernetesClusterStorageProfile"]:
        '''storage_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#storage_profile KubernetesCluster#storage_profile}
        '''
        result = self._values.get("storage_profile")
        return typing.cast(typing.Optional["KubernetesClusterStorageProfile"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#tags KubernetesCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KubernetesClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#timeouts KubernetesCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KubernetesClusterTimeouts"], result)

    @builtins.property
    def web_app_routing(self) -> typing.Optional["KubernetesClusterWebAppRouting"]:
        '''web_app_routing block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#web_app_routing KubernetesCluster#web_app_routing}
        '''
        result = self._values.get("web_app_routing")
        return typing.cast(typing.Optional["KubernetesClusterWebAppRouting"], result)

    @builtins.property
    def windows_profile(self) -> typing.Optional["KubernetesClusterWindowsProfile"]:
        '''windows_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#windows_profile KubernetesCluster#windows_profile}
        '''
        result = self._values.get("windows_profile")
        return typing.cast(typing.Optional["KubernetesClusterWindowsProfile"], result)

    @builtins.property
    def workload_autoscaler_profile(
        self,
    ) -> typing.Optional["KubernetesClusterWorkloadAutoscalerProfile"]:
        '''workload_autoscaler_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#workload_autoscaler_profile KubernetesCluster#workload_autoscaler_profile}
        '''
        result = self._values.get("workload_autoscaler_profile")
        return typing.cast(typing.Optional["KubernetesClusterWorkloadAutoscalerProfile"], result)

    @builtins.property
    def workload_identity_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#workload_identity_enabled KubernetesCluster#workload_identity_enabled}.'''
        result = self._values.get("workload_identity_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterDefaultNodePool",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "vm_size": "vmSize",
        "capacity_reservation_group_id": "capacityReservationGroupId",
        "custom_ca_trust_enabled": "customCaTrustEnabled",
        "enable_auto_scaling": "enableAutoScaling",
        "enable_host_encryption": "enableHostEncryption",
        "enable_node_public_ip": "enableNodePublicIp",
        "fips_enabled": "fipsEnabled",
        "host_group_id": "hostGroupId",
        "kubelet_config": "kubeletConfig",
        "kubelet_disk_type": "kubeletDiskType",
        "linux_os_config": "linuxOsConfig",
        "max_count": "maxCount",
        "max_pods": "maxPods",
        "message_of_the_day": "messageOfTheDay",
        "min_count": "minCount",
        "node_count": "nodeCount",
        "node_labels": "nodeLabels",
        "node_public_ip_prefix_id": "nodePublicIpPrefixId",
        "node_taints": "nodeTaints",
        "only_critical_addons_enabled": "onlyCriticalAddonsEnabled",
        "orchestrator_version": "orchestratorVersion",
        "os_disk_size_gb": "osDiskSizeGb",
        "os_disk_type": "osDiskType",
        "os_sku": "osSku",
        "pod_subnet_id": "podSubnetId",
        "proximity_placement_group_id": "proximityPlacementGroupId",
        "scale_down_mode": "scaleDownMode",
        "tags": "tags",
        "type": "type",
        "ultra_ssd_enabled": "ultraSsdEnabled",
        "upgrade_settings": "upgradeSettings",
        "vnet_subnet_id": "vnetSubnetId",
        "workload_runtime": "workloadRuntime",
        "zones": "zones",
    },
)
class KubernetesClusterDefaultNodePool:
    def __init__(
        self,
        *,
        name: builtins.str,
        vm_size: builtins.str,
        capacity_reservation_group_id: typing.Optional[builtins.str] = None,
        custom_ca_trust_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_auto_scaling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_host_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_node_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_group_id: typing.Optional[builtins.str] = None,
        kubelet_config: typing.Optional[typing.Union["KubernetesClusterDefaultNodePoolKubeletConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        kubelet_disk_type: typing.Optional[builtins.str] = None,
        linux_os_config: typing.Optional[typing.Union["KubernetesClusterDefaultNodePoolLinuxOsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_count: typing.Optional[jsii.Number] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        message_of_the_day: typing.Optional[builtins.str] = None,
        min_count: typing.Optional[jsii.Number] = None,
        node_count: typing.Optional[jsii.Number] = None,
        node_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_public_ip_prefix_id: typing.Optional[builtins.str] = None,
        node_taints: typing.Optional[typing.Sequence[builtins.str]] = None,
        only_critical_addons_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        orchestrator_version: typing.Optional[builtins.str] = None,
        os_disk_size_gb: typing.Optional[jsii.Number] = None,
        os_disk_type: typing.Optional[builtins.str] = None,
        os_sku: typing.Optional[builtins.str] = None,
        pod_subnet_id: typing.Optional[builtins.str] = None,
        proximity_placement_group_id: typing.Optional[builtins.str] = None,
        scale_down_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
        ultra_ssd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        upgrade_settings: typing.Optional[typing.Union["KubernetesClusterDefaultNodePoolUpgradeSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        vnet_subnet_id: typing.Optional[builtins.str] = None,
        workload_runtime: typing.Optional[builtins.str] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#name KubernetesCluster#name}.
        :param vm_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_size KubernetesCluster#vm_size}.
        :param capacity_reservation_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#capacity_reservation_group_id KubernetesCluster#capacity_reservation_group_id}.
        :param custom_ca_trust_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#custom_ca_trust_enabled KubernetesCluster#custom_ca_trust_enabled}.
        :param enable_auto_scaling: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_auto_scaling KubernetesCluster#enable_auto_scaling}.
        :param enable_host_encryption: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_host_encryption KubernetesCluster#enable_host_encryption}.
        :param enable_node_public_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_node_public_ip KubernetesCluster#enable_node_public_ip}.
        :param fips_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fips_enabled KubernetesCluster#fips_enabled}.
        :param host_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#host_group_id KubernetesCluster#host_group_id}.
        :param kubelet_config: kubelet_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubelet_config KubernetesCluster#kubelet_config}
        :param kubelet_disk_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubelet_disk_type KubernetesCluster#kubelet_disk_type}.
        :param linux_os_config: linux_os_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#linux_os_config KubernetesCluster#linux_os_config}
        :param max_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_count KubernetesCluster#max_count}.
        :param max_pods: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_pods KubernetesCluster#max_pods}.
        :param message_of_the_day: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#message_of_the_day KubernetesCluster#message_of_the_day}.
        :param min_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#min_count KubernetesCluster#min_count}.
        :param node_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_count KubernetesCluster#node_count}.
        :param node_labels: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_labels KubernetesCluster#node_labels}.
        :param node_public_ip_prefix_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_public_ip_prefix_id KubernetesCluster#node_public_ip_prefix_id}.
        :param node_taints: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_taints KubernetesCluster#node_taints}.
        :param only_critical_addons_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#only_critical_addons_enabled KubernetesCluster#only_critical_addons_enabled}.
        :param orchestrator_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#orchestrator_version KubernetesCluster#orchestrator_version}.
        :param os_disk_size_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#os_disk_size_gb KubernetesCluster#os_disk_size_gb}.
        :param os_disk_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#os_disk_type KubernetesCluster#os_disk_type}.
        :param os_sku: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#os_sku KubernetesCluster#os_sku}.
        :param pod_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_subnet_id KubernetesCluster#pod_subnet_id}.
        :param proximity_placement_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#proximity_placement_group_id KubernetesCluster#proximity_placement_group_id}.
        :param scale_down_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_mode KubernetesCluster#scale_down_mode}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#tags KubernetesCluster#tags}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#type KubernetesCluster#type}.
        :param ultra_ssd_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ultra_ssd_enabled KubernetesCluster#ultra_ssd_enabled}.
        :param upgrade_settings: upgrade_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#upgrade_settings KubernetesCluster#upgrade_settings}
        :param vnet_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vnet_subnet_id KubernetesCluster#vnet_subnet_id}.
        :param workload_runtime: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#workload_runtime KubernetesCluster#workload_runtime}.
        :param zones: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#zones KubernetesCluster#zones}.
        '''
        if isinstance(kubelet_config, dict):
            kubelet_config = KubernetesClusterDefaultNodePoolKubeletConfig(**kubelet_config)
        if isinstance(linux_os_config, dict):
            linux_os_config = KubernetesClusterDefaultNodePoolLinuxOsConfig(**linux_os_config)
        if isinstance(upgrade_settings, dict):
            upgrade_settings = KubernetesClusterDefaultNodePoolUpgradeSettings(**upgrade_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d248b32efaf2c83899cf2b412ac01b6ccc4446edbca3b4294749a26d70073c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
            check_type(argname="argument capacity_reservation_group_id", value=capacity_reservation_group_id, expected_type=type_hints["capacity_reservation_group_id"])
            check_type(argname="argument custom_ca_trust_enabled", value=custom_ca_trust_enabled, expected_type=type_hints["custom_ca_trust_enabled"])
            check_type(argname="argument enable_auto_scaling", value=enable_auto_scaling, expected_type=type_hints["enable_auto_scaling"])
            check_type(argname="argument enable_host_encryption", value=enable_host_encryption, expected_type=type_hints["enable_host_encryption"])
            check_type(argname="argument enable_node_public_ip", value=enable_node_public_ip, expected_type=type_hints["enable_node_public_ip"])
            check_type(argname="argument fips_enabled", value=fips_enabled, expected_type=type_hints["fips_enabled"])
            check_type(argname="argument host_group_id", value=host_group_id, expected_type=type_hints["host_group_id"])
            check_type(argname="argument kubelet_config", value=kubelet_config, expected_type=type_hints["kubelet_config"])
            check_type(argname="argument kubelet_disk_type", value=kubelet_disk_type, expected_type=type_hints["kubelet_disk_type"])
            check_type(argname="argument linux_os_config", value=linux_os_config, expected_type=type_hints["linux_os_config"])
            check_type(argname="argument max_count", value=max_count, expected_type=type_hints["max_count"])
            check_type(argname="argument max_pods", value=max_pods, expected_type=type_hints["max_pods"])
            check_type(argname="argument message_of_the_day", value=message_of_the_day, expected_type=type_hints["message_of_the_day"])
            check_type(argname="argument min_count", value=min_count, expected_type=type_hints["min_count"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument node_labels", value=node_labels, expected_type=type_hints["node_labels"])
            check_type(argname="argument node_public_ip_prefix_id", value=node_public_ip_prefix_id, expected_type=type_hints["node_public_ip_prefix_id"])
            check_type(argname="argument node_taints", value=node_taints, expected_type=type_hints["node_taints"])
            check_type(argname="argument only_critical_addons_enabled", value=only_critical_addons_enabled, expected_type=type_hints["only_critical_addons_enabled"])
            check_type(argname="argument orchestrator_version", value=orchestrator_version, expected_type=type_hints["orchestrator_version"])
            check_type(argname="argument os_disk_size_gb", value=os_disk_size_gb, expected_type=type_hints["os_disk_size_gb"])
            check_type(argname="argument os_disk_type", value=os_disk_type, expected_type=type_hints["os_disk_type"])
            check_type(argname="argument os_sku", value=os_sku, expected_type=type_hints["os_sku"])
            check_type(argname="argument pod_subnet_id", value=pod_subnet_id, expected_type=type_hints["pod_subnet_id"])
            check_type(argname="argument proximity_placement_group_id", value=proximity_placement_group_id, expected_type=type_hints["proximity_placement_group_id"])
            check_type(argname="argument scale_down_mode", value=scale_down_mode, expected_type=type_hints["scale_down_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument ultra_ssd_enabled", value=ultra_ssd_enabled, expected_type=type_hints["ultra_ssd_enabled"])
            check_type(argname="argument upgrade_settings", value=upgrade_settings, expected_type=type_hints["upgrade_settings"])
            check_type(argname="argument vnet_subnet_id", value=vnet_subnet_id, expected_type=type_hints["vnet_subnet_id"])
            check_type(argname="argument workload_runtime", value=workload_runtime, expected_type=type_hints["workload_runtime"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "vm_size": vm_size,
        }
        if capacity_reservation_group_id is not None:
            self._values["capacity_reservation_group_id"] = capacity_reservation_group_id
        if custom_ca_trust_enabled is not None:
            self._values["custom_ca_trust_enabled"] = custom_ca_trust_enabled
        if enable_auto_scaling is not None:
            self._values["enable_auto_scaling"] = enable_auto_scaling
        if enable_host_encryption is not None:
            self._values["enable_host_encryption"] = enable_host_encryption
        if enable_node_public_ip is not None:
            self._values["enable_node_public_ip"] = enable_node_public_ip
        if fips_enabled is not None:
            self._values["fips_enabled"] = fips_enabled
        if host_group_id is not None:
            self._values["host_group_id"] = host_group_id
        if kubelet_config is not None:
            self._values["kubelet_config"] = kubelet_config
        if kubelet_disk_type is not None:
            self._values["kubelet_disk_type"] = kubelet_disk_type
        if linux_os_config is not None:
            self._values["linux_os_config"] = linux_os_config
        if max_count is not None:
            self._values["max_count"] = max_count
        if max_pods is not None:
            self._values["max_pods"] = max_pods
        if message_of_the_day is not None:
            self._values["message_of_the_day"] = message_of_the_day
        if min_count is not None:
            self._values["min_count"] = min_count
        if node_count is not None:
            self._values["node_count"] = node_count
        if node_labels is not None:
            self._values["node_labels"] = node_labels
        if node_public_ip_prefix_id is not None:
            self._values["node_public_ip_prefix_id"] = node_public_ip_prefix_id
        if node_taints is not None:
            self._values["node_taints"] = node_taints
        if only_critical_addons_enabled is not None:
            self._values["only_critical_addons_enabled"] = only_critical_addons_enabled
        if orchestrator_version is not None:
            self._values["orchestrator_version"] = orchestrator_version
        if os_disk_size_gb is not None:
            self._values["os_disk_size_gb"] = os_disk_size_gb
        if os_disk_type is not None:
            self._values["os_disk_type"] = os_disk_type
        if os_sku is not None:
            self._values["os_sku"] = os_sku
        if pod_subnet_id is not None:
            self._values["pod_subnet_id"] = pod_subnet_id
        if proximity_placement_group_id is not None:
            self._values["proximity_placement_group_id"] = proximity_placement_group_id
        if scale_down_mode is not None:
            self._values["scale_down_mode"] = scale_down_mode
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if ultra_ssd_enabled is not None:
            self._values["ultra_ssd_enabled"] = ultra_ssd_enabled
        if upgrade_settings is not None:
            self._values["upgrade_settings"] = upgrade_settings
        if vnet_subnet_id is not None:
            self._values["vnet_subnet_id"] = vnet_subnet_id
        if workload_runtime is not None:
            self._values["workload_runtime"] = workload_runtime
        if zones is not None:
            self._values["zones"] = zones

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#name KubernetesCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vm_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_size KubernetesCluster#vm_size}.'''
        result = self._values.get("vm_size")
        assert result is not None, "Required property 'vm_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity_reservation_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#capacity_reservation_group_id KubernetesCluster#capacity_reservation_group_id}.'''
        result = self._values.get("capacity_reservation_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_ca_trust_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#custom_ca_trust_enabled KubernetesCluster#custom_ca_trust_enabled}.'''
        result = self._values.get("custom_ca_trust_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_auto_scaling(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_auto_scaling KubernetesCluster#enable_auto_scaling}.'''
        result = self._values.get("enable_auto_scaling")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_host_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_host_encryption KubernetesCluster#enable_host_encryption}.'''
        result = self._values.get("enable_host_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_node_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#enable_node_public_ip KubernetesCluster#enable_node_public_ip}.'''
        result = self._values.get("enable_node_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fips_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fips_enabled KubernetesCluster#fips_enabled}.'''
        result = self._values.get("fips_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#host_group_id KubernetesCluster#host_group_id}.'''
        result = self._values.get("host_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubelet_config(
        self,
    ) -> typing.Optional["KubernetesClusterDefaultNodePoolKubeletConfig"]:
        '''kubelet_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubelet_config KubernetesCluster#kubelet_config}
        '''
        result = self._values.get("kubelet_config")
        return typing.cast(typing.Optional["KubernetesClusterDefaultNodePoolKubeletConfig"], result)

    @builtins.property
    def kubelet_disk_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kubelet_disk_type KubernetesCluster#kubelet_disk_type}.'''
        result = self._values.get("kubelet_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def linux_os_config(
        self,
    ) -> typing.Optional["KubernetesClusterDefaultNodePoolLinuxOsConfig"]:
        '''linux_os_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#linux_os_config KubernetesCluster#linux_os_config}
        '''
        result = self._values.get("linux_os_config")
        return typing.cast(typing.Optional["KubernetesClusterDefaultNodePoolLinuxOsConfig"], result)

    @builtins.property
    def max_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_count KubernetesCluster#max_count}.'''
        result = self._values.get("max_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pods(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_pods KubernetesCluster#max_pods}.'''
        result = self._values.get("max_pods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def message_of_the_day(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#message_of_the_day KubernetesCluster#message_of_the_day}.'''
        result = self._values.get("message_of_the_day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#min_count KubernetesCluster#min_count}.'''
        result = self._values.get("min_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_count KubernetesCluster#node_count}.'''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_labels KubernetesCluster#node_labels}.'''
        result = self._values.get("node_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_public_ip_prefix_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_public_ip_prefix_id KubernetesCluster#node_public_ip_prefix_id}.'''
        result = self._values.get("node_public_ip_prefix_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_taints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#node_taints KubernetesCluster#node_taints}.'''
        result = self._values.get("node_taints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def only_critical_addons_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#only_critical_addons_enabled KubernetesCluster#only_critical_addons_enabled}.'''
        result = self._values.get("only_critical_addons_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def orchestrator_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#orchestrator_version KubernetesCluster#orchestrator_version}.'''
        result = self._values.get("orchestrator_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#os_disk_size_gb KubernetesCluster#os_disk_size_gb}.'''
        result = self._values.get("os_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def os_disk_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#os_disk_type KubernetesCluster#os_disk_type}.'''
        result = self._values.get("os_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#os_sku KubernetesCluster#os_sku}.'''
        result = self._values.get("os_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_subnet_id KubernetesCluster#pod_subnet_id}.'''
        result = self._values.get("pod_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proximity_placement_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#proximity_placement_group_id KubernetesCluster#proximity_placement_group_id}.'''
        result = self._values.get("proximity_placement_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#scale_down_mode KubernetesCluster#scale_down_mode}.'''
        result = self._values.get("scale_down_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#tags KubernetesCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#type KubernetesCluster#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ultra_ssd_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ultra_ssd_enabled KubernetesCluster#ultra_ssd_enabled}.'''
        result = self._values.get("ultra_ssd_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def upgrade_settings(
        self,
    ) -> typing.Optional["KubernetesClusterDefaultNodePoolUpgradeSettings"]:
        '''upgrade_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#upgrade_settings KubernetesCluster#upgrade_settings}
        '''
        result = self._values.get("upgrade_settings")
        return typing.cast(typing.Optional["KubernetesClusterDefaultNodePoolUpgradeSettings"], result)

    @builtins.property
    def vnet_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vnet_subnet_id KubernetesCluster#vnet_subnet_id}.'''
        result = self._values.get("vnet_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workload_runtime(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#workload_runtime KubernetesCluster#workload_runtime}.'''
        result = self._values.get("workload_runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#zones KubernetesCluster#zones}.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterDefaultNodePool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterDefaultNodePoolKubeletConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_unsafe_sysctls": "allowedUnsafeSysctls",
        "container_log_max_line": "containerLogMaxLine",
        "container_log_max_size_mb": "containerLogMaxSizeMb",
        "cpu_cfs_quota_enabled": "cpuCfsQuotaEnabled",
        "cpu_cfs_quota_period": "cpuCfsQuotaPeriod",
        "cpu_manager_policy": "cpuManagerPolicy",
        "image_gc_high_threshold": "imageGcHighThreshold",
        "image_gc_low_threshold": "imageGcLowThreshold",
        "pod_max_pid": "podMaxPid",
        "topology_manager_policy": "topologyManagerPolicy",
    },
)
class KubernetesClusterDefaultNodePoolKubeletConfig:
    def __init__(
        self,
        *,
        allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_log_max_line: typing.Optional[jsii.Number] = None,
        container_log_max_size_mb: typing.Optional[jsii.Number] = None,
        cpu_cfs_quota_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
        cpu_manager_policy: typing.Optional[builtins.str] = None,
        image_gc_high_threshold: typing.Optional[jsii.Number] = None,
        image_gc_low_threshold: typing.Optional[jsii.Number] = None,
        pod_max_pid: typing.Optional[jsii.Number] = None,
        topology_manager_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_unsafe_sysctls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#allowed_unsafe_sysctls KubernetesCluster#allowed_unsafe_sysctls}.
        :param container_log_max_line: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#container_log_max_line KubernetesCluster#container_log_max_line}.
        :param container_log_max_size_mb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#container_log_max_size_mb KubernetesCluster#container_log_max_size_mb}.
        :param cpu_cfs_quota_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#cpu_cfs_quota_enabled KubernetesCluster#cpu_cfs_quota_enabled}.
        :param cpu_cfs_quota_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#cpu_cfs_quota_period KubernetesCluster#cpu_cfs_quota_period}.
        :param cpu_manager_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#cpu_manager_policy KubernetesCluster#cpu_manager_policy}.
        :param image_gc_high_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_gc_high_threshold KubernetesCluster#image_gc_high_threshold}.
        :param image_gc_low_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_gc_low_threshold KubernetesCluster#image_gc_low_threshold}.
        :param pod_max_pid: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_max_pid KubernetesCluster#pod_max_pid}.
        :param topology_manager_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#topology_manager_policy KubernetesCluster#topology_manager_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b35ae5283ebb4881dfe0c3bbeb03011e24335d939ae4594fed70911b5a4c73e5)
            check_type(argname="argument allowed_unsafe_sysctls", value=allowed_unsafe_sysctls, expected_type=type_hints["allowed_unsafe_sysctls"])
            check_type(argname="argument container_log_max_line", value=container_log_max_line, expected_type=type_hints["container_log_max_line"])
            check_type(argname="argument container_log_max_size_mb", value=container_log_max_size_mb, expected_type=type_hints["container_log_max_size_mb"])
            check_type(argname="argument cpu_cfs_quota_enabled", value=cpu_cfs_quota_enabled, expected_type=type_hints["cpu_cfs_quota_enabled"])
            check_type(argname="argument cpu_cfs_quota_period", value=cpu_cfs_quota_period, expected_type=type_hints["cpu_cfs_quota_period"])
            check_type(argname="argument cpu_manager_policy", value=cpu_manager_policy, expected_type=type_hints["cpu_manager_policy"])
            check_type(argname="argument image_gc_high_threshold", value=image_gc_high_threshold, expected_type=type_hints["image_gc_high_threshold"])
            check_type(argname="argument image_gc_low_threshold", value=image_gc_low_threshold, expected_type=type_hints["image_gc_low_threshold"])
            check_type(argname="argument pod_max_pid", value=pod_max_pid, expected_type=type_hints["pod_max_pid"])
            check_type(argname="argument topology_manager_policy", value=topology_manager_policy, expected_type=type_hints["topology_manager_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_unsafe_sysctls is not None:
            self._values["allowed_unsafe_sysctls"] = allowed_unsafe_sysctls
        if container_log_max_line is not None:
            self._values["container_log_max_line"] = container_log_max_line
        if container_log_max_size_mb is not None:
            self._values["container_log_max_size_mb"] = container_log_max_size_mb
        if cpu_cfs_quota_enabled is not None:
            self._values["cpu_cfs_quota_enabled"] = cpu_cfs_quota_enabled
        if cpu_cfs_quota_period is not None:
            self._values["cpu_cfs_quota_period"] = cpu_cfs_quota_period
        if cpu_manager_policy is not None:
            self._values["cpu_manager_policy"] = cpu_manager_policy
        if image_gc_high_threshold is not None:
            self._values["image_gc_high_threshold"] = image_gc_high_threshold
        if image_gc_low_threshold is not None:
            self._values["image_gc_low_threshold"] = image_gc_low_threshold
        if pod_max_pid is not None:
            self._values["pod_max_pid"] = pod_max_pid
        if topology_manager_policy is not None:
            self._values["topology_manager_policy"] = topology_manager_policy

    @builtins.property
    def allowed_unsafe_sysctls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#allowed_unsafe_sysctls KubernetesCluster#allowed_unsafe_sysctls}.'''
        result = self._values.get("allowed_unsafe_sysctls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def container_log_max_line(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#container_log_max_line KubernetesCluster#container_log_max_line}.'''
        result = self._values.get("container_log_max_line")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def container_log_max_size_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#container_log_max_size_mb KubernetesCluster#container_log_max_size_mb}.'''
        result = self._values.get("container_log_max_size_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_cfs_quota_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#cpu_cfs_quota_enabled KubernetesCluster#cpu_cfs_quota_enabled}.'''
        result = self._values.get("cpu_cfs_quota_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cpu_cfs_quota_period(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#cpu_cfs_quota_period KubernetesCluster#cpu_cfs_quota_period}.'''
        result = self._values.get("cpu_cfs_quota_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_manager_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#cpu_manager_policy KubernetesCluster#cpu_manager_policy}.'''
        result = self._values.get("cpu_manager_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_gc_high_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_gc_high_threshold KubernetesCluster#image_gc_high_threshold}.'''
        result = self._values.get("image_gc_high_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def image_gc_low_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_gc_low_threshold KubernetesCluster#image_gc_low_threshold}.'''
        result = self._values.get("image_gc_low_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pod_max_pid(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_max_pid KubernetesCluster#pod_max_pid}.'''
        result = self._values.get("pod_max_pid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def topology_manager_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#topology_manager_policy KubernetesCluster#topology_manager_policy}.'''
        result = self._values.get("topology_manager_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterDefaultNodePoolKubeletConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterDefaultNodePoolKubeletConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterDefaultNodePoolKubeletConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76d23d7f1b8a96888f61ef32252f843b356e991c9be48fc32eea0bd5ff17b1b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedUnsafeSysctls")
    def reset_allowed_unsafe_sysctls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedUnsafeSysctls", []))

    @jsii.member(jsii_name="resetContainerLogMaxLine")
    def reset_container_log_max_line(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerLogMaxLine", []))

    @jsii.member(jsii_name="resetContainerLogMaxSizeMb")
    def reset_container_log_max_size_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerLogMaxSizeMb", []))

    @jsii.member(jsii_name="resetCpuCfsQuotaEnabled")
    def reset_cpu_cfs_quota_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCfsQuotaEnabled", []))

    @jsii.member(jsii_name="resetCpuCfsQuotaPeriod")
    def reset_cpu_cfs_quota_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCfsQuotaPeriod", []))

    @jsii.member(jsii_name="resetCpuManagerPolicy")
    def reset_cpu_manager_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuManagerPolicy", []))

    @jsii.member(jsii_name="resetImageGcHighThreshold")
    def reset_image_gc_high_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageGcHighThreshold", []))

    @jsii.member(jsii_name="resetImageGcLowThreshold")
    def reset_image_gc_low_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageGcLowThreshold", []))

    @jsii.member(jsii_name="resetPodMaxPid")
    def reset_pod_max_pid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodMaxPid", []))

    @jsii.member(jsii_name="resetTopologyManagerPolicy")
    def reset_topology_manager_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopologyManagerPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="allowedUnsafeSysctlsInput")
    def allowed_unsafe_sysctls_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedUnsafeSysctlsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxLineInput")
    def container_log_max_line_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerLogMaxLineInput"))

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxSizeMbInput")
    def container_log_max_size_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerLogMaxSizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaEnabledInput")
    def cpu_cfs_quota_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cpuCfsQuotaEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaPeriodInput")
    def cpu_cfs_quota_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuCfsQuotaPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuManagerPolicyInput")
    def cpu_manager_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuManagerPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="imageGcHighThresholdInput")
    def image_gc_high_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageGcHighThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="imageGcLowThresholdInput")
    def image_gc_low_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageGcLowThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="podMaxPidInput")
    def pod_max_pid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "podMaxPidInput"))

    @builtins.property
    @jsii.member(jsii_name="topologyManagerPolicyInput")
    def topology_manager_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topologyManagerPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedUnsafeSysctls")
    def allowed_unsafe_sysctls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedUnsafeSysctls"))

    @allowed_unsafe_sysctls.setter
    def allowed_unsafe_sysctls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0db9bb5b927a4f98565eba754bf5f7f760f0c0e42c4774c8a09617cf31f599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedUnsafeSysctls", value)

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxLine")
    def container_log_max_line(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerLogMaxLine"))

    @container_log_max_line.setter
    def container_log_max_line(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55637f8affe18fdd4da2913f89c0bb41da7faa05ad692f27c7a73c497085689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerLogMaxLine", value)

    @builtins.property
    @jsii.member(jsii_name="containerLogMaxSizeMb")
    def container_log_max_size_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerLogMaxSizeMb"))

    @container_log_max_size_mb.setter
    def container_log_max_size_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d84f75340b829577ec847bb2b710efd21db508f0f9ea1b9a10e781e59a51975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerLogMaxSizeMb", value)

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaEnabled")
    def cpu_cfs_quota_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cpuCfsQuotaEnabled"))

    @cpu_cfs_quota_enabled.setter
    def cpu_cfs_quota_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12dfdc57a5cd9bcb63adfbbcdb3fe466eb206f7f4b97ee93e9d7d68dbc2b0a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuotaEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cpuCfsQuotaPeriod")
    def cpu_cfs_quota_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuCfsQuotaPeriod"))

    @cpu_cfs_quota_period.setter
    def cpu_cfs_quota_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b11e95f2c6b483b1bf1fd1c23959471577de0a31e40142669bdc9899e75a00b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCfsQuotaPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="cpuManagerPolicy")
    def cpu_manager_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuManagerPolicy"))

    @cpu_manager_policy.setter
    def cpu_manager_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2519818b51889459629e8f207e26cf07bef60baca07e87a4f8efc50246d46f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuManagerPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="imageGcHighThreshold")
    def image_gc_high_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageGcHighThreshold"))

    @image_gc_high_threshold.setter
    def image_gc_high_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db345a5ac0a3b0f18b32cad5dcd3baa2b5a6ce48df4d58919768bb4d7d5e38a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageGcHighThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="imageGcLowThreshold")
    def image_gc_low_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageGcLowThreshold"))

    @image_gc_low_threshold.setter
    def image_gc_low_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8b3525b5360583e80fdf23c945180c6fb0a2a237510baff86b4b0a416aff08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageGcLowThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="podMaxPid")
    def pod_max_pid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "podMaxPid"))

    @pod_max_pid.setter
    def pod_max_pid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d625cc17badb48c84ef7b6d93c869e06e2d1d9764575d1418012ba81862c2c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podMaxPid", value)

    @builtins.property
    @jsii.member(jsii_name="topologyManagerPolicy")
    def topology_manager_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topologyManagerPolicy"))

    @topology_manager_policy.setter
    def topology_manager_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7414b340296f0737b288157465f88512a9d45cb94eb0be2d5b58bdcc43bc20ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topologyManagerPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterDefaultNodePoolKubeletConfig]:
        return typing.cast(typing.Optional[KubernetesClusterDefaultNodePoolKubeletConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterDefaultNodePoolKubeletConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83cb4d959d3a9c5bc5a1017a9df102e49edbde24489291c21c1e18d18c42097f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterDefaultNodePoolLinuxOsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "swap_file_size_mb": "swapFileSizeMb",
        "sysctl_config": "sysctlConfig",
        "transparent_huge_page_defrag": "transparentHugePageDefrag",
        "transparent_huge_page_enabled": "transparentHugePageEnabled",
    },
)
class KubernetesClusterDefaultNodePoolLinuxOsConfig:
    def __init__(
        self,
        *,
        swap_file_size_mb: typing.Optional[jsii.Number] = None,
        sysctl_config: typing.Optional[typing.Union["KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        transparent_huge_page_defrag: typing.Optional[builtins.str] = None,
        transparent_huge_page_enabled: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param swap_file_size_mb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#swap_file_size_mb KubernetesCluster#swap_file_size_mb}.
        :param sysctl_config: sysctl_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#sysctl_config KubernetesCluster#sysctl_config}
        :param transparent_huge_page_defrag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#transparent_huge_page_defrag KubernetesCluster#transparent_huge_page_defrag}.
        :param transparent_huge_page_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#transparent_huge_page_enabled KubernetesCluster#transparent_huge_page_enabled}.
        '''
        if isinstance(sysctl_config, dict):
            sysctl_config = KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig(**sysctl_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29391f8c0110df1b3beda37ff1b5618a7e9556770eb17f110051e374628e77ab)
            check_type(argname="argument swap_file_size_mb", value=swap_file_size_mb, expected_type=type_hints["swap_file_size_mb"])
            check_type(argname="argument sysctl_config", value=sysctl_config, expected_type=type_hints["sysctl_config"])
            check_type(argname="argument transparent_huge_page_defrag", value=transparent_huge_page_defrag, expected_type=type_hints["transparent_huge_page_defrag"])
            check_type(argname="argument transparent_huge_page_enabled", value=transparent_huge_page_enabled, expected_type=type_hints["transparent_huge_page_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if swap_file_size_mb is not None:
            self._values["swap_file_size_mb"] = swap_file_size_mb
        if sysctl_config is not None:
            self._values["sysctl_config"] = sysctl_config
        if transparent_huge_page_defrag is not None:
            self._values["transparent_huge_page_defrag"] = transparent_huge_page_defrag
        if transparent_huge_page_enabled is not None:
            self._values["transparent_huge_page_enabled"] = transparent_huge_page_enabled

    @builtins.property
    def swap_file_size_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#swap_file_size_mb KubernetesCluster#swap_file_size_mb}.'''
        result = self._values.get("swap_file_size_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sysctl_config(
        self,
    ) -> typing.Optional["KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig"]:
        '''sysctl_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#sysctl_config KubernetesCluster#sysctl_config}
        '''
        result = self._values.get("sysctl_config")
        return typing.cast(typing.Optional["KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig"], result)

    @builtins.property
    def transparent_huge_page_defrag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#transparent_huge_page_defrag KubernetesCluster#transparent_huge_page_defrag}.'''
        result = self._values.get("transparent_huge_page_defrag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transparent_huge_page_enabled(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#transparent_huge_page_enabled KubernetesCluster#transparent_huge_page_enabled}.'''
        result = self._values.get("transparent_huge_page_enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterDefaultNodePoolLinuxOsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterDefaultNodePoolLinuxOsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterDefaultNodePoolLinuxOsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee889a0e8ab4f258832efc4ca03a49d28129f7e1bf8758cec5f96444302a8b64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSysctlConfig")
    def put_sysctl_config(
        self,
        *,
        fs_aio_max_nr: typing.Optional[jsii.Number] = None,
        fs_file_max: typing.Optional[jsii.Number] = None,
        fs_inotify_max_user_watches: typing.Optional[jsii.Number] = None,
        fs_nr_open: typing.Optional[jsii.Number] = None,
        kernel_threads_max: typing.Optional[jsii.Number] = None,
        net_core_netdev_max_backlog: typing.Optional[jsii.Number] = None,
        net_core_optmem_max: typing.Optional[jsii.Number] = None,
        net_core_rmem_default: typing.Optional[jsii.Number] = None,
        net_core_rmem_max: typing.Optional[jsii.Number] = None,
        net_core_somaxconn: typing.Optional[jsii.Number] = None,
        net_core_wmem_default: typing.Optional[jsii.Number] = None,
        net_core_wmem_max: typing.Optional[jsii.Number] = None,
        net_ipv4_ip_local_port_range_max: typing.Optional[jsii.Number] = None,
        net_ipv4_ip_local_port_range_min: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh1: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh2: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh3: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_fin_timeout: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_intvl: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_probes: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_time: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_max_syn_backlog: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_max_tw_buckets: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_tw_reuse: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        net_netfilter_nf_conntrack_buckets: typing.Optional[jsii.Number] = None,
        net_netfilter_nf_conntrack_max: typing.Optional[jsii.Number] = None,
        vm_max_map_count: typing.Optional[jsii.Number] = None,
        vm_swappiness: typing.Optional[jsii.Number] = None,
        vm_vfs_cache_pressure: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fs_aio_max_nr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_aio_max_nr KubernetesCluster#fs_aio_max_nr}.
        :param fs_file_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_file_max KubernetesCluster#fs_file_max}.
        :param fs_inotify_max_user_watches: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_inotify_max_user_watches KubernetesCluster#fs_inotify_max_user_watches}.
        :param fs_nr_open: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_nr_open KubernetesCluster#fs_nr_open}.
        :param kernel_threads_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kernel_threads_max KubernetesCluster#kernel_threads_max}.
        :param net_core_netdev_max_backlog: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_netdev_max_backlog KubernetesCluster#net_core_netdev_max_backlog}.
        :param net_core_optmem_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_optmem_max KubernetesCluster#net_core_optmem_max}.
        :param net_core_rmem_default: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_rmem_default KubernetesCluster#net_core_rmem_default}.
        :param net_core_rmem_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_rmem_max KubernetesCluster#net_core_rmem_max}.
        :param net_core_somaxconn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_somaxconn KubernetesCluster#net_core_somaxconn}.
        :param net_core_wmem_default: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_wmem_default KubernetesCluster#net_core_wmem_default}.
        :param net_core_wmem_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_wmem_max KubernetesCluster#net_core_wmem_max}.
        :param net_ipv4_ip_local_port_range_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_ip_local_port_range_max KubernetesCluster#net_ipv4_ip_local_port_range_max}.
        :param net_ipv4_ip_local_port_range_min: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_ip_local_port_range_min KubernetesCluster#net_ipv4_ip_local_port_range_min}.
        :param net_ipv4_neigh_default_gc_thresh1: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_neigh_default_gc_thresh1 KubernetesCluster#net_ipv4_neigh_default_gc_thresh1}.
        :param net_ipv4_neigh_default_gc_thresh2: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_neigh_default_gc_thresh2 KubernetesCluster#net_ipv4_neigh_default_gc_thresh2}.
        :param net_ipv4_neigh_default_gc_thresh3: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_neigh_default_gc_thresh3 KubernetesCluster#net_ipv4_neigh_default_gc_thresh3}.
        :param net_ipv4_tcp_fin_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_fin_timeout KubernetesCluster#net_ipv4_tcp_fin_timeout}.
        :param net_ipv4_tcp_keepalive_intvl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_keepalive_intvl KubernetesCluster#net_ipv4_tcp_keepalive_intvl}.
        :param net_ipv4_tcp_keepalive_probes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_keepalive_probes KubernetesCluster#net_ipv4_tcp_keepalive_probes}.
        :param net_ipv4_tcp_keepalive_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_keepalive_time KubernetesCluster#net_ipv4_tcp_keepalive_time}.
        :param net_ipv4_tcp_max_syn_backlog: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_max_syn_backlog KubernetesCluster#net_ipv4_tcp_max_syn_backlog}.
        :param net_ipv4_tcp_max_tw_buckets: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_max_tw_buckets KubernetesCluster#net_ipv4_tcp_max_tw_buckets}.
        :param net_ipv4_tcp_tw_reuse: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_tw_reuse KubernetesCluster#net_ipv4_tcp_tw_reuse}.
        :param net_netfilter_nf_conntrack_buckets: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_netfilter_nf_conntrack_buckets KubernetesCluster#net_netfilter_nf_conntrack_buckets}.
        :param net_netfilter_nf_conntrack_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_netfilter_nf_conntrack_max KubernetesCluster#net_netfilter_nf_conntrack_max}.
        :param vm_max_map_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_max_map_count KubernetesCluster#vm_max_map_count}.
        :param vm_swappiness: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_swappiness KubernetesCluster#vm_swappiness}.
        :param vm_vfs_cache_pressure: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_vfs_cache_pressure KubernetesCluster#vm_vfs_cache_pressure}.
        '''
        value = KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig(
            fs_aio_max_nr=fs_aio_max_nr,
            fs_file_max=fs_file_max,
            fs_inotify_max_user_watches=fs_inotify_max_user_watches,
            fs_nr_open=fs_nr_open,
            kernel_threads_max=kernel_threads_max,
            net_core_netdev_max_backlog=net_core_netdev_max_backlog,
            net_core_optmem_max=net_core_optmem_max,
            net_core_rmem_default=net_core_rmem_default,
            net_core_rmem_max=net_core_rmem_max,
            net_core_somaxconn=net_core_somaxconn,
            net_core_wmem_default=net_core_wmem_default,
            net_core_wmem_max=net_core_wmem_max,
            net_ipv4_ip_local_port_range_max=net_ipv4_ip_local_port_range_max,
            net_ipv4_ip_local_port_range_min=net_ipv4_ip_local_port_range_min,
            net_ipv4_neigh_default_gc_thresh1=net_ipv4_neigh_default_gc_thresh1,
            net_ipv4_neigh_default_gc_thresh2=net_ipv4_neigh_default_gc_thresh2,
            net_ipv4_neigh_default_gc_thresh3=net_ipv4_neigh_default_gc_thresh3,
            net_ipv4_tcp_fin_timeout=net_ipv4_tcp_fin_timeout,
            net_ipv4_tcp_keepalive_intvl=net_ipv4_tcp_keepalive_intvl,
            net_ipv4_tcp_keepalive_probes=net_ipv4_tcp_keepalive_probes,
            net_ipv4_tcp_keepalive_time=net_ipv4_tcp_keepalive_time,
            net_ipv4_tcp_max_syn_backlog=net_ipv4_tcp_max_syn_backlog,
            net_ipv4_tcp_max_tw_buckets=net_ipv4_tcp_max_tw_buckets,
            net_ipv4_tcp_tw_reuse=net_ipv4_tcp_tw_reuse,
            net_netfilter_nf_conntrack_buckets=net_netfilter_nf_conntrack_buckets,
            net_netfilter_nf_conntrack_max=net_netfilter_nf_conntrack_max,
            vm_max_map_count=vm_max_map_count,
            vm_swappiness=vm_swappiness,
            vm_vfs_cache_pressure=vm_vfs_cache_pressure,
        )

        return typing.cast(None, jsii.invoke(self, "putSysctlConfig", [value]))

    @jsii.member(jsii_name="resetSwapFileSizeMb")
    def reset_swap_file_size_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwapFileSizeMb", []))

    @jsii.member(jsii_name="resetSysctlConfig")
    def reset_sysctl_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSysctlConfig", []))

    @jsii.member(jsii_name="resetTransparentHugePageDefrag")
    def reset_transparent_huge_page_defrag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransparentHugePageDefrag", []))

    @jsii.member(jsii_name="resetTransparentHugePageEnabled")
    def reset_transparent_huge_page_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransparentHugePageEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="sysctlConfig")
    def sysctl_config(
        self,
    ) -> "KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfigOutputReference":
        return typing.cast("KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfigOutputReference", jsii.get(self, "sysctlConfig"))

    @builtins.property
    @jsii.member(jsii_name="swapFileSizeMbInput")
    def swap_file_size_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "swapFileSizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="sysctlConfigInput")
    def sysctl_config_input(
        self,
    ) -> typing.Optional["KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig"]:
        return typing.cast(typing.Optional["KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig"], jsii.get(self, "sysctlConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="transparentHugePageDefragInput")
    def transparent_huge_page_defrag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transparentHugePageDefragInput"))

    @builtins.property
    @jsii.member(jsii_name="transparentHugePageEnabledInput")
    def transparent_huge_page_enabled_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transparentHugePageEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="swapFileSizeMb")
    def swap_file_size_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "swapFileSizeMb"))

    @swap_file_size_mb.setter
    def swap_file_size_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0112f13c42a4d74b4a6dca9403777f31f5cb722c7aa90436985b66ebecf4f33b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "swapFileSizeMb", value)

    @builtins.property
    @jsii.member(jsii_name="transparentHugePageDefrag")
    def transparent_huge_page_defrag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transparentHugePageDefrag"))

    @transparent_huge_page_defrag.setter
    def transparent_huge_page_defrag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__734557f0eb4267173567e5f5a0544a706a29f3c3cf6acc10403a0859edba3d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transparentHugePageDefrag", value)

    @builtins.property
    @jsii.member(jsii_name="transparentHugePageEnabled")
    def transparent_huge_page_enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transparentHugePageEnabled"))

    @transparent_huge_page_enabled.setter
    def transparent_huge_page_enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f36bdf8bd9701655fc2f367857bfbc06984b045a043b8f1b6285117bd7d32f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transparentHugePageEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterDefaultNodePoolLinuxOsConfig]:
        return typing.cast(typing.Optional[KubernetesClusterDefaultNodePoolLinuxOsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterDefaultNodePoolLinuxOsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27553b60bed8d410bac437d97999e495d61f69bee206db7636009c898eee013c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig",
    jsii_struct_bases=[],
    name_mapping={
        "fs_aio_max_nr": "fsAioMaxNr",
        "fs_file_max": "fsFileMax",
        "fs_inotify_max_user_watches": "fsInotifyMaxUserWatches",
        "fs_nr_open": "fsNrOpen",
        "kernel_threads_max": "kernelThreadsMax",
        "net_core_netdev_max_backlog": "netCoreNetdevMaxBacklog",
        "net_core_optmem_max": "netCoreOptmemMax",
        "net_core_rmem_default": "netCoreRmemDefault",
        "net_core_rmem_max": "netCoreRmemMax",
        "net_core_somaxconn": "netCoreSomaxconn",
        "net_core_wmem_default": "netCoreWmemDefault",
        "net_core_wmem_max": "netCoreWmemMax",
        "net_ipv4_ip_local_port_range_max": "netIpv4IpLocalPortRangeMax",
        "net_ipv4_ip_local_port_range_min": "netIpv4IpLocalPortRangeMin",
        "net_ipv4_neigh_default_gc_thresh1": "netIpv4NeighDefaultGcThresh1",
        "net_ipv4_neigh_default_gc_thresh2": "netIpv4NeighDefaultGcThresh2",
        "net_ipv4_neigh_default_gc_thresh3": "netIpv4NeighDefaultGcThresh3",
        "net_ipv4_tcp_fin_timeout": "netIpv4TcpFinTimeout",
        "net_ipv4_tcp_keepalive_intvl": "netIpv4TcpKeepaliveIntvl",
        "net_ipv4_tcp_keepalive_probes": "netIpv4TcpKeepaliveProbes",
        "net_ipv4_tcp_keepalive_time": "netIpv4TcpKeepaliveTime",
        "net_ipv4_tcp_max_syn_backlog": "netIpv4TcpMaxSynBacklog",
        "net_ipv4_tcp_max_tw_buckets": "netIpv4TcpMaxTwBuckets",
        "net_ipv4_tcp_tw_reuse": "netIpv4TcpTwReuse",
        "net_netfilter_nf_conntrack_buckets": "netNetfilterNfConntrackBuckets",
        "net_netfilter_nf_conntrack_max": "netNetfilterNfConntrackMax",
        "vm_max_map_count": "vmMaxMapCount",
        "vm_swappiness": "vmSwappiness",
        "vm_vfs_cache_pressure": "vmVfsCachePressure",
    },
)
class KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig:
    def __init__(
        self,
        *,
        fs_aio_max_nr: typing.Optional[jsii.Number] = None,
        fs_file_max: typing.Optional[jsii.Number] = None,
        fs_inotify_max_user_watches: typing.Optional[jsii.Number] = None,
        fs_nr_open: typing.Optional[jsii.Number] = None,
        kernel_threads_max: typing.Optional[jsii.Number] = None,
        net_core_netdev_max_backlog: typing.Optional[jsii.Number] = None,
        net_core_optmem_max: typing.Optional[jsii.Number] = None,
        net_core_rmem_default: typing.Optional[jsii.Number] = None,
        net_core_rmem_max: typing.Optional[jsii.Number] = None,
        net_core_somaxconn: typing.Optional[jsii.Number] = None,
        net_core_wmem_default: typing.Optional[jsii.Number] = None,
        net_core_wmem_max: typing.Optional[jsii.Number] = None,
        net_ipv4_ip_local_port_range_max: typing.Optional[jsii.Number] = None,
        net_ipv4_ip_local_port_range_min: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh1: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh2: typing.Optional[jsii.Number] = None,
        net_ipv4_neigh_default_gc_thresh3: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_fin_timeout: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_intvl: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_probes: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_keepalive_time: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_max_syn_backlog: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_max_tw_buckets: typing.Optional[jsii.Number] = None,
        net_ipv4_tcp_tw_reuse: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        net_netfilter_nf_conntrack_buckets: typing.Optional[jsii.Number] = None,
        net_netfilter_nf_conntrack_max: typing.Optional[jsii.Number] = None,
        vm_max_map_count: typing.Optional[jsii.Number] = None,
        vm_swappiness: typing.Optional[jsii.Number] = None,
        vm_vfs_cache_pressure: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fs_aio_max_nr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_aio_max_nr KubernetesCluster#fs_aio_max_nr}.
        :param fs_file_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_file_max KubernetesCluster#fs_file_max}.
        :param fs_inotify_max_user_watches: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_inotify_max_user_watches KubernetesCluster#fs_inotify_max_user_watches}.
        :param fs_nr_open: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_nr_open KubernetesCluster#fs_nr_open}.
        :param kernel_threads_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kernel_threads_max KubernetesCluster#kernel_threads_max}.
        :param net_core_netdev_max_backlog: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_netdev_max_backlog KubernetesCluster#net_core_netdev_max_backlog}.
        :param net_core_optmem_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_optmem_max KubernetesCluster#net_core_optmem_max}.
        :param net_core_rmem_default: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_rmem_default KubernetesCluster#net_core_rmem_default}.
        :param net_core_rmem_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_rmem_max KubernetesCluster#net_core_rmem_max}.
        :param net_core_somaxconn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_somaxconn KubernetesCluster#net_core_somaxconn}.
        :param net_core_wmem_default: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_wmem_default KubernetesCluster#net_core_wmem_default}.
        :param net_core_wmem_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_wmem_max KubernetesCluster#net_core_wmem_max}.
        :param net_ipv4_ip_local_port_range_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_ip_local_port_range_max KubernetesCluster#net_ipv4_ip_local_port_range_max}.
        :param net_ipv4_ip_local_port_range_min: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_ip_local_port_range_min KubernetesCluster#net_ipv4_ip_local_port_range_min}.
        :param net_ipv4_neigh_default_gc_thresh1: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_neigh_default_gc_thresh1 KubernetesCluster#net_ipv4_neigh_default_gc_thresh1}.
        :param net_ipv4_neigh_default_gc_thresh2: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_neigh_default_gc_thresh2 KubernetesCluster#net_ipv4_neigh_default_gc_thresh2}.
        :param net_ipv4_neigh_default_gc_thresh3: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_neigh_default_gc_thresh3 KubernetesCluster#net_ipv4_neigh_default_gc_thresh3}.
        :param net_ipv4_tcp_fin_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_fin_timeout KubernetesCluster#net_ipv4_tcp_fin_timeout}.
        :param net_ipv4_tcp_keepalive_intvl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_keepalive_intvl KubernetesCluster#net_ipv4_tcp_keepalive_intvl}.
        :param net_ipv4_tcp_keepalive_probes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_keepalive_probes KubernetesCluster#net_ipv4_tcp_keepalive_probes}.
        :param net_ipv4_tcp_keepalive_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_keepalive_time KubernetesCluster#net_ipv4_tcp_keepalive_time}.
        :param net_ipv4_tcp_max_syn_backlog: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_max_syn_backlog KubernetesCluster#net_ipv4_tcp_max_syn_backlog}.
        :param net_ipv4_tcp_max_tw_buckets: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_max_tw_buckets KubernetesCluster#net_ipv4_tcp_max_tw_buckets}.
        :param net_ipv4_tcp_tw_reuse: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_tw_reuse KubernetesCluster#net_ipv4_tcp_tw_reuse}.
        :param net_netfilter_nf_conntrack_buckets: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_netfilter_nf_conntrack_buckets KubernetesCluster#net_netfilter_nf_conntrack_buckets}.
        :param net_netfilter_nf_conntrack_max: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_netfilter_nf_conntrack_max KubernetesCluster#net_netfilter_nf_conntrack_max}.
        :param vm_max_map_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_max_map_count KubernetesCluster#vm_max_map_count}.
        :param vm_swappiness: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_swappiness KubernetesCluster#vm_swappiness}.
        :param vm_vfs_cache_pressure: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_vfs_cache_pressure KubernetesCluster#vm_vfs_cache_pressure}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e227dc27495a78cd0a014f0c5d59f7387bcc3f645f4219d7673ffaba224f86b8)
            check_type(argname="argument fs_aio_max_nr", value=fs_aio_max_nr, expected_type=type_hints["fs_aio_max_nr"])
            check_type(argname="argument fs_file_max", value=fs_file_max, expected_type=type_hints["fs_file_max"])
            check_type(argname="argument fs_inotify_max_user_watches", value=fs_inotify_max_user_watches, expected_type=type_hints["fs_inotify_max_user_watches"])
            check_type(argname="argument fs_nr_open", value=fs_nr_open, expected_type=type_hints["fs_nr_open"])
            check_type(argname="argument kernel_threads_max", value=kernel_threads_max, expected_type=type_hints["kernel_threads_max"])
            check_type(argname="argument net_core_netdev_max_backlog", value=net_core_netdev_max_backlog, expected_type=type_hints["net_core_netdev_max_backlog"])
            check_type(argname="argument net_core_optmem_max", value=net_core_optmem_max, expected_type=type_hints["net_core_optmem_max"])
            check_type(argname="argument net_core_rmem_default", value=net_core_rmem_default, expected_type=type_hints["net_core_rmem_default"])
            check_type(argname="argument net_core_rmem_max", value=net_core_rmem_max, expected_type=type_hints["net_core_rmem_max"])
            check_type(argname="argument net_core_somaxconn", value=net_core_somaxconn, expected_type=type_hints["net_core_somaxconn"])
            check_type(argname="argument net_core_wmem_default", value=net_core_wmem_default, expected_type=type_hints["net_core_wmem_default"])
            check_type(argname="argument net_core_wmem_max", value=net_core_wmem_max, expected_type=type_hints["net_core_wmem_max"])
            check_type(argname="argument net_ipv4_ip_local_port_range_max", value=net_ipv4_ip_local_port_range_max, expected_type=type_hints["net_ipv4_ip_local_port_range_max"])
            check_type(argname="argument net_ipv4_ip_local_port_range_min", value=net_ipv4_ip_local_port_range_min, expected_type=type_hints["net_ipv4_ip_local_port_range_min"])
            check_type(argname="argument net_ipv4_neigh_default_gc_thresh1", value=net_ipv4_neigh_default_gc_thresh1, expected_type=type_hints["net_ipv4_neigh_default_gc_thresh1"])
            check_type(argname="argument net_ipv4_neigh_default_gc_thresh2", value=net_ipv4_neigh_default_gc_thresh2, expected_type=type_hints["net_ipv4_neigh_default_gc_thresh2"])
            check_type(argname="argument net_ipv4_neigh_default_gc_thresh3", value=net_ipv4_neigh_default_gc_thresh3, expected_type=type_hints["net_ipv4_neigh_default_gc_thresh3"])
            check_type(argname="argument net_ipv4_tcp_fin_timeout", value=net_ipv4_tcp_fin_timeout, expected_type=type_hints["net_ipv4_tcp_fin_timeout"])
            check_type(argname="argument net_ipv4_tcp_keepalive_intvl", value=net_ipv4_tcp_keepalive_intvl, expected_type=type_hints["net_ipv4_tcp_keepalive_intvl"])
            check_type(argname="argument net_ipv4_tcp_keepalive_probes", value=net_ipv4_tcp_keepalive_probes, expected_type=type_hints["net_ipv4_tcp_keepalive_probes"])
            check_type(argname="argument net_ipv4_tcp_keepalive_time", value=net_ipv4_tcp_keepalive_time, expected_type=type_hints["net_ipv4_tcp_keepalive_time"])
            check_type(argname="argument net_ipv4_tcp_max_syn_backlog", value=net_ipv4_tcp_max_syn_backlog, expected_type=type_hints["net_ipv4_tcp_max_syn_backlog"])
            check_type(argname="argument net_ipv4_tcp_max_tw_buckets", value=net_ipv4_tcp_max_tw_buckets, expected_type=type_hints["net_ipv4_tcp_max_tw_buckets"])
            check_type(argname="argument net_ipv4_tcp_tw_reuse", value=net_ipv4_tcp_tw_reuse, expected_type=type_hints["net_ipv4_tcp_tw_reuse"])
            check_type(argname="argument net_netfilter_nf_conntrack_buckets", value=net_netfilter_nf_conntrack_buckets, expected_type=type_hints["net_netfilter_nf_conntrack_buckets"])
            check_type(argname="argument net_netfilter_nf_conntrack_max", value=net_netfilter_nf_conntrack_max, expected_type=type_hints["net_netfilter_nf_conntrack_max"])
            check_type(argname="argument vm_max_map_count", value=vm_max_map_count, expected_type=type_hints["vm_max_map_count"])
            check_type(argname="argument vm_swappiness", value=vm_swappiness, expected_type=type_hints["vm_swappiness"])
            check_type(argname="argument vm_vfs_cache_pressure", value=vm_vfs_cache_pressure, expected_type=type_hints["vm_vfs_cache_pressure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fs_aio_max_nr is not None:
            self._values["fs_aio_max_nr"] = fs_aio_max_nr
        if fs_file_max is not None:
            self._values["fs_file_max"] = fs_file_max
        if fs_inotify_max_user_watches is not None:
            self._values["fs_inotify_max_user_watches"] = fs_inotify_max_user_watches
        if fs_nr_open is not None:
            self._values["fs_nr_open"] = fs_nr_open
        if kernel_threads_max is not None:
            self._values["kernel_threads_max"] = kernel_threads_max
        if net_core_netdev_max_backlog is not None:
            self._values["net_core_netdev_max_backlog"] = net_core_netdev_max_backlog
        if net_core_optmem_max is not None:
            self._values["net_core_optmem_max"] = net_core_optmem_max
        if net_core_rmem_default is not None:
            self._values["net_core_rmem_default"] = net_core_rmem_default
        if net_core_rmem_max is not None:
            self._values["net_core_rmem_max"] = net_core_rmem_max
        if net_core_somaxconn is not None:
            self._values["net_core_somaxconn"] = net_core_somaxconn
        if net_core_wmem_default is not None:
            self._values["net_core_wmem_default"] = net_core_wmem_default
        if net_core_wmem_max is not None:
            self._values["net_core_wmem_max"] = net_core_wmem_max
        if net_ipv4_ip_local_port_range_max is not None:
            self._values["net_ipv4_ip_local_port_range_max"] = net_ipv4_ip_local_port_range_max
        if net_ipv4_ip_local_port_range_min is not None:
            self._values["net_ipv4_ip_local_port_range_min"] = net_ipv4_ip_local_port_range_min
        if net_ipv4_neigh_default_gc_thresh1 is not None:
            self._values["net_ipv4_neigh_default_gc_thresh1"] = net_ipv4_neigh_default_gc_thresh1
        if net_ipv4_neigh_default_gc_thresh2 is not None:
            self._values["net_ipv4_neigh_default_gc_thresh2"] = net_ipv4_neigh_default_gc_thresh2
        if net_ipv4_neigh_default_gc_thresh3 is not None:
            self._values["net_ipv4_neigh_default_gc_thresh3"] = net_ipv4_neigh_default_gc_thresh3
        if net_ipv4_tcp_fin_timeout is not None:
            self._values["net_ipv4_tcp_fin_timeout"] = net_ipv4_tcp_fin_timeout
        if net_ipv4_tcp_keepalive_intvl is not None:
            self._values["net_ipv4_tcp_keepalive_intvl"] = net_ipv4_tcp_keepalive_intvl
        if net_ipv4_tcp_keepalive_probes is not None:
            self._values["net_ipv4_tcp_keepalive_probes"] = net_ipv4_tcp_keepalive_probes
        if net_ipv4_tcp_keepalive_time is not None:
            self._values["net_ipv4_tcp_keepalive_time"] = net_ipv4_tcp_keepalive_time
        if net_ipv4_tcp_max_syn_backlog is not None:
            self._values["net_ipv4_tcp_max_syn_backlog"] = net_ipv4_tcp_max_syn_backlog
        if net_ipv4_tcp_max_tw_buckets is not None:
            self._values["net_ipv4_tcp_max_tw_buckets"] = net_ipv4_tcp_max_tw_buckets
        if net_ipv4_tcp_tw_reuse is not None:
            self._values["net_ipv4_tcp_tw_reuse"] = net_ipv4_tcp_tw_reuse
        if net_netfilter_nf_conntrack_buckets is not None:
            self._values["net_netfilter_nf_conntrack_buckets"] = net_netfilter_nf_conntrack_buckets
        if net_netfilter_nf_conntrack_max is not None:
            self._values["net_netfilter_nf_conntrack_max"] = net_netfilter_nf_conntrack_max
        if vm_max_map_count is not None:
            self._values["vm_max_map_count"] = vm_max_map_count
        if vm_swappiness is not None:
            self._values["vm_swappiness"] = vm_swappiness
        if vm_vfs_cache_pressure is not None:
            self._values["vm_vfs_cache_pressure"] = vm_vfs_cache_pressure

    @builtins.property
    def fs_aio_max_nr(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_aio_max_nr KubernetesCluster#fs_aio_max_nr}.'''
        result = self._values.get("fs_aio_max_nr")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fs_file_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_file_max KubernetesCluster#fs_file_max}.'''
        result = self._values.get("fs_file_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fs_inotify_max_user_watches(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_inotify_max_user_watches KubernetesCluster#fs_inotify_max_user_watches}.'''
        result = self._values.get("fs_inotify_max_user_watches")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fs_nr_open(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#fs_nr_open KubernetesCluster#fs_nr_open}.'''
        result = self._values.get("fs_nr_open")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kernel_threads_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#kernel_threads_max KubernetesCluster#kernel_threads_max}.'''
        result = self._values.get("kernel_threads_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_netdev_max_backlog(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_netdev_max_backlog KubernetesCluster#net_core_netdev_max_backlog}.'''
        result = self._values.get("net_core_netdev_max_backlog")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_optmem_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_optmem_max KubernetesCluster#net_core_optmem_max}.'''
        result = self._values.get("net_core_optmem_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_rmem_default(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_rmem_default KubernetesCluster#net_core_rmem_default}.'''
        result = self._values.get("net_core_rmem_default")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_rmem_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_rmem_max KubernetesCluster#net_core_rmem_max}.'''
        result = self._values.get("net_core_rmem_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_somaxconn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_somaxconn KubernetesCluster#net_core_somaxconn}.'''
        result = self._values.get("net_core_somaxconn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_wmem_default(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_wmem_default KubernetesCluster#net_core_wmem_default}.'''
        result = self._values.get("net_core_wmem_default")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_core_wmem_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_core_wmem_max KubernetesCluster#net_core_wmem_max}.'''
        result = self._values.get("net_core_wmem_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_ip_local_port_range_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_ip_local_port_range_max KubernetesCluster#net_ipv4_ip_local_port_range_max}.'''
        result = self._values.get("net_ipv4_ip_local_port_range_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_ip_local_port_range_min(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_ip_local_port_range_min KubernetesCluster#net_ipv4_ip_local_port_range_min}.'''
        result = self._values.get("net_ipv4_ip_local_port_range_min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_neigh_default_gc_thresh1(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_neigh_default_gc_thresh1 KubernetesCluster#net_ipv4_neigh_default_gc_thresh1}.'''
        result = self._values.get("net_ipv4_neigh_default_gc_thresh1")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_neigh_default_gc_thresh2(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_neigh_default_gc_thresh2 KubernetesCluster#net_ipv4_neigh_default_gc_thresh2}.'''
        result = self._values.get("net_ipv4_neigh_default_gc_thresh2")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_neigh_default_gc_thresh3(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_neigh_default_gc_thresh3 KubernetesCluster#net_ipv4_neigh_default_gc_thresh3}.'''
        result = self._values.get("net_ipv4_neigh_default_gc_thresh3")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_fin_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_fin_timeout KubernetesCluster#net_ipv4_tcp_fin_timeout}.'''
        result = self._values.get("net_ipv4_tcp_fin_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_keepalive_intvl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_keepalive_intvl KubernetesCluster#net_ipv4_tcp_keepalive_intvl}.'''
        result = self._values.get("net_ipv4_tcp_keepalive_intvl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_keepalive_probes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_keepalive_probes KubernetesCluster#net_ipv4_tcp_keepalive_probes}.'''
        result = self._values.get("net_ipv4_tcp_keepalive_probes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_keepalive_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_keepalive_time KubernetesCluster#net_ipv4_tcp_keepalive_time}.'''
        result = self._values.get("net_ipv4_tcp_keepalive_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_max_syn_backlog(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_max_syn_backlog KubernetesCluster#net_ipv4_tcp_max_syn_backlog}.'''
        result = self._values.get("net_ipv4_tcp_max_syn_backlog")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_max_tw_buckets(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_max_tw_buckets KubernetesCluster#net_ipv4_tcp_max_tw_buckets}.'''
        result = self._values.get("net_ipv4_tcp_max_tw_buckets")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_ipv4_tcp_tw_reuse(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_ipv4_tcp_tw_reuse KubernetesCluster#net_ipv4_tcp_tw_reuse}.'''
        result = self._values.get("net_ipv4_tcp_tw_reuse")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def net_netfilter_nf_conntrack_buckets(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_netfilter_nf_conntrack_buckets KubernetesCluster#net_netfilter_nf_conntrack_buckets}.'''
        result = self._values.get("net_netfilter_nf_conntrack_buckets")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def net_netfilter_nf_conntrack_max(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#net_netfilter_nf_conntrack_max KubernetesCluster#net_netfilter_nf_conntrack_max}.'''
        result = self._values.get("net_netfilter_nf_conntrack_max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vm_max_map_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_max_map_count KubernetesCluster#vm_max_map_count}.'''
        result = self._values.get("vm_max_map_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vm_swappiness(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_swappiness KubernetesCluster#vm_swappiness}.'''
        result = self._values.get("vm_swappiness")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vm_vfs_cache_pressure(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#vm_vfs_cache_pressure KubernetesCluster#vm_vfs_cache_pressure}.'''
        result = self._values.get("vm_vfs_cache_pressure")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d29257c618a09308fee27c08fad289554a561c9959007d45046f0b7419b2761a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFsAioMaxNr")
    def reset_fs_aio_max_nr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsAioMaxNr", []))

    @jsii.member(jsii_name="resetFsFileMax")
    def reset_fs_file_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsFileMax", []))

    @jsii.member(jsii_name="resetFsInotifyMaxUserWatches")
    def reset_fs_inotify_max_user_watches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsInotifyMaxUserWatches", []))

    @jsii.member(jsii_name="resetFsNrOpen")
    def reset_fs_nr_open(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsNrOpen", []))

    @jsii.member(jsii_name="resetKernelThreadsMax")
    def reset_kernel_threads_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKernelThreadsMax", []))

    @jsii.member(jsii_name="resetNetCoreNetdevMaxBacklog")
    def reset_net_core_netdev_max_backlog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreNetdevMaxBacklog", []))

    @jsii.member(jsii_name="resetNetCoreOptmemMax")
    def reset_net_core_optmem_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreOptmemMax", []))

    @jsii.member(jsii_name="resetNetCoreRmemDefault")
    def reset_net_core_rmem_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreRmemDefault", []))

    @jsii.member(jsii_name="resetNetCoreRmemMax")
    def reset_net_core_rmem_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreRmemMax", []))

    @jsii.member(jsii_name="resetNetCoreSomaxconn")
    def reset_net_core_somaxconn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreSomaxconn", []))

    @jsii.member(jsii_name="resetNetCoreWmemDefault")
    def reset_net_core_wmem_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreWmemDefault", []))

    @jsii.member(jsii_name="resetNetCoreWmemMax")
    def reset_net_core_wmem_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetCoreWmemMax", []))

    @jsii.member(jsii_name="resetNetIpv4IpLocalPortRangeMax")
    def reset_net_ipv4_ip_local_port_range_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4IpLocalPortRangeMax", []))

    @jsii.member(jsii_name="resetNetIpv4IpLocalPortRangeMin")
    def reset_net_ipv4_ip_local_port_range_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4IpLocalPortRangeMin", []))

    @jsii.member(jsii_name="resetNetIpv4NeighDefaultGcThresh1")
    def reset_net_ipv4_neigh_default_gc_thresh1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4NeighDefaultGcThresh1", []))

    @jsii.member(jsii_name="resetNetIpv4NeighDefaultGcThresh2")
    def reset_net_ipv4_neigh_default_gc_thresh2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4NeighDefaultGcThresh2", []))

    @jsii.member(jsii_name="resetNetIpv4NeighDefaultGcThresh3")
    def reset_net_ipv4_neigh_default_gc_thresh3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4NeighDefaultGcThresh3", []))

    @jsii.member(jsii_name="resetNetIpv4TcpFinTimeout")
    def reset_net_ipv4_tcp_fin_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpFinTimeout", []))

    @jsii.member(jsii_name="resetNetIpv4TcpKeepaliveIntvl")
    def reset_net_ipv4_tcp_keepalive_intvl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpKeepaliveIntvl", []))

    @jsii.member(jsii_name="resetNetIpv4TcpKeepaliveProbes")
    def reset_net_ipv4_tcp_keepalive_probes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpKeepaliveProbes", []))

    @jsii.member(jsii_name="resetNetIpv4TcpKeepaliveTime")
    def reset_net_ipv4_tcp_keepalive_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpKeepaliveTime", []))

    @jsii.member(jsii_name="resetNetIpv4TcpMaxSynBacklog")
    def reset_net_ipv4_tcp_max_syn_backlog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpMaxSynBacklog", []))

    @jsii.member(jsii_name="resetNetIpv4TcpMaxTwBuckets")
    def reset_net_ipv4_tcp_max_tw_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpMaxTwBuckets", []))

    @jsii.member(jsii_name="resetNetIpv4TcpTwReuse")
    def reset_net_ipv4_tcp_tw_reuse(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetIpv4TcpTwReuse", []))

    @jsii.member(jsii_name="resetNetNetfilterNfConntrackBuckets")
    def reset_net_netfilter_nf_conntrack_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetNetfilterNfConntrackBuckets", []))

    @jsii.member(jsii_name="resetNetNetfilterNfConntrackMax")
    def reset_net_netfilter_nf_conntrack_max(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetNetfilterNfConntrackMax", []))

    @jsii.member(jsii_name="resetVmMaxMapCount")
    def reset_vm_max_map_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmMaxMapCount", []))

    @jsii.member(jsii_name="resetVmSwappiness")
    def reset_vm_swappiness(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmSwappiness", []))

    @jsii.member(jsii_name="resetVmVfsCachePressure")
    def reset_vm_vfs_cache_pressure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmVfsCachePressure", []))

    @builtins.property
    @jsii.member(jsii_name="fsAioMaxNrInput")
    def fs_aio_max_nr_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fsAioMaxNrInput"))

    @builtins.property
    @jsii.member(jsii_name="fsFileMaxInput")
    def fs_file_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fsFileMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="fsInotifyMaxUserWatchesInput")
    def fs_inotify_max_user_watches_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fsInotifyMaxUserWatchesInput"))

    @builtins.property
    @jsii.member(jsii_name="fsNrOpenInput")
    def fs_nr_open_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fsNrOpenInput"))

    @builtins.property
    @jsii.member(jsii_name="kernelThreadsMaxInput")
    def kernel_threads_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "kernelThreadsMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreNetdevMaxBacklogInput")
    def net_core_netdev_max_backlog_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreNetdevMaxBacklogInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreOptmemMaxInput")
    def net_core_optmem_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreOptmemMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreRmemDefaultInput")
    def net_core_rmem_default_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreRmemDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreRmemMaxInput")
    def net_core_rmem_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreRmemMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreSomaxconnInput")
    def net_core_somaxconn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreSomaxconnInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreWmemDefaultInput")
    def net_core_wmem_default_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreWmemDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="netCoreWmemMaxInput")
    def net_core_wmem_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netCoreWmemMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4IpLocalPortRangeMaxInput")
    def net_ipv4_ip_local_port_range_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4IpLocalPortRangeMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4IpLocalPortRangeMinInput")
    def net_ipv4_ip_local_port_range_min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4IpLocalPortRangeMinInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh1Input")
    def net_ipv4_neigh_default_gc_thresh1_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4NeighDefaultGcThresh1Input"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh2Input")
    def net_ipv4_neigh_default_gc_thresh2_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4NeighDefaultGcThresh2Input"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh3Input")
    def net_ipv4_neigh_default_gc_thresh3_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4NeighDefaultGcThresh3Input"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpFinTimeoutInput")
    def net_ipv4_tcp_fin_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpFinTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveIntvlInput")
    def net_ipv4_tcp_keepalive_intvl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpKeepaliveIntvlInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveProbesInput")
    def net_ipv4_tcp_keepalive_probes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpKeepaliveProbesInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveTimeInput")
    def net_ipv4_tcp_keepalive_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpKeepaliveTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpMaxSynBacklogInput")
    def net_ipv4_tcp_max_syn_backlog_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpMaxSynBacklogInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpMaxTwBucketsInput")
    def net_ipv4_tcp_max_tw_buckets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netIpv4TcpMaxTwBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpTwReuseInput")
    def net_ipv4_tcp_tw_reuse_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "netIpv4TcpTwReuseInput"))

    @builtins.property
    @jsii.member(jsii_name="netNetfilterNfConntrackBucketsInput")
    def net_netfilter_nf_conntrack_buckets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netNetfilterNfConntrackBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="netNetfilterNfConntrackMaxInput")
    def net_netfilter_nf_conntrack_max_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "netNetfilterNfConntrackMaxInput"))

    @builtins.property
    @jsii.member(jsii_name="vmMaxMapCountInput")
    def vm_max_map_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmMaxMapCountInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSwappinessInput")
    def vm_swappiness_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmSwappinessInput"))

    @builtins.property
    @jsii.member(jsii_name="vmVfsCachePressureInput")
    def vm_vfs_cache_pressure_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmVfsCachePressureInput"))

    @builtins.property
    @jsii.member(jsii_name="fsAioMaxNr")
    def fs_aio_max_nr(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fsAioMaxNr"))

    @fs_aio_max_nr.setter
    def fs_aio_max_nr(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24cd78790b4aedca78b1cef0dd020aa4dd26290bf6f8db1d7e5328184dff20aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsAioMaxNr", value)

    @builtins.property
    @jsii.member(jsii_name="fsFileMax")
    def fs_file_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fsFileMax"))

    @fs_file_max.setter
    def fs_file_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a7a556842c7e7c2c22eb46038660e2d890ff70238ced3964e022e20e3cd530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsFileMax", value)

    @builtins.property
    @jsii.member(jsii_name="fsInotifyMaxUserWatches")
    def fs_inotify_max_user_watches(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fsInotifyMaxUserWatches"))

    @fs_inotify_max_user_watches.setter
    def fs_inotify_max_user_watches(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37ed137129cbbd913010ebcbe57b6e13214afeec7fa1ff1eeb21f5af175d0cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsInotifyMaxUserWatches", value)

    @builtins.property
    @jsii.member(jsii_name="fsNrOpen")
    def fs_nr_open(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fsNrOpen"))

    @fs_nr_open.setter
    def fs_nr_open(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6968626339578a0531805cebef986281d18f61a7d41d1bf08c69d9c493baec5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsNrOpen", value)

    @builtins.property
    @jsii.member(jsii_name="kernelThreadsMax")
    def kernel_threads_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "kernelThreadsMax"))

    @kernel_threads_max.setter
    def kernel_threads_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78048876a220cb18baa6251b170f82ee9f778ce9589dbbcd8749d693d3fedf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kernelThreadsMax", value)

    @builtins.property
    @jsii.member(jsii_name="netCoreNetdevMaxBacklog")
    def net_core_netdev_max_backlog(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreNetdevMaxBacklog"))

    @net_core_netdev_max_backlog.setter
    def net_core_netdev_max_backlog(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606f352fa1673eb3e38fca4c9851934a0222404a1ef8ecbca83600fb1dd03712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreNetdevMaxBacklog", value)

    @builtins.property
    @jsii.member(jsii_name="netCoreOptmemMax")
    def net_core_optmem_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreOptmemMax"))

    @net_core_optmem_max.setter
    def net_core_optmem_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5efc4496a12d74abaa353b14846538819fb26cea23ffc6246a3dfa3a867672)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreOptmemMax", value)

    @builtins.property
    @jsii.member(jsii_name="netCoreRmemDefault")
    def net_core_rmem_default(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreRmemDefault"))

    @net_core_rmem_default.setter
    def net_core_rmem_default(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf298464245b8f8a64d8d28162e551c427021edd4ab9c7b75dd43daed72ffe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreRmemDefault", value)

    @builtins.property
    @jsii.member(jsii_name="netCoreRmemMax")
    def net_core_rmem_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreRmemMax"))

    @net_core_rmem_max.setter
    def net_core_rmem_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37706c5f4abcdbce957518a62b0aee6227c44d3e37167c5643b8c92ffe53f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreRmemMax", value)

    @builtins.property
    @jsii.member(jsii_name="netCoreSomaxconn")
    def net_core_somaxconn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreSomaxconn"))

    @net_core_somaxconn.setter
    def net_core_somaxconn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5170c6d8748348cfd6016ea343fe9a44b9dcaecf14557fb8691be4eddb2361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreSomaxconn", value)

    @builtins.property
    @jsii.member(jsii_name="netCoreWmemDefault")
    def net_core_wmem_default(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreWmemDefault"))

    @net_core_wmem_default.setter
    def net_core_wmem_default(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c64733c79825ea41b191a7a4ac7ec82de89f733c6891c7f4784ab35c8f9ece1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreWmemDefault", value)

    @builtins.property
    @jsii.member(jsii_name="netCoreWmemMax")
    def net_core_wmem_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netCoreWmemMax"))

    @net_core_wmem_max.setter
    def net_core_wmem_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80154a4a484a7316b58baedc6e765889b85b6a2316e605d0b779c3ec5f9321a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netCoreWmemMax", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4IpLocalPortRangeMax")
    def net_ipv4_ip_local_port_range_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4IpLocalPortRangeMax"))

    @net_ipv4_ip_local_port_range_max.setter
    def net_ipv4_ip_local_port_range_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a1a146ac423196842fa366622c5878d1fb0cb25a0e5f11b143fba206290ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4IpLocalPortRangeMax", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4IpLocalPortRangeMin")
    def net_ipv4_ip_local_port_range_min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4IpLocalPortRangeMin"))

    @net_ipv4_ip_local_port_range_min.setter
    def net_ipv4_ip_local_port_range_min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa14f1b91360350821157bdede34d887a777a94af3cb91b1c7db3711313106b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4IpLocalPortRangeMin", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh1")
    def net_ipv4_neigh_default_gc_thresh1(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4NeighDefaultGcThresh1"))

    @net_ipv4_neigh_default_gc_thresh1.setter
    def net_ipv4_neigh_default_gc_thresh1(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5995f61d862d015049c0677a3cf2d9fec67d08b51f698f380fab33f17750eab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4NeighDefaultGcThresh1", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh2")
    def net_ipv4_neigh_default_gc_thresh2(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4NeighDefaultGcThresh2"))

    @net_ipv4_neigh_default_gc_thresh2.setter
    def net_ipv4_neigh_default_gc_thresh2(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e3817652350b9883f9617c20b548e3e8f5a775dd724a90a0d091cf5aec056e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4NeighDefaultGcThresh2", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4NeighDefaultGcThresh3")
    def net_ipv4_neigh_default_gc_thresh3(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4NeighDefaultGcThresh3"))

    @net_ipv4_neigh_default_gc_thresh3.setter
    def net_ipv4_neigh_default_gc_thresh3(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25756de544dff80701aaef0b878c69c85a1ecb3fdeb1d855750e2d2c3abc124c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4NeighDefaultGcThresh3", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpFinTimeout")
    def net_ipv4_tcp_fin_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpFinTimeout"))

    @net_ipv4_tcp_fin_timeout.setter
    def net_ipv4_tcp_fin_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882158c91ca783c9628441c0d9256f5b2b4cd55bd85ada06e9ec20238cbbb506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpFinTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveIntvl")
    def net_ipv4_tcp_keepalive_intvl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpKeepaliveIntvl"))

    @net_ipv4_tcp_keepalive_intvl.setter
    def net_ipv4_tcp_keepalive_intvl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d223970369817426f7d46b700f704f9ed066bf053be9908f49a602426f5d8ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpKeepaliveIntvl", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveProbes")
    def net_ipv4_tcp_keepalive_probes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpKeepaliveProbes"))

    @net_ipv4_tcp_keepalive_probes.setter
    def net_ipv4_tcp_keepalive_probes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e55bf13c9236c2b20bf9ac4c8a1bb63b5c45ec6dfd2158109de0f320dd2f02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpKeepaliveProbes", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpKeepaliveTime")
    def net_ipv4_tcp_keepalive_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpKeepaliveTime"))

    @net_ipv4_tcp_keepalive_time.setter
    def net_ipv4_tcp_keepalive_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e918f203fb04bb4b05e44c681d1c601403bd41c156586def822b2606ad099a40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpKeepaliveTime", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpMaxSynBacklog")
    def net_ipv4_tcp_max_syn_backlog(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpMaxSynBacklog"))

    @net_ipv4_tcp_max_syn_backlog.setter
    def net_ipv4_tcp_max_syn_backlog(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa2f71bf5c7f9e3dcd93d2b63115b4faa89dc0b9cb963ba0250a11c702b3dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpMaxSynBacklog", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpMaxTwBuckets")
    def net_ipv4_tcp_max_tw_buckets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netIpv4TcpMaxTwBuckets"))

    @net_ipv4_tcp_max_tw_buckets.setter
    def net_ipv4_tcp_max_tw_buckets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4efcb4c7777621205f5d3c3bb0241484ea404efe9211e0f6ce47e26a8ad90a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpMaxTwBuckets", value)

    @builtins.property
    @jsii.member(jsii_name="netIpv4TcpTwReuse")
    def net_ipv4_tcp_tw_reuse(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "netIpv4TcpTwReuse"))

    @net_ipv4_tcp_tw_reuse.setter
    def net_ipv4_tcp_tw_reuse(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66596ae6471efcd1d7d145d150c2c1cf23d8756c4884e806f87d2fc0a9215305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netIpv4TcpTwReuse", value)

    @builtins.property
    @jsii.member(jsii_name="netNetfilterNfConntrackBuckets")
    def net_netfilter_nf_conntrack_buckets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netNetfilterNfConntrackBuckets"))

    @net_netfilter_nf_conntrack_buckets.setter
    def net_netfilter_nf_conntrack_buckets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abba017c0453eafee42ad25fa75337fb2a946a7b5555385547062b4aef41491f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netNetfilterNfConntrackBuckets", value)

    @builtins.property
    @jsii.member(jsii_name="netNetfilterNfConntrackMax")
    def net_netfilter_nf_conntrack_max(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netNetfilterNfConntrackMax"))

    @net_netfilter_nf_conntrack_max.setter
    def net_netfilter_nf_conntrack_max(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__252963bf83ff0e5e45e31a424797c506f974e9d6a608bd9275b68f92e8cc37a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netNetfilterNfConntrackMax", value)

    @builtins.property
    @jsii.member(jsii_name="vmMaxMapCount")
    def vm_max_map_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmMaxMapCount"))

    @vm_max_map_count.setter
    def vm_max_map_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae293ada6f38ce6012bc9570a30e018f8c804c1dfb91b8d56cc953845e2ecf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmMaxMapCount", value)

    @builtins.property
    @jsii.member(jsii_name="vmSwappiness")
    def vm_swappiness(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmSwappiness"))

    @vm_swappiness.setter
    def vm_swappiness(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27ae8a304ee3c08cb51f6a50c2cda3056afb4b321d4980fbaa5a2cc8a9d7a1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSwappiness", value)

    @builtins.property
    @jsii.member(jsii_name="vmVfsCachePressure")
    def vm_vfs_cache_pressure(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmVfsCachePressure"))

    @vm_vfs_cache_pressure.setter
    def vm_vfs_cache_pressure(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca60947aae97a74c74f03506b70fb62d326740f62c8722260ce71f3104efeb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmVfsCachePressure", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig]:
        return typing.cast(typing.Optional[KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c071ed9d77aa08a321e96b178e8f0b6af1abdec318bbf95c15c716c7c4b75361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KubernetesClusterDefaultNodePoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterDefaultNodePoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1558650cf24e910438d9a160d0b608b595b9c8adc3f93fc848091ee0ea393002)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKubeletConfig")
    def put_kubelet_config(
        self,
        *,
        allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_log_max_line: typing.Optional[jsii.Number] = None,
        container_log_max_size_mb: typing.Optional[jsii.Number] = None,
        cpu_cfs_quota_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
        cpu_manager_policy: typing.Optional[builtins.str] = None,
        image_gc_high_threshold: typing.Optional[jsii.Number] = None,
        image_gc_low_threshold: typing.Optional[jsii.Number] = None,
        pod_max_pid: typing.Optional[jsii.Number] = None,
        topology_manager_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_unsafe_sysctls: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#allowed_unsafe_sysctls KubernetesCluster#allowed_unsafe_sysctls}.
        :param container_log_max_line: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#container_log_max_line KubernetesCluster#container_log_max_line}.
        :param container_log_max_size_mb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#container_log_max_size_mb KubernetesCluster#container_log_max_size_mb}.
        :param cpu_cfs_quota_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#cpu_cfs_quota_enabled KubernetesCluster#cpu_cfs_quota_enabled}.
        :param cpu_cfs_quota_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#cpu_cfs_quota_period KubernetesCluster#cpu_cfs_quota_period}.
        :param cpu_manager_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#cpu_manager_policy KubernetesCluster#cpu_manager_policy}.
        :param image_gc_high_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_gc_high_threshold KubernetesCluster#image_gc_high_threshold}.
        :param image_gc_low_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#image_gc_low_threshold KubernetesCluster#image_gc_low_threshold}.
        :param pod_max_pid: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_max_pid KubernetesCluster#pod_max_pid}.
        :param topology_manager_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#topology_manager_policy KubernetesCluster#topology_manager_policy}.
        '''
        value = KubernetesClusterDefaultNodePoolKubeletConfig(
            allowed_unsafe_sysctls=allowed_unsafe_sysctls,
            container_log_max_line=container_log_max_line,
            container_log_max_size_mb=container_log_max_size_mb,
            cpu_cfs_quota_enabled=cpu_cfs_quota_enabled,
            cpu_cfs_quota_period=cpu_cfs_quota_period,
            cpu_manager_policy=cpu_manager_policy,
            image_gc_high_threshold=image_gc_high_threshold,
            image_gc_low_threshold=image_gc_low_threshold,
            pod_max_pid=pod_max_pid,
            topology_manager_policy=topology_manager_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putKubeletConfig", [value]))

    @jsii.member(jsii_name="putLinuxOsConfig")
    def put_linux_os_config(
        self,
        *,
        swap_file_size_mb: typing.Optional[jsii.Number] = None,
        sysctl_config: typing.Optional[typing.Union[KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        transparent_huge_page_defrag: typing.Optional[builtins.str] = None,
        transparent_huge_page_enabled: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param swap_file_size_mb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#swap_file_size_mb KubernetesCluster#swap_file_size_mb}.
        :param sysctl_config: sysctl_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#sysctl_config KubernetesCluster#sysctl_config}
        :param transparent_huge_page_defrag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#transparent_huge_page_defrag KubernetesCluster#transparent_huge_page_defrag}.
        :param transparent_huge_page_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#transparent_huge_page_enabled KubernetesCluster#transparent_huge_page_enabled}.
        '''
        value = KubernetesClusterDefaultNodePoolLinuxOsConfig(
            swap_file_size_mb=swap_file_size_mb,
            sysctl_config=sysctl_config,
            transparent_huge_page_defrag=transparent_huge_page_defrag,
            transparent_huge_page_enabled=transparent_huge_page_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putLinuxOsConfig", [value]))

    @jsii.member(jsii_name="putUpgradeSettings")
    def put_upgrade_settings(self, *, max_surge: builtins.str) -> None:
        '''
        :param max_surge: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_surge KubernetesCluster#max_surge}.
        '''
        value = KubernetesClusterDefaultNodePoolUpgradeSettings(max_surge=max_surge)

        return typing.cast(None, jsii.invoke(self, "putUpgradeSettings", [value]))

    @jsii.member(jsii_name="resetCapacityReservationGroupId")
    def reset_capacity_reservation_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityReservationGroupId", []))

    @jsii.member(jsii_name="resetCustomCaTrustEnabled")
    def reset_custom_ca_trust_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomCaTrustEnabled", []))

    @jsii.member(jsii_name="resetEnableAutoScaling")
    def reset_enable_auto_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAutoScaling", []))

    @jsii.member(jsii_name="resetEnableHostEncryption")
    def reset_enable_host_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHostEncryption", []))

    @jsii.member(jsii_name="resetEnableNodePublicIp")
    def reset_enable_node_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNodePublicIp", []))

    @jsii.member(jsii_name="resetFipsEnabled")
    def reset_fips_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFipsEnabled", []))

    @jsii.member(jsii_name="resetHostGroupId")
    def reset_host_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostGroupId", []))

    @jsii.member(jsii_name="resetKubeletConfig")
    def reset_kubelet_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubeletConfig", []))

    @jsii.member(jsii_name="resetKubeletDiskType")
    def reset_kubelet_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubeletDiskType", []))

    @jsii.member(jsii_name="resetLinuxOsConfig")
    def reset_linux_os_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinuxOsConfig", []))

    @jsii.member(jsii_name="resetMaxCount")
    def reset_max_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxCount", []))

    @jsii.member(jsii_name="resetMaxPods")
    def reset_max_pods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPods", []))

    @jsii.member(jsii_name="resetMessageOfTheDay")
    def reset_message_of_the_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageOfTheDay", []))

    @jsii.member(jsii_name="resetMinCount")
    def reset_min_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCount", []))

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @jsii.member(jsii_name="resetNodeLabels")
    def reset_node_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeLabels", []))

    @jsii.member(jsii_name="resetNodePublicIpPrefixId")
    def reset_node_public_ip_prefix_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePublicIpPrefixId", []))

    @jsii.member(jsii_name="resetNodeTaints")
    def reset_node_taints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeTaints", []))

    @jsii.member(jsii_name="resetOnlyCriticalAddonsEnabled")
    def reset_only_critical_addons_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlyCriticalAddonsEnabled", []))

    @jsii.member(jsii_name="resetOrchestratorVersion")
    def reset_orchestrator_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrchestratorVersion", []))

    @jsii.member(jsii_name="resetOsDiskSizeGb")
    def reset_os_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDiskSizeGb", []))

    @jsii.member(jsii_name="resetOsDiskType")
    def reset_os_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDiskType", []))

    @jsii.member(jsii_name="resetOsSku")
    def reset_os_sku(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsSku", []))

    @jsii.member(jsii_name="resetPodSubnetId")
    def reset_pod_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodSubnetId", []))

    @jsii.member(jsii_name="resetProximityPlacementGroupId")
    def reset_proximity_placement_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProximityPlacementGroupId", []))

    @jsii.member(jsii_name="resetScaleDownMode")
    def reset_scale_down_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDownMode", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUltraSsdEnabled")
    def reset_ultra_ssd_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUltraSsdEnabled", []))

    @jsii.member(jsii_name="resetUpgradeSettings")
    def reset_upgrade_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpgradeSettings", []))

    @jsii.member(jsii_name="resetVnetSubnetId")
    def reset_vnet_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVnetSubnetId", []))

    @jsii.member(jsii_name="resetWorkloadRuntime")
    def reset_workload_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadRuntime", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

    @builtins.property
    @jsii.member(jsii_name="kubeletConfig")
    def kubelet_config(
        self,
    ) -> KubernetesClusterDefaultNodePoolKubeletConfigOutputReference:
        return typing.cast(KubernetesClusterDefaultNodePoolKubeletConfigOutputReference, jsii.get(self, "kubeletConfig"))

    @builtins.property
    @jsii.member(jsii_name="linuxOsConfig")
    def linux_os_config(
        self,
    ) -> KubernetesClusterDefaultNodePoolLinuxOsConfigOutputReference:
        return typing.cast(KubernetesClusterDefaultNodePoolLinuxOsConfigOutputReference, jsii.get(self, "linuxOsConfig"))

    @builtins.property
    @jsii.member(jsii_name="upgradeSettings")
    def upgrade_settings(
        self,
    ) -> "KubernetesClusterDefaultNodePoolUpgradeSettingsOutputReference":
        return typing.cast("KubernetesClusterDefaultNodePoolUpgradeSettingsOutputReference", jsii.get(self, "upgradeSettings"))

    @builtins.property
    @jsii.member(jsii_name="capacityReservationGroupIdInput")
    def capacity_reservation_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityReservationGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customCaTrustEnabledInput")
    def custom_ca_trust_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customCaTrustEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAutoScalingInput")
    def enable_auto_scaling_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAutoScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHostEncryptionInput")
    def enable_host_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHostEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNodePublicIpInput")
    def enable_node_public_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNodePublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="fipsEnabledInput")
    def fips_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fipsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hostGroupIdInput")
    def host_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="kubeletConfigInput")
    def kubelet_config_input(
        self,
    ) -> typing.Optional[KubernetesClusterDefaultNodePoolKubeletConfig]:
        return typing.cast(typing.Optional[KubernetesClusterDefaultNodePoolKubeletConfig], jsii.get(self, "kubeletConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="kubeletDiskTypeInput")
    def kubelet_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeletDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="linuxOsConfigInput")
    def linux_os_config_input(
        self,
    ) -> typing.Optional[KubernetesClusterDefaultNodePoolLinuxOsConfig]:
        return typing.cast(typing.Optional[KubernetesClusterDefaultNodePoolLinuxOsConfig], jsii.get(self, "linuxOsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="maxCountInput")
    def max_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsInput")
    def max_pods_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsInput"))

    @builtins.property
    @jsii.member(jsii_name="messageOfTheDayInput")
    def message_of_the_day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageOfTheDayInput"))

    @builtins.property
    @jsii.member(jsii_name="minCountInput")
    def min_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeLabelsInput")
    def node_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "nodeLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpPrefixIdInput")
    def node_public_ip_prefix_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodePublicIpPrefixIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTaintsInput")
    def node_taints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nodeTaintsInput"))

    @builtins.property
    @jsii.member(jsii_name="onlyCriticalAddonsEnabledInput")
    def only_critical_addons_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onlyCriticalAddonsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="orchestratorVersionInput")
    def orchestrator_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orchestratorVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskSizeGbInput")
    def os_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "osDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskTypeInput")
    def os_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="osSkuInput")
    def os_sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osSkuInput"))

    @builtins.property
    @jsii.member(jsii_name="podSubnetIdInput")
    def pod_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityPlacementGroupIdInput")
    def proximity_placement_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proximityPlacementGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownModeInput")
    def scale_down_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scaleDownModeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="ultraSsdEnabledInput")
    def ultra_ssd_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ultraSsdEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="upgradeSettingsInput")
    def upgrade_settings_input(
        self,
    ) -> typing.Optional["KubernetesClusterDefaultNodePoolUpgradeSettings"]:
        return typing.cast(typing.Optional["KubernetesClusterDefaultNodePoolUpgradeSettings"], jsii.get(self, "upgradeSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetSubnetIdInput")
    def vnet_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vnetSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadRuntimeInput")
    def workload_runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadRuntimeInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityReservationGroupId")
    def capacity_reservation_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityReservationGroupId"))

    @capacity_reservation_group_id.setter
    def capacity_reservation_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc04931b19a071905f9cb3667f450373855a6b61f03c5e217c1f981f2c6517e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityReservationGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="customCaTrustEnabled")
    def custom_ca_trust_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customCaTrustEnabled"))

    @custom_ca_trust_enabled.setter
    def custom_ca_trust_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb19d08e6d45526869df1bd900950da119e036428856908186ffa9fb4d253525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customCaTrustEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="enableAutoScaling")
    def enable_auto_scaling(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAutoScaling"))

    @enable_auto_scaling.setter
    def enable_auto_scaling(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58386f1d80d82c49633255324888d6dd3aa901c4028705db77f3acdb4b686d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutoScaling", value)

    @builtins.property
    @jsii.member(jsii_name="enableHostEncryption")
    def enable_host_encryption(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHostEncryption"))

    @enable_host_encryption.setter
    def enable_host_encryption(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19ef0040f59768fe561e3465ccbfbb717c5466032961773a0da0a50a3a1d890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHostEncryption", value)

    @builtins.property
    @jsii.member(jsii_name="enableNodePublicIp")
    def enable_node_public_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableNodePublicIp"))

    @enable_node_public_ip.setter
    def enable_node_public_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136b7d6bc114a341cce30b7977e029925cc1e7dc931584dad7c0c25a1376c6c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNodePublicIp", value)

    @builtins.property
    @jsii.member(jsii_name="fipsEnabled")
    def fips_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fipsEnabled"))

    @fips_enabled.setter
    def fips_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba07c9330a54b3cc73ae3d87de5064037de5889841a21b815f81fe303568c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fipsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="hostGroupId")
    def host_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostGroupId"))

    @host_group_id.setter
    def host_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ba753d42db56769bdd51f8fecfba0281d67a50bbaf864dbb40ede032d3d9649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="kubeletDiskType")
    def kubelet_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubeletDiskType"))

    @kubelet_disk_type.setter
    def kubelet_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974ec59932d0645542779d0de4466e10231bd31a63a4f57026228d288c22b807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubeletDiskType", value)

    @builtins.property
    @jsii.member(jsii_name="maxCount")
    def max_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxCount"))

    @max_count.setter
    def max_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a53b8462abf8dcbbad396f537102da96abe6e656dfd5c68303a2aedf2a5890f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxCount", value)

    @builtins.property
    @jsii.member(jsii_name="maxPods")
    def max_pods(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPods"))

    @max_pods.setter
    def max_pods(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ca5117fbe35aa80bfe0c20da47761868e3d6c44aeaf4bfa7a5f881ea5f119e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPods", value)

    @builtins.property
    @jsii.member(jsii_name="messageOfTheDay")
    def message_of_the_day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageOfTheDay"))

    @message_of_the_day.setter
    def message_of_the_day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44b513163d177b1c69847dc399aacd07b99b101137dc74a662659fc632ff408c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageOfTheDay", value)

    @builtins.property
    @jsii.member(jsii_name="minCount")
    def min_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minCount"))

    @min_count.setter
    def min_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39acbe85a98422f361b98810e8b81d82a1fc67e1642c97597ea9a3401f219825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCount", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef5de2e71fafbdebb5d47a255d31dffcf486fb2b7facc46dc0806896e556719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d937615f529b76811017519dff0c3cd46e2863f3f77a96465c56e9d67d829f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value)

    @builtins.property
    @jsii.member(jsii_name="nodeLabels")
    def node_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nodeLabels"))

    @node_labels.setter
    def node_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec79f7d1402cf8ab5aa05c460266d574b3310e0b09ad201c016c08a1360bc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeLabels", value)

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpPrefixId")
    def node_public_ip_prefix_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodePublicIpPrefixId"))

    @node_public_ip_prefix_id.setter
    def node_public_ip_prefix_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b589d6a44660391076b19d22e0693cc865c84e926f3b3c62f81a152a3e071c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePublicIpPrefixId", value)

    @builtins.property
    @jsii.member(jsii_name="nodeTaints")
    def node_taints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nodeTaints"))

    @node_taints.setter
    def node_taints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8af03e4ecb5462fbda675b53d648aae49e124980a8d8b9c2fc7aef18531f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTaints", value)

    @builtins.property
    @jsii.member(jsii_name="onlyCriticalAddonsEnabled")
    def only_critical_addons_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onlyCriticalAddonsEnabled"))

    @only_critical_addons_enabled.setter
    def only_critical_addons_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc3f466b515f750600aa5adcbdb54b5e4102a3cf6e5cdd7c8b778510dfd327a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyCriticalAddonsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="orchestratorVersion")
    def orchestrator_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orchestratorVersion"))

    @orchestrator_version.setter
    def orchestrator_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3181bf1ab5a4afe19e421c2a30599182b133e754d8303e3a3e2c4aab4e9f242f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orchestratorVersion", value)

    @builtins.property
    @jsii.member(jsii_name="osDiskSizeGb")
    def os_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "osDiskSizeGb"))

    @os_disk_size_gb.setter
    def os_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc32a97ed9766d42ce65a80759cef14234b6eec6034d28319e58a3ae4e418374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDiskSizeGb", value)

    @builtins.property
    @jsii.member(jsii_name="osDiskType")
    def os_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDiskType"))

    @os_disk_type.setter
    def os_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9606a87195767eea22661c4a3bdaa0ab882d0e141a5fd2fb3bcc0d009b43c617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDiskType", value)

    @builtins.property
    @jsii.member(jsii_name="osSku")
    def os_sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osSku"))

    @os_sku.setter
    def os_sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d36a79540c9cb9804da74cb1e2bf795466e8778cd28f991f5913ec9b799d479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osSku", value)

    @builtins.property
    @jsii.member(jsii_name="podSubnetId")
    def pod_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podSubnetId"))

    @pod_subnet_id.setter
    def pod_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c25e8639549a7683664ffd913536ca0bef87029760377701f1874a7feb4c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podSubnetId", value)

    @builtins.property
    @jsii.member(jsii_name="proximityPlacementGroupId")
    def proximity_placement_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proximityPlacementGroupId"))

    @proximity_placement_group_id.setter
    def proximity_placement_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba125a1e127d4d978535d1c9957956869675ee8235ebb9c9c0ea796c6067f9b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proximityPlacementGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="scaleDownMode")
    def scale_down_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scaleDownMode"))

    @scale_down_mode.setter
    def scale_down_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11c98095c81f253787a416eb64f9571ce8203a08aafff47b29f7d76eadc2b14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownMode", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fc2b558c3aa7cbf37a0896c95a61c5729289ca5259291f5a4bb997568bdcad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e700fc2c79b6855b103d48ab98526c81e54a1cc7f494db2f83bfeb254194f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="ultraSsdEnabled")
    def ultra_ssd_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ultraSsdEnabled"))

    @ultra_ssd_enabled.setter
    def ultra_ssd_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce2b6af8826dbb2059ef9a2d44d42e412e98a85f22309538040b3942272c26e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ultraSsdEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c672ba1b67e3df8e020f8595ddf621ac74814338643da2de2a13a4d4db926ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value)

    @builtins.property
    @jsii.member(jsii_name="vnetSubnetId")
    def vnet_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vnetSubnetId"))

    @vnet_subnet_id.setter
    def vnet_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6563f4f702a6ee485c5e295f9db0f5933e16c9d86eda88de7f8c6eb60054c1e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vnetSubnetId", value)

    @builtins.property
    @jsii.member(jsii_name="workloadRuntime")
    def workload_runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadRuntime"))

    @workload_runtime.setter
    def workload_runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36911dee20ff97d0e9b133472ace8e324cd4f5a8d703aec36c1830fdbe1a8418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadRuntime", value)

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0de2703cc4c779950056ddf82e5546be9611f274eb2d615111daf976643eb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterDefaultNodePool]:
        return typing.cast(typing.Optional[KubernetesClusterDefaultNodePool], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterDefaultNodePool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86285f21bb79254cee2459ce790470bb88bf7e1dbd80d8c5cd3996e8e3a93aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterDefaultNodePoolUpgradeSettings",
    jsii_struct_bases=[],
    name_mapping={"max_surge": "maxSurge"},
)
class KubernetesClusterDefaultNodePoolUpgradeSettings:
    def __init__(self, *, max_surge: builtins.str) -> None:
        '''
        :param max_surge: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_surge KubernetesCluster#max_surge}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae54277c4d532648f73822e0310f438ccece2a230bfabfbab63790f5296bf61)
            check_type(argname="argument max_surge", value=max_surge, expected_type=type_hints["max_surge"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_surge": max_surge,
        }

    @builtins.property
    def max_surge(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#max_surge KubernetesCluster#max_surge}.'''
        result = self._values.get("max_surge")
        assert result is not None, "Required property 'max_surge' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterDefaultNodePoolUpgradeSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterDefaultNodePoolUpgradeSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterDefaultNodePoolUpgradeSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b83bac82fcde5a76cd3520a412118e4b3d5618a5d2291051fcbddfb60887cff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxSurgeInput")
    def max_surge_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxSurgeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSurge")
    def max_surge(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxSurge"))

    @max_surge.setter
    def max_surge(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da6d8625a5823d2bd06afeb7278b48394799cbe912d8afa4ae288267781912c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSurge", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterDefaultNodePoolUpgradeSettings]:
        return typing.cast(typing.Optional[KubernetesClusterDefaultNodePoolUpgradeSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterDefaultNodePoolUpgradeSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7fe7bb2bb68fe30013bc109a0ccbe9bed5140dcbd37f6717720b11eac9ecbd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterHttpProxyConfig",
    jsii_struct_bases=[],
    name_mapping={
        "http_proxy": "httpProxy",
        "https_proxy": "httpsProxy",
        "no_proxy": "noProxy",
        "trusted_ca": "trustedCa",
    },
)
class KubernetesClusterHttpProxyConfig:
    def __init__(
        self,
        *,
        http_proxy: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_ca: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param http_proxy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#http_proxy KubernetesCluster#http_proxy}.
        :param https_proxy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#https_proxy KubernetesCluster#https_proxy}.
        :param no_proxy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#no_proxy KubernetesCluster#no_proxy}.
        :param trusted_ca: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#trusted_ca KubernetesCluster#trusted_ca}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af0909251cf11f8f833f74912bb6bbae414ce55bdff403d8ac797fa6872e50e)
            check_type(argname="argument http_proxy", value=http_proxy, expected_type=type_hints["http_proxy"])
            check_type(argname="argument https_proxy", value=https_proxy, expected_type=type_hints["https_proxy"])
            check_type(argname="argument no_proxy", value=no_proxy, expected_type=type_hints["no_proxy"])
            check_type(argname="argument trusted_ca", value=trusted_ca, expected_type=type_hints["trusted_ca"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_proxy is not None:
            self._values["http_proxy"] = http_proxy
        if https_proxy is not None:
            self._values["https_proxy"] = https_proxy
        if no_proxy is not None:
            self._values["no_proxy"] = no_proxy
        if trusted_ca is not None:
            self._values["trusted_ca"] = trusted_ca

    @builtins.property
    def http_proxy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#http_proxy KubernetesCluster#http_proxy}.'''
        result = self._values.get("http_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_proxy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#https_proxy KubernetesCluster#https_proxy}.'''
        result = self._values.get("https_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_proxy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#no_proxy KubernetesCluster#no_proxy}.'''
        result = self._values.get("no_proxy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trusted_ca(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#trusted_ca KubernetesCluster#trusted_ca}.'''
        result = self._values.get("trusted_ca")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterHttpProxyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterHttpProxyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterHttpProxyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b955efe61167f21d4a8fc8a7f674636ed28f2137ebe2da40fdd8497fc756b56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHttpProxy")
    def reset_http_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpProxy", []))

    @jsii.member(jsii_name="resetHttpsProxy")
    def reset_https_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsProxy", []))

    @jsii.member(jsii_name="resetNoProxy")
    def reset_no_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoProxy", []))

    @jsii.member(jsii_name="resetTrustedCa")
    def reset_trusted_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedCa", []))

    @builtins.property
    @jsii.member(jsii_name="httpProxyInput")
    def http_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsProxyInput")
    def https_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="noProxyInput")
    def no_proxy_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "noProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedCaInput")
    def trusted_ca_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustedCaInput"))

    @builtins.property
    @jsii.member(jsii_name="httpProxy")
    def http_proxy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpProxy"))

    @http_proxy.setter
    def http_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae7ec78e4b5f51056f77af899f27aa2ce67d4d43456590fc5ea4f91213b53f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpProxy", value)

    @builtins.property
    @jsii.member(jsii_name="httpsProxy")
    def https_proxy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsProxy"))

    @https_proxy.setter
    def https_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff6366db5353fe0c24a237af0a17c06c49cfaf278b3d3a15801d772a3b5beaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsProxy", value)

    @builtins.property
    @jsii.member(jsii_name="noProxy")
    def no_proxy(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "noProxy"))

    @no_proxy.setter
    def no_proxy(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa319b54c9e47a23e844b487d974b4b500da7a97e4598569d8a6abf6cffe6af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noProxy", value)

    @builtins.property
    @jsii.member(jsii_name="trustedCa")
    def trusted_ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustedCa"))

    @trusted_ca.setter
    def trusted_ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e5d26c36626247dc9dc0ef5dce656b4c17ceef33460cfc2f021becba14697ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedCa", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterHttpProxyConfig]:
        return typing.cast(typing.Optional[KubernetesClusterHttpProxyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterHttpProxyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21bd20d24a411b7662822103b7979090bcf1b19bc74004a67b005e73c8ed1cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class KubernetesClusterIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#type KubernetesCluster#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#identity_ids KubernetesCluster#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebbe8d1d175e77d27b65e2cbdc93fd1d7e8243f0fe7d751a852050d2d0085bd)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#type KubernetesCluster#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#identity_ids KubernetesCluster#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aafd01285533951e1fd23f660a7261a6ce3044279ec40b56acf251b060cbcfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fd71ddad3995b4079c5f844930a44e5ca04c2c776312bba7997a9a28051d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9e7582cf43b0f8f1cc94d10ecb6bf2d977424399895cb6f3c03e76660ffc38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterIdentity]:
        return typing.cast(typing.Optional[KubernetesClusterIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[KubernetesClusterIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697893a1cc0de1b6d5db2d06732d91a8880b12f39eae0875e7fd9b2e2386a455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterIngressApplicationGateway",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_id": "gatewayId",
        "gateway_name": "gatewayName",
        "subnet_cidr": "subnetCidr",
        "subnet_id": "subnetId",
    },
)
class KubernetesClusterIngressApplicationGateway:
    def __init__(
        self,
        *,
        gateway_id: typing.Optional[builtins.str] = None,
        gateway_name: typing.Optional[builtins.str] = None,
        subnet_cidr: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gateway_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#gateway_id KubernetesCluster#gateway_id}.
        :param gateway_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#gateway_name KubernetesCluster#gateway_name}.
        :param subnet_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#subnet_cidr KubernetesCluster#subnet_cidr}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#subnet_id KubernetesCluster#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52b210b26014cc6ce6aa05405d2c165f3243010a1f89465def1b3c2b2b0e96b)
            check_type(argname="argument gateway_id", value=gateway_id, expected_type=type_hints["gateway_id"])
            check_type(argname="argument gateway_name", value=gateway_name, expected_type=type_hints["gateway_name"])
            check_type(argname="argument subnet_cidr", value=subnet_cidr, expected_type=type_hints["subnet_cidr"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gateway_id is not None:
            self._values["gateway_id"] = gateway_id
        if gateway_name is not None:
            self._values["gateway_name"] = gateway_name
        if subnet_cidr is not None:
            self._values["subnet_cidr"] = subnet_cidr
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def gateway_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#gateway_id KubernetesCluster#gateway_id}.'''
        result = self._values.get("gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#gateway_name KubernetesCluster#gateway_name}.'''
        result = self._values.get("gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#subnet_cidr KubernetesCluster#subnet_cidr}.'''
        result = self._values.get("subnet_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#subnet_id KubernetesCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterIngressApplicationGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentity",
    jsii_struct_bases=[],
    name_mapping={},
)
class KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0557bb63ffe6bdb4303604a8df18213ace0914901bb1d1a32db671083b6bac50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a470fddd7a44b95a1a44ed49327815df7ce8b52560f1bbbbcf28954240075a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8211ca2a3a0e6f146cea8c721b8676dfc597ba03a7e0ea2f561c18437a293946)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90243a83d738d348fde91655aaae204dea9fa3563cd3d581e93153686e6c6572)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf990ba44d217e33b311131e7dcaab2a89805f353c6689ca332c783950e30f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fa4774773e9e102d5949ac2788f44ccf43059ee83ef664075f45172b095d88a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentityId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentity]:
        return typing.cast(typing.Optional[KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6653c2b845bdf4a522f690370f5a108da7d611eb37f3ca7ee95b062a7f29ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KubernetesClusterIngressApplicationGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterIngressApplicationGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__556844747c742dbbea413143a04daf04bf6847749a6e38a9b4f79d8526ceb1cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGatewayId")
    def reset_gateway_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayId", []))

    @jsii.member(jsii_name="resetGatewayName")
    def reset_gateway_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayName", []))

    @jsii.member(jsii_name="resetSubnetCidr")
    def reset_subnet_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetCidr", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="effectiveGatewayId")
    def effective_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveGatewayId"))

    @builtins.property
    @jsii.member(jsii_name="ingressApplicationGatewayIdentity")
    def ingress_application_gateway_identity(
        self,
    ) -> KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentityList:
        return typing.cast(KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentityList, jsii.get(self, "ingressApplicationGatewayIdentity"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIdInput")
    def gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayNameInput")
    def gateway_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetCidrInput")
    def subnet_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayId")
    def gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayId"))

    @gateway_id.setter
    def gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3198dc068fdac2568df75bc8300cc5526a7fc46672d22a3830f163874b81f3ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayId", value)

    @builtins.property
    @jsii.member(jsii_name="gatewayName")
    def gateway_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayName"))

    @gateway_name.setter
    def gateway_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bcf05d0ad050301303f4d7dbec2db13d1cb023d912d19507987c41e46c7a84d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayName", value)

    @builtins.property
    @jsii.member(jsii_name="subnetCidr")
    def subnet_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetCidr"))

    @subnet_cidr.setter
    def subnet_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7056c162a622665a773863617d74da0899810e7e1d30e1bc41d51fc1880610b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetCidr", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31de106c55cc5f777f7d86adc45eb0f8445c439423df68369fbe0fdef00d2830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterIngressApplicationGateway]:
        return typing.cast(typing.Optional[KubernetesClusterIngressApplicationGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterIngressApplicationGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0575b484233cc2c2eac990d809d2047467054d1247dfb97d7021abc6f7ccc22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKeyVaultSecretsProvider",
    jsii_struct_bases=[],
    name_mapping={
        "secret_rotation_enabled": "secretRotationEnabled",
        "secret_rotation_interval": "secretRotationInterval",
    },
)
class KubernetesClusterKeyVaultSecretsProvider:
    def __init__(
        self,
        *,
        secret_rotation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret_rotation_interval: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_rotation_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#secret_rotation_enabled KubernetesCluster#secret_rotation_enabled}.
        :param secret_rotation_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#secret_rotation_interval KubernetesCluster#secret_rotation_interval}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867f4869c30749b75f936a03661ecc4157644a6e5d891c1b77e4902317813611)
            check_type(argname="argument secret_rotation_enabled", value=secret_rotation_enabled, expected_type=type_hints["secret_rotation_enabled"])
            check_type(argname="argument secret_rotation_interval", value=secret_rotation_interval, expected_type=type_hints["secret_rotation_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if secret_rotation_enabled is not None:
            self._values["secret_rotation_enabled"] = secret_rotation_enabled
        if secret_rotation_interval is not None:
            self._values["secret_rotation_interval"] = secret_rotation_interval

    @builtins.property
    def secret_rotation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#secret_rotation_enabled KubernetesCluster#secret_rotation_enabled}.'''
        result = self._values.get("secret_rotation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret_rotation_interval(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#secret_rotation_interval KubernetesCluster#secret_rotation_interval}.'''
        result = self._values.get("secret_rotation_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterKeyVaultSecretsProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterKeyVaultSecretsProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKeyVaultSecretsProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33eb5b4cdf75a282ef98182fb1e401be7f86fcdc9fb5b3428e13670a75e522ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecretRotationEnabled")
    def reset_secret_rotation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretRotationEnabled", []))

    @jsii.member(jsii_name="resetSecretRotationInterval")
    def reset_secret_rotation_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretRotationInterval", []))

    @builtins.property
    @jsii.member(jsii_name="secretIdentity")
    def secret_identity(
        self,
    ) -> "KubernetesClusterKeyVaultSecretsProviderSecretIdentityList":
        return typing.cast("KubernetesClusterKeyVaultSecretsProviderSecretIdentityList", jsii.get(self, "secretIdentity"))

    @builtins.property
    @jsii.member(jsii_name="secretRotationEnabledInput")
    def secret_rotation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secretRotationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="secretRotationIntervalInput")
    def secret_rotation_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretRotationIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="secretRotationEnabled")
    def secret_rotation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secretRotationEnabled"))

    @secret_rotation_enabled.setter
    def secret_rotation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b709a391b9660c651ce93ef4c2d02f252281de6e6f69a770239e0ae04ebcc11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretRotationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="secretRotationInterval")
    def secret_rotation_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretRotationInterval"))

    @secret_rotation_interval.setter
    def secret_rotation_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c426d1c60afd436b4622d503aa92e451e6a23116b13e90ef03882e1bb4c1cfe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretRotationInterval", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterKeyVaultSecretsProvider]:
        return typing.cast(typing.Optional[KubernetesClusterKeyVaultSecretsProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterKeyVaultSecretsProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e4c0e2256e3789519eb19ba6bce075ee52cd1d10e19791265877182e771926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKeyVaultSecretsProviderSecretIdentity",
    jsii_struct_bases=[],
    name_mapping={},
)
class KubernetesClusterKeyVaultSecretsProviderSecretIdentity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterKeyVaultSecretsProviderSecretIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterKeyVaultSecretsProviderSecretIdentityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKeyVaultSecretsProviderSecretIdentityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dacf0a744dc091da4266de3d361c1b1e2ea24834a4289327c27defe20f0ae94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KubernetesClusterKeyVaultSecretsProviderSecretIdentityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86ad23778e3c0d75fddb412711bc55eef55d60e2d07862e836563cadf0ed162)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesClusterKeyVaultSecretsProviderSecretIdentityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc5a925cfe25b32d5c72701cdcf4b61c9afa52e6763fa3521ffd3965a564a74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f11fcb0066d2cb3435900edb1756802d3b6673c71d88544b1257219946cf4cd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2301ff10ebbe02f7acacab35d231602de0512e34abaaf3496f46f78c0f24943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class KubernetesClusterKeyVaultSecretsProviderSecretIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKeyVaultSecretsProviderSecretIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__499534eb3a36f01ed7d4ab9f76d516bd39b310546b22ac7eedfd6e9db2ce3614)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentityId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterKeyVaultSecretsProviderSecretIdentity]:
        return typing.cast(typing.Optional[KubernetesClusterKeyVaultSecretsProviderSecretIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterKeyVaultSecretsProviderSecretIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b397bff95d1e75db11931c343cd0d03893c0da2523cfc2d736986ac3561650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKubeAdminConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class KubernetesClusterKubeAdminConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterKubeAdminConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterKubeAdminConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKubeAdminConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15f4b0a335823aefa8141d52cb5ac0fa9e4af8470d315ad6d1322e6fcc002ca9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KubernetesClusterKubeAdminConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ec5295dbf6d5b2e8c29d44f8044d383ebaadc804691a272e94b6ff44cb8615)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesClusterKubeAdminConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec770430e71abdc5c8306ce053a0ad10544b4e59c48c1325c10123d89adae1b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d7e0490ceacd4c513ad62f16da90f3ef59a8c45fcf762bebc14f4eeb9788cf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdd1622b9da0cf110e1d825b85432ce8589bbe5588140e201a43d754a2c18114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class KubernetesClusterKubeAdminConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKubeAdminConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a45428d6571444f3aa2c411f2938c9fb85fcdd3fd7583b559977f47777bc20f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @builtins.property
    @jsii.member(jsii_name="clusterCaCertificate")
    def cluster_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterCaCertificate"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterKubeAdminConfig]:
        return typing.cast(typing.Optional[KubernetesClusterKubeAdminConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterKubeAdminConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2af61b3248fa6317c64a40e8e1d8e5b247b321ea23111bf031e3ab8a9164ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKubeConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class KubernetesClusterKubeConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterKubeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterKubeConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKubeConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d276d4ec8be028ada289f8089ada085ec7742ccd61e134f93c517ed25148ff05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "KubernetesClusterKubeConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__936d94ebf66b3e56c8bcc7f442c15cb7b34db056842ffba91ecec6275d1e689d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesClusterKubeConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b55961579f2e9ea9492b86ec0458f7a78ccdbfa282de176dde5ae737939060)
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
            type_hints = typing.get_type_hints(_typecheckingstub__021a44434bbd2a49203f30a8df1af18787284e52d3957dd0c2a14ae9581ac55a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17853465f08ea6a423706ded228accafabc5bae7c6a6d737c7effb42f426ac0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class KubernetesClusterKubeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKubeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a4423b52fc19fd14ee048ed7b8644c39da5a95a7731ce631496940c4b9b16d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @builtins.property
    @jsii.member(jsii_name="clusterCaCertificate")
    def cluster_ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterCaCertificate"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterKubeConfig]:
        return typing.cast(typing.Optional[KubernetesClusterKubeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterKubeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670869fb9c13c7f7c257f8dca1634b43d333c62344cbec1d52c69327be0f1c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKubeletIdentity",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "object_id": "objectId",
        "user_assigned_identity_id": "userAssignedIdentityId",
    },
)
class KubernetesClusterKubeletIdentity:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        object_id: typing.Optional[builtins.str] = None,
        user_assigned_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_id KubernetesCluster#client_id}.
        :param object_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#object_id KubernetesCluster#object_id}.
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#user_assigned_identity_id KubernetesCluster#user_assigned_identity_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__596030cd7f36ba076f24601952972881a2910d69a8d725842f4b07d1f2054041)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument user_assigned_identity_id", value=user_assigned_identity_id, expected_type=type_hints["user_assigned_identity_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if object_id is not None:
            self._values["object_id"] = object_id
        if user_assigned_identity_id is not None:
            self._values["user_assigned_identity_id"] = user_assigned_identity_id

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_id KubernetesCluster#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#object_id KubernetesCluster#object_id}.'''
        result = self._values.get("object_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_assigned_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#user_assigned_identity_id KubernetesCluster#user_assigned_identity_id}.'''
        result = self._values.get("user_assigned_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterKubeletIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterKubeletIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterKubeletIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec5372b0b90633de07efe4c865397d55dd73c31f0103ecd673a10382f5a416e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetObjectId")
    def reset_object_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectId", []))

    @jsii.member(jsii_name="resetUserAssignedIdentityId")
    def reset_user_assigned_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAssignedIdentityId", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityIdInput")
    def user_assigned_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAssignedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a10adebfd1950f06bbdc1098c7b59a98fa32d83f75ec988c5b44ba7d644a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c75e4c5e85cd19a2f808e187a10d70103da4dfa7d5973f37b3153f6b11ace5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value)

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentityId"))

    @user_assigned_identity_id.setter
    def user_assigned_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c9bef3daf9609d108c85868db9196e23d1b15bab226ef3dcbd2755ac0118ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentityId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterKubeletIdentity]:
        return typing.cast(typing.Optional[KubernetesClusterKubeletIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterKubeletIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57c82e8a114c51b5f81163938be6ca7a883cc569b04eee15649dfba8d6a59a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterLinuxProfile",
    jsii_struct_bases=[],
    name_mapping={"admin_username": "adminUsername", "ssh_key": "sshKey"},
)
class KubernetesClusterLinuxProfile:
    def __init__(
        self,
        *,
        admin_username: builtins.str,
        ssh_key: typing.Union["KubernetesClusterLinuxProfileSshKey", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_username KubernetesCluster#admin_username}.
        :param ssh_key: ssh_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ssh_key KubernetesCluster#ssh_key}
        '''
        if isinstance(ssh_key, dict):
            ssh_key = KubernetesClusterLinuxProfileSshKey(**ssh_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557afa298a21f5e3e9235bb451faa98d7a30ffb6958a3f5d66eb25b0fd39f109)
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument ssh_key", value=ssh_key, expected_type=type_hints["ssh_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_username": admin_username,
            "ssh_key": ssh_key,
        }

    @builtins.property
    def admin_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_username KubernetesCluster#admin_username}.'''
        result = self._values.get("admin_username")
        assert result is not None, "Required property 'admin_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_key(self) -> "KubernetesClusterLinuxProfileSshKey":
        '''ssh_key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ssh_key KubernetesCluster#ssh_key}
        '''
        result = self._values.get("ssh_key")
        assert result is not None, "Required property 'ssh_key' is missing"
        return typing.cast("KubernetesClusterLinuxProfileSshKey", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterLinuxProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterLinuxProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterLinuxProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__412104e73079dd5adca68d7c6853b89d98144bfa51090089418af31b0a8f61a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSshKey")
    def put_ssh_key(self, *, key_data: builtins.str) -> None:
        '''
        :param key_data: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#key_data KubernetesCluster#key_data}.
        '''
        value = KubernetesClusterLinuxProfileSshKey(key_data=key_data)

        return typing.cast(None, jsii.invoke(self, "putSshKey", [value]))

    @builtins.property
    @jsii.member(jsii_name="sshKey")
    def ssh_key(self) -> "KubernetesClusterLinuxProfileSshKeyOutputReference":
        return typing.cast("KubernetesClusterLinuxProfileSshKeyOutputReference", jsii.get(self, "sshKey"))

    @builtins.property
    @jsii.member(jsii_name="adminUsernameInput")
    def admin_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="sshKeyInput")
    def ssh_key_input(self) -> typing.Optional["KubernetesClusterLinuxProfileSshKey"]:
        return typing.cast(typing.Optional["KubernetesClusterLinuxProfileSshKey"], jsii.get(self, "sshKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsername")
    def admin_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminUsername"))

    @admin_username.setter
    def admin_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53837ba056ab9edf7bca665bba1311e99428141141d1a3ed1637569ad475f828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUsername", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterLinuxProfile]:
        return typing.cast(typing.Optional[KubernetesClusterLinuxProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterLinuxProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694f22a0c6ef6bdf8fcf8bf4976e8c68c27fcc7a571e2eb04f77ff31d744bec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterLinuxProfileSshKey",
    jsii_struct_bases=[],
    name_mapping={"key_data": "keyData"},
)
class KubernetesClusterLinuxProfileSshKey:
    def __init__(self, *, key_data: builtins.str) -> None:
        '''
        :param key_data: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#key_data KubernetesCluster#key_data}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3103f9abfbe333f7d6fa1621e69368ead3606d669d3c8abc3e32b00e7f18a70b)
            check_type(argname="argument key_data", value=key_data, expected_type=type_hints["key_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_data": key_data,
        }

    @builtins.property
    def key_data(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#key_data KubernetesCluster#key_data}.'''
        result = self._values.get("key_data")
        assert result is not None, "Required property 'key_data' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterLinuxProfileSshKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterLinuxProfileSshKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterLinuxProfileSshKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__413243aed869640960f15ca73e6a451ff248743b4dc3f57746afc0680435ccc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyDataInput")
    def key_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyDataInput"))

    @builtins.property
    @jsii.member(jsii_name="keyData")
    def key_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyData"))

    @key_data.setter
    def key_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2f23d5c2c8f5529115a709f43999b99745fcbe349cdb6422b5f39453c89bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyData", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterLinuxProfileSshKey]:
        return typing.cast(typing.Optional[KubernetesClusterLinuxProfileSshKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterLinuxProfileSshKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5981ddbc36ff23b936e45a298af5a82b89e16e13d5abc937a63fb88b9a3a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"allowed": "allowed", "not_allowed": "notAllowed"},
)
class KubernetesClusterMaintenanceWindow:
    def __init__(
        self,
        *,
        allowed: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesClusterMaintenanceWindowAllowed", typing.Dict[builtins.str, typing.Any]]]]] = None,
        not_allowed: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KubernetesClusterMaintenanceWindowNotAllowed", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed: allowed block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#allowed KubernetesCluster#allowed}
        :param not_allowed: not_allowed block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#not_allowed KubernetesCluster#not_allowed}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e620fc6d5af60e4413a94f4f560137489625d1d21022fcf2bafce0d1b451b240)
            check_type(argname="argument allowed", value=allowed, expected_type=type_hints["allowed"])
            check_type(argname="argument not_allowed", value=not_allowed, expected_type=type_hints["not_allowed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed is not None:
            self._values["allowed"] = allowed
        if not_allowed is not None:
            self._values["not_allowed"] = not_allowed

    @builtins.property
    def allowed(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesClusterMaintenanceWindowAllowed"]]]:
        '''allowed block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#allowed KubernetesCluster#allowed}
        '''
        result = self._values.get("allowed")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesClusterMaintenanceWindowAllowed"]]], result)

    @builtins.property
    def not_allowed(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesClusterMaintenanceWindowNotAllowed"]]]:
        '''not_allowed block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#not_allowed KubernetesCluster#not_allowed}
        '''
        result = self._values.get("not_allowed")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KubernetesClusterMaintenanceWindowNotAllowed"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMaintenanceWindowAllowed",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "hours": "hours"},
)
class KubernetesClusterMaintenanceWindowAllowed:
    def __init__(
        self,
        *,
        day: builtins.str,
        hours: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param day: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#day KubernetesCluster#day}.
        :param hours: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#hours KubernetesCluster#hours}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b192ac3c1ddbcfdafa15e776e4d9a29941f0906f3518016a5e801d986697cd)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "hours": hours,
        }

    @builtins.property
    def day(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#day KubernetesCluster#day}.'''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hours(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#hours KubernetesCluster#hours}.'''
        result = self._values.get("hours")
        assert result is not None, "Required property 'hours' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterMaintenanceWindowAllowed(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterMaintenanceWindowAllowedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMaintenanceWindowAllowedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b412a823f870e207e1e1d885b9c9578234f4d3fc29ad9ff35475442781ced9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KubernetesClusterMaintenanceWindowAllowedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c2cb9cecfc4a04d67768f48c7b67bbeda50cfee0035800f3f543c6bd203e5cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesClusterMaintenanceWindowAllowedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb5450c84102af889afc8754cb73313bb4bae531cdee8e394fce74e9c55790a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcd0bb451b9e81993b6c063f82906bd2b2a28791fc85b80684ffec6bffd4f52b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4e37011adefe2ed899f33479101d6b0598ef179ce77cb31e904951694fec538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowAllowed]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowAllowed]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowAllowed]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d6f31af3db43b127625a3bc0bccdb13d87ea56fd0a4b9b9f59f003790221f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KubernetesClusterMaintenanceWindowAllowedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMaintenanceWindowAllowedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aec8620611447213d16de723a7767b62f70cab4ce3de49d8bfbda90edf70c470)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e2bf061fb483c729e4cfd620347d12b21b7b9c792085da8bb5e9e8348c4161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value)

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f500d13fd0f33f607f9fc6c0648a3a7e5cf9aeb3bf226e1b0a67a1c7c97b5e3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KubernetesClusterMaintenanceWindowAllowed, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KubernetesClusterMaintenanceWindowAllowed, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KubernetesClusterMaintenanceWindowAllowed, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90deebe24decc889d10c36bf294a8a991e350f1252ae8fa7807ebfd6cbaec7ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMaintenanceWindowNotAllowed",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start"},
)
class KubernetesClusterMaintenanceWindowNotAllowed:
    def __init__(self, *, end: builtins.str, start: builtins.str) -> None:
        '''
        :param end: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#end KubernetesCluster#end}.
        :param start: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#start KubernetesCluster#start}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662d46c75a06e22ea7735591c2cb2bf7739da5d42d6081ca02313c91f1b4370b)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "start": start,
        }

    @builtins.property
    def end(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#end KubernetesCluster#end}.'''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#start KubernetesCluster#start}.'''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterMaintenanceWindowNotAllowed(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterMaintenanceWindowNotAllowedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMaintenanceWindowNotAllowedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3545f37a706ec4a8a76461c4993768f50ea4e73db3ca427160e9e1282176d5dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KubernetesClusterMaintenanceWindowNotAllowedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059dbe1b82a48e34819282740cc6b370f3d58b2b951f1435bf6d425b87394c88)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesClusterMaintenanceWindowNotAllowedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02d16ba2597b30f0d9fb68af85bda38559329cfcda5c2427f09861f75549e4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f62fbfdbf3210a4aee22cde58c90a1cfbc6bff49532891b2244ddcc80da55c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f73da76594cdcb53ba4e7c3c29f725c793ee78c48a023cb03d613b9f57f04df5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowNotAllowed]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowNotAllowed]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowNotAllowed]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15724ff63c3e3b2883c0322f47304cd2078fa5e7736733910aaaa01a1adbff72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KubernetesClusterMaintenanceWindowNotAllowedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMaintenanceWindowNotAllowedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37eb76f4d3a555f64770d91fbd2bf1954ca81387eb027309735f8af463071882)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "end"))

    @end.setter
    def end(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ee279c06b33f1f28346bf942de7a46c761a0bbc9255915831c5720e2fe1fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value)

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "start"))

    @start.setter
    def start(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0392c2cefb06712557adcf029a78e03eae06ff69b931183ce25039f97a1ddf9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KubernetesClusterMaintenanceWindowNotAllowed, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KubernetesClusterMaintenanceWindowNotAllowed, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KubernetesClusterMaintenanceWindowNotAllowed, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b71707e9deed18a5f320700cd86562b6bbef6bd7a69162a10741418e49db39de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KubernetesClusterMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59b271da19b311d67d53f9f3cf97122c0a626cfe0e715f05e547235554d28957)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowed")
    def put_allowed(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesClusterMaintenanceWindowAllowed, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aadc806a8423bdb09003e6a0afd258868532f64d8d8fca84419749449063613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowed", [value]))

    @jsii.member(jsii_name="putNotAllowed")
    def put_not_allowed(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesClusterMaintenanceWindowNotAllowed, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e11286b7262df6e8f96badced69b4c5438a49a74f5be311c5f847ef9980a7fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNotAllowed", [value]))

    @jsii.member(jsii_name="resetAllowed")
    def reset_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowed", []))

    @jsii.member(jsii_name="resetNotAllowed")
    def reset_not_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotAllowed", []))

    @builtins.property
    @jsii.member(jsii_name="allowed")
    def allowed(self) -> KubernetesClusterMaintenanceWindowAllowedList:
        return typing.cast(KubernetesClusterMaintenanceWindowAllowedList, jsii.get(self, "allowed"))

    @builtins.property
    @jsii.member(jsii_name="notAllowed")
    def not_allowed(self) -> KubernetesClusterMaintenanceWindowNotAllowedList:
        return typing.cast(KubernetesClusterMaintenanceWindowNotAllowedList, jsii.get(self, "notAllowed"))

    @builtins.property
    @jsii.member(jsii_name="allowedInput")
    def allowed_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowAllowed]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowAllowed]]], jsii.get(self, "allowedInput"))

    @builtins.property
    @jsii.member(jsii_name="notAllowedInput")
    def not_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowNotAllowed]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowNotAllowed]]], jsii.get(self, "notAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterMaintenanceWindow]:
        return typing.cast(typing.Optional[KubernetesClusterMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a08687c68adaa177b022847ca11674db44407596d1803383d989465b9cb45d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMicrosoftDefender",
    jsii_struct_bases=[],
    name_mapping={"log_analytics_workspace_id": "logAnalyticsWorkspaceId"},
)
class KubernetesClusterMicrosoftDefender:
    def __init__(self, *, log_analytics_workspace_id: builtins.str) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#log_analytics_workspace_id KubernetesCluster#log_analytics_workspace_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083c7c2416298c9d99cfd18c635950df112c5583290ca653505edc307373c0d6)
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_analytics_workspace_id": log_analytics_workspace_id,
        }

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#log_analytics_workspace_id KubernetesCluster#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterMicrosoftDefender(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterMicrosoftDefenderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMicrosoftDefenderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7955d64ea082862c9a8376bac8f04b6a6b74754b575f798f3e9579b2d7bb079c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceIdInput")
    def log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsWorkspaceId"))

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c87ad9675dc8e0efc93f4d537a7f559415135b26e1fb2153586344945fbbe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterMicrosoftDefender]:
        return typing.cast(typing.Optional[KubernetesClusterMicrosoftDefender], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterMicrosoftDefender],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d51b00c57742a92f5d10e273ebb4d772953fba65f7b3c1eb1be71d94f5ec960a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMonitorMetrics",
    jsii_struct_bases=[],
    name_mapping={
        "annotations_allowed": "annotationsAllowed",
        "labels_allowed": "labelsAllowed",
    },
)
class KubernetesClusterMonitorMetrics:
    def __init__(
        self,
        *,
        annotations_allowed: typing.Optional[builtins.str] = None,
        labels_allowed: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations_allowed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#annotations_allowed KubernetesCluster#annotations_allowed}.
        :param labels_allowed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#labels_allowed KubernetesCluster#labels_allowed}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6288c0c064236591bb73e3eb9a38a0e777f4c69e2ade10fe560d8c10455433)
            check_type(argname="argument annotations_allowed", value=annotations_allowed, expected_type=type_hints["annotations_allowed"])
            check_type(argname="argument labels_allowed", value=labels_allowed, expected_type=type_hints["labels_allowed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations_allowed is not None:
            self._values["annotations_allowed"] = annotations_allowed
        if labels_allowed is not None:
            self._values["labels_allowed"] = labels_allowed

    @builtins.property
    def annotations_allowed(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#annotations_allowed KubernetesCluster#annotations_allowed}.'''
        result = self._values.get("annotations_allowed")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels_allowed(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#labels_allowed KubernetesCluster#labels_allowed}.'''
        result = self._values.get("labels_allowed")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterMonitorMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterMonitorMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterMonitorMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48c82493b085ea6a91e17eef77cdacced60767dfe4c9a358b0db5446226f2662)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAnnotationsAllowed")
    def reset_annotations_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotationsAllowed", []))

    @jsii.member(jsii_name="resetLabelsAllowed")
    def reset_labels_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabelsAllowed", []))

    @builtins.property
    @jsii.member(jsii_name="annotationsAllowedInput")
    def annotations_allowed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "annotationsAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsAllowedInput")
    def labels_allowed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelsAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="annotationsAllowed")
    def annotations_allowed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "annotationsAllowed"))

    @annotations_allowed.setter
    def annotations_allowed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5acf1e4ee67cfbdaa580b0bb5dd0a1822a37818ff868e7257b3ef8300cabc3f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotationsAllowed", value)

    @builtins.property
    @jsii.member(jsii_name="labelsAllowed")
    def labels_allowed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelsAllowed"))

    @labels_allowed.setter
    def labels_allowed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195a492016692a9eb5334e8bdd6439dff32dfa46e852aae6207afe5f68687d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelsAllowed", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterMonitorMetrics]:
        return typing.cast(typing.Optional[KubernetesClusterMonitorMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterMonitorMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a386f946582505de73537085c3a57380f3330bf837f6f7a496f46cdf0eb7e9fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterNetworkProfile",
    jsii_struct_bases=[],
    name_mapping={
        "network_plugin": "networkPlugin",
        "dns_service_ip": "dnsServiceIp",
        "docker_bridge_cidr": "dockerBridgeCidr",
        "ebpf_data_plane": "ebpfDataPlane",
        "ip_versions": "ipVersions",
        "load_balancer_profile": "loadBalancerProfile",
        "load_balancer_sku": "loadBalancerSku",
        "nat_gateway_profile": "natGatewayProfile",
        "network_mode": "networkMode",
        "network_plugin_mode": "networkPluginMode",
        "network_policy": "networkPolicy",
        "outbound_type": "outboundType",
        "pod_cidr": "podCidr",
        "pod_cidrs": "podCidrs",
        "service_cidr": "serviceCidr",
        "service_cidrs": "serviceCidrs",
    },
)
class KubernetesClusterNetworkProfile:
    def __init__(
        self,
        *,
        network_plugin: builtins.str,
        dns_service_ip: typing.Optional[builtins.str] = None,
        docker_bridge_cidr: typing.Optional[builtins.str] = None,
        ebpf_data_plane: typing.Optional[builtins.str] = None,
        ip_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        load_balancer_profile: typing.Optional[typing.Union["KubernetesClusterNetworkProfileLoadBalancerProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancer_sku: typing.Optional[builtins.str] = None,
        nat_gateway_profile: typing.Optional[typing.Union["KubernetesClusterNetworkProfileNatGatewayProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        network_mode: typing.Optional[builtins.str] = None,
        network_plugin_mode: typing.Optional[builtins.str] = None,
        network_policy: typing.Optional[builtins.str] = None,
        outbound_type: typing.Optional[builtins.str] = None,
        pod_cidr: typing.Optional[builtins.str] = None,
        pod_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_cidr: typing.Optional[builtins.str] = None,
        service_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network_plugin: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_plugin KubernetesCluster#network_plugin}.
        :param dns_service_ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_service_ip KubernetesCluster#dns_service_ip}.
        :param docker_bridge_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#docker_bridge_cidr KubernetesCluster#docker_bridge_cidr}.
        :param ebpf_data_plane: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ebpf_data_plane KubernetesCluster#ebpf_data_plane}.
        :param ip_versions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ip_versions KubernetesCluster#ip_versions}.
        :param load_balancer_profile: load_balancer_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#load_balancer_profile KubernetesCluster#load_balancer_profile}
        :param load_balancer_sku: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#load_balancer_sku KubernetesCluster#load_balancer_sku}.
        :param nat_gateway_profile: nat_gateway_profile block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#nat_gateway_profile KubernetesCluster#nat_gateway_profile}
        :param network_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_mode KubernetesCluster#network_mode}.
        :param network_plugin_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_plugin_mode KubernetesCluster#network_plugin_mode}.
        :param network_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_policy KubernetesCluster#network_policy}.
        :param outbound_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_type KubernetesCluster#outbound_type}.
        :param pod_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_cidr KubernetesCluster#pod_cidr}.
        :param pod_cidrs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_cidrs KubernetesCluster#pod_cidrs}.
        :param service_cidr: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#service_cidr KubernetesCluster#service_cidr}.
        :param service_cidrs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#service_cidrs KubernetesCluster#service_cidrs}.
        '''
        if isinstance(load_balancer_profile, dict):
            load_balancer_profile = KubernetesClusterNetworkProfileLoadBalancerProfile(**load_balancer_profile)
        if isinstance(nat_gateway_profile, dict):
            nat_gateway_profile = KubernetesClusterNetworkProfileNatGatewayProfile(**nat_gateway_profile)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee8dd7146ebdd597ec5585057aea38455e0531a7be1f0ff33964223da9f99db)
            check_type(argname="argument network_plugin", value=network_plugin, expected_type=type_hints["network_plugin"])
            check_type(argname="argument dns_service_ip", value=dns_service_ip, expected_type=type_hints["dns_service_ip"])
            check_type(argname="argument docker_bridge_cidr", value=docker_bridge_cidr, expected_type=type_hints["docker_bridge_cidr"])
            check_type(argname="argument ebpf_data_plane", value=ebpf_data_plane, expected_type=type_hints["ebpf_data_plane"])
            check_type(argname="argument ip_versions", value=ip_versions, expected_type=type_hints["ip_versions"])
            check_type(argname="argument load_balancer_profile", value=load_balancer_profile, expected_type=type_hints["load_balancer_profile"])
            check_type(argname="argument load_balancer_sku", value=load_balancer_sku, expected_type=type_hints["load_balancer_sku"])
            check_type(argname="argument nat_gateway_profile", value=nat_gateway_profile, expected_type=type_hints["nat_gateway_profile"])
            check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
            check_type(argname="argument network_plugin_mode", value=network_plugin_mode, expected_type=type_hints["network_plugin_mode"])
            check_type(argname="argument network_policy", value=network_policy, expected_type=type_hints["network_policy"])
            check_type(argname="argument outbound_type", value=outbound_type, expected_type=type_hints["outbound_type"])
            check_type(argname="argument pod_cidr", value=pod_cidr, expected_type=type_hints["pod_cidr"])
            check_type(argname="argument pod_cidrs", value=pod_cidrs, expected_type=type_hints["pod_cidrs"])
            check_type(argname="argument service_cidr", value=service_cidr, expected_type=type_hints["service_cidr"])
            check_type(argname="argument service_cidrs", value=service_cidrs, expected_type=type_hints["service_cidrs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_plugin": network_plugin,
        }
        if dns_service_ip is not None:
            self._values["dns_service_ip"] = dns_service_ip
        if docker_bridge_cidr is not None:
            self._values["docker_bridge_cidr"] = docker_bridge_cidr
        if ebpf_data_plane is not None:
            self._values["ebpf_data_plane"] = ebpf_data_plane
        if ip_versions is not None:
            self._values["ip_versions"] = ip_versions
        if load_balancer_profile is not None:
            self._values["load_balancer_profile"] = load_balancer_profile
        if load_balancer_sku is not None:
            self._values["load_balancer_sku"] = load_balancer_sku
        if nat_gateway_profile is not None:
            self._values["nat_gateway_profile"] = nat_gateway_profile
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if network_plugin_mode is not None:
            self._values["network_plugin_mode"] = network_plugin_mode
        if network_policy is not None:
            self._values["network_policy"] = network_policy
        if outbound_type is not None:
            self._values["outbound_type"] = outbound_type
        if pod_cidr is not None:
            self._values["pod_cidr"] = pod_cidr
        if pod_cidrs is not None:
            self._values["pod_cidrs"] = pod_cidrs
        if service_cidr is not None:
            self._values["service_cidr"] = service_cidr
        if service_cidrs is not None:
            self._values["service_cidrs"] = service_cidrs

    @builtins.property
    def network_plugin(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_plugin KubernetesCluster#network_plugin}.'''
        result = self._values.get("network_plugin")
        assert result is not None, "Required property 'network_plugin' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dns_service_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_service_ip KubernetesCluster#dns_service_ip}.'''
        result = self._values.get("dns_service_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_bridge_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#docker_bridge_cidr KubernetesCluster#docker_bridge_cidr}.'''
        result = self._values.get("docker_bridge_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebpf_data_plane(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ebpf_data_plane KubernetesCluster#ebpf_data_plane}.'''
        result = self._values.get("ebpf_data_plane")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#ip_versions KubernetesCluster#ip_versions}.'''
        result = self._values.get("ip_versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def load_balancer_profile(
        self,
    ) -> typing.Optional["KubernetesClusterNetworkProfileLoadBalancerProfile"]:
        '''load_balancer_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#load_balancer_profile KubernetesCluster#load_balancer_profile}
        '''
        result = self._values.get("load_balancer_profile")
        return typing.cast(typing.Optional["KubernetesClusterNetworkProfileLoadBalancerProfile"], result)

    @builtins.property
    def load_balancer_sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#load_balancer_sku KubernetesCluster#load_balancer_sku}.'''
        result = self._values.get("load_balancer_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nat_gateway_profile(
        self,
    ) -> typing.Optional["KubernetesClusterNetworkProfileNatGatewayProfile"]:
        '''nat_gateway_profile block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#nat_gateway_profile KubernetesCluster#nat_gateway_profile}
        '''
        result = self._values.get("nat_gateway_profile")
        return typing.cast(typing.Optional["KubernetesClusterNetworkProfileNatGatewayProfile"], result)

    @builtins.property
    def network_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_mode KubernetesCluster#network_mode}.'''
        result = self._values.get("network_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_plugin_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_plugin_mode KubernetesCluster#network_plugin_mode}.'''
        result = self._values.get("network_plugin_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#network_policy KubernetesCluster#network_policy}.'''
        result = self._values.get("network_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outbound_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_type KubernetesCluster#outbound_type}.'''
        result = self._values.get("outbound_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_cidr KubernetesCluster#pod_cidr}.'''
        result = self._values.get("pod_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#pod_cidrs KubernetesCluster#pod_cidrs}.'''
        result = self._values.get("pod_cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#service_cidr KubernetesCluster#service_cidr}.'''
        result = self._values.get("service_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#service_cidrs KubernetesCluster#service_cidrs}.'''
        result = self._values.get("service_cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNetworkProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterNetworkProfileLoadBalancerProfile",
    jsii_struct_bases=[],
    name_mapping={
        "idle_timeout_in_minutes": "idleTimeoutInMinutes",
        "managed_outbound_ip_count": "managedOutboundIpCount",
        "managed_outbound_ipv6_count": "managedOutboundIpv6Count",
        "outbound_ip_address_ids": "outboundIpAddressIds",
        "outbound_ip_prefix_ids": "outboundIpPrefixIds",
        "outbound_ports_allocated": "outboundPortsAllocated",
    },
)
class KubernetesClusterNetworkProfileLoadBalancerProfile:
    def __init__(
        self,
        *,
        idle_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        managed_outbound_ip_count: typing.Optional[jsii.Number] = None,
        managed_outbound_ipv6_count: typing.Optional[jsii.Number] = None,
        outbound_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        outbound_ip_prefix_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        outbound_ports_allocated: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param idle_timeout_in_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#idle_timeout_in_minutes KubernetesCluster#idle_timeout_in_minutes}.
        :param managed_outbound_ip_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed_outbound_ip_count KubernetesCluster#managed_outbound_ip_count}.
        :param managed_outbound_ipv6_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed_outbound_ipv6_count KubernetesCluster#managed_outbound_ipv6_count}.
        :param outbound_ip_address_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_ip_address_ids KubernetesCluster#outbound_ip_address_ids}.
        :param outbound_ip_prefix_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_ip_prefix_ids KubernetesCluster#outbound_ip_prefix_ids}.
        :param outbound_ports_allocated: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_ports_allocated KubernetesCluster#outbound_ports_allocated}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e83523dc4eb212b800322c3a9cb717e713cedcbf9be86e251cf107828c8fa8)
            check_type(argname="argument idle_timeout_in_minutes", value=idle_timeout_in_minutes, expected_type=type_hints["idle_timeout_in_minutes"])
            check_type(argname="argument managed_outbound_ip_count", value=managed_outbound_ip_count, expected_type=type_hints["managed_outbound_ip_count"])
            check_type(argname="argument managed_outbound_ipv6_count", value=managed_outbound_ipv6_count, expected_type=type_hints["managed_outbound_ipv6_count"])
            check_type(argname="argument outbound_ip_address_ids", value=outbound_ip_address_ids, expected_type=type_hints["outbound_ip_address_ids"])
            check_type(argname="argument outbound_ip_prefix_ids", value=outbound_ip_prefix_ids, expected_type=type_hints["outbound_ip_prefix_ids"])
            check_type(argname="argument outbound_ports_allocated", value=outbound_ports_allocated, expected_type=type_hints["outbound_ports_allocated"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle_timeout_in_minutes is not None:
            self._values["idle_timeout_in_minutes"] = idle_timeout_in_minutes
        if managed_outbound_ip_count is not None:
            self._values["managed_outbound_ip_count"] = managed_outbound_ip_count
        if managed_outbound_ipv6_count is not None:
            self._values["managed_outbound_ipv6_count"] = managed_outbound_ipv6_count
        if outbound_ip_address_ids is not None:
            self._values["outbound_ip_address_ids"] = outbound_ip_address_ids
        if outbound_ip_prefix_ids is not None:
            self._values["outbound_ip_prefix_ids"] = outbound_ip_prefix_ids
        if outbound_ports_allocated is not None:
            self._values["outbound_ports_allocated"] = outbound_ports_allocated

    @builtins.property
    def idle_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#idle_timeout_in_minutes KubernetesCluster#idle_timeout_in_minutes}.'''
        result = self._values.get("idle_timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def managed_outbound_ip_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed_outbound_ip_count KubernetesCluster#managed_outbound_ip_count}.'''
        result = self._values.get("managed_outbound_ip_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def managed_outbound_ipv6_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed_outbound_ipv6_count KubernetesCluster#managed_outbound_ipv6_count}.'''
        result = self._values.get("managed_outbound_ipv6_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def outbound_ip_address_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_ip_address_ids KubernetesCluster#outbound_ip_address_ids}.'''
        result = self._values.get("outbound_ip_address_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def outbound_ip_prefix_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_ip_prefix_ids KubernetesCluster#outbound_ip_prefix_ids}.'''
        result = self._values.get("outbound_ip_prefix_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def outbound_ports_allocated(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_ports_allocated KubernetesCluster#outbound_ports_allocated}.'''
        result = self._values.get("outbound_ports_allocated")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNetworkProfileLoadBalancerProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterNetworkProfileLoadBalancerProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterNetworkProfileLoadBalancerProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a33c76d84e027198b1b3ce8c4ce33d0fc79259ba1f444257d110ebf9cca48db5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdleTimeoutInMinutes")
    def reset_idle_timeout_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleTimeoutInMinutes", []))

    @jsii.member(jsii_name="resetManagedOutboundIpCount")
    def reset_managed_outbound_ip_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedOutboundIpCount", []))

    @jsii.member(jsii_name="resetManagedOutboundIpv6Count")
    def reset_managed_outbound_ipv6_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedOutboundIpv6Count", []))

    @jsii.member(jsii_name="resetOutboundIpAddressIds")
    def reset_outbound_ip_address_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundIpAddressIds", []))

    @jsii.member(jsii_name="resetOutboundIpPrefixIds")
    def reset_outbound_ip_prefix_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundIpPrefixIds", []))

    @jsii.member(jsii_name="resetOutboundPortsAllocated")
    def reset_outbound_ports_allocated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundPortsAllocated", []))

    @builtins.property
    @jsii.member(jsii_name="effectiveOutboundIps")
    def effective_outbound_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "effectiveOutboundIps"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutInMinutesInput")
    def idle_timeout_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleTimeoutInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="managedOutboundIpCountInput")
    def managed_outbound_ip_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "managedOutboundIpCountInput"))

    @builtins.property
    @jsii.member(jsii_name="managedOutboundIpv6CountInput")
    def managed_outbound_ipv6_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "managedOutboundIpv6CountInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundIpAddressIdsInput")
    def outbound_ip_address_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outboundIpAddressIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundIpPrefixIdsInput")
    def outbound_ip_prefix_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outboundIpPrefixIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundPortsAllocatedInput")
    def outbound_ports_allocated_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "outboundPortsAllocatedInput"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutInMinutes")
    def idle_timeout_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "idleTimeoutInMinutes"))

    @idle_timeout_in_minutes.setter
    def idle_timeout_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__531bb23c83838f870e5174073389cfd3d78aa1c1fd0316cdcbf1f0593dfe9c2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeoutInMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="managedOutboundIpCount")
    def managed_outbound_ip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "managedOutboundIpCount"))

    @managed_outbound_ip_count.setter
    def managed_outbound_ip_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1e286b2f78ea015b8cfd4915873b667dfd1c013f1eeac15c598c93cd71d57d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedOutboundIpCount", value)

    @builtins.property
    @jsii.member(jsii_name="managedOutboundIpv6Count")
    def managed_outbound_ipv6_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "managedOutboundIpv6Count"))

    @managed_outbound_ipv6_count.setter
    def managed_outbound_ipv6_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612aebee85969c3ede2b2ac3e78f1da7a692fb0a30e1dbe152407eab29e93fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedOutboundIpv6Count", value)

    @builtins.property
    @jsii.member(jsii_name="outboundIpAddressIds")
    def outbound_ip_address_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outboundIpAddressIds"))

    @outbound_ip_address_ids.setter
    def outbound_ip_address_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5d49c417c850affd668a9a9724b59684f5c8f96228931fb239469ce0e8b7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundIpAddressIds", value)

    @builtins.property
    @jsii.member(jsii_name="outboundIpPrefixIds")
    def outbound_ip_prefix_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outboundIpPrefixIds"))

    @outbound_ip_prefix_ids.setter
    def outbound_ip_prefix_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c44deb60b6ad341c6b107e3c959ec2dc9411cb055ff5ad7dc87402451e17fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundIpPrefixIds", value)

    @builtins.property
    @jsii.member(jsii_name="outboundPortsAllocated")
    def outbound_ports_allocated(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "outboundPortsAllocated"))

    @outbound_ports_allocated.setter
    def outbound_ports_allocated(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1620ad06ee45d2859cf8014cb317a16423f7010823ff0dc6aede620582380f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundPortsAllocated", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterNetworkProfileLoadBalancerProfile]:
        return typing.cast(typing.Optional[KubernetesClusterNetworkProfileLoadBalancerProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterNetworkProfileLoadBalancerProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e79757d6ff27c3745cde5cec4be673803be2c3a0b20da8908bf82103c9e78d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterNetworkProfileNatGatewayProfile",
    jsii_struct_bases=[],
    name_mapping={
        "idle_timeout_in_minutes": "idleTimeoutInMinutes",
        "managed_outbound_ip_count": "managedOutboundIpCount",
    },
)
class KubernetesClusterNetworkProfileNatGatewayProfile:
    def __init__(
        self,
        *,
        idle_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        managed_outbound_ip_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param idle_timeout_in_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#idle_timeout_in_minutes KubernetesCluster#idle_timeout_in_minutes}.
        :param managed_outbound_ip_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed_outbound_ip_count KubernetesCluster#managed_outbound_ip_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63a1c52f508c3b522d4afae369a55ca9fe5879a1d5209b8b6df3f41fbca5a00)
            check_type(argname="argument idle_timeout_in_minutes", value=idle_timeout_in_minutes, expected_type=type_hints["idle_timeout_in_minutes"])
            check_type(argname="argument managed_outbound_ip_count", value=managed_outbound_ip_count, expected_type=type_hints["managed_outbound_ip_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle_timeout_in_minutes is not None:
            self._values["idle_timeout_in_minutes"] = idle_timeout_in_minutes
        if managed_outbound_ip_count is not None:
            self._values["managed_outbound_ip_count"] = managed_outbound_ip_count

    @builtins.property
    def idle_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#idle_timeout_in_minutes KubernetesCluster#idle_timeout_in_minutes}.'''
        result = self._values.get("idle_timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def managed_outbound_ip_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed_outbound_ip_count KubernetesCluster#managed_outbound_ip_count}.'''
        result = self._values.get("managed_outbound_ip_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterNetworkProfileNatGatewayProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterNetworkProfileNatGatewayProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterNetworkProfileNatGatewayProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ca670a2f4cded42bb183d95c225a3cc6959a8f75b468ff0bd814bd36617a5ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdleTimeoutInMinutes")
    def reset_idle_timeout_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleTimeoutInMinutes", []))

    @jsii.member(jsii_name="resetManagedOutboundIpCount")
    def reset_managed_outbound_ip_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedOutboundIpCount", []))

    @builtins.property
    @jsii.member(jsii_name="effectiveOutboundIps")
    def effective_outbound_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "effectiveOutboundIps"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutInMinutesInput")
    def idle_timeout_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleTimeoutInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="managedOutboundIpCountInput")
    def managed_outbound_ip_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "managedOutboundIpCountInput"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutInMinutes")
    def idle_timeout_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "idleTimeoutInMinutes"))

    @idle_timeout_in_minutes.setter
    def idle_timeout_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0539af7835e609331d03701613281d65030d6fdddd8529a9160d48e29ca98ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeoutInMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="managedOutboundIpCount")
    def managed_outbound_ip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "managedOutboundIpCount"))

    @managed_outbound_ip_count.setter
    def managed_outbound_ip_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58545ade43fd69737748707a706a50aabb0bf20014fa90ba5a3b1910e7b6b26d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedOutboundIpCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterNetworkProfileNatGatewayProfile]:
        return typing.cast(typing.Optional[KubernetesClusterNetworkProfileNatGatewayProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterNetworkProfileNatGatewayProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6d1eb7560807370019cc5e0797ef9476105b6770e6333b158504a51b85e339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KubernetesClusterNetworkProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterNetworkProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5caa63a1bf89c917cf97df5f9f03548c605de0becd3098ea8f28964c8531d5e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoadBalancerProfile")
    def put_load_balancer_profile(
        self,
        *,
        idle_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        managed_outbound_ip_count: typing.Optional[jsii.Number] = None,
        managed_outbound_ipv6_count: typing.Optional[jsii.Number] = None,
        outbound_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        outbound_ip_prefix_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        outbound_ports_allocated: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param idle_timeout_in_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#idle_timeout_in_minutes KubernetesCluster#idle_timeout_in_minutes}.
        :param managed_outbound_ip_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed_outbound_ip_count KubernetesCluster#managed_outbound_ip_count}.
        :param managed_outbound_ipv6_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed_outbound_ipv6_count KubernetesCluster#managed_outbound_ipv6_count}.
        :param outbound_ip_address_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_ip_address_ids KubernetesCluster#outbound_ip_address_ids}.
        :param outbound_ip_prefix_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_ip_prefix_ids KubernetesCluster#outbound_ip_prefix_ids}.
        :param outbound_ports_allocated: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#outbound_ports_allocated KubernetesCluster#outbound_ports_allocated}.
        '''
        value = KubernetesClusterNetworkProfileLoadBalancerProfile(
            idle_timeout_in_minutes=idle_timeout_in_minutes,
            managed_outbound_ip_count=managed_outbound_ip_count,
            managed_outbound_ipv6_count=managed_outbound_ipv6_count,
            outbound_ip_address_ids=outbound_ip_address_ids,
            outbound_ip_prefix_ids=outbound_ip_prefix_ids,
            outbound_ports_allocated=outbound_ports_allocated,
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancerProfile", [value]))

    @jsii.member(jsii_name="putNatGatewayProfile")
    def put_nat_gateway_profile(
        self,
        *,
        idle_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        managed_outbound_ip_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param idle_timeout_in_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#idle_timeout_in_minutes KubernetesCluster#idle_timeout_in_minutes}.
        :param managed_outbound_ip_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#managed_outbound_ip_count KubernetesCluster#managed_outbound_ip_count}.
        '''
        value = KubernetesClusterNetworkProfileNatGatewayProfile(
            idle_timeout_in_minutes=idle_timeout_in_minutes,
            managed_outbound_ip_count=managed_outbound_ip_count,
        )

        return typing.cast(None, jsii.invoke(self, "putNatGatewayProfile", [value]))

    @jsii.member(jsii_name="resetDnsServiceIp")
    def reset_dns_service_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServiceIp", []))

    @jsii.member(jsii_name="resetDockerBridgeCidr")
    def reset_docker_bridge_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerBridgeCidr", []))

    @jsii.member(jsii_name="resetEbpfDataPlane")
    def reset_ebpf_data_plane(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbpfDataPlane", []))

    @jsii.member(jsii_name="resetIpVersions")
    def reset_ip_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpVersions", []))

    @jsii.member(jsii_name="resetLoadBalancerProfile")
    def reset_load_balancer_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerProfile", []))

    @jsii.member(jsii_name="resetLoadBalancerSku")
    def reset_load_balancer_sku(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerSku", []))

    @jsii.member(jsii_name="resetNatGatewayProfile")
    def reset_nat_gateway_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNatGatewayProfile", []))

    @jsii.member(jsii_name="resetNetworkMode")
    def reset_network_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkMode", []))

    @jsii.member(jsii_name="resetNetworkPluginMode")
    def reset_network_plugin_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPluginMode", []))

    @jsii.member(jsii_name="resetNetworkPolicy")
    def reset_network_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPolicy", []))

    @jsii.member(jsii_name="resetOutboundType")
    def reset_outbound_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundType", []))

    @jsii.member(jsii_name="resetPodCidr")
    def reset_pod_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodCidr", []))

    @jsii.member(jsii_name="resetPodCidrs")
    def reset_pod_cidrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodCidrs", []))

    @jsii.member(jsii_name="resetServiceCidr")
    def reset_service_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceCidr", []))

    @jsii.member(jsii_name="resetServiceCidrs")
    def reset_service_cidrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceCidrs", []))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerProfile")
    def load_balancer_profile(
        self,
    ) -> KubernetesClusterNetworkProfileLoadBalancerProfileOutputReference:
        return typing.cast(KubernetesClusterNetworkProfileLoadBalancerProfileOutputReference, jsii.get(self, "loadBalancerProfile"))

    @builtins.property
    @jsii.member(jsii_name="natGatewayProfile")
    def nat_gateway_profile(
        self,
    ) -> KubernetesClusterNetworkProfileNatGatewayProfileOutputReference:
        return typing.cast(KubernetesClusterNetworkProfileNatGatewayProfileOutputReference, jsii.get(self, "natGatewayProfile"))

    @builtins.property
    @jsii.member(jsii_name="dnsServiceIpInput")
    def dns_service_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsServiceIpInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerBridgeCidrInput")
    def docker_bridge_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerBridgeCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="ebpfDataPlaneInput")
    def ebpf_data_plane_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ebpfDataPlaneInput"))

    @builtins.property
    @jsii.member(jsii_name="ipVersionsInput")
    def ip_versions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerProfileInput")
    def load_balancer_profile_input(
        self,
    ) -> typing.Optional[KubernetesClusterNetworkProfileLoadBalancerProfile]:
        return typing.cast(typing.Optional[KubernetesClusterNetworkProfileLoadBalancerProfile], jsii.get(self, "loadBalancerProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerSkuInput")
    def load_balancer_sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerSkuInput"))

    @builtins.property
    @jsii.member(jsii_name="natGatewayProfileInput")
    def nat_gateway_profile_input(
        self,
    ) -> typing.Optional[KubernetesClusterNetworkProfileNatGatewayProfile]:
        return typing.cast(typing.Optional[KubernetesClusterNetworkProfileNatGatewayProfile], jsii.get(self, "natGatewayProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="networkModeInput")
    def network_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkModeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPluginInput")
    def network_plugin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkPluginInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPluginModeInput")
    def network_plugin_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkPluginModeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPolicyInput")
    def network_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundTypeInput")
    def outbound_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outboundTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="podCidrInput")
    def pod_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="podCidrsInput")
    def pod_cidrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "podCidrsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceCidrInput")
    def service_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceCidrsInput")
    def service_cidrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceCidrsInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServiceIp")
    def dns_service_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsServiceIp"))

    @dns_service_ip.setter
    def dns_service_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75cb1d94e54da5ecdb14112c5cb1588091a1c9a18632d2144c34587ee07f49d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServiceIp", value)

    @builtins.property
    @jsii.member(jsii_name="dockerBridgeCidr")
    def docker_bridge_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerBridgeCidr"))

    @docker_bridge_cidr.setter
    def docker_bridge_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0996332d94b64a60663c484b325d9344a223b454cfdb4d1b33d27331188a9f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerBridgeCidr", value)

    @builtins.property
    @jsii.member(jsii_name="ebpfDataPlane")
    def ebpf_data_plane(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ebpfDataPlane"))

    @ebpf_data_plane.setter
    def ebpf_data_plane(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a02dd190756cfeb958ec9e3eecab3bb6a515d49f5ad7adc532c33d4316b09dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebpfDataPlane", value)

    @builtins.property
    @jsii.member(jsii_name="ipVersions")
    def ip_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipVersions"))

    @ip_versions.setter
    def ip_versions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa59945f23f6ff5568e149f0fe50289ba276963f29779ac0b1ba818775a8e99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipVersions", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerSku")
    def load_balancer_sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerSku"))

    @load_balancer_sku.setter
    def load_balancer_sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1464aa08bba5db2dcba7c2a81ff4d722a2660fb84a757e83fae9638927da430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerSku", value)

    @builtins.property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkMode"))

    @network_mode.setter
    def network_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c13b70b39c6e53d1b355583357bd40a3f4c5db1f13e0a07de9759b811f55e35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkMode", value)

    @builtins.property
    @jsii.member(jsii_name="networkPlugin")
    def network_plugin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPlugin"))

    @network_plugin.setter
    def network_plugin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f77dbfb8ac8e2efe8b64e2bf6abf7d0698b45ccabc447ef6a6fe1937f1f4891d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkPlugin", value)

    @builtins.property
    @jsii.member(jsii_name="networkPluginMode")
    def network_plugin_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPluginMode"))

    @network_plugin_mode.setter
    def network_plugin_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a43dd8542c74ce06e2c73cb4b33d5d7e43f957909d67f7c60779de12a3e2dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkPluginMode", value)

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPolicy"))

    @network_policy.setter
    def network_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9cbc3a929f29af081f1d9ae40a54d7eb78810e200756d35dc61a9911ea8f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="outboundType")
    def outbound_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outboundType"))

    @outbound_type.setter
    def outbound_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e62e57874e5c16aaa286e92fed5cebb853cf6c7bb37024923a2de8f3a4b7259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundType", value)

    @builtins.property
    @jsii.member(jsii_name="podCidr")
    def pod_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podCidr"))

    @pod_cidr.setter
    def pod_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9913b0d99912b2f0c861d04702dec12149be1781a96e353c5037ae16893fd8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podCidr", value)

    @builtins.property
    @jsii.member(jsii_name="podCidrs")
    def pod_cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "podCidrs"))

    @pod_cidrs.setter
    def pod_cidrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9847cd1f70f8d9e9fc09fc57e28f691f11df8030074f4ea58d10d01fbe9882d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podCidrs", value)

    @builtins.property
    @jsii.member(jsii_name="serviceCidr")
    def service_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceCidr"))

    @service_cidr.setter
    def service_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312f2999204fabeb35f90035dcd578138c43794df782edc80f688202d520c42c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceCidr", value)

    @builtins.property
    @jsii.member(jsii_name="serviceCidrs")
    def service_cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceCidrs"))

    @service_cidrs.setter
    def service_cidrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e919dec016c7a0f841c42409d2392ce88cb611ec517d534848fb7f12df3d2c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceCidrs", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterNetworkProfile]:
        return typing.cast(typing.Optional[KubernetesClusterNetworkProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterNetworkProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7500eb2b721df6d6322d02685709f38c7141275198f7a3cd7d82298c045e6b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterOmsAgent",
    jsii_struct_bases=[],
    name_mapping={"log_analytics_workspace_id": "logAnalyticsWorkspaceId"},
)
class KubernetesClusterOmsAgent:
    def __init__(self, *, log_analytics_workspace_id: builtins.str) -> None:
        '''
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#log_analytics_workspace_id KubernetesCluster#log_analytics_workspace_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f84ad6672e0a6753be9e68d7dff07b264beb3521d185e86b84c57389cb78a4)
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_analytics_workspace_id": log_analytics_workspace_id,
        }

    @builtins.property
    def log_analytics_workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#log_analytics_workspace_id KubernetesCluster#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        assert result is not None, "Required property 'log_analytics_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterOmsAgent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterOmsAgentOmsAgentIdentity",
    jsii_struct_bases=[],
    name_mapping={},
)
class KubernetesClusterOmsAgentOmsAgentIdentity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterOmsAgentOmsAgentIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterOmsAgentOmsAgentIdentityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterOmsAgentOmsAgentIdentityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93463e7e7482f515421bca1421d7b39500abdcfc0c4f6fa2916bec5852a992e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KubernetesClusterOmsAgentOmsAgentIdentityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb388fdd6e35db6a4dcd2ef565a0df59bbbdd21647ef4a2a45aaad95ed4053d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KubernetesClusterOmsAgentOmsAgentIdentityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfbb0d375bf0c2cdf4d819f0b5e73bdb61d797179c194d4abbef0dadf9b23c93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f66e395ec24bb3bff3731c40cd149e745528b52009a44b234c0448843e21c7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ff41dc0e67546558e1f18623accb8e861de8dda0e627cdccd886e97b34a28d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class KubernetesClusterOmsAgentOmsAgentIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterOmsAgentOmsAgentIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99d4dc4e4a0e3646f0fe04a15ef73e736b56f2703c6fb30ee1680717ef981194)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentityId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterOmsAgentOmsAgentIdentity]:
        return typing.cast(typing.Optional[KubernetesClusterOmsAgentOmsAgentIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterOmsAgentOmsAgentIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b0dec128c3ff52c892a81a2a30d9a176348147f0f656b50bacf62fed08e029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KubernetesClusterOmsAgentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterOmsAgentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d1cf2b2dec18589073e74316eab96c0f92705cff8520301d4938328ed5961cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="omsAgentIdentity")
    def oms_agent_identity(self) -> KubernetesClusterOmsAgentOmsAgentIdentityList:
        return typing.cast(KubernetesClusterOmsAgentOmsAgentIdentityList, jsii.get(self, "omsAgentIdentity"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceIdInput")
    def log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsWorkspaceId"))

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b82fdb3a68c31b2630655044fb0c3f2bc64b1387588de89f86e7621b6905a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterOmsAgent]:
        return typing.cast(typing.Optional[KubernetesClusterOmsAgent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[KubernetesClusterOmsAgent]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edd6876d6431792f28b11e7008b3044a3cc4a8ba91719f9740de84ca29669fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterServicePrincipal",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
)
class KubernetesClusterServicePrincipal:
    def __init__(self, *, client_id: builtins.str, client_secret: builtins.str) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_id KubernetesCluster#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_secret KubernetesCluster#client_secret}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27a6ad5302f87187270a018540ec56cff3453aa93864bfbb76a40dc951e521a)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_id KubernetesCluster#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#client_secret KubernetesCluster#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterServicePrincipal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterServicePrincipalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterServicePrincipalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0887a95e43e382523b37bebb5d6585442b8b79211302cca927b24a4804d6cc20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa656da888f9b69b5749ff1a6e74fc1d8de86f4610208dd5278623624e0bde2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b614cdc34167b0ed19eebc684f4012e45a12f7f6cc5bd490d7da80eb1fda566e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterServicePrincipal]:
        return typing.cast(typing.Optional[KubernetesClusterServicePrincipal], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterServicePrincipal],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ced64758f09c56499ed3455b1d618d42a5f0f939a1d85dc85b59b6d680833f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterStorageProfile",
    jsii_struct_bases=[],
    name_mapping={
        "blob_driver_enabled": "blobDriverEnabled",
        "disk_driver_enabled": "diskDriverEnabled",
        "disk_driver_version": "diskDriverVersion",
        "file_driver_enabled": "fileDriverEnabled",
        "snapshot_controller_enabled": "snapshotControllerEnabled",
    },
)
class KubernetesClusterStorageProfile:
    def __init__(
        self,
        *,
        blob_driver_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_driver_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_driver_version: typing.Optional[builtins.str] = None,
        file_driver_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snapshot_controller_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param blob_driver_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#blob_driver_enabled KubernetesCluster#blob_driver_enabled}.
        :param disk_driver_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#disk_driver_enabled KubernetesCluster#disk_driver_enabled}.
        :param disk_driver_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#disk_driver_version KubernetesCluster#disk_driver_version}.
        :param file_driver_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#file_driver_enabled KubernetesCluster#file_driver_enabled}.
        :param snapshot_controller_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#snapshot_controller_enabled KubernetesCluster#snapshot_controller_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90da5eedfd0735040239804ee62907180ec96aaea00d7fdf57cc1fb3a7ef12ca)
            check_type(argname="argument blob_driver_enabled", value=blob_driver_enabled, expected_type=type_hints["blob_driver_enabled"])
            check_type(argname="argument disk_driver_enabled", value=disk_driver_enabled, expected_type=type_hints["disk_driver_enabled"])
            check_type(argname="argument disk_driver_version", value=disk_driver_version, expected_type=type_hints["disk_driver_version"])
            check_type(argname="argument file_driver_enabled", value=file_driver_enabled, expected_type=type_hints["file_driver_enabled"])
            check_type(argname="argument snapshot_controller_enabled", value=snapshot_controller_enabled, expected_type=type_hints["snapshot_controller_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if blob_driver_enabled is not None:
            self._values["blob_driver_enabled"] = blob_driver_enabled
        if disk_driver_enabled is not None:
            self._values["disk_driver_enabled"] = disk_driver_enabled
        if disk_driver_version is not None:
            self._values["disk_driver_version"] = disk_driver_version
        if file_driver_enabled is not None:
            self._values["file_driver_enabled"] = file_driver_enabled
        if snapshot_controller_enabled is not None:
            self._values["snapshot_controller_enabled"] = snapshot_controller_enabled

    @builtins.property
    def blob_driver_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#blob_driver_enabled KubernetesCluster#blob_driver_enabled}.'''
        result = self._values.get("blob_driver_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disk_driver_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#disk_driver_enabled KubernetesCluster#disk_driver_enabled}.'''
        result = self._values.get("disk_driver_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disk_driver_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#disk_driver_version KubernetesCluster#disk_driver_version}.'''
        result = self._values.get("disk_driver_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_driver_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#file_driver_enabled KubernetesCluster#file_driver_enabled}.'''
        result = self._values.get("file_driver_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def snapshot_controller_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#snapshot_controller_enabled KubernetesCluster#snapshot_controller_enabled}.'''
        result = self._values.get("snapshot_controller_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterStorageProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterStorageProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterStorageProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c005ba9c6e4392f63ac99866f02065969864b4c8a95547cdcd1e15a48e8d2be8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBlobDriverEnabled")
    def reset_blob_driver_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlobDriverEnabled", []))

    @jsii.member(jsii_name="resetDiskDriverEnabled")
    def reset_disk_driver_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskDriverEnabled", []))

    @jsii.member(jsii_name="resetDiskDriverVersion")
    def reset_disk_driver_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskDriverVersion", []))

    @jsii.member(jsii_name="resetFileDriverEnabled")
    def reset_file_driver_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileDriverEnabled", []))

    @jsii.member(jsii_name="resetSnapshotControllerEnabled")
    def reset_snapshot_controller_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotControllerEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="blobDriverEnabledInput")
    def blob_driver_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "blobDriverEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="diskDriverEnabledInput")
    def disk_driver_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "diskDriverEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="diskDriverVersionInput")
    def disk_driver_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskDriverVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="fileDriverEnabledInput")
    def file_driver_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fileDriverEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotControllerEnabledInput")
    def snapshot_controller_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "snapshotControllerEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="blobDriverEnabled")
    def blob_driver_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "blobDriverEnabled"))

    @blob_driver_enabled.setter
    def blob_driver_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2320929629f18adeb6850abb87a5a08258f79dcc74dc09d2991ececed9678eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blobDriverEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="diskDriverEnabled")
    def disk_driver_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "diskDriverEnabled"))

    @disk_driver_enabled.setter
    def disk_driver_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f197b6bc84a3766711012a400c9227bddb20b8307f1436646d8ff6ba93a1fa59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskDriverEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="diskDriverVersion")
    def disk_driver_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskDriverVersion"))

    @disk_driver_version.setter
    def disk_driver_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47567124e44288a0220038ca8e7d89b42712714c60dd55d67b00f06c052f74ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskDriverVersion", value)

    @builtins.property
    @jsii.member(jsii_name="fileDriverEnabled")
    def file_driver_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fileDriverEnabled"))

    @file_driver_enabled.setter
    def file_driver_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664c677745f13505a601d2f552ee4a4cc53793fa5606058c12b0539827f10b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileDriverEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotControllerEnabled")
    def snapshot_controller_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "snapshotControllerEnabled"))

    @snapshot_controller_enabled.setter
    def snapshot_controller_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aef6a1d692dc69b5fbade25a6e81f44c0f42ba27319e0cd30fff882653a494e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotControllerEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterStorageProfile]:
        return typing.cast(typing.Optional[KubernetesClusterStorageProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterStorageProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf62b1e2ad58bec65634bec5bec7741e3401a33d8823a744b63c9e38edb7c37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class KubernetesClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#create KubernetesCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#delete KubernetesCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#read KubernetesCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#update KubernetesCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbbbf1e369b91597cf9a6c5e089cc1b752794d4ad8e122c0fd6f57bc64dff54)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#create KubernetesCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#delete KubernetesCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#read KubernetesCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#update KubernetesCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b13d335fa96d8353b47fbac1dbf416d995939401d92b8f69a900ff6142af9a33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8eafcad85924ddd894ffeca52b9a3204cdcfda50446ed5cbd26f818556b31c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b34dad81e9617544311ea976cc86af964e22bde741def769b030f08b8c9ec96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d95fa08938125c77fadb738695a871bf6079ef3190dd1104249a0006f515b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b535cb51f4e8943a55c3444b7b86291796f8497a48b7dfe49b905ac18970ec39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KubernetesClusterTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KubernetesClusterTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KubernetesClusterTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816275d90510a8fc6e501ebdfd5594b350935f89492374f3be644509bab44f64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterWebAppRouting",
    jsii_struct_bases=[],
    name_mapping={"dns_zone_id": "dnsZoneId"},
)
class KubernetesClusterWebAppRouting:
    def __init__(self, *, dns_zone_id: builtins.str) -> None:
        '''
        :param dns_zone_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_zone_id KubernetesCluster#dns_zone_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc8e36a6a1403e5a55da6779e6fe55e40731d6d31e9655c1f891e5188075d78)
            check_type(argname="argument dns_zone_id", value=dns_zone_id, expected_type=type_hints["dns_zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns_zone_id": dns_zone_id,
        }

    @builtins.property
    def dns_zone_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_zone_id KubernetesCluster#dns_zone_id}.'''
        result = self._values.get("dns_zone_id")
        assert result is not None, "Required property 'dns_zone_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterWebAppRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterWebAppRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterWebAppRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__962c8c009f2b1157e8356c65c08b2481f72f6e63dfa3f57b373aaee2bb952a21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dnsZoneIdInput")
    def dns_zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsZoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsZoneId")
    def dns_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsZoneId"))

    @dns_zone_id.setter
    def dns_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36c91a3b0b5eb33c57a9eca365e88767527aca8830d2da7f60fe35e82c4e80cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsZoneId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterWebAppRouting]:
        return typing.cast(typing.Optional[KubernetesClusterWebAppRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterWebAppRouting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed202e3d569d4d06f6c5ac154d3dbb86d1cde469354c620c44768999e7a3834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterWindowsProfile",
    jsii_struct_bases=[],
    name_mapping={
        "admin_username": "adminUsername",
        "admin_password": "adminPassword",
        "gmsa": "gmsa",
        "license": "license",
    },
)
class KubernetesClusterWindowsProfile:
    def __init__(
        self,
        *,
        admin_username: builtins.str,
        admin_password: typing.Optional[builtins.str] = None,
        gmsa: typing.Optional[typing.Union["KubernetesClusterWindowsProfileGmsa", typing.Dict[builtins.str, typing.Any]]] = None,
        license: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_username KubernetesCluster#admin_username}.
        :param admin_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_password KubernetesCluster#admin_password}.
        :param gmsa: gmsa block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#gmsa KubernetesCluster#gmsa}
        :param license: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#license KubernetesCluster#license}.
        '''
        if isinstance(gmsa, dict):
            gmsa = KubernetesClusterWindowsProfileGmsa(**gmsa)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e52e4de9ffae2efad7f1a23e5e33fb56f204513c1fbfb77a872c85981fbab01)
            check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument gmsa", value=gmsa, expected_type=type_hints["gmsa"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_username": admin_username,
        }
        if admin_password is not None:
            self._values["admin_password"] = admin_password
        if gmsa is not None:
            self._values["gmsa"] = gmsa
        if license is not None:
            self._values["license"] = license

    @builtins.property
    def admin_username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_username KubernetesCluster#admin_username}.'''
        result = self._values.get("admin_username")
        assert result is not None, "Required property 'admin_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#admin_password KubernetesCluster#admin_password}.'''
        result = self._values.get("admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gmsa(self) -> typing.Optional["KubernetesClusterWindowsProfileGmsa"]:
        '''gmsa block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#gmsa KubernetesCluster#gmsa}
        '''
        result = self._values.get("gmsa")
        return typing.cast(typing.Optional["KubernetesClusterWindowsProfileGmsa"], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#license KubernetesCluster#license}.'''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterWindowsProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterWindowsProfileGmsa",
    jsii_struct_bases=[],
    name_mapping={"dns_server": "dnsServer", "root_domain": "rootDomain"},
)
class KubernetesClusterWindowsProfileGmsa:
    def __init__(self, *, dns_server: builtins.str, root_domain: builtins.str) -> None:
        '''
        :param dns_server: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_server KubernetesCluster#dns_server}.
        :param root_domain: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#root_domain KubernetesCluster#root_domain}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36bd0c91b8e72a2056406fa782c8f9fd0db193ccb0ca8a34b83688fd4df62f65)
            check_type(argname="argument dns_server", value=dns_server, expected_type=type_hints["dns_server"])
            check_type(argname="argument root_domain", value=root_domain, expected_type=type_hints["root_domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns_server": dns_server,
            "root_domain": root_domain,
        }

    @builtins.property
    def dns_server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_server KubernetesCluster#dns_server}.'''
        result = self._values.get("dns_server")
        assert result is not None, "Required property 'dns_server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#root_domain KubernetesCluster#root_domain}.'''
        result = self._values.get("root_domain")
        assert result is not None, "Required property 'root_domain' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterWindowsProfileGmsa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterWindowsProfileGmsaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterWindowsProfileGmsaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46ea2e620a40ffe0126a17f74e72ac5468fc246f0a7b3749db0a23286f24e5b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dnsServerInput")
    def dns_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsServerInput"))

    @builtins.property
    @jsii.member(jsii_name="rootDomainInput")
    def root_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServer")
    def dns_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsServer"))

    @dns_server.setter
    def dns_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d3df999401705360206106591ee466b9612c3327d7fa021caedad46723fba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServer", value)

    @builtins.property
    @jsii.member(jsii_name="rootDomain")
    def root_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootDomain"))

    @root_domain.setter
    def root_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40018fccf74b299550ad5fd279e1c539ea9b75e03cac363102f9838e72d9053c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootDomain", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterWindowsProfileGmsa]:
        return typing.cast(typing.Optional[KubernetesClusterWindowsProfileGmsa], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterWindowsProfileGmsa],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00ba80a1c26b1bd7d8d45b6734195cb5a365618f97d7154bdce0e1233dcc42c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KubernetesClusterWindowsProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterWindowsProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f000b757042ff5a36ba9d5683a7792698ecefc65d2b01af0907b9dc718bf66de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGmsa")
    def put_gmsa(self, *, dns_server: builtins.str, root_domain: builtins.str) -> None:
        '''
        :param dns_server: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#dns_server KubernetesCluster#dns_server}.
        :param root_domain: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#root_domain KubernetesCluster#root_domain}.
        '''
        value = KubernetesClusterWindowsProfileGmsa(
            dns_server=dns_server, root_domain=root_domain
        )

        return typing.cast(None, jsii.invoke(self, "putGmsa", [value]))

    @jsii.member(jsii_name="resetAdminPassword")
    def reset_admin_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPassword", []))

    @jsii.member(jsii_name="resetGmsa")
    def reset_gmsa(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGmsa", []))

    @jsii.member(jsii_name="resetLicense")
    def reset_license(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicense", []))

    @builtins.property
    @jsii.member(jsii_name="gmsa")
    def gmsa(self) -> KubernetesClusterWindowsProfileGmsaOutputReference:
        return typing.cast(KubernetesClusterWindowsProfileGmsaOutputReference, jsii.get(self, "gmsa"))

    @builtins.property
    @jsii.member(jsii_name="adminPasswordInput")
    def admin_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsernameInput")
    def admin_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="gmsaInput")
    def gmsa_input(self) -> typing.Optional[KubernetesClusterWindowsProfileGmsa]:
        return typing.cast(typing.Optional[KubernetesClusterWindowsProfileGmsa], jsii.get(self, "gmsaInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseInput")
    def license_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @admin_password.setter
    def admin_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__024e6d856244a4b6039e882ce365b4c15727dcc940c8af652c351525e607317c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPassword", value)

    @builtins.property
    @jsii.member(jsii_name="adminUsername")
    def admin_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminUsername"))

    @admin_username.setter
    def admin_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee579195b50bec99580298d0c3dc5101bd7590b167cf9c73ea3cb50730873a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUsername", value)

    @builtins.property
    @jsii.member(jsii_name="license")
    def license(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "license"))

    @license.setter
    def license(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e61a8f2e7b9fbee130ba6246ba67fd27eeb95fef712fdfbc24ae702b2ca8aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "license", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KubernetesClusterWindowsProfile]:
        return typing.cast(typing.Optional[KubernetesClusterWindowsProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterWindowsProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cde3a9ef2448f9862514550ceac571acb6a670289c56c0031314b205cc63ba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterWorkloadAutoscalerProfile",
    jsii_struct_bases=[],
    name_mapping={"keda_enabled": "kedaEnabled"},
)
class KubernetesClusterWorkloadAutoscalerProfile:
    def __init__(
        self,
        *,
        keda_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param keda_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#keda_enabled KubernetesCluster#keda_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e3c4199bfb704a8068c80eadeb69f30272bd04e54c9fcf95f0ef73e0a1c6f28)
            check_type(argname="argument keda_enabled", value=keda_enabled, expected_type=type_hints["keda_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if keda_enabled is not None:
            self._values["keda_enabled"] = keda_enabled

    @builtins.property
    def keda_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster#keda_enabled KubernetesCluster#keda_enabled}.'''
        result = self._values.get("keda_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesClusterWorkloadAutoscalerProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesClusterWorkloadAutoscalerProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kubernetesCluster.KubernetesClusterWorkloadAutoscalerProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8638b86e2633fc01bfeb155f3c019a0828a393a8fad8541d3e5e918a0d148993)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKedaEnabled")
    def reset_keda_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKedaEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="kedaEnabledInput")
    def keda_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "kedaEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="kedaEnabled")
    def keda_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "kedaEnabled"))

    @keda_enabled.setter
    def keda_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a627ca64b2a6437a846ab8b3fd68e330236ab89f6c78d021d97a3422fe84faed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kedaEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KubernetesClusterWorkloadAutoscalerProfile]:
        return typing.cast(typing.Optional[KubernetesClusterWorkloadAutoscalerProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KubernetesClusterWorkloadAutoscalerProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8dfc0a3cccb39c7830255676e89f7acd64b7bd5482b1a2d35ea573660f6d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "KubernetesCluster",
    "KubernetesClusterAciConnectorLinux",
    "KubernetesClusterAciConnectorLinuxOutputReference",
    "KubernetesClusterAutoScalerProfile",
    "KubernetesClusterAutoScalerProfileOutputReference",
    "KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl",
    "KubernetesClusterAzureActiveDirectoryRoleBasedAccessControlOutputReference",
    "KubernetesClusterConfig",
    "KubernetesClusterDefaultNodePool",
    "KubernetesClusterDefaultNodePoolKubeletConfig",
    "KubernetesClusterDefaultNodePoolKubeletConfigOutputReference",
    "KubernetesClusterDefaultNodePoolLinuxOsConfig",
    "KubernetesClusterDefaultNodePoolLinuxOsConfigOutputReference",
    "KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig",
    "KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfigOutputReference",
    "KubernetesClusterDefaultNodePoolOutputReference",
    "KubernetesClusterDefaultNodePoolUpgradeSettings",
    "KubernetesClusterDefaultNodePoolUpgradeSettingsOutputReference",
    "KubernetesClusterHttpProxyConfig",
    "KubernetesClusterHttpProxyConfigOutputReference",
    "KubernetesClusterIdentity",
    "KubernetesClusterIdentityOutputReference",
    "KubernetesClusterIngressApplicationGateway",
    "KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentity",
    "KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentityList",
    "KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentityOutputReference",
    "KubernetesClusterIngressApplicationGatewayOutputReference",
    "KubernetesClusterKeyVaultSecretsProvider",
    "KubernetesClusterKeyVaultSecretsProviderOutputReference",
    "KubernetesClusterKeyVaultSecretsProviderSecretIdentity",
    "KubernetesClusterKeyVaultSecretsProviderSecretIdentityList",
    "KubernetesClusterKeyVaultSecretsProviderSecretIdentityOutputReference",
    "KubernetesClusterKubeAdminConfig",
    "KubernetesClusterKubeAdminConfigList",
    "KubernetesClusterKubeAdminConfigOutputReference",
    "KubernetesClusterKubeConfig",
    "KubernetesClusterKubeConfigList",
    "KubernetesClusterKubeConfigOutputReference",
    "KubernetesClusterKubeletIdentity",
    "KubernetesClusterKubeletIdentityOutputReference",
    "KubernetesClusterLinuxProfile",
    "KubernetesClusterLinuxProfileOutputReference",
    "KubernetesClusterLinuxProfileSshKey",
    "KubernetesClusterLinuxProfileSshKeyOutputReference",
    "KubernetesClusterMaintenanceWindow",
    "KubernetesClusterMaintenanceWindowAllowed",
    "KubernetesClusterMaintenanceWindowAllowedList",
    "KubernetesClusterMaintenanceWindowAllowedOutputReference",
    "KubernetesClusterMaintenanceWindowNotAllowed",
    "KubernetesClusterMaintenanceWindowNotAllowedList",
    "KubernetesClusterMaintenanceWindowNotAllowedOutputReference",
    "KubernetesClusterMaintenanceWindowOutputReference",
    "KubernetesClusterMicrosoftDefender",
    "KubernetesClusterMicrosoftDefenderOutputReference",
    "KubernetesClusterMonitorMetrics",
    "KubernetesClusterMonitorMetricsOutputReference",
    "KubernetesClusterNetworkProfile",
    "KubernetesClusterNetworkProfileLoadBalancerProfile",
    "KubernetesClusterNetworkProfileLoadBalancerProfileOutputReference",
    "KubernetesClusterNetworkProfileNatGatewayProfile",
    "KubernetesClusterNetworkProfileNatGatewayProfileOutputReference",
    "KubernetesClusterNetworkProfileOutputReference",
    "KubernetesClusterOmsAgent",
    "KubernetesClusterOmsAgentOmsAgentIdentity",
    "KubernetesClusterOmsAgentOmsAgentIdentityList",
    "KubernetesClusterOmsAgentOmsAgentIdentityOutputReference",
    "KubernetesClusterOmsAgentOutputReference",
    "KubernetesClusterServicePrincipal",
    "KubernetesClusterServicePrincipalOutputReference",
    "KubernetesClusterStorageProfile",
    "KubernetesClusterStorageProfileOutputReference",
    "KubernetesClusterTimeouts",
    "KubernetesClusterTimeoutsOutputReference",
    "KubernetesClusterWebAppRouting",
    "KubernetesClusterWebAppRoutingOutputReference",
    "KubernetesClusterWindowsProfile",
    "KubernetesClusterWindowsProfileGmsa",
    "KubernetesClusterWindowsProfileGmsaOutputReference",
    "KubernetesClusterWindowsProfileOutputReference",
    "KubernetesClusterWorkloadAutoscalerProfile",
    "KubernetesClusterWorkloadAutoscalerProfileOutputReference",
]

publication.publish()

def _typecheckingstub__98ce399717b7c228e398ae9350214c956093962687d3c01a8de989177b29e827(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_node_pool: typing.Union[KubernetesClusterDefaultNodePool, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    aci_connector_linux: typing.Optional[typing.Union[KubernetesClusterAciConnectorLinux, typing.Dict[builtins.str, typing.Any]]] = None,
    api_server_authorized_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    automatic_channel_upgrade: typing.Optional[builtins.str] = None,
    auto_scaler_profile: typing.Optional[typing.Union[KubernetesClusterAutoScalerProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_active_directory_role_based_access_control: typing.Optional[typing.Union[KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_policy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_encryption_set_id: typing.Optional[builtins.str] = None,
    dns_prefix: typing.Optional[builtins.str] = None,
    dns_prefix_private_cluster: typing.Optional[builtins.str] = None,
    edge_zone: typing.Optional[builtins.str] = None,
    enable_pod_security_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_application_routing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_proxy_config: typing.Optional[typing.Union[KubernetesClusterHttpProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[KubernetesClusterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    image_cleaner_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    image_cleaner_interval_hours: typing.Optional[jsii.Number] = None,
    ingress_application_gateway: typing.Optional[typing.Union[KubernetesClusterIngressApplicationGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_secrets_provider: typing.Optional[typing.Union[KubernetesClusterKeyVaultSecretsProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    kubelet_identity: typing.Optional[typing.Union[KubernetesClusterKubeletIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes_version: typing.Optional[builtins.str] = None,
    linux_profile: typing.Optional[typing.Union[KubernetesClusterLinuxProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    local_account_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maintenance_window: typing.Optional[typing.Union[KubernetesClusterMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    microsoft_defender: typing.Optional[typing.Union[KubernetesClusterMicrosoftDefender, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_metrics: typing.Optional[typing.Union[KubernetesClusterMonitorMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    network_profile: typing.Optional[typing.Union[KubernetesClusterNetworkProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    node_resource_group: typing.Optional[builtins.str] = None,
    oidc_issuer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    oms_agent: typing.Optional[typing.Union[KubernetesClusterOmsAgent, typing.Dict[builtins.str, typing.Any]]] = None,
    open_service_mesh_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_cluster_public_fqdn_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_dns_zone_id: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    role_based_access_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_command_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    service_principal: typing.Optional[typing.Union[KubernetesClusterServicePrincipal, typing.Dict[builtins.str, typing.Any]]] = None,
    sku_tier: typing.Optional[builtins.str] = None,
    storage_profile: typing.Optional[typing.Union[KubernetesClusterStorageProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KubernetesClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    web_app_routing: typing.Optional[typing.Union[KubernetesClusterWebAppRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    windows_profile: typing.Optional[typing.Union[KubernetesClusterWindowsProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_autoscaler_profile: typing.Optional[typing.Union[KubernetesClusterWorkloadAutoscalerProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_identity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__582dde823364d3d292d3e328092b995493d5e15052d2787b0fbcc897c5f8d8ea(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c06e8a93744e65ea41f990989bea8872a7a93ae3f8ac1308e59268051ddeabd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715b4afd55737e18bb367c2ee549d29a43249d4daee1aa36dfe4c71922f4a1c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6554414a66e267cf74667cf0e7526a4a5695e3fdd16889992185ee5d1c3b7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47109014c1c82426bd297eeea58079adff001cd23810b7d89347066f2af615b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b952f0e07d1d7acb7a380e65b766993dc015c34784786a674c7a4b2051d78a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0133a8bf763049472f7020c0d0d6c212661ce152e4ece61711458e9ef318827d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855cc036ef4c003c092ddb519d49836d1759f8c87e01c9e690bf2b3fe624a180(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b94249a6afe6d2c098d7b88a99d27dbb0d0457309a399872b2f27a779e56f5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74e4aaa00d6360d9fc498b62c1ee6692ff384184b2802dd2db73e141ba4c079(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c80eaf170dd5942b27aa73b5dbec4fbc6c5c1f0709a4df4ac72602a27d43812(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d2712cef0529aacde86896e5b205f72805ba3ae79d88079e6af4e6c78a25fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4eb80977968be56080b990640a47520eedc5d2ccc1fa18564d74d438eae4809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0a09d5a9b07d01d348e9118ecd6f62ca52bf274b9e6182ad8d6ff2250407dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b22b38d2c019ce47a445aa4880fb44d853b5b27f2ad2077af7042bb11162154(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3abdf0464f7b181b2de336e9358946ef52b1ba90a67d51d48c44fd03bb65ac51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc5b0b484304154020fc2f13e3b347a8111dc0766ea3056be30fe707f52f3b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e538f940093aa6b614a5f229c1d340a39ef9c8a38393e084d05cc2fc530b1b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9989347c527d6e283c9182909b0f34eea00dd6fc3c503a4e7b2d5ec8f1c06a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3598725d46f205d0eccfe4d0ec77c57ff8f7fc831c94e5c8871957a68ae0857c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e27c52f23f5c9e3a832499e49a8ec5d54880eb52dd4dc94e647ff05dc98f15(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16f0a2df36b8f40eea1f0bd9224083135d6856d766b8e6411e102378a49d372(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28531ca8e8bfa87f36ed0279b0cc0c2cce76630fb78b6372df1ca852df42be13(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a781d10eb864942071a817e882239f815ed3fc79081cd31404e880b2a3117a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db7d6d55f0b710ef87479b188052fc6a28f7e40153c9c972d6a0077d8b7d8bf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bbb7e1aa822a26f760595ba13573c76f606f9b7a28ea8ccc1f85cdadfe09a4f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3f370bf96f12687f74553af6aece77b582d7ef104f8bf13a1d17f9821aa9fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb01a15967585abb6329ad24958c3917c0f89bf7001bef35f86a9a29cb8758c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69316152f2e32fc84978aae494d5ec2c5fe5bd1d3d92c239eaaa79ce1025ff95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607074898a400d1dbfc83ab061e17f21f4556d702ad0ce681441ad7002a1c528(
    *,
    subnet_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac60ae4df6361a52a41737fcc8ab5e9587a062e0291780393dbd018f1e2f5227(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5c8db946b148801ec10790ba71cd7bb298fd30a87b1113cb94414e69f19165(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e6dffa8a73b32ffa6bcf9ea4219c506b363ef7842278facb867e0908b3ffb1(
    value: typing.Optional[KubernetesClusterAciConnectorLinux],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831617a446d26cf4b19da83eeef042df1a97ed16a3bb453321366b344e56437e(
    *,
    balance_similar_node_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    empty_bulk_delete_max: typing.Optional[builtins.str] = None,
    expander: typing.Optional[builtins.str] = None,
    max_graceful_termination_sec: typing.Optional[builtins.str] = None,
    max_node_provisioning_time: typing.Optional[builtins.str] = None,
    max_unready_nodes: typing.Optional[jsii.Number] = None,
    max_unready_percentage: typing.Optional[jsii.Number] = None,
    new_pod_scale_up_delay: typing.Optional[builtins.str] = None,
    scale_down_delay_after_add: typing.Optional[builtins.str] = None,
    scale_down_delay_after_delete: typing.Optional[builtins.str] = None,
    scale_down_delay_after_failure: typing.Optional[builtins.str] = None,
    scale_down_unneeded: typing.Optional[builtins.str] = None,
    scale_down_unready: typing.Optional[builtins.str] = None,
    scale_down_utilization_threshold: typing.Optional[builtins.str] = None,
    scan_interval: typing.Optional[builtins.str] = None,
    skip_nodes_with_local_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_nodes_with_system_pods: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971c330a9a1f7db6f79d2c520a5b2ebb7d74da2f5affef53d178c57fee78b585(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07b403ece3b8d03e56ecdf59d7b1b49364882852ee37c2168a9f0c943e7b4eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5323f23d5746df83afd352319328535f447fbd57425a2982b84a67620bffd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01996b7de5515c40ffd236ad36c3111b0e0facaaa7ef5da6741a28ac8daa23c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78f4d5b97cd70f8cd3f132f6cbdbb9e69869566575183c43d17c868f06ff454(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556ef2ecb57013c5ade1fc1e8d3619252233b2dfcdad5505707aa48a82d25dba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f641f09ec31d69f4c5777fdc275830b3b8db14099fb59b551d7ce69827d19f3a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faeb880ccd1cf296f9b86c751688b712625b66737c122eb6a203b0b6f878834d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d00ddb62653bb7b367e88320c93a234ed48cfb2033eaf66adee1f6282711487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08997754a87e618e00409636e13a438bd2defb0347bef3fc9ef743f2415ec05f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f83619f675cb901fb9e4fdfdb93c97831969df75581adb26856bbca28fe5e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ceb97098b7f8e5c6ce6a16d6b356f595bedd029b4ece908880b1a4d666f65e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599239132e0e5d583629441c4aa4e134ef93022b6cb666cd24867ccc1ed860e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ab15a3ba35e0d059d9efdaba8d048aedc43f2139e62379d00889ed2a6cf8b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d07229cd3e2168445fae7b9fbf5bec73770d3b5bdc80e7abaacb5fd4dde357(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0673d144092e3d7e8869eda8f4ef23c9fea1d41633f8be6b938216c6196e2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7282f2ab8547698958ee19519035103b92439a8dbf6147633ab71b737ae6bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3af00c5c4b86c0681252d0c31fe094bad76535a48baeaa630dbf1211b45b68c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f30ca8ba54343404e43f706c87e1876e787a8680071dc8517cfb83e3e4f2814(
    value: typing.Optional[KubernetesClusterAutoScalerProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d8040b4e7c0b0f85eff013a32ec1b824579b9f264b11867ce58475fc2248a5(
    *,
    admin_group_object_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    azure_rbac_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_app_id: typing.Optional[builtins.str] = None,
    managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    server_app_id: typing.Optional[builtins.str] = None,
    server_app_secret: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb10bf7d3f0c6163bfe80e4bf6d152b4aed923ac32b74890e06529727a2a7c09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6330883a838c3f3331f4e2b7d7864c5e81d55d0589a866aa2c5a8873a98e6c4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69f0fb600eb03e1aa210e2db0c013ef22519879b67327891744c13cdf3052d3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36bfabfc303b7a0aca4d72f794b0c44395939ece0737a3f40044cc73c9ec35e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394f764bf5be8cbddb7e22eb0ba8a77bc33982899e67653a52322fd98a455154(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e0e447ec8891729725a2f0a66bc75fedfea2e14152c3ab8005ec3a2e8924d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec24a3c0b2afa1edb8e4212b8edd80faa462747c6de959b65fd0b0169520b6e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b71ce1a9fda8d8918500b3cacab804bfcbca2a3984dd45a92aff6e5268a127(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c788f2f29c0cba845a8a40bbfa9ee2785f1aa2cb3ec47272891aafb3120da0(
    value: typing.Optional[KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c27101fa956b9dcd1f20b6d95db8d4240a517affd5768be3aaf7f703c03223(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_node_pool: typing.Union[KubernetesClusterDefaultNodePool, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    aci_connector_linux: typing.Optional[typing.Union[KubernetesClusterAciConnectorLinux, typing.Dict[builtins.str, typing.Any]]] = None,
    api_server_authorized_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    automatic_channel_upgrade: typing.Optional[builtins.str] = None,
    auto_scaler_profile: typing.Optional[typing.Union[KubernetesClusterAutoScalerProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_active_directory_role_based_access_control: typing.Optional[typing.Union[KubernetesClusterAzureActiveDirectoryRoleBasedAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_policy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_encryption_set_id: typing.Optional[builtins.str] = None,
    dns_prefix: typing.Optional[builtins.str] = None,
    dns_prefix_private_cluster: typing.Optional[builtins.str] = None,
    edge_zone: typing.Optional[builtins.str] = None,
    enable_pod_security_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_application_routing_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_proxy_config: typing.Optional[typing.Union[KubernetesClusterHttpProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[KubernetesClusterIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    image_cleaner_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    image_cleaner_interval_hours: typing.Optional[jsii.Number] = None,
    ingress_application_gateway: typing.Optional[typing.Union[KubernetesClusterIngressApplicationGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_secrets_provider: typing.Optional[typing.Union[KubernetesClusterKeyVaultSecretsProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    kubelet_identity: typing.Optional[typing.Union[KubernetesClusterKubeletIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes_version: typing.Optional[builtins.str] = None,
    linux_profile: typing.Optional[typing.Union[KubernetesClusterLinuxProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    local_account_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maintenance_window: typing.Optional[typing.Union[KubernetesClusterMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    microsoft_defender: typing.Optional[typing.Union[KubernetesClusterMicrosoftDefender, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_metrics: typing.Optional[typing.Union[KubernetesClusterMonitorMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    network_profile: typing.Optional[typing.Union[KubernetesClusterNetworkProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    node_resource_group: typing.Optional[builtins.str] = None,
    oidc_issuer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    oms_agent: typing.Optional[typing.Union[KubernetesClusterOmsAgent, typing.Dict[builtins.str, typing.Any]]] = None,
    open_service_mesh_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_cluster_public_fqdn_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_dns_zone_id: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    role_based_access_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_command_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    service_principal: typing.Optional[typing.Union[KubernetesClusterServicePrincipal, typing.Dict[builtins.str, typing.Any]]] = None,
    sku_tier: typing.Optional[builtins.str] = None,
    storage_profile: typing.Optional[typing.Union[KubernetesClusterStorageProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KubernetesClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    web_app_routing: typing.Optional[typing.Union[KubernetesClusterWebAppRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    windows_profile: typing.Optional[typing.Union[KubernetesClusterWindowsProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_autoscaler_profile: typing.Optional[typing.Union[KubernetesClusterWorkloadAutoscalerProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_identity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d248b32efaf2c83899cf2b412ac01b6ccc4446edbca3b4294749a26d70073c(
    *,
    name: builtins.str,
    vm_size: builtins.str,
    capacity_reservation_group_id: typing.Optional[builtins.str] = None,
    custom_ca_trust_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_auto_scaling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_host_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_node_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_group_id: typing.Optional[builtins.str] = None,
    kubelet_config: typing.Optional[typing.Union[KubernetesClusterDefaultNodePoolKubeletConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    kubelet_disk_type: typing.Optional[builtins.str] = None,
    linux_os_config: typing.Optional[typing.Union[KubernetesClusterDefaultNodePoolLinuxOsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    max_count: typing.Optional[jsii.Number] = None,
    max_pods: typing.Optional[jsii.Number] = None,
    message_of_the_day: typing.Optional[builtins.str] = None,
    min_count: typing.Optional[jsii.Number] = None,
    node_count: typing.Optional[jsii.Number] = None,
    node_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_public_ip_prefix_id: typing.Optional[builtins.str] = None,
    node_taints: typing.Optional[typing.Sequence[builtins.str]] = None,
    only_critical_addons_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    orchestrator_version: typing.Optional[builtins.str] = None,
    os_disk_size_gb: typing.Optional[jsii.Number] = None,
    os_disk_type: typing.Optional[builtins.str] = None,
    os_sku: typing.Optional[builtins.str] = None,
    pod_subnet_id: typing.Optional[builtins.str] = None,
    proximity_placement_group_id: typing.Optional[builtins.str] = None,
    scale_down_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
    ultra_ssd_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    upgrade_settings: typing.Optional[typing.Union[KubernetesClusterDefaultNodePoolUpgradeSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    vnet_subnet_id: typing.Optional[builtins.str] = None,
    workload_runtime: typing.Optional[builtins.str] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35ae5283ebb4881dfe0c3bbeb03011e24335d939ae4594fed70911b5a4c73e5(
    *,
    allowed_unsafe_sysctls: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_log_max_line: typing.Optional[jsii.Number] = None,
    container_log_max_size_mb: typing.Optional[jsii.Number] = None,
    cpu_cfs_quota_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cpu_cfs_quota_period: typing.Optional[builtins.str] = None,
    cpu_manager_policy: typing.Optional[builtins.str] = None,
    image_gc_high_threshold: typing.Optional[jsii.Number] = None,
    image_gc_low_threshold: typing.Optional[jsii.Number] = None,
    pod_max_pid: typing.Optional[jsii.Number] = None,
    topology_manager_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d23d7f1b8a96888f61ef32252f843b356e991c9be48fc32eea0bd5ff17b1b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0db9bb5b927a4f98565eba754bf5f7f760f0c0e42c4774c8a09617cf31f599(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55637f8affe18fdd4da2913f89c0bb41da7faa05ad692f27c7a73c497085689(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d84f75340b829577ec847bb2b710efd21db508f0f9ea1b9a10e781e59a51975(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12dfdc57a5cd9bcb63adfbbcdb3fe466eb206f7f4b97ee93e9d7d68dbc2b0a5c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b11e95f2c6b483b1bf1fd1c23959471577de0a31e40142669bdc9899e75a00b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2519818b51889459629e8f207e26cf07bef60baca07e87a4f8efc50246d46f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db345a5ac0a3b0f18b32cad5dcd3baa2b5a6ce48df4d58919768bb4d7d5e38a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8b3525b5360583e80fdf23c945180c6fb0a2a237510baff86b4b0a416aff08(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d625cc17badb48c84ef7b6d93c869e06e2d1d9764575d1418012ba81862c2c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7414b340296f0737b288157465f88512a9d45cb94eb0be2d5b58bdcc43bc20ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83cb4d959d3a9c5bc5a1017a9df102e49edbde24489291c21c1e18d18c42097f(
    value: typing.Optional[KubernetesClusterDefaultNodePoolKubeletConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29391f8c0110df1b3beda37ff1b5618a7e9556770eb17f110051e374628e77ab(
    *,
    swap_file_size_mb: typing.Optional[jsii.Number] = None,
    sysctl_config: typing.Optional[typing.Union[KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    transparent_huge_page_defrag: typing.Optional[builtins.str] = None,
    transparent_huge_page_enabled: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee889a0e8ab4f258832efc4ca03a49d28129f7e1bf8758cec5f96444302a8b64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0112f13c42a4d74b4a6dca9403777f31f5cb722c7aa90436985b66ebecf4f33b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734557f0eb4267173567e5f5a0544a706a29f3c3cf6acc10403a0859edba3d64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f36bdf8bd9701655fc2f367857bfbc06984b045a043b8f1b6285117bd7d32f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27553b60bed8d410bac437d97999e495d61f69bee206db7636009c898eee013c(
    value: typing.Optional[KubernetesClusterDefaultNodePoolLinuxOsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e227dc27495a78cd0a014f0c5d59f7387bcc3f645f4219d7673ffaba224f86b8(
    *,
    fs_aio_max_nr: typing.Optional[jsii.Number] = None,
    fs_file_max: typing.Optional[jsii.Number] = None,
    fs_inotify_max_user_watches: typing.Optional[jsii.Number] = None,
    fs_nr_open: typing.Optional[jsii.Number] = None,
    kernel_threads_max: typing.Optional[jsii.Number] = None,
    net_core_netdev_max_backlog: typing.Optional[jsii.Number] = None,
    net_core_optmem_max: typing.Optional[jsii.Number] = None,
    net_core_rmem_default: typing.Optional[jsii.Number] = None,
    net_core_rmem_max: typing.Optional[jsii.Number] = None,
    net_core_somaxconn: typing.Optional[jsii.Number] = None,
    net_core_wmem_default: typing.Optional[jsii.Number] = None,
    net_core_wmem_max: typing.Optional[jsii.Number] = None,
    net_ipv4_ip_local_port_range_max: typing.Optional[jsii.Number] = None,
    net_ipv4_ip_local_port_range_min: typing.Optional[jsii.Number] = None,
    net_ipv4_neigh_default_gc_thresh1: typing.Optional[jsii.Number] = None,
    net_ipv4_neigh_default_gc_thresh2: typing.Optional[jsii.Number] = None,
    net_ipv4_neigh_default_gc_thresh3: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_fin_timeout: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_keepalive_intvl: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_keepalive_probes: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_keepalive_time: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_max_syn_backlog: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_max_tw_buckets: typing.Optional[jsii.Number] = None,
    net_ipv4_tcp_tw_reuse: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    net_netfilter_nf_conntrack_buckets: typing.Optional[jsii.Number] = None,
    net_netfilter_nf_conntrack_max: typing.Optional[jsii.Number] = None,
    vm_max_map_count: typing.Optional[jsii.Number] = None,
    vm_swappiness: typing.Optional[jsii.Number] = None,
    vm_vfs_cache_pressure: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29257c618a09308fee27c08fad289554a561c9959007d45046f0b7419b2761a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24cd78790b4aedca78b1cef0dd020aa4dd26290bf6f8db1d7e5328184dff20aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a7a556842c7e7c2c22eb46038660e2d890ff70238ced3964e022e20e3cd530(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37ed137129cbbd913010ebcbe57b6e13214afeec7fa1ff1eeb21f5af175d0cd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6968626339578a0531805cebef986281d18f61a7d41d1bf08c69d9c493baec5e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78048876a220cb18baa6251b170f82ee9f778ce9589dbbcd8749d693d3fedf8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606f352fa1673eb3e38fca4c9851934a0222404a1ef8ecbca83600fb1dd03712(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5efc4496a12d74abaa353b14846538819fb26cea23ffc6246a3dfa3a867672(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf298464245b8f8a64d8d28162e551c427021edd4ab9c7b75dd43daed72ffe7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37706c5f4abcdbce957518a62b0aee6227c44d3e37167c5643b8c92ffe53f7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5170c6d8748348cfd6016ea343fe9a44b9dcaecf14557fb8691be4eddb2361(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64733c79825ea41b191a7a4ac7ec82de89f733c6891c7f4784ab35c8f9ece1c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80154a4a484a7316b58baedc6e765889b85b6a2316e605d0b779c3ec5f9321a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a1a146ac423196842fa366622c5878d1fb0cb25a0e5f11b143fba206290ee7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa14f1b91360350821157bdede34d887a777a94af3cb91b1c7db3711313106b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5995f61d862d015049c0677a3cf2d9fec67d08b51f698f380fab33f17750eab6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e3817652350b9883f9617c20b548e3e8f5a775dd724a90a0d091cf5aec056e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25756de544dff80701aaef0b878c69c85a1ecb3fdeb1d855750e2d2c3abc124c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882158c91ca783c9628441c0d9256f5b2b4cd55bd85ada06e9ec20238cbbb506(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d223970369817426f7d46b700f704f9ed066bf053be9908f49a602426f5d8ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e55bf13c9236c2b20bf9ac4c8a1bb63b5c45ec6dfd2158109de0f320dd2f02(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e918f203fb04bb4b05e44c681d1c601403bd41c156586def822b2606ad099a40(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa2f71bf5c7f9e3dcd93d2b63115b4faa89dc0b9cb963ba0250a11c702b3dbc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4efcb4c7777621205f5d3c3bb0241484ea404efe9211e0f6ce47e26a8ad90a49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66596ae6471efcd1d7d145d150c2c1cf23d8756c4884e806f87d2fc0a9215305(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abba017c0453eafee42ad25fa75337fb2a946a7b5555385547062b4aef41491f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252963bf83ff0e5e45e31a424797c506f974e9d6a608bd9275b68f92e8cc37a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae293ada6f38ce6012bc9570a30e018f8c804c1dfb91b8d56cc953845e2ecf4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27ae8a304ee3c08cb51f6a50c2cda3056afb4b321d4980fbaa5a2cc8a9d7a1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca60947aae97a74c74f03506b70fb62d326740f62c8722260ce71f3104efeb9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c071ed9d77aa08a321e96b178e8f0b6af1abdec318bbf95c15c716c7c4b75361(
    value: typing.Optional[KubernetesClusterDefaultNodePoolLinuxOsConfigSysctlConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1558650cf24e910438d9a160d0b608b595b9c8adc3f93fc848091ee0ea393002(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc04931b19a071905f9cb3667f450373855a6b61f03c5e217c1f981f2c6517e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb19d08e6d45526869df1bd900950da119e036428856908186ffa9fb4d253525(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58386f1d80d82c49633255324888d6dd3aa901c4028705db77f3acdb4b686d05(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19ef0040f59768fe561e3465ccbfbb717c5466032961773a0da0a50a3a1d890(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136b7d6bc114a341cce30b7977e029925cc1e7dc931584dad7c0c25a1376c6c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba07c9330a54b3cc73ae3d87de5064037de5889841a21b815f81fe303568c28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba753d42db56769bdd51f8fecfba0281d67a50bbaf864dbb40ede032d3d9649(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974ec59932d0645542779d0de4466e10231bd31a63a4f57026228d288c22b807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53b8462abf8dcbbad396f537102da96abe6e656dfd5c68303a2aedf2a5890f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ca5117fbe35aa80bfe0c20da47761868e3d6c44aeaf4bfa7a5f881ea5f119e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b513163d177b1c69847dc399aacd07b99b101137dc74a662659fc632ff408c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39acbe85a98422f361b98810e8b81d82a1fc67e1642c97597ea9a3401f219825(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef5de2e71fafbdebb5d47a255d31dffcf486fb2b7facc46dc0806896e556719(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d937615f529b76811017519dff0c3cd46e2863f3f77a96465c56e9d67d829f19(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec79f7d1402cf8ab5aa05c460266d574b3310e0b09ad201c016c08a1360bc20(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b589d6a44660391076b19d22e0693cc865c84e926f3b3c62f81a152a3e071c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8af03e4ecb5462fbda675b53d648aae49e124980a8d8b9c2fc7aef18531f89(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc3f466b515f750600aa5adcbdb54b5e4102a3cf6e5cdd7c8b778510dfd327a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3181bf1ab5a4afe19e421c2a30599182b133e754d8303e3a3e2c4aab4e9f242f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc32a97ed9766d42ce65a80759cef14234b6eec6034d28319e58a3ae4e418374(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9606a87195767eea22661c4a3bdaa0ab882d0e141a5fd2fb3bcc0d009b43c617(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d36a79540c9cb9804da74cb1e2bf795466e8778cd28f991f5913ec9b799d479(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c25e8639549a7683664ffd913536ca0bef87029760377701f1874a7feb4c7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba125a1e127d4d978535d1c9957956869675ee8235ebb9c9c0ea796c6067f9b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11c98095c81f253787a416eb64f9571ce8203a08aafff47b29f7d76eadc2b14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fc2b558c3aa7cbf37a0896c95a61c5729289ca5259291f5a4bb997568bdcad(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e700fc2c79b6855b103d48ab98526c81e54a1cc7f494db2f83bfeb254194f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce2b6af8826dbb2059ef9a2d44d42e412e98a85f22309538040b3942272c26e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c672ba1b67e3df8e020f8595ddf621ac74814338643da2de2a13a4d4db926ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6563f4f702a6ee485c5e295f9db0f5933e16c9d86eda88de7f8c6eb60054c1e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36911dee20ff97d0e9b133472ace8e324cd4f5a8d703aec36c1830fdbe1a8418(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0de2703cc4c779950056ddf82e5546be9611f274eb2d615111daf976643eb7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86285f21bb79254cee2459ce790470bb88bf7e1dbd80d8c5cd3996e8e3a93aa4(
    value: typing.Optional[KubernetesClusterDefaultNodePool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae54277c4d532648f73822e0310f438ccece2a230bfabfbab63790f5296bf61(
    *,
    max_surge: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b83bac82fcde5a76cd3520a412118e4b3d5618a5d2291051fcbddfb60887cff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da6d8625a5823d2bd06afeb7278b48394799cbe912d8afa4ae288267781912c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7fe7bb2bb68fe30013bc109a0ccbe9bed5140dcbd37f6717720b11eac9ecbd8(
    value: typing.Optional[KubernetesClusterDefaultNodePoolUpgradeSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af0909251cf11f8f833f74912bb6bbae414ce55bdff403d8ac797fa6872e50e(
    *,
    http_proxy: typing.Optional[builtins.str] = None,
    https_proxy: typing.Optional[builtins.str] = None,
    no_proxy: typing.Optional[typing.Sequence[builtins.str]] = None,
    trusted_ca: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b955efe61167f21d4a8fc8a7f674636ed28f2137ebe2da40fdd8497fc756b56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae7ec78e4b5f51056f77af899f27aa2ce67d4d43456590fc5ea4f91213b53f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff6366db5353fe0c24a237af0a17c06c49cfaf278b3d3a15801d772a3b5beaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa319b54c9e47a23e844b487d974b4b500da7a97e4598569d8a6abf6cffe6af(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5d26c36626247dc9dc0ef5dce656b4c17ceef33460cfc2f021becba14697ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21bd20d24a411b7662822103b7979090bcf1b19bc74004a67b005e73c8ed1cc(
    value: typing.Optional[KubernetesClusterHttpProxyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebbe8d1d175e77d27b65e2cbdc93fd1d7e8243f0fe7d751a852050d2d0085bd(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aafd01285533951e1fd23f660a7261a6ce3044279ec40b56acf251b060cbcfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fd71ddad3995b4079c5f844930a44e5ca04c2c776312bba7997a9a28051d44(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9e7582cf43b0f8f1cc94d10ecb6bf2d977424399895cb6f3c03e76660ffc38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697893a1cc0de1b6d5db2d06732d91a8880b12f39eae0875e7fd9b2e2386a455(
    value: typing.Optional[KubernetesClusterIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52b210b26014cc6ce6aa05405d2c165f3243010a1f89465def1b3c2b2b0e96b(
    *,
    gateway_id: typing.Optional[builtins.str] = None,
    gateway_name: typing.Optional[builtins.str] = None,
    subnet_cidr: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0557bb63ffe6bdb4303604a8df18213ace0914901bb1d1a32db671083b6bac50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a470fddd7a44b95a1a44ed49327815df7ce8b52560f1bbbbcf28954240075a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8211ca2a3a0e6f146cea8c721b8676dfc597ba03a7e0ea2f561c18437a293946(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90243a83d738d348fde91655aaae204dea9fa3563cd3d581e93153686e6c6572(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf990ba44d217e33b311131e7dcaab2a89805f353c6689ca332c783950e30f03(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa4774773e9e102d5949ac2788f44ccf43059ee83ef664075f45172b095d88a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6653c2b845bdf4a522f690370f5a108da7d611eb37f3ca7ee95b062a7f29ddd(
    value: typing.Optional[KubernetesClusterIngressApplicationGatewayIngressApplicationGatewayIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556844747c742dbbea413143a04daf04bf6847749a6e38a9b4f79d8526ceb1cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3198dc068fdac2568df75bc8300cc5526a7fc46672d22a3830f163874b81f3ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bcf05d0ad050301303f4d7dbec2db13d1cb023d912d19507987c41e46c7a84d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7056c162a622665a773863617d74da0899810e7e1d30e1bc41d51fc1880610b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31de106c55cc5f777f7d86adc45eb0f8445c439423df68369fbe0fdef00d2830(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0575b484233cc2c2eac990d809d2047467054d1247dfb97d7021abc6f7ccc22(
    value: typing.Optional[KubernetesClusterIngressApplicationGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867f4869c30749b75f936a03661ecc4157644a6e5d891c1b77e4902317813611(
    *,
    secret_rotation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret_rotation_interval: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33eb5b4cdf75a282ef98182fb1e401be7f86fcdc9fb5b3428e13670a75e522ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b709a391b9660c651ce93ef4c2d02f252281de6e6f69a770239e0ae04ebcc11(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c426d1c60afd436b4622d503aa92e451e6a23116b13e90ef03882e1bb4c1cfe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e4c0e2256e3789519eb19ba6bce075ee52cd1d10e19791265877182e771926(
    value: typing.Optional[KubernetesClusterKeyVaultSecretsProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dacf0a744dc091da4266de3d361c1b1e2ea24834a4289327c27defe20f0ae94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86ad23778e3c0d75fddb412711bc55eef55d60e2d07862e836563cadf0ed162(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc5a925cfe25b32d5c72701cdcf4b61c9afa52e6763fa3521ffd3965a564a74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11fcb0066d2cb3435900edb1756802d3b6673c71d88544b1257219946cf4cd7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2301ff10ebbe02f7acacab35d231602de0512e34abaaf3496f46f78c0f24943(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499534eb3a36f01ed7d4ab9f76d516bd39b310546b22ac7eedfd6e9db2ce3614(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b397bff95d1e75db11931c343cd0d03893c0da2523cfc2d736986ac3561650(
    value: typing.Optional[KubernetesClusterKeyVaultSecretsProviderSecretIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f4b0a335823aefa8141d52cb5ac0fa9e4af8470d315ad6d1322e6fcc002ca9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ec5295dbf6d5b2e8c29d44f8044d383ebaadc804691a272e94b6ff44cb8615(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec770430e71abdc5c8306ce053a0ad10544b4e59c48c1325c10123d89adae1b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7e0490ceacd4c513ad62f16da90f3ef59a8c45fcf762bebc14f4eeb9788cf2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd1622b9da0cf110e1d825b85432ce8589bbe5588140e201a43d754a2c18114(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45428d6571444f3aa2c411f2938c9fb85fcdd3fd7583b559977f47777bc20f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2af61b3248fa6317c64a40e8e1d8e5b247b321ea23111bf031e3ab8a9164ee(
    value: typing.Optional[KubernetesClusterKubeAdminConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d276d4ec8be028ada289f8089ada085ec7742ccd61e134f93c517ed25148ff05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936d94ebf66b3e56c8bcc7f442c15cb7b34db056842ffba91ecec6275d1e689d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b55961579f2e9ea9492b86ec0458f7a78ccdbfa282de176dde5ae737939060(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021a44434bbd2a49203f30a8df1af18787284e52d3957dd0c2a14ae9581ac55a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17853465f08ea6a423706ded228accafabc5bae7c6a6d737c7effb42f426ac0e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4423b52fc19fd14ee048ed7b8644c39da5a95a7731ce631496940c4b9b16d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670869fb9c13c7f7c257f8dca1634b43d333c62344cbec1d52c69327be0f1c11(
    value: typing.Optional[KubernetesClusterKubeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596030cd7f36ba076f24601952972881a2910d69a8d725842f4b07d1f2054041(
    *,
    client_id: typing.Optional[builtins.str] = None,
    object_id: typing.Optional[builtins.str] = None,
    user_assigned_identity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5372b0b90633de07efe4c865397d55dd73c31f0103ecd673a10382f5a416e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a10adebfd1950f06bbdc1098c7b59a98fa32d83f75ec988c5b44ba7d644a78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c75e4c5e85cd19a2f808e187a10d70103da4dfa7d5973f37b3153f6b11ace5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c9bef3daf9609d108c85868db9196e23d1b15bab226ef3dcbd2755ac0118ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57c82e8a114c51b5f81163938be6ca7a883cc569b04eee15649dfba8d6a59a3(
    value: typing.Optional[KubernetesClusterKubeletIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557afa298a21f5e3e9235bb451faa98d7a30ffb6958a3f5d66eb25b0fd39f109(
    *,
    admin_username: builtins.str,
    ssh_key: typing.Union[KubernetesClusterLinuxProfileSshKey, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412104e73079dd5adca68d7c6853b89d98144bfa51090089418af31b0a8f61a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53837ba056ab9edf7bca665bba1311e99428141141d1a3ed1637569ad475f828(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694f22a0c6ef6bdf8fcf8bf4976e8c68c27fcc7a571e2eb04f77ff31d744bec0(
    value: typing.Optional[KubernetesClusterLinuxProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3103f9abfbe333f7d6fa1621e69368ead3606d669d3c8abc3e32b00e7f18a70b(
    *,
    key_data: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413243aed869640960f15ca73e6a451ff248743b4dc3f57746afc0680435ccc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2f23d5c2c8f5529115a709f43999b99745fcbe349cdb6422b5f39453c89bc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5981ddbc36ff23b936e45a298af5a82b89e16e13d5abc937a63fb88b9a3a80(
    value: typing.Optional[KubernetesClusterLinuxProfileSshKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e620fc6d5af60e4413a94f4f560137489625d1d21022fcf2bafce0d1b451b240(
    *,
    allowed: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesClusterMaintenanceWindowAllowed, typing.Dict[builtins.str, typing.Any]]]]] = None,
    not_allowed: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesClusterMaintenanceWindowNotAllowed, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b192ac3c1ddbcfdafa15e776e4d9a29941f0906f3518016a5e801d986697cd(
    *,
    day: builtins.str,
    hours: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b412a823f870e207e1e1d885b9c9578234f4d3fc29ad9ff35475442781ced9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2cb9cecfc4a04d67768f48c7b67bbeda50cfee0035800f3f543c6bd203e5cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb5450c84102af889afc8754cb73313bb4bae531cdee8e394fce74e9c55790a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd0bb451b9e81993b6c063f82906bd2b2a28791fc85b80684ffec6bffd4f52b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e37011adefe2ed899f33479101d6b0598ef179ce77cb31e904951694fec538(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d6f31af3db43b127625a3bc0bccdb13d87ea56fd0a4b9b9f59f003790221f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowAllowed]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec8620611447213d16de723a7767b62f70cab4ce3de49d8bfbda90edf70c470(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e2bf061fb483c729e4cfd620347d12b21b7b9c792085da8bb5e9e8348c4161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f500d13fd0f33f607f9fc6c0648a3a7e5cf9aeb3bf226e1b0a67a1c7c97b5e3c(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90deebe24decc889d10c36bf294a8a991e350f1252ae8fa7807ebfd6cbaec7ac(
    value: typing.Optional[typing.Union[KubernetesClusterMaintenanceWindowAllowed, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662d46c75a06e22ea7735591c2cb2bf7739da5d42d6081ca02313c91f1b4370b(
    *,
    end: builtins.str,
    start: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3545f37a706ec4a8a76461c4993768f50ea4e73db3ca427160e9e1282176d5dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059dbe1b82a48e34819282740cc6b370f3d58b2b951f1435bf6d425b87394c88(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02d16ba2597b30f0d9fb68af85bda38559329cfcda5c2427f09861f75549e4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f62fbfdbf3210a4aee22cde58c90a1cfbc6bff49532891b2244ddcc80da55c2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73da76594cdcb53ba4e7c3c29f725c793ee78c48a023cb03d613b9f57f04df5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15724ff63c3e3b2883c0322f47304cd2078fa5e7736733910aaaa01a1adbff72(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KubernetesClusterMaintenanceWindowNotAllowed]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37eb76f4d3a555f64770d91fbd2bf1954ca81387eb027309735f8af463071882(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ee279c06b33f1f28346bf942de7a46c761a0bbc9255915831c5720e2fe1fd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0392c2cefb06712557adcf029a78e03eae06ff69b931183ce25039f97a1ddf9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71707e9deed18a5f320700cd86562b6bbef6bd7a69162a10741418e49db39de(
    value: typing.Optional[typing.Union[KubernetesClusterMaintenanceWindowNotAllowed, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b271da19b311d67d53f9f3cf97122c0a626cfe0e715f05e547235554d28957(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aadc806a8423bdb09003e6a0afd258868532f64d8d8fca84419749449063613(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesClusterMaintenanceWindowAllowed, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e11286b7262df6e8f96badced69b4c5438a49a74f5be311c5f847ef9980a7fa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KubernetesClusterMaintenanceWindowNotAllowed, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a08687c68adaa177b022847ca11674db44407596d1803383d989465b9cb45d6(
    value: typing.Optional[KubernetesClusterMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083c7c2416298c9d99cfd18c635950df112c5583290ca653505edc307373c0d6(
    *,
    log_analytics_workspace_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7955d64ea082862c9a8376bac8f04b6a6b74754b575f798f3e9579b2d7bb079c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c87ad9675dc8e0efc93f4d537a7f559415135b26e1fb2153586344945fbbe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51b00c57742a92f5d10e273ebb4d772953fba65f7b3c1eb1be71d94f5ec960a(
    value: typing.Optional[KubernetesClusterMicrosoftDefender],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6288c0c064236591bb73e3eb9a38a0e777f4c69e2ade10fe560d8c10455433(
    *,
    annotations_allowed: typing.Optional[builtins.str] = None,
    labels_allowed: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c82493b085ea6a91e17eef77cdacced60767dfe4c9a358b0db5446226f2662(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5acf1e4ee67cfbdaa580b0bb5dd0a1822a37818ff868e7257b3ef8300cabc3f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195a492016692a9eb5334e8bdd6439dff32dfa46e852aae6207afe5f68687d57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a386f946582505de73537085c3a57380f3330bf837f6f7a496f46cdf0eb7e9fb(
    value: typing.Optional[KubernetesClusterMonitorMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee8dd7146ebdd597ec5585057aea38455e0531a7be1f0ff33964223da9f99db(
    *,
    network_plugin: builtins.str,
    dns_service_ip: typing.Optional[builtins.str] = None,
    docker_bridge_cidr: typing.Optional[builtins.str] = None,
    ebpf_data_plane: typing.Optional[builtins.str] = None,
    ip_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    load_balancer_profile: typing.Optional[typing.Union[KubernetesClusterNetworkProfileLoadBalancerProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancer_sku: typing.Optional[builtins.str] = None,
    nat_gateway_profile: typing.Optional[typing.Union[KubernetesClusterNetworkProfileNatGatewayProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    network_mode: typing.Optional[builtins.str] = None,
    network_plugin_mode: typing.Optional[builtins.str] = None,
    network_policy: typing.Optional[builtins.str] = None,
    outbound_type: typing.Optional[builtins.str] = None,
    pod_cidr: typing.Optional[builtins.str] = None,
    pod_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_cidr: typing.Optional[builtins.str] = None,
    service_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e83523dc4eb212b800322c3a9cb717e713cedcbf9be86e251cf107828c8fa8(
    *,
    idle_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    managed_outbound_ip_count: typing.Optional[jsii.Number] = None,
    managed_outbound_ipv6_count: typing.Optional[jsii.Number] = None,
    outbound_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    outbound_ip_prefix_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    outbound_ports_allocated: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a33c76d84e027198b1b3ce8c4ce33d0fc79259ba1f444257d110ebf9cca48db5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531bb23c83838f870e5174073389cfd3d78aa1c1fd0316cdcbf1f0593dfe9c2c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1e286b2f78ea015b8cfd4915873b667dfd1c013f1eeac15c598c93cd71d57d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612aebee85969c3ede2b2ac3e78f1da7a692fb0a30e1dbe152407eab29e93fcd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5d49c417c850affd668a9a9724b59684f5c8f96228931fb239469ce0e8b7f8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c44deb60b6ad341c6b107e3c959ec2dc9411cb055ff5ad7dc87402451e17fcd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1620ad06ee45d2859cf8014cb317a16423f7010823ff0dc6aede620582380f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e79757d6ff27c3745cde5cec4be673803be2c3a0b20da8908bf82103c9e78d(
    value: typing.Optional[KubernetesClusterNetworkProfileLoadBalancerProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63a1c52f508c3b522d4afae369a55ca9fe5879a1d5209b8b6df3f41fbca5a00(
    *,
    idle_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    managed_outbound_ip_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca670a2f4cded42bb183d95c225a3cc6959a8f75b468ff0bd814bd36617a5ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0539af7835e609331d03701613281d65030d6fdddd8529a9160d48e29ca98ebb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58545ade43fd69737748707a706a50aabb0bf20014fa90ba5a3b1910e7b6b26d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6d1eb7560807370019cc5e0797ef9476105b6770e6333b158504a51b85e339(
    value: typing.Optional[KubernetesClusterNetworkProfileNatGatewayProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5caa63a1bf89c917cf97df5f9f03548c605de0becd3098ea8f28964c8531d5e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75cb1d94e54da5ecdb14112c5cb1588091a1c9a18632d2144c34587ee07f49d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0996332d94b64a60663c484b325d9344a223b454cfdb4d1b33d27331188a9f4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a02dd190756cfeb958ec9e3eecab3bb6a515d49f5ad7adc532c33d4316b09dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa59945f23f6ff5568e149f0fe50289ba276963f29779ac0b1ba818775a8e99c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1464aa08bba5db2dcba7c2a81ff4d722a2660fb84a757e83fae9638927da430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c13b70b39c6e53d1b355583357bd40a3f4c5db1f13e0a07de9759b811f55e35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77dbfb8ac8e2efe8b64e2bf6abf7d0698b45ccabc447ef6a6fe1937f1f4891d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a43dd8542c74ce06e2c73cb4b33d5d7e43f957909d67f7c60779de12a3e2dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9cbc3a929f29af081f1d9ae40a54d7eb78810e200756d35dc61a9911ea8f08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e62e57874e5c16aaa286e92fed5cebb853cf6c7bb37024923a2de8f3a4b7259(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9913b0d99912b2f0c861d04702dec12149be1781a96e353c5037ae16893fd8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9847cd1f70f8d9e9fc09fc57e28f691f11df8030074f4ea58d10d01fbe9882d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312f2999204fabeb35f90035dcd578138c43794df782edc80f688202d520c42c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e919dec016c7a0f841c42409d2392ce88cb611ec517d534848fb7f12df3d2c59(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7500eb2b721df6d6322d02685709f38c7141275198f7a3cd7d82298c045e6b58(
    value: typing.Optional[KubernetesClusterNetworkProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f84ad6672e0a6753be9e68d7dff07b264beb3521d185e86b84c57389cb78a4(
    *,
    log_analytics_workspace_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93463e7e7482f515421bca1421d7b39500abdcfc0c4f6fa2916bec5852a992e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb388fdd6e35db6a4dcd2ef565a0df59bbbdd21647ef4a2a45aaad95ed4053d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfbb0d375bf0c2cdf4d819f0b5e73bdb61d797179c194d4abbef0dadf9b23c93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f66e395ec24bb3bff3731c40cd149e745528b52009a44b234c0448843e21c7f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff41dc0e67546558e1f18623accb8e861de8dda0e627cdccd886e97b34a28d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d4dc4e4a0e3646f0fe04a15ef73e736b56f2703c6fb30ee1680717ef981194(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b0dec128c3ff52c892a81a2a30d9a176348147f0f656b50bacf62fed08e029(
    value: typing.Optional[KubernetesClusterOmsAgentOmsAgentIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1cf2b2dec18589073e74316eab96c0f92705cff8520301d4938328ed5961cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b82fdb3a68c31b2630655044fb0c3f2bc64b1387588de89f86e7621b6905a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edd6876d6431792f28b11e7008b3044a3cc4a8ba91719f9740de84ca29669fb(
    value: typing.Optional[KubernetesClusterOmsAgent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27a6ad5302f87187270a018540ec56cff3453aa93864bfbb76a40dc951e521a(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0887a95e43e382523b37bebb5d6585442b8b79211302cca927b24a4804d6cc20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa656da888f9b69b5749ff1a6e74fc1d8de86f4610208dd5278623624e0bde2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b614cdc34167b0ed19eebc684f4012e45a12f7f6cc5bd490d7da80eb1fda566e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ced64758f09c56499ed3455b1d618d42a5f0f939a1d85dc85b59b6d680833f(
    value: typing.Optional[KubernetesClusterServicePrincipal],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90da5eedfd0735040239804ee62907180ec96aaea00d7fdf57cc1fb3a7ef12ca(
    *,
    blob_driver_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_driver_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_driver_version: typing.Optional[builtins.str] = None,
    file_driver_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snapshot_controller_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c005ba9c6e4392f63ac99866f02065969864b4c8a95547cdcd1e15a48e8d2be8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2320929629f18adeb6850abb87a5a08258f79dcc74dc09d2991ececed9678eff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f197b6bc84a3766711012a400c9227bddb20b8307f1436646d8ff6ba93a1fa59(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47567124e44288a0220038ca8e7d89b42712714c60dd55d67b00f06c052f74ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664c677745f13505a601d2f552ee4a4cc53793fa5606058c12b0539827f10b1a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aef6a1d692dc69b5fbade25a6e81f44c0f42ba27319e0cd30fff882653a494e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf62b1e2ad58bec65634bec5bec7741e3401a33d8823a744b63c9e38edb7c37(
    value: typing.Optional[KubernetesClusterStorageProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbbbf1e369b91597cf9a6c5e089cc1b752794d4ad8e122c0fd6f57bc64dff54(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13d335fa96d8353b47fbac1dbf416d995939401d92b8f69a900ff6142af9a33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8eafcad85924ddd894ffeca52b9a3204cdcfda50446ed5cbd26f818556b31c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b34dad81e9617544311ea976cc86af964e22bde741def769b030f08b8c9ec96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d95fa08938125c77fadb738695a871bf6079ef3190dd1104249a0006f515b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b535cb51f4e8943a55c3444b7b86291796f8497a48b7dfe49b905ac18970ec39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816275d90510a8fc6e501ebdfd5594b350935f89492374f3be644509bab44f64(
    value: typing.Optional[typing.Union[KubernetesClusterTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc8e36a6a1403e5a55da6779e6fe55e40731d6d31e9655c1f891e5188075d78(
    *,
    dns_zone_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962c8c009f2b1157e8356c65c08b2481f72f6e63dfa3f57b373aaee2bb952a21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c91a3b0b5eb33c57a9eca365e88767527aca8830d2da7f60fe35e82c4e80cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed202e3d569d4d06f6c5ac154d3dbb86d1cde469354c620c44768999e7a3834(
    value: typing.Optional[KubernetesClusterWebAppRouting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e52e4de9ffae2efad7f1a23e5e33fb56f204513c1fbfb77a872c85981fbab01(
    *,
    admin_username: builtins.str,
    admin_password: typing.Optional[builtins.str] = None,
    gmsa: typing.Optional[typing.Union[KubernetesClusterWindowsProfileGmsa, typing.Dict[builtins.str, typing.Any]]] = None,
    license: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36bd0c91b8e72a2056406fa782c8f9fd0db193ccb0ca8a34b83688fd4df62f65(
    *,
    dns_server: builtins.str,
    root_domain: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ea2e620a40ffe0126a17f74e72ac5468fc246f0a7b3749db0a23286f24e5b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d3df999401705360206106591ee466b9612c3327d7fa021caedad46723fba5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40018fccf74b299550ad5fd279e1c539ea9b75e03cac363102f9838e72d9053c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00ba80a1c26b1bd7d8d45b6734195cb5a365618f97d7154bdce0e1233dcc42c(
    value: typing.Optional[KubernetesClusterWindowsProfileGmsa],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f000b757042ff5a36ba9d5683a7792698ecefc65d2b01af0907b9dc718bf66de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024e6d856244a4b6039e882ce365b4c15727dcc940c8af652c351525e607317c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee579195b50bec99580298d0c3dc5101bd7590b167cf9c73ea3cb50730873a69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e61a8f2e7b9fbee130ba6246ba67fd27eeb95fef712fdfbc24ae702b2ca8aba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cde3a9ef2448f9862514550ceac571acb6a670289c56c0031314b205cc63ba0(
    value: typing.Optional[KubernetesClusterWindowsProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3c4199bfb704a8068c80eadeb69f30272bd04e54c9fcf95f0ef73e0a1c6f28(
    *,
    keda_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8638b86e2633fc01bfeb155f3c019a0828a393a8fad8541d3e5e918a0d148993(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a627ca64b2a6437a846ab8b3fd68e330236ab89f6c78d021d97a3422fe84faed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8dfc0a3cccb39c7830255676e89f7acd64b7bd5482b1a2d35ea573660f6d61(
    value: typing.Optional[KubernetesClusterWorkloadAutoscalerProfile],
) -> None:
    """Type checking stubs"""
    pass
