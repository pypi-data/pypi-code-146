import invoke
from invoke import Collection

from . import image, misc, pypi


@invoke.task
def clean(ctx):
    """
    Remove all intermediate files from the source tree.
    """
    ctx.run("git clean -xdf")


ns = Collection()
ns.add_task(clean)
ns.add_collection(pypi)
ns.add_collection(image)
ns.add_collection(misc)
