import os


def env_var_bool(env_name: str) -> bool:
    return os.getenv(env_name, "false").lower() in {"1", "true", "yes", "t"}
