import pathlib
import urllib.request

from dict_tools.data import NamespaceDict

HAS_LIBS = (True,)


def __virtual__(hub):
    return HAS_LIBS


def context(hub, ctx, directory: pathlib.Path):
    ctx = hub.pop_create.idem_cloud.init.context(ctx, directory)
    ctx.servers = [None]
    ctx.service_name = "k8s"
    ctx.has_acct_plugin = False

    release_version = "release-23.0"
    open_api_spec = f"https://raw.githubusercontent.com/kubernetes-client/python/{release_version}/scripts/swagger.json"
    resource = hub.OPT.pop_create.resource or "all"

    # Download and parse open-api spec for k8s python client to get plugin metadata
    plugins = {}
    with urllib.request.urlopen(open_api_spec) as f:
        k8s_openapi_spec_str = f.read().decode("utf-8")
        if k8s_openapi_spec_str:
            plugins = hub.pop_create.k8s.plugin.get_plugins(
                k8s_openapi_spec_str=k8s_openapi_spec_str, resource=resource
            )

    # Initialize cloud spec
    ctx.cloud_spec = NamespaceDict(
        api_version=release_version,
        project_name=ctx.project_name,
        service_name=ctx.service_name,
        request_format={
            "present": hub.pop_create.k8s.template.PRESENT_REQUEST_FORMAT,
            "absent": hub.pop_create.k8s.template.ABSENT_REQUEST_FORMAT,
            "describe": hub.pop_create.k8s.template.DESCRIBE_REQUEST_FORMAT,
        },
        plugins=plugins,
    )

    hub.cloudspec.init.run(
        ctx,
        directory,
        create_plugins=["state_modules"],
    )
    ctx.cloud_spec.plugins = {}
    return ctx
