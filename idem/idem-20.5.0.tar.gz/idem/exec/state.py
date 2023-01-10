# An exec module that can run states


async def run(
    hub,
    path: str,
    name: str = None,
    acct_profile: str = None,
    test: bool = False,
    *args,
    **kwargs,
):
    """
    Trigger a state manually from the CLI.
    This skips ESM, Reconciliation, and some parts of State contracts.
    This is useful in scenarios when you want to run a state directly without any file inputs.

    Generic example:

    .. code-block:: bash

        $ idem exec state.run <state.ref> kwarg1=value1 test=True acct_profile=default

    Specific example:

    .. code-block:: bash

        $ idem exec state.run time.sleep duration=1 test=True --output=json
    """
    # Construct the ctx that a state uses
    ctx = await hub.idem.acct.ctx(
        f"states.{path}",
        profile=acct_profile or hub.OPT.idem.get("acct_profile"),
        acct_key=hub.OPT.acct.get("acct_key"),
        acct_file=hub.OPT.acct.get("acct_file"),
        hard_fail=True,
        validate=True,
    )
    # Override ctx.test with the value from the parameters
    ctx.test = test

    # Call the state with the given parameters and await the result
    ret = await hub.pop.loop.unwrap(hub.states[path](ctx, name=name, *args, **kwargs))

    return {
        "result": ret["result"],
        "comment": ret["comment"],
        "ret": ret["new_state"],
        "test": test,
    }
