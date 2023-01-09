import click

from clutchGen.file_parser import parse_file
from clutchGen.generator import generate_structure
from clutchGen.render_context import set_default_render_context


def handle_generate_project(path: str, verbose: bool) -> None:
    structure, _default_context = parse_file(path)
    set_default_render_context(_default_context)
    click.echo("Generating project")
    generate_structure(structure)
