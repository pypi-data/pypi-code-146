import typer

from pathlib import Path

from .process_env.check_file_prop import checkExistingFile
from .process_env.conda_env_export import conda_env_export

app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome conda dependency export utility
    """


@app.command()
def export_env(envname: str = typer.Option(None, help="The conda environment name"), filename: Path = typer.Option("environment.yml", help="The conda dependency file name", dir_okay=True,
                                                                                                                   writable=True, resolve_path=True), force: bool = typer.Option(False, help="Use to overwrite existing environment.yml file")):
    """
    Export conda env with pip dependencies and version history
    """

    try:
        checkExistingFile(filename=filename, force=force)
        conda_env_export(filename=filename, envname=envname)
        print('Generated conda yml file')
        raise typer.Exit()
    except Exception as e:
        print(e)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
