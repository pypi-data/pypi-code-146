"""CLI Helpers"""

import sys

import click


def success(message: str, newline=True):
    click.secho(message, fg="green", nl=newline)


def warn(message: str):
    click.secho(message, fg="yellow")


def info(message: str, bold=False):
    click.secho(message, bold=bold)


def error(message: str, color="red"):
    click.secho(message, fg=color, err=True)


# This function is for errors that are followed by program exit
def fail(
    message="Something went wrong",
    hint="Please check the Sym documentation at https://docs.symops.com/",
):
    """Raise a usage error with a useful message"""
    click.secho(f"✖ {message}.", fg="red", bold=True, err=True)
    click.secho(f"{hint}.", fg="cyan")

    sys.exit(1)
