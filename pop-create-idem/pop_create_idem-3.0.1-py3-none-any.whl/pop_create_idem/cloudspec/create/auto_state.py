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
        exec_ref = hub.cloudspec.parse.plugin.mod_ref(ctx, ref, plugin)

        # Set up the base template
        if not plugin.functions:
            to_write = hub.cloudspec.parse.plugin.header(plugin)

        else:
            to_write = hub.cloudspec.parse.plugin.header(plugin)
            mod_file.write_text(to_write)
            func_data = hub.cloudspec.parse.function.parse(
                plugin.functions, targets=("get", "list", "create", "update", "delete")
            )
            present_parameter = hub.cloudspec.parse.param.simple_map(
                plugin.functions["create"].params
            )

            # Make the get, list, create, delete, and update functions; these are required for every auto_state exec module
            for function_name in "get", "list", "create", "delete", "update":
                base_template = hub.cloudspec.template.auto_state[function_name.upper()]
                template_str = f"{base_template}\n    {cloud_spec.request_format[function_name]}\n\n\n"
                template = hub.tool.jinja.template(template_str)

                to_write += template.render(
                    service_name=cloud_spec.service_name,
                    function=dict(
                        ref=ref,
                        exec_ref=f"exec.{exec_ref}",
                        **func_data[function_name]["function"],
                    ),
                    parameter=func_data[function_name]["parameter"],
                    present_parameter=present_parameter,
                )

        mod_file.write_text(to_write)
