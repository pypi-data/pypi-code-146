import os
from typing import Optional

from servicefoundry.auto_gen.models import DockerFileBuild
from servicefoundry.builder.docker_service import build_docker_image
from servicefoundry.logger import logger

__all__ = ["build"]


def _get_expanded_and_absolute_path(path: str):
    return os.path.abspath(os.path.expanduser(path))


def _build_docker_image(
    tag: str,
    path: str = ".",
    file: Optional[str] = None,
    cache_from: Optional[str] = None,
):
    path = _get_expanded_and_absolute_path(path)

    if file:
        file = _get_expanded_and_absolute_path(file)

    build_docker_image(
        path=path,
        tag=tag,
        # TODO: can we pick target platform(s) picked from cluster
        platform="linux/amd64",
        dockerfile=file,
        cache_from=[cache_from],
    )


def build(
    tag: str,
    build_configuration: DockerFileBuild,
    cache_from: Optional[str] = None,
):
    dockerfile_path = _get_expanded_and_absolute_path(
        build_configuration.dockerfile_path
    )
    with open(dockerfile_path) as f:
        dockerfile_content = f.read()
        logger.info("Dockerfile content:-")
        logger.info(dockerfile_content)

    _build_docker_image(
        tag=tag,
        path=build_configuration.build_context_path,
        file=build_configuration.dockerfile_path,
        cache_from=cache_from,
    )
