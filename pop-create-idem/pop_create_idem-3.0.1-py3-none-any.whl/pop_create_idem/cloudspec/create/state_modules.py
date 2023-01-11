import pathlib

from cloudspec import CloudSpec


def run(hub, ctx, root_directory: pathlib.Path or str):
    if isinstance(root_directory, str):
        root_directory = pathlib.Path(root_directory)
    cloud_spec = CloudSpec(**ctx.cloud_spec)
    states_dir = root_directory / ctx.clean_name / "states" / ctx.service_name

    for ref, plugin in cloud_spec.plugins.items():
        mod_file = hub.cloudspec.parse.plugin.touch(states_dir, ref)
        ref = hub.cloudspec.parse.plugin.ref(ctx, ref)
        state_ref = hub.cloudspec.parse.plugin.mod_ref(ctx, ref, plugin)
        to_write = hub.cloudspec.parse.plugin.header(plugin)
        if not plugin.functions:
            mod_file.write_text(to_write)
            continue
        func_data = hub.cloudspec.parse.function.parse(
            plugin.functions, targets=("present", "absent", "describe")
        )
        present_parameter = hub.cloudspec.parse.param.simple_map(
            plugin.functions["present"].params
        )
        common_params = {}
        for name, param in plugin.functions["absent"].params.items():
            if name in plugin.functions["describe"].params:
                common_params[name] = plugin.functions["describe"].params[name]

        common_params = hub.cloudspec.parse.param.mappings(common_params)

        # Create the present, absent, and describe functions; these are required for every state module
        for function_name, TEMPLATE in zip(
            ("present", "absent", "describe"),
            (
                hub.cloudspec.template.state.PRESENT_FUNCTION,
                hub.cloudspec.template.state.ABSENT_FUNCTION,
                hub.cloudspec.template.state.DESCRIBE_FUNCTION,
            ),
        ):
            template = hub.tool.jinja.template(
                f"{TEMPLATE}\n    {cloud_spec.request_format[function_name]}\n\n\n"
            )

            to_write += template.render(
                service_name=cloud_spec.service_name,
                function=dict(
                    ref=ref,
                    state_ref=f"states.{state_ref}",
                    **func_data[function_name]["function"],
                ),
                parameter=func_data[function_name]["parameter"],
                present_parameter=present_parameter,
                get_params=common_params,
            )

            mod_file.write_text(to_write)
