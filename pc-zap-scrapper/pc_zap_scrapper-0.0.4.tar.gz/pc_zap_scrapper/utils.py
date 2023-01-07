import os
from dotenv import load_dotenv
from getpass import getpass
from loguru import logger
from pathlib import Path
from pc_zap_scrapper import PATH_TEMP, PATH_TEMP_DOTENV


ENV_VARS = [
    "DB_USERNAME",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
]

def configure(dotenv_path=None):
    """Configurations of env var to Postgres connection"""

    result = False

    if dotenv_path is not None:
        result = load_dotenv(dotenv_path=dotenv_path)
        
    else:
        result = _input_env_vars()

    _export_envars_to_temp_dotenv()

def _input_env_var(envvar: str) -> None:
    """Inputation of env var by the user"""
    env_value = None

    if envvar == "DB_PASSWORD":
        env_value = getpass(envvar+":")
    else:
        env_value = input(envvar+":")

    if not env_value:
        raise Exception(f"Variable env {envvar} not defined.")
    else:
        return env_value
    
def _input_env_vars():
    """Setting all env vars."""

    for envvar in ENV_VARS:
        os.environ[envvar] = _input_env_var(envvar)
    
    return True

def _export_envars_to_temp_dotenv():
    """Export connection env vars to temporary .env file"""

    if not os.path.exists(PATH_TEMP):
        os.makedirs(PATH_TEMP)

    logger.info(f"Exporting env vars to {PATH_TEMP_DOTENV}")
    
    with open(PATH_TEMP_DOTENV, "w") as file:
        for envvar in ENV_VARS:
            file.write(f"{envvar}={os.environ[envvar]}\n")

def validate_environment():
    """Logging env vars"""

    for envvar in ENV_VARS:
        logger.info(f"{envvar}: {os.getenv(envvar)}")
