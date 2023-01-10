from typing import Optional

import typer
from rich import print

import uva.commands as commands

app = typer.Typer()


@app.command()
def login(
    username: str = typer.Option(
        None,
        "--username",
        "-u",
        prompt="Enter your uva username",
        show_default=False,
        help="Your uva username"
    ),
    password: str = typer.Option(
        None,
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
def submit(
        problem_id: int = typer.Option(
          ...,
          "--problem-id",
          "-id",
          show_default=False,
          help="Uva problem id"
        ),
        filepath: str = typer.Option(
            ...,
            "--filepath",
            "-f",
            show_default=False,
            help="Path to the solution file"
        ),
        language: int = typer.Option(
            None,
            "--language",
            "-l",
            show_default=False,
            help="1 for ANSI, 2 for JAVA, 3 for C++, 4 for Pascal, 5 for C++11, 6 for Python."
        )
):
    commands.submit(problem_id, filepath, language)


@app.command()
def latest_subs(count: int = 10):
    subs = commands.get_latest_subs(count)
    if subs:
        print(subs)


@app.command()
def pdf(problem_id: int):
    commands.get_pdf_file(str(problem_id))


if __name__ == "__main__":
    app()
