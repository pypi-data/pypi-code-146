import pathlib
import tempfile

__contracts__ = ["soft_fail"]

SKIP_ESM = True


async def block(hub, ctx, name: str, sls: str = None, render: str = None):
    """
    Render a block of sls and add it to the state runs

    .. code-block:: sls

        delay:
          time.sleep:
            - duration: 2

        delayed_render_block:
          render.block:
            - block: >
               # Use "raw" statements so jinja doesn't process this block in the first pass through the renderer
               {% raw %}
               # new state to be processed

               new_state:
                 exec.run:
                   - path: test.ping

               {% endraw %}
            # Only process these new states after other requirements have been met
            - require:
               - time: delay

    """
    result = dict(comment=[], new_state={}, old_state=None, name=name, result=True)
    # Create a temporary run name to use while compiling the new sls block
    temporary_run = f"delayed-render-{name}"
    main_run = ctx.run_name

    # Write the new sls block to a temporary to a temporary file
    # So that it can be processed the same way as input sls
    with tempfile.NamedTemporaryFile(suffix=".sls", delete=True) as fh:
        fh.write(sls.encode())
        fh.flush()
        path = pathlib.Path(fh.name)
        # Pass through other sources from the main run to resolve includes in the new sls with existing sources
        sources = [f"file://{path.parent.absolute()}"] + hub.idem.RUNS[main_run][
            "sls_sources"
        ]

        # Create a temporary run to process the new sls block
        await hub.idem.state.create(
            name=temporary_run,
            sls_sources=sources,
            # Allow a different render pipe to be used for the new render block
            # Default to the renderer of the main run
            render=render or hub.idem.RUNS[main_run].get("render"),
            # Copy state.apply parameters from the main run
            **{
                k: hub.idem.RUNS[main_run].get(k)
                for k in (
                    "runtime",
                    "subs",
                    "cache_dir",
                    "test",
                    "acct_file",
                    "acct_key",
                    "acct_profile",
                    "acct_blob",
                    "managed_state",
                    "param_sources",
                    "acct_data",
                    "invert_state",
                )
            },
        )
        try:
            # Resolve the new sls block with the main run
            gather_data = await hub.idem.resolve.init.gather(
                main_run, f"{path.stem}", sources=sources
            )
            # Add the newly resolved blocks to the temporary run
            await hub.idem.sls_source.init.update(temporary_run, gather_data)

            # Report any errors from compiling the new render block
            if hub.idem.RUNS[temporary_run]["errors"]:
                result["result"] = False
                result["comment"].extend(hub.idem.RUNS[temporary_run]["errors"])
            else:
                # Iterate over the states added to the temporary run
                for new_name, new_state in hub.idem.RUNS[temporary_run]["high"].items():
                    # If a state name from the new render block has the same name as a state in the main run, then fail
                    if new_name in hub.idem.RUNS[main_run]["high"]:
                        result["result"] = False
                        result["comment"].append(
                            f"State named '{new_state}' already exists in the run"
                        )
                        # Don't add the duplicate state to the main run
                        continue
                    else:
                        # Report the state that was added to the run in this state's output
                        result["new_state"][new_name] = new_state
                        # Add the state from the new render block to the main run
                        hub.idem.RUNS[main_run]["high"][new_name] = new_state
        finally:
            # Clear the temporary run we created
            hub.idem.RUNS.pop(temporary_run, None)

    return result


def is_pending(hub, ret):
    """
    Always skip reconciliation for this plugin
    """
    return False
