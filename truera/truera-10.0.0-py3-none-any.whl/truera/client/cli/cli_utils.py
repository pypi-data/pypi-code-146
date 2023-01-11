from enum import Enum
import json
import os
import sys
from typing import List, Optional, Union

import click

from truera.client import data_source_utils
from truera.client import truera_workspace_utils
import truera.client.client_environment as env
from truera.client.client_utils import InvalidInputDataFormat
from truera.client.client_utils import NotSupportedFileTypeException
from truera.client.client_utils import TextExtractorParams
from truera.client.public.auth_details import AuthDetails
from truera.client.public.auth_details import AuthDetailsMode
from truera.protobuf.public.common.schema_pb2 import \
    ColumnDetails  # pylint: disable=no-name-in-module
from truera.protobuf.public.util.data_type_pb2 import \
    StaticDataTypeEnum  # pylint: disable=no-name-in-module


class SplitType(Enum):
    All = 0
    Train = 1
    Test = 2
    Validate = 3
    OOT = 4
    Prod = 5
    Custom = 9


class ModelType(Enum):
    SkLearn = 0  # deprecated in favor of pyfunc
    H2O = 1
    Datarobot_v1 = 2
    PyFunc = 3
    Virtual = 4
    Pmml = 5
    MLeap = 6
    Datarobot_v2 = 7


def _map_split_type(split_type: str):
    if split_type.lower() == "all":
        return SplitType.All
    if split_type.lower() == "train":
        return SplitType.Train
    if split_type.lower() == "test":
        return SplitType.Test
    if split_type.lower() == "validate":
        return SplitType.Validate
    if split_type.lower() == "oot":
        return SplitType.OOT
    if split_type.lower() == "prod":
        return SplitType.Prod
    if split_type.lower() == "custom":
        return SplitType.Custom
    click.echo(
        "Provided split type was invalid: " + split_type +
        ". Valid types are all, train, test, validate, oot, prod, and custom."
    )
    sys.exit(1)


def _map_model_type(model_type: str):
    mp = {
        "pyfunc": ModelType.PyFunc,
        "h2o": ModelType.H2O,
        "datarobot_v1": ModelType.Datarobot_v1,
        "pmml": ModelType.Pmml,
        "mleap": ModelType.MLeap,
        "virtual": ModelType.Virtual,
        "datarobot_v2": ModelType.Datarobot_v2
    }
    key = model_type.lower()
    if key in mp:
        return mp[key]
    click.echo(
        f"Provided model type was invalid: {model_type}. Valid types are {mp.keys()}."
    )
    sys.exit(1)


def _try_load_split_json(input_split: str):
    try:
        return json.loads(input_split)
    except ValueError:
        click.echo("Split json was not valid:")
        click.echo(input_split)
        sys.exit(1)


def _format_and_return_json(obj):
    return json.dumps(obj, indent=4, sort_keys=True)


def _validate_split_values(
    split_name, split_type, pre_transform_path, post_transform_path,
    labels_path, extra_data_path
):
    # Exits if split type is not valid.
    _map_split_type(split_type)

    if split_name == None:
        click.echo("Provided split name cannot be null.")
        sys.exit(1)

    # Check the user's paths.
    _verify_path_exists(pre_transform_path, "pre transform path")
    _verify_path_exists(post_transform_path, "post transform path")
    _verify_path_exists(labels_path, "labels path")
    _verify_path_exists(extra_data_path, "extra data path")


def _verify_path_exists(path: str, name_for_error: str):
    if path is not None:
        if not os.path.isfile(path):
            click.echo("Path does not refer to a file: " + path)
            sys.exit(1)


def _get_connection_string_unvalidated(connection_string: str) -> Optional[str]:
    if connection_string:
        return connection_string

    env_value = env.LocalContextStorage.get_cli_env_context().connection_string
    if env_value:
        return env_value

    return None


