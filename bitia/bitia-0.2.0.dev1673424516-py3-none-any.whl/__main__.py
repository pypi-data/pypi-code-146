"""BiTIA command line interface to submit job to the BiTIA server.

https://bitia.link

(c) 2022-, Subconscious Compute, https://subcom.tech
"""

import typing as T
import os
import functools
from enum import Enum

from rich.progress import track

import bitia.helper as bhelper
from bitia.logger import logger, cprint, set_logger_level, console

from bitia import version as bversion
import bitia.pipeline as bpipeline
import bitia.session as bsession
import bitia.config as bconfig


import typer

app = typer.Typer()


class VerbosityLevel(str, Enum):
    debug = "debug"
    info = "info"
    warning = "warning"


def version_callback(value: bool):
    """callback for version"""
    if value:
        print(version())


def session(func):
    """Load a session before and save the session after the function call"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bsession.load_session()
        retval = func(*args, **kwargs)
        bsession.save_session()
        return retval

    return wrapper


@app.command("create-container")
@session
def create_remote_container(
    user_input,
    *,
    recreate: bool = False,
    output_lines: T.List[str] = [],
):
    """Create container for the pipeline. The container starts running
    immediately on the server. Use command `logs` to stream the output.
    """
    pipeline = bpipeline.user_input_to_pipeline(user_input)
    # for a command pipeline, always create a new container.
    if pipeline.is_a_command():
        recreate = True
    res = bhelper.post_pipeline_task(
        pipeline,
        endpoint="container/create",
        params=dict(recreate="true" if recreate else "false"),
        server=bconfig.get_server(),
        stream=True,
    )
    res.raise_for_status()
    _lines = (
        track(res.iter_lines(), description="BiTIA is setting up required infra...")
        if not bconfig.get_config("plain", default=False)
        else res.iter_lines()
    )
    for line in _lines:
        output_lines.append(line.decode().rstrip())
        logger.info(output_lines[-1])
    return res


@app.command("list-container")
@session
def list_containers(user_input):
    """List the remote server associated with the pipeline."""
    if not _list_remote_container(user_input):
        for container in _list_remote_container(user_input):
            cprint(container)


def _list_remote_container(user_input) -> T.List[str]:
    pipeline = bpipeline.user_input_to_pipeline(user_input)
    logger.debug(f"sha256 of `{pipeline.zipfile}` is `{pipeline.checksum}`")
    logger.info(
        f"Finding container for user input `{user_input}` with sha256sum={pipeline.checksum}"
    )
    res = bhelper.get(
        endpoint="container/list",
        server=bconfig.get_server(),
        params=dict(pipeline_sha256=pipeline.checksum),
    )
    if res.status_code != 200:
        return []
    return res.json()["containers"].split(",")


@app.command("artifacts")
@session
def get_generated_artifacts(user_input):
    # check if the containers for the corresponding pipeline exists
    if not _list_remote_container(user_input):
        cprint(
            "Artifacts for this pipeline doesn't exist, please run the pipeline using `bitia run` first..."
        )
        return
    pipeline = bpipeline.user_input_to_pipeline(user_input)
    res = bhelper.get(
        endpoint="artifacts",
        server=bconfig.get_server(),
        params=dict(pipeline_sha256=pipeline.checksum),
    )
    res.raise_for_status()
    path = res._content
    assert path is not None
    path = path.decode()[1:-1].rstrip()
    server = bconfig.get_server().rstrip("/")
    cprint("Directory is being served at: ")
    cprint(f"{server}/{path}")


@app.command("logs")
@session
def stream_log(user_input):
    """Stream logs for the most recent run of a given pipeline."""
    pipeline = bpipeline.user_input_to_pipeline(user_input)
    logger.info(
        f"Finding container for user input {user_input} with sha256sum={pipeline.checksum}"
    )
    res = bhelper.get(
        endpoint="logs",
        params=dict(pipeline_sha256=pipeline.checksum),
        server=bconfig.get_server(),
        stream=True,
    )
    res.raise_for_status()
    for line in res.iter_lines():
        cprint(line.decode().rstrip())


@app.command("submit")
@session
def submit_pipeline(user_input, *, rerun: bool = False, output_lines: T.List[str]):
    """Submit your pipelin (url, directory, zip_file).

    Prepare the user directory to send to the server. User can also provide link
    to the pipeline to run.
    """
    res = create_remote_container(user_input, recreate=rerun, output_lines=output_lines)
    logger.info("Remote container: %s", res)
    containers = _list_remote_container(user_input)
    cprint(f"{containers}")
    return containers


@app.command("run")
@session
def run_user_input(user_input, *, rerun: bool = False, output_lines: T.List[str] = []):
    """Run a pipeline"""
    create_remote_container(user_input, recreate=rerun, output_lines=output_lines)
    containers = _list_remote_container(user_input)
    for container in containers:
        for _bl in bhelper.log_container(container, server=bconfig.get_server()):
            print(_bl.decode().rstrip())


@app.command("checksum")
def checksum(user_input):
    pipeline = bpipeline.user_input_to_pipeline(user_input)
    cprint(pipeline.checksum)


@app.callback()
def main(
    verbose: VerbosityLevel = typer.Option(
        VerbosityLevel.warning, case_sensitive=False
    ),
    plain: bool = False,
    server: T.Optional[str] = None,
):
    """
    Callback
    """
    bconfig.set_config("plain", plain)
    bconfig.set_config("verbosity", verbose.value)
    set_logger_level(verbose.value)

    if server is not None:
        bconfig.set_server(server)
    elif os.environ.get("BITIA_SERVER"):
        bconfig.set_server(os.environ["BITIA_SERVER"])
    else:
        # TODO: Read from default config file.
        pass
    cprint(f"Using server {bconfig.get_server()}")


@app.command()
def version():
    """version information"""
    cprint(bversion())


if __name__ == "__main__":
    app()
