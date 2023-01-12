#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

"""
MSK Configuration
"""

from __future__ import annotations

from typing import Any, Optional

from troposphere.msk import Configuration


class MskConfiguration(Configuration):
    default_configurations: dict = {
        "auto.create.topics.enable": False,
        "default.replication.factor": 3,
        "min.insync.replicas": 2,
        "num.io.threads": 8,
        "num.network.threads": 5,
        "num.partitions": 1,
        "num.replica.fetchers": 2,
        "replica.lag.time.max.ms": 30000,
        "socket.receive.buffer.bytes": 102400,
        "socket.request.max.bytes": 104857600,
        "socket.send.buffer.bytes": 102400,
        "unclean.leader.election.enable": True,
        "zookeeper.session.timeout.ms": 18000,
    }

    def __init__(self, title: Optional[str], **kwargs: Any):
        self.configuration_dict: dict = {}
        if "ServerProperties" not in kwargs:
            kwargs.update(
                {
                    "ServerProperties": self.config_dict_to_string(
                        self.default_configurations
                    )
                }
            )
        super().__init__(title, **kwargs)

    @staticmethod
    def config_dict_to_string(config: dict) -> str:
        return "\n".join(["%s=%s" % (key, value) for key, value in config.items()])
