#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecs_composex.mods_manager import XResourceModule
    from ecs_composex.common.settings import ComposeXSettings
    from ecs_composex.mods_manager import ModManager

from compose_x_common.aws.msk import MSK_CLUSTER_ARN_RE
from compose_x_common.compose_x_common import keyisset
from ecs_composex.common.logging import LOG
from ecs_composex.compose.x_resources.network_x_resources import NetworkXResource
from ecs_composex.ingress_settings import lookup_security_group
from ecs_composex.resource_settings import link_resource_to_services
from ecs_composex.vpc.vpc_params import STORAGE_SUBNETS
from troposphere import GetAtt, Ref, Select, Split
from troposphere.msk import Cluster as CfnMskCluster

from ecs_composex_msk_cluster.msk_cluster_params import (
    CONTROL_CLOUD_ATTR_MAPPING,
    MSK_CLUSTER_ARN,
    MSK_CLUSTER_CLIENTS_SHARED_SG,
    MSK_CLUSTER_SG_PARAM,
)

from .msk_cluster_ecs import handle_kafka_iam_permissions


class MskCluster(NetworkXResource):
    """
    Class to manage MSK Cluster resource
    """

    def __init__(
        self,
        name: str,
        definition: dict,
        module: XResourceModule,
        settings: ComposeXSettings,
    ):
        super().__init__(name, definition, module, settings)

        self.clients_security_group = None
        self.security_group_param = MSK_CLUSTER_SG_PARAM
        self.clients_security_group_param = MSK_CLUSTER_CLIENTS_SHARED_SG
        self.subnets_override = STORAGE_SUBNETS
        self.post_processing_properties: list = [
            "EncryptionInfo.EncryptionAtRest.DataVolumeKMSKeyId",
            "BrokerNodeGroupInfo.ClientSubnets",
        ]
        self.ref_parameter = MSK_CLUSTER_ARN
        self.cluster_arn_parameter = MSK_CLUSTER_ARN
        self.cloud_control_attributes_mapping = CONTROL_CLOUD_ATTR_MAPPING

    @property
    def cluster_uuid(self):
        if self.cfn_resource:
            return Select(1, Split(":cluster/", Ref(self.cfn_resource)))
        else:
            return Select(
                1,
                Split(
                    ":cluster/", self.attributes_outputs[MSK_CLUSTER_ARN]["ImportValue"]
                ),
            )

    def init_outputs(self):
        self.output_properties: dict = {
            MSK_CLUSTER_ARN: (self.logical_name, self.cfn_resource, Ref, None),
            MSK_CLUSTER_SG_PARAM: (
                f"{self.logical_name}{self.security_group_param.title}",
                self.security_group,
                GetAtt,
                self.security_group_param.return_value,
            ),
            MSK_CLUSTER_CLIENTS_SHARED_SG: (
                f"{self.logical_name}{self.clients_security_group_param.title}",
                self.clients_security_group,
                GetAtt,
                self.clients_security_group_param.return_value,
            ),
        }

    def to_ecs(self, settings, modules: ModManager, root_stack=None) -> None:
        """
        Maps a database service to ECS services
        """
        for target in self.families_targets:
            if target[0].service_compute.launch_type != "EXTERNAL":
                if self.cfn_resource:
                    client_sg_id = self.add_attribute_to_another_stack(
                        target[0].stack, self.clients_security_group_param, settings
                    )
                    target[0].service_networking.extra_security_groups.append(
                        client_sg_id["ImportParameter"]
                    )
                    target[0].ecs_service.ecs_service.NetworkConfiguration = target[
                        0
                    ].service_networking.ecs_network_config
                elif (
                    self.lookup_properties
                    and MSK_CLUSTER_CLIENTS_SHARED_SG in self.lookup_properties
                    and MSK_CLUSTER_CLIENTS_SHARED_SG in self.attributes_outputs
                ):
                    LOG.info(
                        f"{self.module.res_key}.{self.name} - "
                        "Associating found ClientsSecurityGroup from Lookup."
                    )
                    target[0].service_networking.extra_security_groups.append(
                        self.attributes_outputs[MSK_CLUSTER_CLIENTS_SHARED_SG][
                            "ImportValue"
                        ]
                    )
                    target[0].ecs_service.ecs_service.NetworkConfiguration = target[
                        0
                    ].service_networking.ecs_network_config
            else:
                LOG.warning(
                    f"{self.stack.title} - {target[0].name} - "
                    "When using EXTERNAL Launch Type, networking settings cannot be set."
                )
        if self.cluster_arn_parameter:
            link_resource_to_services(
                settings,
                self,
                arn_parameter=self.cluster_arn_parameter,
                access_subkeys=["MSKCluster"],
            )
            handle_kafka_iam_permissions(self, settings)


def describe_kafka_cluster(
    cluster: MskCluster, account_id: str, resource_id: str
) -> dict:
    client = cluster.lookup_session.client("kafka")
    cluster_r = client.describe_cluster_v2(ClusterArn=resource_id)
    return cluster_r["ClusterInfo"]


def define_msk_clusters_mappings(module: XResourceModule, settings: ComposeXSettings):
    for cluster in module.lookup_resources:
        cluster.init_outputs()
        cluster.lookup_resource(
            MSK_CLUSTER_ARN_RE,
            describe_kafka_cluster,
            CfnMskCluster.resource_type,
            "kafka:cluster",
            "Cluster",
            use_arn_for_id=True,
        )
        if keyisset("ClientsSecurityGroup", cluster.lookup):
            client_sg = lookup_security_group(
                settings, cluster.lookup["ClientsSecurityGroup"]
            )
            cluster.lookup_properties.update({MSK_CLUSTER_CLIENTS_SHARED_SG: client_sg})
            cluster.generate_cfn_mappings_from_lookup_properties()
            cluster.generate_outputs()
        else:
            LOG.warning(
                f"{module.res_key}.{cluster.name} - "
                "ClientsSecurityGroup not set. Inbound to MSK might not work."
            )

        settings.mappings[module.mapping_key].update(
            {cluster.logical_name: cluster.mappings}
        )
