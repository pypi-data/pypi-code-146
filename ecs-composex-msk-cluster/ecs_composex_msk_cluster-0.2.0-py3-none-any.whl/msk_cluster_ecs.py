#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>


from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecs_composex.common.settings import ComposeXSettings
    from .msk_cluster import MskCluster

from compose_x_common.compose_x_common import keyisset, set_else_none
from ecs_composex.common.logging import LOG

from .msk_cluster_ecs_iam import handle_iam_kafka_resources_access


def handle_kafka_iam_permissions(resource: MskCluster, settings: ComposeXSettings):
    for target in resource.families_targets:
        if target[0] and (not target[0].stack or not target[0].template):
            continue
        if not target[3]:
            LOG.warning(
                f"{resource.module.res_key}.{resource.name} - Access not defined for {target[0].name}"
            )
            continue
        kafka_access = set_else_none("KafkaAccess", target[-1])
        if keyisset("Iam", kafka_access):
            handle_iam_kafka_resources_access(
                resource, settings, target[0], kafka_access["Iam"]
            )
