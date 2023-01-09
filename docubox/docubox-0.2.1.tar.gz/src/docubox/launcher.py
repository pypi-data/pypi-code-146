#!python.exe
import importlib.util
import pathlib
import re
import sys

description = """DocuBox - The swiss army knife for document solution powered by Python.
Copyright (C) 2022,2023 Hiroshi Miura

DocuBox is a single binary utility that have several document solution commands.
When it is called as sphinx-build, it behave as sphinx.
When it is called as mkdocs, it behave as mkdocs.

Please symbolic link to the name you want.

Supported features
"""

commands = [
    # (command name, package, func)
    ("babel", "babel.messages.frontend", "main"),
    ("j2", "j2cli", "main"),
    ("jinja2", "jinja2.ext", "babel_extract"),
    ("jsonschema", "jsonxchema.cli", "main"),
    ("m2r", "m2r", "main"),
    ("markdown_it", "markdown_it.cli.parse", "main"),
    ("mkdocs", "mkdocs.__main__", "cli"),
    ("myst-anchors", "myst_parser.cli", "print_anchors"),
    ("myst-docutils-html", "myst_parser.cli.docutils_", "cli_html"),
    ("myst-docutils-html5", "myst_parser.cli.docutils_", "cli_html5"),
    ("myst-docutils-latex", "myst_parser.cli.docutils_", "cli_latex"),
    ("myst-docutils-pseudoxml", "myst_parser.cli.docutils_", "cli_pseudoxml"),
    ("myst-docutils-xml", "myst_parser.cli.docutils_", "cli_xml"),
    ("pygmentize", "pygments.cmdline", "main"),
    ("sphinx-apidoc", "sphinx.ext.apidoc", "main"),
    ("sphinx-autogen", "sphinx.ext.autosummary.generate", "main"),
    ("sphinx-build", "sphinx.cmd.build", "main"),
    ("sphinx-quickstart", "sphinx.cmd.quickstart", "main"),
    ("sphinx-intl", "sphinx_intl.commands", "main"),
]


def main():
    cmdname = pathlib.Path(sys.argv[0]).name.lower()
    for cmd in commands:
        if cmdname == cmd[0]:
            try:
                mod = importlib.import_module(cmd[1])
                func = getattr(mod, cmd[2])
                return(func())
            except ModuleNotFoundError as e:
                print(e.msg)
                break
    # unknown command or got exception
    print(description)
    for cmd in commands:
        print(f"- {cmd[0]}")
    return(1)


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
