import pathlib

import pop.hub
from dict_tools.data import NamespaceDict

if __name__ == "__main__":
    root_directory = pathlib.Path.cwd()

    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="pop_create")
    hub.pop.sub.add(dyne_name="config")
    hub.config.integrate.load(["pop_create"], "pop_create", parse_cli=False, logs=False)
    ctx = NamespaceDict({{cookiecutter}})

    idem_dynes = ["exec", "states"]
    if not ctx.has_acct_plugin:
        idem_dynes.append("tool")
        idem_dynes.append("acct")

    dyne_list = set(idem_dynes + list(ctx.short_dyne_list))
    # FIXME generating tests is problematic for some reason
    # pop_create_core = ["seed", "tests", "docs"]
    pop_create_core = ["seed", "docs"]
    seed_ctx = NamespaceDict(vertical=True, dyne_list=dyne_list)

    if "cloud_spec" not in ctx:
        # The openapi3/swagger plugin might call this with their own spec
        ctx.cloud_spec = {}

    # Bring in the full context, but don't override any of our overrides
    for k in ctx:
        if k not in seed_ctx:
            seed_ctx[k] = ctx[k]

    # Run a traditional pop seed on the directory with common idem states
    hub.pop_create.init.run(
        directory=root_directory, subparsers=pop_create_core, **seed_ctx
    )
