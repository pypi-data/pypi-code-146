import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from ...core_objects import ModelInfo
from ..schema.server_info import Version


def match_semvar(version: Optional[Version], match_expr: str) -> bool:
    """
    Match the version with match_expr
    :param version: Server version
    :param match_expr: Version to match with. Read more at VersionInfo.match
    :return: True if server version matches, otherwise False
    """
    if not version:
        return False

    if version.prerelease:
        return Version(version.major, version.minor, version.patch).match(match_expr)

    return version.match(match_expr)


def get_model_artifact_info(artifact_dir: Path) -> List[Dict[str, Any]]:
    """
    Get model artifact files details
    :param artifact_dir: Model artifact directory
    :return: List of artifact files details
    """
    info: List[Dict[str, Any]] = []

    for f in os.listdir(artifact_dir):
        file_stats = os.stat(os.path.join(artifact_dir, f))
        info.append(
            {'name': f, 'size': file_stats.st_size, 'modified': file_stats.st_mtime}
        )
    return info


def read_model_yaml(artifact_dir: Path) -> Optional[ModelInfo]:
    """
    Read model info from model.yaml file inside artifact dir
    :param artifact_dir: Model artifact dir
    :return: ModelInfo object if model.yaml file is found, otherwise None
    """
    yaml_file = artifact_dir / 'model.yaml'
    if not yaml_file.is_file():
        return None

    with yaml_file.open() as f:
        return ModelInfo.from_dict(yaml.safe_load(f))
