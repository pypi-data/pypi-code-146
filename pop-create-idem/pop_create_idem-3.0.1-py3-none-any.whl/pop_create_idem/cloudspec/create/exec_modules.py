import pathlib

from cloudspec import CloudSpec


def run(hub, ctx, root_directory: pathlib.Path or str):
    if isinstance(root_directory, str):
        root_directory = pathlib.Path(root_directory)
    cloud_spec = CloudSpec(**ctx.cloud_spec)
    exec_dir = root_directory / ctx.clean_name / "exec" / ctx.service_name

    for ref, plugin in cloud_spec.plugins.items():
        mod_file = hub.cloudspec.parse.plugin.touch(exec_dir, ref)
        ref = hub.cloudspec.parse.plugin.ref(ctx, ref)
        cli_ref = hub.cloudspec.parse.plugin.mod_ref(ctx, ref, plugin)

        to_write = hub.cloudspec.parse.plugin.header(plugin)

        for function_name, function_data in plugin.functions.items():
            template = hub.tool.jinja.template(
                f"{hub.cloudspec.template.exec.FUNCTION}\n    {cloud_spec.request_format}\n\n\n"
            )

            function_alias = plugin.func_alias.get(function_name, function_name)

            to_write += template.render(
                function=dict(
                    name=function_name,
                    hardcoded=function_data.hardcoded,
                    doc=hub.cloudspec.create.function.doc(function_data)
                    + hub.cloudspec.parse.param.sphinx_doc(function_data.params)
                    + hub.cloudspec.parse.function.return_type(function_data),
                    ref=f"{ref}.{function_alias}",
                    cli_ref=f"{cli_ref}.{function_alias}",
                    header_params=hub.cloudspec.parse.param.headers(
                        function_data.params
                    ),
                    required_call_params=hub.cloudspec.parse.param.callers(
                        function_data.params
                    ),
                    return_type=function_data.return_type,
                ),
                parameter=dict(
                    mapping=hub.cloudspec.parse.param.mappings_get_map_params(
                        function_data.params
                    )
                ),
            )

        mod_file.write_text(to_write)
