# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

"""
Configure MSK Cluster autoscaling
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from troposphere import Template
    from .msk_cluster import MskCluster

from compose_x_common.compose_x_common import set_else_none
from ecs_composex.common.cfn_conditions import define_stack_name
from ecs_composex.common.troposphere_tools import add_resource
from troposphere import (
    AWS_ACCOUNT_ID,
    AWS_PARTITION,
    AWS_REGION,
    AWS_URL_SUFFIX,
    Ref,
    Sub,
)
from troposphere.applicationautoscaling import (
    PredefinedMetricSpecification,
    ScalableTarget,
    ScalableTargetAction,
    ScalingPolicy,
    TargetTrackingScalingPolicyConfiguration,
)


def set_scalable_target(
    cluster: MskCluster, storage_scaling: dict
) -> Union[None, ScalableTarget]:
    return ScalableTarget(
        f"{cluster.logical_name}ScalableTarget",
        DependsOn=[cluster.cfn_resource.title],
        ServiceNamespace="kafka",
        MaxCapacity=storage_scaling["MaxInGB"],
        MinCapacity=1,
        ResourceId=Ref(cluster.cfn_resource),
        RoleARN=Sub(
            f"arn:${{{AWS_PARTITION}}}:iam::${{{AWS_ACCOUNT_ID}}}:role/"
            f"aws-service-role/kafka.application-autoscaling.${{{AWS_URL_SUFFIX}}}/"
            "AWSServiceRoleForApplicationAutoScaling_KafkaCluster"
        ),
        ScalableDimension="kafka:broker-storage:VolumeSize",
    )


def set_scaling_policy(
    cluster: MskCluster,
    storage_scaling: dict,
    scaling_target: ScalableTarget,
) -> ScalingPolicy:
    return ScalingPolicy(
        f"{cluster.logical_name}StorageScalingPolicy",
        DependsOn=[scaling_target.title],
        PolicyName=Sub(
            "MSK Storage Scaling - ${StackName}", StackName=define_stack_name()
        ),
        PolicyType="TargetTrackingScaling",
        ScalingTargetId=Ref(scaling_target),
        TargetTrackingScalingPolicyConfiguration=TargetTrackingScalingPolicyConfiguration(
            DisableScaleIn=True,
            TargetValue=float(storage_scaling["Target"]),
            PredefinedMetricSpecification=PredefinedMetricSpecification(
                PredefinedMetricType="KafkaBrokerStorageUtilization"
            ),
        ),
    )


def add_storage_scaling(cluster: MskCluster, template: Template) -> None:
    """
    Adds storage autoscaling to the MSK Cluster. Application Autoscaling will add capacity
    as the data on the cluster grows. However, it won't scale in (remove capacity).
    This feature is mostly aimed at ensuring there is always storage available on the Kafka cluster
    """

    if not cluster.cfn_resource or not cluster.parameters:
        return
    storage_scaling = set_else_none("StorageScaling", cluster.parameters)
    if not storage_scaling:
        return
    scaling_target = set_scalable_target(cluster, storage_scaling)
    scaling_policy = set_scaling_policy(cluster, storage_scaling, scaling_target)
    add_resource(template, scaling_target)
    add_resource(template, scaling_policy)
