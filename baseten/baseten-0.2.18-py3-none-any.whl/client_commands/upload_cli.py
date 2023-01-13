from pathlib import Path

import click

from baseten.common.files import TrainingType, upload_dataset


@click.group()
def upload():
    pass


@upload.command()
@click.argument("data_dir", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("--name", "-n", required=True, type=str)
@click.option(
    "--training-type",
    "-t", required=True,
    type=click.Choice([t.value for t in TrainingType], case_sensitive=False)
)
def dataset(data_dir, name, training_type):
    dataset_id = upload_dataset(name, Path(data_dir), TrainingType[training_type.upper()])
    click.echo()
    click.echo(f"Dataset ID:\n{dataset_id}")
