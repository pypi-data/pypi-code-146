import click

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
from truera.client.client_environment import connection_string_message
from truera.client.client_utils import infer_format
from truera.client.client_utils import TextExtractorParams
import truera.client.services.artifact_interaction_client as cl


@click.group(help="Commands for adding data sources.")
def data_source():
    pass


@data_source.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="Create a data source from a file on your machine."
)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--file_path", "--file", callback=cli_utils.validate_file, required=True
)
@click.option(
    "--name",
    "--dsn",
    required=True,
    help="A name that can be used to refer to the data-source later."
)
@click.option(
    "--format",
    type=click.Choice(['infer', 'csv', 'parquet'], case_sensitive=False),
    default='infer'
)
@click.option(
    "--first_row_is_header",
    type=bool,
    default=cli_utils.ReasonableDefaults.
    text_extractor_defaults["first_row_is_header"],
    help=
    f"Option for if the first row is the header. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['first_row_is_header']}."
)
@click.option(
    "--column_delimiter",
    default=cli_utils.ReasonableDefaults.
    text_extractor_defaults["column_delimiter"],
    help=
    f"Delimiter for distinguishing between columns. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['column_delimiter']}."
)
@click.option(
    "--quote_character",
    default=cli_utils.ReasonableDefaults.
    text_extractor_defaults["quote_character"],
    help=
    f"Denotes the start and end of a string. Delimiters within quoted strings are ignored. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['quote_character']}."
)
@click.option(
    "--null_value",
    default=cli_utils.ReasonableDefaults.text_extractor_defaults["null_value"],
    help=
    f"Denotes the value that should be treated as null. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['null_value']}."
)
@click.option(
    "--empty_value",
    default=cli_utils.ReasonableDefaults.text_extractor_defaults["empty_value"],
    help=
    f"Denotes the value that should be treated as the empty string. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['empty_value']}."
)
@click.option(
    "--date_format",
    default=cli_utils.ReasonableDefaults.text_extractor_defaults["date_format"],
    help=
    f"Denotes format of datetimes during extract. The default of 'yyyy-MM-dd HH:mm:ssZZ' is equivalent to pandas date format of '%Y-%m-%d %H:%M:%S%z'. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['date_format']}."
)
@click.option(
    "--column_schema",
    callback=cli_utils.parse_column_schema,
    help=(
        "Column schema that the data source should respect. Formatted "
        "as a comma separated list of columns with the form "
        "<column_name>:<data_type> where `data_type` is a value in the "
        "StaticDataTypeEnum message. Ex. `col_1:STRING,col_2:FLOAT32`"
    )
)
@click.option(
    "--column_schema_path",
    callback=cli_utils.validate_and_load_column_schema_path,
    help=(
        "File system path to a JSON or YAML file containing the column schema "
        "which should be respected by the data source."
    )
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def file(
    project_name,
    file_path,
    name,
    format,
    first_row_is_header,
    column_delimiter,
    quote_character,
    null_value,
    empty_value,
    date_format,
    column_schema,
    column_schema_path,
    connection_string,
    log_level,
    columns=[]
):
    UncaughtExceptionHandler.wrap(
        _upload_data_source_file, project_name, file_path, name, format,
        first_row_is_header, column_delimiter, quote_character, null_value,
        empty_value, date_format, connection_string, log_level, columns
    )


def _upload_data_source_file(
    project_name, file_path, name, format, first_row_is_header,
    column_delimiter, quote_character, null_value, empty_value, date_format,
    connection_string, log_level, columns
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        format = infer_format(format, file_path)
        project_id = client.get_project_id(project_name)
        text_extractor_params = TextExtractorParams(
            format, first_row_is_header, column_delimiter, quote_character,
            null_value, empty_value, date_format, columns
        )
        table_id = client.upload_data_source_file(
            project_id, file_path, name, text_extractor_params
        )

        output_dict = {
            "project_name": project_name,
            "data_source_name": name,
            "table_id": table_id
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@data_source.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="Create a data source from a wasb blob."
)
@click.option("--project_name", "-p", required=True)
@click.option("--uri", required=True)
@click.option(
    '--account_key',
    envvar='WASB_ACCOUNT_KEY',
    prompt=True,
    prompt_required=False,
    hide_input=True
)
@click.option(
    "--data_source_credential_id",
    "--cred_id",
    help="Credential ID of existing credential to use for this connection."
)
@click.option(
    "--name",
    "--dsn",
    required=True,
    help="A name that can be used to refer to the datasource later."
)
@click.option(
    "--format",
    type=click.Choice(['infer', 'csv', 'parquet'], case_sensitive=False),
    default='infer'
)
@click.option(
    "--first_row_is_header",
    type=bool,
    default=cli_utils.ReasonableDefaults.
    text_extractor_defaults["first_row_is_header"],
    help=
    f"Option for if the first row is the header. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['first_row_is_header']}."
)
@click.option(
    "--column_delimiter",
    default=cli_utils.ReasonableDefaults.
    text_extractor_defaults["column_delimiter"],
    help=
    f"Delimiter for distinguishing between columns. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['column_delimiter']}."
)
@click.option(
    "--quote_character",
    default=cli_utils.ReasonableDefaults.
    text_extractor_defaults["quote_character"],
    help=
    f"Denotes the start and end of a string. Delimiters within quoted strings are ignored. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['quote_character']}."
)
@click.option(
    "--null_value",
    default=cli_utils.ReasonableDefaults.text_extractor_defaults["null_value"],
    help=
    f"Denotes the value that should be treated as null. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['null_value']}."
)
@click.option(
    "--empty_value",
    default=cli_utils.ReasonableDefaults.text_extractor_defaults["empty_value"],
    help=
    f"Denotes the value that should be treated as the empty string. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['empty_value']}."
)
@click.option(
    "--date_format",
    default=cli_utils.ReasonableDefaults.text_extractor_defaults["date_format"],
    help=
    f"Denotes format of datetimes during extract. The default of 'yyyy-MM-dd HH:mm:ssZZ' is equivalent to pandas date format of '%Y-%m-%d %H:%M:%S%z'. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['date_format']}."
)
@click.option(
    "--column_schema",
    callback=cli_utils.parse_column_schema,
    help=(
        "Column schema that the data source should respect. Formatted "
        "as a comma separated list of columns with the form "
        "<column_name>:<data_type> where `data_type` is a value in the "
        "StaticDataTypeEnum message. Ex. `col_1:STRING,col_2:FLOAT32`"
    )
)
@click.option(
    "--column_schema_path",
    callback=cli_utils.validate_and_load_column_schema_path,
    help=(
        "File system path to a JSON or YAML file containing the column schema "
        "which should be respected by the data source."
    )
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def wasb(
    project_name,
    uri,
    account_key,
    data_source_credential_id,
    name,
    format,
    first_row_is_header,
    column_delimiter,
    quote_character,
    null_value,
    empty_value,
    date_format,
    column_schema,
    column_schema_path,
    connection_string,
    log_level,
    columns=[]
):
    UncaughtExceptionHandler.wrap(
        _add_wasb_data_source, project_name, uri, account_key,
        data_source_credential_id, name, format, first_row_is_header,
        column_delimiter, quote_character, null_value, empty_value, date_format,
        connection_string, log_level, columns
    )


def _add_wasb_data_source(
    project_name, uri, account_key, data_source_credential_id, name, format,
    first_row_is_header, column_delimiter, quote_character, null_value,
    empty_value, date_format, connection_string, log_level, columns
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        format = infer_format(format, uri)
        project_id = client.get_project_id(project_name)
        text_extractor_params = TextExtractorParams(
            format, first_row_is_header, column_delimiter, quote_character,
            null_value, empty_value, date_format, columns
        )
        table_id = client.add_wasb_data_source(
            project_id, uri, account_key, data_source_credential_id, name,
            text_extractor_params
        )

        output_dict = {
            "project_name": project_name,
            "data_source_name": name,
            "table_id": table_id
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@data_source.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="Create a data source from a s3 bucket."
)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--uri",
    required=True,
    help=
    "Path to a file or folder in s3 which should be read. Folders must contain csv files directly rather than within another subfolder."
)
@click.option(
    "--access_key_id",
    "--id",
    envvar='AWS_ACCESS_KEY',
    help=
    "Access key id with permission to access the bucket. Can also be set via env variable 'AWS_ACCESS_KEY'."
)
@click.option(
    '--secret_access_key',
    prompt=True,
    prompt_required=False,
    hide_input=True,
    envvar='AWS_SECRET_KEY',
    help=
    "Access key secret with permission to access the bucket. Can also be set via env variable 'AWS_SECRET_KEY'."
)
@click.option(
    "--data_source_credential_id",
    "--cred_id",
    help="Credential ID of existing credential to use for this connection."
)
@click.option(
    "--name",
    "--dsn",
    required=True,
    help="A name that can be used to refer to the datasource later."
)
@click.option(
    "--format",
    type=click.Choice(['infer', 'csv', 'parquet'], case_sensitive=False),
    default='infer'
)
@click.option(
    "--first_row_is_header",
    type=bool,
    default=cli_utils.ReasonableDefaults.
    text_extractor_defaults["first_row_is_header"],
    help=
    f"Option for if the first row is the header. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['first_row_is_header']}."
)
@click.option(
    "--column_delimiter",
    default=cli_utils.ReasonableDefaults.
    text_extractor_defaults["column_delimiter"],
    help=
    f"Delimiter for distinguishing between columns. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['column_delimiter']}."
)
@click.option(
    "--quote_character",
    default=cli_utils.ReasonableDefaults.
    text_extractor_defaults["quote_character"],
    help=
    f"Denotes the start and end of a string. Delimiters within quoted strings are ignored. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['quote_character']}."
)
@click.option(
    "--null_value",
    default=cli_utils.ReasonableDefaults.text_extractor_defaults["null_value"],
    help=
    f"Denotes the value that should be treated as null. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['null_value']}."
)
@click.option(
    "--empty_value",
    default=cli_utils.ReasonableDefaults.text_extractor_defaults["empty_value"],
    help=
    f"Denotes the value that should be treated as the empty string. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['empty_value']}."
)
@click.option(
    "--date_format",
    default=cli_utils.ReasonableDefaults.text_extractor_defaults["date_format"],
    help=
    f"Denotes format of datetimes during extract. The default of 'yyyy-MM-dd HH:mm:ssZZ' is equivalent to pandas date format of '%Y-%m-%d %H:%M:%S%z'. Default: {cli_utils.ReasonableDefaults.text_extractor_defaults['date_format']}."
)
@click.option(
    "--column_schema",
    callback=cli_utils.parse_column_schema,
    help=(
        "Column schema that the data source should respect. Formatted "
        "as a comma separated list of columns with the form "
        "<column_name>:<data_type> where `data_type` is a value in the "
        "StaticDataTypeEnum message. Ex. `col_1:STRING,col_2:FLOAT32`"
    )
)
@click.option(
    "--column_schema_path",
    callback=cli_utils.validate_and_load_column_schema_path,
    help=(
        "File system path to a JSON or YAML file containing the column schema "
        "which should be respected by the data source."
    )
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def s3_bucket(
    project_name,
    uri,
    access_key_id,
    secret_access_key,
    data_source_credential_id,
    name,
    format,
    first_row_is_header,
    column_delimiter,
    quote_character,
    null_value,
    empty_value,
    date_format,
    column_schema,
    column_schema_path,
    connection_string,
    log_level,
    columns=[]
):
    UncaughtExceptionHandler.wrap(
        _add_s3_bucket_data_source, project_name, uri, access_key_id,
        secret_access_key, data_source_credential_id, name, format,
        first_row_is_header, column_delimiter, quote_character, null_value,
        empty_value, date_format, connection_string, log_level, columns
    )


def _add_s3_bucket_data_source(
    project_name, uri, access_key_id, secret_access_key,
    data_source_credential_id, name, format, first_row_is_header,
    column_delimiter, quote_character, null_value, empty_value, date_format,
    connection_string, log_level, columns
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        format = infer_format(format, uri)
        project_id = client.get_project_id(project_name)
        text_extractor_params = TextExtractorParams(
            format, first_row_is_header, column_delimiter, quote_character,
            null_value, empty_value, date_format, columns
        )
        table_id = client.add_s3_bucket_data_source(
            project_id, uri, access_key_id, secret_access_key,
            data_source_credential_id, name, text_extractor_params
        )

        output_dict = {
            "project_name": project_name,
            "data_source_name": name,
            "table_id": table_id
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@data_source.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="Create a data source from a mysql database."
)
@click.option("--project_name", "-p", required=True)
@click.option("--uri", required=True)
@click.option("--database_name", required=True)
@click.option("--table_name", required=True)
@click.option("--username", "-u")
@click.option(
    '--password', "--pw", prompt=True, prompt_required=False, hide_input=True
)
@click.option(
    "--data_source_credential_id",
    "--cred_id",
    help="Credential ID of existing credential to use for this connection."
)
@click.option(
    "--name",
    "--dsn",
    required=True,
    help="A name that can be used to refer to the datasource later."
)
@click.option(
    "--column_schema",
    callback=cli_utils.parse_column_schema,
    help=(
        "Column schema that the data source should respect. Formatted "
        "as a comma separated list of columns with the form "
        "<column_name>:<data_type> where `data_type` is a value in the "
        "StaticDataTypeEnum message. Ex. `col_1:STRING,col_2:FLOAT32`"
    )
)
@click.option(
    "--column_schema_path",
    callback=cli_utils.validate_and_load_column_schema_path,
    help=(
        "File system path to a JSON or YAML file containing the column schema "
        "which should be respected by the data source."
    )
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def mysql_db(
    project_name,
    uri,
    database_name,
    table_name,
    username,
    password,
    data_source_credential_id,
    name,
    column_schema,
    column_schema_path,
    connection_string,
    log_level,
    columns=[]
):
    UncaughtExceptionHandler.wrap(
        _add_mysql_data_source, project_name, uri, database_name, table_name,
        username, password, data_source_credential_id, name, connection_string,
        log_level, columns
    )


def _add_mysql_data_source(
    project_name, uri, database_name, table_name, username, password,
    data_source_credential_id, name, connection_string, log_level, columns
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        table_id = client.add_mysql_db_data_source(
            project_id,
            uri,
            database_name,
            table_name,
            username,
            password,
            data_source_credential_id,
            name,
            columns=columns
        )

        output_dict = {
            "project_name": project_name,
            "data_source_name": name,
            "table_id": table_id
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@data_source.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="Create a data source from a bigquery table."
)
@click.option("--project_name", "-p", required=True)
@click.option("--database_name", required=True, help="BigQuery project name")
@click.option(
    "--table_name", required=True, help="BigQuery dataset_name.table_name"
)
@click.option(
    '--password',
    "--pw",
    prompt=True,
    prompt_required=False,
    hide_input=True,
    help=
    "BigQuery Dataset-specific JSON Service Account Key string to use for this connection. https://cloud.google.com/bigquery/docs/authentication/service-account-file"
)
@click.option(
    "--data_source_credential_id",
    "--cred_id",
    help="Credential ID of existing credential to use for this connection."
)
@click.option(
    "--name",
    "--dsn",
    required=True,
    help="A name that can be used to refer to the datasource later."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option(
    "--column_schema",
    callback=cli_utils.parse_column_schema,
    help=(
        "Column schema that the data source should respect. Formatted "
        "as a comma separated list of columns with the form "
        "<column_name>:<data_type> where `data_type` is a value in the "
        "StaticDataTypeEnum message. Ex. `col_1:STRING,col_2:FLOAT32`"
    )
)
@click.option(
    "--column_schema_path",
    callback=cli_utils.validate_and_load_column_schema_path,
    help=(
        "File system path to a JSON or YAML file containing the column schema "
        "which should be respected by the data source."
    )
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def bigquery(
    project_name,
    database_name,
    table_name,
    password,
    data_source_credential_id,
    name,
    column_schema,
    column_schema_path,
    connection_string,
    log_level,
    columns=[]
):
    UncaughtExceptionHandler.wrap(
        _add_bigquery_data_source, project_name, database_name, table_name,
        password, data_source_credential_id, name, connection_string, log_level,
        columns
    )


def _add_bigquery_data_source(
    project_name, database_name, table_name, password,
    data_source_credential_id, name, connection_string, log_level, columns
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        table_id = client.add_bigquery_data_source(
            project_id=project_id,
            database_name=database_name,
            table_name=table_name,
            password=password,
            credential_id=data_source_credential_id,
            name=name,
            columns=columns
        )

        output_dict = {
            "project_name": project_name,
            "data_source_name": name,
            "table_id": table_id
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@data_source.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="Create a data source from a hive warehouse."
)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--uri",
    required=True,
    help="The uri of the HiveServer2 service formatted as host:port."
)
@click.option("--database_name", required=True)
@click.option("--table_name", required=True)
@click.option("--username", "-u")
@click.option(
    '--password', "--pw", prompt=True, prompt_required=False, hide_input=True
)
@click.option(
    "--data_source_credential_id",
    "--cred_id",
    help="Credential ID of existing credential to use for this connection."
)
@click.option(
    "--name",
    "--dsn",
    required=True,
    help="A name that can be used to refer to the datasource later."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def hive(
    project_name, uri, database_name, table_name, username, password,
    data_source_credential_id, name, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _add_hive_data_source, project_name, uri, database_name, table_name,
        username, password, data_source_credential_id, name, connection_string,
        log_level
    )


def _add_hive_data_source(
    project_name, uri, database_name, table_name, username, password,
    data_source_credential_id, name, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        table_id = client.add_hive_data_source(
            project_id, uri, database_name, table_name, username, password,
            data_source_credential_id, name
        )

        output_dict = {
            "project_name": project_name,
            "data_source_name": name,
            "table_id": table_id
        }
        click.echo(cli_utils._format_and_return_json(output_dict))


@data_source.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="Create a data source from a jdbc connection."
)
@click.option("--project_name", "-p", required=True)
@click.option("--uri", required=True)
@click.option("--database_name", required=True)
@click.option("--table_name", required=True)
@click.option("--username", "-u")
@click.option(
    '--password', "--pw", prompt=True, prompt_required=False, hide_input=True
)
@click.option(
    "--data_source_credential_id",
    "--cred_id",
    help="Credential ID of existing credential to use for this connection."
)
@click.option(
    "--name",
    "--dsn",
    required=True,
    help="A name that can be used to refer to the datasource later."
)
@click.option(
    "--column_schema",
    callback=cli_utils.parse_column_schema,
    help=(
        "Column schema that the data source should respect. Formatted "
        "as a comma separated list of columns with the form "
        "<column_name>:<data_type> where `data_type` is a value in the "
        "StaticDataTypeEnum message. Ex. `col_1:STRING,col_2:FLOAT32`"
    )
)
@click.option(
    "--column_schema_path",
    callback=cli_utils.validate_and_load_column_schema_path,
    help=(
        "File system path to a JSON or YAML file containing the column schema "
        "which should be respected by the data source."
    )
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def jdbc(
    project_name,
    uri,
    database_name,
    table_name,
    username,
    password,
    data_source_credential_id,
    name,
    column_schema,
    column_schema_path,
    connection_string,
    log_level,
    columns=[]
):
    UncaughtExceptionHandler.wrap(
        _add_jdbc_data_source, project_name, uri, database_name, table_name,
        username, password, data_source_credential_id, name, connection_string,
        log_level, columns
    )


def _add_jdbc_data_source(
    project_name, uri, database_name, table_name, username, password,
    data_source_credential_id, name, connection_string, log_level, columns
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        table_id = client.add_jdbc_data_source(
            project_id,
            uri,
            database_name,
            table_name,
            username,
            password,
            data_source_credential_id,
            name,
            columns=columns
        )

        output_dict = {
            "project_name": project_name,
            "data_source_name": name,
            "table_id": table_id
        }
        click.echo(cli_utils._format_and_return_json(output_dict))
