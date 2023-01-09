import click

from clutchGen.configs import get_default_file_name, get_template_file


def handle_template_info(template_name: str):
    click.echo(f"Template {get_template_file(template_name)}")
    default_name = get_default_file_name(template_name)
    if default_name:
        click.echo(f"Default generation filename {default_name}")
