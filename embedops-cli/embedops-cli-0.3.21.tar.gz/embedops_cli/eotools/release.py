#!/usr/bin/env python
"""
`release.py`
=======================================================================
Script to send release data to EmbedOps Platform.
* Author(s): Jimmy Gomez
"""
import logging
import sys
from os import getenv
from embedops_cli.api import get_client, Configuration, ReleaseCreateProps
from embedops_cli.api.rest import ApiException
from embedops_cli.config import settings

_logger = logging.getLogger("create_release")


def create_release():
    """Entrypoint for the `eotools-create-release` tool"""
    if getenv("CI") is None or getenv("CI") != "true":
        _logger.error("ERROR: Not a pipeline run")
        sys.exit(1)
    if settings.get("tag") is None:
        _logger.error("ERROR: No tag envvar found")
        sys.exit(1)
    run_id = settings.run_id
    name = settings.tag
    urls = sys.argv[1:]
    try:
        data = ReleaseCreateProps(run_id, name, urls)
        api_client = get_client()
        configuration = Configuration()
        configuration.api_key["X-API-Key"] = settings.api_repo_key
        configuration.host = f"{settings.host}/api/v1"
        api_client.create_release_from_ci(data)
    except (ValueError, TypeError, ApiException) as err:
        if len(err.args) > 0:
            _logger.error(err.args[0])
        else:
            _logger.error(err)
        sys.exit(1)
    finally:
        # this kills the thread pool so the process can exit
        del api_client


if __name__ == "__main__":
    create_release()
