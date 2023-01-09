from typing import Optional

import click

from clutchGen.handlers import (
    handle_create_template,
    handle_delete_template,
    handle_edit_template,
    handle_generate_project,
    handle_list_templates,
    handle_template_info,
)
from clutchGen.utils import complete_templates_names


@click.group()
def cli():
    pass


@cli.command("run")
@click.option(
    "--path",
    "-p",
    default="structure.yaml",
    help="Path to config file (default=structure.yaml)",
    type=click.Path(exists=True),
)
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable showing of processing logs")
def generate_project(path: str, verbose: bool):
    handle_generate_project(path, verbose)


@cli.group()
def templates():
    pass


@templates.command("list")
def list_():
    handle_list_templates()


@templates.command("new")
@click.argument("file", type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.option("-n", "--template-name", "template_name", prompt=True)
@click.option("-g", "--generation-name", "generation_name", prompt=True, required=False, default="")
def create(file: str, template_name: str, generation_name: Optional[str] = ""):
    handle_create_template(file, template_name, generation_name)


@templates.command("delete")
@click.argument("template_name", shell_complete=complete_templates_names)
def delete(template_name: str):
    handle_delete_template(template_name)


@templates.command("edit")
@click.argument("template_name", shell_complete=complete_templates_names)
@click.argument("field", type=click.Choice(["file", "name", "default-name"]))
@click.argument("value")
def edit(template_name: str, field, value):
    handle_edit_template(template_name, field, value)


@templates.command("info")
@click.argument("template_name", shell_complete=complete_templates_names)
def template_info(template_name: str):
    handle_template_info(template_name)


if __name__ == "__main__":
    cli()
