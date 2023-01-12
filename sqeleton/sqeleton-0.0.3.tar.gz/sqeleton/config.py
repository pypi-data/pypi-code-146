from typing import Any, Dict
import toml


class ConfigParseError(Exception):
    pass


def is_uri(s: str) -> bool:
    return "://" in s


def _apply_config(config: Dict[str, Any], run_name: str, kw: Dict[str, Any]):
    # Load config
    databases = config.pop("database", {})

    # Update keywords
    new_kw["__conf__"] = run_args

    return new_kw


def apply_config_from_file(path: str, run_name: str, kw: Dict[str, Any]):
    with open(path) as f:
        return _apply_config(toml.load(f), run_name, kw)


def apply_config_from_string(toml_config: str, run_name: str, kw: Dict[str, Any]):
    return _apply_config(toml.loads(toml_config), run_name, kw)
