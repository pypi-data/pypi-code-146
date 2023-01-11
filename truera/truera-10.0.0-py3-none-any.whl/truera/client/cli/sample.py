import os

import click

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
import truera.client.model_preprocessing as model_processing


@click.group(help="Get a basic example of the given artifact.")
def sample():
    pass


@sample.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--format",
    default="yaml",
    required=False,
    type=click.Choice(['yaml', 'json'])
)
def feature_list(format):
    sample_source = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "util",
        "feature_list_sample." + format
    )

    with open(sample_source) as fp:
        click.echo(fp.read())


@sample.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--format",
    default="yaml",
    required=False,
    type=click.Choice(['yaml', 'json'])
)
def column_spec_file(format):
    sample_source = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "util",
        "column_spec_file_sample." + format
    )

    with open(sample_source) as fp:
        click.echo(fp.read())


@sample.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--output_dir",
    required=True,
    help="Output folder for the sample packaged python model."
)
@click.option(
    "--model_output_type",
    default="classification",
    type=click.Choice(['classification', 'regression'])
)
@click.option(
    "--model_path", help="Optional path to an already serialized model."
)
@click.option(
    "--code_file",
    multiple=True,
    help="Code file to be included with the model. Multiple are allowed."
)
def packaged_python_model(output_dir, model_output_type, model_path, code_file):
    UncaughtExceptionHandler.wrap(
        _package_sample_folder, output_dir, model_output_type, model_path,
        code_file
    )


def _package_sample_folder(
    output_dir, model_output_type, model_path, code_file
):
    logger = cli_logger.create_cli_logger(None)
    model_processing.prepare_template_model_folder(
        output_dir, model_output_type, model_path, code_file
    )
    click.echo("Done")
