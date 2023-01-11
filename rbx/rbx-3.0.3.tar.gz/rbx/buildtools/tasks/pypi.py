import invoke


@invoke.task
def check(ctx):
    """
    Check Python package distribution manifest.
    """
    ctx.run("check-manifest -v")


@invoke.task
def build(ctx):
    """
    Build Python package distribution locally.
    """
    ctx.run("python setup.py sdist bdist_wheel")


@invoke.task(check, build)
def upload(ctx):
    """
    Check, build, and upload Python package distribution to local PyPI.
    """
    ctx.run("twine upload dist/* -r scoota-pypi")
