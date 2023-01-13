import os
from typing import Optional

from .autodetect import get_secrets_generator


__all__ = ("get_secret", "validate_secret", "get_token", "get_flag", "validate_token")


# Delegate everything to the autodetected generator, except when values are to be read from the environment


def get_user_id() -> str:
    if "KYZYLBORDA_USER_ID" not in os.environ:
        raise ValueError("Cannot get user id from the environment. Make sure that the application is invoked correctly")
    return os.environ["KYZYLBORDA_USER_ID"]


def get_token(user_id: Optional[str]=None) -> str:
    if user_id is None:
        if "KYZYLBORDA_SECRET_token" in os.environ:
            return os.environ["KYZYLBORDA_SECRET_token"]
        user_id = get_user_id()
    secrets_generator = get_secrets_generator()
    if hasattr(secrets_generator, "get_token"):
        return secrets_generator.get_token(user_id)
    if hasattr(secrets_generator, "get_secret"):
        return secrets_generator.get_secret("token", user_id, mac=True)
    raise ValueError("The secrets generator provided by the task defines neither get_token nor get_secret")


def validate_token(token: Optional[str]=None) -> bool:
    if token is None:
        token = get_token()
    secrets_generator = get_secrets_generator()
    if hasattr(secrets_generator, "validate_token"):
        return secrets_generator.validate_token(token)
    if hasattr(secrets_generator, "validate_secret"):
        return secrets_generator.validate_secret("token", token)
    raise ValueError("The secrets generator provided by the task defines neither validate_token nor validate_secret")


def get_secret(name: str, seed: Optional[str]=None, mac: bool=False) -> str:
    if seed is None:
        if f"KYZYLBORDA_SECRET_{name}" in os.environ:
            return os.environ[f"KYZYLBORDA_SECRET_{name}"]
        if name == "token":
            seed = get_user_id()
        else:
            seed = get_token()
    secrets_generator = get_secrets_generator()
    if hasattr(secrets_generator, "get_secret"):
        return secrets_generator.get_secret(name, seed, mac)
    raise ValueError("The secrets generator provided by the task does not define get_secret")


def validate_secret(name: str, secret: Optional[str]=None) -> bool:
    secrets_generator = get_secrets_generator()
    if secret is None:
        secret = get_secret(name)
    if hasattr(secrets_generator, "validate_secret"):
        return secrets_generator.validate_secret(name, secret)
    raise ValueError("The secrets generator provided by the task does not define validate_secret")


def get_flag(token: Optional[str]=None) -> str:
    if token is None:
        if "KYZYLBORDA_SECRET_flag" in os.environ:
            return os.environ["KYZYLBORDA_SECRET_flag"]
        token = get_token()
    secrets_generator = get_secrets_generator()
    if hasattr(secrets_generator, "get_flag"):
        return secrets_generator.get_flag(token)
    if hasattr(secrets_generator, "get_secret"):
        return secrets_generator.get_secret("flag", token)
    raise ValueError("The secrets generator provided by the task defines neither get_flag nor get_secret")
