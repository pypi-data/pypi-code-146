import subprocess
import sys
from typing import List

from docker.errors import APIError, BuildError

import docker
from servicefoundry.logger import logger

__all__ = [
    "push_docker_image",
    "docker_build",
    "pull_docker_image",
    "push_docker_image_with_latest_tag",
]


def _get_docker_client():
    try:
        return docker.from_env()
    except Exception as ex:
        raise Exception("Could not connect to Docker") from ex


# this is required since push does throw an error if it
# fails - so we have to parse the response logs to catch the error
# the other option is to run `docker login` as a subprocess but it's
# not recommended to provide password to subprocess
def catch_error_in_push(response: List[dict]):
    for line in response:
        if line.get("error") is not None:
            raise Exception(
                f'Failed to push to registry with message \'{line.get("error")}\''
            )


def build_docker_image(
    path: str, tag: str, platform: str, dockerfile: str, cache_from: List[str]
):
    logger.info("Starting docker build...")
    try:
        for result in _get_docker_client().api.build(
            decode=True,
            path=path,
            tag=tag,
            platform=platform,
            dockerfile=dockerfile,
            cache_from=cache_from,
        ):
            for (_, value) in result.items():
                if isinstance(value, str):
                    logger.info(value)
    except (BuildError, APIError) as ex:
        raise Exception("Error while building Docker image") from ex


def push_docker_image(
    image_uri: str,
    docker_login_username: str,
    docker_login_password: str,
):
    client = _get_docker_client()
    auth_config = {"username": docker_login_username, "password": docker_login_password}

    logger.info(f"Pushing {image_uri}")
    response = client.images.push(
        repository=image_uri, auth_config=auth_config, decode=True, stream=True
    )
    catch_error_in_push(response=response)


def push_docker_image_with_latest_tag(
    image_uri: str,
    docker_login_username: str,
    docker_login_password: str,
):
    client = _get_docker_client()
    auth_config = {"username": docker_login_username, "password": docker_login_password}

    repository_without_tag, _ = image_uri.rsplit(":", 1)
    image = client.images.get(image_uri)
    image.tag(repository=repository_without_tag, tag="latest")

    logger.info(f"Pushing {repository_without_tag}:latest")
    response = client.images.push(
        repository=repository_without_tag,
        tag="latest",
        auth_config=auth_config,
        decode=True,
        stream=True,
    )
    catch_error_in_push(response=response)


def pull_docker_image(
    image_uri: str,
    docker_login_username: str,
    docker_login_password: str,
):
    auth_config = {"username": docker_login_username, "password": docker_login_password}
    logger.info(f"Pulling cache image {image_uri}")
    _get_docker_client().images.pull(repository=image_uri, auth_config=auth_config)