def _get_connection_string(connection_string: str) -> Optional[str]:
    connection_string = _get_connection_string_unvalidated(connection_string)
    if connection_string:
        truera_workspace_utils.validate_remote_url(connection_string)
    return connection_string


def _get_use_http():
    env_value = env.LocalContextStorage.get_cli_env_context().use_http
    if env_value:
        return env_value

    return False


def _get_verify_cert():
    return env.LocalContextStorage.get_cli_env_context().verify_cert


def _get_auth_details():
    env_ctx = env.LocalContextStorage.get_cli_env_context()
    if env_ctx.username and env_ctx.password:
        return AuthDetails(
            mode=AuthDetailsMode.BASIC_AUTH,
            username=env_ctx.username,
            password=env_ctx.password
        )
    if env_ctx.token:
        return AuthDetails(mode=AuthDetailsMode.TOKEN_AUTH, token=env_ctx.token)
    # TODO: Implement client-side service account auth in CLI

    raise click.UsageError(
        "Please use \"save credentials\" to set up credentials to access Truera endpoint. See tru save credentials --help for more details"
    )


def get_backup_client(
    connection_string, logger, verify_cert: Union[bool, str] = None
):
    from truera.client.services.backup_service_client import \
        BackupServiceClient

    connection_string = _get_connection_string(connection_string)
    if connection_string is None:
        raise click.UsageError(
            "No connection string provided, Please pass or save connection string!"
        )
    use_http = _get_use_http()
    auth_details = _get_auth_details()
    if verify_cert is None:
        verify_cert = _get_verify_cert()
    client = BackupServiceClient.create(
        connection_string=connection_string,
        logger=logger,
        auth_details=auth_details,
        use_http=use_http,
        verify_cert=verify_cert
    )
    return client


def get_billing_client(
    connection_string, logger, verify_cert: Union[bool, str] = None
):
    from truera.client.services.billing_service_client import \
        BillingServiceClient

    connection_string = _get_connection_string(connection_string)
    if connection_string is None:
        raise click.UsageError(
            "No connection string provided, Please pass or save connection string!"
        )
    use_http = _get_use_http()
    auth_details = _get_auth_details()
    if verify_cert is None:
        verify_cert = _get_verify_cert()
    client = BillingServiceClient.create(
        connection_string=connection_string,
        logger=logger,
        auth_details=auth_details,
        use_http=use_http,
        verify_cert=verify_cert
    )
    return client


def get_artifact_repo_client(
    connection_string,
    logger,
    ignore_version_mismatch=False,
    *,
    verify_cert: Union[bool, str] = None
):
    from truera.client.services.artifact_repo_client_factory import \
        get_ar_client

    connection_string = _get_connection_string(
        connection_string
    ) or ReasonableDefaults.artifact_repo_connection_string
    use_http = _get_use_http()
    auth_details = _get_auth_details()
    if verify_cert is None:
        verify_cert = _get_verify_cert()
    return get_ar_client(
        connection_string,
        auth_details,
        logger,
        use_http,
        ignore_version_mismatch=ignore_version_mismatch,
        verify_cert=verify_cert
    )


def get_data_service_client(
    connection_string, logger, verify_cert: Union[bool, str] = None
):
    from truera.client.services.data_service_client import DataServiceClient

    connection_string = _get_connection_string(
        connection_string
    ) or ReasonableDefaults.data_service_connection_string
    if verify_cert is None:
        verify_cert = _get_verify_cert()
    return DataServiceClient.create(
        connection_string=connection_string,
        logger=logger,
        auth_details=_get_auth_details(),
        use_http=_get_use_http(),
        verify_cert=verify_cert
    )


