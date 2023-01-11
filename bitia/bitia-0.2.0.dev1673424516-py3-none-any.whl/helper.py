"""Helper module"""

__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import sys
from pathlib import Path
import typing as T

import requests

import bitia.session as bsession
from bitia.pipeline import Pipeline
from bitia.logger import logger


def log_container(container: str, server: str, *, timestamps: bool = False):
    assert (
        container
    ), "Failed to determine the container that is runnning the pipeline. There is probably a bug in server end."
    for line in bsession.fetch_logs(container, server=server, timestamps=timestamps):
        yield line


def _check_server_status(server: str) -> int:
    res = requests.get(server)
    return res.status_code


def post_pipeline_task(
    pipeline: Pipeline,
    *,
    endpoint: str,
    server: str,
    params: T.Dict[str, str] = {},
    **kwargs,
):
    """Submit to the api for a given endpoint and pipeline file"""
    if (code := _check_server_status(server)) != 200:
        logger.warning(
            "%s may not be alive (status code: %s). Try other one?", server, code
        )
        sys.exit(1)
    pipeline_zip = pipeline.zipfile
    numbytes = pipeline_zip.stat().st_size
    assert numbytes > 0
    logger.info(
        "Submitting %s (size=%.2f KB) to the %s",
        pipeline.zipfile,
        numbytes / 1024.0,
        server,
    )

    #  submit and print the output.
    endpoint = endpoint.strip("/")
    with pipeline_zip.open("rb") as f_pipeline:
        files = {"pipeline_zip": f_pipeline}
        return bsession.post(
            f"{server}/{endpoint}",
            files=files,
            params=params,
            data=dict(pipeline=pipeline.data()).update(**kwargs),
            stream=kwargs.get("stream", False),
        )


def post(
    endpoint: str,
    *,
    server: str,
    stream: bool = False,
    params: T.Dict[str, str] = {},
    **kwargs,
):
    """A generic post function."""
    logger.info(f"Posting with data {kwargs}")
    return bsession.post(
        f"{server}/{endpoint}", json=kwargs, params=params, stream=stream, **kwargs
    )


def get(
    endpoint: str,
    *,
    server: str,
    stream: bool = False,
    params: T.Dict[str, str] = {},
    **kwargs,
):
    """A generic post function."""
    logger.info(f"Posting with data {kwargs}")
    return bsession.get(
        f"{server}/{endpoint}", params=params, json=kwargs, stream=stream, **kwargs
    )


def submit_job(
    pipeline_zip: Path, *, server: str, rerun: bool = False, params: dict = {}
):
    """Submit job to the API and stream the output."""
    numbytes = pipeline_zip.stat().st_size
    if (code := _check_server_status(server)) != 200:
        logger.warning(
            "%s may not be alive (status code: %s). Try other one?", server, code
        )
        sys.exit(1)
    assert numbytes > 0
    logger.info(
        "Submitting %s (size=%.2f KB) to the %s",
        pipeline_zip,
        numbytes / 1024.0,
        server,
    )

    #  submit and print the output.
    with pipeline_zip.open("rb") as f_pipeline:
        files = {"pipeline_zip": f_pipeline}
        response = bsession.post(
            f"{server}/submit/?rerun={rerun}",
            files=files,
            params=params,
            json=dict(filename=pipeline_zip, rerun=rerun),
        )
        return response.json()
