import os
from functools import lru_cache
from pathlib import Path
from typing import Mapping, Optional

import yaml
from pydantic import BaseModel

from chalk.config.project_config import load_project_config


class TokenConfig(BaseModel):
    name: Optional[str]
    clientId: Optional[str]
    clientSecret: Optional[str]
    apiServer: Optional[str]
    activeEnvironment: Optional[str]


class AuthConfig(BaseModel):
    tokens: Optional[Mapping[str, TokenConfig]]


# using lru_cache for 3.8 compat
@lru_cache(maxsize=None)
def _load_global_config() -> Optional[AuthConfig]:
    home = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~"))
    path = None
    for filename in [".chalk.yml"]:
        p = os.path.join(home, filename)
        if os.path.exists(p):
            path = p

    if path is None:
        return None

    with open(path, "r") as f:
        parsed = yaml.safe_load(f)
        return AuthConfig(**parsed)


def _load_config_from_env() -> Optional[TokenConfig]:
    envvars = dict(
        clientId=os.getenv("_CHALK_CLIENT_ID"),
        clientSecret=os.getenv("_CHALK_CLIENT_SECRET"),
        apiServer=os.getenv("_CHALK_API_SERVER"),
        activeEnvironment=os.getenv("_CHALK_ACTIVE_ENVIRONMENT"),
    )
    if any(v is None for v in envvars.values()):
        return None

    return TokenConfig(**envvars)


def load_token() -> Optional[TokenConfig]:
    envvar_config = _load_config_from_env()
    if envvar_config is not None:
        return envvar_config

    global_cfg = _load_global_config()
    if global_cfg is None:
        return None

    absdir = Path(os.getcwd()).absolute().resolve()
    project_config = load_project_config()
    if project_config:
        absdir = Path(project_config.local_path).parent
    tokens = global_cfg.tokens or {}
    return tokens.get(str(absdir)) or tokens.get("default")
