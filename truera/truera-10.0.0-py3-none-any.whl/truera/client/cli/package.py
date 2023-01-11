import os
import shutil
import sys
import uuid

import click

from truera.client.cli.add import add
import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
from truera.client.cli.cli_utils import validate_directory
from truera.client.cli.cli_utils import validate_file
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
import truera.client.model_preprocessing as model_processing


@click.group(help="Commands for packaging models before upload.")
def package():
    pass


@package.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--model_path",
    help=
    "Path to pickle file, zip, other serialized format, or directory representing of the model object to package.",
    required=True
)
@click.option(
    "--output_dir",
    "--dir",
    help="Path to output directory after processing.",
    required=True
)
@click.option(
    "--dependencies",
    "--dep",
    help=
    "Comma separated list of the conda dependencies of the model, sklearn version / tf version / pytorch version must be included in this. Example: ',blas=1.0,glib=2.66.1'.",
    default=None
)
@click.option(
    "--pip_dependencies",
    "--pip_dep",
    help=
    "Comma separated list of the pip dependencies of the model. Example: 'cloudpickle==1.2.1,xgboost==0.90'.",
    default=None
)
@click.option(
    "--pip_requirements_file",
    help=
    "Requirements file documenting your pip dependencies. This option assumes all dependencies can be installed via pip. It is recommended that you only include the minimal set of dependencies and allow platform specific transitive dependencies to be resolved in truera.",
    default=None
)
@click.option(
    "--python_version",
    help=
    "Verision of python that should be used along with pip requirements file. Ignored otherwise. The format can be of the form 'python=x.x.x' or 'x.x.x'.",
    default="3.7.3"
)
@click.option(
    "--conda_file",
    "--conda",
    help=
    "Alternative to specifying dependencies / pip dependencies. The specified file will be coppied in as conda.yaml.",
    default=None
)
@click.option(
    "--framework_wrapper",
    "-w",
    help=
    "File that wraps the framework. Built in options are: {}, or you can specify your own file."
    .format(model_processing.BUILT_IN_FRAMEWORK_WRAPPER_LIST),
    required=True
)
@click.option(
    "--model_output_type",
    "--ot",
    help="Type of output from the model.",
    required=False,
    default="classification",
    type=click.Choice(["classification", "regression"])
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def python_model(
    model_path, output_dir, framework_wrapper, model_output_type, conda_file,
    dependencies, pip_dependencies, pip_requirements_file, python_version,
    log_level
):
    UncaughtExceptionHandler.wrap(
        package_python_model, model_path, output_dir, framework_wrapper,
        model_output_type, conda_file, dependencies, pip_dependencies,
        pip_requirements_file, python_version, log_level
    )


def package_python_model(
    model_path, output_dir, framework_wrapper, model_output_type, conda_file,
    dependencies, pip_dependencies, pip_requirements_file, python_version,
    log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    pip_dependencies = model_processing.PipDependencyParser.parse_from_string(
        pip_dependencies
    )
    model_processing.prepare_python_model_folder(
        model_file_path=model_path,
        output_dir=output_dir,
        framework_wrapper=framework_wrapper,
        model_output_type=model_output_type,
        conda_file=conda_file,
        dependencies=dependencies,
        pip_dependencies=pip_dependencies,
        pip_requirements_file=pip_requirements_file,
        python_version=python_version,
        logger=logger
    )
    model_processing.verify_python_model_folder(
        output_dir, logger=logger, silent=True
    )
    click.echo("Done")


@package.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--jar_path",
    "--jar",
    help="Path to H2O model generation JAR.",
    required=True
)
@click.option(
    "--model_zip_path",
    "--zip",
    help="Path to the ZIP of MOJO model.",
    required=True
)
@click.option(
    "--output_dir",
    "--dir",
    help="Path to packaged model directory.",
    required=True
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def h2o_model(jar_path, model_zip_path, output_dir, log_level):
    UncaughtExceptionHandler.wrap(
        package_h2o_model, jar_path, model_zip_path, output_dir, log_level
    )


def package_h2o_model(jar_path, model_zip_path, output_dir, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    model_processing.prepare_h2o_model(
        jar_path, model_zip_path, output_dir, logger
    )
    model_processing.verify_h2o_model_folder(output_dir, logger, silent=True)
    click.echo("Done")


@package.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--jar_path",
    "--jar",
    help="Path to jar containing the model.",
    required=True
)
@click.option(
    "--model_package_id",
    "-m",
    help=
    "Model id from the package. For example, if the model class name is com.datarobot.prediction.ABC123.DRModel, then this value should be ABC123.",
    required=True
)
@click.option(
    "--api_version",
    help=
    "Major version of DataRobot Prediction API used in the provided model jar. Accepted versions are either `2` (latest) or `1`.",
    required=True,
    type=int
)
@click.option(
    "--output_dir",
    "--dir",
    help="Path to output directory after processing.",
    required=True
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def datarobot_model(
    jar_path: str, model_package_id: str, output_dir: str, api_version: int,
    log_level
):
    UncaughtExceptionHandler.wrap(
        package_datarobot_model, jar_path, model_package_id, output_dir,
        api_version, log_level
    )


def package_datarobot_model(
    jar_path: str, model_package_id: str, output_dir: str, api_version: int,
    log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    model_processing.prepare_data_robot_model(
        jar_path, model_package_id, output_dir, api_version, logger
    )
    model_processing.verify_datarobot_model_folder(
        output_dir, logger, silent=True
    )
    click.echo("Done")


@package.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--pmml_file",
    "--pmml",
    help="Path to the pmml file to package.",
    callback=validate_file,
    required=True
)
@click.option("--output_field", help="Output field representing prediction.")
@click.option(
    "--evaluator_jar_path",
    "--eval_jar",
    help=
    "Path to jar containing desired pmml evaluator. Truera does not distribute this jar, so the correct version for the model should be provided here. This can be downloaded from public maven repositories: org.jpmml:pmml-evaluator.",
    callback=validate_file,
    required=True
)
@click.option(
    "--model_jar_path",
    "--model_jar",
    help=
    "Path to the desired model jar. Truera does not distribute this jar, so the correct version for the model should be provided here. This can be downloaded from public maven repositories: org.jpmml:pmml-model.",
    callback=validate_file,
    required=True
)
@click.option(
    "--output_dir",
    "--dir",
    help="Path to output directory after processing.",
    required=True
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def pmml_model(
    pmml_file, output_field, evaluator_jar_path, model_jar_path, output_dir,
    log_level
):
    UncaughtExceptionHandler.wrap(
        _package_pmml_model, pmml_file, output_field, evaluator_jar_path,
        model_jar_path, output_dir, log_level
    )


def _package_pmml_model(
    pmml_file, output_field, evaluator_jar_path, model_jar_path, output_dir,
    log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    model_processing.prepare_pmml_model(
        pmml_file, output_field, evaluator_jar_path, model_jar_path, output_dir,
        logger
    )
    model_processing.verify_pmml_model_folder(output_dir, logger, silent=True)
    click.echo("Done")


@package.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--zip_file",
    "--zip",
    help="Path to a zip of the mleap model.",
    callback=validate_file
)
@click.option(
    "--mleap_folder",
    "--folder",
    help="Path to folder of the mleap model.",
    callback=validate_directory
)
@click.option("--version", help="Version of mleap.", required=True)
@click.option(
    "--output_dir",
    "--dir",
    help="Path to output directory after processing.",
    required=True
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def mleap_model(zip_file, mleap_folder, version, output_dir, log_level):
    UncaughtExceptionHandler.wrap(
        _package_mleap_model, zip_file, mleap_folder, version, output_dir,
        log_level
    )


def _package_mleap_model(
    zip_file, mleap_folder, version, output_dir, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    model_processing.prepare_mleap_model(
        zip_file, mleap_folder, version, output_dir, logger
    )
    model_processing.verify_mleap_model_folder(output_dir, logger, silent=True)
    click.echo("Done")


if __name__ == '__main__':
    package()
