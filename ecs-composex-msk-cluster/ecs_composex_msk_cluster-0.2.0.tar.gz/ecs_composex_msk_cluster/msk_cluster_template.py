#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from troposphere import Template
    from ecs_composex.mods_manager import XResourceModule
    from .msk_cluster import MskCluster

from compose_x_common.aws.msk import list_all_kafka_versions
from compose_x_common.compose_x_common import keyisset, set_else_none
from ecs_composex.common.cfn_conditions import define_stack_name
from ecs_composex.common.cfn_params import ROOT_STACK_NAME
from ecs_composex.common.logging import LOG
from ecs_composex.common.stacks import ComposeXStack
from ecs_composex.common.troposphere_tools import (
    add_outputs,
    add_resource,
    build_template,
)
from ecs_composex.resources_import import import_record_properties
from ecs_composex.vpc.vpc_params import (
    APP_SUBNETS,
    PUBLIC_SUBNETS,
    STORAGE_SUBNETS,
    VPC_ID,
)
from troposphere import GetAtt, Output, Ref, Sub
from troposphere.ec2 import SecurityGroup
from troposphere.msk import Cluster as AwsMskCluster

from .msk_cluster_conditions import (
    CLIENTS_USE_SASL_IAM_CON,
    CLIENTS_USE_SASL_IAM_CON_T,
    CLIENTS_USE_SASL_SCRAM_CON,
    CLIENTS_USE_SASL_SCRAM_CON_T,
    CLIENTS_USE_TLS_AUTH_CON,
    CLIENTS_USE_TLS_AUTH_CON_T,
    CLUSTER_PRIVATE_ONLY_CON,
    CLUSTER_PRIVATE_ONLY_CON_T,
    CLUSTER_PUBLICLY_ADDRESSED_CON,
    CLUSTER_PUBLICLY_ADDRESSED_CON_T,
)
from .msk_cluster_params import (
    MSK_CLUSTER_ADDRESSING_TYPE,
    MSK_CLUSTER_SG_PARAM,
    MSK_CLUSTER_USE_SASL_IAM,
    MSK_CLUSTER_USE_SASL_SCRAM,
    MSK_PORTS_MAPPING,
)
from .msk_sg_ingress import handle_msk_auth_settings
from .msk_storage_scaling import add_storage_scaling


class MskClusterStack(ComposeXStack):
    """
    Class to represent an MSK Cluster' Stack
    """

    def __init__(self, name, stack_template, cluster, top_stack, **kwargs):
        self.cluster = cluster
        super().__init__(name, stack_template, **kwargs)
        self.parent_stack = top_stack
        self.cluster.stack = self


def validate_cluster_version(cluster: MskCluster, input_version) -> None:
    """
    Validates the kafka version
    """
    versions = list_all_kafka_versions(session=cluster.lookup_session)
    for version in versions:
        if version["Version"] == input_version:
            break
    else:
        raise ValueError(
            f"{cluster.module.res_key}.{cluster.name} - ",
            f"Version {input_version} is not valid. Versions supported",
            [_v["Version"] for _v in versions if _v["Status"] == "ACTIVE"],
        )
    if keyisset("Status", version) and version["Status"] != "ACTIVE":
        raise ValueError(
            f"{cluster.module.res_key}.{cluster.name} - "
            f"Version {version['Version']} is not active: {version['Status']}"
        )


def set_msk_cluster_template(module: XResourceModule, cluster: MskCluster) -> Template:
    template = build_template(
        f"{module.res_key}.{cluster.name} Stack Template",
        [
            MSK_CLUSTER_USE_SASL_IAM,
            MSK_CLUSTER_USE_SASL_SCRAM,
            MSK_CLUSTER_ADDRESSING_TYPE,
            VPC_ID,
            STORAGE_SUBNETS,
            APP_SUBNETS,
            PUBLIC_SUBNETS,
        ],
    )
    template.add_condition(
        CLUSTER_PUBLICLY_ADDRESSED_CON_T, CLUSTER_PUBLICLY_ADDRESSED_CON
    )
    template.add_condition(CLUSTER_PRIVATE_ONLY_CON_T, CLUSTER_PRIVATE_ONLY_CON)
    template.add_condition(CLIENTS_USE_SASL_SCRAM_CON_T, CLIENTS_USE_SASL_SCRAM_CON)
    template.add_condition(CLIENTS_USE_SASL_IAM_CON_T, CLIENTS_USE_SASL_IAM_CON)
    template.add_condition(CLIENTS_USE_TLS_AUTH_CON_T, CLIENTS_USE_TLS_AUTH_CON)
    template.add_mapping("MSKPorts", MSK_PORTS_MAPPING)
    return template


