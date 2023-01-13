
import typer
from pathlib import Path
import os


def checkFileName(filename: Path):
    filename = str(filename)

    if not filename.endswith(('.yml', '.txt')):
        print('Provide filename with extension as yml or txt')
        raise typer.Exit(code=1)

    return


def checkExistingFile(filename: Path, force: bool):

    checkFileName(filename=filename)

    exists = os.path.isfile(filename)

    if exists and not force:
        print('Use --force to overwrite file')
        raise typer.Exit(code=1)

    return
