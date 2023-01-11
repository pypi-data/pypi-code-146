"""
Functions for processing plugins
"""
import pathlib

from cloudspec import CloudSpecPlugin


def header(hub, plugin: CloudSpecPlugin) -> str:
    """
    Initialize the render of a plugin file and return the template
    """
    # noinspection JinjaAutoinspect
    template = hub.tool.jinja.template(hub.cloudspec.template.plugin.HEADER)

    return template.render(plugin=plugin)


def ref(hub, ctx, ref: str) -> str:
    split = ref.split(".")
    subs = split[:-1]
    mod = split[-1]
    return ".".join([ctx.service_name] + subs + [mod])


def mod_ref(hub, ctx, ref: str, plugin: CloudSpecPlugin) -> str:
    split = ref.split(".")
    subs = split[:-1]
    mod = split[-1]
    return ".".join([ctx.service_name] + subs + [plugin.virtualname or mod])


def touch(hub, root: pathlib.Path, ref: str):
    """
    Create all the files underneath the new sub
    """
    split = ref.split(".")
    subs = split[:-1]
    mod = split[-1]

    for sub in subs:
        root = root / sub
    root = root / f"{mod}.py"
    hub.tool.path.touch(root)
    return root
