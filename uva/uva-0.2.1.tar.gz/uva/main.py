import time

import typer
from rich import print, box
from rich.console import Console
from rich.live import Live
from rich.table import Table

import uva.commands as commands

app = typer.Typer()


@app.command()
def login(
    username: str = typer.Option(
        ...,
        "--username",
        "-u",
        prompt="Enter your uva username",
        show_default=False,
        help="Your uva username"
    ),
    password: str = typer.Option(
        ...,
        "--password",
        "-p",
        prompt="Enter your uva password",
        show_default=False,
        hide_input=True,
        help="Your uva password"
    )
):
    """
        Logs you into the uva portal
    """
    commands.login(username, password)


@app.command()
def logout():
    commands.logout()


@app.command()
def latest_subs(count: int = 10):
    subs = commands.get_latest_subs(count)
    if subs:
        print(subs)


# 1 for ANSI, 2 for JAVA, 3 for C++, 4 for Pascal, 5 for C++11, 6 for Python.
@app.command()
def submit(problem_id: int, filepath: str, language: int):
    commands.submit(problem_id, filepath, language)


@app.command()
def pdf(problem_id: int):
    commands.get_pdf_file(str(problem_id))


if __name__ == "__main__":
    app()
