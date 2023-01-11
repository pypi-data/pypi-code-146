import pathlib

import pop.hub
from dict_tools.data import NamespaceDict

if __name__ == "__main__":
    root_directory = pathlib.Path.cwd()

    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="pop_create")
    hub.pop.sub.add(dyne_name="cloudspec")
    hub.pop.sub.add(dyne_name="config")
    hub.config.integrate.load(
        ["cloudspec", "pop_create"], "cloudspec", parse_cli=False, logs=False
    )
    ctx = NamespaceDict({{cookiecutter}})

    hub.cloudspec.init.run(
        ctx,
        root_directory,
        create_plugins=["exec_modules", "tests", "docs"],
    )

    # Sanitize based on other arguments
    if ctx.has_acct_plugin:
        hub.tool.path.rmtree(root_directory / ctx.clean_name / "acct")
        hub.tool.path.rmtree(root_directory / ctx.clean_name / "tool")

    # End with the cicd template
    hub.pop_create.init.run(directory=root_directory, subparsers=["cicd"], **ctx)

    # TODO Run sphinx on the docstrings to make sure it all works
