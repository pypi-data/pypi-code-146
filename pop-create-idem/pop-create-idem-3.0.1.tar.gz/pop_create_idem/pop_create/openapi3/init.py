import pathlib
from typing import Dict

import openapi3.object_base
import requests
import yaml
from dict_tools.data import NamespaceDict


def context(hub, ctx, directory: pathlib.Path):
    ctx = hub.pop_create.idem_cloud.init.context(ctx, directory)

    spec = hub.pop_create.openapi3.init.read(source=ctx.specification)

    api = openapi3.OpenAPI(spec, validate=True)
    errors = api.errors()
    if errors:
        for e in errors:
            hub.log.warning(e)

    # list these as defaults in the acct plugin
    if api.servers:
        ctx.servers = [x.url for x in api.servers]
    else:
        ctx.servers = ["https://"]

    hub.log.debug(f"Working with openapi spec version: {api.openapi}")
    ctx.cloud_api_version = api.info.version or "latest"
    ctx.clean_api_version = hub.tool.format.case.snake(ctx.cloud_api_version).strip("_")
    # If the api version starts with a digit then make sure it can be used for python namespacing
    if ctx.clean_api_version[0].isdigit():
        ctx.clean_api_version = "v" + ctx.clean_api_version

    cloud_spec = NamespaceDict(
        api_version=ctx.cloud_api_version,
        project_name=ctx.project_name,
        service_name=ctx.service_name,
        request_format=hub.pop_create.openapi3.template.HTTP_REQUEST.format(
            acct_plugin=ctx.acct_plugin
        ),
        plugins=hub.pop_create.openapi3.parse.plugins(ctx, api.paths),
    )
    ctx.cloud_spec = cloud_spec

    hub.pop_create.init.run(directory=directory, subparsers=["idem_cloud"], **ctx)
    return ctx


def read(hub, source: str or Dict):
    """
    If the path is a file, then parse the json contents of the file,
    If the path is a url, then return a json response from the url.
    """
    if isinstance(source, Dict):
        return source

    path = pathlib.Path(source)

    if path.exists():
        with path.open("r") as fh:
            ret = yaml.safe_load(fh)
    else:
        request = requests.get(source, headers={"Content-Type": "application/json"})
        ret = request.json()

    return ret
