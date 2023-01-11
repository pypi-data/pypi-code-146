import pprint

"""
A sample state using the sample idem_cloud modules for an idea of what a state module should look like.
By convention, all states should have a "present" and an "absent" function, nothing else.
"""


async def present(hub, ctx, name: str, **kwargs):
    """
    Ensure that a resource exists and is in the correct state.

    Example:

    .. code-block:: sls

        my_state_name:
          {{cookiecutter.service_name}}.sample.present:
            name: item_name
            acct_profile: default
            my_kwarg: my_value
    """
    try:
        if name in await hub.exec.{{cookiecutter.service_name}}.sample.list(ctx)["ret"]:
            comment = f"{name} is already exists"
            my_instance = before = await hub.exec.{{cookiecutter.service_name}}.sample.get(ctx, name)["ret"]
        else:
            before = {}
            if ctx.test:
                # If `idem state` was run with the `--test` flag, then don't actually make any changes
                comment = (
                    f"{name} would be created with kwargs: {pprint.pformat(kwargs)}"
                )
            else:
                hub.exec.{{cookiecutter.service_name}}.create(ctx, name, **kwargs)
                comment = f"Created {name} with kwargs: {pprint.pformat(kwargs)}"
            # Now that it exists, retrieve it
            my_instance = await hub.exec.{{cookiecutter.service_name}}.sample.get(ctx, name)["ret"]

        # TODO verify that my_instance is in the correct state and has all the correct parameters
        # TODO This is where the heavy lifting takes place
        # TODO call idem_cloud modules to update the instance as needed.
        # TODO If ctx.test is True, then only comment on what changes would be made

        after = await hub.exec.{{cookiecutter.service_name}}.sample.get(ctx, name)["ret"]
        changes = {"old": before, "new": after}
        result = True
    except Exception as e:
        comment = str(e)
        changes = {}
        result = False

    # This is what is expected of every state return
    return {
        "name": name,
        "changes": changes,
        "result": result,
        "comment": comment,
    }


async def absent(hub, ctx, name: str, **kwargs):

    """
    A sample state using the sample idem_cloud modules for an idea of what an absent function should look like.

    Example:

    .. code-block:: sls

        my_state_name:
          {{cookiecutter.service_name}}.sample.absent:
            name: item_name
            acct_profile: default
            my_kwarg: my_value
    """
    try:
        if name not in await hub.exec.{{cookiecutter.service_name}}.sample.list(ctx)["ret"]:
            comment = f"{name} is already absent"
            before = {}
        else:
            before = await hub.exec.{{cookiecutter.service_name}}.sample.get(ctx, name)["ret"]
            if ctx.test:
                # If `idem state` was run with the `--test` flag, then don't actually make any changes
                comment = (
                    f"{name} would be deleted with kwargs: {pprint.pformat(kwargs)}"
                )
            else:
                hub.exec.{{cookiecutter.service_name}}.delete(ctx, name, **kwargs)["ret"]
                comment = f"Deleted {name} with kwargs: {pprint.pformat(kwargs)}"

        # Some clouds will return an empty dict, some will return an object that is "pending deletion"
        after = await hub.exec.{{cookiecutter.service_name}}.sample.get(ctx, name)["ret"]
        changes = {"old": before, "new": after}
        result = True
    except Exception as e:
        result = False
        changes = {}
        comment = str(e)

    # This is what is expected of every state return
    return {
        "name": name,
        "changes": changes,
        "result": result,
        "comment": comment,
    }
