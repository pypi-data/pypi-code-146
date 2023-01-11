import pathlib

import pop.hub
from dict_tools.data import NamespaceDict

if __name__ == "__main__":
    root_directory = pathlib.Path.cwd()
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="tool")
    hub.pop.sub.load_subdirs(hub.tool, recurse=True)
    ctx = NamespaceDict({{cookiecutter}})

    # Sanitize based on other arguments
    if ctx.has_acct_plugin:
        hub.tool.path.rmtree(root_directory / ctx.clean_name / "acct")
        hub.tool.path.rmtree(root_directory / ctx.clean_name / "tool")
        hub.tool.path.delete(
            root_directory / ctx.clean_name / "exec" / ctx.service_name / "sample.py"
        )
        hub.tool.path.delete(
            root_directory / ctx.clean_name / "states" / ctx.service_name / "sample.py"
        )
