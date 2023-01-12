'''
# Terraform CDK opentelekomcloud Provider ~> 1.26

This repo builds and publishes the Terraform opentelekomcloud Provider bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-opentelekomcloud](https://www.npmjs.com/package/@cdktf/provider-opentelekomcloud).

`npm install @cdktf/provider-opentelekomcloud`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-opentelekomcloud](https://pypi.org/project/cdktf-cdktf-provider-opentelekomcloud).

`pipenv install cdktf-cdktf-provider-opentelekomcloud`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Opentelekomcloud](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Opentelekomcloud).

`dotnet add package HashiCorp.Cdktf.Providers.Opentelekomcloud`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-opentelekomcloud](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-opentelekomcloud).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-opentelekomcloud</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-opentelekomcloud-go`](https://github.com/cdktf/cdktf-provider-opentelekomcloud-go) package.

`go get github.com/cdktf/cdktf-provider-opentelekomcloud-go/opentelekomcloud`

## Docs

Find auto-generated docs for this provider here: [./API.md](./API.md)
You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-opentelekomcloud).

## Versioning

This project is explicitly not tracking the Terraform opentelekomcloud Provider version 1:1. In fact, it always tracks `latest` of `~> 1.26` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform opentelekomcloud Provider](https://github.com/terraform-providers/terraform-provider-opentelekomcloud)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [terraform cdk](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### projen

This is mostly based on [projen](https://github.com/eladb/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on projen

There's a custom [project builder](https://github.com/hashicorp/cdktf-provider-project) which encapsulate the common settings for all `cdktf` providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [Repository Manager](https://github.com/hashicorp/cdktf-repository-manager/)
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

from ._jsii import *

__all__ = [
    "antiddos_v1",
    "as_configuration_v1",
    "as_group_v1",
    "as_policy_v1",
    "as_policy_v2",
    "blockstorage_volume_v2",
    "cbr_policy_v3",
    "cbr_vault_v3",
    "cce_addon_v3",
    "cce_cluster_v3",
    "cce_node_pool_v3",
    "cce_node_v3",
    "ces_alarmrule",
    "compute_bms_server_v2",
    "compute_bms_tags_v2",
    "compute_floatingip_associate_v2",
    "compute_floatingip_v2",
    "compute_instance_v2",
    "compute_keypair_v2",
    "compute_secgroup_v2",
    "compute_servergroup_v2",
    "compute_volume_attach_v2",
    "csbs_backup_policy_v1",
    "csbs_backup_v1",
    "css_cluster_v1",
    "css_snapshot_configuration_v1",
    "cts_event_notification_v3",
    "cts_tracker_v1",
    "data_opentelekomcloud_antiddos_v1",
    "data_opentelekomcloud_cbr_backup_ids_v3",
    "data_opentelekomcloud_cbr_backup_v3",
    "data_opentelekomcloud_cce_addon_template_v3",
    "data_opentelekomcloud_cce_cluster_kubeconfig_v3",
    "data_opentelekomcloud_cce_cluster_v3",
    "data_opentelekomcloud_cce_node_ids_v3",
    "data_opentelekomcloud_cce_node_v3",
    "data_opentelekomcloud_compute_availability_zones_v2",
    "data_opentelekomcloud_compute_bms_flavors_v2",
    "data_opentelekomcloud_compute_bms_keypairs_v2",
    "data_opentelekomcloud_compute_bms_nic_v2",
    "data_opentelekomcloud_compute_bms_server_v2",
    "data_opentelekomcloud_compute_flavor_v2",
    "data_opentelekomcloud_compute_instance_v2",
    "data_opentelekomcloud_csbs_backup_policy_v1",
    "data_opentelekomcloud_csbs_backup_v1",
    "data_opentelekomcloud_css_flavor_v1",
    "data_opentelekomcloud_cts_tracker_v1",
    "data_opentelekomcloud_dcs_az_v1",
    "data_opentelekomcloud_dcs_maintainwindow_v1",
    "data_opentelekomcloud_dcs_product_v1",
    "data_opentelekomcloud_dds_flavors_v3",
    "data_opentelekomcloud_dds_instance_v3",
    "data_opentelekomcloud_deh_host_v1",
    "data_opentelekomcloud_deh_server_v1",
    "data_opentelekomcloud_dms_az_v1",
    "data_opentelekomcloud_dms_maintainwindow_v1",
    "data_opentelekomcloud_dms_product_v1",
    "data_opentelekomcloud_dns_nameservers_v2",
    "data_opentelekomcloud_dns_zone_v2",
    "data_opentelekomcloud_identity_agency_v3",
    "data_opentelekomcloud_identity_auth_scope_v3",
    "data_opentelekomcloud_identity_credential_v3",
    "data_opentelekomcloud_identity_group_v3",
    "data_opentelekomcloud_identity_project_v3",
    "data_opentelekomcloud_identity_projects_v3",
    "data_opentelekomcloud_identity_role_custom_v3",
    "data_opentelekomcloud_identity_role_v3",
    "data_opentelekomcloud_identity_user_v3",
    "data_opentelekomcloud_images_image_v2",
    "data_opentelekomcloud_kms_data_key_v1",
    "data_opentelekomcloud_kms_key_v1",
    "data_opentelekomcloud_lb_certificate_v3",
    "data_opentelekomcloud_lb_flavor_v3",
    "data_opentelekomcloud_lb_flavors_v3",
    "data_opentelekomcloud_lb_listener_v3",
    "data_opentelekomcloud_lb_loadbalancer_v3",
    "data_opentelekomcloud_lb_member_ids_v2",
    "data_opentelekomcloud_networking_network_v2",
    "data_opentelekomcloud_networking_port_v2",
    "data_opentelekomcloud_networking_secgroup_rule_ids_v2",
    "data_opentelekomcloud_networking_secgroup_v2",
    "data_opentelekomcloud_obs_bucket",
    "data_opentelekomcloud_obs_bucket_object",
    "data_opentelekomcloud_rds_backup_v3",
    "data_opentelekomcloud_rds_flavors_v1",
    "data_opentelekomcloud_rds_flavors_v3",
    "data_opentelekomcloud_rds_instance_v3",
    "data_opentelekomcloud_rds_versions_v3",
    "data_opentelekomcloud_rts_software_config_v1",
    "data_opentelekomcloud_rts_software_deployment_v1",
    "data_opentelekomcloud_rts_stack_resource_v1",
    "data_opentelekomcloud_rts_stack_v1",
    "data_opentelekomcloud_s3_bucket_object",
    "data_opentelekomcloud_sdrs_domain_v1",
    "data_opentelekomcloud_sfs_file_system_v2",
    "data_opentelekomcloud_sfs_turbo_share_v1",
    "data_opentelekomcloud_vbs_backup_policy_v2",
    "data_opentelekomcloud_vbs_backup_v2",
    "data_opentelekomcloud_vpc_bandwidth",
    "data_opentelekomcloud_vpc_bandwidth_v2",
    "data_opentelekomcloud_vpc_eip_v1",
    "data_opentelekomcloud_vpc_peering_connection_v2",
    "data_opentelekomcloud_vpc_route_ids_v2",
    "data_opentelekomcloud_vpc_route_v2",
    "data_opentelekomcloud_vpc_subnet_ids_v1",
    "data_opentelekomcloud_vpc_subnet_v1",
    "data_opentelekomcloud_vpc_v1",
    "data_opentelekomcloud_vpcep_public_service_v1",
    "data_opentelekomcloud_vpcep_service_v1",
    "data_opentelekomcloud_vpnaas_service_v2",
    "dcs_instance_v1",
    "dds_instance_v3",
    "deh_host_v1",
    "dms_instance_v1",
    "dms_topic_v1",
    "dns_ptrrecord_v2",
    "dns_recordset_v2",
    "dns_zone_v2",
    "ecs_instance_v1",
    "evs_volume_v3",
    "fw_firewall_group_v2",
    "fw_policy_v2",
    "fw_rule_v2",
    "identity_agency_v3",
    "identity_credential_v3",
    "identity_group_membership_v3",
    "identity_group_v3",
    "identity_mapping_v3",
    "identity_project_v3",
    "identity_protocol_v3",
    "identity_provider_v3",
    "identity_role_assignment_v3",
    "identity_role_v3",
    "identity_user_group_membership_v3",
    "identity_user_v3",
    "images_image_access_accept_v2",
    "images_image_access_v2",
    "images_image_v2",
    "ims_data_image_v2",
    "ims_image_v2",
    "kms_grant_v1",
    "kms_key_v1",
    "lb_certificate_v2",
    "lb_certificate_v3",
    "lb_l7_policy_v2",
    "lb_l7_rule_v2",
    "lb_listener_v2",
    "lb_listener_v3",
    "lb_loadbalancer_v2",
    "lb_loadbalancer_v3",
    "lb_member_v2",
    "lb_member_v3",
    "lb_monitor_v2",
    "lb_monitor_v3",
    "lb_policy_v3",
    "lb_pool_v2",
    "lb_pool_v3",
    "lb_rule_v3",
    "lb_whitelist_v2",
    "logtank_group_v2",
    "logtank_topic_v2",
    "mrs_cluster_v1",
    "mrs_job_v1",
    "nat_dnat_rule_v2",
    "nat_gateway_v2",
    "nat_snat_rule_v2",
    "networking_floatingip_associate_v2",
    "networking_floatingip_v2",
    "networking_network_v2",
    "networking_port_v2",
    "networking_router_interface_v2",
    "networking_router_route_v2",
    "networking_router_v2",
    "networking_secgroup_rule_v2",
    "networking_secgroup_v2",
    "networking_subnet_v2",
    "networking_vip_associate_v2",
    "networking_vip_v2",
    "obs_bucket",
    "obs_bucket_object",
    "obs_bucket_policy",
    "provider",
    "rds_instance_v1",
    "rds_instance_v3",
    "rds_parametergroup_v3",
    "rds_read_replica_v3",
    "rts_software_config_v1",
    "rts_software_deployment_v1",
    "rts_stack_v1",
    "s3_bucket",
    "s3_bucket_object",
    "s3_bucket_policy",
    "sdrs_protected_instance_v1",
    "sdrs_protectiongroup_v1",
    "sfs_file_system_v2",
    "sfs_share_access_rules_v2",
    "sfs_turbo_share_v1",
    "smn_subscription_v2",
    "smn_topic_attribute_v2",
    "smn_topic_v2",
    "swr_domain_v2",
    "swr_organization_permissions_v2",
    "swr_organization_v2",
    "swr_repository_v2",
    "vbs_backup_policy_v2",
    "vbs_backup_share_v2",
    "vbs_backup_v2",
    "vpc_bandwidth_associate_v2",
    "vpc_bandwidth_v2",
    "vpc_eip_v1",
    "vpc_flow_log_v1",
    "vpc_peering_connection_accepter_v2",
    "vpc_peering_connection_v2",
    "vpc_route_v2",
    "vpc_subnet_v1",
    "vpc_v1",
    "vpcep_endpoint_v1",
    "vpcep_service_v1",
    "vpnaas_endpoint_group_v2",
    "vpnaas_ike_policy_v2",
    "vpnaas_ipsec_policy_v2",
    "vpnaas_service_v2",
    "vpnaas_site_connection_v2",
    "waf_alarm_notification_v1",
    "waf_ccattackprotection_rule_v1",
    "waf_certificate_v1",
    "waf_datamasking_rule_v1",
    "waf_domain_v1",
    "waf_falsealarmmasking_rule_v1",
    "waf_policy_v1",
    "waf_preciseprotection_rule_v1",
    "waf_webtamperprotection_rule_v1",
    "waf_whiteblackip_rule_v1",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import antiddos_v1
from . import as_configuration_v1
from . import as_group_v1
from . import as_policy_v1
from . import as_policy_v2
from . import blockstorage_volume_v2
from . import cbr_policy_v3
from . import cbr_vault_v3
from . import cce_addon_v3
from . import cce_cluster_v3
from . import cce_node_pool_v3
from . import cce_node_v3
from . import ces_alarmrule
from . import compute_bms_server_v2
from . import compute_bms_tags_v2
from . import compute_floatingip_associate_v2
from . import compute_floatingip_v2
from . import compute_instance_v2
from . import compute_keypair_v2
from . import compute_secgroup_v2
from . import compute_servergroup_v2
from . import compute_volume_attach_v2
from . import csbs_backup_policy_v1
from . import csbs_backup_v1
from . import css_cluster_v1
from . import css_snapshot_configuration_v1
from . import cts_event_notification_v3
from . import cts_tracker_v1
from . import data_opentelekomcloud_antiddos_v1
from . import data_opentelekomcloud_cbr_backup_ids_v3
from . import data_opentelekomcloud_cbr_backup_v3
from . import data_opentelekomcloud_cce_addon_template_v3
from . import data_opentelekomcloud_cce_cluster_kubeconfig_v3
from . import data_opentelekomcloud_cce_cluster_v3
from . import data_opentelekomcloud_cce_node_ids_v3
from . import data_opentelekomcloud_cce_node_v3
from . import data_opentelekomcloud_compute_availability_zones_v2
from . import data_opentelekomcloud_compute_bms_flavors_v2
from . import data_opentelekomcloud_compute_bms_keypairs_v2
from . import data_opentelekomcloud_compute_bms_nic_v2
from . import data_opentelekomcloud_compute_bms_server_v2
from . import data_opentelekomcloud_compute_flavor_v2
from . import data_opentelekomcloud_compute_instance_v2
from . import data_opentelekomcloud_csbs_backup_policy_v1
from . import data_opentelekomcloud_csbs_backup_v1
from . import data_opentelekomcloud_css_flavor_v1
from . import data_opentelekomcloud_cts_tracker_v1
from . import data_opentelekomcloud_dcs_az_v1
from . import data_opentelekomcloud_dcs_maintainwindow_v1
from . import data_opentelekomcloud_dcs_product_v1
from . import data_opentelekomcloud_dds_flavors_v3
from . import data_opentelekomcloud_dds_instance_v3
from . import data_opentelekomcloud_deh_host_v1
from . import data_opentelekomcloud_deh_server_v1
from . import data_opentelekomcloud_dms_az_v1
from . import data_opentelekomcloud_dms_maintainwindow_v1
from . import data_opentelekomcloud_dms_product_v1
from . import data_opentelekomcloud_dns_nameservers_v2
from . import data_opentelekomcloud_dns_zone_v2
from . import data_opentelekomcloud_identity_agency_v3
from . import data_opentelekomcloud_identity_auth_scope_v3
from . import data_opentelekomcloud_identity_credential_v3
from . import data_opentelekomcloud_identity_group_v3
from . import data_opentelekomcloud_identity_project_v3
from . import data_opentelekomcloud_identity_projects_v3
from . import data_opentelekomcloud_identity_role_custom_v3
from . import data_opentelekomcloud_identity_role_v3
from . import data_opentelekomcloud_identity_user_v3
from . import data_opentelekomcloud_images_image_v2
from . import data_opentelekomcloud_kms_data_key_v1
from . import data_opentelekomcloud_kms_key_v1
from . import data_opentelekomcloud_lb_certificate_v3
from . import data_opentelekomcloud_lb_flavor_v3
from . import data_opentelekomcloud_lb_flavors_v3
from . import data_opentelekomcloud_lb_listener_v3
from . import data_opentelekomcloud_lb_loadbalancer_v3
from . import data_opentelekomcloud_lb_member_ids_v2
from . import data_opentelekomcloud_networking_network_v2
from . import data_opentelekomcloud_networking_port_v2
from . import data_opentelekomcloud_networking_secgroup_rule_ids_v2
from . import data_opentelekomcloud_networking_secgroup_v2
from . import data_opentelekomcloud_obs_bucket
from . import data_opentelekomcloud_obs_bucket_object
from . import data_opentelekomcloud_rds_backup_v3
from . import data_opentelekomcloud_rds_flavors_v1
from . import data_opentelekomcloud_rds_flavors_v3
from . import data_opentelekomcloud_rds_instance_v3
from . import data_opentelekomcloud_rds_versions_v3
from . import data_opentelekomcloud_rts_software_config_v1
from . import data_opentelekomcloud_rts_software_deployment_v1
from . import data_opentelekomcloud_rts_stack_resource_v1
from . import data_opentelekomcloud_rts_stack_v1
from . import data_opentelekomcloud_s3_bucket_object
from . import data_opentelekomcloud_sdrs_domain_v1
from . import data_opentelekomcloud_sfs_file_system_v2
from . import data_opentelekomcloud_sfs_turbo_share_v1
from . import data_opentelekomcloud_vbs_backup_policy_v2
from . import data_opentelekomcloud_vbs_backup_v2
from . import data_opentelekomcloud_vpc_bandwidth
from . import data_opentelekomcloud_vpc_bandwidth_v2
from . import data_opentelekomcloud_vpc_eip_v1
from . import data_opentelekomcloud_vpc_peering_connection_v2
from . import data_opentelekomcloud_vpc_route_ids_v2
from . import data_opentelekomcloud_vpc_route_v2
from . import data_opentelekomcloud_vpc_subnet_ids_v1
from . import data_opentelekomcloud_vpc_subnet_v1
from . import data_opentelekomcloud_vpc_v1
from . import data_opentelekomcloud_vpcep_public_service_v1
from . import data_opentelekomcloud_vpcep_service_v1
from . import data_opentelekomcloud_vpnaas_service_v2
from . import dcs_instance_v1
from . import dds_instance_v3
from . import deh_host_v1
from . import dms_instance_v1
from . import dms_topic_v1
from . import dns_ptrrecord_v2
from . import dns_recordset_v2
from . import dns_zone_v2
from . import ecs_instance_v1
from . import evs_volume_v3
from . import fw_firewall_group_v2
from . import fw_policy_v2
from . import fw_rule_v2
from . import identity_agency_v3
from . import identity_credential_v3
from . import identity_group_membership_v3
from . import identity_group_v3
from . import identity_mapping_v3
from . import identity_project_v3
from . import identity_protocol_v3
from . import identity_provider_v3
from . import identity_role_assignment_v3
from . import identity_role_v3
from . import identity_user_group_membership_v3
from . import identity_user_v3
from . import images_image_access_accept_v2
from . import images_image_access_v2
from . import images_image_v2
from . import ims_data_image_v2
from . import ims_image_v2
from . import kms_grant_v1
from . import kms_key_v1
from . import lb_certificate_v2
from . import lb_certificate_v3
from . import lb_l7_policy_v2
from . import lb_l7_rule_v2
from . import lb_listener_v2
from . import lb_listener_v3
from . import lb_loadbalancer_v2
from . import lb_loadbalancer_v3
from . import lb_member_v2
from . import lb_member_v3
from . import lb_monitor_v2
from . import lb_monitor_v3
from . import lb_policy_v3
from . import lb_pool_v2
from . import lb_pool_v3
from . import lb_rule_v3
from . import lb_whitelist_v2
from . import logtank_group_v2
from . import logtank_topic_v2
from . import mrs_cluster_v1
from . import mrs_job_v1
from . import nat_dnat_rule_v2
from . import nat_gateway_v2
from . import nat_snat_rule_v2
from . import networking_floatingip_associate_v2
from . import networking_floatingip_v2
from . import networking_network_v2
from . import networking_port_v2
from . import networking_router_interface_v2
from . import networking_router_route_v2
from . import networking_router_v2
from . import networking_secgroup_rule_v2
from . import networking_secgroup_v2
from . import networking_subnet_v2
from . import networking_vip_associate_v2
from . import networking_vip_v2
from . import obs_bucket
from . import obs_bucket_object
from . import obs_bucket_policy
from . import provider
from . import rds_instance_v1
from . import rds_instance_v3
from . import rds_parametergroup_v3
from . import rds_read_replica_v3
from . import rts_software_config_v1
from . import rts_software_deployment_v1
from . import rts_stack_v1
from . import s3_bucket
from . import s3_bucket_object
from . import s3_bucket_policy
from . import sdrs_protected_instance_v1
from . import sdrs_protectiongroup_v1
from . import sfs_file_system_v2
from . import sfs_share_access_rules_v2
from . import sfs_turbo_share_v1
from . import smn_subscription_v2
from . import smn_topic_attribute_v2
from . import smn_topic_v2
from . import swr_domain_v2
from . import swr_organization_permissions_v2
from . import swr_organization_v2
from . import swr_repository_v2
from . import vbs_backup_policy_v2
from . import vbs_backup_share_v2
from . import vbs_backup_v2
from . import vpc_bandwidth_associate_v2
from . import vpc_bandwidth_v2
from . import vpc_eip_v1
from . import vpc_flow_log_v1
from . import vpc_peering_connection_accepter_v2
from . import vpc_peering_connection_v2
from . import vpc_route_v2
from . import vpc_subnet_v1
from . import vpc_v1
from . import vpcep_endpoint_v1
from . import vpcep_service_v1
from . import vpnaas_endpoint_group_v2
from . import vpnaas_ike_policy_v2
from . import vpnaas_ipsec_policy_v2
from . import vpnaas_service_v2
from . import vpnaas_site_connection_v2
from . import waf_alarm_notification_v1
from . import waf_ccattackprotection_rule_v1
from . import waf_certificate_v1
from . import waf_datamasking_rule_v1
from . import waf_domain_v1
from . import waf_falsealarmmasking_rule_v1
from . import waf_policy_v1
from . import waf_preciseprotection_rule_v1
from . import waf_webtamperprotection_rule_v1
from . import waf_whiteblackip_rule_v1
