from typing import Any, Dict, Optional, TypedDict

from sym.shared.cli.helpers.config.base import ConfigBase

from sym.flow.cli.models import AuthToken, Organization


class ConfigSchema(TypedDict, total=False):
    org: str
    client_id: str
    email: str
    auth_token: AuthToken


def deepget(key: str, data: Dict[str, Any]) -> Optional[str]:
    """Tries to get a nested value from a dict"""
    for k in key.split("."):
        try:
            data = data[k]
        except KeyError:
            return None

    return data if isinstance(data, str) else None


class Config(ConfigBase[ConfigSchema]):
    @classmethod
    def get_value(cls, key: str) -> Optional[str]:
        config = cls.instance()
        return deepget(key, config)

    @classmethod
    def get_org(cls) -> Organization:
        config = cls.instance()
        return Organization(slug=config["org"], client_id=config["client_id"])

    @classmethod
    def set_org(cls, org: Organization):
        config = cls.instance()
        config["org"] = org.slug
        config["client_id"] = org.client_id

    @classmethod
    def is_logged_in(cls):
        return "auth_token" in cls.instance()

    @classmethod
    def get_access_token(cls) -> Optional[str]:
        try:
            return cls.instance()["auth_token"]["access_token"]
        except KeyError:
            return None

    @classmethod
    def logout(cls):
        if not cls.is_logged_in():
            return

        cfg = cls.instance()
        cfg.pop("email", None)
        cfg.pop("auth_token", None)


def store_login_config(email: str, org: Organization, auth_token: AuthToken) -> str:
    Config.set_org(org)
    cfg = Config.instance()
    cfg["email"] = email
    cfg["auth_token"] = auth_token
    return str(cfg.file)
