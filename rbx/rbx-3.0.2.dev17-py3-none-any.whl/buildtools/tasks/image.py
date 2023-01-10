from os import environ, getcwd, path

import invoke

from .. import REGISTRY

BASEPATH = path.basename(getcwd())


@invoke.task(name="build", iterable=["build_arg"])
def build_image(ctx, build_arg=None, name=None, version=None, target=None, test=False):
    """Build the docker image.

    The image name defaults to the name of the working folder.
    It can be overriden with the $SERVICE environment variable.

    The version defaults to 'develop'.
    It can be overriden with the $VERSION environment variable.

    Note that parameters always take precedence over environment variables.
    """
    command = ["docker build"]

    if target:
        command.append("--target {}".format(target))

    if test:
        command.append("--build-arg INSTALL_TEST_DEPENDENCIES=yes")

    for arg in build_arg:
        command.append("--build-arg {}".format(arg))

    command.append(
        "-t {registry}/{repository}:{version} .".format(
            registry=REGISTRY,
            repository=name or environ.get("SERVICE", BASEPATH),
            version=version or environ.get("VERSION", "develop"),
        )
    )

    command = " ".join(command)
    ctx.run(command)


@invoke.task(name="upload")
def upload_image(ctx, name=None, version=None):
    """Login then upload the docker image to the registry.

    The image name defaults to the name of the working folder.
    It can be overriden with the $SERVICE environment variable.

    The version defaults to 'develop'.
    It can be overriden with the $VERSION environment variable.

    Needless to say, this image must have been already built.

    Note that parameters always take precedence over environment variables.
    """
    ctx.run("`aws ecr get-login --no-include-email`")
    command = "docker push {registry}/{repository}:{version}".format(
        registry=REGISTRY,
        repository=name or environ.get("SERVICE", BASEPATH),
        version=version or environ.get("VERSION", "develop"),
    )
    ctx.run(command)
