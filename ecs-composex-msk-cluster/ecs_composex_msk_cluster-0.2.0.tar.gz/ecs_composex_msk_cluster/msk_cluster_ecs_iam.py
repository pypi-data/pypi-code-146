#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

"""
Manages the IAM Permissions & SCRAM configuration for authentication to the Kafka cluster resources
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecs_composex.common.settings import ComposeXSettings
    from ecs_composex.ecs.ecs_family import ComposeFamily
    from ecs_composex_msk_cluster.msk_cluster import MskCluster

from compose_x_common.compose_x_common import set_else_none
from ecs_composex.common.logging import LOG
from ecs_composex.common.troposphere_tools import add_resource
from troposphere import Ref, Select, Split, Sub
from troposphere.iam import PolicyType

from .msk_cluster_params import MSK_CLUSTER_ARN

MSK_TOPIC_PERMS_MAPPING: dict = {
    "Admin": [
        "kafka-cluster:*Topic*",
        "kafka-cluster:ReadData",
        "kafka-cluster:WriteData",
    ],
    "Producer": ["kafka-cluster:DescribeTopic", "kafka-cluster:WriteData"],
    "Consumer": ["kafka-cluster:DescribeTopic", "kafka-cluster:ReadData"],
    "ProducerConsumer": [
        "kafka-cluster:DescribeTopic",
        "kafka-cluster:WriteData",
        "kafka-cluster:ReadData",
    ],
}
MSK_GROUP_PERMS_MAPPING: dict = {
    "Admin": [
        "kafka-cluster:DescribeGroup",
        "kafka-cluster:AlterGroup",
        "kafka-cluster:DeleteGroup",
    ],
    "Consumer": [
        "kafka-cluster:DescribeGroup",
        "kafka-cluster:AlterGroup",
    ],
}
MSK_TRANSACTIONAL_IDS_PERMS_MAPPING: dict = {
    "Producer": [
        "kafka-cluster:AlterTransactionalId",
        "kafka-cluster:DescribeTransactionalId",
    ],
}


def handle_topic_iam_policy(
    resource: MskCluster,
    topics_def: dict,
    statement: list,
    cluster_arn_prefix: Select,
) -> None:
    """
    Creates the IAM policies for MSK IAM connectivity to Kafka Topics
    """
    for access_type, topics_regex in topics_def.items():
        if access_type not in MSK_TOPIC_PERMS_MAPPING:
            LOG.warning(
                f"{resource.module.res_key}.{resource.name}"
                " Topic permissions {access_type} is invalid."
                f" Must be one of {list(MSK_TOPIC_PERMS_MAPPING.keys())}"
            )
            continue
        access_type_statement: dict = {
            "Sid": f"Topic{access_type}",
            "Effect": "Allow",
            "Action": MSK_TOPIC_PERMS_MAPPING[access_type],
            "Resource": [
                Sub(
                    f"${{CLUSTER_ARN_PREFIX}}:topic/${{CLUSTER_ID}}/{regex}",
                    CLUSTER_ARN_PREFIX=cluster_arn_prefix,
                    CLUSTER_ID=resource.cluster_uuid,
                )
                for regex in topics_regex
            ],
        }
        statement.append(access_type_statement)


def handle_group_iam_policy(
    resource: MskCluster,
    groups_def: dict,
    statement: list,
    cluster_arn_prefix: Select,
) -> None:
    """
    Creates the IAM policies for MSK IAM connectivity to Kafka Topics
    """
    for access_type, topics_regex in groups_def.items():
        if access_type not in MSK_GROUP_PERMS_MAPPING:
            LOG.warning(
                f"{resource.module.res_key}.{resource.name}"
                " Topic permissions {access_type} is invalid."
                f" Must be one of {list(MSK_GROUP_PERMS_MAPPING.keys())}"
            )
            continue

        access_type_statement: dict = {
            "Sid": f"Group{access_type}",
            "Effect": "Allow",
            "Action": MSK_GROUP_PERMS_MAPPING[access_type],
            "Resource": [
                Sub(
                    f"${{CLUSTER_ARN_PREFIX}}:group/${{CLUSTER_ID}}/{regex}",
                    CLUSTER_ARN_PREFIX=cluster_arn_prefix,
                    CLUSTER_ID=resource.cluster_uuid,
                )
                for regex in topics_regex
            ],
        }
        statement.append(access_type_statement)


def handle_transactional_iam_policy(
    resource: MskCluster,
    transactional_def: dict,
    statement: list,
    cluster_arn_prefix: Select,
) -> None:
    """
    Creates the IAM policies for MSK IAM connectivity to Kafka Topics
    """
    for access_type, topics_regex in transactional_def.items():
        if access_type not in MSK_TRANSACTIONAL_IDS_PERMS_MAPPING:
            LOG.warning(
                f"{resource.module.res_key}.{resource.name}"
                " Transactional ID permissions {access_type} is invalid."
                f" Must be one of {list(MSK_TRANSACTIONAL_IDS_PERMS_MAPPING.keys())}"
            )
            continue
        access_type_statement: dict = {
            "Sid": f"Transactions{access_type}",
            "Effect": "Allow",
            "Action": MSK_TRANSACTIONAL_IDS_PERMS_MAPPING[access_type],
            "Resource": [
                Sub(
                    f"${{CLUSTER_ARN_PREFIX}}:transactional-id/${{CLUSTER_ID}}/{regex}",
                    CLUSTER_ARN_PREFIX=cluster_arn_prefix,
                    CLUSTER_ID=resource.cluster_uuid,
                )
                for regex in topics_regex
            ],
        }
        statement.append(access_type_statement)


def handle_cluster_permissions(
    resource: MskCluster,
    settings: ComposeXSettings,
    cluster_def: dict,
    statement: list,
    cluster_arn_prefix,
) -> None:
    """
    Handle Cluster permissions
    """
    idempotent_write = set_else_none("IdempotentWrite", cluster_def, False)
    if idempotent_write:
        statement.append(
            {
                "Effect": "Allow",
                "Action": ["kafka-cluster:WriteDataIdempotently"],
                "Sid": "ClusterWriteIdempotently",
                "Resource": Ref(resource.cluster_arn_parameter),
            }
        )


def handle_iam_kafka_resources_access(
    resource: MskCluster,
    settings: ComposeXSettings,
    family: ComposeFamily,
    family_target_def: dict,
) -> None:
    """
    Creates IAM Policies for access to MSK resources [topic, group, cluster, transactional-id]
    """
    if resource.cfn_resource:
        cluster_arn_id = resource.add_attribute_to_another_stack(
            family.stack, resource.cluster_arn_parameter, settings
        )
        cluster_arn_prefix = Select(
            0, Split(":cluster/", Ref(cluster_arn_id["ImportParameter"]))
        )
    else:
        cluster_arn_id = resource.attributes_outputs[MSK_CLUSTER_ARN]["ImportValue"]
        cluster_arn_prefix = Select(0, Split(":cluster/", cluster_arn_id))

    statement: list = [
        {
            "Sid": "ConnectToCluster",
            "Effect": "Allow",
            "Resource": [
                Ref(cluster_arn_id["ImportParameter"])
                if resource.cfn_resource
                else cluster_arn_id
            ],
            "Action": ["kafka-cluster:Connect"],
        }
    ]
    handle_cluster_permissions(
        resource,
        settings,
        set_else_none("cluster", family_target_def, {}),
        statement,
        cluster_arn_prefix,
    )
    handle_topic_iam_policy(
        resource,
        set_else_none("topic", family_target_def, {}),
        statement,
        cluster_arn_prefix,
    )
    handle_group_iam_policy(
        resource,
        set_else_none("group", family_target_def, {}),
        statement,
        cluster_arn_prefix,
    )
    handle_transactional_iam_policy(
        resource,
        set_else_none("transactional-id", family_target_def, {}),
        statement,
        cluster_arn_prefix,
    )

    iam_policy = PolicyType(
        f"KafkaAccess{family.logical_name}{resource.module.mapping_key}{resource.logical_name}",
        PolicyName=f"KafkaAccess{family.logical_name}{resource.module.mapping_key}{resource.logical_name}",
        PolicyDocument={"Version": "2012-10-17", "Statement": statement},
        Roles=[family.iam_manager.task_role.name],
    )
    add_resource(family.template, iam_policy)