def get_scheduled_ingestion_client(
    connection_string, logger, verify_cert: Union[bool, str] = None
):
    from truera.client.services.scheduled_ingestion_client import \
        ScheduledIngestionClient
    connection_string = _get_connection_string(
        connection_string
    ) or ReasonableDefaults.data_service_connection_string
    if verify_cert is None:
        verify_cert = _get_verify_cert()
    return ScheduledIngestionClient.create(
        connection_string=connection_string,
        data_service_client=get_data_service_client(
            connection_string, logger, verify_cert
        ),
        logger=logger,
        auth_details=_get_auth_details(),
        use_http=_get_use_http(),
        verify_cert=verify_cert
    )


def get_rbac_service_client(
    connection_string, logger, verify_cert: Union[bool, str] = None
):
    from truera.client.services.rbac_service_client import RbacServiceClient

    connection_string = _get_connection_string(connection_string)
    if verify_cert is None:
        verify_cert = _get_verify_cert()
    return RbacServiceClient.create(
        connection_string=connection_string,
        logger=logger,
        auth_details=_get_auth_details(),
        use_http=_get_use_http(),
        verify_cert=verify_cert
    )


def get_user_manager_service_client(
    connection_string, logger, verify_cert: Union[bool, str] = None
):
    from truera.client.services.user_manager_service_client import \
        UserManagerServiceClient

    connection_string = _get_connection_string(connection_string)
    if verify_cert is None:
        verify_cert = _get_verify_cert()
    return UserManagerServiceClient.create(
        connection_string=connection_string,
        logger=logger,
        auth_details=_get_auth_details(),
        use_http=_get_use_http(),
        verify_cert=verify_cert
    )


def get_model_test_client(
    connection_string, logger, verify_cert: Union[bool, str] = None
):
    from truera.client.services.model_test_client import ModelTestClient

    connection_string = _get_connection_string(connection_string)
    if verify_cert is None:
        verify_cert = _get_verify_cert()
    return ModelTestClient(
        connection_string=connection_string,
        logger=logger,
        auth_details=_get_auth_details(),
        use_http=_get_use_http(),
        verify_cert=verify_cert
    )


def get_config_service_client(
    connection_string, logger, verify_cert: Union[bool, str] = None
):
    from truera.client.services.configuration_service_client import \
        ConfigurationServiceClient

    connection_string = _get_connection_string(connection_string)
    if verify_cert is None:
        verify_cert = _get_verify_cert()
    return ConfigurationServiceClient(
        connection_string=connection_string,
        auth_details=_get_auth_details(),
        logger=logger,
        use_http=_get_use_http(),
        verify_cert=verify_cert
    )


def get_monitoring_control_plane_client(
    connection_string, logger, verify_cert: Union[bool, str] = None
):
    from truera.client.services.monitoring_control_plane_client import \
        MonitoringControlPlaneClient

    connection_string = _get_connection_string(connection_string)
    if connection_string is None:
        raise click.UsageError(
            "No connection string provided, Please pass or save connection string!"
        )
    use_http = _get_use_http()
    auth_details = _get_auth_details()
    if verify_cert is None:
        verify_cert = _get_verify_cert()
    client = MonitoringControlPlaneClient.create(
        connection_string=connection_string,
        logger=logger,
        auth_details=auth_details,
        use_http=use_http,
        verify_cert=verify_cert
    )
    return client


def validate_file(ctx, param, value):
    if value is None:
        return None
    if not os.path.isfile(value):
        raise click.BadParameter("The provided file does not exist: " + value)
    return value


def validate_directory(ctx, param, value):
    if value is None:
        return None
    if not os.path.isdir(value):
        raise click.BadParameter(
            "The provided directory does not exist: " + value
        )
    return value


