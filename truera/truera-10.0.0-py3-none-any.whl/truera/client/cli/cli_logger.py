from enum import Enum
import logging

import click

import truera.client.client_environment as env


def create_cli_logger(level_override=None):
    env_ctx = env.LocalContextStorage.get_cli_env_context()
    set_level = env_ctx.log_level.lower()

    logging.basicConfig()

    if level_override:
        set_level = level_override

    logger = logging.getLogger("tru")

    if set_level == "silent":
        logger.setLevel("ERROR")
    elif set_level == "default":
        logger.setLevel("INFO")
    elif set_level == "verbose":
        logger.setLevel("DEBUG")
    else:
        click.echo(
            "Warning - Invalid log level set: " + set_level +
            ". Defaulting to 'Default'."
        )
        logger.setLevel("INFO")

    return logger


log_level_message = "Options: silent, default, verbose. The default can be set via >tru save log-level <level>."
