import os
import subprocess
import sys

import click

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
from truera.client.client_environment import connection_string_message
from truera.client.feature_client import FeatureClient
import truera.client.model_preprocessing as model_processing
import truera.client.services.artifact_interaction_client as cl


@click.group(
    help=
    "Commands for verifying packaged models and other artifacts before upload."
)
def verify():
    pass


@verify.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--dir_to_check",
    "--dir",
    help="Path to directory to verify.",
    required=True
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def python_model(dir_to_check, log_level):
    UncaughtExceptionHandler.wrap(_verify_pyfunc_model, dir_to_check, log_level)


def _verify_pyfunc_model(dir_to_check, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    model_processing.verify_python_model_folder(dir_to_check, logger=logger)


@verify.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--dir_to_check",
    "--dir",
    help="Path to directory to verify.",
    required=True
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def h2o_model(dir_to_check, log_level):
    UncaughtExceptionHandler.wrap(_verify_h2o_model, dir_to_check, log_level)


def _verify_h2o_model(dir_to_check, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    model_processing.verify_h2o_model_folder(dir_to_check, logger)


@verify.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--dir_to_check",
    "--dir",
    help="Path to directory to verify.",
    required=True
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def datarobot_model(dir_to_check, log_level):
    UncaughtExceptionHandler.wrap(
        _verify_datarobot_model, dir_to_check, log_level
    )


def _verify_datarobot_model(dir_to_check, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    model_processing.verify_datarobot_model_folder(dir_to_check, logger)


@verify.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--dir_to_check",
    "--dir",
    help="Path to directory to verify.",
    required=True
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def pmml_model(dir_to_check, log_level):
    UncaughtExceptionHandler.wrap(_verify_pmml_model, dir_to_check, log_level)


def _verify_pmml_model(dir_to_check, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    model_processing.verify_pmml_model_folder(dir_to_check, logger)


@verify.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=cli_utils.feature_is_hidden("neural_network")
)
@click.option(
    "--model_dir", help="Path to model directory to verify.", required=True
)
@click.option(
    "--data_dir", help="Path to dataset directory to verify.", required=True
)
@click.option(
    "--python_executable",
    "--python",
    help=
    "Path to a Python executable to run the model in. If not provided, then default environment will be used.",
    callback=cli_utils.validate_file
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def nn_model(model_dir, data_dir, python_executable, log_level):
    UncaughtExceptionHandler.wrap(
        _verify_nn_model, model_dir, data_dir, python_executable, log_level
    )


def _verify_nn_model(model_dir, data_dir, python_executable, log_level):
    python_executable = python_executable or "python"
    script = os.path.join(os.path.dirname(__file__), "verify_nn_ingestion.py")
    command = f"{python_executable} {script} --model_dir={model_dir} --data_dir={data_dir} --log_level={log_level}"
    if subprocess.run(["bash", "-c", command]).returncode != 0:
        sys.exit(1)
    click.echo("Done")


@verify.command(
    help=
    "Given a feature map file, verify that the map is in a valid form from the given pre to post transform files. This assumes that the pre and post transform files have headers with the columns.",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.option(
    "--map_file", "-f", help="Path to feature map to verify.", required=True
)
@click.option(
    "--pre_transform_path",
    "--pre",
    help="Path to an example pre transform file with a header the map is from.",
    required=True
)
@click.option(
    "--post_transform_path",
    "--post",
    help="Path to an example post transform file with a header the map is to.",
    required=True
)
@click.option("--id_column", help="Id column of data.")
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def feature_map(
    map_file, pre_transform_path, post_transform_path, id_column, log_level
):
    UncaughtExceptionHandler.wrap(
        _verify_feature_map, map_file, pre_transform_path, post_transform_path,
        id_column, log_level
    )


def _verify_feature_map(
    map_file, pre_transform_path, post_transform_path, id_column, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    FeatureClient.verify_feature_map_from_map_file(
        map_file,
        pre_transform_path,
        post_transform_path,
        logger,
        id_column=id_column
    )
    click.echo("Done")


# Could eventually be merged into set connection string
@verify.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def connection(connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _verify_connection, connection_string, log_level
    )


def _verify_connection(connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        logger.info("Succeeded!")


@verify.command(
    help=
    "Given a packaged model, feature map file, and data verify that the model can be loaded in a given conda environment.",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.option(
    "--model",
    "-m",
    help="Path to a packaged model to verify.",
    callback=cli_utils.validate_directory,
    required=True
)
@click.option(
    "--model_output_type",
    "--ot",
    help="Type of output from the model.",
    default="classification",
    type=click.Choice(["classification", "regression"])
)
@click.option(
    "--map_file",
    "-f",
    help="Path to feature map to use to verify.",
    callback=cli_utils.validate_file
)
@click.option(
    "--pre_transform_path",
    "--pre",
    help="Path to an example pre transform file with a header the map is from.",
    callback=cli_utils.validate_file
)
@click.option(
    "--post_transform_path",
    "--post",
    help="Path to an example post transform file with a header the map is to.",
    callback=cli_utils.validate_file
)
@click.option(
    "--labels_path",
    "--label",
    help="Path to a label file with without a header.",
    callback=cli_utils.validate_file,
    required=True
)
@click.option("--id_column", help="Id column of data.")
@click.option(
    "--python_executable",
    "--python",
    help=
    "Path to a Python executable to run the model in. If not provided, then default environment will be used.",
    callback=cli_utils.validate_file
)
@click.option("--skip_confirmation", "--skip", is_flag=True, default=False)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def packaged_model(
    model, model_output_type, map_file, pre_transform_path, post_transform_path,
    labels_path, id_column, python_executable, skip_confirmation, log_level
):
    UncaughtExceptionHandler.wrap(
        _verify_packaged_model, model, model_output_type, map_file,
        pre_transform_path, post_transform_path, labels_path, id_column,
        python_executable, skip_confirmation, log_level
    )


def _verify_packaged_model(
    model, model_output_type, map_file, pre_transform_path, post_transform_path,
    labels_path, id_column, python_executable, skip_confirmation, log_level
):
    if map_file:
        UncaughtExceptionHandler.wrap(
            _verify_feature_map, map_file, pre_transform_path,
            post_transform_path, id_column, log_level
        )
    python_executable = python_executable or "python"
    script = os.path.join(os.path.dirname(__file__), "run_model_on_data.py")
    command = f"{python_executable} {script} --ot={model_output_type} --label={labels_path} --package_directory={model}"
    if not map_file:
        command = f"{command} --default_map=True"
    if pre_transform_path:
        command = f"{command} --pre={pre_transform_path}"
    if post_transform_path:
        command = f"{command} --post={post_transform_path}"
    if skip_confirmation:
        command = f"{command} --skip_confirmation={skip_confirmation}"
    if id_column:
        command = f"{command} --id_column={id_column}"
    if subprocess.run(["bash", "-c", command]).returncode != 0:
        sys.exit(1)

    click.echo("Done")


if __name__ == '__main__':
    verify()
