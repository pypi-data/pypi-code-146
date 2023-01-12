#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .msk_cluster import MskCluster
    from ecs_composex.common.settings import ComposeXSettings
    from troposphere import Template

from compose_x_common.compose_x_common import keyisset
from ecs_composex.common import get_nested_property
from ecs_composex.common.logging import LOG
from ecs_composex.common.troposphere_tools import add_resource
from ecs_composex.kinesis_firehose.kinesis_firehose_stack import DeliveryStream
from ecs_composex.s3.s3_bucket import Bucket
from troposphere import Ref
from troposphere.logs import LogGroup
from troposphere.msk import BrokerLogs, CloudWatchLogs, LoggingInfo


def add_log_group(cluster: MskCluster, template: Template) -> None:
    """
    Creates a new Log Group for the cluster and configures the property for it.
    """
    param, prop, value = get_nested_property(
        cluster.cfn_resource, "LoggingInfo.BrokerLogs.CloudWatchLogs"
    )
    if isinstance(value, CloudWatchLogs):
        LOG.warning(
            f"{cluster.module.res_key}.{cluster.name} - "
            "Properties for LoggingInfo.BrokerLogs.CloudWatchLogs already set. Skipping"
        )
        return
    log_group = LogGroup(f"{cluster.logical_name}BrokersLogGroup")
    add_resource(template, log_group)
    if value and value is not None:
        setattr(param, prop, CloudWatchLogs(Enabled=True, LogGroup=Ref(log_group)))
    else:
        if not hasattr(cluster.cfn_resource, "LoggingInfo"):
            setattr(
                cluster.cfn_resource,
                "LoggingInfo",
                LoggingInfo(
                    BrokerLogs=BrokerLogs(
                        CloudWatchLogs=CloudWatchLogs(
                            Enabled=True, LogGroup=Ref(log_group)
                        )
                    )
                ),
            )
        else:
            if not hasattr(
                cluster.cfn_resource.LoggingInfo.BrokerLogs, "CloudWatchLogs"
            ):
                setattr(
                    cluster.cfn_resource.LoggingInfo,
                    "CloudWatchLogs",
                    CloudWatchLogs(Enabled=True, LogGroup=Ref(log_group)),
                )


def handle_logging(
    cluster: MskCluster, cluster_template: Template, settings: ComposeXSettings
) -> None:
    if cluster.parameters and keyisset("CreateLogGroup", cluster.parameters):
        add_log_group(cluster, cluster_template)