def parse_column_schema(ctx, param, column_schema: str) -> List[ColumnDetails]:
    if column_schema == None:
        return

    # Validate that column schema is only specified one way
    if ctx.params.get('columns') != None:
        raise click.BadOptionUsage(
            "column_schema",
            "Unable to handle multiple sources of a column schema. Please use only "
            "one of `column_schema` or `column_schema_path`."
        )

    column_details = []
    for column in column_schema.split(','):
        try:
            column_data = column.strip().split(':')
            if len(column_data) != 2:
                raise click.BadParameter(
                    "Unable to deserialize column schema provided in "
                    "`column_schema` option. Could not separate name "
                    f"and data type in column `{column}`"
                )

            name, data_type = column_data
            column_details.append(
                data_source_utils.column_to_static_column_details(
                    name, data_type
                )
            )
        except InvalidInputDataFormat as e:
            raise click.BadParameter(e.message)

    ctx.params['columns'] = column_details
    return column_schema


def validate_and_load_column_schema_path(
    ctx, param, column_schema_path: str
) -> str:
    if column_schema_path == None:
        return

    if ctx.params.get('columns') != None:
        raise click.BadOptionUsage(
            "column_schema_path",
            "Unable to handle multiple sources of a column schema. Please use only "
            "one of `column_schema` or `column_schema_path`."
        )

    validate_file(ctx, param, column_schema_path)

    try:
        ctx.params['columns'] = data_source_utils.get_column_details_from_file(
            column_schema_path
        )
    except NotSupportedFileTypeException as e:
        raise click.BadParameter(e.message)

    return column_schema_path


def feature_is_active(feature_name):
    context = env.LocalContextStorage.get_cli_env_context()
    return context.get_feature_switch_value(feature_name)


def feature_is_hidden(feature_name):
    return not feature_is_active(feature_name)


CLI_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class ReasonableDefaults():
    artifact_repo_connection_string = 'http://localhost:9291'
    data_service_connection_string = 'http://localhost:9212'

    text_extractor_defaults = {
        "column_delimiter": TextExtractorParams.DEFAULT_COLUMN_DELIMITER,
        "first_row_is_header": TextExtractorParams.DEFAULT_FIRST_ROW_IS_HEADER,
        "quote_character": TextExtractorParams.DEFAULT_QUOTE_CHARACTER,
        "null_value": TextExtractorParams.DEFAULT_NULL_VALUE,
        "empty_value": TextExtractorParams.DEFAULT_EMPTY_VALUE,
        "date_format": TextExtractorParams.DEFAULT_DATE_FORMAT,
        "columns": TextExtractorParams.DEFAULT_COLUMNS
    }


def get_split_max_size():
    return int(env.LocalContextStorage.get_cli_env_context().split_max_size)


def get_build_info():
    build_info_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "BUILDINFO.txt"
    )
    commit = None
    build_time = None
    if os.path.isfile(build_info_path):
        with open(build_info_path) as f:
            commit_line_start = "Commit Id:"
            time_line_start = "Commit Time:"

            for l in f.readlines():
                if l.startswith(commit_line_start):
                    # Only grab first 8 characters of commit hash.
                    commit = l[len(commit_line_start):].strip()[:8]
                if l.startswith(time_line_start):
                    build_time = l[len(time_line_start):].strip()

    cli_version_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "cli_version.txt"
    )
    with open(cli_version_path) as f:
        cli_version = f.read()

    return commit, build_time, cli_version


def format_remaining_list(remaining_list):
    current_type = None
    message = ""
    for remaining in remaining_list:
        if current_type != remaining.type:
            message += f"{remaining.type}:\n"
        message += f"\tname: {remaining.name}, id:{remaining.id}, can be deleted recursively:{remaining.can_be_deleted_via_recursive_flag}\n"

    return message


def format_columns_output(columns, status, error):
    if status == "OK":
        columns_formatted = []

        for column in columns:
            columns_formatted.append(
                {
                    "name":
                        column.name,
                    "type":
                        StaticDataTypeEnum.Name(
                            column.data_type.static_data_type
                        )
                }
            )

        return _format_and_return_json({"columns": columns_formatted})
    elif status == "STARTED":
        return _format_and_return_json({"state": status})
    else:
        output_dict = {"state": status}
        if error or status == "FAILED":
            output_dict["error"] = error
        return _format_and_return_json(output_dict)
