""" Primary CLI group entrypoint
"""
import os
import traceback
import logging
import click
from sermos.logging_config import setup_logging

setup_logging(default_level=os.environ.get('LOG_LEVEL', 'INFO').upper(),
              establish_logging_config=False)
logger = logging.getLogger(__name__)

# Not all CLI tools will be functional / available depending on which extras
# are installed. For example, the config server won't work if the `workers`
# extra isn't available, which installs celery and networkx.
collection = []

warning_msg = "{} CLI tools are not available. This is most "\
               "likely due to a missing import. Verify you have the correct "\
               "Sermos extras installed."
try:
    from sermos.cli.deploy import deployment
    collection.append(deployment)
except ImportError as e:
    logger.debug(warning_msg.format("Deployment"))
    logger.debug(f"{traceback.format_exc()}")

try:
    from sermos.cli.config_server import config_server
    collection.append(config_server)
except ImportError as e:
    logger.debug(warning_msg.format("Configuration Server"))
    logger.debug(f"{traceback.format_exc()}")

try:
    from sermos.cli.proxy import sermos_proxy
    collection.append(sermos_proxy)
except ImportError as e:
    logger.debug(warning_msg.format("Proxy Service"))
    logger.debug(f"{traceback.format_exc()}")

try:
    from sermos.cli.version import get_version
    collection.append(get_version)
except ImportError as e:
    logger.debug(warning_msg.format("Version"))
    logger.debug(f"{traceback.format_exc()}")

sermos = click.CommandCollection(sources=collection)
