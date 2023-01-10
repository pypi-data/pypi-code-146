from os import environ

import invoke
from fabric import Connection

from .. import CONFIGURATIONS


@invoke.task
def deploy(
    ctx, host, user, key_filename, service, environment, sandboxed=None, version=None
):
    """Deploy a new Docker image and start the container on a Remote Server.

    The sandboxed flag defaults to 'false'.
    It can be overriden with the $SANDBOXED environment variable.

    The version defaults to 'develop'.
    It can be overriden with the $VERSION environment variable.

    Note that passing the parameters always takes precedence over the environment variables.
    """
    if sandboxed is None:
        sandboxed = environ.get("SANDBOXED", "false")

    if version is None:
        version = environ.get("VERSION", "latest")

    connection = Connection(
        host=host, user=user, connect_kwargs={"key_filename": key_filename}
    )

    # Login to Scoota Docker Registry
    connection.run("`aws ecr get-login --no-include-email`", echo=True)

    # Get the latest configuration for the Server we are deploying to.
    # Valid configurations are located at '/<Service>/<Env>/'
    connection.run(
        "aws s3 sync {config}/{service}/{env} {service}".format(
            config=CONFIGURATIONS, env=environment, service=service
        ),
        echo=True,
    )

    # Restart the Docker container forcing recreate so that new version is used.
    # Using `force-recreate` alone doesn't seem to be enough to use the latest version. So we
    # do `down` and then `up`.
    connection.run(
        "docker-compose -p {service}{env} -f {service}/docker-compose.yml down"
        " --volumes --remove-orphans".format(service=service, env=environment),
        echo=True,
        env={
            "SANDBOXED": sandboxed,
            "VERSION": version,
        },
        warn=True,
    )
    connection.run(
        "docker-compose -p {service}{env} -f {service}/docker-compose.yml up -d".format(
            service=service, env=environment
        ),
        echo=True,
        env={
            "SANDBOXED": sandboxed,
            "VERSION": version,
        },
    )

    # Remove all unused Docker Images
    connection.run("docker rmi `docker images -q` || true", echo=True)
    connection.run("docker rm `docker ps -a -q` || true", echo=True)


ns = invoke.Collection(deploy)
