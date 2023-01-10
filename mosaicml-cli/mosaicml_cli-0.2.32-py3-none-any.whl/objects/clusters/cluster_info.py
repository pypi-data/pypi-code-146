"""Helpers for cluster info"""
from typing import List

from mcli.config import MCLIConfig
from mcli.models import Cluster


def get_cluster_list() -> List[Cluster]:
    conf = MCLIConfig.load_config()
    return conf.clusters