def build_msk_clusters(module: XResourceModule, msk_top_stack: ComposeXStack):
    """
    Creates a new MSK cluster from properties
    Each MSK cluster gets its own template & own stack to allow for better re-usability.
    """
    for cluster in module.new_resources:
        cluster_template = set_msk_cluster_template(module, cluster)
        if cluster.parameters and keyisset(
            "CreateKafkaConfiguration", cluster.parameters
        ):
            LOG.warning(
                f"{cluster.module.res_key}.{cluster.name} - "
                "At the moment, the AWS::MSK::Configuration does not return the Revision. "
                "Therefore cannot be used here yet. "
                "See https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/1138"
            )
        cluster.clients_security_group = add_resource(
            cluster_template,
            SecurityGroup(
                f"{cluster.logical_name}ClientsSecurityGroup",
                GroupName=Sub(
                    f"${{StackName}}-{cluster.logical_name}--clients",
                    StackName=define_stack_name(cluster_template),
                ),
                GroupDescription=Sub(
                    f"${{StackName}} {cluster.name} Clients SG",
                    StackName=define_stack_name(),
                ),
                VpcId=Ref(VPC_ID),
            ),
        )
        cluster.security_group = add_resource(
            cluster_template,
            SecurityGroup(
                f"{cluster.logical_name}SecurityGroup",
                GroupName=Sub(
                    f"${{StackName}}-{cluster.logical_name}",
                    StackName=define_stack_name(),
                ),
                GroupDescription=Sub(
                    f"${{StackName}} {cluster.name}", StackName=define_stack_name()
                ),
                VpcId=Ref(VPC_ID),
            ),
        )
        cluster_sg_id = GetAtt(
            cluster.security_group, MSK_CLUSTER_SG_PARAM.return_value
        )
        cluster_props = import_record_properties(
            cluster.properties,
            AwsMskCluster,
        )
        broker_info = set_else_none("BrokerNodeGroupInfo", cluster_props, {})
        security_groups = set_else_none("SecurityGroups", broker_info, [cluster_sg_id])
        if security_groups and cluster_sg_id not in security_groups:
            security_groups.append(
                GetAtt(cluster.security_group, MSK_CLUSTER_SG_PARAM.return_value)
            )
        if broker_info:
            setattr(broker_info, "SecurityGroups", security_groups)
            client_subnets = (
                getattr(broker_info, "ClientSubnets")
                if hasattr(broker_info, "ClientSubnets")
                else []
            )
            if not client_subnets:
                setattr(broker_info, "ClientSubnets", Ref(cluster.subnets_override))
        else:
            cluster_props.update(
                {
                    "BrokerNodeGroupInfo": {"SecurityGroups": security_groups},
                    "ClientSubnets": Ref(cluster.subnets_override),
                }
            )
        cluster.cfn_resource = AwsMskCluster(cluster.logical_name, **cluster_props)
        validate_cluster_version(cluster, cluster.cfn_resource.KafkaVersion)
        cluster_stack = MskClusterStack(
            cluster.logical_name,
            cluster=cluster,
            stack_template=cluster_template,
            top_stack=msk_top_stack,
            stack_parameters={
                ROOT_STACK_NAME.title: Ref(ROOT_STACK_NAME),
                VPC_ID.title: Ref(VPC_ID),
                STORAGE_SUBNETS.title: Ref(STORAGE_SUBNETS),
                PUBLIC_SUBNETS.title: Ref(PUBLIC_SUBNETS),
                APP_SUBNETS.title: Ref(APP_SUBNETS),
            },
        )

        handle_msk_auth_settings(cluster)
        add_resource(cluster_template, cluster.cfn_resource)
        add_storage_scaling(cluster, cluster_template)
        add_resource(msk_top_stack.stack_template, cluster_stack)
        cluster.init_outputs()
        cluster.generate_outputs()
        add_outputs(cluster_template, cluster.outputs)

        new_outputs = []
        for output_name in cluster.stack.stack_template.outputs:
            new_outputs.append(
                Output(
                    output_name,
                    Value=GetAtt(cluster_stack.title, f"Outputs.{output_name}"),
                )
            )
        add_outputs(msk_top_stack.stack_template, new_outputs)
