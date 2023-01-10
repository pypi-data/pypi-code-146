import itertools
import os
from pathlib import Path
from typing import List, Literal, Mapping, Optional

import yaml
from pydantic import BaseModel

from chalk._version import __version__


class EnvironmentSettings(BaseModel):
    runtime: Optional[Literal["python310"]]
    requirements: Optional[str]
    dockerfile: Optional[str]


class MetadataSettings(BaseModel):
    name: str
    missing: str


class FeatureSettings(BaseModel):
    metadata: Optional[List[MetadataSettings]]


class ValidationSettings(BaseModel):
    feature: Optional[FeatureSettings]


class ProjectSettings(BaseModel):
    project: str
    environments: Optional[Mapping[str, EnvironmentSettings]]
    validation: Optional[ValidationSettings]
    local_path: str
    chalkpy: str


def _load_project_config_at_path(filename: Path) -> Optional[ProjectSettings]:
    has_default_requirements = os.path.exists(filename.parent / "requirements.txt")
    try:
        with open(filename, "r") as f:
            parsed = yaml.safe_load(f)
            settings = ProjectSettings(
                **parsed,
                local_path=str(filename.absolute().resolve()),
                chalkpy=__version__,
            )
            if has_default_requirements and settings.environments is not None:
                for cfg in settings.environments.values():
                    if cfg.requirements is None:
                        cfg.requirements = "requirements.txt"
            return settings
    except OSError:
        return None


def load_project_config() -> Optional[ProjectSettings]:
    base = Path(os.getcwd())

    for d in itertools.chain([base], base.parents):
        project = _load_project_config_at_path(d / "chalk.yaml") or _load_project_config_at_path(d / "chalk.yml")

        if project is not None:
            return project

    return None
