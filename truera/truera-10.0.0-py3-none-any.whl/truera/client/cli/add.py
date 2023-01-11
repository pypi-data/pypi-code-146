import json
import logging
import os
import sys
from typing import Any, Mapping, Optional, Tuple

import click

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.credential import credential
from truera.client.cli.data_source import data_source
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
from truera.client.client_environment import connection_string_message
from truera.client.client_utils import _STRING_TO_QOI
from truera.client.client_utils import validate_model_metadata
from truera.client.feature_client import FeatureClient
import truera.client.services.artifact_interaction_client as cl
from truera.client.util.data_split.data_split_path_container import \
    DataSplitPathContainer
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_UNKNOWN  # pylint: disable=no-name-in-module
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module
from truera.protobuf.public.util import split_mode_pb2 as sm_pb


@click.group(help="Commands for adding artifacts to truera.")
def add():
    pass


add.add_command(data_source)
add.add_command(credential)


@add.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=cli_utils.feature_is_hidden("neural_network")
)
@click.option(
    "--project_name",
    "-p",
    help="Friendly name for the project.",
    required=True
)
@click.option(
    "--score_type",
    default="logits",
    required=False,
    type=click.Choice(_STRING_TO_QOI.keys())
)
@click.option(
    "--input_data_format",
    default="tabular",
    required=False,
    type=click.Choice(["tabular", "time_series_tabular", "image"])
)
@click.option("--description_json", default=None, required=False, hidden=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def nn_project(
    project_name, *, score_type, input_data_format, description_json,
    connection_string, log_level
):

    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project = client.create_project(
            project_name,
            score_type,
            input_data_format=input_data_format,
            description_json=description_json
        )
        output_dict = {
            "project_name": project_name,
            "project_id": project.id,
            "score_type": score_type,
            "input_data_format": input_data_format
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--project_name",
    "-p",
    help="Friendly name for the project.",
    required=True
)
@click.option(
    "--score_type",
    default="logits",
    required=False,
    type=click.Choice(_STRING_TO_QOI.keys())
)
@click.option("--description_json", default=None, required=False, hidden=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def project(
    project_name, score_type, description_json, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project = client.create_project(
            project_name, score_type, description_json=description_json
        )
        output_dict = {
            "project_name": project_name,
            "project_id": project.id,
            "score_type": score_type
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--project_name",
    "-p",
    help="Name of the project to add the data_collection to.",
    required=True
)
@click.option(
    "--data_collection_name",
    "-d",
    help="Friendly name for the data_collection.",
    required=True
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def data_collection(
    project_name, *, data_collection_name, connection_string, log_level
):

    # TODO(AB#7226): Add parameter for specifying transform type

    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project = cl.Project(project_name, client, project_id=project_name)
        if not project.exists():
            logger.error("Provided project does not exist: " + project_name)
            sys.exit(1)

        data_collection = project.create_data_collection(
            data_collection_name, FEATURE_TRANSFORM_TYPE_UNKNOWN
        )

        data_collection.upload(client, project_name)
        output_dict = {
            "data_collection_name": data_collection_name,
            "project_id": project.id
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--project_name",
    "-p",
    help="Id of the project data_collection resides in.",
    required=True
)
@click.option(
    "--data_collection_name",
    "-d",
    help="Id of the data_collection to add a split to.",
    required=True
)
@click.option(
    "--split_name",
    "-s",
    help="Name of the split to be created in the data_collection.",
    required=True
)
@click.option(
    "--split_type",
    "-t",
    help="Split type: all, train, test, validate, oot, or custom",
    required=True
)
@click.option("--pre_transform_path", "--pre", default=None)
@click.option("--post_transform_path", "--post", default=None)
@click.option("--labels_path", "--label", default=None)
@click.option("--extra_data_path", "--extra", default=None)
@click.option(
    "--id_column",
    "--id",
    help="Name of id column in the split files.",
    required=cli_utils.feature_is_active("data_service_split_ingestion"),
    default=None
)
@click.option(
    "--do_not_use_data_service", is_flag=True, default=False, hidden=True
)
@click.option(
    "--split_time_range_begin",
    "--begin",
    default=None,
    help=
    "Begin time for the split in RFC 3339 format. Example of accepted format: 2020-01-01T10:00:20.021-05:00",
    hidden=cli_utils.feature_is_hidden("timestamps_on_splits")
)
@click.option(
    "--split_time_range_end",
    "--end",
    default=None,
    help=
    "End time for the split in RFC 3339 format. Example of accepted format: 2020-01-01T10:00:20.021-05:00",
    hidden=cli_utils.feature_is_hidden("timestamps_on_splits")
)
@click.option(
    "--timestamp_col",
    default=None,
    help=
    "If used, all columns of the data will be added to the pre_transform file and this column will be used as timestamp of each row. This column will be dropped from the data before it is given to the model."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def split(
    project_name, *, data_collection_name, connection_string, split_name,
    split_type, pre_transform_path, post_transform_path, labels_path,
    extra_data_path, log_level, id_column, do_not_use_data_service,
    split_time_range_begin, split_time_range_end, timestamp_col
):

    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)
    model_test_client = cli_utils.get_model_test_client(
        connection_string, logger
    )

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project = cl.Project(project_name, client, project_id=project_name)

        project_id = client.get_project_id(project_name)
        data_collection_id = client.get_data_collection_id(
            project_id, data_collection_name
        )

        data_collection = cl.DataCollection(
            data_collection_name, FEATURE_TRANSFORM_TYPE_UNKNOWN
        )
        cli_utils._validate_split_values(
            split_name, split_type, pre_transform_path, post_transform_path,
            labels_path, extra_data_path
        )

        output_dict = {
            "data_collection_name": data_collection_name,
            "project_id": project.id,
        }

        if do_not_use_data_service or not cli_utils.feature_is_active(
            "data_service_split_ingestion"
        ):
            data_collection.create_data_split(
                split_name,
                cli_utils._map_split_type(split_type),
                pre_transform_path=pre_transform_path,
                post_transform_path=post_transform_path,
                labels_path=labels_path,
                extra_data_path=extra_data_path,
                split_time_range_begin=split_time_range_begin,
                split_time_range_end=split_time_range_end,
                split_mode=sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED
            )
            split = {"split_name": split_name}

            files_uploaded = data_collection.upload_new_split(
                client, project_name
            )

            output_dict["files uploaded"] = str(files_uploaded)
            output_dict["split"] = split
        else:
            data_split_params = DataSplitPathContainer(
                pre_data=pre_transform_path,
                post_data=post_transform_path,
                extra_data=extra_data_path,
                label_data=labels_path
            )

            split = client.create_data_split_via_data_service(
                project_id,
                data_collection_id,
                split_name,
                split_type,
                data_split_params,
                id_column,
                timestamp_col=timestamp_col,
                split_time_range_begin=split_time_range_begin,
                split_time_range_end=split_time_range_end,
                split_mode=sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED
            )
            output_dict["split"] = split
        # TODO(AB #6997): (move call to auto create tests to the backend)
        if not cli_utils.feature_is_hidden(
            "create_model_tests_on_split_ingestion"
        ):
            split_metadata = client.get_split_metadata(
                project_name, data_collection_name, split_name
            )
            model_test_client.create_tests_from_split(
                project_id, split_metadata["id"]
            )
        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=cli_utils.feature_is_hidden("neural_network")
)
@click.option(
    "--project_name",
    "-p",
    help="Id of the project data_collection resides in.",
    required=True
)
@click.option(
    "--data_collection_name",
    "-d",
    help="Id of the data_collection to add a split to.",
    required=True
)
@click.option(
    "--split_name",
    "-s",
    help="Name of the split to be created in the data_collection.",
    required=True
)
@click.option(
    "--split_type",
    "-t",
    help="Split type: all, train, test, validate, oot, or custom",
    required=True
)
@click.option(
    "--split_dir",
    required=True,
    default=None,
    callback=cli_utils.validate_directory
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def split_nn(
    project_name, *, data_collection_name, connection_string, split_name,
    split_type, split_dir, log_level
):

    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project = cl.Project(project_name, client, project_id=project_name)
        client.get_project_id(project_name)
        client.get_data_collection_id(project_name, data_collection_name)

        data_collection = cl.DataCollection(
            data_collection_name, FEATURE_TRANSFORM_TYPE_UNKNOWN
        )
        data_collection.create_data_split(
            split_name,
            cli_utils._map_split_type(split_type),
            split_dir=split_dir,
            split_mode=sm_pb.SplitMode.SPLIT_MODE_NON_TABULAR
        )
        split = {"split_name": split_name}

        files_uploaded = data_collection.upload_new_split(client, project_name)

        output_dict = {
            "data_collection_name": data_collection_name,
            "project_id": project.id,
            "files uploaded": str(files_uploaded),
            "split": split
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--project_name",
    "-p",
    help="Id of the project data_collection resides in.",
    required=True
)
@click.option(
    "--data_collection_name",
    "-d",
    help="Id of the data_collection to add a split to.",
    required=True
)
@click.option(
    "--split_name",
    "-s",
    help="Name of the split to be created in the data_collection.",
    required=True
)
@click.option(
    "--split_type",
    "-t",
    help="Split type: all, train, test, validate, oot, or custom",
    required=True
)
@click.option("--predictions_path", "--predictions", required=True)
@click.option("--labels_path", "--label", default=None)
@click.option(
    "--id_column",
    "--id",
    help="Name of id column in the split files.",
    required=cli_utils.feature_is_active("data_service_split_ingestion"),
    default=None
)
@click.option(
    "--do_not_use_data_service", is_flag=True, default=False, hidden=True
)
@click.option(
    "--split_time_range_begin",
    "--begin",
    default=None,
    help=
    "Begin time for the split in RFC 3339 format. Example of accepted format: 2020-01-01T10:00:20.021-05:00",
    hidden=cli_utils.feature_is_hidden("timestamps_on_splits")
)
@click.option(
    "--split_time_range_end",
    "--end",
    default=None,
    help=
    "End time for the split in RFC 3339 format. Example of accepted format: 2020-01-01T10:00:20.021-05:00",
    hidden=cli_utils.feature_is_hidden("timestamps_on_splits")
)
@click.option(
    "--timestamp_col",
    default=None,
    help=
    "If used, all columns of the data will be added to the pre_transform file and this column will be used as timestamp of each row. This column will be dropped from the data before it is given to the model.",
    hidden=cli_utils.feature_is_hidden("data_service_split_ingestion")
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def monitoring_super_lite_split(
    project_name, *, data_collection_name, connection_string, split_name,
    split_type, predictions_path, labels_path, log_level, id_column,
    do_not_use_data_service, split_time_range_begin, split_time_range_end,
    timestamp_col
):

    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project = cl.Project(project_name, client, project_id=project_name)
        project_id = client.get_project_id(project_name)
        data_collection_id = client.get_data_collection_id(
            project_id, data_collection_name
        )

        data_collection = cl.DataCollection(
            data_collection_name, FEATURE_TRANSFORM_TYPE_UNKNOWN
        )

        cli_utils._validate_split_values(
            split_name,
            split_type,
            pre_transform_path=None,
            post_transform_path=None,
            labels_path=labels_path,
            extra_data_path=None
        )

        output_dict = {
            "data_collection_name": data_collection_name,
            "project_id": project.id,
        }

        if do_not_use_data_service or not cli_utils.feature_is_active(
            "data_service_split_ingestion"
        ):
            data_collection.create_data_split(
                split_name,
                cli_utils._map_split_type(split_type),
                labels_path=labels_path,
                split_time_range_begin=split_time_range_begin,
                split_time_range_end=split_time_range_end,
                split_mode=sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED
            )
            split = {"split_name": split_name}

            files_uploaded = data_collection.upload_new_split(
                client, project_name
            )

            output_dict["files uploaded"] = str(files_uploaded)
            output_dict["split"] = split
        else:
            data_split_params = DataSplitPathContainer(label_data=labels_path)

            split = client.create_data_split_via_data_service(
                project_id,
                data_collection_id,
                split_name,
                split_type,
                data_split_params,
                id_column,
                timestamp_col=timestamp_col,
                split_time_range_begin=split_time_range_begin,
                split_time_range_end=split_time_range_end,
                split_mode=sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED
            )
            output_dict["split"] = split

        model_metadata = client.get_model_metadata(project_name)

        prediction_cache(
            project_name=project_name,
            model_name=model_metadata["name"],
            data_collection_name=data_collection_name,
            split_name=split_name,
            path_to_prediction_cache=predictions_path,
            score_type=project.score_type,
            create_model=False,
            model_output_type=model_metadata["model_output_type"],
            client_name="cli_client",
            client_version="cli_client_version",
            connection_string=connection_string,
            log_level=log_level
        )

        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option("--model_name", "-m", required=True)
@click.option(
    "--model_type",
    "-t",
    help=
    "Type of the model to create, options are: Datarobot_v1, Datarobot_v2, H2O, MLeap, Pmml, Virtual, or PyFunc.",
    required=True
)
@click.option(
    "--model_output_type",
    "--ot",
    help="Type of output from the model.",
    required=False,
    default="default",
    type=click.Choice(["default", "classification", "regression"]),
    hidden=cli_utils.feature_is_hidden("model_specific_output_type")
)
@click.option(
    "--data_collection_name",
    "-d",
    default=None,
    help="Optional data_collection id to connect to the model when it is created."
)
@click.option(
    '--path_to_model',
    "--path",
    help='Path to the model to upload',
    required=False,
    default=""
)
@click.option(
    "--train_split_name",
    default=None,
    help="(Optional) Name of the train data split of the model.",
    required=False
)
@click.option(
    "--train_parameters",
    default=None,
    help="(Optional) Path to a json file containing model training parameters.",
    required=False
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def model(
    project_name, *, model_name, model_type, model_output_type, path_to_model,
    data_collection_name, train_split_name, train_parameters, connection_string,
    log_level
):

    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project = cl.Project(project_name, client, project_id=project_name)
        project_id = client.get_project_id(project_name)

        if data_collection_name:
            client.get_data_collection_id(project_id, data_collection_name)

        model_type = cli_utils._map_model_type(model_type)
        if not path_to_model and model_type != cli_utils.ModelType.Virtual:
            logger.error(
                f"path_to_model argument must be specified unless model_type is 'virtual'"
            )
            sys.exit(1)
        train_split_name, metadata_dict = _validate_and_load_model_metadata(
            client=client,
            logger=logger,
            project_name=project_name,
            data_collection_name=data_collection_name,
            train_split_name=train_split_name,
            train_parameters=train_parameters
        )

        model = project.create_model(
            model_name,
            model_type,
            model_output_type,
            path_to_model,
            data_collection_name=data_collection_name,
            train_split_name=train_split_name,
            train_parameters=metadata_dict
        )
        output_dict = {
            "model_name": model_name,
            "project_id": project_name,
            "model_type": model_type.name,
            "path_to_model": path_to_model,
            "data_collection_name": data_collection_name,
            "train_split_name": train_split_name,
            "train_parameters": metadata_dict
        }
        model.upload(client)
        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option("--model_name", "-m", required=True)
@click.option(
    "--train_split_name",
    default=None,
    help="(Optional) Name of the train data split of the model.",
    required=False
)
@click.option(
    "--train_parameters",
    default=None,
    help="(Optional) Path to a json file containing model training parameters.",
    required=False
)
@click.option(
    "--data_collection_name",
    "-d",
    default=None,
    help="(Optional) Name of the data collection of the model.",
    required=False
)
@click.option(
    "--overwrite",
    help="Overwrite existing values (if exist).",
    is_flag=True,
    show_default=True
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def model_metadata(
    project_name, *, model_name, train_split_name, train_parameters,
    data_collection_name, overwrite, connection_string, log_level
):

    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)
    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        if data_collection_name:
            if client.set_data_collection_for_model(
                project_name, model_name, data_collection_name, overwrite
            ):
                logger.info(
                    f"Set data_collection \"{data_collection_name}\" to model \"{model_name}\""
                )
            else:
                click.echo(
                    "The specified model (" + model_name +
                    ") already has a data_collection specified. Please specify a different model or use --overwrite."
                )
                sys.exit(1)
        current_model_metadata = client.get_model_metadata(
            project_name, model_name
        )
        data_collection_name = client.get_data_collection_name(
            project_id, current_model_metadata["data_collection_id"]
        )
        train_split_name, metadata_dict = _validate_and_load_model_metadata(
            client=client,
            logger=logger,
            project_name=project_name,
            data_collection_name=data_collection_name,
            train_split_name=train_split_name,
            train_parameters=train_parameters
        )

        client.add_train_split_to_model(
            project_name=project_name,
            model_name=model_name,
            train_split_name=train_split_name,
            overwrite=overwrite
        )
        client.add_train_parameters_to_model(
            project_name=project_name,
            model_name=model_name,
            train_parameters=metadata_dict,
            overwrite=overwrite
        )
        output_dict = {
            "model_name": model_name,
            "project_id": project_name,
            "data_collection_name": data_collection_name,
            "train_split_name": train_split_name,
            "train_parameters": metadata_dict
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


def _validate_and_load_model_metadata(
    client: cl.ArtifactInteractionClient,
    logger: logging.Logger,
    project_name: str,
    data_collection_name: Optional[str] = None,
    train_split_name: Optional[str] = None,
    train_parameters: Optional[str] = None
) -> Tuple[str, Mapping[str, str]]:
    existing_split_names = None
    if train_split_name:
        if not data_collection_name:
            logger.error(
                f"`data_collection_name` must be provided to be able to specify `train_split_name`."
            )
            sys.exit(1)
        existing_split_names = client.get_all_datasplits_in_data_collection(
            project_name, data_collection_name
        )

    metadata_dict = None
    if train_parameters:
        if not os.path.exists(train_parameters):
            logger.error(f"Could not find file {train_parameters}.")
            sys.exit(1)

        metadata_dict = json.load(open(train_parameters, 'r'))

    validate_model_metadata(
        train_split_name=train_split_name,
        existing_split_names=existing_split_names,
        train_parameters=metadata_dict,
        logger=logger
    )
    return train_split_name, metadata_dict


@add.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option("--data_collection_name", "-d", required=True)
@click.option(
    "--feature_description_file",
    "--file",
    required=True,
    callback=cli_utils.validate_file,
    help="File containing a all of the data for a data_collection's features."
)
@click.option("--force", "-f", is_flag=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def feature_list(
    project_name, *, data_collection_name, feature_description_file, force,
    connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project = cl.Project(project_name, client, project_id=project_name)
        project_id = client.get_project_id(project_name)
        client.get_data_collection_id(project_id, data_collection_name)

        feature_client = FeatureClient(ar_client, logger)
        feature_list_id = feature_client.upload_feature_list_metadata(
            feature_description_file, project_name, data_collection_name, force
        )
        output_dict = {
            "id": feature_list_id,
            "project_name": project_name,
            "data_collection_name": data_collection_name
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--project_name",
    "-p",
    help=
    "Id of the project the data source resides in, and split should be created in.",
    required=True
)
@click.option(
    "--data_source_name",
    "--dsn",
    help="Name of the data source to create a split from."
)
@click.option("--table_id", help="Table id to create a split from.")
@click.option(
    "--data_collection_name",
    "-d",
    help="Name of the data_collection to add a split to.",
    required=True
)
@click.option(
    "--split_name",
    "-s",
    help="Name of the split to be created in the data_collection.",
    required=True
)
@click.option(
    "--split_type",
    "-t",
    type=click.Choice(
        ['all', 'train', 'test', 'validate', 'oot', 'custom'],
        case_sensitive=False
    ),
    help="Split type: all, train, test, validate, oot, or custom",
    required=True
)
@click.option(
    "--approx_row_count",
    "--count",
    help="Approximate number of rows to ingest.",
    default=5000
)
@click.option(
    "--seed",
    help="Optional seed to use in random sampling.",
    default=None,
    type=int
)
@click.option(
    "--sample_kind",
    help="Provides the strategy to use while sub-sampling the rows.",
    type=click.Choice(['random', 'first'], case_sensitive=False),
    default='random'
)
@click.option(
    "--label_col",
    "--label",
    default=None,
    help=
    "If used, all other columns of the data will be added to the pre_transform file and this column will be added to the labels file."
)
@click.option(
    "--id_col",
    default=None,
    help=
    "If used, all columns of the data will be added to the pre_transform file and this column will be used as the id. This column will be dropped from the data before it is given to the model."
)
@click.option(
    "--timestamp_col",
    default=None,
    help=
    "If used, all columns of the data will be added to the pre_transform file and this column will be used as timestamp of each row. This column will be dropped from the data before it is given to the model."
)
@click.option(
    "--prediction_col",
    "--prediction",
    default=None,
    help=
    "If used, all other columns of the data will be added to the pre_transform file and this column will be treated as the model's predictions.",
    hidden=cli_utils.feature_is_hidden("monitoring_lite")
)
@click.option(
    "--column_spec_file",
    "--col_file",
    default=None,
    callback=cli_utils.validate_file,
    help=
    "File containing list of columns for each split file: pre_transform, post_transform, labels, extra_data, predictions."
)
@click.option(
    "--split_time_range_begin",
    "--begin",
    default=None,
    help=
    "Begin time for the split in RFC 3339 format. Example of accepted format: 2020-01-01T10:00:20.021-05:00",
    hidden=cli_utils.feature_is_hidden("timestamps_on_splits")
)
@click.option(
    "--split_time_range_end",
    "--end",
    default=None,
    help=
    "End time for the split in RFC 3339 format. Example of accepted format: 2020-01-01T10:00:20.021-05:00",
    hidden=cli_utils.feature_is_hidden("timestamps_on_splits")
)
@click.option(
    "--model_name",
    default=None,
    help=
    "Name of model associated with the provided predictions. If prediction_col not provided, model_name will be ignored",
    hidden=cli_utils.feature_is_hidden("monitoring_lite")
)
@click.option(
    "--score_type",
    default=None,
    help=
    "Score type associated with the provided predictions. This will default to project score type. If prediction_col not provided, score_type will be ignored.",
    type=click.Choice(_STRING_TO_QOI.keys()),
    hidden=cli_utils.feature_is_hidden("monitoring_lite")
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def split_from_table(
    project_name, *, data_source_name, table_id, data_collection_name,
    split_name, split_type, approx_row_count, seed, sample_kind, label_col,
    id_col, prediction_col, column_spec_file, split_time_range_begin,
    split_time_range_end, model_name, score_type, connection_string, log_level,
    timestamp_col
):

    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        data_collection_id = client.get_data_collection_id(
            project_id, data_collection_name
        )
        rowset_identifier = cl.RowsetIdentifierInfo(
            table_id, data_source_name, project_id
        )
        output_split_info = cl.OutputSplitInfo(
            project_id, data_collection_id, split_name, split_type,
            split_time_range_begin, split_time_range_end
        )
        model_info_for_cache = cl.ModelInfoForCache(
            project_id, model_name, score_type
        )
        create_split_col_info = cl.CreateDataSplitColumnSpec(
            label_col, id_col, prediction_col, [], column_spec_file, False,
            timestamp_col
        )
        output_spec = cl.OutputSpec(approx_row_count, sample_kind, seed)
        operation_id = client.create_data_split_from_data_source(
            rowset_identifier,
            output_split_info,
            model_info_for_cache,
            create_split_col_info,
            output_spec,
            split_mode=sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED
        )

        output_dict = {"operation_id": operation_id}

        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--project_name",
    "-p",
    help=
    "Id of the project the data source resides in, and split should be created in.",
    required=True
)
@click.option(
    "--table_id",
    "--rs",
    help=
    "Id of the table which should have a filter applied. Either this or data source name is required."
)
@click.option(
    "--data_source_name",
    "--dsn",
    help=
    "Name of the data source to add a filter to. Either this or table id is required."
)
@click.option(
    "--filter",
    required=True,
    help=
    "SQL filter expression to be applied to the input. If it contains spaces then it should be surrounded by quotes. example: 'a<5' or 'NOT b == 8.0'."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def filter_to_table(
    project_name, *, table_id, data_source_name, filter, connection_string,
    log_level
):

    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        input_table_id, output_table_id = client.add_filter_to_rowset(
            project_id, table_id, data_source_name, filter
        )

        output_dict = {
            "input_table_id": input_table_id,
            "output_table_id": output_table_id,
            "filter": filter
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=cli_utils.feature_is_hidden("external_caches")
)
@click.option("--project_name", "-p", required=True)
@click.option("--model_name", "-m", required=True)
@click.option("--data_collection_name", "-d", required=True)
@click.option("--split_name", "-s", required=True, help="data_split id")
@click.option(
    "--path_to_prediction_cache",
    "--path",
    help="Path to the model predictions to upload",
    callback=cli_utils.validate_file,
    required=True
)
@click.option(
    "--score_type",
    default="logits",
    required=False,
    type=click.Choice(_STRING_TO_QOI.keys())
)
@click.option("--create_model", required=False, is_flag=True)
@click.option(
    "--model_output_type",
    "--ot",
    help="Type of output from the model.",
    required=False,
    default="default",
    type=click.Choice(["default", "classification", "regression"])
)
@click.option("--client_name", required=True)
@click.option("--client_version", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def prediction_cache(
    project_name, *, model_name, data_collection_name, split_name,
    path_to_prediction_cache, score_type, create_model, model_output_type,
    client_name, client_version, connection_string, log_level
):

    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project = cl.Project(project_name, client, project_id=project_name)
        project_id = client.get_project_id(project_name)

        project_score_type = client.get_project_metadata(project_name)[
            "settings"]["score_type"]
        if project_score_type != score_type:
            logger.warning(
                f"Provided cache score type {score_type} does not match project score type: {project_score_type} and will not be used"
            )

        if data_collection_name:
            client.get_data_collection_id(project_id, data_collection_name)

        if split_name not in client.get_all_datasplits_in_data_collection(
            project_name, data_collection_name
        ):
            logger.error(
                f"Provided split does not exist on project's data collection. Project id: \
                {project_name} Data_Collection id: {data_collection_name} Split id: {split_name}"
            )
            sys.exit(1)

        pred_cache = project.create_prediction_cache(
            model_name, data_collection_name, split_name,
            path_to_prediction_cache, score_type, model_output_type,
            client_name, client_version
        )

        pred_cache.upload(client, create_model=create_model)
        output_dict = {
            "project_id": project_name,
            "model_name": model_name,
            "path_to_prediction_cache": path_to_prediction_cache,
            "data_collection_name": data_collection_name,
            "split_name": split_name,
            "score_type": score_type,
            "format": pred_cache.format,
            "cache_id": pred_cache.cache_id,
            "virtual_model_id": pred_cache.model_id
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=cli_utils.feature_is_hidden("external_caches")
)
@click.option("--project_name", "-p", required=True)
@click.option("--model_name", "-m", required=True)
@click.option("--data_collection_name", "-d", required=True)
@click.option("--split_name", "-s", required=True, help="data_split id")
@click.option(
    "--path_to_explanation_cache",
    "--path",
    help="Path to the explanations to upload",
    callback=cli_utils.validate_file,
    required=True
)
@click.option(
    "--score_type",
    default="logits",
    required=False,
    type=click.Choice(_STRING_TO_QOI.keys())
)
@click.option("--create_model", required=False, is_flag=True)
@click.option(
    "--model_output_type",
    "--ot",
    help="Type of output from the model.",
    required=False,
    default="default",
    type=click.Choice(["default", "classification", "regression"])
)
@click.option("--client_name", required=True)
@click.option("--client_version", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def explanation_cache(
    project_name, *, model_name, data_collection_name, split_name,
    path_to_explanation_cache, score_type, create_model, model_output_type,
    client_name, client_version, connection_string, log_level
):

    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)
    cs_client = cli_utils.get_config_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project = cl.Project(project_name, client, project_id=project_name)
        project_id = client.get_project_id(project_name)

        if cs_client.get_influence_algorithm_type(project_id) != "truera-qii":
            logger.error(
                f"Adding feature influences or explanation caches is only supported for projects with influence algorithm \"truera-qii!\""
            )
            sys.exit(1)

        project_score_type = client.get_project_metadata(project_name)[
            "settings"]["score_type"]
        if project_score_type != score_type:
            logger.warning(
                f"Provided cache score type {score_type} does not match project score type: {project_score_type} and will not be used"
            )

        if data_collection_name:
            client.get_data_collection_id(project_id, data_collection_name)

        if split_name not in client.get_all_datasplits_in_data_collection(
            project_name, data_collection_name
        ):
            logger.error(
                f"Provided split does not exist on project's data collection. Project id: \
                {project_name} Data_Collection id: {data_collection_name} Split id: {split_name}"
            )
            sys.exit(1)

        explanation_cache = project.create_explanation_cache(
            model_name,
            data_collection_name,
            split_name,
            cache_location=path_to_explanation_cache,
            score_type=score_type,
            model_output_type=model_output_type,
            explanation_algorithm_type=ExplanationAlgorithmType.TRUERA_QII,
            client_name=client_name,
            client_version=client_version
        )

        explanation_cache.upload(client, create_model=create_model)
        output_dict = {
            "project_id": project_name,
            "model_name": model_name,
            "path_to_explanation_cache": path_to_explanation_cache,
            "data_collection_name": data_collection_name,
            "split_name": split_name,
            "score_type": score_type,
            "format": explanation_cache.format,
            "cache_id": explanation_cache.cache_id,
            "virtual_model_id": explanation_cache.model_id
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(
    help="Manually trigger a backup.",
    hidden=cli_utils.feature_is_hidden("admin")
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def manual_backup(connection_string, log_level):

    logger = cli_logger.create_cli_logger(log_level)
    backup_client = cli_utils.get_backup_client(connection_string, logger)
    response = backup_client.trigger_backup()
    output_dict = {"path": response.backup.backup_folder_path}
    click.echo(cli_utils._format_and_return_json(output_dict))


@add.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=cli_utils.feature_is_hidden("delayed_label")
)
@click.option(
    "--project_name",
    "-p",
    help="Name of the project the split exists in.",
    required=True
)
@click.option(
    "--data_collection_name",
    "-d",
    help="Name of the data_collection the split exists in.",
    required=True
)
@click.option("--table_id", "--rs", help="Table id to fetch labels from.")
@click.option(
    "--data_source_name",
    "--dsn",
    help="Name of the data source to fetch label data from."
)
@click.option(
    "--split_name",
    "-s",
    help="Name of the existing split the labels should be uploaded to.",
    required=True
)
@click.option(
    "--approx_row_count",
    "--count",
    help="Approximate number of rows to ingest.",
    default=5000
)
@click.option(
    "--seed",
    help="Optional seed to use in random sampling.",
    default=None,
    type=int
)
@click.option(
    "--sample_kind",
    help="Provides the strategy to use while sub-sampling the rows.",
    type=click.Choice(['random', 'first'], case_sensitive=False),
    default='random'
)
@click.option(
    "--label_column",
    "--label",
    help="Name of the label column in data source.",
    required=True
)
@click.option(
    "--id_column",
    "--id",
    help="Name of id column in the data source.",
    required=True
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def labels(
    project_name, *, data_collection_name, table_id, data_source_name,
    split_name, approx_row_count, seed, sample_kind, label_column, id_column,
    connection_string, log_level
):
    _ingest_delayed(
        project_name=project_name,
        data_collection_name=data_collection_name,
        table_id=table_id,
        data_source_name=data_source_name,
        split_name=split_name,
        approx_row_count=approx_row_count,
        seed=seed,
        sample_kind=sample_kind,
        label_column=label_column,
        extra_columns=None,
        id_column=id_column,
        connection_string=connection_string,
        log_level=log_level
    )


@add.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=cli_utils.feature_is_hidden("delayed_extra_data")
)
@click.option(
    "--project_name",
    "-p",
    help="Name of the project the split exists in.",
    required=True
)
@click.option(
    "--data_collection_name",
    "-d",
    help="Name of the data_collection the split exists in.",
    required=True
)
@click.option("--table_id", "-t", help="Table id to fetch extra_data from.")
@click.option(
    "--data_source_name",
    "--dsn",
    help="Name of the data source to fetch label data from."
)
@click.option(
    "--split_name",
    "-s",
    help="Name of the existing split the labels should be uploaded to.",
    required=True
)
@click.option(
    "--approx_row_count",
    "--count",
    help="Approximate number of rows to ingest.",
    default=5000
)
@click.option(
    "--seed",
    help="Optional seed to use in random sampling.",
    default=None,
    type=int
)
@click.option(
    "--sample_kind",
    help="Provides the strategy to use while sub-sampling the rows.",
    type=click.Choice(['random', 'first'], case_sensitive=False),
    default='random'
)
@click.option(
    "--extra_data_column",
    "--extra_data",
    help="Name of the label column in data source.",
    required=True
)
@click.option(
    "--id_column",
    "--id",
    help="Name of id column in the data source.",
    required=True
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@UncaughtExceptionHandler.decorate
def extra_data(
    project_name, *, data_collection_name, table_id, data_source_name,
    split_name, approx_row_count, seed, sample_kind, extra_data_column,
    id_column, connection_string, log_level
):
    _ingest_delayed(
        project_name=project_name,
        data_collection_name=data_collection_name,
        table_id=table_id,
        data_source_name=data_source_name,
        split_name=split_name,
        approx_row_count=approx_row_count,
        seed=seed,
        sample_kind=sample_kind,
        label_column=None,
        extra_columns=[extra_data_column],
        id_column=id_column,
        connection_string=connection_string,
        log_level=log_level
    )


def _ingest_delayed(
    project_name, *, data_collection_name, table_id, data_source_name,
    split_name, approx_row_count, seed, sample_kind, label_column,
    extra_columns, id_column, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)
    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        operation_id = client.ingest_delayed(
            project_name=project_name,
            data_source_name=data_source_name,
            rowset_id=table_id,
            data_collection_name=data_collection_name,
            existing_split_name=split_name,
            pre_columns=None,
            post_columns=None,
            label_column=label_column,
            prediction_column=None,
            feature_influence_columns=None,
            extra_columns=extra_columns,
            id_column=id_column,
            model_info_for_cache=None,
            approx_row_count=approx_row_count,
            seed=seed,
            sample_strategy=sample_kind
        )

        output_dict = {"operation_id": operation_id}
        click.echo(cli_utils._format_and_return_json(output_dict))


if __name__ == '__main__':
    add()
